import json, sys
p = "/home/theaestheticfur/SillyTavern Presets/Realistic Frankenstein 2.2.1.3 — Limitless Realism/Base/Realistic Frankenstein 2.2.1.3 — Limitless Realism — Basic BOLT Configuration.json"
d = json.load(open(p, encoding='utf-8'))
print(type(d), list(d.keys())[:40])
prompts = d['prompts']
print(len(prompts))
for i, pr in enumerate(prompts):
    print(i, repr(pr.get('identifier'))[:44], '|', pr.get('name'), '|', pr.get('role'), '|', len(pr.get('content') or ''), '| en=', pr.get('enabled'), '| marker=', pr.get('marker'))
