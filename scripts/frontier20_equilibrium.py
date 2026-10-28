# Original Arturo-GA, Apache-2.0. A bounded mixed strategy for the symmetric
# within-turn order game. This is a local queue model, not a solved game or
# a claim about the opponent's private stock. It avoids choosing an arbitrary
# last member of the best-response cycle used by Market1/Market2.
import hashlib as _f20e_hashlib
import random as _f20e_random
_F20E_PARENT=agent
_F20E_REPORT=dict(f20e_turns=0,f20e_changed=0,f20e_matrix_entries=0,f20e_errors=0,f20e_max_gap=0.)

def _f20e_mix(matrix,iterations=256):
    n=len(matrix);regret=[0.]*n;average=[0.]*n
    scale=max(1.,max(abs(v) for row in matrix for v in row))
    for _ in range(iterations):
        positive=[max(0.,v) for v in regret];total=sum(positive)
        policy=[v/total for v in positive] if total>1e-12 else [1./n]*n
        payoff=[sum(a*b for a,b in zip(row,policy))/scale for row in matrix]
        for i in range(n):regret[i]+=payoff[i];average[i]+=policy[i]
    probability=[v/iterations for v in average]
    gap=max(sum(a*b for a,b in zip(row,probability)) for row in matrix)
    return probability,gap

def _f20e_apply(obs,action):
    step=int(obs['step'])
    if step<216 or _r37_similarity(obs)<.95:return action
    orders=[list(o) for o in action.get('market',[])]
    if not 2<=len(orders)<=10:return action
    stock={p:max(0,int(q)) for p,q in projected_shed(action,FarmView(obs)).items()}
    pool=list(_f19_permutations(orders,stock))
    if len(pool)<2:return action
    # Cover the entire bounded permutation stream rather than only its prefix.
    if len(pool)>32:
        indices=sorted({0,*[round(i*(len(pool)-1)/31) for i in range(32)]})
        pool=[pool[i] for i in indices]
    inventory=dict(obs['market']['inventory']);params=_v44y_params(obs);n=len(pool)
    funcs=[_v44y_factor_margin(p,inventory,stock,params) for p in pool]
    matrix=[[0.]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            value=funcs[j](pool[i]);matrix[i][j]=value;matrix[j][i]=-value
    if not any(v for row in matrix for v in row):return action
    probability,gap=_f20e_mix(matrix)
    _F20E_REPORT['f20e_turns']+=1;_F20E_REPORT['f20e_matrix_entries']+=n*n
    _F20E_REPORT['f20e_max_gap']=max(_F20E_REPORT['f20e_max_gap'],gap)
    # Reproducible private RNG based on legal current observations only. Never
    # consume the simulator's RNG or read future shop draws/configuration seed.
    key=repr((step,int(obs['player']),sorted(inventory.items()),sorted(stock.items()),obs['farms'][int(obs['player'])]['money']))
    seed=int.from_bytes(_f20e_hashlib.blake2b(key.encode(),digest_size=8,person=b'F20Queue').digest(),'big')
    u=_f20e_random.Random(seed).random();chosen=n-1
    for i,p in enumerate(probability):
        u-=p
        if u<=0:chosen=i;break
    if pool[chosen]==orders:return action
    _F20E_REPORT['f20e_changed']+=1
    return dict(action,market=pool[chosen])

_F20E_TELEMETRY={}
def agent(observation,configuration=None):
    if int(observation['step'])==0:
        for k in _F20E_REPORT:_F20E_REPORT[k]=0
    action=_F20E_PARENT(observation,configuration)
    try:
        action=_f20e_apply(observation,action)
        st=_RACE_STATE.get(int(observation['player']))
        if st is not None and st.get('step')==int(observation['step']):st['prev_action']=action
    except Exception:_F20E_REPORT['f20e_errors']+=1
    _F20E_TELEMETRY.clear();_F20E_TELEMETRY.update(getattr(_F20E_PARENT,'telemetry',{}));_F20E_TELEMETRY.update(_F20E_REPORT)
    return action
agent.telemetry=_F20E_TELEMETRY
agent=globals().pop('agent')
