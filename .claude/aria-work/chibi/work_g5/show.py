import json, sys
S='/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/src/'
cc=json.load(open(S+"Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json",encoding='utf-8'))
for p in cc['prompts']:
    for pre in sys.argv[1:]:
        if p['identifier'].startswith(pre):
            print('='*100)
            print('ID', p['identifier'], '| name:', p.get('name'), '| role:', p.get('role'), '| pos', p.get('injection_position'), '| depth', p.get('injection_depth'), '| order', p.get('injection_order'), '| trigger', p.get('injection_trigger'))
            print('-'*100)
            print(p['content'])
            print('-'*100)
            print('LEN', len(p['content']))
