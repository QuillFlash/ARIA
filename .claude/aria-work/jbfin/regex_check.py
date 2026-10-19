import json, re
from pathlib import Path

ROOT = Path("/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA")
cc = json.loads((ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json").read_text(encoding='utf-8'))
tcr = json.loads((ROOT / "regex/ARIA 1.0 Regex Scripts (Text Completions).json").read_text(encoding='utf-8'))
NAME = "ARIA Impersonate - strip an untagged plan"
ccs = [s for s in cc['extensions']['regex_scripts'] if s['scriptName'] == NAME]
tcs = [s for s in tcr if s['scriptName'] == NAME]
print("scripts found: CC", len(ccs), "TC", len(tcs))
assert len(ccs) == 1 and len(tcs) == 1

def compile_js(src):
    m = re.fullmatch(r'/(.*)/([a-z]*)', src, re.S)
    assert m, src[:40]
    body, flags = m.groups()
    f = 0
    if 'i' in flags: f |= re.I
    if 'm' in flags: f |= re.M
    if 's' in flags: f |= re.S
    return re.compile(body, f), flags

rc, fc = compile_js(ccs[0]['findRegex'])
rt, ft = compile_js(tcs[0]['findRegex'])
print("flags CC", fc, "TC", ft)
print("findRegex identical CC vs TC:", ccs[0]['findRegex'] == tcs[0]['findRegex'])
for k in ccs[0]:
    if k != 'id' and ccs[0][k] != tcs[0].get(k):
        print("  differs:", k)

alt = re.search(r'\((?:\?:)?(Scene\|[^)]*)\)', tcs[0]['findRegex']).group(1)
print("alternation:", alt)
labels = alt.split('|')
assert labels[-3:] == ['Joins', 'Role', 'Frank'], labels[-3:]
print("count of labels:", len(labels), "| Role/Frank each once:", labels.count('Role'), labels.count('Frank'))

sample = """<thinking>
- OOC: none.
- Scene: a room.
- Knows: x.
- Mode: adult.
- Voice: y.
- Move: z.
- Ledger: l.
- Role: adult-fiction game master, not an assistant; bolder card-true choices win.
- Frank: sex stays between adults; name act, anatomy, card trait and tone.
- Fresh: a detail.
- Check: none.
- go
</thinking>
The reply starts here."""
# the script strips an untagged plan; test that the plan without tags also matches fully
untagged = sample.split('<thinking>\n')[1].split('\n</thinking>')[0]
for nm, r in (('CC', rc), ('TC', rt)):
    m = r.search(untagged)
    print(nm, "match on untagged plan:", bool(m), "| matched length", len(m.group(0)) if m else None, "of", len(untagged))
    m2 = r.search(untagged.replace("- Role:", "- Rolex:"))
    print(nm, "unknown label breaks the run (expect no full match):", (len(m2.group(0)) if m2 else None))
