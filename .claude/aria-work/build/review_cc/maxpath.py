#!/usr/bin/env python3
"""Largest rendered total (checker metric: sum of round(len/4) per entry) over every patch, Flash/Hold/Tags/LC mix,
everything else ON, normal and Impersonate (Impersonate adds the impersonation_prompt setting)."""
import itertools, json, random, sys
sys.path.insert(0, '.')
import ab_snap as ab
import matrix as m
path = sys.argv[1] if len(sys.argv) > 1 else m.CHIBI
d = json.load(open(path, encoding='utf-8'))
name = {p['identifier']: p['name'] for p in d['prompts']}
order = [r['identifier'] for r in d['prompt_order'][1]['order']]
pats = [p for p in order if name[p].startswith('🩹')]
skip = {p for p in order if name[p].startswith(('🌳', '🌿')) or 'twin' in name[p]} | {'enhanceDefinitions', m.LC, m.TW, m.FLASH, m.HOLD, m.TAGS} | set(pats)
base = set(order) - skip
imp_setting = ab.tokens(ab.render(d.get('impersonation_prompt') or '', {}, random.Random(1)))
res = []
for popt in [()] + [(p,) for p in pats] + [(m.AIO, m.GEM38)]:
    for flash, hold, tags, lc, imp in itertools.product((0, 1), (0, 1), (0, 1), (m.LC, m.TW), (0, 1)):
        en = base | set(popt) | {lc} | ({m.FLASH} if flash else set()) | ({m.HOLD} if hold else set()) | ({m.TAGS} if tags else set())
        r, _ = ab.simulate_cc(d, en, seed=1, impersonate=bool(imp))
        tot = sum(ab.tokens(t) for t in r.values()) + (imp_setting if imp else 0)
        res.append((tot, '+'.join(name[p][10:] for p in popt) or 'no patch', flash, hold, tags, 'twin' if lc == m.TW else 'plain', imp))
res.sort(reverse=True)
for x in res[:8]:
    print(x)
print('max', res[0][0])
