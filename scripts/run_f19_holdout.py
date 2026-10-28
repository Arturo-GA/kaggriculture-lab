import json
from pathlib import Path
from evaluate import run
def main():
    p=json.loads(Path('results/frontier19/plan.json').read_text(encoding='utf-8'))
    assert not Path('results/frontier19/holdout.json').exists()
    run(p['candidates']+[p['control']],p['opponents'],p['seeds'],5,'results/frontier19/holdout.json')
if __name__=='__main__':main()
