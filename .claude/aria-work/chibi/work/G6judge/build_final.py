#!/usr/bin/env python3
"""Write $S/chibi/final/G6.json from cand7.json: prompts, tc, tokens, notes, judge_notes."""
import json, sys
sys.path.insert(0, '.')
from rows import rows, paths, CEIL, IDS
from m import t
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
d = json.load(open('cand7.json', encoding='utf-8'))
src = json.load(open('src_g6.json', encoding='utf-8'))
draft = json.load(open(S + '/chibi/drafts/G6.json', encoding='utf-8'))
r, rs, rd = rows(d), rows(src), rows(draft)
p, pd, ps = paths(r), paths(rd), paths(rs)
kit = lambda rr: paths(rr)['GLM'] + rr['FG lines (with Runs)'] + rr['VoiceExtra'] + rr['Hold two lines']
tok = {}
for k, pid in IDS.items():
    tok[pid] = t(d['prompts'][pid]['content'], {'ariaBondsLine': 'x', 'ariaFateLine': 'x'} if k == 'ds' else {})[0]
NAMES = {'claude own': 'Claude 5 own text (ceiling 80)', 'g38 own (gemini38Patch)': 'gemini38Patch, the Gemini 3.8 Flash text (ceiling 50)',
         'gem own': 'Gemini All-In-One own text (ceiling 50)', 'gem lines': 'ariaPatchGate, Gemini All-In-One, 2 lines (ceiling 90)',
         'gem Speech (ariaChopGate)': 'ariaChopGate, Gemini Speech line (replaces the Codex Chop line, 30.5)',
         'glm own': 'GLM own text (ceiling 50)', 'glm lines': 'ariaPatchGate, GLM, 5 lines (ceiling 120)',
         'kimi own': 'Kimi / Qwen own text (ceiling 50)', 'kimi lines': 'ariaPatchGate, Kimi / Qwen, 1 line (ceiling 90)',
         'mpro own': 'MiMo V2.6 Pro own text (ceiling 50)', 'mpro lines': 'ariaPatchGate, MiMo V2.6 Pro, 1 line (ceiling 90)',
         'mflash own': 'MiMo V2.6 Flash own text (ceiling 50)', 'mflash lines': 'ariaPatchGate, MiMo V2.6 Flash, 3 lines (ceiling 90)',
         'ds own (Tally on)': 'DeepSeek own text, Tally on (ceiling 50)', 'ds own (no Tally)': 'DeepSeek own text, Tally off',
         'ds lines': 'ariaPatchGate, DeepSeek, 3 lines (ceiling 90)', 'Tally (Bonds+Fate)': 'ariaPatchTally, Bonds and Fate on (ceiling 55)',
         'Tally (Bonds only)': 'ariaPatchTally, Bonds only', 'Tally (Fate only)': 'ariaPatchTally, Fate only', 'Joins': 'ariaPatchJoins (ceiling 25)',
         'FG lines (with Runs)': 'ariaFlashGate with Runs (ceiling 90)', 'FG lines (no Runs)': 'ariaFlashGate without Runs (DeepSeek on)',
         'VoiceExtra': 'ariaVoiceExtra (ceiling 12)', 'Hold two lines': 'ariaHoldLine + ariaHoldGate (ceiling 55)',
         '  HoldLine': 'ariaHoldLine', '  HoldGate': 'ariaHoldGate'}
for k, v in r.items():
    tok[NAMES[k]] = v
for sw in ('aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro', 'aria-patch-mimo-flash', 'aria-patch-deepseek', 'aria-flash-gate', 'aria-character-hold'):
    tok[f'tc.module_{sw} (own text, switch on' + (', Bonds and Fate on)' if sw == 'aria-patch-deepseek' else ')')] = t('{{.' + sw + ' = on}}' + d['tc']['module_' + sw], {'ariaBondsLine': 'x', 'ariaFateLine': 'x'} if sw == 'aria-patch-deepseek' else {})[0]
    tok[f'tc.switch_comment_{sw}'] = 0
grp = sum(v for k, v in r.items() if k in CEIL)
tok['group sum of the ceiling rows (sum of ceilings 1237; lines counted once, as in the draft)'] = grp
for k, v in p.items():
    tok[f'path: {k} (own text + 2 x plan/gate lines)'] = v
tok['kitted-out G6 share: GLM path + Flash Gate with Runs + ariaVoiceExtra + Hold (table share 447)'] = kit(r)
tok['frozen checker, CC everything ON with G1-G3 finals, G4/G5 drafts, a 55-token JB stand-in and this G6'] = 3212
d['tokens'] = tok
d['notes'] = open('notes.txt', encoding='utf-8').read().strip()
d['judge_notes'] = open('judge_notes.txt', encoding='utf-8').read().strip()
out = S + '/chibi/final/G6.json'
json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', out)
print(f'group {grp}  kitted {kit(r)} (draft {kit(rd)}, source {kit(rs)})')
for k, v in sorted(p.items(), key=lambda x: -x[1]): print(f'  {v:7.2f} {k}   draft {pd[k]:7.2f}  source {ps[k]:7.2f}')
