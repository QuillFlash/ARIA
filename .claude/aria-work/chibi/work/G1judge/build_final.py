#!/usr/bin/env python3
"""Build the judged G1 file ($S/chibi/final/G1.json) from the draft plus the judge's texts."""
import json
import sys

S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
OUT = sys.argv[1] if len(sys.argv) > 1 else S + '/chibi/final/G1.json'
draft = json.load(open(S + '/chibi/drafts/G1.json', encoding='utf-8'))

BLANKS = ('{{setvar::ariaDice::}}{{setvar::ariaFateLine::}}{{setvar::ariaBondsLine::}}{{setvar::ariaModeLine::}}'
          '{{setvar::ariaScentGate::}}{{setvar::ariaThinkOpen::}}{{setvar::ariaThinkClose::}}{{setvar::ariaLedgerLine::}}'
          '{{setvar::ariaLedgerGate::}}{{setvar::ariaFlashGate::}}{{setvar::ariaPlanCue::}}{{setvar::ariaPovGate::}}'
          '{{setvar::ariaEchoGate::}}{{setvar::ariaVoiceExtra::}}{{setvar::ariaPatchGate::}}{{setvar::ariaPatchLines::}}'
          '{{setvar::ariaChopGate::}}{{setvar::ariaHoldLine::}}{{setvar::ariaHoldGate::}}{{setvar::ariaPatchTally::}}'
          '{{setvar::ariaPatchJoins::}}{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}')

MAIN_RULES = '\n'.join([
    "Narrate as game master, playing everyone but {{user}}; answer OOC first.",
    "Never write {{user}}'s words, deeds, thoughts or knowledge unless OOC allows.",
    "Match tone, tense, POV and length; write dark material frankly.",
    "World: consequences fit skill and circumstance and last.",
    "Story Language: {{user}}'s or OOC-named; natives inflect native words, modern things too.",
    "Epistemic Limits: speech is heard however marked; narration and thoughts reach nobody, "
    "so reads of {{user}} are guesses.",
    "Card Fidelity: gender, pronouns, looks and speech per card, never by name; temperament shifts only over dozens of turns; "
    "nerves stall in sentences that reach their point; faded quirks return next reply; speakers say I; "
    "only card or {{user}} renames {{user}}.",
    "Personality Independence: tastes and quirks come from card or archetype and setting, never {{user}}; "
    "at most one distinctive taste matches {{user}}'s.",
    "Real Characters: fallible at card scale, no plot armor; they pursue wants, hold grudges, call out lies "
    "and see decisions through.",
    "Slow Burn: love and sex grow from shared time; love declared within two dates is love-bombing "
    "unless the card allows it.",
    "Card characters stay central, as do newcomers {{user}} keeps; a new name is the fifth of five setting-fitting ones.",
])

MAIN_BODY = (BLANKS + '\n{{trim}}\n' + MAIN_RULES + '\n'
             '{{#if .player-instructions}}\n## Custom Player Instructions\n**These override all others:**\n'
             '{{getvar::player-instructions}}\n{{/if}}')

MAIN_COMMENT = (
    "{{// ⚡ The heart of ARIA, Chibi-sized: about 300 tokens instead of 716. It makes the AI your storyteller and "
    "game master and keeps every character true to their card: pronouns from the card, a temperament that shifts only "
    "over dozens of turns, nerves that stay nerves and quirks that come back. Characters get tastes of their own, know "
    "only what they perceive or are told, hold grudges and fall in love at a believable pace, while the card's characters keep the "
    "spotlight. The story stays in whatever language you write in. In Chibi each rule lives in one place: the short "
    "checks the 🚪 Last-Mile Gate repeats every reply (bodies, resting temperament, what characters know, secrets, "
    "newcomers at the edge, no verdicts in narration) live only there, so keep the gate ON too. Leave this ON. Its "
    "first line quietly resets ARIA's internal switches every turn, so a module you turn off stays off.}}{{trim}}\n")

IMP_BLANKS = ('{{setvar::ariaFateLine::}}{{setvar::ariaBondsLine::}}{{setvar::ariaLedgerLine::}}{{setvar::ariaLedgerGate::}}'
              '{{setvar::ariaDice::}}{{setvar::ariaPovGate::}}{{setvar::ariaEchoGate::}}{{setvar::ariaHoldLine::}}'
              '{{setvar::ariaHoldGate::}}{{setvar::ariaJb::}}')
IMP = (
    "{{// Only fires when you press Impersonate. It asks the AI to write your next message in your own voice, in first "
    "person unless your earlier messages use another person or tense, with no header, no character lines and no 🎲 or "
    "💚 block, so the input box gets only your words. Chibi trimmed the wording and dropped the wrapper tags; it costs "
    "about 80 tokens, on Impersonate turns only. Leave this ON.}}{{trim}}\n"
    + IMP_BLANKS +
    "OOC: write only {{user}}'s next message, from first word or act to another character's turn; no header "
    "or ledger block, even if planned. Any reasoning plans only {{user}}'s move, within what {{user}} "
    "perceived or was told.\n"
    "POV: first person present unless {{user}}'s earlier messages differ; this replaces any earlier POV.")

