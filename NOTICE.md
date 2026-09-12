# Attribution and changes

The immutable `baseline/v37.py` is extracted from the user-provided notebook
“Kaggriculture V37 — More Yield, Smarter Labor”, Ahmed Berat Özer, September 12, 2026.
It includes the full Apache License 2.0 and upstream notices, retained verbatim.
See `baseline/notebook_notes.md` for the author's attribution and evaluation claims.

The baseline credits thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
prvsiyan, Dmitrii Gluzdov, lucifer19, leoprovorov and Kaggle contributors,
among others. These credits imply no endorsement of this project.

Modified September 12, 2026 by Arturo-GA / Kaggriculture Lab:

- `candidates/h2.py`, `h6.py`, `h8.py`: replace the four-turn sale-reservation horizon.
- `candidates/pressure.py`: choose 4/6/8 using visible rival yield and price sensitivity.
- `candidates/matched6.py`: use six turns only under persistent public layout similarity.
- `build.py`, `evaluate.py`, tests, research, notebook and packaging: new project tooling.

The project additions are provided under Apache-2.0. All inherited source and
license notices are retained. Public opponent source files are used only locally
for evaluation and are excluded from Git and the exported runtime.
