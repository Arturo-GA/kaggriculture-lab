"""Verify frozen Frontier3 in Kaggle before emitting its submission archive."""
import hashlib
import json
from pathlib import Path
from build import package
from evaluate import run
from frontier3_validation import assess


def main():
    root=Path('results/frontier3');release=json.loads((root/'release.json').read_text())
    name=release['candidate']
    for n,h in release['source_sha256'].items():
        assert hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest()==h
    rows=run([name,'frontier2_early'],release['cloud_opponents'],release['cloud_seeds'],2,root/'cloud_games.json')
    receipt=assess(root/'cloud_games.json',name)
    receipt.update(total_games=len(rows),leaderboard_submitted=False,kernel=release['kernel'])
    assert release['release_type']=='experimental'
    receipt['release_type']='experimental'
    receipt['local_strategy_gate_passed']=release['local_strategy_gate_passed']
    receipt['export_checks_passed']=receipt['runtime_passed'] and receipt['baseline_comparison_passed']
    if receipt['export_checks_passed']:
        Path('main.py').write_bytes(Path('candidates',name+'.py').read_bytes())
        package(name,'submission.tar.gz')
        receipt['archive_sha256']=hashlib.sha256(Path('submission.tar.gz').read_bytes()).hexdigest()
    (root/'cloud_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)
    assert receipt['export_checks_passed'],'Cloud runtime/baseline checks failed: no archive exported.'


if __name__=='__main__':main()
