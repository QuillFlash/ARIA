import json, sys
p='/home/theaestheticfur/SillyTavern Presets/Realistic Frankenstein 2.2.1.3 — Limitless Realism/Douyin/Realistic Frankenstein 2.2.1.3 Douyin Edition.json'
d=json.load(open(p,encoding='utf-8'))
ps=d['prompts']
for a in sys.argv[1:]:
    i=int(a)
    x=ps[i]
    print('='*100)
    print(i, x.get('name'), '| role', x.get('role'), '| pos', x.get('injection_position'), '| depth', x.get('injection_depth'))
    print('-'*100)
    print(x.get('content'))
