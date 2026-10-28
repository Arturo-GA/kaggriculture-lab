"""Extract the user-provided V41 as data and freeze a diagnostic comparison."""
import argparse
import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('results/review_v41')
EXPECTED = '8951ff93742015cba535b125223cf2e541bb7b602080fc4584f30c2613d210f3'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook', type=Path)
    args = parser.parse_args()
    notebook = json.loads(args.notebook.read_text(encoding='utf-8'))
    cells = [''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'code']
    source = next(c.split('\n', 1)[1] for c in cells if c.startswith('%%writefile main.py'))
    data = source.replace('\r\n', '\n').encode('utf-8')
    assert digest(data) == EXPECTED
    tree = ast.parse(data)
    base = ast.parse(Path('baseline/v37.py').read_bytes())
    exec_strings = lambda t: [n.args[0].value for n in ast.walk(t)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'exec'
        and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)]
    # Both embedded executable strings are unchanged from the already reviewed V37.
    assert exec_strings(tree) == exec_strings(base)
    imports = set()
    for t in [tree, *map(ast.parse, exec_strings(tree))]:
        for node in ast.walk(t):
            if isinstance(node, ast.Import):
                imports.update(a.name.split('.')[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module.split('.')[0])
    assert imports <= {'__future__', 'copy', 'base64', 'json', 'zlib', 'math', 'itertools', 'time'}
    Path('candidates/v41_review.py').write_bytes(data)
    OUT.mkdir(exist_ok=True)
    receipt = dict(notebook_name=args.notebook.name, notebook_sha256=digest(args.notebook.read_bytes()),
        source_sha256=EXPECTED, source_lines=len(source.splitlines()), imports=sorted(imports),
        inherited_exec_strings_identical=True, notebook_cells_executed=False,
        attribution='Ahmed Berat Ozer and upstream authors; Apache-2.0 notices retained verbatim.',
        reported_rating=2797, rating_provenance='User report, not independently linked to a submission.',
        use='Evaluation only; ignored source, no competition upload.')
    (OUT/'source.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    plan = dict(created_utc=datetime.now(timezone.utc).isoformat(), scope='Diagnostic comparison, no candidate tuning or promotion.',
        candidates=['matched6', 'ml_critic', 'frontier', 'frontier2_early'],
        opponents=['v41_review', 'matched6'], fast_seeds=list(range(91001,91009)),
        official_seeds=list(range(92001,92005)), seats=[0,1],
        measures=['wins/ties/losses', 'paired score versus matched6', 'cash and margin', 'runtime', 'observable failures'],
        live_selection='Latest 8 completed public episodes per each of the four exact submissions. Preserve original audit files.',
        limitations='Ratings are time-dependent and opponents differ. C++ is exploratory; official engine required. Replay actions are not reacting private policies.')
    path = OUT/'plan.json'
    assert not path.exists(), 'Keep the original protocol; do not overwrite it.'
    path.write_text(json.dumps(plan, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
