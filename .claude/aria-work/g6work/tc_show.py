import json, re, sys
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
TC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
d = json.load(open(TC, encoding='utf-8'))
c = d['sysprompt']['content']
print(len(c))
# print the switch section and block starts
for m in re.finditer(r'\{\{#if \.(aria-[a-z0-9-]+)\}\}', c):
    print(m.start(), m.group(1))
print('--- post_history len', len(d['sysprompt']['post_history']))
print(d.keys())
print(d['sysprompt'].keys())
