#!/usr/bin/env python3
"""Independent wiring audit of the 🔓 Jailbreak work against HEAD (reviewer's own script).

Every check rebuilds the expected working-tree text from HEAD plus the exact spec'd insertion, so anything else that
changed shows up as a failure.
"""
import json, re, subprocess, sys, uuid
from pathlib import Path

ROOT = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
S = ROOT / '.claude/aria-work'
CCN = "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TCN = "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
MARN = "Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json"
RXN = 'regex/ARIA 1.0 Regex Scripts (Text Completions).json'

fails, passes = [], 0


def ok(cond, msg):
    global passes
    if cond:
        passes += 1
    else:
        fails.append(msg)
    return cond


def head_raw(name):
    r = subprocess.run(['git', '-C', str(ROOT), 'show', f'HEAD:{name}'], capture_output=True, check=True)
    return r.stdout.decode('utf-8')


def work_raw(name):
    return (ROOT / name).read_text(encoding='utf-8')


fin = json.loads((S / 'jb/final.json').read_text(encoding='utf-8'))
L1, L2 = fin['lines']
JB_BODY = L1 + '\n' + L2
N = 2
ok(len(fin['lines']) == N, 'final.json does not hold exactly 2 lines')
ok(all(l.startswith('- ') and ': ' in l for l in fin['lines']), 'a JB line does not start "- Label: "')
ok([re.match(r'- (\w+):', l).group(1) for l in fin['lines']] == ['Role', 'Frank'], 'labels are not Role, Frank')
ok(round(len(L1 + '\n' + L2) / 4) <= 130 and len(L1 + L2) / 4 <= 130, f'JB lines over 130 tokens: {len(L1 + L2) / 4}')
ok('\\n' not in JB_BODY, 'literal backslash-n in the JB lines')

# ------------------------------------------------------------------ CC
cc_raw, cc0_raw = work_raw(CCN), head_raw(CCN)
cc, cc0 = json.loads(cc_raw), json.loads(cc0_raw)
P, P0 = cc['prompts'], cc0['prompts']
byid = {p['identifier']: p for p in P}
byid0 = {p['identifier']: p for p in P0}
pick = lambda pre, d: [v for k, v in d.items() if k.startswith(pre)]
jb_objs = [p for p in P if p.get('name', '').startswith('🔓')]
ok(len(jb_objs) == 1, f'expected one 🔓 prompt, found {len(jb_objs)}')
jb = jb_objs[0]
JBID = jb['identifier']
hold = pick('dc8b1acb', byid)[0]
freaky = pick('4537b57d', byid)[0]
try:
    u = uuid.UUID(JBID)
    ok(u.version == 4 and str(u) == JBID, 'JB identifier is not a canonical uuid4')
except ValueError:
    ok(False, 'JB identifier is not a uuid')
for name in (CCN, TCN, MARN, RXN):
    ok(JBID not in head_raw(name), f'JB identifier already existed at HEAD in {name}')
ok(cc_raw.count(JBID) == 2, f'JB id appears {cc_raw.count(JBID)} times in CC (expected 2: prompts + prompt_order[1])')
ok(list(jb.keys()) == list(hold.keys()), f'key order differs from Character Hold: {list(jb.keys())}')
for k in hold:
    if k in ('identifier', 'name', 'content'):
        continue
    ok(jb[k] == hold[k], f'JB {k}={jb[k]!r} but Character Hold has {hold[k]!r}')
