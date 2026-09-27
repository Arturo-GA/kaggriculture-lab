# Original Arturo-GA deadlock fix, Apache-2.0.
# The inherited rescue assumes every PICKUP WHEAT command makes progress.
# A zero-quantity pickup must not suppress that rescue. Preserve the actual
# physical commands; only remove this false blocker while evaluating rescue.
_F18_FEED_RESCUE_PARENT = _v234_rescue
_F18_FEED_REPORT = dict(f18_feed_zero_requests=0, f18_feed_rescues=0, f18_feed_errors=0)


def _v234_rescue(obs, action, state):
    commands = [action.get('farmer') or ['PASS']] + list(action.get('hands') or [])
    stalled = [i for i, c in enumerate(commands) if len(c) >= 3 and c[:2] == ['PICKUP', 'WHEAT'] and int(c[2]) == 0]
    if not stalled:
        return _F18_FEED_RESCUE_PARENT(obs, action, state)
    _F18_FEED_REPORT['f18_feed_zero_requests'] += 1
    masked = [list(c) for c in commands]
    for i in stalled:
        masked[i] = ['PASS']
    probe = dict(action, farmer=masked[0], hands=masked[1:])
    result = _F18_FEED_RESCUE_PARENT(obs, probe, state)
    if result.get('market', []) == action.get('market', []):
        return action
    _F18_FEED_REPORT['f18_feed_rescues'] += 1
    return dict(action, market=result['market'])


_F18_FEED_PARENT = agent
_F18_FEED_TELEMETRY = {}


def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for k in _F18_FEED_REPORT:
            _F18_FEED_REPORT[k] = 0
    action = _F18_FEED_PARENT(observation, configuration)
    _F18_FEED_TELEMETRY.clear()
    _F18_FEED_TELEMETRY.update(getattr(_F18_FEED_PARENT, 'telemetry', {}))
    _F18_FEED_TELEMETRY.update(_F18_FEED_REPORT)
    return action


agent.telemetry = _F18_FEED_TELEMETRY
agent = globals().pop('agent')
