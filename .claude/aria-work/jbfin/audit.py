#!/usr/bin/env python3
"""Wiring audit for the JB (Role and Frank) against JB.md's Wiring in CC / Wiring in TC / Checker change.
Run: python3 -I audit.py   (prints PASS or FAIL per item; exit 1 on any FAIL)"""
import json, re, subprocess, sys, uuid
from pathlib import Path

ROOT = Path("/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA")
S = ROOT / ".claude/aria-work"
CCP = ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TCP = ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
RXP = ROOT / "regex/ARIA 1.0 Regex Scripts (Text Completions).json"
CHK = ROOT / "tools/aria_budget.py"

fin = json.loads((S / "jb/final.json").read_text(encoding='utf-8'))
LINES = fin['lines']
LABELS = fin['labels']
N = len(LINES)

raw_cc = CCP.read_text(encoding='utf-8')
raw_tc = TCP.read_text(encoding='utf-8')
raw_rx = RXP.read_text(encoding='utf-8')
cc = json.loads(raw_cc)
tc = json.loads(raw_tc)
rx = json.loads(raw_rx)

results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))


P = cc['prompts']
byid = {p['identifier']: p for p in P}
by8 = {p['identifier'][:8]: p for p in P}
hold = by8['dc8b1acb']
freaky = by8['4537b57d']
jbs = [p for p in P if p['name'].startswith('🔓')]
check('CC: exactly one JB prompt object', len(jbs) == 1, f'found {len(jbs)}')
jb = jbs[0]
jid = jb['identifier']

# ---- the object: key set, key order, values
check('CC object: key set and key order equal Character Hold\'s', list(jb.keys()) == list(hold.keys()),
      f'{list(jb.keys())} vs {list(hold.keys())}')
for k in hold:
    if k in ('identifier', 'name', 'content'):
        continue
    check(f'CC object: {k} equals Hold\'s ({hold[k]!r})', jb.get(k) == hold[k], f'JB has {jb.get(k)!r}')
check('CC object: role system and injection_position 0', jb['role'] == 'system' and jb['injection_position'] == 0)
u = None
try:
    u = uuid.UUID(jid)
except Exception as e:
    pass
check('CC object: identifier is a uuid4 string', u is not None and u.version == 4 and str(u) == jid, jid)
check('CC object: identifier unique in prompts[]', sum(1 for p in P if p['identifier'] == jid) == 1)
check('CC object: name', jb['name'] == '🔓 Jailbreak (needs Adult Context)', jb['name'])

# ---- position in prompts[]
ids = [p['identifier'] for p in P]
fi = ids.index(freaky['identifier'])
check('CC prompts[]: right after Freaky Override', ids.index(jid) == fi + 1, f'Freaky {fi}, JB {ids.index(jid)}')

# ---- prompt_order
po1 = cc['prompt_order'][1]['order']
rows = [r['identifier'] for r in po1]
check('CC prompt_order[1]: JB appears exactly once', rows.count(jid) == 1)
ri = rows.index(jid)
check('CC prompt_order[1]: row right after Freaky\'s row', ri == rows.index(freaky['identifier']) + 1, f'JB row {ri}')
check('CC prompt_order[1]: row is {"identifier", "enabled": false} in that key order',
      po1[ri] == {'identifier': jid, 'enabled': False} and list(po1[ri].keys()) == ['identifier', 'enabled'])
check('CC prompt_order[0] untouched (does not name JB)', all(r['identifier'] != jid for r in cc['prompt_order'][0]['order']))
check('CC prompt_order[1] still names every prompt exactly once', sorted(rows) == sorted(ids))
raw_row = '                {\n                    "identifier": "%s",\n                    "enabled": false\n                },\n' % jid
check('CC prompt_order raw row formatted like neighbours', raw_row in raw_cc)

# ---- content
c = jb['content']
m = re.fullmatch(r'(\{\{//[^\n]*?\}\})\{\{trim\}\}\n(.*)', c, re.S)
check('CC content: a {{// … }}{{trim}} comment, a newline, then the body', bool(m))
comment, body = (m.group(1), m.group(2)) if m else ('', '')
for word, why in (('Adult Context', 'needs Adult Context'), ('Logic Core', 'needs a Logic Core'), ('OFF', 'ships OFF'),
                  ('Realistic Frankenstein', 'what it is distilled from')):
    check(f'CC comment mentions {why}', word in comment)
check('CC comment equals the approved cc_comment', comment == fin['cc_comment'])
want_body = '{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}' % (N, '\n'.join(LINES))
check('CC body: {{#if .ariaModeLine}}{{setvar::ariaJbLines::N}}{{setvar::ariaJb::<lines joined by a real newline>}}{{/if}}',
      body == want_body)
