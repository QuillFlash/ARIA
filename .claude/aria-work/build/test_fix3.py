"""Fix 3 test: the plan-cleanup regex scripts on real renders of the Logic Core (ARIA TC, Chibi TC, historic old text), with
{{user}} rendered as a name, tags on and off, as an echoed template followed by a reply.

OLD = the snapshot's scripts (before Fix 3), NEW = the live files. Exit code 0 only when every NEW assertion holds:
  1. new-style echoes (tags on): wherever OLD scripts clean an old-style echo of the same shape, NEW scripts must clean the new-style one
     completely (the "For a message written as ... line." sentence and the "Every response starts with" line gone, reply whole);
  2. old-style echoes (the real pre-beta-7 render and the current text with the old sentence): NEW output == OLD output, character for character;
  3. tags off: NEW output == OLD output and clean;
  4. a plain reply, and a reply that merely contains the phrases, is never changed;
  5. CC's scripts and the TC regex file's scripts behave identically;
  6. node (real JavaScript) gives the same output as Python on a sample.
usage: python3 test_fix3.py
"""
import json
import re
import subprocess
import sys

from rxlib import *

OLD_SCRIPTS_CC = json.load(open(SNAP_CC, encoding='utf-8'))['extensions']['regex_scripts']
OLD_SCRIPTS_TC = json.load(open(SNAP_RX, encoding='utf-8'))
NEW_SCRIPTS_CC = json.load(open(CCFILE, encoding='utf-8'))['extensions']['regex_scripts']
NEW_SCRIPTS_TC = json.load(open(RXFILE, encoding='utf-8'))

REPLY = ("The kettle clicked off, and Aria set two cups on the counter before she looked up.\n\n"
         "\"Sit down, Manager. You look like you've been arguing with a spreadsheet again.\"")
REPLY_PROSE = ("She read the card aloud. For a message written as a letter, she kept it to one line. "
               "Every response starts with a greeting, she muttered, and the cups stayed full.")
NAMES = ["Lewis", "User", "Lewis the Manager", "D'Artagnan", "Aria ✨", "Dr. Elena Marchetti-Vasquez of the Westerbrook Line",
         "Lewis " + "X" * 60]
MODES = (('display', 2, 'display'), ('prompt', 2, 'prompt'), ('impersonate', 1, 'save'))

PHRASES = ['For a message written as', 'When this turn asks for', 'Every response starts with', 'closes on the line after go',
           'Nothing above go enters the reply', 'The reply starts on the line after that', 'Reasoning ends at go']
PLAN_PHRASES = ['opens the reply, then', '- go', '- OOC']

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
    return cond


def shapes(lc, tags_on):
    """Echo shapes. Tags on: the full echoed template; the template with one newline before the reply; a real plan followed by the
    echoed closing lines; the closing lines alone; the template followed by a real plan. Tags off: the <logic_core> block."""
    out = {'full': lc + '\n\n', 'full, one newline': lc + '\n'}
    if tags_on:
        closing = lc[lc.index('closes on the line after go.'):]
        out['plan + closing'] = '<thinking>\n' + plan_lines(lc) + '\n</thinking> ' + closing + '\n\n'
        out['closing only'] = closing + '\n\n'
        out['full + real plan'] = lc + '\n' + plan_lines(lc) + '\n</thinking>\n\n'
    return out


def run_all(cc_scripts, tc_scripts, text):
    return {side: {m: pipeline(sc, text, pl, pm) for m, pl, pm in MODES} for side, sc in (('cc', cc_scripts), ('tc', tc_scripts))}


def clean(mode, out, reply, tags_on=True):
    """Nothing of the template is left and the reply is whole. The reply's own text is not searched (a reply may contain the phrases).
    Tags off, display: the generic fold script wraps the whole <logic_core> block into a Thoughts box, so its text may sit inside a box."""
    rest = out.replace(reply, '')
    if mode == 'display' and not tags_on:
        rest = re.sub(r'<details.*?</details>', '', rest, flags=re.S)
    bad = [p for p in PHRASES if p in rest]
    if mode != 'display':
        bad += [p for p in PLAN_PHRASES if p in rest]
    if mode == 'display':
        return (not bad and out.count(reply) == 1 and out.rstrip().endswith(reply)), bad
    return (not bad and out.strip() == reply.strip()), bad


# ------------------------------------------------------------------ the cases
cases = []   # (label, shape, text, reply, kind, tags_on)
tc = tc_preset()
old_tc_preset = json.load(open(OLD_TC, encoding='utf-8'))
g3 = g3_text()
for name in NAMES:
    for tags in (True, False):
        for config in ('lean', 'full'):
            o = overrides_for(tc, config, tags)
            lc, state = render_tc_logic_core(tc, o, name)
            chibi = render_chibi_logic_core(g3, state, name)
            sources = [('new', 'ARIA TC', lc), ('new', 'Chibi TC', chibi)]
            if tags:
                new_sentence = re.search(r'For a message written as [^\n]*? line\.', lc).group(0)
                assert lc.count(new_sentence) == 1
                old_sentence = f"When this turn asks for {name}'s own message, plan {name}'s move only and skip the Fate, Bonds and Ledger lines."
                sources.append(('old', 'ARIA TC with the old sentence', lc.replace(new_sentence, old_sentence)))
                hist, _ = render_tc_logic_core(old_tc_preset, overrides_for(old_tc_preset, config, tags), name)
                sources.append(('old', 'pre-beta-7 TC render', hist))
            for kind, label, text in sources:
                assert ('For a message written as' in text) == (kind == 'new') and ('When this turn asks for' in text) == (kind == 'old'), label
                assert '{{' not in text, label
                for shape, body in shapes(text, tags).items():
                    for rname, reply in (('reply', REPLY), ('prose reply', REPLY_PROSE)):
                        cases.append((f"{label} | {name[:14]} | tags {'on' if tags else 'off'} | {config} | {shape} | {rname}",
                                      shape, body + reply, reply, kind, tags))
