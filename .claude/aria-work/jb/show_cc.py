import json, sys
p = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
d = json.load(open(p, encoding='utf-8'))
prompts = d['prompts']
keys = sys.argv[1:]
for k in keys:
    for i, pr in enumerate(prompts):
        ident = pr.get('identifier') or ''
        if ident == k or (len(k) >= 6 and ident.startswith(k)):
            print('=' * 100)
            print('INDEX', i, '| ID', ident, '| NAME', pr.get('name'), '| ROLE', pr.get('role'))
            print('inj_pos', pr.get('injection_position'), 'depth', pr.get('injection_depth'), 'order', pr.get('injection_order'), 'trigger', pr.get('injection_trigger'), 'enabled', pr.get('enabled'), 'sys', pr.get('system_prompt'), 'marker', pr.get('marker'), 'forbid', pr.get('forbid_overrides'))
            print('KEYS:', list(pr.keys()))
            print('-' * 100)
            print(pr.get('content'))