check('CC content: no literal backslash-n pair anywhere', '\\n' not in c, f'{c.count(chr(92) + "n")} pair(s)')
check('CC body: N equals the number of lines', N == 2 and body.startswith('{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}'))

# ---- Main Prompt blanks
main = byid['main']
mm = re.search(r'\{\{trim\}\}\n((?:\{\{setvar::[\w-]+::\}\})+)\n\{\{trim\}\}\n', main['content'])
check('CC Main: has a first-line blanking run', bool(mm))
run = mm.group(1) if mm else ''
blanks = re.findall(r'\{\{setvar::([\w-]+)::\}\}', run)
check('CC Main: the run ends with {{setvar::ariaJb::}}{{setvar::ariaJbLines::}} (appended)', blanks[-2:] == ['ariaJb', 'ariaJbLines'], f'last two: {blanks[-2:]}')
check('CC Main: each JB blank appears once', blanks.count('ariaJb') == 1 and blanks.count('ariaJbLines') == 1)
check('CC Main: no duplicate blanks in the run', len(blanks) == len(set(blanks)))

# ---- Logic Cores
lcs = [by8['15b770cf'], by8['591b8c15']]
CTR = '{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}{{#if .ariaHoldLine}}'
PRT = '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}- Fresh:'
for lc in lcs:
    t = lc['content']
    nm = lc['name']
    check(f'CC {nm}: counter right after the Ledger counter', t.count(CTR) == 1 and t.count('{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}') == 1)
    check(f'CC {nm}: print after the Ledger block and before "- Fresh:" (newline pattern of its neighbours)', t.count(PRT) == 1 and t.count('{{getvar::ariaJb}}') == 1)
tail = lambda t: t.split('}}{{trim}}', 1)[1]
check('CC Logic Cores: identical after their comments', tail(lcs[0]['content']) == tail(lcs[1]['content']))

# ---- Impersonation Turn
imp = by8['379e3c22']
ib = re.search(r'\{\{trim\}\}\n((?:\{\{setvar::[\w-]+::\}\})+)<impersonation_turn>', imp['content'])
check('CC Impersonation Turn: blanking run found', bool(ib))
iblanks = re.findall(r'\{\{setvar::([\w-]+)::\}\}', ib.group(1)) if ib else []
check('CC Impersonation Turn: {{setvar::ariaJb::}} in the run (appended, once)', iblanks[-1:] == ['ariaJb'] and iblanks.count('ariaJb') == 1, str(iblanks))
check('CC Impersonation Turn: does not blank ariaJbLines (the count is guarded by ariaJb)', 'ariaJbLines' not in iblanks)

# ---- CC regex
NAME = 'ARIA Impersonate - strip an untagged plan'
ccs = [s for s in cc['extensions']['regex_scripts'] if s['scriptName'] == NAME]
check('CC regex: one script', len(ccs) == 1)
alt = re.search(r'\((?:\?:)?(Scene\|[^)]*)\)', ccs[0]['findRegex']).group(1).split('|')
check('CC regex: alternation ends ...|Joins|Role|Frank', alt[-3:] == ['Joins'] + LABELS, str(alt[-3:]))
check('CC regex: each JB label once', all(alt.count(l) == 1 for l in LABELS))

# ---- TC regex
tcr = [s for s in rx if s['scriptName'] == NAME]
check('TC regex: one script, findRegex equals CC\'s', len(tcr) == 1 and tcr[0]['findRegex'] == ccs[0]['findRegex'])
check('TC regex file: indentation is four spaces (no tabs)', '\t' not in raw_rx.split('"findRegex"')[0] and raw_rx.startswith('[\n    {\n        "id"'))
diff_stat = subprocess.run(['git', '-C', str(ROOT), 'diff', '--numstat', '--', str(RXP)], capture_output=True, text=True).stdout.split()
check('TC regex file: git diff --numstat shows exactly 1 added and 1 removed line', diff_stat[:2] == ['1', '1'], str(diff_stat[:2]))
alt_re = re.compile(re.fullmatch(r'/(.*)/([a-z]*)', tcr[0]['findRegex'], re.S).group(1), re.I)
check('TC regex: compiles in Python', alt_re is not None)

