import json, re, sys
from m import *
import cand
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
CC = S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
cc = json.load(open(CC, encoding='utf-8'))
by = {p['identifier'][:8]: p for p in cc['prompts']}

def vars_of(body, state=None):
    st = dict(state or {})
    out = ab.render(body, st, random.Random(1))
    sets = {k: v for k, v in st.items() if isinstance(v, str) and v and (state or {}).get(k) != v}
    return out, sets

def tk(s): return len(s) / 4

rows = []
def row(name, val, target):
    flag = 'ok' if val <= target + 1e-9 else f'OVER +{val-target:.2f}'
    print(f'{val:7.2f} / {target:<4}  {name:44} {flag}')
    rows.append((name, val, target))

B = cand.B
# Claude
out, s = vars_of(B['b59a2ad1']); row('Claude 5 own', tk(out), 80)
out, s = vars_of(B['333dbbed']); row('Gemini 3.8 Flash Method (own)', tk(s['gemini38Patch']), 50)
out, s = vars_of(B['ac96376e'], {'gemini38Patch': ''}); row('Gemini AIO own (no Method)', tk(out), 50); row('Gemini AIO gate lines', tk(s['ariaPatchGate']), 90); row('Gemini AIO ariaChopGate (<=30)', tk(s['ariaChopGate']), 30)
out, s = vars_of(B['1f2e1f97']); row('GLM own', tk(out), 50); row('GLM 5 lines', tk(s['ariaPatchGate']), 120)
out, s = vars_of(B['9bb6c2b0']); row('Kimi/Qwen own', tk(out), 50); row('Kimi/Qwen gate', tk(s['ariaPatchGate']), 90)
out, s = vars_of(B['33f92483']); row('MiMo Pro own', tk(out), 50); row('MiMo Pro gate', tk(s['ariaPatchGate']), 90)
out, s = vars_of(B['3a027832']); row('MiMo Flash own', tk(out), 50); row('MiMo Flash gate', tk(s['ariaPatchGate']), 90)
for lab, st in (('both', {'ariaBondsLine': 'x', 'ariaFateLine': 'x'}), ('bonds', {'ariaBondsLine': 'x'}), ('fate', {'ariaFateLine': 'x'}), ('none', {})):
    out, s = vars_of(B['e04b9c2b'], st)
    if lab == 'both':
        row('DeepSeek own (Tally on)', tk(out), 50); row('DeepSeek gate', tk(s['ariaPatchGate']), 90); row('DeepSeek Joins', tk(s['ariaPatchJoins']), 25)
        row('DeepSeek Tally (both)', tk(s['ariaPatchTally']), 55)
    elif lab != 'none':
        print(f'        Tally {lab}: {tk(s["ariaPatchTally"]):.2f}')
    else:
        print(f'        DeepSeek own (no Tally): {tk(out):.2f}')
out, s = vars_of(B['2e3e7f63']); row('Flash Gate (with Runs)', tk(s['ariaFlashGate']), 90); row('ariaVoiceExtra', tk(s['ariaVoiceExtra']), 12)
out, s = vars_of(B['2e3e7f63'], {'ariaPatchJoins': 'x'}); print(f'        Flash Gate without Runs: {tk(s["ariaFlashGate"]):.2f}')
out, s = vars_of(B['dc8b1acb']); row('Hold two lines', tk(s['ariaHoldLine']) + tk(s['ariaHoldGate']), 55); print(f"        Hold plan {tk(s['ariaHoldLine']):.2f} gate {tk(s['ariaHoldGate']):.2f}")
print()
over = sum(max(0, v - t) for _, v, t in rows); under = sum(max(0, t - v) for _, v, t in rows)
print(f'rows over by {over:.1f} in total; rows under by {under:.1f}; net {over - under:+.1f}')
