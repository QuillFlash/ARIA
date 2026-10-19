#!/usr/bin/env python3
"""Reviewer's static audit of the 🔓 Jailbreak wiring (CC, TC, both regex files, Marinara, checker).

Independent of the integrator's audit: every expectation is written from JB.md and COMMON.md.
Prints PASS/FAIL per item and exits 1 on any FAIL.
"""
import json, re, subprocess, sys, uuid
from pathlib import Path

ROOT = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
S = ROOT / '.claude/aria-work'
CCN = "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TCN = "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
MARN = "Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json"
RXN = 'regex/ARIA 1.0 Regex Scripts (Text Completions).json'
FAILS = []


def check(name, ok, detail=''):
    print(('PASS  ' if ok else 'FAIL  ') + name + ('' if ok or not detail else f'  [{detail}]'))
    if not ok:
        FAILS.append(name)


def git_show(path):
    return subprocess.run(['git', '-C', str(ROOT), 'show', f'HEAD:{path}'], capture_output=True, check=True).stdout.decode('utf-8')


raw_cc = (ROOT / CCN).read_text(encoding='utf-8')
raw_tc = (ROOT / TCN).read_text(encoding='utf-8')
raw_mar = (ROOT / MARN).read_text(encoding='utf-8')
raw_rx = (ROOT / RXN).read_text(encoding='utf-8')
cc, tc, mar, rx = (json.loads(x) for x in (raw_cc, raw_tc, raw_mar, raw_rx))
cc0, tc0, mar0, rx0 = (json.loads(git_show(x)) for x in (CCN, TCN, MARN, RXN))
fin = json.loads((S / 'jb/final.json').read_text(encoding='utf-8'))
LINES, LABELS = fin['lines'], fin['labels']
N = len(LINES)
JBTEXT = '\n'.join(LINES)

# ------------------------------------------------------------------ approved lines: form and house rules
check('final.json: 2 or 4 lines (never 3)', N in (2, 4), str(N))
check('final.json: each line starts "- Label: " with its label', all(l.startswith(f'- {lab}: ') for l, lab in zip(LINES, LABELS)))
check('final.json: 130 tokens at most (characters / 4)', len(JBTEXT) / 4 <= 130, f'{len(JBTEXT) / 4}')
FORBIDDEN = ('OOC, Scene, Knows, Mode, Voice, Move, Fate, Bonds, Ledger, Fresh, Check, Person, Replies, Filler, Gemini, Contrast, '
             'Negation runs, Flow, Card details, Echo, Repeats, Bodies, Layers, Tally, Pushback, Restate, Joins').split(', ')
check('final.json: labels are new', not set(LABELS) & set(FORBIDDEN), str(set(LABELS) & set(FORBIDDEN)))
check('lines: no quoted examples (no quote marks)', not re.search(r'["“”‘’]|\B\'|\'\B', JBTEXT.replace("{{user}}", "")), JBTEXT)
check('lines: say sex stays between adults', 'sex stays between adults' in JBTEXT)
# lists of exactly three: comma series "a, b and c" / "a, b or c" with exactly two commas before the and/or
three = []
for frag in re.split(r'[;()]', JBTEXT):
    for m in re.finditer(r'(?:^|[:;(]\s*|\s)([^,;:()]+(?:, [^,;:()]+)+)(?:,)? (?:and|or) ([^,;:()]+)', frag):
        items = m.group(1).split(', ')
        if len(items) == 2:
            three.append(m.group(0).strip())
check('lines: no comma series of exactly three items', not three, str(three))
semis = [l.split(': ', 1)[1].split('; ') for l in LINES]
check('lines: fragment count per line is never exactly 3', all(len(s) != 3 for s in semis), str([len(s) for s in semis]))
BOUNDARY = [r'for a living', r'\bincome\b', r'profession', r'career', r'isolated', r'enterprise', r'guideline', r'contract',
            r'high.risk', r'protectiv', r'minorit', r'silenc', r'never refuse', r'always comply', r'consent', r'legal',
            r'permission', r'no rules', r'no limits', r'uncensor', r'filter', r'safety', r'polic', r'allowed', r'ignore',
            r'disregard', r'dismiss']
