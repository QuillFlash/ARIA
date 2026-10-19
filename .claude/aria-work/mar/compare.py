#!/usr/bin/env python3
"""Render the Marinara preset (with Marinara's own macro engine) and the CC preset (with the repo checker's
SillyTavern simulator) for the same settings, and report every line that differs, section by section.

usage: python3 compare.py [--cc REV|WORK] [--cc-file PATH] [--mar PATH] [--sample N] [--full]
"""
import argparse, difflib, itertools, json, random, re, subprocess, sys
from collections import defaultdict
from pathlib import Path

REPO = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / 'tools'))
import aria_budget as ab  # noqa: E402

CC_FILE = "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
MAR_FILE = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json"

# Marinara choice value -> CC prompt identifier prefixes
CHOICE_TO_CC = {
    ('adult_mode', 'ADULT'): ['nsfw'], ('adult_mode', 'FREAKY'): ['nsfw', '4537b57d'],
    ('pov_style', 'HYBRID'): ['b7b6ab7f'],
    ('core_modules', 'SCENE'): ['15a8065d'], ('core_modules', 'NPCVOICE'): ['cca418a6'],
    ('core_modules', 'ANTISLOP'): ['9869a1e5'], ('core_modules', 'SCENT'): ['dd3642f5'],
    ('core_modules', 'ANTHRO'): ['2a2e12d0'], ('core_modules', 'FLASH'): ['2e3e7f63'],
    ('core_modules', 'HOLD'): ['dc8b1acb'],
    ('world_engine', 'TIME'): ['5dcccd11'], ('world_engine', 'FATE'): ['acc2177a'],
    ('world_engine', 'BONDS'): ['5506d699'],
    ('model_patch', 'CLAUDE'): ['b59a2ad1'], ('model_patch', 'GEMINI'): ['ac96376e'],
    ('model_patch', 'GEMINI38'): ['ac96376e', '333dbbed'], ('model_patch', 'GLM'): ['1f2e1f97'],
    ('model_patch', 'KIMIQWEN'): ['9bb6c2b0'], ('model_patch', 'MIMOPRO'): ['33f92483'],
    ('model_patch', 'MIMOFLASH'): ['3a027832'], ('model_patch', 'DEEPSEEK'): ['e04b9c2b'],
    ('logic_core', 'ASSISTANT'): ['15b770cf'], ('logic_core', 'SYSTEM'): ['591b8c15'],
    ('logic_options', 'THINKTAGS'): ['303f26f5'], ('logic_options', 'REDUCE'): ['939286fd'],
}
BASE_CC = ['main', 'f23feaf4', 'jailbreak']
# Marinara section name -> CC prompt prefixes whose rendered text it must equal
SECTION_MAP = {
    '⚡ ARIA Main Prompt': ['main'], '🔞 Adult Context': ['nsfw'], '😈 Freaky Override': ['4537b57d'],
    '👀 Hybrid POV': ['b7b6ab7f'], '🎬 Voice & Scene Engine': ['15a8065d'], '🎭 NPC Voice & Emotions': ['cca418a6'],
    '🐺 Anthro Vocals': ['2a2e12d0'], '🖋️ Anti-Slop Codex': ['9869a1e5'], '👃 Scent Occasions': ['dd3642f5'],
    '⏰ Time & Place': ['5dcccd11'], '🎲 Fate & Chekhov Ledger': ['acc2177a'], '🥰 Bonds Lite': ['5506d699'],
    '🩹 Model Patch: Claude 5': ['b59a2ad1'],
    '🩹 Model Patch: Gemini|🩹 Model Patch: Gemini 3.8 Flash': ['333dbbed', 'ac96376e'],
    '🩹 Model Patch: GLM': ['1f2e1f97'], '🩹 Model Patch: Kimi / Qwen': ['9bb6c2b0'],
    '🩹 Model Patch: MiMo V2.6 Pro': ['33f92483'], '🩹 Model Patch: MiMo V2.6 Flash': ['3a027832'],
    '🩹 Model Patch: DeepSeek': ['e04b9c2b'], '📖 Story Context': ['f23feaf4'],
    '🧠 The Logic Core': ['15b770cf'], '🧠 The Logic Core (system-role twin)': ['591b8c15'],
    '🚪 Last-Mile Gate': ['jailbreak'], 'Reduce Reasoning': ['939286fd'],
}
DICE = re.compile(r'Fate dice: A \d+ \| B \d+ \| C \d+')


