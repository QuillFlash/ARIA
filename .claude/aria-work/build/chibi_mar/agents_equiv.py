"""With state_mode AGENTS every section must equal its state_mode NONE render plus the Agents block (Main) and the Scene note (Logic Cores)."""
import json, random, subprocess, sys
from common import *
import build_chibi_mar as b
MAR = Path(sys.argv[1]) if len(sys.argv) > 1 else CHIBI_MAR
cfgs = json.loads((W / 'mar/configs.json').read_text())
random.seed(3)
cfgs = random.sample(cfgs, 400)
pairs = []
for c in cfgs:
    pairs.append(dict(c, state_mode='NONE')); pairs.append(dict(c, state_mode='AGENTS'))
p = W / 'build/chibi_mar/agents_equiv_cfg.json'; p.write_text(json.dumps(pairs))
out = json.loads(subprocess.run(['node', str(W / 'mar/me/mrender.mjs'), str(MAR), str(p), '--force'], capture_output=True,
                                check=True, cwd=W / 'mar/me').stdout)
import re
DICE = re.compile(r'Fate dice: A \d+ \| B \d+ \| C \d+')
bad = 0
for i in range(0, len(out), 2):
    n = {k: DICE.sub('Fate dice', v) for k, v in out[i].items()}
    a = {k: DICE.sub('Fate dice', v) for k, v in out[i + 1].items()}
    assert n.keys() == a.keys()
    for name in n:
        if n[name] == a[name]:
            continue
        if name == '⚡ ARIA Main Prompt':
            tail = a[name][len(n[name]):]
            ok = a[name].startswith(n[name]) and '<agent_context_protocol>' in tail and tail.strip().endswith('</agent_context_protocol>')
        elif name.startswith('🧠 The Logic Core'):
            note = b.AGENTS_NOTE
            ok = a[name].replace(note, '', 1) == n[name]
        else:
            ok = False
        if not ok:
            bad += 1
            print('AGENTS DIFF in', name, json.dumps(pairs[i + 1])[:200])
print(len(out) // 2, 'config pairs;', bad, 'unexpected Agents differences')