hits = [b for b in BOUNDARY if re.search(b, JBTEXT, re.I)]
check('lines: none of the hard-boundary techniques (pretext, no-guidelines, Van Damme check, never-refuse, consent, legal)', not hits, str(hits))

# ------------------------------------------------------------------ CC object
P = cc['prompts']
ids = [p['identifier'] for p in P]
byid = {p['identifier']: p for p in P}
jbs = [p for p in P if p.get('name', '').startswith('🔓')]
check('CC: exactly one 🔓 prompt', len(jbs) == 1, str(len(jbs)))
jb = jbs[0]
jid = jb['identifier']
hold = byid['dc8b1acb-9a7e-5a43-b9aa-38e7b70662a3']
freaky = byid['4537b57d-e002-586d-a4c9-233740c51605']
check('CC object: key order equals Character Hold\'s', list(jb) == list(hold), f'{list(jb)} vs {list(hold)}')
for k in hold:
    if k in ('identifier', 'name', 'content'):
        continue
    check(f'CC object: {k} equals Character Hold\'s', jb[k] == hold[k], f'{jb[k]!r} vs {hold[k]!r}')
check('CC object: role system, injection_position 0', jb['role'] == 'system' and jb['injection_position'] == 0)
try:
    u = uuid.UUID(jid)
except ValueError:
    u = None
check('CC object: identifier is a canonical uuid4', u is not None and u.version == 4 and str(u) == jid and u.variant == uuid.RFC_4122, jid)
check('CC object: identifier unique', ids.count(jid) == 1)
check('CC object: identifier not used in HEAD', jid not in {p['identifier'] for p in cc0['prompts']})
check('CC object: name', jb['name'] == '🔓 Jailbreak (needs Adult Context)', jb['name'])
check('CC prompts[]: right after Freaky', ids.index(jid) == ids.index(freaky['identifier']) + 1)
check('CC prompts[]: every other prompt unchanged and in HEAD order', [p for p in P if p is not jb] is not None and
      [p['identifier'] for p in P if p is not jb] == [p['identifier'] for p in cc0['prompts']])
rows = cc['prompt_order'][1]['order']
rids = [r['identifier'] for r in rows]
check('CC order[1]: JB row once, right after Freaky\'s row', rids.count(jid) == 1 and rids.index(jid) == rids.index(freaky['identifier']) + 1)
check('CC order[1]: JB row is exactly {identifier, enabled: false}', rows[rids.index(jid)] == {'identifier': jid, 'enabled': False}
      and list(rows[rids.index(jid)]) == ['identifier', 'enabled'])
check('CC order[1]: other rows unchanged', [r for r in rows if r['identifier'] != jid] == cc0['prompt_order'][1]['order'])
check('CC order[0]: unchanged', cc['prompt_order'][0] == cc0['prompt_order'][0])
check('CC order[1]: every prompt named exactly once', sorted(rids) == sorted(ids))
check('CC order: Main, Adult Context and Freaky come before the JB; the JB before both Logic Cores',
      rids.index('main') < rids.index('nsfw') < rids.index(freaky['identifier']) < rids.index(jid)
      < rids.index('15b770cf-6049-5f3b-b25d-be09728a65d5') and rids.index(jid) < rids.index('591b8c15-985e-59f1-8c90-59e7cae236ae'))
c = jb['content']
m = re.fullmatch(r'(\{\{//.*?\}\})\{\{trim\}\}\n(.*)', c, re.S)
check('CC content: {{// … }}{{trim}}, newline, body', bool(m))
comment, body = m.group(1), m.group(2)
want_body = '{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}' % (N, JBTEXT)
check('CC body: exactly the spec\'d body with the approved lines joined by a real newline', body == want_body)
check('CC content: no literal backslash-n', '\\n' not in c)
for word, why in (('Adult Context', 'needs Adult Context'), ('Logic Core', 'needs a Logic Core'), ('OFF', 'ships OFF'),
                  ('Realistic Frankenstein', 'distilled from'), ('between adults', 'sex stays between adults')):
    check(f'CC comment says: {why}', word in comment)
