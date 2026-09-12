"""Load only the locally built, pinned accelerator with its verification receipt."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import sysconfig

ROOT = Path(__file__).resolve().parent
_DLL_HANDLES = []


def load(allow_unverified=False):
    folder = ROOT / 'outputs/accelerator'
    binary = folder / ('kagsim' + sysconfig.get_config_var('EXT_SUFFIX'))
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    build = json.loads((ROOT / 'results/cppsim_build.json').read_text())
    if digest != build['binary_sha256']:
        raise RuntimeError('Accelerator binary differs from the recorded build')
    if not allow_unverified:
        verified = json.loads((ROOT / 'results/cppsim_verification.json').read_text())
        if not verified['passed'] or digest != verified['binary_sha256']:
            raise RuntimeError('Run verify_accelerator.py before using this accelerator')
    if os.name == 'nt':
        compiler = shutil.which('g++')
        if compiler:
            _DLL_HANDLES.append(os.add_dll_directory(str(Path(compiler).parent)))
    sys.path.insert(0, str(folder))
    import kagsim
    if Path(kagsim.__file__).resolve() != binary.resolve():
        raise RuntimeError('A different kagsim installation was imported')
    return kagsim
