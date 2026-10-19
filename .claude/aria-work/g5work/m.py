#!/usr/bin/env python3
"""Tiny measuring helper: python3 m.py 'text'  or  import m; m.t('text') -> rendered tokens (chars/4, {{user}} = 'User')."""
import sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab

def t(text, state=None):
    st = dict(state or {})
    out = ab.render(text, st, random.Random(1))
    return len(out) / 4, len(out)

if __name__ == '__main__':
    for a in sys.argv[1:]:
        print(t(a), a[:80])
