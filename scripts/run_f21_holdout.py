from evaluate import run
from validate_f21 import ROOT,read,assess

if __name__=='__main__':
    p=read(ROOT/'holdout_plan.json')
    run([p['candidate'],p['control']],p['opponents'],p['seeds'],p['workers'],ROOT/'holdout.json')
    assess()
