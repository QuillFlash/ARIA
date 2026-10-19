#!/usr/bin/env python3
"""Check a Marinara preset's plan line counts and measure its fully kitted-out token figures.

usage: python3 verify.py [--mar PATH]
Uses the configs.json that compare.py last wrote (run compare.py first).
- Every rendered Logic Core: the "N dashed lines" number equals the "- " lines before "- go", and the gate's plan cue agrees.
- No unrendered {{macro}} survives in any section.
- Fully kitted-out tokens (characters / 4 of all rendered sections) for every model patch, state_mode NONE (N) and AGENTS (A),
  with Think Tags and Reduce Reasoning on.
"""
import argparse, json, re, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
DEFAULT = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json"


def render(path, cfg_file):
    args = ['node', str(HERE / 'me' / 'mrender.mjs'), str(path), str(cfg_file), '--force']
    return json.loads(subprocess.run(args, capture_output=True, check=True, cwd=HERE / 'me').stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mar', default=str(DEFAULT))
    a = ap.parse_args()
    configs = json.loads((HERE / 'configs.json').read_text())
    out = render(a.mar, HERE / 'configs.json')
    bad = checked = 0
    for cfg, r in zip(configs, out):
        for name in ['🧠 The Logic Core', '🧠 The Logic Core (system-role twin)']:
            t = r.get(name, '')
            if not t.strip():
                continue
            checked += 1
            # ARIA: "then N dashed lines" (Tags on), "Reasoning writes N dashed lines" (Tags off);
            # Chibi: "then N dashed lines and go" (Tags on), "Reasoning: N lines; go ends it." (Tags off)
            m = re.search(r'(?:then|writes) (\d+) dashed lines|Reasoning: (\d+) lines;', t)
            if m:
                m = re.search(r'(\d+)', m.group(0))
            lines = t.split('\n')
            if '- go' not in lines:
                bad += 1
                print('NO GO LINE', name, json.dumps(cfg))
                continue
            dashed = [l for l in lines[:lines.index('- go')] if l.startswith('- ')]
            if not m or int(m.group(1)) != len(dashed):
                bad += 1
                if bad < 4:
                    print('COUNT MISMATCH', name, m and m.group(1), len(dashed), json.dumps(cfg))
            g = r.get('🚪 Last-Mile Gate', '')
            gm = re.search(r'Begin with <(?:thinking|thought)>, then (\d+) dashed lines', g)
            if gm and int(gm.group(1)) != len(dashed):
                bad += 1
                print('GATE COUNT MISMATCH', gm.group(1), len(dashed), json.dumps(cfg))
    print(f'{len(configs)} configs; {checked} Logic Core renders count-checked; {bad} mismatches')
    left = {(n, x) for r in out for n, t in r.items() for x in re.findall(r'\{\{[^}]*\}\}', t)}
    print('unrendered macros:', sorted(left)[:10])
    doc = json.loads(Path(a.mar).read_text(encoding='utf-8'))
    lo_block = [c for c in doc['data']['choiceBlocks'] if c['variableName'] == 'logic_options'][0]
    extra = []
    full = dict(adult_mode='FREAKY', pov_style='HYBRID',
                core_modules=['SCENE', 'NPCVOICE', 'ANTISLOP', 'SCENT', 'ANTHRO', 'FLASH', 'HOLD'],
                world_engine=['TIME', 'FATE', 'BONDS'], logic_core='ASSISTANT',
                logic_options=['THINKTAGS', 'REDUCE'] + extra, state_mode='NONE')
    cf = [dict(full, model_patch=p, state_mode=sm)
          for p in ['NONE', 'CLAUDE', 'GEMINI', 'GEMINI38', 'GLM', 'KIMIQWEN', 'MIMOPRO', 'MIMOFLASH', 'DEEPSEEK']
          for sm in ['NONE', 'AGENTS']]
    (HERE / 'cf.json').write_text(json.dumps(cf))
    res = render(a.mar, HERE / 'cf.json')
    figs = {f"{c['model_patch']}/{c['state_mode'][0]}": round(len('\n'.join(r.values())) / 4) for c, r in zip(cf, res)}
    print('tokens' + (' (JB on)' if extra else ''), ' '.join(f'{k}={v}' for k, v in figs.items()))
    print('max', max(figs.values()))


if __name__ == '__main__':
    main()
