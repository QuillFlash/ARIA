import json, sys
p = sys.argv[1]
d = json.load(open(p, encoding='utf-8'))
ids = sys.argv[2:]
for k, v in d.get('prompts', {}).items():
    if not ids or any(k.startswith(x) for x in ids):
        print('=====', k, v.get('name'))
        print(v.get('content'))
        print()
if not ids:
    for k, v in (d.get('tc') or {}).items():
        print('===== TC', k)
        print(v)
        print()
