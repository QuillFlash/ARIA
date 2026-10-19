import json, sys, subprocess, re
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
from paths import *
REPO = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA'
FILE = "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
d = json.load(open(CC, encoding='utf-8'))
by = {p['identifier']: p for p in d['prompts']}
texts = []
for pid in (CODEX, GATE):
    c = by[pid]['content']
    c = c.split('{{trim}}', 1)[1]
    c = re.sub(r'\{\{[^{}]*\}\}', ' ', c)
    texts.append(c)
clauses = []
for t in texts:
    for line in t.split('\n'):
        line = line.strip()
        if len(line) < 12:
            continue
        for frag in re.split(r';', line):
            frag = frag.strip().rstrip('.')
            if ':' in frag[:14]:
                frag = frag.split(':', 1)[1].strip()
            # json-escape for searching raw file text
            if len(frag) >= 14:
                clauses.append(frag)
seen = set()
for cl in clauses:
    key = json.dumps(cl, ensure_ascii=False)[1:-1]
    key = key[:70]
    if key in seen:
        continue
    seen.add(key)
    out = subprocess.run(['git', '-C', REPO, 'log', '--format=%h %ad %s', '--date=short', '-S' + key, '--', FILE],
                         capture_output=True, text=True).stdout.strip().splitlines()
    first = out[-1] if out else '(not found as a unit)'
    print(f'{first[:110]:110} | {cl[:90]}')