print(f'{len(cases)} cases (names x tags x lean/full x echo shapes x replies; ARIA TC, Chibi TC, two old-style sources)')

results = []
for label, shape, text, reply, kind, tags in cases:
    results.append((label, shape, text, reply, kind, tags,
                    run_all(OLD_SCRIPTS_CC, OLD_SCRIPTS_TC, text), run_all(NEW_SCRIPTS_CC, NEW_SCRIPTS_TC, text)))

# ------------------------------------------------------------------ baseline: which (shape, mode) do the OLD scripts clean for OLD-style echoes?
baseline = {}
for label, shape, text, reply, kind, tags, old, new in results:
    if kind == 'old':
        for m, _, _ in MODES:
            ok, _ = clean(m, old['tc'][m], reply, tags)
            baseline[(shape, m)] = baseline.get((shape, m), True) and ok
covered = {k for k, v in baseline.items() if v}
uncovered = sorted(k for k, v in baseline.items() if not v)
print('shape/mode pairs the OLD scripts already clean for old-style echoes:', len(covered), '| not covered even before Fix 3:', uncovered)

# ------------------------------------------------------------------ assertions
old_style_runs = tags_off_runs = new_style_runs = 0
for label, shape, text, reply, kind, tags, old, new in results:
    for m, _, _ in MODES:
        check(new['cc'][m] == new['tc'][m], f'CC and TC scripts differ in {m} for: {label}')
        if kind == 'old':
            old_style_runs += 1
            check(new['tc'][m] == old['tc'][m], f'old-style echo: NEW output differs from OLD in {m} for: {label}')
        elif not tags:
            tags_off_runs += 1
            ok, bad = clean(m, new['tc'][m], reply, tags)
            check(ok, f'tags off: NEW leaves {bad or "something"} in {m} for: {label}')
            check(new['tc'][m] == old['tc'][m], f'tags off: Fix 3 changed the result in {m} for: {label}')
        elif (shape, m) in covered:
            new_style_runs += 1
            ok, bad = clean(m, new['tc'][m], reply, tags)
            check(ok, f'new-style echo: NEW leaves {bad or "something"} in {m} for: {label}')

print(f'checked: {new_style_runs} new-style (tags on) pipeline runs must be clean, {old_style_runs} old-style runs must equal OLD, '
      f'{tags_off_runs} tags-off runs must be unchanged and clean')

# the bug, for the report: OLD scripts on new-style tags-on echoes
leave = total = 0
for label, shape, text, reply, kind, tags, old, new in results:
    if kind == 'new' and tags and (shape, 'prompt') in covered:
        total += 1
        leave += any('For a message written as' in old['tc'][m] for m, _, _ in MODES)
print(f'OLD scripts leave the "For a message written as" sentence behind in {leave} of {total} tags-on new-style cases whose shape they handle for old echoes')

# ------------------------------------------------------------------ plain replies are never touched
for reply in (REPLY, REPLY_PROSE):
    for m, pl, pm in MODES:
        out = pipeline(NEW_SCRIPTS_TC, reply, pl, pm)
        check(out.strip() == reply.strip(), f'a plain reply was changed in {m}: {out[:80]!r}')

# ------------------------------------------------------------------ the longest {{user}} name the new group still reaches
o = overrides_for(tc, 'full', True)
longest = 0
for n in range(1, 200):
    lc, _ = render_tc_logic_core(tc, o, 'N' * n)
    if pipeline(NEW_SCRIPTS_TC, lc + '\n\n' + REPLY, 2, 'prompt').strip() == REPLY.strip():
        longest = n
print(f'longest single-word {{user}} name the NEW scripts still clean (ARIA TC, everything on, tags on): {longest} characters')
check(longest >= 60, f'name bound too short: {longest}')

# ------------------------------------------------------------------ JS differential
sample = [(l, t) for l, s, t, r, k, g, o_, n_ in results][::max(1, len(results) // 150)]
open(W + '/build/js_payload.json', 'w', encoding='utf-8').write(
    json.dumps({'scripts': NEW_SCRIPTS_TC, 'cases': [{'id': i, 'text': t} for i, (l, t) in enumerate(sample)]}, ensure_ascii=False))
res = subprocess.run(['node', W + '/build/js_pipeline.mjs', W + '/build/js_payload.json'], capture_output=True, text=True)
if res.returncode != 0:
    failures.append('node run failed: ' + res.stderr[:300])
else:
    js = json.loads(res.stdout)
    diffs = 0
    for i, (l, t) in enumerate(sample):
        for m, pl, pm in MODES:
            if pipeline(NEW_SCRIPTS_TC, t, pl, pm) != js[str(i)][m]:
                diffs += 1
                failures.append(f'JS and Python differ in {m} for: {l}')
    node_v = subprocess.run(['node', '--version'], capture_output=True, text=True).stdout.strip()
    print(f'JS (node {node_v}) vs Python: {len(sample)} texts x 3 pipelines, {diffs} differences')

print()
if failures:
    import collections
    print(f'{len(failures)} FAILURE(S) by kind:', dict(collections.Counter(f.split(' for:')[0].split(' in ')[0][:48] for f in failures)))
    for f in failures[:30]:
        print('  -', f)
    if len(failures) > 30:
        print(f'  ... and {len(failures) - 30} more')
    sys.exit(1)
print(f'ALL PASS ({len(results)} cases)')
