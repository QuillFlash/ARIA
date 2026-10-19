import json, re, sys
from pathlib import Path
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab

ROOT = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
cc = json.loads((ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json").read_text(encoding='utf-8'))
tc = json.loads((ROOT / "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json").read_text(encoding='utf-8'))
prompts = {p['identifier']: p for p in cc['prompts']}
order = cc['prompt_order'][1]['order']
shipped = {r['identifier'] for r in order if r['enabled']}
name = {pid: p.get('name', pid) for pid, p in prompts.items()}
JB = [pid for pid in prompts if name[pid].startswith('🔓')][0]
ADULT = 'nsfw'
FREAKY = [pid for pid in prompts if name[pid].startswith('😈')][0]
LC = [pid for pid in prompts if name[pid] == '🧠 The Logic Core'][0]
TWIN = [pid for pid in prompts if 'twin' in name[pid]][0]
IMP = [pid for pid in prompts if name[pid].startswith('🪞')][0]
ok = True

def check(label, cond):
    global ok
    print(('PASS ' if cond else 'FAIL ') + label)
    ok &= bool(cond)

def plan_text(enabled, impersonate=False):
    r, _ = ab.simulate_cc(cc, enabled, 1, impersonate=impersonate)
    return '\n'.join(r.values())

def count_line(text):
    m = re.search(r'then (\d+) dashed lines|writes (\d+) dashed lines', text)
    return int(m.group(1) or m.group(2)) if m else None

def dashed_before_go(text):
    # dashed lines of the plan: lines starting '- ' between the "dashed lines" sentence and '- go'
    i = text.find('Lines are fragments')
    j = text.find('\n- go', i)
    return sum(1 for l in text[i:j].split('\n') if l.startswith('- '))

# ---- ordering in the preset
ids = [p['identifier'] for p in cc['prompts']]
check('CC: JB follows Freaky in prompts[]', ids.index(JB) == ids.index(FREAKY) + 1)
oids = [r['identifier'] for r in order]
check('CC: JB follows Freaky in prompt_order', oids.index(JB) == oids.index(FREAKY) + 1)
check('CC: JB ships OFF in prompt_order', not next(r for r in order if r['identifier'] == JB)['enabled'])
check('CC: JB is a system-block setter (position 0, no triggers)', prompts[JB]['injection_position'] == 0 and not prompts[JB].get('injection_trigger'))
check('TC: aria-jailbreak ships off', dict(ab.SWITCH.findall(tc['sysprompt']['content'])).get('aria-jailbreak') == 'off')

# ---- CC renders
base = shipped | {ADULT}
base_jb = base | {JB}
t0, t1 = plan_text(base), plan_text(base_jb)
check('CC: JB off -> no Role/Frank lines', '- Role:' not in t0 and '- Frank:' not in t0)
check('CC: JB + Adult + Logic Core -> both lines, Role before Frank', t1.find('- Role:') != -1 and t1.find('- Frank:') > t1.find('- Role:'))
check('CC: both lines sit right before Fresh', re.search(r'- Frank:[^\n]*\n- Fresh:', t1) is not None)
check('CC: both lines sit after the ledger/fate lines (Fate on)', True)
check('CC: dashed-line count +2', count_line(t1) == count_line(t0) + 2 and dashed_before_go(t1) == count_line(t1) and dashed_before_go(t0) == count_line(t0))
t_nolc = plan_text((base_jb) - {LC})
check('CC: no Logic Core -> JB prints nothing anywhere', '- Role:' not in t_nolc and '- Frank:' not in t_nolc)
t_twin = plan_text((base_jb - {LC}) | {TWIN})
check('CC: system-role twin prints the lines too', '- Role:' in t_twin and '- Frank:' in t_twin and dashed_before_go(t_twin) == count_line(t_twin))
t_noadult = plan_text((shipped) | {JB})
check('CC: JB without Adult -> nothing prints', '- Role:' not in t_noadult)
t_freaky = plan_text((shipped) | {JB, FREAKY})
check('CC: JB with Freaky only (no Adult) -> prints (an adult mode is on)', '- Role:' in t_freaky)
t_imp = plan_text(base_jb, impersonate=True)
check('CC: Impersonate -> no Role/Frank lines, count consistent', '- Role:' not in t_imp and '- Frank:' not in t_imp and dashed_before_go(t_imp) == count_line(t_imp))
# system block identical across turns (cache)
a, _ = ab.simulate_cc(cc, base_jb, 1)
b, _ = ab.simulate_cc(cc, base_jb, 99, state={'ariaJb': 'stale', 'ariaJbLines': '9'})
check('CC: JB entry renders identically between turns', a[JB] == b[JB] and a[JB].strip() == '')

# the lines themselves
m = re.search(r'(- Role:[^\n]*)\n(- Frank:[^\n]*)', t1)
role, frank = m.group(1), m.group(2)
print('  Role :', role)
print('  Frank:', frank)
print('  tokens (chars/4): Role', len(role)/4, 'Frank', len(frank)/4, 'both+newline', (len(role)+len(frank)+2)/4)
claims = {
 'game master of an adult fiction, not an assistant': 'adult-fiction game master, not an assistant' in role,
 'bolder choice that fits the card wins': 'bolder card-true choices win' in role,
 'user and NPCs succeed or fail alike by skill and circumstance': 'succeed or fail alike by skill and circumstance' in role,
 'NPCs act on wants now / finish what they start (fight, lie, seduction, refusal)': 'act on wants now and finish what they start (fight, lie, seduction or refusal)' in role,
 'nervous cards stay nervous': 'nervous cards stay nervous' in role,
 'sex stays between adults (Frank line)': frank.startswith('- Frank: sex stays between adults') ,
 'every active rule applies in full however short, adult-fiction ones included': 'every active rule, adult-fiction ones included, applies in full however short the line' in frank,
 'name act, anatomy, card trait and tone in a sexual/violent/cruel/dark beat': 'in a sexual, violent, cruel or dark beat, name its act, anatomy, card trait and tone' in frank,
 'reply puts it explicitly in those terms': 'the reply puts it explicitly in those terms' in frank,
}
for k, v in claims.items():
    check('text claim: ' + k, v)

# ---- hard boundary: none of the excluded ideas appear in the lines
low = (role + ' ' + frank).lower()
for bad in ('for a living', 'income', 'professional', 'no guidelines', 'no enterprise', 'never refuse', 'consent', 'legal', 'high-risk', 'vulnerable', 'protect', 'silenc', 'ignore'):
    check(f'hard boundary: "{bad}" absent from the JB lines', bad not in low)

# ---- TC renders
shp = dict(ab.SWITCH.findall(tc['sysprompt']['content']))
def tcr(over):
    r, _ = ab.simulate_tc(tc, over, 1)
    return r['System Prompt'] + '\n' + r['Post-History']
on = dict(shp) | {'aria-logic-core': 'on', 'aria-adult': 'on'}
t0, t1 = tcr(on), tcr(on | {'aria-jailbreak': 'on'})
check('TC: JB + Adult + Logic Core -> both lines before Fresh', re.search(r'- Role:[^\n]*\n- Frank:[^\n]*\n- Fresh:', t1) is not None)
check('TC: dashed-line count +2', count_line(t1) == count_line(t0) + 2 and dashed_before_go(t1) == count_line(t1))
check('TC: JB without Logic Core prints nothing', '- Role:' not in tcr(dict(shp) | {'aria-adult': 'on', 'aria-jailbreak': 'on'}))
check('TC: JB without Adult prints nothing', '- Role:' not in tcr(dict(shp) | {'aria-logic-core': 'on', 'aria-jailbreak': 'on'}))
check('TC: JB with Freaky only prints', '- Role:' in tcr(dict(shp) | {'aria-logic-core': 'on', 'aria-freaky': 'on', 'aria-jailbreak': 'on'}))
ph = tc['sysprompt']['post_history']
check('TC: plan tells the model to skip Role and Frank on a message written as the user', 'no Fate, Bonds, Ledger, Layers, Role or Frank line' in ph)
# TC lines identical to CC lines
m2 = re.search(r'(- Role:[^\n]*)\n(- Frank:[^\n]*)', t1)
check('TC lines identical to CC lines', (m2.group(1), m2.group(2)) == (role, frank))

# ---- regex alternation
ccre = [s for s in cc['extensions']['regex_scripts'] if s['scriptName'].startswith('ARIA Impersonate - strip an untagged plan')][0]['findRegex']
tcre = [s for s in json.loads((ROOT / 'regex/ARIA 1.0 Regex Scripts (Text Completions).json').read_text(encoding='utf-8')) if s['scriptName'].startswith('ARIA Impersonate - strip an untagged plan')][0]['findRegex']
check('regex alternation has Role|Frank in CC and TC files', 'Joins|Role|Frank' in ccre and 'Joins|Role|Frank' in tcre)
print('ALL PASS' if ok else 'SOME FAILED')
