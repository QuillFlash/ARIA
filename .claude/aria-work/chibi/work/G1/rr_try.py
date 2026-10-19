import sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
def tok(s):
    r = ab.render(s, {}, random.Random(1)); return ab.tokens(r), len(r)
V = {}
V['a'] = """<reasoning_constraints>
Strictly, while reasoning: one simple plan; skip crafting, drafting, refining and rechecking; then write outside the thinking block at once.
</reasoning_constraints>"""
V['b'] = """<reasoning_constraints>
Strictly: one simple plan, no crafting, drafting, refining or rechecking, then write outside the thinking block at once.
</reasoning_constraints>"""
V['c'] = """<reasoning_constraints>
Strictly follow while reasoning: make one simple plan, skip crafting, drafting, refining and rechecking, then write outside the thinking block at once.
</reasoning_constraints>"""
V['d'] = """<constraints>
Strictly, while reasoning: one simple plan; skip crafting, drafting, refining and rechecking; then write outside the thinking block at once.
</constraints>"""
V['e'] = """<reasoning_constraints>Strictly: one simple plan; skip crafting, drafting, refining and rechecking; then write outside the thinking block at once.</reasoning_constraints>"""
V['f'] = """<reasoning_constraints>
One simple plan; skip crafting, drafting, refining and rechecking; then write outside the thinking block at once.
</reasoning_constraints>"""
for k,v in V.items():
    print(k, tok(v))
