#!/usr/bin/env python3
"""t.py: measure strings. usage: python3 t.py file  (each line = one candidate, rendered with the ARIA renderer) or import t; t.n(s)"""
import sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab

def r(s, state=None):
    st = dict(state or {})
    return ab.render(s, st, random.Random(1))

def n(s, state=None):
    o = r(s, state)
    return len(o) / 4

if __name__ == '__main__':
    for l in open(sys.argv[1], encoding='utf-8').read().split('\n'):
        if l.strip():
            o = r(l)
            print(f'{len(o):5} {len(o)/4:6.1f}  {l[:120]}')
