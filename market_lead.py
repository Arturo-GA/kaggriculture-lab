"""Public supply scenario for extending an already guarded sale reservation."""


def _lab_allow_long_lead(obs, item, due, quantity):
    player, step = int(obs['player']), int(obs['step'])
    native_horizon = (6 if 336 <= step < 648 and
                      _R37_PLAYERS[player]['streak'] >= 6 else 4)
    if due <= step + native_horizon:
        return True
    st = _LAB_GATE_STATES.get(player)
    if not st or not st['supported']:
        return False
    samples = [v for t, v in st['samples'][item]]
    if len(samples) < 12:
        return False
    avg = sum(samples) / len(samples)
    sd = _lab_math.sqrt(sum((v - avg) ** 2 for v in samples) / len(samples))
    dt = due - step
    drain = _lab_drain(obs['town']['unlocked_shops'], item, step, due)
    # Mean recent supply is the central scenario. A second, more conservative
    # scenario discounts it by its standard error (not a calibrated CI).
    supply_low = max(0.0, avg - sd / _lab_math.sqrt(len(samples))) * dt
    if supply_low <= drain:
        return False
    inv = obs['market']['inventory'][item]
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for key, patch in obs['market'].get('params', {}).items():
        if key in params:
            params[key].update(patch)
    now = sum(_r37_market_price(item, inv + j, params) for j in range(quantity))
    later = sum(_r37_market_price(item, inv + int(supply_low - drain) + j, params)
                for j in range(quantity))
    _LAB_GATE_REPORT['lead_considered'] = _LAB_GATE_REPORT.get('lead_considered', 0) + 1
    if now - later >= max(6, 0.005 * now):
        _LAB_GATE_REPORT['lead_units'] = _LAB_GATE_REPORT.get('lead_units', 0) + quantity
        return True
    return False
