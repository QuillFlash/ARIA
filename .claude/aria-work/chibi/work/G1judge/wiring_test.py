#!/usr/bin/env python3
"""Frozen-checker run on in-memory copies of the snapshot with the judged G1 texts and a stand-in JB (per JB.md)."""
import contextlib
import copy
import io
import json
import sys
import uuid

S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
sys.path.insert(0, S + '/spec/frozen')
import aria_budget as ab  # noqa: E402

G1 = json.load(open(sys.argv[1], encoding='utf-8'))
JB = json.load(open(S + '/jb/final.json', encoding='utf-8'))
jb_lines = '\n'.join(JB['lines'])
jb_n = len(JB['lines'])
JB_SET = '{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}' % (jb_n, jb_lines)
COUNT_AFTER = '{{#if .ariaBondsLine}}{{addvar::logicCoreLines::1}}{{/if}}{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}'
COUNT_JB = '{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}'
PRINT_AFTER = '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}'
PRINT_JB = '{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}'


def add_jb_to_logic_core(text):
    assert text.count(COUNT_AFTER) == 1 and text.count(PRINT_AFTER) == 1
    text = text.replace(COUNT_AFTER, COUNT_AFTER + COUNT_JB)
    return text.replace(PRINT_AFTER, PRINT_AFTER + PRINT_JB)


def run(label, fn, preset):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        totals, errors = fn(preset)
    print(f'--- {label}: totals {totals}')
    print('    errors:', errors or 'none')
    return totals, errors


# ---------------- CC
cc = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
by = {p['identifier']: p for p in cc['prompts']}
for pid, p in G1['prompts'].items():
    by[pid]['content'] = p['content']
for pid in ('15b770cf-6049-5f3b-b25d-be09728a65d5', '591b8c15-985e-59f1-8c90-59e7cae236ae'):
    by[pid]['content'] = add_jb_to_logic_core(by[pid]['content'])
hold = by['dc8b1acb-9a7e-5a43-b9aa-38e7b70662a3']
jb = copy.deepcopy(hold)
jb['identifier'] = str(uuid.UUID(int=12345))
jb['name'] = '🔓 Jailbreak (needs Adult Context)'
jb['content'] = '{{// stand-in}}{{trim}}\n' + JB_SET
idx = next(i for i, p in enumerate(cc['prompts']) if p['identifier'].startswith('4537b57d'))
cc['prompts'].insert(idx + 1, jb)
order = cc['prompt_order'][1]['order']
oi = next(i for i, r in enumerate(order) if r['identifier'].startswith('4537b57d'))
order.insert(oi + 1, {'identifier': jb['identifier'], 'enabled': False})
run('CC snapshot + judged G1 + stand-in JB', ab.analyse_cc, cc)

# ---------------- TC
tc = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
c = tc['sysprompt']['content']
a = c.index('{{setvar::ariaDice::}}')
b = c.index('{{/if}}', c.index('{{getvar::player-instructions}}')) + len('{{/if}}')
c = c[:a] + G1['tc']['main_prompt'] + c[b:]
r0 = c.index('{{// README')
r1 = c.index('}}{{trim}}', r0) + len('}}{{trim}}')
assert G1['tc']['readme_comment'].endswith('}}{{trim}}')
c = c[:r0] + G1['tc']['readme_comment'] + c[r1:]
ci0 = c.index('{{// If you have any additional')
ci1 = c.index('}}', c.index('requested specifically.))', ci0)) + 2
c = c[:ci0] + G1['tc']['custom_instructions_comment'] + c[ci1:]
fz = '{{.aria-freaky = off}}'
assert c.count(fz) == 1
c = c.replace(fz, fz + '\n{{// 🔓 Jailbreak: stand-in}}{{.aria-jailbreak = off}}')
fb = '</freaky_override>\n{{/if}}'
assert c.count(fb) == 1
c = c.replace(fb, fb + '{{#if .aria-jailbreak}}' + JB_SET + '{{/if}}')
tc['sysprompt']['content'] = c
tc['sysprompt']['post_history'] = add_jb_to_logic_core(tc['sysprompt']['post_history'])
run('TC snapshot + judged G1 + stand-in JB', ab.analyse_tc, tc)

# rendered spot checks: Impersonate turn with everything ON, Main + Imp text only
ids = {r['identifier'] for r in order} - {pid for pid in by if by[pid].get('name', '').startswith(('🌳', '🌿', '🩹'))} - {'591b8c15-985e-59f1-8c90-59e7cae236ae', 'enhanceDefinitions'}
rendered, state = ab.simulate_cc(cc, ids | {jb['identifier'], 'nsfw'}, seed=1, impersonate=True)
print('--- Impersonate turn (JB on, Adult on): ariaJb =', repr(state.get('ariaJb')), ' logicCoreLines =', state.get('logicCoreLines'))
rendered, state = ab.simulate_cc(cc, ids | {jb['identifier'], 'nsfw'}, seed=1)
print('--- normal turn (JB on, Adult on): ariaJb set =', bool(state.get('ariaJb')), ' logicCoreLines =', state.get('logicCoreLines'))