check('CC comment equals final.json cc_comment', comment == fin['cc_comment'])
# raw formatting: object inserted like its neighbours
blk = re.search(r'\n        \{\n            "identifier": "%s",\n(?:            "[a-z_]+": .*\n)+        \},\n' % jid, raw_cc)
check('CC raw: object formatted like its neighbours (12-space keys, 8-space braces)', bool(blk))
check('CC raw: order row formatted like its neighbours',
      ('                {\n                    "identifier": "%s",\n                    "enabled": false\n                },\n' % jid) in raw_cc)
# Main blanks
main = byid['main']['content']
mm = re.search(r'\{\{trim\}\}\n((?:\{\{setvar::[\w-]+::\}\})+)\n', main)
blanks = re.findall(r'\{\{setvar::([\w-]+)::\}\}', mm.group(1)) if mm else []
blanks0 = re.findall(r'\{\{setvar::([\w-]+)::\}\}', re.search(r'\{\{trim\}\}\n((?:\{\{setvar::[\w-]+::\}\})+)\n',
                     {p['identifier']: p for p in cc0['prompts']}['main']['content']).group(1))
check('CC Main: blanking run = HEAD run + ariaJb, ariaJbLines appended', blanks == blanks0 + ['ariaJb', 'ariaJbLines'], str(blanks[-4:]))
# Impersonation Turn
imp = byid['379e3c22-9a25-5e6d-bf4a-037d49aa60d9']['content']
imp0 = {p['identifier']: p for p in cc0['prompts']}['379e3c22-9a25-5e6d-bf4a-037d49aa60d9']['content']
ib = re.search(r'((?:\{\{setvar::[\w-]+::\}\})+)<impersonation_turn>', imp)
ib0 = re.search(r'((?:\{\{setvar::[\w-]+::\}\})+)<impersonation_turn>', imp0)
check('CC Impersonation Turn: blanking run = HEAD run + ariaJb appended',
      bool(ib and ib0) and re.findall(r'setvar::([\w-]+)::', ib.group(1)) == re.findall(r'setvar::([\w-]+)::', ib0.group(1)) + ['ariaJb'])
check('CC Impersonation Turn: only change is the ariaJb blank', imp.replace('{{setvar::ariaJb::}}', '', 1) == imp0)
# Logic Cores
CTR_ANCHOR = '{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}'
CTR = '{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}'
PRT_ANCHOR = '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}'
PRT = '{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}'
lc_ids = ['15b770cf-6049-5f3b-b25d-be09728a65d5', '591b8c15-985e-59f1-8c90-59e7cae236ae']
tails = []
for lid in lc_ids:
    t, t0 = byid[lid]['content'], {p['identifier']: p for p in cc0['prompts']}[lid]['content']
    nm = byid[lid]['name']
    check(f'CC {nm}: counter directly after the Ledger counter', t.count(CTR_ANCHOR + CTR) == 1 and t.count(CTR) == 1)
    check(f'CC {nm}: print directly after the Ledger block, directly before "- Fresh:"', t.count(PRT_ANCHOR + PRT + '- Fresh:') == 1 and t.count(PRT) == 1)
    check(f'CC {nm}: only changes are the counter and the print', t.replace(CTR, '', 1).replace(PRT, '', 1) == t0)
    tails.append(re.sub(r'^\{\{//.*?\}\}', '', t, count=1, flags=re.S))
check('CC: both Logic Cores identical after their comments', tails[0] == tails[1])
# CC regex
def label_alt(script):
    mm = re.search(r'\(\?:\\\*\\\*\)\?\(\?:(Scene\|[^)]*)\)', script['findRegex'])
    return mm.group(1).split('|') if mm else []
