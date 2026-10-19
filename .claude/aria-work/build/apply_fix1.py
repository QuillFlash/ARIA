"""Fix 1: append {{setvar::gemini38Patch::}} to the CC Main Prompt's first-line blanking run (raw-text replacement)."""
import json

R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
CC = R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"


def esc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


raw = open(CC, encoding="utf-8", newline="").read()
before = json.loads(raw)

old = "{{setvar::ariaJbLines::}}\n{{trim}}\nYou are the narrator and game master"
new = "{{setvar::ariaJbLines::}}{{setvar::gemini38Patch::}}\n{{trim}}\nYou are the narrator and game master"
assert raw.count(esc(old)) == 1, raw.count(esc(old))
assert "{{setvar::gemini38Patch::}}" not in raw
out = raw.replace(esc(old), esc(new))
assert out != raw and out.count("{{setvar::gemini38Patch::}}") == 1

# integrity: still parses, still round-trips in the file's own format, and only the Main Prompt's content changed
after = json.loads(out)
assert json.dumps(after, ensure_ascii=False, indent=4) == out
assert len(before["prompts"]) == len(after["prompts"])
changed = [b["identifier"] for b, a in zip(before["prompts"], after["prompts"]) if b != a]
assert changed == ["main"], changed
b2 = dict(before); a2 = dict(after)
b2["prompts"] = a2["prompts"] = None
assert b2 == a2, "something outside prompts changed"
m_before = next(p for p in before["prompts"] if p["identifier"] == "main")["content"]
m_after = next(p for p in after["prompts"] if p["identifier"] == "main")["content"]
assert m_after == m_before.replace(old, new)

open(CC, "w", encoding="utf-8", newline="").write(out)
print("Fix 1 applied: 1 replacement, Main Prompt only;", len(raw), "->", len(out), "chars")
