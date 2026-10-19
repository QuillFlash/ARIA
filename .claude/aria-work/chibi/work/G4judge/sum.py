import sys, importlib
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G4judge')
import m
mod = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else 'bodies')
tot, rounded = 0, 0
for k, v in mod.B.items():
    n, s = m.report(k[:8], v)
    tot += n + sum(s.values())
    rounded += round(n / 4) + sum(round(x / 4) for x in s.values())
print(f'TOTAL {tot} ch = {tot/4:.2f} tok exact; per-row rounded sum {rounded}; ceiling 2000 ch / 500')
