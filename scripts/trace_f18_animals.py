"""Read-only replay diagnostic: exact pre-refresh feeding/care and realized animal output."""
import contextlib, importlib, io, json
from pathlib import Path
from audit_f17_replays import audit
from research_top100 import write


def main():
    source=json.loads(Path('results/frontier18/live_accounting.json').read_text(encoding='utf-8'))
    meta=next(r for r in source['rows'] if r['margin']<0)
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original=engine._daily_refresh_animals;calls=[0];rows=[]
    def refresh(farm,day):
        seat=calls[0]%2;calls[0]+=1;before=[]
        for y,tiles in enumerate(farm['tiles']):
            for x,t in enumerate(tiles):
                if isinstance(t,dict) and t.get('animal'):
                    before.append(dict(day=day,seat=seat,x=x,y=y,animal=t['animal'],placed_day=t['placed_day'],
                        fed=t['fed_today'],cared=t['cared_today'],pending=t.get('pending_care_bonus',0),held=t['yield_units']))
        result=original(farm,day)
        for r in before:
            after=farm['tiles'][r['y']][r['x']]
            r['escaped']=not bool(after.get('animal'))
            r['yield_added']=after.get('yield_units',0)-r['held'] if not r['escaped'] else None
            rows.append(r)
        return result
    engine._daily_refresh_animals=refresh
    try:
        out=audit({k:meta[k] for k in ('id','seat','margin','raw_path')})
        assert out['recorded_rewards']==meta['recorded_rewards']
    finally:engine._daily_refresh_animals=original
    write(Path('results/frontier18/animal_trace.json'),dict(episode=meta['id'],reproduced_exactly=True,rows=rows))
    for seat in (0,1):
        sheep=[r for r in rows if r['seat']==seat and r['animal']=='SHEEP']
        print('seat',seat,'sheep_days',len(sheep),'unfed',sum(not r['fed'] for r in sheep),
              'uncared',sum(not r['cared'] for r in sheep),'output',sum(r['yield_added'] or 0 for r in sheep),flush=True)


if __name__=='__main__':main()