ok(jb['role'] == 'system' and jb['injection_position'] == 0, 'JB role/injection_position wrong')
ok(jb['name'] == '🔓 Jailbreak (needs Adult Context)', f'JB name {jb["name"]!r}')
ids = [p['identifier'] for p in P]
ok(ids.index(JBID) == ids.index(freaky['identifier']) + 1, 'JB is not right after Freaky in prompts[]')
ok([i for i in ids if i != JBID] == [p['identifier'] for p in P0], 'prompts[] order changed apart from the JB')
order = cc['prompt_order'][1]['order']
oids = [r['identifier'] for r in order]
ok(oids.index(JBID) == oids.index(freaky['identifier']) + 1, 'JB row is not right after Freaky in prompt_order[1]')
ok(order[oids.index(JBID)] == {'identifier': JBID, 'enabled': False}, 'JB order row is not {identifier, enabled:false}')
ok(list(order[oids.index(JBID)].keys()) == ['identifier', 'enabled'], 'JB order row key order')
ok([r for r in order if r['identifier'] != JBID] == cc0['prompt_order'][1]['order'], 'prompt_order[1] changed apart from the JB row')
ok(cc['prompt_order'][0] == cc0['prompt_order'][0], 'prompt_order[0] changed')
ok(len(cc['prompt_order']) == len(cc0['prompt_order']), 'prompt_order length changed')
ok(sorted(oids) == sorted(ids), 'not every prompt is named exactly once in prompt_order[1]')
# JB content
exp_jb = (fin['cc_comment'] + '{{trim}}\n{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::'
          + JB_BODY + '}}{{/if}}')
ok(jb['content'] == exp_jb, 'JB content differs from final.json comment + spec body')
# Main Prompt
m0 = byid0['main']['content']
anchor = '{{setvar::ariaPatchJoins::}}\n{{trim}}'
ok(m0.count(anchor) == 1, 'Main Prompt anchor not unique at HEAD')
ok(byid['main']['content'] == m0.replace(anchor, '{{setvar::ariaPatchJoins::}}{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}\n{{trim}}'),
   'Main Prompt differs from HEAD + two blanks at the end of the blanking run')
first = byid['main']['content'].split('{{trim}}')[1]
ok(first.strip().endswith('{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}'), 'JB blanks are not at the end of the blanking line')
# Impersonation Turn
imp0 = pick('379e3c22', byid0)[0]['content']
a = '{{setvar::ariaHoldGate::}}<impersonation_turn>'
ok(imp0.count(a) == 1, 'Impersonation anchor')
ok(pick('379e3c22', byid)[0]['content'] == imp0.replace(a, '{{setvar::ariaHoldGate::}}{{setvar::ariaJb::}}<impersonation_turn>'),
   'Impersonation Turn differs from HEAD + ariaJb blank at the end of its run')
# Logic Cores
CNT_A = '{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}{{#if .ariaHoldLine}}'
CNT_N = ('{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}'
         '{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}{{#if .ariaHoldLine}}')
PR_A = '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}- Fresh:'
PR_N = '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}- Fresh:'
after_comment = lambda t: t[t.index('}}{{trim}}') + 2:]
lcs = []
for pre in ('15b770cf', '591b8c15'):
    c0 = pick(pre, byid0)[0]['content']
    ok(c0.count(CNT_A) == 1 and c0.count(PR_A) == 1, f'{pre} anchors not unique at HEAD')
    exp = c0.replace(CNT_A, CNT_N).replace(PR_A, PR_N)
    ok(pick(pre, byid)[0]['content'] == exp, f'{pre} Logic Core differs from HEAD + counter + print')
    lcs.append(pick(pre, byid)[0]['content'])
ok(after_comment(lcs[0]) == after_comment(lcs[1]), 'the two CC Logic Cores differ after their comments')
# neighbours' newline pattern: each print block is {{#if .x}}{{getvar::x}}\n{{/if}}
ok(re.search(r'\{\{#if \.ariaFateLine\}\}\{\{getvar::ariaFateLine\}\}\n\{\{/if\}\}', lcs[0]) is not None, 'neighbour pattern check')
# Every other prompt unchanged
changed = {p['identifier'] for p in P if p['identifier'] in byid0 and p != byid0[p['identifier']]}
expect_changed = {'main', pick('15b770cf', byid)[0]['identifier'], pick('591b8c15', byid)[0]['identifier'],
                  pick('379e3c22', byid)[0]['identifier']}
