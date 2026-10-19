import json, sys
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
CC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
d = json.load(open(CC, encoding='utf-8'))
for pre in sys.argv[1:]:
    for p in d['prompts']:
        if p['identifier'].startswith(pre):
            print('=' * 100)
            print('ID', p['identifier'], '| NAME', p['name'], '| role', p.get('role'), '| pos', p.get('injection_position'), '| depth', p.get('injection_depth'), '| order', p.get('injection_order'), '| trigger', p.get('injection_trigger'))
            print('-' * 100)
            print(p['content'])
