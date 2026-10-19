"""Frozen checker on in-memory copies of the snapshot CC and TC with a G3 file (and optionally the G1/G2 finals)
swapped in, plus a stand-in JB wired per JB.md. Nothing is written outside this folder.

usage: python3 checker_test.py G3.json [--with-g1g2]
"""
import contextlib, copy, io, json, random, sys, uuid
S = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work"
sys.path.insert(0, S + "/spec/frozen")
import aria_budget as ab

g3 = json.load(open(sys.argv[1], encoding='utf-8'))
with_g1g2 = '--with-g1g2' in sys.argv
jb = json.load(open(S + "/jb/final.json", encoding='utf-8'))
LINES = '\n'.join(jb['lines'])
N = len(jb['lines'])

# ---------------- CC
cc = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
by = {p['identifier']: p for p in cc['prompts']}
groups = [g3]
if with_g1g2:
    groups = [json.load(open(S + f"/chibi/final/{g}.json", encoding='utf-8')) for g in ('G1', 'G2')] + [g3]
for g in groups:
    for pid, v in g['prompts'].items():
        by[pid]['content'] = v['content']
if not with_g1g2:  # G1 final already carries the JB blanks in Main and the Impersonation Turn
    m = by['main']['content']
    assert m.count('{{setvar::ariaPatchJoins::}}') == 1
    by['main']['content'] = m.replace('{{setvar::ariaPatchJoins::}}', '{{setvar::ariaPatchJoins::}}{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}')
    imp = by['379e3c22-9a25-5e6d-bf4a-037d49aa60d9']
    assert imp['content'].count('{{setvar::ariaHoldGate::}}') == 1
    imp['content'] = imp['content'].replace('{{setvar::ariaHoldGate::}}', '{{setvar::ariaHoldGate::}}{{setvar::ariaJb::}}')
hold = [p for p in cc['prompts'] if p['identifier'].startswith('dc8b1acb')][0]
new = copy.deepcopy(hold)
new['identifier'] = str(uuid.UUID(int=random.Random(7).getrandbits(128), version=4))
new['name'] = '🔓 Jailbreak (needs Adult Context)'
new['content'] = jb['cc_comment'] + '{{trim}}\n{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}' % (N, LINES)
idx = [i for i, p in enumerate(cc['prompts']) if p['identifier'].startswith('4537b57d')][0]
cc['prompts'].insert(idx + 1, new)
order = cc['prompt_order'][1]['order']
oi = [i for i, r in enumerate(order) if r['identifier'].startswith('4537b57d')][0]
order.insert(oi + 1, {'identifier': new['identifier'], 'enabled': False})

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    totals, errors = ab.analyse_cc(cc)
print('CC totals', totals)
print('CC errors (the frozen BUDGET is the old 6000):')
for e in errors:
    print('  -', e)

# Render checks of the Logic Core in the full CC turn: everything ON (+ the JB) with Adult on, Tags on and off
all_ids = {r['identifier'] for r in order} - {'enhanceDefinitions'}
names = {p['identifier']: p['name'] for p in cc['prompts']}
patches = {pid for pid in all_ids if names[pid].startswith('🩹')}
twin = '591b8c15-985e-59f1-8c90-59e7cae236ae'
tags = '303f26f5-bc2f-5dde-a9e9-aaaacd3eff4b'
base = {pid for pid in all_ids if not names[pid].startswith(('🌳', '🌿'))} - patches - {twin}
ds = [pid for pid in patches if 'DeepSeek' in names[pid]][0]
for label, en, imp in (('Tags ON, DeepSeek patch, normal', base | {ds}, False),
                       ('Tags OFF, DeepSeek patch, normal', (base | {ds}) - {tags}, False),
                       ('Tags ON, DeepSeek patch, Impersonate', base | {ds}, True)):
    r, st = ab.simulate_cc(cc, en, seed=1, impersonate=imp)
    lc = r.get('15b770cf-6049-5f3b-b25d-be09728a65d5', '')
    dashed = [l for l in lc.split('\n') if l.startswith('- ')]
    print(f'\n=== CC {label}: logicCoreLines={st.get("logicCoreLines")}, dashed lines before go={len(dashed) - 1}, '
          f'Logic Core tokens={ab.tokens(lc)}')
    print(lc)

# ---------------- TC
tc = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
sp = tc['sysprompt']
ph = sp['post_history']
i = ph.index('<final_gate>')
gate = ph[i:]
if with_g1g2:
    g2 = json.load(open(S + "/chibi/final/G2.json", encoding='utf-8'))
    gate = g2['tc']['post_history_gate']
sp['post_history'] = g3['tc']['post_history_logic_core'] + gate
c = sp['content']
c = c.replace('{{.aria-freaky = off}}\n', '{{.aria-freaky = off}}\n' + jb['tc_switch_comment'] + '{{.aria-jailbreak = off}}\n', 1)
c = c.replace('{{setvar::ariaPatchJoins::}}\n', '{{setvar::ariaPatchJoins::}}{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}\n', 1)
block = '{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}{{/if}}' % (N, LINES)
assert c.count('</freaky_override>\n{{/if}}{{#if .aria-hybrid-pov}}') == 1
c = c.replace('</freaky_override>\n{{/if}}{{#if .aria-hybrid-pov}}', '</freaky_override>\n{{/if}}' + block + '{{#if .aria-hybrid-pov}}', 1)
sp['content'] = c
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    totals, errors = ab.analyse_tc(tc)
print('\nTC totals', totals)
print('TC errors (the frozen BUDGET is the old 6000):')
for e in errors:
    print('  -', e)
sw = dict(ab.SWITCH.findall(sp['content']))
allon = {s: 'on' for s in sw if not s.startswith('aria-patch')} | {s: 'off' for s in sw if s.startswith('aria-patch')} | {'aria-patch-deepseek': 'on'}
for label, ov in (('thinking-tags on', allon), ('thinking-tags off', dict(allon, **{'aria-thinking-tags': 'off'}))):
    r, st = ab.simulate_tc(tc, ov, seed=1)
    post = r['Post-History']
    lc = post[:post.index('<final_gate>')]
    print(f'\n=== TC everything ON + JB + DeepSeek, {label}: logicCoreLines={st.get("logicCoreLines")}, '
          f'dashed lines before go={len([l for l in lc.split(chr(10)) if l.startswith("- ")]) - 1}')
    print(lc)
