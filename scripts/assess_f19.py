"""Reuse exact job/hash/error checks, with the independent F19 predeclared gate."""
from pathlib import Path
import assess_f18
if __name__=='__main__':
    assess_f18.ROOT=Path('results/frontier19')
    assess_f18.main()