ok(changed == expect_changed, f'unexpected prompts changed: {changed ^ expect_changed}')
# Regex
RX_OLD = '|Layers|Tally|Pushback|Restate|Joins)'
RX_NEW = '|Layers|Tally|Pushback|Restate|Joins|Role|Frank)'
rs, rs0 = cc['extensions']['regex_scripts'], cc0['extensions']['regex_scripts']
ok(len(rs) == len(rs0), 'regex script count changed')
for s, s0 in zip(rs, rs0):
    if s['id'].startswith('d7a2ca91'):
        ok(s0['findRegex'].count(RX_OLD) == 1, 'CC regex anchor')
        ok(s == dict(s0, findRegex=s0['findRegex'].replace(RX_OLD, RX_NEW)), 'CC d7a2ca91 differs from HEAD + Role|Frank')
        cc_rx = s['findRegex']
    else:
        ok(s == s0, f'CC regex {s["id"][:8]} changed')
# Other top-level keys
ok({k: v for k, v in cc.items() if k not in ('prompts', 'prompt_order', 'extensions')} ==
   {k: v for k, v in cc0.items() if k not in ('prompts', 'prompt_order', 'extensions')}, 'CC top-level settings changed')
ok({k: v for k, v in cc['extensions'].items() if k != 'regex_scripts'} ==
   {k: v for k, v in cc0['extensions'].items() if k != 'regex_scripts'}, 'CC extensions changed beyond regex_scripts')
# Raw text: work raw == head raw with only the expected substitutions (no re-dump)
def enc(x):
    return json.dumps(x, ensure_ascii=False)[1:-1]
exp_raw = cc0_raw
for old, new, n in [
    (enc(byid0['main']['content']), enc(byid['main']['content']), 1),
    (enc(imp0), enc(pick('379e3c22', byid)[0]['content']), 1),
    (enc(pick('15b770cf', byid0)[0]['content']), enc(lcs[0]), 1),
    (enc(pick('591b8c15', byid0)[0]['content']), enc(lcs[1]), 1),
    (enc(RX_OLD), enc(RX_NEW), 1),
]:
    ok(exp_raw.count(old) == n, f'raw anchor count {exp_raw.count(old)} != {n}')
    exp_raw = exp_raw.replace(old, new)
# the prompt object, formatted like its neighbours, inserted after Freaky's object
fr_end = exp_raw.index('"identifier": "4537b57d')
fr_close = exp_raw.index('\n        },\n', fr_end) + len('\n        },\n')
obj = '        {\n' + ',\n'.join(f'            {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}' for k, v in jb.items()) + '\n        },\n'
exp_raw = exp_raw[:fr_close] + obj + exp_raw[fr_close:]
row_at = exp_raw.index('"identifier": "4537b57d', exp_raw.index('"prompt_order"'))
row_at = exp_raw.index('"identifier": "4537b57d', row_at + 1) if exp_raw.count('"identifier": "4537b57d', exp_raw.index('"prompt_order"')) > 1 else row_at
row_close = exp_raw.index('\n                },\n', row_at) + len('\n                },\n')
row = '                {\n                    "identifier": "%s",\n                    "enabled": false\n                },\n' % JBID
exp_raw = exp_raw[:row_close] + row + exp_raw[row_close:]
ok(exp_raw == cc_raw, 'CC raw text is not HEAD + the expected raw insertions (formatting drift?)')

