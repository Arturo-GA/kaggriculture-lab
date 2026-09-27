"""Build isolated Frontier16 candidates; never rewrite deployed candidates."""
import hashlib,json
from pathlib import Path

PARENT='f15_e81'
PIN='9f0b05ea0b081134268b281c182b6e3cd1c9298d358e016ea2a8c447014db7eb'
VARIANTS={'f16_queue':(1,.9),'f16_queue3':(3,.9),'f16_queue_all':(1,0.)}
NEW_PARENT='n27_lynnsakurai_031656'
NEW_PIN='03165654e70bd04479a1db776f58146531c320e622db09b9e59ae0a4353c7b82'


def main():
    parent=Path('candidates',PARENT+'.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()==PIN
    layer=Path('frontier16_queue.py').read_text(encoding='utf-8')
    manifest=dict(parent=PARENT,parent_sha256=PIN,variants={})
    for name,(passes,similarity) in VARIANTS.items():
        source=parent.decode()+'\n# Original Frontier16 queue assignment (Arturo-GA, Apache-2.0).\n'
        source+=f'_F16_PASSES={passes!r}\n_F16_SIMILARITY={similarity!r}\n'+layer
        compile(source,name,'exec');data=source.encode()
        Path('candidates',name+'.py').write_bytes(data)
        manifest['variants'][name]=dict(passes=passes,similarity=similarity,sha256=hashlib.sha256(data).hexdigest())
    new_path=Path('candidates',NEW_PARENT+'.py')
    if not new_path.exists():
        # The committed derivative retains the complete byte-exact upstream prefix.
        restored=Path('candidates/f16_repaired.py').read_bytes()[:1148715]
        assert hashlib.sha256(restored).hexdigest()==NEW_PIN
        new_path.write_bytes(restored)
    new=new_path.read_bytes()
    assert hashlib.sha256(new).hexdigest()==NEW_PIN
    manifest['new_parent']=dict(name=NEW_PARENT,sha256=NEW_PIN,license='Apache-2.0; retained NOTICE.txt and all source notices')
    for name,window,queue in [('f16_new_queue',False,True),('f16_new_window',True,False),('f16_new_both',True,True)]:
        source=new.decode()+'\n# Modified by Arturo-GA / Kaggriculture Lab, September 27, 2026. Apache-2.0.\nagent=kaggle_submission_agent\n'
        if window:source+='\n'+Path('frontier16_window.py').read_text(encoding='utf-8')
        if queue:source+='\n_F16_PASSES=1\n_F16_SIMILARITY=0.9\n'+layer
        compile(source,name,'exec');data=source.encode()
        Path('candidates',name+'.py').write_bytes(data)
        manifest['variants'][name]=dict(parent=NEW_PARENT,window=window,queue=queue,sha256=hashlib.sha256(data).hexdigest())
    base=Path('candidates/f16_new_both.py').read_bytes()
    observer=Path('frontier16_observability.py').read_text(encoding='utf-8')
    releases={'f16_selected':base+b'\n'+observer.encode(),
        'f16_repaired':base+b'\n'+Path('frontier16_hole_guard.py').read_text(encoding='utf-8').encode()+b'\n'+observer.replace(
            "_F16_OBS_REPORT.update(getattr(_F16_OBS_PARENT,'telemetry',{}))",
            "_F16_OBS_REPORT.update(getattr(_F16_OBS_PARENT,'telemetry',{}))\n    _F16_OBS_REPORT.update(_F16_HOLE_REPORT)").encode()}
    for name,data in releases.items():
        target=Path('candidates',name+'.py')
        if target.exists():assert target.read_bytes()==data,'Refuse to rewrite a frozen release: '+name
        else:target.write_bytes(data)
        manifest['variants'][name]=dict(parent='f16_new_both',sha256=hashlib.sha256(data).hexdigest())
    Path('results/frontier16/build.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