# ---- TC
s = tc['sysprompt']['content']
ph = tc['sysprompt']['post_history']
SW = '{{.aria-freaky = off}}\n{{// 🔓 Jailbreak: '
check('TC switch: right after the aria-freaky switch', s.count(SW) == 1)
sw = re.search(r'(\{\{// 🔓 Jailbreak: [^\n]*?\}\})\{\{\.aria-jailbreak = off\}\}\n', s)
check('TC switch: {{// … }}{{.aria-jailbreak = off}} on its own line', bool(sw))
check('TC switch comment equals the approved tc_switch_comment', bool(sw) and sw.group(1) == fin['tc_switch_comment'])
check('TC switch comment mentions aria-adult and aria-logic-core', bool(sw) and 'aria-adult' in sw.group(1) and 'aria-logic-core' in sw.group(1))
check('TC switch: followed by the Hybrid POV switch', '{{.aria-jailbreak = off}}\n{{// 👀 Hybrid POV:' in s)
tm = re.search(r'\{\{setvar::ariaDice::\}\}((?:\{\{setvar::[\w-]+::\}\})+)', s)
tb = re.findall(r'\{\{setvar::([\w-]+)::\}\}', tm.group(0)) if tm else []
check('TC Main: blanking line ends with {{setvar::ariaJb::}}{{setvar::ariaJbLines::}} (appended)', tb[-2:] == ['ariaJb', 'ariaJbLines'], f'last two: {tb[-2:]}')
check('TC Main: blanking line has the same blanks, in the same order, as CC\'s', tb == blanks, f'TC {len(tb)} vs CC {len(blanks)}')
want_blk = '{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}{{/if}}' % (N, '\n'.join(LINES))
check('TC block: exact text of the spec\'d block, same lines as CC', s.count(want_blk) == 1)
check('TC block: right after the freaky block, nothing between (no stray newline), then the Hybrid POV block',
      s.count('</freaky_override>\n{{/if}}' + want_blk + '{{#if .aria-hybrid-pov}}') == 1)
check('TC block: after the adult and freaky module blocks',
      s.index('{{#if .aria-adult}}') < s.index('{{#if .aria-freaky}}') < s.index(want_blk) < s.index('{{#if .aria-hybrid-pov}}'))
check('TC block: no literal backslash-n pair in sysprompt.content or post_history', '\\n' not in s and '\\n' not in ph)
check('TC post_history: counter right after the Ledger counter', ph.count(CTR) == 1)
check('TC post_history: print after the Ledger block, before "- Fresh:"', ph.count(PRT) == 1)
want_close = "For a message written as {{user}}, plan only {{user}}'s move, with no Fate, Bonds, Ledger, Layers, Role or Frank line."
check('TC post_history: closing sentence lists Role and Frank and stays grammatical', ph.count(want_close) == 1)
check('TC post_history: still inside {{#if .aria-logic-core}}…{{/if}} before <final_gate>',
      ph.index('{{#if .aria-logic-core}}') < ph.index('{{getvar::ariaJb}}') < ph.index('{{/if}}<final_gate>'))
check('TC sysprompt/post_history: other keys unchanged', list(tc['sysprompt'].keys()) == ['name', 'content', 'post_history'])

# ---- checker
src = CHK.read_text(encoding='utf-8')
check('Checker: BUDGET = 7000', re.search(r'^BUDGET = 7000$', src, re.M) is not None)
sys.path.insert(0, str(ROOT / 'tools'))
import importlib
ab = importlib.import_module('aria_budget')
check('Checker: budget_for gives 3000 for any filename containing "Chibi Edition"',
      ab.budget_for('Aria 1.0 Chibi Edition — (Chat Completions).json') == 3000 and ab.budget_for('x Chibi Edition y') == 3000)
check('Checker: budget_for keeps BUDGET (7000) for every other preset',
      ab.budget_for(CCP.name) == 7000 and ab.budget_for(TCP.name) == 7000 and ab.budget_for('') == 7000 and ab.BUDGET == 7000)
check('Checker: error messages name the budget that applies',
      src.count("over the {budget_for(filename)} budget") == 2 and 'over the {BUDGET} budget' not in src)
check('Checker: DEFAULT_PRESETS unchanged (CC + TC only)',
      'DEFAULT_PRESETS = [\n    ROOT / "Aria\'s Realistic Intelligence Assistance 1.0 — (Chat Completions).json",\n    ROOT / "Aria\'s Realistic Intelligence Assistance 1.0 — (Text Completions).json",\n]' in src)
check('Checker: main() passes the filename to both analysers', '(analyse_tc if \'sysprompt\' in preset else analyse_cc)(preset, path.name)' in src)
check('Checker: budget_for is separated from neighbouring top-level code by two blank lines',
      re.search(r'\n\n\ndef budget_for\(filename\):\n(?:    .*\n)+\n\n(?=\S)', src) is not None)

# ---- print
bad = 0
for name, ok, detail in results:
    if not ok:
        bad += 1
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok or not detail else f'   [{detail}]'))
print(f'\n{len(results) - bad} PASS, {bad} FAIL of {len(results)}')
sys.exit(1 if bad else 0)
