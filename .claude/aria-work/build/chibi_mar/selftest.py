"""Rebuild ARIA's Marinara sections from ARIA's CC with the converter; every section must match byte for byte."""
import difflib, re, sys
from common import *
import mar_convert as mc

def comment_of(content):
    m = re.match(r'^(?:\{\{#if [^\n]*?\}\})?\{\{// (.*?) \}\}\{\{trim\}\}\n', content, re.S)
    return m.group(1) if m else None

def agents_parts(content):
    m = re.search(r'\{\{#if state_mode == "AGENTS"\}\}\n<agent_context_protocol>.*?\{\{/if\}\}$', content, re.S)
    return m.group(0)

def run(cc_path=ARIA_CC, mar_path=ARIA_MAR, verbose=True):
    cc = mc.CC(load(cc_path)); M = load(mar_path)
    S = M['data']['sections']
    comments = {}
    for idx, key in mc.SECTION_KEYS.items():
        c = comment_of(S[idx]['content'])
        assert c is not None, (idx, key)
        comments[key] = c
    agents_block = agents_parts(S[0]['content'])
    note = re.search(r'\{\{#if state_mode == "AGENTS"\}\}( The engine[^{]*)\{\{/if\}\}', S[33]['content']).group(1)
    out, V = mc.build_all(cc, comments, agents_block, note)
    bad = 0
    for idx, key in mc.SECTION_KEYS.items():
        if key not in out:
            print('not built:', idx, key); continue
        want = S[idx]['content']; got = out[key]
        if want != got:
            bad += 1
            print('DIFF', idx, key)
            for l in difflib.unified_diff(want.split('\n'), got.split('\n'), 'MAR', 'BUILT', lineterm='', n=0):
                print('   ', l[:300])
    print('selftest:', bad, 'differing sections')
    return bad

if __name__ == '__main__':
    sys.exit(1 if run() else 0)


def comment_rules_test():
    """The comment rules, run on ARIA's CC comments, must give ARIA Marinara's comments (rule-based sections only)."""
    import build_chibi_mar as b
    cc = mc.CC(load(ARIA_CC)); M = load(ARIA_MAR); S = M['data']['sections']
    got = b.adapt_comments(cc, False)
    bad = 0
    for idx, key in mc.SECTION_KEYS.items():
        if key not in got:
            continue
        want = comment_of(S[idx]['content'])
        if key == 'story':
            want = want  # identical text
        if got[key] != want:
            bad += 1
            print('COMMENT DIFF', idx, key)
            sm = difflib.SequenceMatcher(None, want, got[key], autojunk=False)
            for op, a1, a2, b1, b2 in sm.get_opcodes():
                if op != 'equal':
                    print('    ', op, repr(want[max(0, a1 - 30):a2 + 10]), '=>', repr(got[key][max(0, b1 - 30):b2 + 10]))
    print('comment rules:', bad, 'differing comments')
    return bad
