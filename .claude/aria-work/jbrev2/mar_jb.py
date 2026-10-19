import json, subprocess
from pathlib import Path
MAR = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/mar')
PRESET = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json"
fin = json.loads(Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/jb/final.json').read_text(encoding='utf-8'))
JBL = [l.replace('{{user}}', 'User') for l in fin['lines']]
configs = json.loads((MAR / 'configs.json').read_text())
out = json.loads(subprocess.run(['node', str(MAR / 'me/mrender.mjs'), PRESET, str(MAR / 'configs.json'), '--force'],
                                capture_output=True, check=True, cwd=MAR / 'me').stdout)
LCS = ['🧠 The Logic Core', '🧠 The Logic Core (system-role twin)']
bad, active_n, checked = [], 0, 0
for cfg, r in zip(configs, out):
    want = 'JAILBREAK' in cfg['logic_options'] and cfg['adult_mode'] != 'NONE'
    for name in LCS:
        t = r.get(name, '')
        if not t.strip():
            continue
        checked += 1
        lines = t.split('\n')
        has = [l for l in lines if l.startswith(('- Role:', '- Frank:'))]
        if want:
            active_n += 1
            i = lines.index(JBL[0]) if JBL[0] in lines else -1
            if has != JBL or i < 0 or lines[i:i + 3][2:3] != [l for l in lines if l.startswith('- Fresh:')][:1] or \
               ('Ledger' in t and not lines[i - 1].startswith('- Ledger:')):
                bad.append(('placement/content', name, cfg))
        elif has:
            bad.append(('printed while inactive', name, cfg))
    outside = '\n'.join(v for k, v in r.items() if k not in LCS)
    if 'adult-fiction game master' in outside or '- Frank:' in outside:
        bad.append(('outside the Logic Cores', None, cfg))
print(f'{len(configs)} configs, {checked} Logic Core renders, {active_n} with the JB active, {len(bad)} problems')
for b in bad[:5]:
    print('  ', b)
