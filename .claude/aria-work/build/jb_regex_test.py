import json, re, sys
live = json.load(open('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/regex/ARIA 1.0 Regex Scripts (Text Completions).json', encoding='utf-8'))
s = [x for x in live if 'strip an untagged plan' in x['scriptName']][0]['findRegex']
m = re.match(r'^/(.*)/([a-z]*)$', s, re.S)
pat, flags = m.group(1), m.group(2)
rx = re.compile(pat, re.I if 'i' in flags else 0)
lines = json.load(open(sys.argv[1], encoding='utf-8'))['lines']
plan = """- OOC: none.
- Scene: a room.
- Knows: x.
- Mode: realism, persona-true.
- Voice: a.
- Move: b.
%s
- Fresh: c.
- Check: d.
- go
Reply text follows here.""" % '\n'.join(lines)
mm = rx.search(plan)
print('matched:', bool(mm))
if mm:
    print('remainder:', repr(plan[mm.end():]))
