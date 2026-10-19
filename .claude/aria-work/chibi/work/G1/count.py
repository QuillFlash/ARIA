import sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
# usage: count.py file  -> per line and total tokens using the checker's render ({{user}} counts as 'User')
txt = open(sys.argv[1], encoding='utf-8').read().rstrip('\n')
tot = 0
for l in txt.split('\n'):
    r = ab.render(l, {}, random.Random(1))
    n = len(r); tot += n + 1
    print(f'{n:4} {n/4:6.1f} | {l[:80]}')
whole = ab.render(txt, {}, random.Random(1))
print('total chars', len(whole), 'tokens', ab.tokens(whole))
