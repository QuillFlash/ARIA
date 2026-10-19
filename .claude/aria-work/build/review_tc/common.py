import json, re, sys
from pathlib import Path
REPO = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
W = REPO / '.claude/aria-work'
OUT = W / 'build/review_tc/out'
CHIBI_TC = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"
ARIA_TC = REPO / "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
CHIBI_CC = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"
ARIA_CC = REPO / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
RX_TC = REPO / 'regex/ARIA 1.0 Regex Scripts (Text Completions).json'
sys.path.insert(0, str(REPO / 'tools'))
sys.path.insert(0, str(W / 'spec'))
import aria_budget as ab  # noqa
from skeleton import skeleton  # noqa

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def finals():
    f = {}
    for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'JB'):
        f[g] = load(W / 'chibi/final' / f'{g}.json')
    return f

SW = re.compile(r'\{\{\.(aria-[\w-]+) = (on|off)\}\}')