# ------------------------------------------------------------------ TC
tc_raw, tc0_raw = work_raw(TCN), head_raw(TCN)
tc, tc0 = json.loads(tc_raw), json.loads(tc0_raw)
s0, s1 = tc0['sysprompt']['content'], tc['sysprompt']['content']
sw_a = '{{.aria-freaky = off}}\n'
ok(s0.count(sw_a) == 1, 'TC switch anchor')
sw_new = sw_a + fin['tc_switch_comment'] + '{{.aria-jailbreak = off}}\n'
bl_a = '{{setvar::ariaPatchJoins::}}\n{{trim}}\nYou are'
ok(s0.count(bl_a) == 1, 'TC blank anchor')
bl_new = '{{setvar::ariaPatchJoins::}}{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}\n{{trim}}\nYou are'
blk_a = '</freaky_override>\n{{/if}}'
ok(s0.count(blk_a) == 1, 'TC block anchor')
blk_new = blk_a + ('{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::' + JB_BODY
                   + '}}{{/if}}{{/if}}')
exp_s = s0.replace(sw_a, sw_new).replace(bl_a, bl_new).replace(blk_a, blk_new)
ok(s1 == exp_s, 'TC sysprompt.content differs from HEAD + switch + blanks + block')
# the adult block comes before the freaky block, and the JB block after both
ok(s1.index('{{#if .aria-adult}}') < s1.index('{{#if .aria-freaky}}') < s1.index('{{#if .aria-jailbreak}}'), 'TC block order')
p0, p1 = tc0['sysprompt']['post_history'], tc['sysprompt']['post_history']
CL_A = 'with no Fate, Bonds, Ledger or Layers line.'
CL_N = 'with no Fate, Bonds, Ledger, Layers, Role or Frank line.'
ok(p0.count(CNT_A) == 1 and p0.count(PR_A) == 1 and p0.count(CL_A) == 1, 'TC post_history anchors')
ok(p1 == p0.replace(CNT_A, CNT_N).replace(PR_A, PR_N).replace(CL_A, CL_N), 'TC post_history differs from HEAD + counter + print + sentence')
# TC post_history Logic Core vs CC Logic Core: the shared model-facing text must match
ok({k: v for k, v in tc.items() if k != 'sysprompt'} == {k: v for k, v in tc0.items() if k != 'sysprompt'}, 'TC other keys changed')
ok(tc['sysprompt']['name'] == tc0['sysprompt']['name'], 'TC sysprompt name changed')
exp_tc_raw = tc0_raw
for old, new in [(enc(s0), enc(s1)), (enc(p0), enc(p1))]:
    ok(exp_tc_raw.count(old) == 1, 'TC raw anchor')
    exp_tc_raw = exp_tc_raw.replace(old, new)
ok(exp_tc_raw == tc_raw, 'TC raw text drift')
ok(tc['sysprompt']['content'].count('{{if .aria-flash-gate}}') == tc0['sysprompt']['content'].count('{{if .aria-flash-gate}}'), 'flash-gate if touched')

# ------------------------------------------------------------------ TC regex file
rx_raw, rx0_raw = work_raw(RXN), head_raw(RXN)
ok(rx0_raw.count(enc(RX_OLD)) == 1, 'TC regex raw anchor')
ok(rx_raw == rx0_raw.replace(enc(RX_OLD), enc(RX_NEW)), 'TC regex file is not HEAD + the label (formatting drift?)')
rx = json.loads(rx_raw)
tc_rx = [s for s in rx if s['id'].startswith('d7a2ca91')][0]['findRegex']
ok(tc_rx == cc_rx, 'TC and CC untagged-plan regexes differ')
ok(rx_raw.startswith('[\n    {\n        "id"'), 'TC regex file lost its four-space indentation')
d = subprocess.run(['git', '-C', str(ROOT), 'diff', '--numstat', '--', RXN], capture_output=True, text=True).stdout.split()
ok(d[:2] == ['1', '1'], f'TC regex numstat {d[:2]}')


def to_py(js):
    m = re.fullmatch(r'/(.*)/([a-z]*)', js, re.S)
    body, flags = m.group(1), m.group(2)
    f = 0
    for ch in flags:
        f |= {'i': re.I, 'm': re.M, 's': re.S, 'g': 0, 'u': 0}[ch]
    return re.compile(body, f)


