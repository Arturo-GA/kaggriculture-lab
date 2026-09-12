"""Additional funding check for the second market gate experiment, Apache-2.0."""


def _lab_gate_funded(obs, action, tape, due):
    farm = obs['farms'][int(obs['player'])]
    hires = int(farm['hires_today'])
    land = len(farm['unlocked_quadrants']) - 1
    budget = 0
    prices = obs['market']['prices']
    for t in range(int(obs['step']), due + 1):
        for order in (action if t == int(obs['step']) else tape[t]).get('market', []):
            if not order or order[0] == 'SELL':
                continue
            if order[0] == 'HIRE':
                a, b = 1, 1
                for _ in range(hires):
                    a, b = b, a + b
                budget += a
                hires += 1
            elif order[0] == 'BUY_LAND':
                if land < 3:
                    budget += (1000, 2000, 4000)[land]
                    land += 1
            elif len(order) < 3:
                return False
            elif order[0] == 'BUY_SEED':
                budget += max(0, int(order[2])) * {
                    'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}[order[1]]
            elif order[0] == 'BUY_ANIMAL':
                budget += max(0, int(order[2])) * {'GOOSE': 300, 'COW': 400, 'SHEEP': 500}[order[1]]
            elif order[0] == 'BUY_PRODUCT':
                budget += max(0, int(order[2])) * (int(prices[order[1]] * 1.25) + 10)
            else:
                return False
    # All planned spending is reserved without counting any prospective sale.
    # The product-price buffer is a scenario, not a global upper bound.
    return farm['money'] >= budget + 12000
