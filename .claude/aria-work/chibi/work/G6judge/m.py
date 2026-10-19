import sys, random, re
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
def t(text, state=None):
    st = dict(state or {})
    out = ab.render(text, st, random.Random(1))
    return len(out)/4, out, st
def show(label, text, state=None):
    n, out, st = t(text, state)
    print(f'{n:7.2f}  {label}')
    return n
def frags(line):
    # count top-level semicolon fragments per line
    return [len([f for f in l.split(';')]) for l in line.split('\n') if l.strip()]
