_ML_PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')

_ML_SHOP_NAMES = ('BAKERY', 'PIZZA_SHOP', 'BRUNCH_SPOT', 'YARN_STORE',
                  'ICE_CREAM_SHOP', 'PET_CAFE', 'SMOOTHIE_SHOP', 'FARMERS_MARKET')

_ML_SPECIES = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'GOOSE', 'COW', 'SHEEP')

def _ml_features(obs, previous_inventory):
    seat = int(obs['player'])
    own, rival = obs['farms'][seat], obs['farms'][1 - seat]
    matching = occupied = 0
    for row_a, row_b in zip(own['tiles'], rival['tiles']):
        for a, b in zip(row_a, row_b):
            a = (a.get('crop'), a.get('animal')) if isinstance(a, dict) else (None, None)
            b = (b.get('crop'), b.get('animal')) if isinstance(b, dict) else (None, None)
            if a != (None, None) or b != (None, None):
                occupied += 1
                matching += a == b
    features = [matching / max(1, occupied), (own['money'] - rival['money']) / 100000]
    for farm in (own, rival):
        tiles = [t for row in farm['tiles'] for t in row if isinstance(t, dict)]
        features += [farm['money'] / 100000, len(farm['hands']) / 20,
                     len(farm['unlocked_quadrants']) / 4,
                     sum(t.get('kind') == 'WEED' for t in tiles) / 100]
        for species in _ML_SPECIES:
            members = [t for t in tiles if t.get('crop') == species or t.get('animal') == species]
            features += [len(members) / 100, sum(t.get('yield_units', 0) for t in members) / 100]
    market = obs['market']
    for item in _ML_PRODUCTS:
        features += [market['prices'][item] / 500,
                     (market['inventory'][item] - 10000) / 1000,
                     (market['inventory'][item] - previous_inventory.get(item, market['inventory'][item])) / 100,
                     obs['private']['shed'].get(item, 0) / 100,
                     sum(inv.get(item, 0) for inv in obs['private']['inventories']) / 100]
    features += [obs['town']['unlocked_shops'].count(shop) / 8 for shop in _ML_SHOP_NAMES]
    return features

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
