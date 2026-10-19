"""Measure candidate G4 texts: rendered chars and chars/4 (comments stripped, {{user}} -> User), plus set variables."""
import json, random, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab

def measure(text, state=None):
    st = dict(state or {})
    before = dict(st)
    out = ab.render(text, st, random.Random(1))
    sets = {k: v for k, v in st.items() if isinstance(v, str) and v and before.get(k) != v}
    return out, sets

def report(label, text, state=None):
    out, sets = measure(text, state)
    s = f'{len(out):5} ch {len(out)/4:7.2f} tok  {label}'
    for k, v in sets.items():
        s += f'\n{"":5}    {len(v):5} ch {len(v)/4:7.2f} tok    sets {k}'
    print(s)
    return len(out), {k: len(v) for k, v in sets.items()}

if __name__ == '__main__':
    d = json.load(open(sys.argv[1], encoding='utf-8'))
    tot = 0
    for pid, p in d['prompts'].items():
        n, sets = report(p['name'], p['content'])
        tot += n + sum(sets.values())
    print(f'TOTAL {tot} ch = {tot/4:.2f} tok')
