import json, subprocess, sys, re
f = "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
def main_at(rev, pid='main'):
    raw = subprocess.run(['git', 'show', f'{rev}:{f}'], capture_output=True, cwd='/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA').stdout.decode('utf-8')
    d = json.loads(raw)
    for p in d['prompts']:
        if p['identifier'].startswith(pid):
            return re.sub(r'\{\{//.*?\}\}', '', p['content'], flags=re.S)
for rev in sys.argv[2:]:
    print('=====', rev)
    print(main_at(rev, sys.argv[1]))