for label, js in (('CC', cc_rx), ('TC', tc_rx)):
    try:
        rxc = to_py(js)
        ok(True, '')
    except re.error as e:
        ok(False, f'{label} regex does not compile: {e}')
        continue
    sample = ('- OOC: none.\n- Scene: x.\n- Knows: y.\n- Mode: realism.\n- Voice: z.\n- Move: m.\n- Ledger: l.\n'
              + L1.replace('{{user}}', 'Lewis') + '\n' + L2 + '\n- Fresh: f.\n- Check: c.\n- go\nLewis smiles.')
    out = rxc.sub('', sample, count=1)
    ok(out == 'Lewis smiles.', f'{label} regex leaves {out[:80]!r}')
    # without the new labels the old regex must fail to strip the whole plan (proves the labels matter)
    old = to_py(js.replace('|Role|Frank)', ')'))
    ok(old.sub('', sample, count=1) != 'Lewis smiles.', f'{label}: old regex already strips Role/Frank plans (test is weak)')

# ------------------------------------------------------------------ Marinara
mr_raw, mr0_raw = work_raw(MARN), head_raw(MARN)
md, md0 = json.loads(mr_raw), json.loads(mr0_raw)
ok(json.dumps(md, ensure_ascii=False, indent='\t') == mr_raw, 'Marinara does not round-trip exactly')
ok(not mr_raw.endswith('\n'), 'Marinara has a trailing newline')
cb = [c for c in md['data']['choiceBlocks'] if c['variableName'] == 'logic_options'][0]
cb0 = [c for c in md0['data']['choiceBlocks'] if c['variableName'] == 'logic_options'][0]
opts, opts0 = json.loads(cb['options']), json.loads(cb0['options'])
ok(opts[:-1] == opts0 and len(opts) == len(opts0) + 1, 'logic_options: existing options changed')
new = opts[-1]
ok(list(new.keys()) == ['id', 'label', 'value'], 'new option key order')
ok(re.fullmatch(r'opt_[A-Za-z0-9_-]{12}', new['id']) is not None, f'new option id {new["id"]}')
ok(new['label'] == '🔓 Jailbreak (needs Adult Context)' and new['value'] == 'JAILBREAK', 'new option label/value')
ok(cb['options'] == json.dumps(opts, ensure_ascii=False, separators=(',', ':')), 'options string is not compact JSON')
ok(cb0['options'] == json.dumps(opts0, ensure_ascii=False, separators=(',', ':')), '(HEAD options format check)')
ok('JAILBREAK' not in json.dumps(cb.get('defaultChoices')), 'JAILBREAK is in defaultChoices')
ok(cb.get('defaultChoices') == cb0.get('defaultChoices'), 'defaultChoices changed')
ok(cb['question'].startswith(cb0['question'].split(' Deselect all options to disable.')[0]) and
   cb['question'].endswith(' Deselect all options to disable.'), 'question not extended in place')
added_q = cb['question'][len(cb0['question'].split(' Deselect all options to disable.')[0]):-len(' Deselect all options to disable.')]
ok(added_q.count('. ') == 0 and added_q.strip().endswith('.'), f'question gained more than one sentence: {added_q!r}')
ok({k: v for k, v in cb.items() if k not in ('question', 'options')} == {k: v for k, v in cb0.items() if k not in ('question', 'options')},
   'logic_options block changed beyond question/options')
