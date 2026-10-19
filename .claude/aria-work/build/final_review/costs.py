import json, sys, re
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
def T(r): return sum(len(t) for t in r.values()) / 4
for f in [R + "/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"]:
    P = json.load(open(f)); sys_ = P['sysprompt']['content']
    sh = dict(ab.SWITCH.findall(sys_))
    print('===', f[-45:], 'shipped', sh)
    pre = {'aria-freaky': {'aria-adult': 'on'}, 'aria-jailbreak': {'aria-adult': 'on', 'aria-logic-core': 'on'}, 'aria-thinking-tags': {'aria-logic-core': 'on'}, 'aria-flash-gate': {'aria-patch-glm': 'on'}}
    for m in re.finditer(r'\{\{//((?:(?!\}\}).)*)\}\}\s*\{\{\.(aria-[\w-]+) = (on|off)\}\}', sys_, re.S):
        com, s, v = m.group(1), m.group(2), m.group(3)
        base = dict(sh) | pre.get(s, {})
        on = dict(base) | {s: 'on'}; off = dict(base) | {s: 'off'}
        cost = T(ab.simulate_tc(P, on, 1)[0]) - T(ab.simulate_tc(P, off, 1)[0])
        quoted = re.findall(r'(?:about|About|~)\s*([\d,]+)\s*tokens?|([\d,]+) tokens', com)
        q = [a or b for a, b in quoted]
        print(f'  {s:24} {v:3} flip cost {cost:7.2f}  quoted {q}')
P = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"))
prompts = {p['identifier']: p for p in P['prompts']}; nm = {k: v.get('name', '') for k, v in prompts.items()}
order = P['prompt_order'][1]['order']; shipped = {r['identifier'] for r in order if r['enabled']}
byname = {nm[p]: p for p in prompts}
def pid(prefix): return [p for p in prompts if nm[p].startswith(prefix)][0]
pre = {pid('😈'): {pid('🔞')}, pid('🔓'): {pid('🔞')}, pid('🔦'): {pid('🩹 Model Patch: GLM')}}
print('=== ARIA CC')
for r in order:
    p = prompts[r['identifier']]; c = p.get('content') or ''
    m = re.match(r'\{\{//((?:(?!\}\}).)*)\}\}', c, re.S)
    if not m: continue
    q = re.findall(r'(?:about|About|~)\s*([\d,]+)\s*tokens?', m.group(1))
    if not q and 'zero tokens' not in m.group(1): continue
    base = set(shipped) | pre.get(p['identifier'], set())
    on = base | {p['identifier']}; off = base - {p['identifier']}
    cost = T(ab.simulate_cc(P, on, 1)[0]) - T(ab.simulate_cc(P, off, 1)[0])
    print(f"  {nm[p['identifier']][:44]:44} {'on ' if r['enabled'] else 'off'} flip {cost:7.2f} quoted {q or 'zero'}")
