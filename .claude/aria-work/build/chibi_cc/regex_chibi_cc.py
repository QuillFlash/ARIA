"""Regex check for Chibi CC: the plan-cleanup scripts (Fix 3 versions, copied unchanged from ARIA CC) on real renders of
Chibi CC's Logic Core (plain and system-role twin), tags on and off, lean and everything on, {{user}} as several names,
echoed templates followed by a reply, through the display, prompt and Impersonate pipelines. ARIA CC's own Logic Core is the baseline:
every (shape, pipeline) pair ARIA CC's scripts clean for ARIA's plan must also be clean for Chibi's.
Also: the untagged-plan strip (script 'ARIA Impersonate - strip an untagged plan') on Chibi plans with Role/Frank, and node vs Python.
"""
import copy, json, re, subprocess, sys, collections
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/build')
from rxlib import R, W, ab, pipeline  # noqa: E402

CHIBI = R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"
ARIA = R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
LC = '15b770cf-6049-5f3b-b25d-be09728a65d5'
TW = '591b8c15-985e-59f1-8c90-59e7cae236ae'
TAGS = '303f26f5-bc2f-5dde-a9e9-aaaacd3eff4b'
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


def load(path):
    return json.load(open(path, encoding='utf-8'))


def enabled_sets(d):
    prompts = {p['identifier']: p for p in d['prompts']}
    name = {k: v['name'] for k, v in prompts.items()}
    order = [r['identifier'] for r in d['prompt_order'][1]['order']]
    patches = {k for k in prompts if name[k].startswith('🩹')}
    skip = {'59602978-fdc0-4a8a-af0a-26b2ec58793b', '8b4cf33f-9fb5-45a0-94ce-9b95478875d7', 'enhanceDefinitions'} | patches
    full = (set(order) - skip - {LC, TW, TAGS}) | {'1f2e1f97-1cde-5d46-8eb0-87e2fe55f916'}   # GLM, the largest patch
    lean = {'main', '0dc06d25-6eaa-4f98-8711-c4456f19e80e', 'f23feaf4-fa91-5bae-8ff7-02cf49c447e0', 'jailbreak',
            '15a8065d-1d77-5db5-9d95-675f4424d44e'}
    return {'lean': lean, 'full': full}


def render_lc(d, user, config, which, tags):
    p = copy.deepcopy(d)
    for x in p['prompts']:
        if x.get('content'):
            x['content'] = x['content'].replace('{{user}}', user)
    en = set(enabled_sets(d)[config]) | {which}
    if tags:
        en.add(TAGS)
    r, _ = ab.simulate_cc(p, en, seed=1)
    return r[which].strip('\n')


def plan_lines(lc):
    lines = lc.split('\n')
    a = next(i for i, l in enumerate(lines) if l.startswith('- OOC:'))
    b = next(i for i, l in enumerate(lines) if l == '- go')
    return '\n'.join(lines[a:b + 1])


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


def cases(d):
    for user in NAMES:
        for tags in (True, False):
            for which, wl in ((LC, 'plain'), (TW, 'twin')):
                for config in ('lean', 'full'):
                    lc = render_lc(d, user, config, which, tags)
                    assert '{{' not in lc
                    for shape, body in shapes(lc, tags).items():
                        for rn, reply in (('reply', REPLY), ('prose reply', REPLY_PROSE)):
                            yield (f"{user[:12]} | tags {'on' if tags else 'off'} | {wl} | {config} | {shape} | {rn}",
                                   shape, body + reply, reply, tags)


chibi, aria = load(CHIBI), load(ARIA)
S_CH = chibi['extensions']['regex_scripts']
S_AR = aria['extensions']['regex_scripts']
check(S_CH == S_AR, 'Chibi CC regex scripts differ from ARIA CC')

base_cov = {}   # (shape, mode, tags) -> ARIA CC's scripts clean ARIA's plan everywhere
for label, shape, text, reply, tags in cases(aria):
    for m, pl, pm in MODES:
        ok, _ = clean(m, pipeline(S_AR, text, pl, pm), reply, tags)
        k = (shape, m, tags)
        base_cov[k] = base_cov.get(k, True) and ok
