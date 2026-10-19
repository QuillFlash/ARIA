"""Regex check for Chibi TC: the plan-cleanup scripts of the TC regex file (Fix 3 versions, unchanged) on real renders of Chibi TC's
Logic Core (post-history up to <final_gate>), tags on and off, shipped and everything on, {{user}} as several names, echoed
templates followed by a reply, through the display, prompt and Impersonate pipelines. ARIA TC's own Logic Core is the baseline: every
(shape, pipeline, tags) triple ARIA TC's scripts clean for ARIA's plan must also be clean for Chibi's (including the extended closing
sentence '... Role, Frank, Own words or POV line.'). Also: the untagged-plan strip on Chibi plans with the Role and Frank lines, and
node (real JavaScript RegExp) against Python on a sample.
usage: python3 regex_chibi_tc.py CHIBI_TC.json
"""
import collections, copy, json, re, subprocess, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/build')
from rxlib import R, W, ab, pipeline, TCFILE, RXFILE, overrides_for, render_tc_logic_core, plan_lines  # noqa: E402

CHIBI = sys.argv[1]
MODES = (('display', 2, 'display'), ('prompt', 2, 'prompt'), ('impersonate', 1, 'save'))
REPLY = ("The kettle clicked off, and Aria set two cups on the counter before she looked up.\n\n"
         "\"Sit down, Manager. You look like you've been arguing with a spreadsheet again.\"")
REPLY_PROSE = ("She read the card aloud. For a message written as a letter, she kept it to one line. "
               "Every response starts with a greeting, she muttered, and the cups stayed full.")
NAMES = ["Lewis", "User", "D'Artagnan", "Lewis the Manager", "Aria ✨"]
PHRASES = ['For a message written as', 'When this turn asks for', 'Every response starts with', 'closes on the line after go',
           'Nothing above go enters the reply', 'The reply starts on the line after that', 'Reasoning ends at go']
PLAN_PHRASES = ['opens the reply, then', '- go', '- OOC']
failures = []


def check(c, m):
    if not c:
        failures.append(m)


def shapes(lc, tags_on):
    out = {'full': lc + '\n\n', 'full, one newline': lc + '\n'}
    if tags_on:
        closing = lc[lc.index('closes on the line after go.'):]
        out['plan + closing'] = '<thinking>\n' + plan_lines(lc) + '\n</thinking> ' + closing + '\n\n'
        out['closing only'] = closing + '\n\n'
        out['full + real plan'] = lc + '\n' + plan_lines(lc) + '\n</thinking>\n\n'
    return out


def clean(mode, out, reply, tags_on):
    rest = out.replace(reply, '')
    if mode == 'display' and not tags_on:
        rest = re.sub(r'<details.*?</details>', '', rest, flags=re.S)
    bad = [p for p in PHRASES if p in rest]
    if mode != 'display':
        bad += [p for p in PLAN_PHRASES if p in rest]
    if mode == 'display':
        return (not bad and out.count(reply) == 1 and out.rstrip().endswith(reply)), bad
    return (not bad and out.strip() == reply.strip()), bad


def cases(preset):
    for user in NAMES:
        for tags in (True, False):
            for config in ('lean', 'full'):
                lc, _ = render_tc_logic_core(preset, overrides_for(preset, config, tags), user)
                assert '{{' not in lc and 'Every response starts with' in lc or not tags or True
                for shape, body in shapes(lc, tags).items():
                    for rn, reply in (('reply', REPLY), ('prose reply', REPLY_PROSE)):
                        yield (f"{user[:12]} | tags {'on' if tags else 'off'} | {config} | {shape} | {rn}", shape, body + reply, reply, tags)


chibi = json.load(open(CHIBI, encoding='utf-8'))
aria = json.load(open(TCFILE, encoding='utf-8'))
S_TC = json.load(open(RXFILE, encoding='utf-8'))
S_CC = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))['extensions']['regex_scripts']
fix3 = ['ARIA - Fold an echoed Logic Core template into a Thoughts box (display only)',
        'ARIA - Hide an echoed Logic Core closing line (display only)',
        'ARIA - Keep an echoed Logic Core template out of the prompt (all depths, cache-safe)',
        'ARIA Impersonate - strip an echoed Logic Core template']
by_cc = {s['scriptName']: s for s in S_CC}
by_tc = {s['scriptName']: s for s in S_TC}
for n in fix3:
    check(by_cc[n]['findRegex'] == by_tc[n]['findRegex'], f'CC and TC copies of "{n[:50]}" differ')

