import json, random, sys
S = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work"
sys.path.insert(0, S + "/spec/frozen")
import aria_budget as ab
def rend(text, st):
    st = dict(st)
    return ab.render(text, st, random.Random(1)), st
files = sys.argv[1:]
mods = {"ariaModeLine": "- Mode: MODE", "ariaFateLine": "- Fate: FATE", "ariaBondsLine": "- Bonds: BONDS", "ariaLedgerLine": "- Ledger: LEDGER",
        "ariaHoldLine": "- Hold: HOLD", "ariaPatchGate": "- PatchGate: PG", "ariaPatchJoins": "- Joins: JOINS", "ariaPatchTally": "- Tally: TALLY",
        "ariaPatchLines": "2", "ariaVoiceExtra": "; VOICEEXTRA", "ariaJb": "- Role: ROLE\n- Frank: FRANK", "ariaJbLines": "2"}
tags = {"ariaThinkOpen": "<thinking>", "ariaThinkClose": "</thinking>"}
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    c = d['prompts']['15b770cf-6049-5f3b-b25d-be09728a65d5']['content']
    for lab, st in (("TAGS OFF, bare", {}), ("TAGS ON, bare", tags), ("TAGS OFF, all modules", mods), ("TAGS ON, all modules", dict(mods, **tags))):
        out, s2 = rend(c, st)
        print(f"##### {f.split('/')[-1]} | {lab} | {len(out)} chars, {ab.tokens(out)} tok | logicCoreLines={s2.get('logicCoreLines')} | cue={s2.get('ariaPlanCue','')!r}")
        print(out)
        print()
