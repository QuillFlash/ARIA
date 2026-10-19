#!/usr/bin/env python3
"""meas.py FILE  -> per-line char/token counts of a text file as rendered by the ARIA renderer ({{user}} = 'User')."""
import sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab

def render(text, state=None):
    st = dict(state or {})
    return ab.render(text, st, random.Random(1)), st

if __name__ == '__main__':
    txt = open(sys.argv[1], encoding='utf-8').read()
    out, st = render(txt)
    tot = 0
    for l in out.split('\n'):
        print(f'{len(l):5} {len(l)/4:6.1f}  {l[:100]}')
    print('TOTAL chars', len(out), 'tokens', len(out)/4)