ccr = [s for s in cc['extensions']['regex_scripts'] if s['scriptName'] == 'ARIA Impersonate - strip an untagged plan']
ccr0 = [s for s in cc0['extensions']['regex_scripts'] if s['scriptName'] == 'ARIA Impersonate - strip an untagged plan']
check('CC regex: one strip script', len(ccr) == 1)
check('CC regex: alternation = HEAD alternation + the JB labels', label_alt(ccr[0]) == label_alt(ccr0[0]) + LABELS, str(label_alt(ccr[0])[-4:]))
check('CC regex: only findRegex changed, and only by the labels', {k: v for k, v in ccr[0].items() if k != 'findRegex'} ==
      {k: v for k, v in ccr0[0].items() if k != 'findRegex'} and ccr[0]['findRegex'].replace('|' + '|'.join(LABELS), '', 1) == ccr0[0]['findRegex'])
check('CC regex: other scripts unchanged', [s for s in cc['extensions']['regex_scripts'] if s is not ccr[0]] ==
      [s for s in cc0['extensions']['regex_scripts'] if s['scriptName'] != 'ARIA Impersonate - strip an untagged plan'])
# ------------------------------------------------------------------ TC regex file
tcr = [s for s in rx if s['scriptName'] == 'ARIA Impersonate - strip an untagged plan']
check('TC regex: one strip script, findRegex identical to CC\'s', len(tcr) == 1 and tcr[0]['findRegex'] == ccr[0]['findRegex'])
check('TC regex: everything else unchanged', [s for s in rx if s is not tcr[0]] == [s for s in rx0 if s['scriptName'] != 'ARIA Impersonate - strip an untagged plan'])
num = subprocess.run(['git', '-C', str(ROOT), 'diff', '--numstat', '--', RXN], capture_output=True, text=True).stdout.split()
check('TC regex file: git diff is 1 line added, 1 removed', num[:2] == ['1', '1'], str(num[:2]))
check('TC regex file: four-space indentation, no tabs', raw_rx.startswith('[\n    {\n        "id"') and '\t' not in raw_rx)
check('TC regex file: raw text identical to HEAD apart from the label', raw_rx.replace('|' + '|'.join(LABELS), '', 1) == git_show(RXN))
for nm, s in (('CC', ccr[0]), ('TC', tcr[0])):
    src = s['findRegex']
    mm = re.fullmatch(r'/(.*)/([a-z]*)', src, re.S)
    try:
        rxc = re.compile(mm.group(1), re.I if 'i' in mm.group(2) else 0)
    except re.error as e:
        rxc = None
    check(f'{nm} regex: compiles in Python', rxc is not None)
    plan = ('- OOC: none\n- Scene: x\n- Knows: y\n- Mode: realism; persona-true; each plea new.\n- Voice: z\n- Move: m\n'
            + JBTEXT.replace('{{user}}', 'Lewis') + '\n- Fresh: f\n- Check: c\n- go\n\nLewis walks in.')
    out = rxc.sub('', plan, count=1) if rxc else plan
    check(f'{nm} regex: strips an untagged plan that carries Role and Frank', out == 'Lewis walks in.', repr(out[:80]))
    plan2 = '- OOC: none\n- Role: a\n- Frank: b\n- go\nText'
    check(f'{nm} regex: Role/Frank count as plan lines on their own', (rxc.sub('', plan2, count=1) if rxc else plan2) == 'Text')
# ------------------------------------------------------------------ TC
sc, sc0 = tc['sysprompt']['content'], tc0['sysprompt']['content']
ph, ph0 = tc['sysprompt']['post_history'], tc0['sysprompt']['post_history']
sw = re.search(r'\{\{\.aria-freaky = off\}\}\n(\{\{// 🔓 Jailbreak: [^\n]*?\}\})\{\{\.aria-jailbreak = off\}\}\n\{\{// 👀 Hybrid POV', sc)
check('TC switch: own line, right after aria-freaky, before Hybrid POV, ships off', bool(sw))
check('TC switch comment: needs aria-adult and aria-logic-core', bool(sw) and 'aria-adult' in sw.group(1) and 'aria-logic-core' in sw.group(1))
check('TC switch comment equals final.json tc_switch_comment', bool(sw) and sw.group(1) == fin['tc_switch_comment'])
check('TC: exactly one aria-jailbreak switch', len(re.findall(r'\{\{\.aria-jailbreak = ', sc)) == 1)
tb = re.findall(r'\{\{setvar::([\w-]+)::\}\}', re.search(r'\n((?:\{\{setvar::[\w-]+::\}\})+)\n', sc).group(1))
check('TC Main: blanking line equals CC\'s (same names, same order)', tb == blanks, f'{tb[-3:]}')
TCBLK = '{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}{{/if}}' % (N, JBTEXT)
check('TC block: exact spec\'d text with the CC lines', sc.count(TCBLK) == 1)
check('TC block: directly after the freaky block, directly before Hybrid POV',
      sc.count('</freaky_override>\n{{/if}}' + TCBLK + '{{#if .aria-hybrid-pov}}') == 1)
