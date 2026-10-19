"""Fix 4: refresh the stale token costs quoted in comments (TC switch comments, CC entry comments). Comments only: raw-text
replacement with asserted counts, then the rendered text of every configuration must be unchanged."""
import json
import random
from rxlib import *

EDITS = {
    TCFILE: [
        ("Great for 24B+ models, costs about 325 tokens a turn.", "Great for 24B+ models, costs about 405 tokens a turn."),
        ("moods and instincts). About 360 tokens.", "moods and instincts). About 350 tokens."),
    ],
    CCFILE: [
        ("Leave this ON; it costs about 300 tokens.", "Leave this ON; it costs about 350 tokens."),
    ],
}


def esc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def comment_spans(s):
    out, i = [], 0
    while i < len(s):
        if s.startswith('{{//', i):
            j = ab.take_macro(s, i)
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


def texts(d, is_tc):
    if is_tc:
        return [d['sysprompt']['content'], d['sysprompt']['post_history']]
    return [p.get('content') or '' for p in d['prompts']]


outs = {}
for path, edits in EDITS.items():
    is_tc = path == TCFILE
    raw = open(path, encoding='utf-8', newline='').read()
    before = json.loads(raw)
    out = raw
    for old, new in edits:
        assert out.count(esc(old)) == 1, (old, out.count(esc(old)))
        out = out.replace(esc(old), esc(new))
    after = json.loads(out)
    assert json.dumps(after, ensure_ascii=False, indent=4) == out, 'format changed'
    # each edit sits wholly inside a {{// ... }} comment of the parsed text
    for old, new in edits:
        hits = 0
        for t in texts(after, is_tc):
            for a, b in comment_spans(t):
                if new in t[a:b]:
                    hits += 1
        assert hits == 1, (new, hits)
        for t in texts(before, is_tc):
            assert t.count(old) in (0, 1)
    # only the intended strings changed anywhere in the structure
    tb, ta = texts(before, is_tc), texts(after, is_tc)
    for x, y in zip(tb, ta):
        for old, new in edits:
            x = x.replace(old, new)
        assert x == y
    outs[path] = out

for path, out in outs.items():
    open(path, 'w', encoding='utf-8', newline='').write(out)
print('Fix 4 applied:', {p.split('/')[-1][-40:]: len(e) for p, e in EDITS.items()})
