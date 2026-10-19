#!/usr/bin/env python3
"""Global estimate: snapshot CC/TC with G1-G3 finals, G4/G5 drafts, a G6 file and a stand-in Chibi JB, run through the frozen checker."""
import json, sys, copy, io, contextlib, uuid, random
S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
sys.path.insert(0, S + '/spec/frozen')
import aria_budget as ab
CC = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
JB_LINES = "- Role: " + "x" * 95 + "\n- Frank: " + "y" * 105   # stand-in, about 55 tokens
def load(p):
    return json.load(open(p, encoding='utf-8'))
def build_cc(g6path, groups=('final/G1', 'final/G2', 'final/G3', 'drafts/G4', 'drafts/G5')):
    cc = copy.deepcopy(CC)
    by = {p['identifier']: p for p in cc['prompts']}
    for g in groups:
        d = load(f'{S}/chibi/{g}.json')
        for pid, p in d['prompts'].items():
            by[pid]['content'] = p['content']
    if g6path:
        for pid, p in load(g6path)['prompts'].items():
            by[pid]['content'] = p['content']
    # stand-in JB entry after Freaky (needs Adult's ariaModeLine)
    jid = 'jb-standin'
    jb = dict(by['dc8b1acb-9a7e-5a43-b9aa-38e7b70662a3'])
    jb.update(identifier=jid, name='🔓 Jailbreak (needs Adult Context)',
              content='{{// stand-in}}{{trim}}\n{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::' + JB_LINES + '}}{{/if}}')
    i = [p['identifier'] for p in cc['prompts']].index('4537b57d-e002-586d-a4c9-233740c51605')
    cc['prompts'].insert(i + 1, jb)
    order = cc['prompt_order'][1]['order']
    k = [r['identifier'] for r in order].index('4537b57d-e002-586d-a4c9-233740c51605')
    order.insert(k + 1, {'identifier': jid, 'enabled': False})
    return cc
def run(cc, quiet=True):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        totals, errors = ab.analyse_cc(cc)
    return totals, errors, buf.getvalue()
def path_cost(cc, extra_ids):
    """everything ON (checker's set without patches) plus the given ids; returns per-entry dict."""
    prompts = {p['identifier']: p for p in cc['prompts']}
    name = {pid: prompts[pid].get('name', pid) for pid in prompts}
    order = cc['prompt_order'][1]['order']
    patches = {pid for pid in prompts if name[pid].startswith('🩹')}
    skip = {pid for pid in prompts if name[pid].startswith(('🌳', '🌿')) or 'twin' in name[pid]} | {'enhanceDefinitions'} | patches
    no_patch = {r['identifier'] for r in order} - skip
    r, _ = ab.simulate_cc(cc, no_patch | set(extra_ids), seed=1)
    return {name[k]: ab.tokens(v) for k, v in r.items()}
if __name__ == '__main__':
    g6 = sys.argv[1] if len(sys.argv) > 1 else None
    cc = build_cc(g6)
    totals, errors, out = run(cc)
    print('G6 file:', g6)
    for k, v in totals.items():
        print(f'  {k:22} {v}')
    print('  errors:', [e for e in errors if 'over the' not in e] or 'none (budget errors ignored)')
    pr = {p['identifier']: p for p in cc['prompts']}
    pats = [p for p in pr if pr[p]['name'].startswith('🩹')]
    base = sum(path_cost(cc, []).values())
    print('  everything ON without any patch:', base)
    for p in sorted(pats, key=lambda p: -sum(path_cost(cc, [p]).values())):
        extra = [p] + (['ac96376e-5777-595b-8f48-359f864b0685'] if p.startswith('333dbbed') else []) + (['333dbbed-344d-4a6c-90c5-b0625291115a'] if p.startswith('ac96376e') else [])
        print(f'   {sum(path_cost(cc, extra).values()) - base:6}  {pr[p]["name"]}' + ('  (with 3.8 Flash)' if p.startswith('ac96376e') else '') + ('  (with All-In-One)' if p.startswith('333dbbed') else ''))
