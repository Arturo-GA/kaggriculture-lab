"""Pull the listed public notebooks one by one with retries (Kaggle API), skipping those already on disk.
usage: python pull_public_notebooks.py <folder containing refs.txt (one owner/slug per line)>"""
import sys, time, contextlib, io
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi(); api.authenticate()
FOLDER = Path(sys.argv[1])
refs = [l.strip() for l in (FOLDER / 'refs.txt').read_text().splitlines() if l.strip()]
ok = failed = 0
for ref in refs:
    d = FOLDER / ref.replace('/', '_')
    if list(d.glob('*.ipynb')) or list(d.glob('*.py')):
        ok += 1; continue
    d.mkdir(parents=True, exist_ok=True)
    for attempt in range(4):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                api.kernels_pull(ref, path=str(d), metadata=True, quiet=True)
            ok += 1
            break
        except Exception as e:
            msg = repr(e)[:160]
            time.sleep(5 * (attempt + 1))
    else:
        failed += 1
        print('FAILED', ref, msg, flush=True)
    time.sleep(1.0)
print('ok', ok, 'failed', failed, flush=True)