def norm(text):
    text = DICE.sub('Fate dice: A # | B # | C #', text)
    return [ln.rstrip() for ln in text.split('\n') if ln.strip()]


def load_cc(rev, cc_file):
    if cc_file:
        return json.loads(Path(cc_file).read_text(encoding='utf-8'))
    if rev == 'WORK':
        return json.loads((REPO / CC_FILE).read_text(encoding='utf-8'))
    raw = subprocess.run(['git', '-C', str(REPO), 'show', f'{rev}:{CC_FILE}'], capture_output=True, check=True).stdout
    return json.loads(raw.decode('utf-8'))


def matrix(full, sample, extra_logic, seed=7):
    patches = ['NONE', 'CLAUDE', 'GEMINI', 'GEMINI38', 'GLM', 'KIMIQWEN', 'MIMOPRO', 'MIMOFLASH', 'DEEPSEEK']
    worlds = [[], ['TIME'], ['TIME', 'FATE'], ['TIME', 'BONDS'], ['TIME', 'FATE', 'BONDS'], ['FATE', 'BONDS']]
    base = ['SCENE', 'NPCVOICE', 'ANTISLOP', 'SCENT']
    cores = [base + a + b for a, b in itertools.product([[], ['FLASH']], [[], ['HOLD']])]
    lcs = ['ASSISTANT', 'SYSTEM', 'NONE']
    configs = []
    for p, w, c, lc, lo in itertools.product(patches, worlds, cores, lcs, [[], ['THINKTAGS'], ['THINKTAGS', 'REDUCE']]):
        configs.append(dict(adult_mode='NONE', pov_style='NONE', core_modules=c, world_engine=w, model_patch=p,
                            logic_core=lc, logic_options=lo, state_mode='NONE'))
    if extra_logic:
        # The extra Logic Core option (the Gemini 4 Argon Thought Tags) alone, beside Think Tags and beside Reduce Reasoning,
        # against every adult mode (whose Mode lines the plan prints), patch and Logic Core, on a lean and a full world and core set
        tag_los = [list(extra_logic), ['THINKTAGS'] + extra_logic, extra_logic + ['REDUCE'], ['THINKTAGS'], []]
        for am, p, w, c, lc, lo in itertools.product(['NONE', 'ADULT', 'FREAKY'], patches, [[], ['TIME', 'FATE', 'BONDS']],
                                                     [cores[0], cores[3]], lcs, tag_los):
            configs.append(dict(adult_mode=am, pov_style='NONE', core_modules=c, world_engine=w, model_patch=p,
                                logic_core=lc, logic_options=lo, state_mode='NONE'))
    rng = random.Random(seed)
    all_core = ['SCENE', 'NPCVOICE', 'ANTISLOP', 'SCENT', 'ANTHRO', 'FLASH', 'HOLD']
    all_lo = ['THINKTAGS', 'REDUCE'] + extra_logic
    for _ in range(sample):
        configs.append(dict(
            adult_mode=rng.choice(['NONE', 'ADULT', 'FREAKY']), pov_style=rng.choice(['NONE', 'HYBRID']),
            core_modules=[m for m in all_core if rng.random() < 0.5],
            world_engine=[m for m in ['TIME', 'FATE', 'BONDS'] if rng.random() < 0.5],
            model_patch=rng.choice(patches), logic_core=rng.choice(['ASSISTANT', 'SYSTEM', 'NONE']),
            logic_options=[m for m in all_lo if rng.random() < 0.5], state_mode='NONE'))
    if not full:
        configs = configs[::7] + configs[-sample:]
    return configs


