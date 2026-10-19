"""Exact size of the Agents-only text in a Marinara preset: rendered Main and Logic Core with state_mode AGENTS vs NONE."""
import json, subprocess, sys
from common import *
MAR = Path(sys.argv[1]) if len(sys.argv) > 1 else CHIBI_MAR
base = dict(adult_mode='NONE', pov_style='NONE', core_modules=['SCENE'], world_engine=[], model_patch='NONE',
            logic_core='ASSISTANT', logic_options=[])
cfgs = [dict(base, state_mode='NONE'), dict(base, state_mode='AGENTS'),
        dict(base, logic_core='SYSTEM', state_mode='NONE'), dict(base, logic_core='SYSTEM', state_mode='AGENTS')]
p = W / 'build' / 'chibi_mar' / 'agents_cfg.json'
p.write_text(json.dumps(cfgs))
out = json.loads(subprocess.run(['node', str(W / 'mar/me/mrender.mjs'), str(MAR), str(p), '--force'],
                                capture_output=True, check=True, cwd=W / 'mar/me').stdout)
def d(i, j, name): return len(out[j][name]) - len(out[i][name])
main = d(0, 1, '⚡ ARIA Main Prompt'); lc = d(0, 1, '🧠 The Logic Core'); twin = d(2, 3, '🧠 The Logic Core (system-role twin)')
print('Main block +%d chars, Logic Core note +%d (twin +%d); total %d chars = %.1f tokens (sections are joined by a newline)' %
      (main, lc, twin, main + lc, (main + lc) / 4))
