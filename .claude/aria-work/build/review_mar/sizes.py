"""Shipped-default size (defaultChoices, sections as shipped) and the Agents text cost, read from the rendered output."""
import json, subprocess, sys
from pathlib import Path
MAR_DIR = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/mar')
HERE = Path(__file__).resolve().parent
marf = sys.argv[1]
doc = json.loads(Path(marf).read_text(encoding='utf-8'))
dc = json.loads(doc['data']['preset']['defaultChoices'])
def render(cfgs, force):
    p = HERE / 'sizes_cfg.json'; p.write_text(json.dumps(cfgs))
    args = ['node', str(MAR_DIR / 'me' / 'mrender.mjs'), marf, str(p)] + (['--force'] if force else [])
    return json.loads(subprocess.run(args, capture_output=True, check=True, cwd=MAR_DIR / 'me').stdout)
for force in (False, True):
    r = render([dc, dict(dc, state_mode='AGENTS')], force)
    tot = [round(len('\n'.join(x.values())) / 4) for x in r]
    nonempty = [round(len('\n'.join(v for v in x.values() if v.strip())) / 4) for x in r]
    print('defaults', 'force' if force else 'as shipped', 'N/A tokens:', tot, '(non-empty sections only:', nonempty, ')')
base = dict(dc, logic_options=[])
r = render([dict(base, state_mode='NONE'), dict(base, state_mode='AGENTS'), dict(base, logic_core='SYSTEM', state_mode='NONE'),
            dict(base, logic_core='SYSTEM', state_mode='AGENTS')], True)
main = len(r[1]['⚡ ARIA Main Prompt']) - len(r[0]['⚡ ARIA Main Prompt'])
lc = len(r[1]['🧠 The Logic Core']) - len(r[0]['🧠 The Logic Core'])
tw = len(r[3]['🧠 The Logic Core (system-role twin)']) - len(r[2]['🧠 The Logic Core (system-role twin)'])
print('Agents: Main +%d, Logic Core note +%d, twin note +%d chars; rendered (Main + one note) %.2f tokens; block + both notes %.2f'
      % (main, lc, tw, (main + lc) / 4, (main + lc + tw) / 4))
