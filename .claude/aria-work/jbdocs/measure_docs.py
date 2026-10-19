#!/usr/bin/env python3
"""Re-measure every token figure the guide quotes, for the files given on the command line.

usage: python3 measure_docs.py <CC.json> <TC.json>

Uses simulate_cc / simulate_tc and tokens() from tools/aria_budget.py (characters / 4 of the rendered text,
comments stripped), the same metric the checker uses.
"""
import json
import sys
from pathlib import Path

ROOT = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
sys.path.insert(0, str(ROOT / 'tools'))
import aria_budget as ab  # noqa: E402


def total(rendered):
    return sum(ab.tokens(t) for t in rendered.values())


def cc_report(path):
    preset = json.loads(Path(path).read_text(encoding='utf-8'))
    prompts = {p['identifier']: p for p in preset['prompts']}
    order = preset['prompt_order'][1]['order']
    name = {pid: prompts[pid].get('name', pid) for pid in prompts}
    shipped = {r['identifier'] for r in order if r['enabled']}
    by_prefix = lambda *pre: {pid for pid in prompts if name[pid].startswith(pre)}
    patches = by_prefix('🩹')
    core = shipped - by_prefix('🎲', '⏰')
    skip_all_on = by_prefix('🌳', '🌿') | {pid for pid in prompts if 'twin' in name[pid]} | {'enhanceDefinitions'} | patches
    no_patch = {r['identifier'] for r in order} - skip_all_on

    def patch_cost(pid):
        r, _ = ab.simulate_cc(preset, no_patch | {pid}, seed=1)
        return total(r)

    costs = {name[p]: patch_cost(p) for p in patches}
    largest = max(patches, key=patch_cost)
    all_on = no_patch | {largest}
    out = {}
    out['core'] = total(ab.simulate_cc(preset, core, 1)[0])
    out['shipped default'] = total(ab.simulate_cc(preset, shipped, 1)[0])
    out['everything ON'] = total(ab.simulate_cc(preset, all_on, 1)[0])
    out['largest patch'] = name[largest]
    out['patch costs (CC, everything else ON)'] = costs
    # Impersonate delta, the checker's own formula
    imp, _ = ab.simulate_cc(preset, all_on, 1, impersonate=True)
    normal, _ = ab.simulate_cc(preset, all_on, 1)
    imp_setting = ab.tokens(ab.render(preset.get('impersonation_prompt') or '', {}, __import__('random').Random(1)))
    out['Impersonate adds'] = (sum(ab.tokens(t) for t in imp.values()) - out['everything ON']
                               + sum(ab.tokens(normal[pid]) for pid in normal if pid not in imp) + imp_setting)
    # the same everything-ON path without the Jailbreak, to price it
    jb = [pid for pid in prompts if name[pid].startswith('🔓')]
    if jb:
        out['everything ON without Jailbreak'] = total(ab.simulate_cc(preset, all_on - set(jb), 1)[0])
        out['Jailbreak cost (everything ON)'] = out['everything ON'] - out['everything ON without Jailbreak']
        # as shipped default + Adult + Logic Core only vs + Jailbreak (the cost a user would see)
        adult = {'nsfw'}
        base = shipped | adult
        out['shipped + Adult'] = total(ab.simulate_cc(preset, base, 1)[0])
        out['shipped + Adult + Jailbreak'] = total(ab.simulate_cc(preset, base | set(jb), 1)[0])
        out['Jailbreak cost (shipped + Adult)'] = out['shipped + Adult + Jailbreak'] - out['shipped + Adult']
        # Impersonate with the Jailbreak path on
        imp_base, _ = ab.simulate_cc(preset, base | set(jb), 1, impersonate=True)
        nrm_base, _ = ab.simulate_cc(preset, base | set(jb), 1)
        out['shipped + Adult + JB: normal'] = total(nrm_base)
        out['shipped + Adult + JB: Impersonate (entries only)'] = total(imp_base)
    return out


