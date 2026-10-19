import sys, random
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
def tok(s):
    r = ab.render(s, {}, random.Random(1)); return ab.tokens(r), len(r)
V = {}
V['a'] = """OOC: write {{user}}'s next message, starting on their first word or action. Plan only {{user}}'s move, from persona and earlier messages, with only what they perceived or were told. Stop where another character would answer; no header, character lines, 🎲 block or 💚 block, whatever the plan says.
<POV>
This turn's POV replaces any earlier one: first person present, unless {{user}}'s earlier messages use another person or tense.
</POV>"""
V['b'] = """<impersonation_turn>
OOC: write {{user}}'s next message, starting on their first word or action. Plan only {{user}}'s move from persona and earlier messages, knowing only what they perceived or were told. Stop where another character would answer; no header, character lines, 🎲 block or 💚 block, whatever the plan says.
</impersonation_turn>
<POV>
Replaces any earlier POV this turn: first person present, unless {{user}}'s earlier messages use another person or tense.
</POV>"""
V['c'] = """<impersonation_turn>
OOC: write {{user}}'s next message, starting on their first word or action and stopping where another character would answer. Plan only {{user}}'s move from persona and earlier messages, with only what they perceived or were told. No header, character lines, 🎲 block or 💚 block, whatever the plan says.
</impersonation_turn>
<POV>This turn's POV replaces any earlier one: first person present, unless {{user}}'s earlier messages use another person or tense.</POV>"""
V['d'] = """OOC: write {{user}}'s next message, starting on their first word or action and stopping where another character would answer. Plan only {{user}}'s move from persona and earlier messages, with only what they perceived or were told. No header, character lines, 🎲 block or 💚 block, whatever the plan says.
<POV>This turn's POV replaces any earlier one: first person present, unless {{user}}'s earlier messages use another person or tense.</POV>"""
V['e'] = """<impersonation_turn>OOC: write {{user}}'s next message, starting on their first word or action and stopping where another character would answer. Plan only {{user}}'s move from persona and earlier messages, with only what they perceived or were told. No header, character lines, 🎲 block or 💚 block, whatever the plan says.</impersonation_turn>
<POV>This turn's POV replaces any earlier one: first person present, unless {{user}}'s earlier messages use another person or tense.</POV>"""
for k,v in V.items():
    print(k, tok(v))
