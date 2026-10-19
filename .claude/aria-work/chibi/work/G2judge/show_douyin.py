import json, sys
P = '/home/theaestheticfur/SillyTavern Presets/Realistic Frankenstein 2.2.1.3 — Limitless Realism/Douyin/Realistic Frankenstein 2.2.1.3 Douyin Edition.json'
d = json.load(open(P, encoding='utf-8'))
by = {p['identifier']: p for p in d['prompts']}
order = d['prompt_order'][-1]['order'] if d.get('prompt_order') else []
if len(sys.argv) == 1:
    for p in d['prompts']:
        c = p.get('content') or ''
        print(f"{len(c)//4:5} {p['identifier'][:14]:14} {p.get('name')}")
else:
    for p in d['prompts']:
        if any(x.lower() in (p.get('name') or '').lower() for x in sys.argv[1:]):
            print('=====', p['identifier'], p.get('name'))
            print(p.get('content'))
            print()
