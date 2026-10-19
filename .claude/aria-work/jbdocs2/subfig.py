import json, sys, re
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
ROOT = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/'
tc = json.load(open(ROOT + "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
sw = dict(ab.SWITCH.findall(tc['sysprompt']['content']))
T = lambda o: sum(ab.tokens(t) for t in ab.simulate_tc(tc, o, 1)[0].values())
R = lambda o: ab.simulate_tc(tc, o, 1)
sh = dict(sw)
# Joins line (gate only, LC off)
r, st = R(sh | {'aria-patch-deepseek': 'on'})
print('Joins var chars/4:', len(st.get('ariaPatchJoins', '')) / 4)
print('deepseek shipped delta:', T(sh | {'aria-patch-deepseek': 'on'}) - T(sh))
fg = sh | {'aria-flash-gate': 'on'}
print('deepseek delta with flash-gate on (no Joins, no Runs):', T(fg | {'aria-patch-deepseek': 'on'}) - T(fg))
# Runs line
r, st = R(sh | {'aria-flash-gate': 'on'})
post = r['Post-History']
runs = [l for l in post.split('\n') if 'Runs' in l]
print('Runs lines:', [(l[:60], len(l) / 4) for l in runs])
print('flash-gate shipped delta:', T(sh | {'aria-flash-gate': 'on'}) - T(sh))
# Tally
lc = sh | {'aria-logic-core': 'on'}
def ds_delta(base):
    return T(base | {'aria-patch-deepseek': 'on'}) - T(base | {'aria-patch-deepseek': 'off'})
d0 = ds_delta(lc)
for label, extra in (('Fate', {'aria-fate': 'on'}), ('Bonds', {'aria-bonds': 'on'}), ('both', {'aria-fate': 'on', 'aria-bonds': 'on'})):
    print(f'Tally with {label}: {ds_delta(lc | extra) - d0}')
    r, st = R(lc | extra | {'aria-patch-deepseek': 'on'})
    print('   ariaPatchTally chars/4:', len(st.get('ariaPatchTally', '')) / 4)
