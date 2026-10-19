#!/usr/bin/env python3
"""Wire the candidate lines the way BUILD.md / JB.md say (CC entry and TC block), render them in front of the approved Chibi Logic Core
(G3 final) with the frozen checker's renderer, and check the plan: lines print before Fresh, count matches the dashed lines, nothing without Adult."""
import json, random, re, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab  # noqa: E402

W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
cand = json.load(open(sys.argv[1], encoding='utf-8'))
lines = cand['lines']
g3 = json.load(open(f'{W}/chibi/final/G3.json', encoding='utf-8'))
cc_lc = g3['prompts']['15b770cf-6049-5f3b-b25d-be09728a65d5']['content']
tc_lc = g3['tc']['post_history_logic_core']
body = '\n'.join(lines)  # a real newline, never a literal backslash-n
assert '\\n' not in body

cc_entry = cand['cc_comment'] + '{{trim}}\n' + '{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::' + body + '}}{{/if}}'
tc_block = '{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::' + body + '}}{{/if}}{{/if}}'
adult = '{{setvar::ariaModeLine::- Mode: realism, persona-true.}}'


def dashed(plan):
    head = plan.split('go')[0]
    body_lines = [l for l in plan.splitlines() if l.startswith('- ') and l != '- go']
    m = re.search(r'(\d+) (?:dashed )?lines', plan)
    return len(body_lines), int(m.group(1)) if m else None


ok = True
for label, text_before, lc, extra in (
    ('CC', cc_entry, cc_lc, {}),
    ('TC', tc_block, tc_lc, {'aria-jailbreak': 'on', 'aria-logic-core': 'on'}),
):
    for adult_on in (True, False):
        for tags in (False, True):
            st = dict(extra)
            if tags:
                st.update(ariaThinkOpen='<thinking>', ariaThinkClose='</thinking>')
            rnd = random.Random(1)
            pre = (adult if adult_on else '') + text_before
            ab.render(pre, st, rnd)
            plan = ab.render(lc, st, rnd)
            printed = 'Role:' in plan and 'Frank:' in plan
            n_lines, claimed = dashed(plan)
            good = (printed == adult_on) and n_lines == claimed
            ok &= good
            print(f'{label} adult={adult_on!s:5} tags={tags!s:5} printed={printed!s:5} dashed lines={n_lines} head says {claimed} -> {"OK" if good else "FAIL"}')
            if label == 'CC' and adult_on and not tags:
                print(plan)
print('ALL OK' if ok else 'FAILURES')
