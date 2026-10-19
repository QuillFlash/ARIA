import json, re
from pathlib import Path
REPO = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
W = REPO / '.claude' / 'aria-work'
ARIA_CC = REPO / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
CHIBI_CC = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"
ARIA_MAR = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json"
CHIBI_MAR = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Agent Gating.json"

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def split_comment(text):
    """Split text into (comment_without_markers, rest) at the leading {{// ... }}{{trim}} + newline."""
    m = re.match(r'\{\{// (.*?) ?\}\}\{\{trim\}\}\n?', text, re.S)
    if not m:
        return None, text
    return m.group(1), text[m.end():]