def tc_report(path):
    preset = json.loads(Path(path).read_text(encoding='utf-8'))
    system = preset['sysprompt']['content']
    shipped = dict(ab.SWITCH.findall(system))
    patches = [s for s in shipped if s.startswith('aria-patch')]
    off = {s: 'off' for s in shipped}

    def patch_cost(p):
        r_on, _ = ab.simulate_tc(preset, off | {p: 'on'}, 1)
        r_off, _ = ab.simulate_tc(preset, off, 1)
        return total(r_on) - total(r_off)

    costs = {p: patch_cost(p) for p in patches}
    largest = max(patches, key=patch_cost)
    non_patch_on = {s: 'on' for s in shipped if not s.startswith('aria-patch')}
    all_on = non_patch_on | {p: ('on' if p == largest else 'off') for p in patches}
    roomy = dict(shipped) | {'aria-logic-core': 'on', 'aria-fate': 'on', 'aria-time-place': 'on'}
    out = {}
    out['shipped (lean, 32k)'] = total(ab.simulate_tc(preset, shipped, 1)[0])
    out['+ Logic Core, Fate, Time'] = total(ab.simulate_tc(preset, roomy, 1)[0])
    out['everything ON (checker)'] = total(ab.simulate_tc(preset, all_on, 1)[0])
    out['largest patch (checker)'] = largest
    out['patch costs (TC, alone, others off)'] = costs
    for p in patches:
        o = non_patch_on | {q: ('on' if q == p else 'off') for q in patches}
        out[f'everything ON + {p}'] = total(ab.simulate_tc(preset, o, 1)[0])
    out['patch costs (TC, with all modules on)'] = {
        p: out[f'everything ON + {p}'] - total(ab.simulate_tc(preset, non_patch_on | {q: 'off' for q in patches}, 1)[0])
        for p in patches}
    out['everything ON, no patch'] = total(ab.simulate_tc(preset, non_patch_on | {q: 'off' for q in patches}, 1)[0])
    if 'aria-jailbreak' in shipped:
        o = dict(non_patch_on) | {q: 'off' for q in patches} | {'aria-jailbreak': 'off'}
        out['everything ON, no patch, no Jailbreak'] = total(ab.simulate_tc(preset, o, 1)[0])
        # shipped + Logic Core + Adult vs + Jailbreak
        a = dict(shipped) | {'aria-logic-core': 'on', 'aria-adult': 'on'}
        b = a | {'aria-jailbreak': 'on'}
        out['TC shipped + Logic Core + Adult'] = total(ab.simulate_tc(preset, a, 1)[0])
        out['TC shipped + Logic Core + Adult + Jailbreak'] = total(ab.simulate_tc(preset, b, 1)[0])
        out['Jailbreak cost (TC, Logic Core + Adult)'] = out['TC shipped + Logic Core + Adult + Jailbreak'] - out['TC shipped + Logic Core + Adult']
        # Jailbreak without a Logic Core: nothing prints
        c = dict(shipped) | {'aria-adult': 'on', 'aria-jailbreak': 'on'}
        d = dict(shipped) | {'aria-adult': 'on'}
        out['Jailbreak cost (TC, Adult but no Logic Core)'] = total(ab.simulate_tc(preset, c, 1)[0]) - total(ab.simulate_tc(preset, d, 1)[0])
        # Jailbreak without Adult: nothing prints
        e = dict(shipped) | {'aria-logic-core': 'on', 'aria-jailbreak': 'on'}
        f = dict(shipped) | {'aria-logic-core': 'on'}
        out['Jailbreak cost (TC, Logic Core but no Adult)'] = total(ab.simulate_tc(preset, e, 1)[0]) - total(ab.simulate_tc(preset, f, 1)[0])
    return out


def show(title, d):
    print('==', title)
    for k, v in d.items():
        if isinstance(v, dict):
            print(f'  {k}:')
            for kk, vv in sorted(v.items(), key=lambda kv: -kv[1]):
                print(f'      {vv:6}  {kk}')
        else:
            print(f'  {k}: {v}')


if __name__ == '__main__':
    cc_path, tc_path = sys.argv[1], sys.argv[2]
    show('CC ' + cc_path, cc_report(cc_path))
    show('TC ' + tc_path, tc_report(tc_path))
