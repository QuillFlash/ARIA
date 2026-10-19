"""Rendered module text: Chibi CC vs Chibi TC, over a matrix of shared switches."""
import itertools, difflib
from common import *
cc, tc = load(CHIBI_CC), load(CHIBI_TC)
P = {p['identifier']: p for p in cc['prompts']}
pref = lambda pre: [pid for pid in P if pid.startswith(pre)][0]
MAP = {  # CC id prefix -> TC switch (None = always on in TC)
    'main': None, '9869a1e5': None, '15a8065d': None, 'cca418a6': 'aria-npc-voice', '2a2e12d0': 'aria-anthro',
    'dd3642f5': 'aria-scent', 'b7b6ab7f': 'aria-hybrid-pov', 'nsfw': 'aria-adult', '4537b57d': 'aria-freaky',
    '05f6e90d': 'aria-jailbreak', '5dcccd11': 'aria-time-place', 'acc2177a': 'aria-fate', '5506d699': 'aria-bonds',
    '1f2e1f97': 'aria-patch-glm', '9bb6c2b0': 'aria-patch-kimi-qwen', '33f92483': 'aria-patch-mimo-pro',
    '3a027832': 'aria-patch-mimo-flash', 'e04b9c2b': 'aria-patch-deepseek', '2e3e7f63': 'aria-flash-gate',
    'dc8b1acb': 'aria-character-hold', '303f26f5': 'aria-thinking-tags', '15b770cf': 'aria-logic-core'}
IDS = {k: pref(k) for k in MAP}
STORY, CUSTOM = pref('f23feaf4'), pref('0dc06d25')
order = [r['identifier'] for r in cc['prompt_order'][1]['order']]
PATCHES = ['aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro', 'aria-patch-mimo-flash', 'aria-patch-deepseek', None]
TC_ONLY_LC = [(' A message written as {{user}} skips it.'.replace('{{user}}', 'User'), '')]
problems, n = [], 0
for patch, flash, hold, tags, mode, jb, fate, bonds, time_, pov in itertools.product(
        PATCHES, (0, 1), (0, 1), (0, 1), ("none", "adult", "freaky"), (0, 1), (0, 1), (0, 1), (0, 1), (0,)):
    pov = time_
    sw = {'aria-logic-core': 'on', 'aria-thinking-tags': 'on' if tags else 'off', 'aria-adult': 'on' if mode != 'none' else 'off',
          'aria-freaky': 'on' if mode == 'freaky' else 'off', 'aria-jailbreak': 'on' if jb else 'off', 'aria-hybrid-pov': 'on' if pov else 'off',
          'aria-npc-voice': 'on', 'aria-anthro': 'on', 'aria-scent': 'on', 'aria-time-place': 'on' if time_ else 'off',
          'aria-fate': 'on' if fate else 'off', 'aria-bonds': 'on' if bonds else 'off', 'aria-flash-gate': 'on' if flash else 'off',
          'aria-character-hold': 'on' if hold else 'off'}
    for p in PATCHES[:-1]:
        sw[p] = 'on' if p == patch else 'off'
    en = {IDS['main'], STORY, CUSTOM, IDS['9869a1e5'], IDS['15a8065d'], 'jailbreak', IDS['15b770cf']}
    en |= {IDS[k] for k, s in MAP.items() if s and sw.get(s) == 'on'}
    en |= {r['identifier'] for r in cc['prompt_order'][1]['order'] if r['identifier'] in ('chatHistory', 'worldInfoBefore', 'worldInfoAfter', 'charDescription', 'charPersonality', 'scenario', 'personaDescription', 'dialogueExamples')}
    rc, stc = ab.simulate_cc(cc, en, 1)
    rt, stt = ab.simulate_tc(tc, sw, 1)
    n += 1
    tag = f'patch={patch} flash={flash} hold={hold} tags={tags} mode={mode} jb={jb} fate={fate} bonds={bonds} time={time_} pov={pov}'
    sysT, postT = rt['System Prompt'], rt['Post-History']
    # 1. every CC system-block module's rendered text appears in TC's system prompt (Main: up to the custom-instructions part)
    for k, pid in IDS.items():
        if pid not in rc or k in ('15b770cf',):
            continue
        t = rc[pid].strip()
        if t and t not in sysT:
            problems.append((tag, 'module text not in TC system', k, t[:120]))
    # 2. splice variables equal
    keys = {v for v in set(stc) | set(stt) if (v.startswith('aria') and not v.startswith('aria-')) or v == 'logicCoreLines'}
    for v in sorted(keys):
        if (stc.get(v) or '') != (stt.get(v) or ''):
            problems.append((tag, 'variable differs', v, (stc.get(v), stt.get(v))))
    # 3. Logic Core: CC's rendered LC vs TC's post-history before <final_gate>
    lcT = postT.split('<final_gate>')[0]
    lcC = rc[IDS['15b770cf']]
    lcT2 = lcT.replace(' A message written as User skips it.', '')
    lcT2 = re.sub(r' For a message written as User, plan only User\'s move; skip any [^.]*? line\.', '', lcT2)
    if lcC.strip() != lcT2.strip():
        problems.append((tag, 'LC differs', '', '\n'.join(difflib.unified_diff(lcC.strip().split('\n'), lcT2.strip().split('\n'), lineterm='', n=0))))
    # 4. gate
    gC = rc['jailbreak'].strip()
    gT = '<final_gate>' + postT.split('<final_gate>', 1)[1]
    pass
    if gC != gT.strip():
        problems.append((tag, 'gate differs', '', '\n'.join(difflib.unified_diff(gC.split('\n'), gT.strip().split('\n'), lineterm='', n=0))))
print('configs', n, 'problems', len(problems))
seen = set()
for p in problems:
    key = (p[1], p[2], str(p[3])[:300])
    if key in seen:
        continue
    seen.add(key)
    print(p[0]); print('  ', p[1], p[2]); print('  ', str(p[3])[:1500])
    if len(seen) > 25:
        break
