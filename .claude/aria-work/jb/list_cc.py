import json
p = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
d = json.load(open(p, encoding='utf-8'))
order = {o['identifier']: o for o in d['prompt_order'][1]['order']}
print([ (po['character_id'], len(po['order'])) for po in d['prompt_order']])
for i, pr in enumerate(d['prompts']):
    o = order.get(pr['identifier'])
    print(i, pr['identifier'][:12], '|', pr.get('name'), '|', pr.get('role'), '| pos', pr.get('injection_position'), 'd', pr.get('injection_depth'), '| len', len(pr.get('content') or ''), '| order-en', (o or {}).get('enabled'))