sec = {s['name']: s for s in md['data']['sections']}
sec0 = {s['name']: s for s in md0['data']['sections']}
M_HOLD = '{{#if core_modules contains "HOLD"}}'
M_CNT_A = '{{#if world_engine contains "FATE" || world_engine contains "BONDS"}}{{addvar::logicCoreLines::1}}{{/if}}' + M_HOLD
M_CNT = '{{#if logic_options contains "JAILBREAK" && adult_mode != "NONE"}}{{addvar::logicCoreLines::2}}{{/if}}'
M_PR_A = 'copies it.\n{{/if}}- Fresh:'
M_PR = 'copies it.\n{{/if}}{{#if logic_options contains "JAILBREAK" && adult_mode != "NONE"}}' + JB_BODY + '\n{{/if}}- Fresh:'
for name in ('🧠 The Logic Core', '🧠 The Logic Core (system-role twin)'):
    c0 = sec0[name]['content']
    ok(c0.count(M_CNT_A) == 1 and c0.count(M_PR_A) == 1, f'Marinara {name} anchors')
    ok(sec[name]['content'] == c0.replace(M_CNT_A, M_CNT_A[:-len(M_HOLD)] + M_CNT + M_HOLD).replace(M_PR_A, M_PR), f'Marinara {name} differs from HEAD + counter + lines')
g0 = sec0['🚪 Last-Mile Gate']['content']
ok(g0.count(M_CNT_A) == 1, 'gate anchor')
ok(sec['🚪 Last-Mile Gate']['content'] == g0.replace(M_CNT_A, M_CNT_A[:-len(M_HOLD)] + M_CNT + M_HOLD), 'Marinara gate differs from HEAD + counter')
for name in sec:
    if name in ('🧠 The Logic Core', '🧠 The Logic Core (system-role twin)', '🚪 Last-Mile Gate'):
        continue
    ok(sec[name] == sec0.get(name), f'Marinara section {name} changed')
ok([s['name'] for s in md['data']['sections']] == [s['name'] for s in md0['data']['sections']], 'section list changed')
for k in md['data']:
    if k in ('sections', 'choiceBlocks', 'preset'):
        continue
    ok(md['data'][k] == md0['data'][k], f'Marinara data.{k} changed')
for c, c0 in zip(md['data']['choiceBlocks'], md0['data']['choiceBlocks']):
    if c['variableName'] != 'logic_options':
        ok(c == c0, f'choice block {c["variableName"]} changed')
pr, pr0 = md['data']['preset'], md0['data']['preset']
ok({k: v for k, v in pr.items() if k not in ('description', 'updatedAt')} == {k: v for k, v in pr0.items() if k not in ('description', 'updatedAt')},
   'Marinara preset fields changed beyond description/updatedAt')
ok({k: v for k, v in md.items() if k not in ('data', 'exportedAt')} == {k: v for k, v in md0.items() if k not in ('data', 'exportedAt')}, 'Marinara top level changed')
# No bare {{#if name}} added in Marinara
added = mr_raw
ok(not re.search(r'\{\{#if (?:JAILBREAK|ariaJb|\.ariaJb)', mr_raw), 'bare if on a JB name in Marinara')
ok('ariaJb' not in mr_raw, 'Marinara uses an aria splice variable')

# ------------------------------------------------------------------ checker
ck, ck0 = work_raw('tools/aria_budget.py'), head_raw('tools/aria_budget.py')
ok('BUDGET = 7000' in ck and 'BUDGET = 6000' in ck0, 'BUDGET')
ok(re.search(r"DEFAULT_PRESETS = \[.*?\]", ck, re.S).group(0) == re.search(r"DEFAULT_PRESETS = \[.*?\]", ck0, re.S).group(0), 'DEFAULT_PRESETS changed')
sys.path.insert(0, str(ROOT / 'tools'))
import importlib
ab = importlib.import_module('aria_budget')
ok(ab.budget_for("Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json") == 3000, 'chibi budget')
ok(ab.budget_for(CCN) == 7000 and ab.budget_for(TCN) == 7000 and ab.budget_for('') == 7000, 'default budget')
ok(not re.search(r'\{BUDGET\} budget', ck), 'an error message still names BUDGET instead of the per-file budget')
ok(not re.search(r'6[,.]?000', re.sub(r'\{0,6000\}', '', ck)), 'a 6000 mention remains in the checker')

print(f'{passes} checks passed, {len(fails)} failed')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
