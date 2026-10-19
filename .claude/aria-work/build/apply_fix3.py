"""Fix 3: the optional closing-sentence group in four plan-cleanup scripts accepts the old and the current sentence.
Raw-text replacement on the JSON-escaped string, with asserted counts; CC and the TC regex file are written only if everything holds."""
import json

R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
CC = R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
RX = R + "/regex/ARIA 1.0 Regex Scripts (Text Completions).json"

OLD = r'(?:[ \t]*When this turn asks for [^\n]{0,300}?Ledger lines\.)?'
NEW = r'(?:[ \t]*(?:When this turn asks for [^\n]{0,300}?Ledger lines|For a message written as [^\n]{0,300}? line)\.)?'
EXPECT = {0: 1, 1: 1, 2: 1, 24: 2}            # script index -> occurrences of the group
TOTAL = sum(EXPECT.values())


def esc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def scripts_of(d, is_cc):
    return d['extensions']['regex_scripts'] if is_cc else d


outs = {}
for path, is_cc in ((CC, True), (RX, False)):
    raw = open(path, encoding='utf-8', newline='').read()
    before = json.loads(raw)
    assert raw.count(esc(OLD)) == TOTAL, (path, raw.count(esc(OLD)))
    assert raw.count(esc(NEW)) == 0
    out = raw.replace(esc(OLD), esc(NEW))
    assert out.count(esc(NEW)) == TOTAL and out.count(esc(OLD)) == 0
    after = json.loads(out)
    assert json.dumps(after, ensure_ascii=False, indent=4) == out, 'format changed'      # four-space indent, no trailing newline
    sb, sa = scripts_of(before, is_cc), scripts_of(after, is_cc)
    assert len(sb) == len(sa) == 31
    for i, (b, a) in enumerate(zip(sb, sa)):
        if i in EXPECT:
            assert b['findRegex'].count(OLD) == EXPECT[i], (i, b['findRegex'].count(OLD))
            assert a['findRegex'] == b['findRegex'].replace(OLD, NEW), i
            assert {k: v for k, v in b.items() if k != 'findRegex'} == {k: v for k, v in a.items() if k != 'findRegex'}, i
        else:
            assert a == b, f'script {i} changed'
    if is_cc:
        rest_b = dict(before); rest_a = dict(after)
        rest_b['extensions'] = {k: v for k, v in before['extensions'].items() if k != 'regex_scripts'}
        rest_a['extensions'] = {k: v for k, v in after['extensions'].items() if k != 'regex_scripts'}
        assert rest_a == rest_b, 'something outside regex_scripts changed'
    outs[path] = (out, sa)

# CC and TC copies identical, all 31 findRegex strings still equal between the two files
cc_scripts, tc_scripts = outs[CC][1], outs[RX][1]
for i in EXPECT:
    assert cc_scripts[i] == tc_scripts[i], f'script {i}: CC and TC copies differ'
assert [s['findRegex'] for s in cc_scripts] == [s['findRegex'] for s in tc_scripts]

for path, (out, _) in outs.items():
    open(path, 'w', encoding='utf-8', newline='').write(out)
print(f'Fix 3 applied: {TOTAL} replacements in each of CC regex_scripts and the TC regex file (scripts {sorted(EXPECT)}: {EXPECT})')
