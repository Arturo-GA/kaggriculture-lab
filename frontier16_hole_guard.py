# Compatibility fix for legal empty market slots introduced after the R37 layer.
# Step839 previously called _r37_reorder_sales on these slots, raised IndexError,
# and returned the unchanged action. Preserve that decision explicitly. Do not
# compact the slots: their positions influence lockstep market settlement.
_F16_HOLE_PARENT=_s839_apply
_F16_HOLE_REPORT=dict(f16_preemption_hole_skips=0)


def _s839_apply(obs,action):
    if int(obs.get('step',0))==0:_F16_HOLE_REPORT['f16_preemption_hole_skips']=0
    if any(not order for order in action.get('market',[])):
        _F16_HOLE_REPORT['f16_preemption_hole_skips']+=1
        return action
    return _F16_HOLE_PARENT(obs,action)