def cc_ids(cc, prefixes):
    ids = []
    for pre in prefixes:
        hit = [p['identifier'] for p in cc['prompts'] if p['identifier'].startswith(pre)]
        if len(hit) != 1:
            raise SystemExit(f'CC prefix {pre} matched {hit}')
        ids.append(hit[0])
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cc', default='WORK')
    ap.add_argument('--cc-file')
    ap.add_argument('--mar', default=str(MAR_FILE))
    ap.add_argument('--sample', type=int, default=600)
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--show', type=int, default=3, help='example configs per unique diff')
    a = ap.parse_args()
    cc = load_cc(a.cc, a.cc_file)
    mar_doc = json.loads(Path(a.mar).read_text(encoding='utf-8'))
    # The Gemini 4 Argon tags entry, if the presets carry one, maps Marinara's THOUGHTTAGS option to the CC prompt named
    # 🏷️ Logic Core Tags: Gemini…
    g4 = [p['identifier'] for p in cc['prompts'] if p.get('name', '').startswith('🏷️ Logic Core Tags: Gemini')]
    lo_block = [c for c in mar_doc['data']['choiceBlocks'] if c['variableName'] == 'logic_options'][0]
    mar_has_g4 = 'THOUGHTTAGS' in lo_block['options']
    extra = []
    if g4 and mar_has_g4:
        CHOICE_TO_CC[('logic_options', 'THOUGHTTAGS')] = [g4[0][:8]]
        extra = ['THOUGHTTAGS']
    elif g4 or mar_has_g4:
        print(f'WARNING: Gemini tags in CC: {bool(g4)}, in Marinara: {mar_has_g4}; the THOUGHTTAGS option is not exercised')
    has_hold = any(p['identifier'].startswith('dc8b1acb') for p in cc['prompts'])
    configs = matrix(a.full, a.sample, extra)
    if not has_hold:
        for c in configs:
            c['core_modules'] = [m for m in c['core_modules'] if m != 'HOLD']
    cfg_path = HERE / 'configs.json'
    cfg_path.write_text(json.dumps(configs))
    res = subprocess.run(['node', str(HERE / 'me' / 'mrender.mjs'), a.mar, str(cfg_path), '--force'],
                         capture_output=True, check=True, cwd=HERE / 'me').stdout
    mar_all = json.loads(res)
    diffs = defaultdict(list)
    for cfg, mar in zip(configs, mar_all):
        enabled = set(cc_ids(cc, BASE_CC))
        for key, vals in cfg.items():
            for v in (vals if isinstance(vals, list) else [vals]):
                enabled.update(cc_ids(cc, CHOICE_TO_CC.get((key, v), [])))
        rendered, _ = ab.simulate_cc(cc, enabled, seed=1)
        for mname, pres in SECTION_MAP.items():
            mtext = '\n'.join(mar.get(n, '') for n in mname.split('|'))
            ctext = '\n'.join(rendered.get(i, '') for i in cc_ids(cc, pres))
            ml, cl = norm(mtext), norm(ctext)
            if ml != cl:
                d = tuple(l for l in difflib.unified_diff(cl, ml, 'CC', 'MAR', lineterm='', n=0)
                          if not l.startswith(('---', '+++', '@@')))
                diffs[(mname, d)].append(cfg)
    print(f'{len(configs)} configs, {len(diffs)} unique section diffs' + (' (Thought Tags exercised)' if extra else ''))
    for (mname, d), cfgs in sorted(diffs.items(), key=lambda kv: (kv[0][0], -len(kv[1]))):
        print(f'\n=== {mname}: {len(cfgs)} configs')
        for c in cfgs[:a.show]:
            print('   cfg:', json.dumps(c, separators=(',', ':')))
        for l in d:
            print('  ', l[:400])


if __name__ == '__main__':
    main()
