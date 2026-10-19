#!/usr/bin/env python3
"""Frozen checker on in-memory snapshot copies with a G6 file swapped in (CC and TC), alone and with the other groups
plus the JB wired per JB.md. Also checks, for every patch shape, that logicCoreLines equals the dashed plan lines printed
before go, and that the gate shows each patch line once.  usage: python3 g6check.py G6.json"""
import contextlib, copy, io, json, random, re, sys, uuid
S = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work"
sys.path.insert(0, S + "/spec/frozen"); sys.path.insert(0, '.')
import aria_budget as ab
from tcmap import wrap, body, MAP
G6 = json.load(open(sys.argv[1] if len(sys.argv) > 1 and __name__ == '__main__' else 'cand6.json', encoding='utf-8'))
JB = json.load(open(S + "/jb/final.json", encoding='utf-8'))
JBL = '\n'.join(JB['lines']); N = len(JB['lines'])
def load(p): return json.load(open(p, encoding='utf-8'))
def cc_build(others):
    cc = load(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json")
    by = {p['identifier']: p for p in cc['prompts']}
    groups = ([load(S + f"/chibi/{g}.json") for g in ('final/G1', 'final/G2', 'final/G3', 'drafts/G4', 'drafts/G5')] if others else []) + [G6]
    for g in groups:
        for pid, v in g['prompts'].items(): by[pid]['content'] = v['content']
    if others:   # JB entry per JB.md (G1 final has the blanks, G3 final the counter and print)
        hold = by['dc8b1acb-9a7e-5a43-b9aa-38e7b70662a3']; new = copy.deepcopy(hold)
        new['identifier'] = str(uuid.UUID(int=random.Random(7).getrandbits(128), version=4)); new['name'] = '🔓 Jailbreak (needs Adult Context)'
        new['content'] = JB['cc_comment'] + '{{trim}}\n{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}' % (N, JBL)
        i = [k for k, p in enumerate(cc['prompts']) if p['identifier'].startswith('4537b57d')][0]; cc['prompts'].insert(i + 1, new)
        o = cc['prompt_order'][1]['order']; k = [k for k, r in enumerate(o) if r['identifier'].startswith('4537b57d')][0]
        o.insert(k + 1, {'identifier': new['identifier'], 'enabled': False})
    return cc
def tc_build(others):
    tc = load(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json")
    sp = tc['sysprompt']; c = sp['content']
    cc_src = load(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json")
    bys = {p['identifier'][:8]: p for p in cc_src['prompts']}
    for sw, short in MAP.items():
        seg = wrap(sw, body(bys[short]['content'])); assert c.count(seg) == 1, sw
        c = c.replace(seg, G6['tc']['module_' + sw])
        m = re.search(r'\{\{//(?:(?!\}\}).)*\}\}(?=\{\{\.' + re.escape(sw) + r' = )', c, re.S); assert m, sw
        key = 'switch_comment_' + sw
        if key in G6['tc']: c = c[:m.start()] + G6['tc'][key] + c[m.end():]
    if others:
        g2, g3 = load(S + '/chibi/final/G2.json'), load(S + '/chibi/final/G3.json')
        sp['post_history'] = g3['tc']['post_history_logic_core'] + g2['tc']['post_history_gate']
        c = c.replace('{{.aria-freaky = off}}\n', '{{.aria-freaky = off}}\n' + JB['tc_switch_comment'] + '{{.aria-jailbreak = off}}\n', 1)
        c = c.replace('{{setvar::ariaPatchJoins::}}\n', '{{setvar::ariaPatchJoins::}}{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}\n', 1)
        blk = '{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}{{/if}}' % (N, JBL)
        assert c.count('</freaky_override>\n{{/if}}{{#if .aria-hybrid-pov}}') == 1
        c = c.replace('</freaky_override>\n{{/if}}{{#if .aria-hybrid-pov}}', '</freaky_override>\n{{/if}}' + blk + '{{#if .aria-hybrid-pov}}', 1)
    sp['content'] = c
    return tc
def quiet(f, *a):
    b = io.StringIO()
    with contextlib.redirect_stdout(b): return f(*a)
LC_IDS = ('15b770cf-6049-5f3b-b25d-be09728a65d5', '591b8c15-985e-59f1-8c90-59e7cae236ae')
def plan_lines(text):
    pre = text.split('\n- go')[0]
    return len([l for l in pre.split('\n') if l.startswith('- ')])
def main():
  bad = 0
  for others in (False, True):
      tag = 'snapshot + G6' if not others else 'G1-G3 finals + G4/G5 drafts + JB + G6'
      cc = cc_build(others)
      tot, err = quiet(ab.analyse_cc, cc)
      err = [e for e in err if 'over the' not in e]
      print(f'CC [{tag}] everything ON {tot["everything ON"]}, shipped {tot["shipped default"]}; errors: {err or "none"}'); bad += len(err)
      tc = tc_build(others)
      tot, err = quiet(ab.analyse_tc, tc)
      err = [e for e in err if 'over the' not in e]
      print(f'TC [{tag}] everything ON {tot["everything ON"]}; errors: {err or "none"}'); bad += len(err)
      # line counts over every shape
      order = cc['prompt_order'][1]['order']; P = {p['identifier']: p for p in cc['prompts']}
      names = {k: P[k]['name'] for k in P}
      allids = {r['identifier'] for r in order} - {'enhanceDefinitions'}
      patches = sorted(k for k in allids if names[k].startswith('🩹'))
      fg, hold, tags = '2e3e7f63-8463-51ff-ba8f-e5b05162c193', 'dc8b1acb-9a7e-5a43-b9aa-38e7b70662a3', '303f26f5-bc2f-5dde-a9e9-aaaacd3eff4b'
      fate, bonds = 'acc2177a-34e4-4941-93a2-b80bc18b8c91', '5506d699-fb00-49ce-a631-73b3f0036eae'
      base = {k for k in allids if not names[k].startswith(('🌳', '🌿', '🩹'))} - {LC_IDS[1], fg, hold, tags, fate, bonds}
      n = 0
      for p in patches + [None]:
          for extra in ([], ['333dbbed-344d-4a6c-90c5-b0625291115a'] if p and p.startswith('ac96') else []):
              for f in (0, 1):
                  for h in (0, 1):
                    for t in (0, 1):
                      for fb in ((0, 0), (1, 0), (0, 1), (1, 1)):
                        for lc in LC_IDS:
                          for imp in (False, True):
                              en = (base - {LC_IDS[0]}) | {lc} | ({p} if p else set()) | set(extra) | ({fg} if f else set()) | ({hold} if h else set()) | ({tags} if t else set()) | ({fate} if fb[0] else set()) | ({bonds} if fb[1] else set())
                              r, st = ab.simulate_cc(cc, en, seed=1, impersonate=imp)
                              text = r[lc]; n += 1
                              if plan_lines(text) != int(st['logicCoreLines']):
                                  bad += 1; print('COUNT MISMATCH', names.get(p), f, h, t, fb, lc[:8], imp, plan_lines(text), st['logicCoreLines'])
                              gate = r['jailbreak']
                              for v in ('ariaPatchGate', 'ariaPatchJoins', 'ariaFlashGate', 'ariaHoldGate'):
                                  val = st.get(v)
                                  shared = 1 if (v == 'ariaPatchGate' and val and val.startswith('- Contrast: cut a not/n')) else 0
                                  if val and gate.count(val) != 1 + shared:
                                      bad += 1; print('GATE PRINT', v, names.get(p), f, h, imp)
      print(f'  line-count and gate-print checks over {n} CC shapes: {"OK" if not bad else bad}')
  print('TOTAL PROBLEMS:', bad)

if __name__ == '__main__':
    main()