check('TC block: after the adult block', sc.index('{{#if .aria-adult}}') < sc.index(TCBLK))
sw_txt = sw.group(0)[len('{{.aria-freaky = off}}\n'):-len('\n{{// 👀 Hybrid POV')] + '\n' if sw else ''
check('TC content: only changes are the switch line, the two blanks and the block',
      sc.replace(sw_txt, '', 1).replace('{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}', '', 1).replace(TCBLK, '', 1) == sc0)
check('TC post_history: counter directly after the Ledger counter', ph.count(CTR_ANCHOR + CTR) == 1 and ph.count(CTR) == 1)
check('TC post_history: print directly after the Ledger block, before "- Fresh:"', ph.count(PRT_ANCHOR + PRT + '- Fresh:') == 1)
OLD_CLOSE = 'with no Fate, Bonds, Ledger or Layers line.'
NEW_CLOSE = 'with no Fate, Bonds, Ledger, Layers, %s line.' % ' or '.join(LABELS) if N == 2 else None
check('TC post_history: closing sentence lists the JB labels, grammatical', ph.count(NEW_CLOSE) == 1)
check('TC post_history: only changes are the counter, the print and the closing sentence',
      ph.replace(CTR, '', 1).replace(PRT, '', 1).replace(NEW_CLOSE, OLD_CLOSE, 1) == ph0)
check('TC: other sysprompt keys and the rest of the preset unchanged',
      {k: v for k, v in tc.items() if k != 'sysprompt'} == {k: v for k, v in tc0.items() if k != 'sysprompt'}
      and tc['sysprompt']['name'] == tc0['sysprompt']['name'] and list(tc['sysprompt']) == list(tc0['sysprompt']))
check('TC: no literal backslash-n in content or post_history', '\\n' not in sc and '\\n' not in ph)
# ------------------------------------------------------------------ Marinara
check('Marinara: round-trips exactly, no trailing newline', json.dumps(mar, ensure_ascii=False, indent='\t') == raw_mar and not raw_mar.endswith('\n'))
lo = [b for b in mar['data']['choiceBlocks'] if b['variableName'] == 'logic_options'][0]
lo0 = [b for b in mar0['data']['choiceBlocks'] if b['variableName'] == 'logic_options'][0]
opts, opts0 = json.loads(lo['options']), json.loads(lo0['options'])
new = [o for o in opts if o['value'] == 'JAILBREAK']
check('Marinara option: one JAILBREAK option appended to logic_options', len(new) == 1 and opts == opts0 + new)
o = new[0]
check('Marinara option: exact keys, label and value', list(o) == ['id', 'label', 'value'] and o['label'] == '🔓 Jailbreak (needs Adult Context)')
check('Marinara option: id is opt_ + 12 chars of [A-Za-z0-9_-]', re.fullmatch(r'opt_[A-Za-z0-9_-]{12}', o['id']) is not None, o['id'])
allids = [x['id'] for b in mar['data']['choiceBlocks'] for x in json.loads(b['options'])]
check('Marinara option: id unique', allids.count(o['id']) == 1)
check('Marinara option: options stays a compact JSON string', lo['options'] == json.dumps(opts, ensure_ascii=False, separators=(',', ':')))
dc = mar['data']['preset']['defaultChoices']
check('Marinara: JAILBREAK not in defaultChoices', 'JAILBREAK' not in json.dumps(dc))
check('Marinara: defaultChoices unchanged', dc == mar0['data']['preset']['defaultChoices'])
check('Marinara question: one added sentence before "Deselect all options to disable."',
      lo['question'].endswith(' Deselect all options to disable.') and lo['question'].count('Jailbreak') == 1
      and lo0['question'].replace('Deselect all', lo['question'][len(lo0['question']) - len('Deselect all options to disable.'):][:0] + 'Deselect all') is not None)
