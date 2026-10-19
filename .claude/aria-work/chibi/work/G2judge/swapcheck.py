"""Swap a G2 candidate into in-memory copies of the snapshot CC and TC presets, run the frozen checker's analyses,
and print rendered Codex and gate texts for a few configurations."""
import json, sys, random, io, contextlib
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
from paths import *
import aria_budget as ab

cand = json.load(open(sys.argv[1], encoding='utf-8'))
show = len(sys.argv) > 2

cc = json.load(open(CC, encoding='utf-8'))
by = {p['identifier']: p for p in cc['prompts']}
for pid in (CODEX, GATE):
    by[pid]['content'] = cand['prompts'][pid]['content']

tc = json.load(open(TC, encoding='utf-8'))
c = tc['sysprompt']['content']
a = c.index('{{setvar::ariaEchoGate::- ')
b = c.index('</anti_slop>') + len('</anti_slop>')
cx = cand['prompts'][CODEX]['content']
body = cx[cx.index('{{trim}}\n') + len('{{trim}}\n'):]
tc['sysprompt']['content'] = c[:a] + body + c[b:]
ph = tc['sysprompt']['post_history']
i = ph.index('<final_gate>')
tc['sysprompt']['post_history'] = ph[:i] + cand['tc']['post_history_gate']

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    tcc, ecc = ab.analyse_cc(cc)
    ttc, etc_ = ab.analyse_tc(tc)
print('CC totals:', tcc)
print('CC errors:', ecc or 'none')
print('TC totals:', ttc)
print('TC errors:', etc_ or 'none')

# source totals for comparison
cc0 = json.load(open(CC, encoding='utf-8')); tc0 = json.load(open(TC, encoding='utf-8'))
with contextlib.redirect_stdout(io.StringIO()):
    t0, e0 = ab.analyse_cc(cc0); u0, f0 = ab.analyse_tc(tc0)
print('source CC totals:', t0, 'errors:', e0 or 'none')
print('source TC totals:', u0, 'errors:', f0 or 'none')

if show:
    order = [r['identifier'] for r in cc['prompt_order'][1]['order']]
    allids = {p['identifier'] for p in cc['prompts']}
    def run(enabled, label):
        r, st = ab.simulate_cc(cc, enabled, seed=1)
        print(f'\n######## CC render: {label}')
        print(r.get(CODEX, '(codex off)'))
        print('--------')
        print(r.get(GATE, '(gate off)'))
    base = {r['identifier'] for r in cc['prompt_order'][1]['order'] if r['enabled']}
    run(base, 'shipped default')
    names = {p['identifier']: p.get('name', '') for p in cc['prompts']}
    pick = lambda pre: {pid for pid in allids if names[pid].startswith(pre)}
    full = base | pick('🎲') | pick('⏰') | pick('🥰') | pick('👀') | pick('🔞') | pick('🔦') | pick('🧷') | pick('🏷️') | {'1f2e1f97-1cde-5d46-8eb0-87e2fe55f916'}
    run(full, 'everything plus GLM patch, Flash Gate, Hold, Tags')
    gem = base | {'ac96376e-5777-595b-8f48-359f864b0685'}
    r, st = ab.simulate_cc(cc, gem, seed=1)
    print('\n######## CC gate with the Gemini patch')
    print(r[GATE])
    rt, _ = ab.simulate_tc(tc, {}, seed=1)
    print('\n######## TC post-history (shipped switches)')
    print(rt['Post-History'])
    on = {s: 'on' for s in dict(ab.SWITCH.findall(tc['sysprompt']['content'])) if not s.startswith('aria-patch')}
    on['aria-patch-deepseek'] = 'on'
    rt, _ = ab.simulate_tc(tc, on, seed=1)
    ph = rt['Post-History']
    print('\n######## TC post-history gate (everything on, DeepSeek patch)')
    print(ph[ph.index('<final_gate>'):])
