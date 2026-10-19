import json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/jbdocs2/hist/'
for c in ('9c7db79', 'ece78b2', 'a623fe6'):
    tc = json.load(open(W + f'tc_{c}.json', encoding='utf-8'))
    sw = dict(ab.SWITCH.findall(tc['sysprompt']['content']))
    T = lambda o: sum(ab.tokens(t) for t in ab.simulate_tc(tc, o, 1)[0].values())
    sh = dict(sw)
    out = {'LC(as shipped)': T(sh | {'aria-logic-core': 'on'}) - T(sh)}
    for s in ('aria-adult', 'aria-time-place', 'aria-fate', 'aria-character-hold'):
        if s in sw:
            out[s] = (T(sh | {s: 'on'}) - T(sh | {s: 'off'}),
                      T(sh | {'aria-logic-core': 'on', s: 'on'}) - T(sh | {'aria-logic-core': 'on', s: 'off'}))
    print(c, out)
