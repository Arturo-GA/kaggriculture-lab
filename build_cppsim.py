"""Build the pinned public accelerator on this Windows/MinGW workstation.

Dependency source stays in ignored vendor/cppsim; output stays in outputs/.
Install pybind11==3.0.1 in the project venv before running this script.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig
import pybind11

ROOT = Path(__file__).resolve().parent
REVISION = 'da15925dcf2357d750cbae4bf35712011b4733c8'


def main():
    source = ROOT / 'vendor/cppsim'
    revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    assert revision == REVISION, (revision, REVISION)
    assert not subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True).strip()
    compiler = shutil.which('g++')
    if os.name != 'nt' or not compiler:
        raise RuntimeError('This builder targets Windows with g++; use the upstream build on Linux.')
    out = ROOT / 'outputs/accelerator'
    out.mkdir(parents=True, exist_ok=True)
    target = out / ('kagsim' + sysconfig.get_config_var('EXT_SUFFIX'))
    command = [compiler, '-O3', '-shared', '-std=c++17', '-static-libgcc', '-static-libstdc++',
               '-pthread', '-I' + pybind11.get_include(), '-I' + sysconfig.get_path('include'),
               str(source / 'python/kagsim.cpp'), '-L' + str(Path(sys.base_prefix) / 'libs'),
               '-lpython' + str(sys.version_info.major) + str(sys.version_info.minor), '-o', str(target)]
    subprocess.run(command, check=True)
    record = dict(url='https://github.com/destbreso/kaggriculture-cppsim', revision=revision,
                  compiler=subprocess.check_output([compiler, '--version'], text=True).splitlines()[0],
                  python=sys.version, pybind11=pybind11.__version__,
                  binary_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                  attribution='destbreso; upstream engine port nikital7; Apache-2.0',
                  status='built; equivalence not yet established')
    (ROOT / 'results/cppsim_build.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
