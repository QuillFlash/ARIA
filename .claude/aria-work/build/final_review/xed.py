import json, sys, re, difflib
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
sys.path.insert(0, R + '/tools')
import aria_budget as ab
C = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"))
T = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"))
prompts = {p['identifier']: p for p in C['prompts']}; nm = {k: v.get('name', '') for k, v in prompts.items()}
order = [r['identifier'] for r in C['prompt_order'][1]['order']]
def pid(pre): 
    m = [p for p in prompts if nm[p].startswith(pre)]; assert len(m) == 1, (pre, m); return m[0]
MAP = {'aria-logic-core': pid('🧠 The Logic Core') if False else [p for p in prompts if nm[p] == '🧠 The Logic Core'][0], 'aria-thinking-tags': pid('🏷️'), 'aria-adult': pid('🔞'), 'aria-freaky': pid('😈'),
       'aria-jailbreak': pid('🔓'), 'aria-hybrid-pov': pid('👀'), 'aria-npc-voice': pid('🎭'), 'aria-anthro': pid('🐺'), 'aria-scent': pid('👃'),
       'aria-time-place': pid('⏰'), 'aria-fate': pid('🎲'), 'aria-bonds': pid('🥰'), 'aria-patch-glm': pid('🩹 Model Patch: GLM'),
       'aria-patch-kimi-qwen': pid('🩹 Model Patch: Kimi'), 'aria-patch-mimo-pro': pid('🩹 Model Patch: MiMo V2.6 Pro'), 'aria-patch-mimo-flash': pid('🩹 Model Patch: MiMo V2.6 Flash'),
       'aria-patch-deepseek': pid('🩹 Model Patch: DeepSeek'), 'aria-flash-gate': pid('🔦'), 'aria-character-hold': pid('🧷')}
ALWAYS = [p for p in order if nm[p].startswith(('⚡', '🖋️', '🎬', '📖', '🍃', '🚪'))]
def cc_render(ov, seed=1):
    en = set(ALWAYS) | {MAP[s] for s, v in ov.items() if v == 'on'}
    r, _ = ab.simulate_cc(C, en, seed)
    return r
def tc_render(ov, seed=1):
    return ab.simulate_tc(T, ov, seed)[0]
if __name__ == '__main__':
    sh = dict(ab.SWITCH.findall(T['sysprompt']['content']))
    print('ALWAYS:', [nm[p] for p in ALWAYS])
    ov = {s: 'on' for s in sh} | {p: 'off' for p in sh if p.startswith('aria-patch')} | {'aria-patch-deepseek': 'on', 'aria-freaky':'on'}
    c = cc_render(ov); t = tc_render(ov)
    sysc = '\n'.join(c[p] for p in order if p in c and (prompts[p].get('injection_position') or 0) == 0)
    norm = lambda s: re.sub(r'\n+', '\n', s).strip()
    for l in difflib.unified_diff(norm(sysc).split('\n'), norm(t['System Prompt']).split('\n'), 'cc', 'tc', lineterm='', n=0): print('SYS', l[:250])
    inchat = '\n'.join(c[p] for p in order if p in c and (prompts[p].get('injection_position') or 0) == 1)
    for l in difflib.unified_diff(norm(inchat).split('\n'), norm(t['Post-History']).split('\n'), 'cc', 'tc', lineterm='', n=0): print('POST', l[:300])