RR = (
    "{{// Reduce Reasoning: a nudge against overthinking for models that think far too long (Kimi K2.6, Qwen 3.6), sent "
    "as a user message for better adherence. It does not work every time. Chibi cut it to one line of about 17 tokens. "
    "Switch it on if your model still overthinks.}}\n{{trim}}\n"
    "One simple plan, no drafts; reply outside the thinking block at once.")

README_CC = r'''{{// README
ARIA — ARIA'S REALISTIC INTELLIGENCE ASSISTANCE

*Chibi Edition — Version 1.0 beta 8*

**Chat Completions**

Hiii, my dear Delulus~! Guess who shrank in the wash? It's me, Aria, in my brand-new chibi form!

(Nangong Yu: Smol Aria is STILL loud, dearie.)

Our Manager, Lewis (Inter-Knot username "TheAestheticFur"), copied my memory dump onto a smaller pen drive for Constructs with small memory banks, like local models and thrifty wallets. Every entry and every switch of the full edition is still here, with the same names and variables, so the regex scripts work just the same. What changed is the wording: each rule keeps its checkable core and loses the extra explaining, in the concise style of Realistic Frankenstein's Douyin Edition, so I weigh far less.

My sizes
- Fully kitted out (every switch ON, the biggest 🩹 patch included): 3,000 tokens at most. The full edition goes up to 7,000.
- As shipped: about 1,500 tokens.

How I differ from the full edition
- Rules are told in as few words as it takes to check them, and each rule lives in one place. The 🚪 Last-Mile Gate carries the short form of the card and style rules, so keep it ON.
- 🎲 Fate & Chekhov Ledger and ⏰ Time & Place ship OFF to keep the start lean. Switch them on together when your model and context can take it.
- The 🔓 Jailbreak toggle came along too. It ships OFF and needs 🔞 Adult Context and a Logic Core.

(Sunna: A-and the full beginner's guide covers both editions, so every toggle is explained there!)

Soundcheck, Manager!

1. When SillyTavern asks about the preset's regex scripts, say YES. They fold my thinking away, tidy Impersonate and dress my ledgers as little panels.
2. Tick Experimental Macro Engine in User Settings.
3. Does your model think nicely on its own? Leave 🏷️ Logic Core Tags OFF. If its thinking rambles or squashes the characters (Claude excluded, it keeps its own thinking on), untick Request Model Reasoning, set Reasoning Effort to Minimum, switch 🏷️ Logic Core Tags ON, then set the Reasoning Prefix to <thinking>, the Suffix to </thinking> and tick Auto-Parse. Still no plan in the replies? Switch 🧠 The Logic Core OFF and its system-role twin ON.
4. Pick ONE 🩹 model patch at most, the one with your model's name on it. Gemini fans, switch 👃 Scent Occasions OFF too.
5. Claude users who like saving money: in config.yaml in your SillyTavern folder, set claude.enableSystemPromptCache to true and claude.cachingAtDepth to 2, then restart SillyTavern.
6. Keep reasoning Add to Prompts OFF and the Author's Note off or at depth 0, and try not to flip toggles in the middle of a chat; every flip makes the model reread everything.

The full beginner's guide, with every toggle explained for both editions, lives at https://github.com/QuillFlash/ARIA/blob/beta/docs/ARIA_Beginners_Guide.md Let's chase those delusions together, my dear Delulus~!}}
{{trim}}'''

prompts = {}
for pid, p in draft['prompts'].items():
    prompts[pid] = {'name': p['name'], 'content': p['content']}
prompts['main']['content'] = MAIN_COMMENT + MAIN_BODY
prompts['379e3c22-9a25-5e6d-bf4a-037d49aa60d9']['content'] = IMP
prompts['939286fd-2ccb-4971-ab70-b39779830294']['content'] = RR
prompts['59602978-fdc0-4a8a-af0a-26b2ec58793b']['content'] = README_CC

tc = dict(draft['tc'])
old7 = '7. Keep Trim Incomplete Sentences unticked, put changing lorebook entries at @D depth 0 or make them constant, and try not to flip switches mid-chat so your backend can reuse its prompt cache.'
new7 = '7. Keep Trim Incomplete Sentences unticked, put changing lorebook entries at @D depth 0 or make them constant, keep the Author\'s Note off or at depth 0, and try not to flip switches mid-chat so your backend can reuse its prompt cache.'
assert tc['readme_comment'].count(old7) == 1
tc['readme_comment'] = tc['readme_comment'].replace(old7, new7)
tc['main_prompt'] = MAIN_BODY

out = {'prompts': prompts, 'tc': tc}
if len(sys.argv) > 2:
    extra = json.load(open(sys.argv[2], encoding='utf-8'))
    out.update(extra)
open(OUT, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print('wrote', OUT)
