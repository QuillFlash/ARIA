#!/usr/bin/env python3
"""Reviewer's Marinara check: render HEAD and the working Marinara file with Marinara's own macro engine for the same
configs (HEAD without JAILBREAK) and require identical sections, except that when the JB should print (JAILBREAK chosen,
adult_mode not NONE, a Logic Core chosen) the Logic Core gains exactly the two approved lines before '- Fresh:', its
count grows by 2, and the gate's plan cue agrees.
"""
import itertools, json, re, subprocess, sys
from pathlib import Path

ROOT = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
S = ROOT / '.claude/aria-work'
HERE = Path(__file__).resolve().parent
MARN = "Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json"
FIN = json.loads((S / 'jb/final.json').read_text(encoding='utf-8'))
JBL = [l.replace('{{user}}', 'User') for l in FIN['lines']]
INSERT = '\n' + '\n'.join(JBL) + '\n- Fresh:'
COUNT = re.compile(r'(then|writes) (\d+) dashed lines')


def render(preset_path, cfgs):
    cfg_file = HERE / 'mar_cfgs.json'
    cfg_file.write_text(json.dumps(cfgs))
    out = subprocess.run(['node', str(S / 'mar/me/mrender.mjs'), str(preset_path), str(cfg_file), '--force'],
                         capture_output=True, check=True, cwd=S / 'mar/me').stdout
    return json.loads(out)


def main():
    head_path = HERE / 'mar_head.json'
    head_path.write_bytes(subprocess.run(['git', '-C', str(ROOT), 'show', f'HEAD:{MARN}'], capture_output=True, check=True).stdout)
    patches = ['NONE', 'CLAUDE', 'GEMINI', 'GEMINI38', 'GLM', 'KIMIQWEN', 'MIMOPRO', 'MIMOFLASH', 'DEEPSEEK']
    base = ['SCENE', 'NPCVOICE', 'ANTISLOP', 'SCENT']
    cfgs = []
    for am, lc, lo, w, p, c, sm in itertools.product(
            ['NONE', 'ADULT', 'FREAKY'], ['ASSISTANT', 'SYSTEM', 'NONE'],
            [[], ['JAILBREAK'], ['THINKTAGS', 'JAILBREAK'], ['THINKTAGS'], ['THINKTAGS', 'REDUCE', 'JAILBREAK']],
            [[], ['FATE'], ['BONDS'], ['TIME', 'FATE', 'BONDS']], patches, [base, base + ['ANTHRO', 'FLASH', 'HOLD']],
            ['NONE', 'AGENTS']):
        cfgs.append(dict(adult_mode=am, pov_style='NONE', core_modules=c, world_engine=w, model_patch=p,
                         logic_core=lc, logic_options=lo, state_mode=sm))
    work = render(ROOT / MARN, cfgs)
    head = render(head_path, [dict(c, logic_options=[o for o in c['logic_options'] if o != 'JAILBREAK']) for c in cfgs])
    errs, active_n = [], 0
    for cfg, w, h in zip(cfgs, work, head):
        active = 'JAILBREAK' in cfg['logic_options'] and cfg['adult_mode'] != 'NONE' and cfg['logic_core'] != 'NONE'
        active_n += active
        lab = json.dumps(cfg, separators=(',', ':'))
        if set(w) != set(h):
            errs.append(f'section set differs | {lab}')
        for name in h:
            wt, ht = w.get(name, ''), h[name]
            if active and name in ('🧠 The Logic Core', '🧠 The Logic Core (system-role twin)') and ht.strip():
                exp = COUNT.sub(lambda m: f'{m.group(1)} {int(m.group(2)) + 2} dashed lines', ht, count=1)
                if exp.count('\n- Fresh:') != 1:
                    errs.append(f'Fresh anchor in {name} | {lab}')
                exp = exp.replace('\n- Fresh:', INSERT)
                if wt != exp:
                    errs.append(f'{name} is not HEAD + JB lines + count 2 | {lab}')
            elif active and name == '🚪 Last-Mile Gate' and 'THINKTAGS' in cfg['logic_options']:
                exp = re.sub(r'(Begin with <thinking>, then )(\d+)', lambda m: f'{m.group(1)}{int(m.group(2)) + 2}', ht)
                if wt != exp:
                    errs.append(f'gate cue is not HEAD + 2 | {lab}')
            elif wt != ht:
                errs.append(f'{name} differs from HEAD | {lab}')
        for name, t in w.items():
            if ('- Role:' in t or '- Frank:' in t) and not (active and 'Logic Core' in name):
                errs.append(f'JB text in {name} | {lab}')
        if active:
            lcname = '🧠 The Logic Core' if cfg['logic_core'] == 'ASSISTANT' else '🧠 The Logic Core (system-role twin)'
            t = w.get(lcname, '')
            lines = t.split('\n')
            gi = lines.index('- go')
            dashed = [l for l in lines[:gi] if l.startswith('- ')]
            n = int(COUNT.search(t).group(2))
            if n != len(dashed) or [l for l in dashed if l.startswith(('- Role:', '- Frank:'))] != JBL:
                errs.append(f'plan count or JB lines wrong in {lcname} | {lab}')
    print(f'Marinara: {len(cfgs)} configs, {active_n} with the JB active, {len(errs)} problems')
    for e in errs[:12]:
        print('   ', e)
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
