"""Learned option selection; embedded with model weights into a stdlib-only bot."""
_ML_PLAYERS = {}
_ML_OPTIONS = (0, 2, 8, 12, 18)  # 0 retains matched6's adaptive 4/6-turn policy
_ML_REPORT = {}


def _ml_tree_predict(tree, features):
    # sklearn converts inputs to float32 before branching. Match its decisions
    # exactly while keeping the submitted policy independent of numpy/sklearn.
    import struct
    node = 0
    while tree['left'][node] != -1:
        index = tree['feature'][node]
        value = struct.unpack('f', struct.pack('f', features[index]))[0]
        node = tree['left'][node] if value <= tree['threshold'][node] else tree['right'][node]
    return tree['value'][node]


def _ml_choose(features, model):
    predictions = [_ml_tree_predict(t, features) for t in model['trees']]
    scores = [0.0]
    for option in range(1, len(_ML_OPTIONS)):
        values = sorted(row[option] for row in predictions)
        scores.append(values[int(model['quantile'] * (len(values) - 1))])
    best = max(range(len(scores)), key=scores.__getitem__)
    return best if scores[best] > model['threshold'] else 0


def _ml_before(obs, config):
    seat, step = int(obs['player']), int(obs['step'])
    st = _ML_PLAYERS.get(seat)
    if st is None or step <= st['step']:
        st = _ML_PLAYERS[seat] = {'step': -1, 'option': 0, 'features': None, 'inventory_288': {}}
        _ML_REPORT.clear()
        _ML_REPORT.update(ml_option=0, ml_decisions=0, ml_changed_horizons=0, ml_errors=0)
    st['step'] = step
    if step == 288:
        st['inventory_288'] = dict(obs['market']['inventory'])
    if step != 336:
        return
    st['features'] = _ml_features(obs, st['inventory_288'])
    supported = all((config or {}).get(k, v) == v for k, v in
                    [('boardSize', 10), ('episodeSteps', 720), ('turnsPerDay', 24),
                     ('shedCapacity', 100), ('maxMarketOrdersPerTurn', 10)])
    if not supported:
        return
    if _ML_FORCE_OPTION is not None:
        st['option'] = _ML_FORCE_OPTION
    elif _ML_MODEL is not None:
        st['option'] = _ml_choose(st['features'], _ML_MODEL)
    _ML_REPORT.update(ml_option=st['option'], ml_decisions=1)


def _ml_horizon(obs, native):
    st = _ML_PLAYERS.get(int(obs['player']))
    if not st or not st['option']:
        return native
    horizon = _ML_OPTIONS[st['option']]
    _ML_REPORT['ml_changed_horizons'] += int(horizon != native)
    return horizon