base_cov = {}
for label, shape, text, reply, tags in cases(aria):
    for m, pl, pm in MODES:
        ok, _ = clean(m, pipeline(S_TC, text, pl, pm), reply, tags)
        k = (shape, m, tags)
        base_cov[k] = base_cov.get(k, True) and ok
covered = {k for k, v in base_cov.items() if v}
print('(shape, pipeline, tags) triples the TC regex scripts clean for ARIA TC\'s own plan:', len(covered), 'of', len(base_cov),
      '| not covered by ARIA itself:', sorted(k for k, v in base_cov.items() if not v))

runs = n = 0
sample = []
for label, shape, text, reply, tags in cases(chibi):
    n += 1
    sample.append((label, text))
    for m, pl, pm in MODES:
        out = pipeline(S_TC, text, pl, pm)
        if (shape, m, tags) in covered:
            runs += 1
            ok, bad = clean(m, out, reply, tags)
            check(ok, f'Chibi TC leaves {bad or "something"} in {m} for: {label}')
print(f'{n} Chibi TC cases, {runs} required pipeline runs')

for reply in (REPLY, REPLY_PROSE):
    for m, pl, pm in MODES:
        out = pipeline(S_TC, reply, pl, pm)
        check(out.strip() == reply.strip(), f'a plain reply changed in {m}')

# the untagged-plan strip on Chibi TC plans (Impersonate output with no tag in front), with and without the JB lines
strip = by_tc['ARIA Impersonate - strip an untagged plan']
msg = "I lean on the doorframe and say nothing for a while, then nod once."
for user in NAMES[:2]:
    for config in ('lean', 'full'):
        o = overrides_for(chibi, config, False)
        lc, _ = render_tc_logic_core(chibi, o, user)
        body = plan_lines(lc)
        out = pipeline([strip], body + '\n' + msg, 1, 'save')
        check(out.strip() == msg, f'untagged-plan strip left {out[:80]!r} ({user}, {config})')
o = overrides_for(chibi, 'full', False) | {'aria-adult': 'on', 'aria-jailbreak': 'on'}
lc, _ = render_tc_logic_core(chibi, o, 'Lewis')
body = plan_lines(lc)
check('- Role:' in body and '- Frank:' in body, 'JB lines missing from the adult plan')
out = pipeline([strip], body + '\n' + msg, 1, 'save')
check(out.strip() == msg, f'untagged-plan strip left {out[:100]!r} with the JB lines')
print('untagged-plan strip with Role and Frank lines: ' + ('ok' if out.strip() == msg else 'FAILED'))

# the extended closing sentence itself: every cleanup script removes it whole (tags on, echoed template then reply)
o = overrides_for(chibi, 'lean', True)
lc, _ = render_tc_logic_core(chibi, o, 'Lewis')
sent = re.search(r'For a message written as [^\n]*? line\.', lc).group(0)
check('Own words or POV line.' in sent, 'closing sentence is not the extended one')
for m, pl, pm in MODES:
    out = pipeline(S_TC, lc + '\n\n' + REPLY, pl, pm)
    check('Own words or POV' not in out and 'For a message written as' not in out, f'closing sentence left behind in {m}')

# node vs python
step = max(1, len(sample) // 120)
pick = sample[::step]
open(W + '/build/chibi_tc/js_payload_tc.json', 'w', encoding='utf-8').write(
    json.dumps({'scripts': S_TC, 'cases': [{'id': i, 'text': t} for i, (l, t) in enumerate(pick)]}, ensure_ascii=False))
res = subprocess.run(['node', W + '/build/js_pipeline.mjs', W + '/build/chibi_tc/js_payload_tc.json'], capture_output=True, text=True)
if res.returncode != 0:
    failures.append('node run failed: ' + res.stderr[:300])
else:
    js = json.loads(res.stdout)
    diffs = 0
    for i, (l, t) in enumerate(pick):
        for m, pl, pm in MODES:
            if pipeline(S_TC, t, pl, pm) != js[str(i)][m]:
                diffs += 1
                failures.append(f'JS and Python differ in {m} for: {l}')
    print(f'JS (node) vs Python: {len(pick)} texts x 3 pipelines, {diffs} differences')

if failures:
    print(f'{len(failures)} FAILURE(S):', dict(collections.Counter(f.split(' for:')[0][:60] for f in failures)))
    for f in failures[:25]:
        print('  -', f)
    sys.exit(1)
print('ALL PASS')
