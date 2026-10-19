import sys, json, io, contextlib
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G5judge')
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
from global_est import build_cc
args = sys.argv[1:]
cc = build_cc(args[0], args[1] if len(args) > 1 else None)
prompts = {p['identifier']: p for p in cc['prompts']}
name = {pid: prompts[pid].get('name', pid) for pid in prompts}
order = cc['prompt_order'][1]['order']
by_prefix = lambda *pre: {pid for pid in prompts if name[pid].startswith(pre)}
patches = by_prefix('🩹')
skip = by_prefix('🌳', '🌿') | {pid for pid in prompts if 'twin' in name[pid]} | {'enhanceDefinitions'} | patches
no_patch = {r['identifier'] for r in order} - skip
def cost(pid):
    r, _ = ab.simulate_cc(cc, no_patch | {pid}, seed=1)
    return sum(ab.tokens(t) for t in r.values())
costs = sorted(((cost(p), name[p]) for p in patches), reverse=True)
for c, n in costs: print(c, n)
largest = max(patches, key=cost)
r, st = ab.simulate_cc(cc, no_patch | {largest}, seed=1)
for pid, t in r.items():
    if name[pid].startswith(('🧠', '🚪')):
        print('=====', name[pid], ab.tokens(t))
        print(t)
