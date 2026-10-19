#!/usr/bin/env python3
"""frag.py: fragment cost tool. A text file marks optional fragments as [[name: text]]; this prints, for each, the tokens it costs
(difference of renders with and without it), and writes variants. usage: python3 frag.py file.txt [drop1,drop2,...|ALL]"""
import re, sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab

PAT = re.compile(r'\[\[([A-Za-z0-9_]+):((?:(?!\]\]).)*)\]\]', re.S)

def render(s):
    return ab.render(s, {}, random.Random(1))

def build(text, drop):
    def rep(m):
        return '' if (drop == 'ALL' or m.group(1) in drop) else m.group(2)
    return PAT.sub(rep, text)

def main():
    text = open(sys.argv[1], encoding='utf-8').read()
    drop = set()
    if len(sys.argv) > 2:
        drop = 'ALL' if sys.argv[2] == 'ALL' else set(x for x in sys.argv[2].split(',') if x)
    names = [m.group(1) for m in PAT.finditer(text)]
    full = len(render(build(text, set())))
    print('FULL (all fragments kept):', full, 'chars', full / 4, 'tokens')
    for n in names:
        without = len(render(build(text, {n})))
        frag = [m.group(2) for m in PAT.finditer(text) if m.group(1) == n][0]
        print(f'  {n:8} {((full - without) / 4):6.1f} tok  {frag[:90]!r}')
    cur = build(text, drop)
    out = render(cur)
    print('CURRENT (dropping %s):' % (sorted(drop) if drop != 'ALL' else 'ALL'), len(out), 'chars', len(out) / 4, 'tokens')
    open(sys.argv[1].rsplit('.', 1)[0] + '.out', 'w', encoding='utf-8').write(cur)

if __name__ == '__main__':
    main()