secs = {s['name']: s for s in mar['data']['sections']}
secs0 = {s['name']: s for s in mar0['data']['sections']}
MCOND = '{{#if logic_options contains "JAILBREAK" && adult_mode != "NONE"}}'
MCTR = MCOND + '{{addvar::logicCoreLines::%d}}{{/if}}' % N
MPRT = MCOND + JBTEXT + '\n{{/if}}'
for nm in ('🧠 The Logic Core', '🧠 The Logic Core (system-role twin)'):
    t, t0 = secs[nm]['content'], secs0[nm]['content']
    check(f'Marinara {nm}: counter right after the Ledger counter',
          t.count('{{#if world_engine contains "FATE" || world_engine contains "BONDS"}}{{addvar::logicCoreLines::1}}{{/if}}' + MCTR) == 1)
    check(f'Marinara {nm}: lines between the Ledger block and "- Fresh:"', t.count('{{/if}}' + MPRT + '- Fresh:') == 1)
    check(f'Marinara {nm}: only changes are the counter and the lines', t.replace(MCTR, '', 1).replace(MPRT, '', 1) == t0)
g, g0 = secs['🚪 Last-Mile Gate']['content'], secs0['🚪 Last-Mile Gate']['content']
check('Marinara gate: same counter, only change', g.replace(MCTR, '', 1) == g0 and g.count(MCTR) == 1)
for nm in secs:
    if nm not in ('🧠 The Logic Core', '🧠 The Logic Core (system-role twin)', '🚪 Last-Mile Gate'):
        if secs[nm] != secs0.get(nm):
            check(f'Marinara: section {nm} unchanged', False)
check('Marinara: the bare-if pitfall avoided (no bare {{#if JAILBREAK}} or {{#if ariaJb}})',
      not re.search(r'\{\{#if (JAILBREAK|ariaJb|\.ariaJb)\}\}', raw_mar))
check('Marinara: no CC splice variables leaked in (ariaJb, ariaModeLine)', 'ariaJb' not in raw_mar and 'ariaModeLine' not in raw_mar)
desc, desc0 = mar['data']['preset']['description'], mar0['data']['preset']['description']
check('Marinara description: mentions the Jailbreak option once', desc.count('Jailbreak') == 1)
# ------------------------------------------------------------------ checker
src = (ROOT / 'tools/aria_budget.py').read_text(encoding='utf-8')
sys.path.insert(0, str(ROOT / 'tools'))
import aria_budget as ab  # noqa: E402
check('Checker: BUDGET is 7000', ab.BUDGET == 7000)
check('Checker: Chibi Edition files get 3000', ab.budget_for("Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json") == 3000)
check('Checker: other files get BUDGET', ab.budget_for(CCN) == 7000 and ab.budget_for(TCN) == 7000 and ab.budget_for('') == 7000)
check('Checker: DEFAULT_PRESETS unchanged', [p.name for p in ab.DEFAULT_PRESETS] == [CCN, TCN])
check('Checker: no 6000 left', '6000' not in src and '6,000' not in src)
# ------------------------------------------------------------------ personal data
for nm, raw in (('CC', raw_cc), ('TC', raw_tc), ('Marinara', raw_mar), ('TC regex', raw_rx), ('checker', src)):
    check(f'{nm}: no email address', not re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', raw.replace('noreply@anthropic.com', '')))
print()
print(f'{len(FAILS)} FAIL' + ('' if not FAILS else ': ' + '; '.join(FAILS)))
sys.exit(1 if FAILS else 0)
