"""Verify the frozen learned candidate in Kaggle before exporting its archive."""
import hashlib
import json
from pathlib import Path

from build import package
from evaluate import run


def main():
    release = json.loads(Path('results/ml/release_plan.json').read_text())
    candidate = release['candidate']
    for name, digest in release['source_sha256'].items():
        assert hashlib.sha256(Path('candidates', name+'.py').read_bytes()).hexdigest() == digest
    rows = run([candidate, 'matched6'], ['matched6'], release['cloud_seeds'], 2,
               'results/ml/cloud_games.json')
    controls = {(r['seed'],r['seat']):r for r in rows if r['candidate']=='matched6'}
    selected = [r for r in rows if r['candidate']==candidate]
    wins_delta = sum(r['win']-controls[(r['seed'],r['seat'])]['win'] for r in selected)
    score_delta = sum(r['win']+.5*r['tie']-controls[(r['seed'],r['seat'])]['win']
                      -.5*controls[(r['seed'],r['seat'])]['tie'] for r in selected)
    errors = [(r['seed'],r['seat'],k,v) for r in selected for k,v in r['telemetry'].items()
              if ('error' in k or 'fallback' in k) and v]
    max_ms = max(r['max_call_ms'] for r in selected)
    passed = wins_delta>0 and score_delta>0 and not errors and max_ms<1000
    receipt = dict(passed=passed,candidate=candidate,games=len(rows),
                   candidate_wins=sum(r['win'] for r in selected),
                   candidate_ties=sum(r['tie'] for r in selected),
                   win_delta=wins_delta,score_delta=score_delta,max_call_ms=max_ms,errors=errors,
                   source_sha256=release['source_sha256'][candidate])
    if passed:
        Path('main.py').write_bytes(Path('candidates',candidate+'.py').read_bytes())
        package(candidate,'submission.tar.gz')
        receipt['archive_sha256']=hashlib.sha256(Path('submission.tar.gz').read_bytes()).hexdigest()
    Path('results/ml/cloud_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)
    assert passed, 'Cloud confirmation failed: no submission archive exported'


if __name__=='__main__':
    main()
