"""Read public notebook artifacts, preserving metadata; never execute their cells."""
from pathlib import Path
import json
from research_top100 import api,limited

REFS=[
 'leoprovorov/a-song-of-ice-and-fire-fixed-flexible',
 'evgendvorkin/kaggriculture-version-31-26-09-bronze-going-up',
 'lynnsakurai/farmer-john-and-the-wheat-seller',
 'flexonafft/kaggriculture-multi-route-farming-agent',
 'georgymamarin/kaggriculture-what-2600-farms-do-differently',
 'leoprovorov/god-s-mode-hacked-stores',
 'tetsutani/demand-preserving-turn-sale-timing',
]
def main():
    client=api()
    for ref in REFS:
        folder=Path('vendor/f19_public',ref.replace('/','_'));folder.mkdir(parents=True,exist_ok=True)
        if not list(folder.glob('*.ipynb')):limited(client.kernels_pull,ref,path=str(folder),metadata=True,quiet=True)
        nb=next(folder.glob('*.ipynb'));cells=json.loads(nb.read_text(encoding='utf-8'))['cells']
        print(ref,[(c['cell_type'],len(''.join(c['source'])),''.join(c['source'])[:180]) for c in cells],flush=True)
if __name__=='__main__':main()
