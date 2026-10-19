"""Exact wiring check for a G3 file: skeleton equals source skeleton + the two JB.md additions; JB strings exact."""
import json, sys
S = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work"
sys.path.insert(0, S + "/spec")
from skeleton import skeleton
f = sys.argv[1]
d = json.load(open(f, encoding='utf-8'))
cc = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
tc = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
by = {p['identifier']: p for p in cc['prompts']}
LEDGER_CTR = '{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}{{#if .ariaHoldLine}}'
JB_CTR = '{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}'
LEDGER_PRT = '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}- Fresh:'
JB_PRT = '{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}'
CTR = '{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}{{#if .ariaHoldLine}}'
PRT = '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}- Fresh:'
CLOSE = "For a message written as {{user}}, plan only {{user}}'s move, with no Fate, Bonds, Ledger, Layers, Role or Frank line."
def with_jb(src):
    assert src.count(LEDGER_CTR) == 1 and src.count(LEDGER_PRT) == 1
    src = src.replace(LEDGER_CTR, LEDGER_CTR.replace('{{/if}}{{#if .ariaHoldLine}}', '{{/if}}' + JB_CTR + '{{#if .ariaHoldLine}}'))
    src = src.replace(LEDGER_PRT, LEDGER_PRT.replace('{{/if}}- Fresh:', '{{/if}}' + JB_PRT + '- Fresh:'))
    return src
ok = True
for pid in ['15b770cf-6049-5f3b-b25d-be09728a65d5', '591b8c15-985e-59f1-8c90-59e7cae236ae']:
    src, dr = by[pid]['content'], d['prompts'][pid]['content']
    exp = with_jb(src)
    a, b = skeleton(exp), skeleton(dr)
    print(pid[:8], 'skeleton == source+JB:', a == b, '| CTR once:', dr.count(CTR) == 1, '| PRT once:', dr.count(PRT) == 1,
          '| one ariaJbLines read:', dr.count('{{getvar::ariaJbLines}}') == 1, '| one ariaJb print:', dr.count('{{getvar::ariaJb}}') == 1,
          '| name unchanged:', d['prompts'][pid]['name'] == by[pid]['name'])
    ok &= a == b
tail = lambda t: t.split('}}{{trim}}', 1)[1]
p, t = (d['prompts'][k]['content'] for k in ['15b770cf-6049-5f3b-b25d-be09728a65d5', '591b8c15-985e-59f1-8c90-59e7cae236ae'])
print('twins identical after comments:', tail(p) == tail(t))
ph = tc['sysprompt']['post_history']
src_seg = ph[:ph.index('<final_gate>')]
dseg = d['tc']['post_history_logic_core']
exp = with_jb(src_seg)
print('TC skeleton == source+JB:', skeleton(exp) == skeleton(dseg), '| CTR', dseg.count(CTR) == 1, '| PRT', dseg.count(PRT) == 1, '| CLOSE', dseg.count(CLOSE) == 1)
print('TC ends like source:', dseg.endswith('</logic_core>{{/if}}\n{{/if}}'), '| starts with comment+trim+newline+if:', '}}{{trim}}\n{{#if .aria-logic-core}}' in dseg)
# The TC Logic Core body (after the wrapper opening) equals the CC body plus the two TC additions
cc_body = tail(p)
tc_body = dseg.split('}}{{trim}}\n', 1)[1]
assert tc_body.startswith('{{#if .aria-logic-core}}') and tc_body.endswith('\n{{/if}}')
inner = tc_body[len('{{#if .aria-logic-core}}'):-len('\n{{/if}}')]
print('CC body starts with newline:', cc_body.startswith('\n'))
x = inner.replace('{{getvar::ariaPatchTally}} A message written as {{user}} skips it.\n', '{{getvar::ariaPatchTally}}\n')
x = x.replace(' ' + CLOSE, '')
print('TC inner == CC body (minus TC-only notes):', x == cc_body[1:])
sys.exit(0 if ok else 1)
