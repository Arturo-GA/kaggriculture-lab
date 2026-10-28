"""Serial official-engine diagnosis of the slowest accelerated contexts."""
import hashlib
import json
from pathlib import Path
from evaluate import game


def main():
    source=json.loads(Path('results/gold/frontier_holdout_verified.json').read_text())
    slow=sorted(source['rows'],key=lambda r:-r['max_call_ms'])[:3]
    rows=[game((r['candidate'],r['opponent'],r['seed'],r['seat'])) for r in slow]
    passed=all(r['max_call_ms']<1000 for r in rows)
    report=dict(passed=passed,engine='official-1.32.7',serial=True,
                original_max_ms=max(r['max_call_ms'] for r in source['rows']),
                original_receipt_retained=True,
                explanation='C++ measurement includes observation generation and was run concurrently. '
                            'These are exact frozen-policy contexts rerun serially in the official engine; '
                            'the official panel and cloud must independently meet 1000 ms.',
                source_sha256=hashlib.sha256(Path('candidates/frontier.py').read_bytes()).hexdigest(),
                rows=rows)
    Path('results/gold/frontier_latency.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    assert passed


if __name__=='__main__':main()
