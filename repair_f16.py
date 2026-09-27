"""Keep the failed release intact and register the corrected release on fresh seeds."""
import datetime,hashlib,json
from pathlib import Path


def main():
    old=Path('results/frontier16');root=old/'repaired';root.mkdir(exist_ok=True)
    assert not (root/'plan.json').exists(),'Do not overwrite registered validation.'
    plan=json.loads((old/'plan.json').read_text())
    source=Path('candidates/f16_new_both.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()==plan['screen_parent_sha256']
    source+=b'\n'+Path('frontier16_hole_guard.py').read_text(encoding='utf-8').encode()
    source+=b'\n'+Path('frontier16_observability.py').read_text(encoding='utf-8').replace(
        "_F16_OBS_REPORT.update(getattr(_F16_OBS_PARENT,'telemetry',{}))",
        "_F16_OBS_REPORT.update(getattr(_F16_OBS_PARENT,'telemetry',{}))\n    _F16_OBS_REPORT.update(_F16_HOLE_REPORT)").encode()
    compile(source,'f16_repaired','exec');Path('candidates/f16_repaired.py').write_bytes(source)
    failed=json.loads((old/'holdout.json').read_text())
    errors=[dict(seed=r['seed'],opponent=r['opponent'],seat=r['seat'],errors={k:v for k,v in r['telemetry'].items() if ('error' in k or 'fallback' in k) and v}) for r in failed['rows'] if any(v for k,v in r['telemetry'].items() if 'error' in k or 'fallback' in k)]
    (old/'rejection.json').write_text(json.dumps(dict(candidate=plan['candidate'],sha256=plan['hashes'][plan['candidate']],
        validation_stopped=True,completed_games=len(failed['rows']),reason='Swallowed upstream IndexError in step839 for legal empty market slots.',errors=errors),indent=2)+'\n',encoding='utf-8')
    plan['registered_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    plan['candidate']='f16_repaired';plan['hashes']['f16_repaired']=hashlib.sha256(source).hexdigest()
    del plan['hashes']['f16_selected']
    plan['holdout_seeds']=list(range(16301,16309));plan['cloud_seeds']=list(range(16401,16405))
    plan['prior_rejection']='../rejection.json; original plan, candidate and incomplete games preserved.'
    plan['repair']='Explicitly skip step839 on empty-slot lists, preserving the old fallback action and slot positions. Other exceptions remain visible; no gate thresholds relaxed.'
    (root/'plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    (root/'selection.json').write_text(json.dumps(dict(candidate=plan['candidate'],sha256=hashlib.sha256(source).hexdigest()),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(candidate=plan['candidate'],sha256=hashlib.sha256(source).hexdigest()),indent=2))


if __name__=='__main__':main()
