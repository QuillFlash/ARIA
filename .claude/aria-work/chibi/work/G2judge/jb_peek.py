import json, sys
d = json.load(open('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/jb/final.json', encoding='utf-8'))
def walk(x, p=''):
    if isinstance(x, dict):
        for k, v in x.items():
            walk(v, p + '/' + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            walk(v, p + f'[{i}]')
    else:
        s = str(x)
        print(p, '=>', s[:1500])
walk(d)
