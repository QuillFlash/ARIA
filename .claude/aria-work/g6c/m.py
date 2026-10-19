"""Quick token meter for candidate lines: chars/4 of the rendered text ({{user}} counts as User)."""
import sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab

def r(text, state=None):
    st = dict(state or {})
    return ab.render(text, st, random.Random(1))

def t(text, state=None):
    return len(r(text, state)) / 4

def show(label, text, limit=None, state=None):
    n = t(text, state)
    flag = ''
    if limit is not None:
        flag = '  OK' if n <= limit else f'  OVER by {n - limit:.2f}'
    print(f'{n:7.2f}  {label}{flag}')
    return n
