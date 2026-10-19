import json, sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
ROOT = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/'
cc = json.load(open(ROOT + "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
P = {p['identifier']: p for p in cc['prompts']}
name = {pid: P[pid].get('name', pid) for pid in P}
order = cc['prompt_order'][1]['order']
by_prefix = lambda *pre: {pid for pid in P if name[pid].startswith(pre)}
patches = by_prefix('🩹')
skip = by_prefix('🌳', '🌿') | {pid for pid in P if 'twin' in name[pid]} | {'enhanceDefinitions'} | patches
GLM = [pid for pid in patches if 'GLM' in name[pid]][0]
all_on = ({r['identifier'] for r in order} - skip) | {GLM}
n, sn = ab.simulate_cc(cc, all_on, 1)
i, si = ab.simulate_cc(cc, all_on, 1, impersonate=True)
imp_setting = ab.tokens(ab.render(cc.get('impersonation_prompt') or '', {}, random.Random(1)))
print('impersonation_prompt setting:', imp_setting)
for pid in set(n) | set(i):
    a = ab.tokens(n.get(pid, '')); b = ab.tokens(i.get(pid, ''))
    if a != b:
        print(f'{b - a:+5}  {name[pid]}  (normal {a}, impersonate {b})', '' if pid in i else '[skipped on Impersonate, checker adds it back]')
for v in ('ariaFateLine', 'ariaBondsLine', 'ariaLedgerLine', 'ariaLedgerGate', 'ariaDice', 'ariaPovGate', 'ariaEchoGate', 'ariaHoldLine', 'ariaHoldGate', 'ariaJb', 'ariaPatchTally'):
    print(f'  {v:16} normal {len(sn.get(v, "")) / 4:6.1f}  impersonate {len(si.get(v, "")) / 4:6.1f}')
