import json, re, sys
from pathlib import Path

ROOT = Path("/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA")
p = ROOT / "regex/ARIA 1.0 Regex Scripts (Text Completions).json"
raw = p.read_text(encoding='utf-8')
assert raw.count('\r') == 0
old = "Tally|Pushback|Restate|Joins)"
new = "Tally|Pushback|Restate|Joins|Role|Frank)"
o = json.dumps(old, ensure_ascii=False)[1:-1]
n = json.dumps(new, ensure_ascii=False)[1:-1]
print("occurrences of old:", raw.count(o), "| of new already:", raw.count(n))
assert raw.count(o) == 1, raw.count(o)
assert raw.count(n) == 0
out = raw.replace(o, n)
assert out.count(n) == 1
with open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(out)
print("written")
