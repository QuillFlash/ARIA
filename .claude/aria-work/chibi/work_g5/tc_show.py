import json, re, sys
S='/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/src/'
tc=json.load(open(S+"Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json",encoding='utf-8'))
sp=tc['sysprompt']['content']
print('keys', list(tc.keys()), list(tc['sysprompt'].keys()))
print('len sysprompt.content', len(sp))
# find blocks
for key in sys.argv[1:]:
    for m in re.finditer(re.escape(key), sp):
        print('FOUND', key, 'at', m.start())
