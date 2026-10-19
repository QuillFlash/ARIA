"""Rough global estimate: swap group drafts into an in-memory copy of the snapshot CC and run the frozen checker."""
import json, sys, io, contextlib
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
sys.path.insert(0, S + '/spec/frozen')
import aria_budget as ab
cc = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
files = sys.argv[1:]
by = {p['identifier']: p for p in cc['prompts']}
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    for pid, p in (d.get('prompts') or {}).items():
        if pid in by:
            by[pid]['content'] = p['content']
# Chibi ships Fate and Time & Place OFF
for row in cc['prompt_order'][1]['order']:
    nm = by[row['identifier']].get('name', '')
    if nm.startswith('🎲') or nm.startswith('⏰'):
        row['enabled'] = False
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    totals, errors = ab.analyse_cc(cc)
out = buf.getvalue()
print(out)
print(totals)
print('errors:', errors[:20])
