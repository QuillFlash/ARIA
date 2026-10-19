"""Scratch: compare Chibi TC's everything-ON render with Chibi CC's, section by section."""
import json, sys, difflib, re
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
R = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA'
tcp = sys.argv[1]
tc = json.load(open(tcp, encoding='utf-8'))
cc = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json", encoding='utf-8'))

# TC everything ON as the checker computes it
system = tc['sysprompt']['content']
shipped = dict(ab.SWITCH.findall(system))
patches = [s for s in shipped if s.startswith('aria-patch')]
base = {s: 'on' for s in shipped if not s.startswith('aria-patch')} | {p: 'off' for p in patches}
def cost(p):
    a, _ = ab.simulate_tc(tc, base | {p: 'on'}, 1)
    b, _ = ab.simulate_tc(tc, base, 1)
    return sum(ab.tokens(t) for t in a.values()) - sum(ab.tokens(t) for t in b.values())
costs = {p: cost(p) for p in patches}
print('TC patch costs over the all-ON base:', costs)
largest = max(costs, key=costs.get)
allon = base | {largest: 'on'}
r, st = ab.simulate_tc(tc, allon, 1)
for k, v in r.items():
    print(k, len(v), len(v)/4, ab.tokens(v))
open('out/tc_allon_system.txt', 'w').write(r['System Prompt'])
open('out/tc_allon_post.txt', 'w').write(r['Post-History'])

# CC everything ON as the checker computes it
prompts = {p['identifier']: p for p in cc['prompts']}
order = [x['identifier'] for x in cc['prompt_order'][1]['order']]
name = {k: v['name'] for k, v in prompts.items()}
pat = {k for k in prompts if name[k].startswith('🩹')}
skip = {k for k in prompts if name[k].startswith(('🌳', '🌿'))} | {k for k in prompts if 'twin' in name[k]} | {'enhanceDefinitions'} | pat
nop = set(order) - skip
GLM = [k for k in pat if 'GLM' in name[k]][0]
rc, stc = ab.simulate_cc(cc, nop | {GLM}, 1)
sysblock = '\n'.join(t for pid, t in rc.items() if (prompts[pid].get('injection_position') or 0) == 0)
inchat = '\n'.join(t for pid, t in rc.items() if (prompts[pid].get('injection_position') or 0) == 1)
print('CC system block', len(sysblock)/4, 'in-chat', len(inchat)/4)
open('out/cc_allon_system.txt', 'w').write(sysblock)
open('out/cc_allon_inchat.txt', 'w').write(inchat)
