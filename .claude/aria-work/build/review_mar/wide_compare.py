"""Wider render comparison than compare.py: extra random seeds (pov HYBRID, ANTHRO, every adult mode, JB), own configs
file (never touches mar/configs.json), plus a strict mode that compares exact text (dice masked, outer whitespace trimmed)."""
import json, subprocess, sys, difflib, re
from collections import defaultdict
from pathlib import Path
MAR_DIR = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/mar')
sys.path.insert(0, str(MAR_DIR))
import compare as cp
HERE = Path(__file__).resolve().parent
ccf, marf = sys.argv[1], sys.argv[2]
seeds = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [11, 23, 101]
n = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
cc = json.loads(Path(ccf).read_text(encoding='utf-8'))
jb = [p['identifier'] for p in cc['prompts'] if p.get('name', '').startswith('🔓')]
cp.CHOICE_TO_CC[('logic_options', 'JAILBREAK')] = [jb[0][:8]]
configs = []
for s in seeds:
    configs += cp.matrix(False, n, ['JAILBREAK'], seed=s)[-n:]
# every patch x adult mode x JB x pov x lc x tags, with all cores and all worlds (the heaviest paths)
import itertools
allc = ['SCENE', 'NPCVOICE', 'ANTISLOP', 'SCENT', 'ANTHRO', 'FLASH', 'HOLD']
for p, am, pov, lc, lo, fl in itertools.product(['NONE', 'CLAUDE', 'GEMINI', 'GEMINI38', 'GLM', 'KIMIQWEN', 'MIMOPRO', 'MIMOFLASH', 'DEEPSEEK'],
                                      ['NONE', 'ADULT', 'FREAKY'], ['NONE', 'HYBRID'], ['ASSISTANT', 'SYSTEM', 'NONE'],
                                      [['THINKTAGS', 'REDUCE', 'JAILBREAK'], ['JAILBREAK']], [True, False]):
    configs.append(dict(adult_mode=am, pov_style=pov, core_modules=allc if fl else [m for m in allc if m != 'FLASH'],
                        world_engine=['TIME', 'FATE', 'BONDS'], model_patch=p, logic_core=lc, logic_options=lo, state_mode='NONE'))
cfg_path = HERE / 'wide_configs.json'
cfg_path.write_text(json.dumps(configs))
out = json.loads(subprocess.run(['node', str(MAR_DIR / 'me' / 'mrender.mjs'), marf, str(cfg_path), '--force'],
                                capture_output=True, check=True, cwd=MAR_DIR / 'me').stdout)
diffs = defaultdict(list); strict = defaultdict(list)
D = re.compile(r'Fate dice: A \d+ \| B \d+ \| C \d+')
for cfg, mar in zip(configs, out):
    enabled = set(cp.cc_ids(cc, cp.BASE_CC))
    for key, vals in cfg.items():
        for v in (vals if isinstance(vals, list) else [vals]):
            enabled.update(cp.cc_ids(cc, cp.CHOICE_TO_CC.get((key, v), [])))
    rendered, _ = cp.ab.simulate_cc(cc, enabled, seed=1)
    for mname, pres in cp.SECTION_MAP.items():
        mtext = '\n'.join(mar.get(x, '') for x in mname.split('|'))
        ctext = '\n'.join(rendered.get(i, '') for i in cp.cc_ids(cc, pres))
        ml, cl = cp.norm(mtext), cp.norm(ctext)
        if ml != cl:
            d = tuple(l for l in difflib.unified_diff(cl, ml, 'CC', 'MAR', lineterm='', n=0) if not l.startswith(('---', '+++', '@@')))
            diffs[(mname, d)].append(cfg)
        ms, cs = D.sub('#', mtext).strip(), D.sub('#', ctext).strip()
        if ms != cs:
            strict[mname].append((cfg, cs, ms))
print(len(configs), 'configs;', len(diffs), 'unique section diffs;', 'strict-text differences in', {k: len(v) for k, v in strict.items()})
for (m, d), cf in list(diffs.items())[:6]:
    print('==', m, len(cf), json.dumps(cf[0]))
    for l in d[:8]: print('   ', l[:300])
for m, v in list(strict.items())[:4]:
    cfg, cs, ms = v[0]
    sm = difflib.SequenceMatcher(None, cs, ms, autojunk=False)
    print('STRICT', m, json.dumps(cfg)[:160])
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op != 'equal': print('    ', op, repr(cs[max(0, a1-40):a2+10]), '=>', repr(ms[max(0, b1-40):b2+10]))
