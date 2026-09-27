"""Build bounded original experiments on frozen F17. No upload or submission."""
import hashlib,json
from pathlib import Path

PIN='62b766886208e572462c19f45706cf9d0eded7d048c39a55a6093212bd72426f'


def main():
    parent=Path('candidates/f17_selected.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()==PIN
    variants={
        'f18_calendar':(True,False,12),
        'f18_rotation':(False,True,12),
        'f18_rotation_cautious':(False,True,30),
        'f18_combined':(True,True,12),
    }
    report={}
    for name,(calendar,rotation,premium) in variants.items():
        data=parent+b'\n# Original Arturo-GA experiments, 27 September 2026; Apache-2.0.\n'
        data+=f'_F18_CALENDAR={calendar!r}\n_F18_ROTATION={rotation!r}\n_F18_ROTATION_PREMIUM={premium!r}\n'.encode()
        data+=Path('frontier18_calendar.py').read_bytes();compile(data,name,'exec')
        Path('candidates',name+'.py').write_bytes(data)
        report[name]=dict(sha256=hashlib.sha256(data).hexdigest(),calendar=calendar,rotation=rotation,premium=premium)
    root=Path('results/frontier18');root.mkdir(exist_ok=True)
    (root/'build.json').write_text(json.dumps(dict(parent_sha256=PIN,variants=report),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
