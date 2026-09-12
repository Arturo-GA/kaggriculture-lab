"""Kaggle CPU experiment: screening, untouched holdout, and gated packaging."""
import hashlib
import json
import shutil
import statistics
import subprocess
import sys
from pathlib import Path

import build
from evaluate import run


def launch(args):
    subprocess.run([sys.executable, 'evaluate.py', *args], check=True)


def main():
    manifest = build.build()
    launch(['--candidates','h2','h6','h8','pressure','matched6','--seeds','101','202','303',
            '--workers','2','--output','results/cloud_screen.json'])
    rows = json.loads(Path('results/cloud_screen.json').read_text())['rows']
    scores = {}
    for candidate in ('h2','h6','h8','pressure','matched6'):
        subset = [r for r in rows if r['candidate']==candidate]
        scores[candidate] = [sum(r['win']+.5*r['tie'] for r in subset)/len(subset),
                             statistics.mean(r['margin'] for r in subset)]
    screen_winner = max(scores, key=scores.get)
    # Preselected after the separate local public-opponent panel: this variant
    # preserves V37's results against the different Nagata layout, unlike h6.
    # It still loses some margin vs prvsiyan; release remains experimental.
    selected = 'matched6'
    print('Screen winner:', screen_winner, 'Experimental release:', selected, scores, flush=True)
    # These seeds are never used in screening or to tune the selected candidate.
    launch(['--candidates',selected,'v37','--opponents','v37',
            '--seeds','82001','82002','82003','82004','--workers','2',
            '--output','results/cloud_holdout.json'])
    holdout = json.loads(Path('results/cloud_holdout.json').read_text())['rows']
    selected_rows = [r for r in holdout if r['candidate']==selected]
    controls = [r for r in holdout if r['candidate']=='v37']
    # Weed placement can differ by seat. Swapping labels must reverse the margin;
    # identical policies need not tie on an asymmetric realized farm.
    for seed in {r['seed'] for r in controls}:
        pair = [r for r in controls if r['seed']==seed]
        assert len(pair)==2 and sum(r['margin'] for r in pair)==0, 'Paired self-play failed'
    pass_gate = (sum(r['win'] for r in selected_rows) > len(selected_rows)/2 and
                 statistics.mean(r['margin'] for r in selected_rows)>0 and
                 max(r['max_call_ms'] for r in selected_rows)<1000 and
                 all(not value for r in selected_rows for key,value in r['telemetry'].items()
                     if 'error' in key or 'fallback' in key))
    released = selected if pass_gate else 'v37'
    launch(['--candidates',released,'--opponents','starter', '--seeds','7',
            '--workers','2','--output','results/cloud_smoke.json'])
    smoke = json.loads(Path('results/cloud_smoke.json').read_text())['rows']
    assert all(r['win']==1 for r in smoke)
    build.package(released, 'submission.tar.gz')
    shutil.copyfile('candidates/'+released+'.py','main.py')
    receipt = dict(selected_by_screen=screen_winner,release_candidate=selected,screen_scores=scores,holdout_gate=pass_gate,
                   packaged=released,source_sha256=manifest['candidates'][released],
                   archive_sha256=hashlib.sha256(Path('submission.tar.gz').read_bytes()).hexdigest(),
                   scope='CPU policy search; internal-family validation only; no leaderboard submission',
                   leaderboard_score=None)
    Path('results/cloud_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)


if __name__ == '__main__':
    main()
