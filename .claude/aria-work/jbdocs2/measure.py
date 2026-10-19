import json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
ROOT = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/'
cc = json.load(open(ROOT + "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
tc = json.load(open(ROOT + "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
P = {p['identifier']: p for p in cc['prompts']}
name = {pid: P[pid].get('name', pid) for pid in P}
order = cc['prompt_order'][1]['order']
by_prefix = lambda *pre: {pid for pid in P if name[pid].startswith(pre)}
patches = by_prefix('🩹')
skip = by_prefix('🌳', '🌿') | {pid for pid in P if 'twin' in name[pid]} | {'enhanceDefinitions'} | patches
no_patch = {r['identifier'] for r in order} - skip
JB = [pid for pid in P if name[pid].startswith('🔓')][0]
GLM = [pid for pid in patches if 'GLM' in name[pid]][0]
tot = lambda r: sum(ab.tokens(t) for t in r.values())

def cc_total(enabled, imp=False):
    r, st = ab.simulate_cc(cc, enabled, seed=1, impersonate=imp)
    return tot(r), r, st

all_on = no_patch | {GLM}
a, ra, sa = cc_total(all_on)
b, rb, sb = cc_total(all_on - {JB})
print('CC everything ON (GLM):', a, ' without JB:', b, ' JB delta:', a - b)
print('JB lines raw chars/4:', len(sa.get('ariaJb', '')) / 4, ' lines:', sa.get('ariaJbLines'))
print('logicCoreLines with/without JB:', sa.get('logicCoreLines'), sb.get('logicCoreLines'))
# JB with Adult off (Freaky on alone?)
nsfw = 'nsfw'; freaky = [pid for pid in P if name[pid].startswith('😈')][0]
c, rc, sc = cc_total(all_on - {nsfw})
print('CC everything ON minus Adult (Freaky still on): ariaModeLine=', repr(sc.get('ariaModeLine')), ' ariaJb set:', bool(sc.get('ariaJb')))
d, rd, sd = cc_total(all_on - {nsfw, freaky})
print('CC everything ON minus Adult and Freaky: ariaJb set:', bool(sd.get('ariaJb')), ' delta vs no JB:', d - cc_total(all_on - {nsfw, freaky, JB})[0])
# shipped default + Adult + LC + JB delta
shipped = {r['identifier'] for r in order if r['enabled']}
e1 = cc_total(shipped | {nsfw, JB})[0]; e0 = cc_total(shipped | {nsfw})[0]
print('Shipped + Adult: JB delta', e1 - e0)
# LC off: twin off and LC off
LC = [pid for pid in P if name[pid] == '🧠 The Logic Core'][0]
f1 = cc_total((shipped | {nsfw, JB}) - {LC})[0]; f0 = cc_total((shipped | {nsfw}) - {LC})[0]
print('Shipped + Adult, no Logic Core: JB delta', f1 - f0)
# Impersonate
imp_tot = None
r_imp, _ = ab.simulate_cc(cc, all_on, seed=1, impersonate=True)
print('Impersonate: ariaJb printed in LC?', 'Role:' in r_imp.get(LC, ''))

# TC
sw = dict(ab.SWITCH.findall(tc['sysprompt']['content']))
tpatches = [s for s in sw if s.startswith('aria-patch')]
def tc_total(over):
    r, st = ab.simulate_tc(tc, over, seed=1)
    return tot(r), r, st
for patch in tpatches:
    over = {s: 'on' for s in sw if not s.startswith('aria-patch')} | {p: ('on' if p == patch else 'off') for p in tpatches}
    t, r, st = tc_total(over)
    t0, _, _ = tc_total(over | {'aria-jailbreak': 'off'})
    print(f'TC everything ON with {patch}: {t}  (JB delta {t - t0})')
over = {s: 'on' for s in sw if not s.startswith('aria-patch')} | {p: 'off' for p in tpatches}
t, r, st = tc_total(over | {'aria-adult': 'off'})
print('TC all on but aria-adult off (freaky on): ariaModeLine=', repr(st.get('ariaModeLine')), ' JB set:', bool(st.get('ariaJb')))
t, r, st = tc_total(over | {'aria-logic-core': 'off'})
t0, _, _ = tc_total(over | {'aria-logic-core': 'off', 'aria-jailbreak': 'off'})
print('TC all on but logic core off: JB delta', t - t0)
print('TC shipped:', tc_total(sw)[0])
