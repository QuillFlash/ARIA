"""What each Chibi TC switch costs, measured the way the guide's switch table does: flip one switch from the shipped state.
Dependent switches are flipped with their prerequisite(s) on in both renders. Tokens = the checker's metric (sum of rounded parts)
and exact characters / 4 of the whole render. usage: measure_chibi_tc.py CHIBI_TC.json"""
import json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab

tc = json.load(open(sys.argv[1], encoding='utf-8'))
shipped = dict(ab.SWITCH.findall(tc['sysprompt']['content']))


def total(ov):
    r, _ = ab.simulate_tc(tc, ov, seed=1)
    return sum(ab.tokens(t) for t in r.values()), sum(len(t) for t in r.values()) / 4


def delta(sw, extra=None, to=None):
    base = dict(shipped) | (extra or {})
    flipped = dict(base)
    flipped[sw] = to or ('off' if base[sw] == 'on' else 'on')
    a, ca = total(base)
    b, cb = total(flipped)
    return abs(b - a), abs(cb - ca)


print('shipped state, switches ON:', [k for k, v in shipped.items() if v == 'on'], '| total', total(shipped))
rows = {}
for s in shipped:
    extra, note = None, 'from the shipped state'
    if s == 'aria-freaky':
        extra, note = {'aria-adult': 'on'}, 'with aria-adult on'
    elif s == 'aria-jailbreak':
        extra, note = {'aria-adult': 'on'}, 'with aria-adult on (aria-logic-core ships on)'
    rows[s] = (shipped[s], delta(s, extra), note)
    print(f'{s:24} ships {shipped[s]:3} | {rows[s][1][0]:4} tokens (exact {rows[s][1][1]:7.2f}) | {note}')
print()
print('Extra context:')
# Logic Core with tags on / off, and the full-edition style comparisons
for tags in ('on', 'off'):
    t, c = delta('aria-logic-core', {'aria-thinking-tags': tags})
    print(f'  aria-logic-core flip, tags {tags}: {t} tokens (exact {c:.2f})')
# tags: on -> off with the Logic Core on (shipped)
t, c = delta('aria-thinking-tags')
print(f'  aria-thinking-tags flip with the Logic Core on (shipped): {t} (exact {c:.2f})')
# adult and freaky and JB with the Logic Core OFF (no plan lines), for comparison
for label, extra in (('adult, LC off', {'aria-logic-core': 'off'}), ):
    t, c = delta('aria-adult', extra)
    print(f'  aria-adult {label}: {t} (exact {c:.2f})')
for label, extra in (('over adult, LC on', {'aria-adult': 'on'}), ('over adult+freaky, LC on', {'aria-adult': 'on', 'aria-freaky': 'on'})):
    t, c = delta('aria-jailbreak', extra)
    print(f'  aria-jailbreak {label}: {t} (exact {c:.2f})')
# modules that put lines in the plan and the gate: with the Logic Core off, to show the share that is the module alone
for sw in ('aria-fate', 'aria-bonds', 'aria-time-place', 'aria-hybrid-pov', 'aria-character-hold', 'aria-flash-gate'):
    t, c = delta(sw, {'aria-logic-core': 'off'})
    print(f'  {sw} with the Logic Core off: {t} (exact {c:.2f})')
# bonds with fate on, patches
t, c = delta('aria-bonds', {'aria-fate': 'on'})
print(f'  aria-bonds with aria-fate on: {t} (exact {c:.2f})')
for p in ('aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro', 'aria-patch-mimo-flash', 'aria-patch-deepseek'):
    t, c = delta(p)
    print(f'  {p} flip from shipped: {t} (exact {c:.2f})')
t, c = delta('aria-flash-gate', {'aria-patch-glm': 'on'})
print(f'  aria-flash-gate with the GLM patch on: {t} (exact {c:.2f})')
t, c = delta('aria-patch-deepseek', {'aria-fate': 'on', 'aria-bonds': 'on'})
print(f'  aria-patch-deepseek with fate and bonds on (Tally prints): {t} (exact {c:.2f})')
