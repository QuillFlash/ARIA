import json, sys
p = "/home/theaestheticfur/SillyTavern Presets/Realistic Frankenstein 2.2.1.3 — Limitless Realism/Base/Realistic Frankenstein 2.2.1.3 — Limitless Realism — Basic BOLT Configuration.json"
d = json.load(open(p, encoding='utf-8'))
prompts = d['prompts']
for a in sys.argv[1:]:
    i = int(a)
    pr = prompts[i]
    print('=' * 100)
    print('INDEX', i, '| ID', pr.get('identifier'), '| NAME', pr.get('name'), '| ROLE', pr.get('role'))
    print('inj_pos', pr.get('injection_position'), 'depth', pr.get('injection_depth'), 'order', pr.get('injection_order'), 'trigger', pr.get('injection_trigger'))
    print('-' * 100)
    print(pr.get('content'))