covered = {k for k, v in base_cov.items() if v}
print('(shape, pipeline, tags) triples ARIA CC cleans for its own plan:', len(covered), 'of', len(base_cov),
      '| not covered by ARIA itself:', sorted(k for k, v in base_cov.items() if not v))

runs = n = 0
sample = []
for label, shape, text, reply, tags in cases(chibi):
    n += 1
    sample.append((label, text))
    for m, pl, pm in MODES:
        out = pipeline(S_CH, text, pl, pm)
        if (shape, m, tags) in covered:
            runs += 1
            ok, bad = clean(m, out, reply, tags)
            check(ok, f'Chibi leaves {bad or "something"} in {m} for: {label}')
print(f'{n} Chibi cases, {runs} required pipeline runs')

# plain replies untouched
for reply in (REPLY, REPLY_PROSE):
    for m, pl, pm in MODES:
        out = pipeline(S_CH, reply, pl, pm)
        check(out.strip() == reply.strip(), f'a plain reply changed in {m}')

# the untagged-plan strip on Chibi plans (Impersonate output with no tag in front), with and without the JB lines
strip = next(s for s in S_CH if s['scriptName'] == 'ARIA Impersonate - strip an untagged plan')
for user in NAMES[:2]:
    for config in ('lean', 'full'):
        lc = render_lc(chibi, user, config, LC, False)
        body = plan_lines(lc)
        msg = "I lean on the doorframe and say nothing for a while, then nod once."
        out = pipeline([strip], body + '\n' + msg, 1, 'save')
        check(out.strip() == msg, f'untagged-plan strip left {out[:80]!r} ({user}, {config})')
        check('Role:' in body or config == 'lean', 'full plan should hold the JB lines only when adult mode is on')
# the full render above has Adult off (no mode set) so JB lines are absent; build one with Adult and JB on
en = set(enabled_sets(chibi)['full']) | {LC}
en |= {'nsfw', '05f6e90d-b30b-48d5-b2bf-26a6e45faffa'}
r, _ = ab.simulate_cc(chibi, en, seed=1)
body = plan_lines(r[LC])
check('- Role:' in body and '- Frank:' in body, 'JB lines missing from the adult plan')
msg = "I lean on the doorframe and say nothing for a while, then nod once."
out = pipeline([strip], body + '\n' + msg, 1, 'save')
check(out.strip() == msg, f'untagged-plan strip left {out[:100]!r} with the JB lines')
print('untagged-plan strip with Role and Frank lines: ' + ('ok' if out.strip() == msg else 'FAILED'))

# node vs python
step = max(1, len(sample) // 120)
pick = sample[::step]
open(W + '/build/chibi_cc/js_payload.json', 'w', encoding='utf-8').write(
    json.dumps({'scripts': S_CH, 'cases': [{'id': i, 'text': t} for i, (l, t) in enumerate(pick)]}, ensure_ascii=False))
res = subprocess.run(['node', W + '/build/js_pipeline.mjs', W + '/build/chibi_cc/js_payload.json'], capture_output=True, text=True)
if res.returncode != 0:
    failures.append('node run failed: ' + res.stderr[:300])
else:
    js = json.loads(res.stdout)
    diffs = 0
    for i, (l, t) in enumerate(pick):
        for m, pl, pm in MODES:
            if pipeline(S_CH, t, pl, pm) != js[str(i)][m]:
                diffs += 1
                failures.append(f'JS and Python differ in {m} for: {l}')
    print(f'JS (node) vs Python: {len(pick)} texts x 3 pipelines, {diffs} differences')

if failures:
    print(f'{len(failures)} FAILURE(S):', dict(collections.Counter(f.split(' for:')[0][:60] for f in failures)))
    for f in failures[:25]:
        print('  -', f)
    sys.exit(1)
print('ALL PASS')
