# Behavior-neutral final wrapper: expose inherited error counters at season end.
_F16_OBS_PARENT=agent
_F16_OBS_REPORT={}


def agent(observation,configuration=None):
    action=_F16_OBS_PARENT(observation,configuration)
    _F16_OBS_REPORT.clear()
    _F16_OBS_REPORT.update(getattr(_F16_OBS_PARENT,'telemetry',{}))
    if int(observation['step'])==718:
        for name,value in list(globals().items()):
            if name=='_F16_OBS_REPORT' or not name.endswith('_REPORT') or not isinstance(value,dict):continue
            for key,count in value.items():
                if isinstance(count,(int,float)) and ('error' in str(key).lower() or 'fallback' in str(key).lower()):
                    _F16_OBS_REPORT['upstream'+name+'_'+str(key)]=count
    return action


agent.telemetry=_F16_OBS_REPORT
agent=globals().pop('agent')
