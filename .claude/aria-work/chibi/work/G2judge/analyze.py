"""Per-line analysis of a G2 JSON: rendered chars/tokens per line, semicolon fragment counts, and a heuristic flag
for comma/and/or enumerations of exactly three items. Also prints exact (unrounded) group totals."""
import json, sys, re, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
from paths import *
import aria_budget as ab

def render(text, state=None):
    st = dict(state or {})
    out = ab.render(text, st, random.Random(1))
    return out, st

def frag_report(line):
    body = line.split(':', 1)[1] if ':' in line[:30] else line
    frags = [f for f in body.split(';')]
    return len(frags)

def three_lists(line):
    """Heuristic: find 'A, B and/or C' with exactly two commas before a final and/or inside one fragment."""
    hits = []
    for frag in line.split(';'):
        # split by ' and ' / ' or ' final coordination preceded by comma-separated items
        m = re.findall(r'((?:[^,;:()]+,){2}[^,;:()]+?\b(?:and|or)\b[^,;:()]+)', frag)
        for x in m:
            # count commas in the candidate run
            items = [i for i in re.split(r',|\band\b|\bor\b', x) if i.strip()]
            if len(items) == 3:
                hits.append(x.strip())
    return hits

def main(path):
    d = json.load(open(path, encoding='utf-8'))
    total = 0.0
    for pid, p in d['prompts'].items():
        out, st = render(p['content'])
        print(f"=== {p['name']}: rendered {len(out)} chars = {len(out)/4:.2f} tokens")
        total += len(out) / 4
        for ln in out.split('\n'):
            if not ln.strip():
                continue
            print(f"  {len(ln)+1:4}c {(len(ln)+1)/4:6.2f}t  frags={frag_report(ln)}  {ln[:110]}")
            for h in three_lists(ln):
                print('        3-LIST?', h)
        for k, v in st.items():
            if isinstance(v, str) and v:
                print(f"  [sets {k}] {len(v)} chars = {len(v)/4:.2f} tokens; frags={frag_report(v)}")
                total += len(v) / 4
                for ln in v.split('\n'):
                    for h in three_lists(ln):
                        print('        3-LIST?', h)
    print(f"GROUP TOTAL (exact, CC): {total:.2f} tokens")
    for k, v in (d.get('tc') or {}).items():
        out, _ = render(v)
        print(f"TC {k}: {len(out)} chars = {len(out)/4:.2f} tokens")

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else DRAFT)
