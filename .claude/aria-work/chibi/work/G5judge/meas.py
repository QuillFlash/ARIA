#!/usr/bin/env python3
"""Per-line token measure (chars/4 of the rendered text, frozen renderer) for a text file or for the body of a prompt.
usage: meas.py FILE [FILE ...]   prints each rendered line's tokens and the total (exact, not rounded)"""
import sys, random, re
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab


def render(text, state=None):
    st = dict(state or {})
    out = ab.render(text, st, random.Random(1))
    return out, st


def show(path, state=None):
    text = open(path, encoding='utf-8').read()
    out, st = render(text, state)
    print(f'==== {path}')
    for line in out.split('\n'):
        print(f'{len(line)/4:7.2f}  {line[:150]}')
    print(f'{len(out)/4:7.2f}  TOTAL own (rounded {ab.tokens(out)})')
    for k, v in st.items():
        if isinstance(v, str) and v and (state or {}).get(k) != v:
            print(f'{len(v)/4:7.2f}  [sets {k}]')
    return len(out) / 4


if __name__ == '__main__':
    state = {}
    args = []
    for a in sys.argv[1:]:
        if a.startswith('--state='):
            import json
            state = json.loads(a[len('--state='):])
        else:
            args.append(a)
    tot = 0
    for p in args:
        tot += show(p, state)
    if len(args) > 1:
        print(f'{tot:7.2f}  ALL FILES')
