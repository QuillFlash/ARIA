import json, subprocess, sys, difflib
REPO = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA'
F = "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
ids = {'time': '5dcccd11', 'fate': 'acc2177a', 'bonds': '5506d699'}
which = sys.argv[1]
commits = subprocess.run(['git', '-C', REPO, 'log', '--format=%h %s', '--', F], capture_output=True, text=True).stdout.strip().split('\n')[::-1]
prev = None
for line in commits:
    h, msg = line.split(' ', 1)
    try:
        blob = subprocess.run(['git', '-C', REPO, 'show', f'{h}:{F}'], capture_output=True, text=True, check=True).stdout
        d = json.loads(blob)
    except Exception as e:
        continue
    cont = None
    for p in d.get('prompts', []):
        if p.get('identifier', '').startswith(ids[which]):
            cont = p.get('content'); break
    if cont is None:
        continue
    # strip leading comment
    import re
    body = re.sub(r'^\{\{//[\s\S]*?\}\}\{\{trim\}\}', '', cont)
    if body != prev:
        print(f'################ {h} {msg}')
        if prev is None:
            print(body)
        else:
            a = prev.replace('. ', '.\n').replace('; ', ';\n').split('\n')
            b = body.replace('. ', '.\n').replace('; ', ';\n').split('\n')
            for l in difflib.unified_diff(a, b, lineterm='', n=0):
                if l.startswith(('---', '+++')): continue
                print(l)
        prev = body
