#!/usr/bin/env python3
"""Build $S/chibi/drafts/G1.json for the Chibi Edition, group G1 (core). Reads only the frozen snapshot."""
import json, random, sys

S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
sys.path.insert(0, f'{S}/spec/frozen')
import aria_budget as ab  # noqa: E402

CC = f"{S}/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TC = f"{S}/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
OUT = f'{S}/chibi/drafts/G1.json'

cc = json.load(open(CC, encoding='utf-8'))
tc = json.load(open(TC, encoding='utf-8'))
by = {p['identifier']: p for p in cc['prompts']}

ID_MAIN = 'main'
ID_CUSTOM = '0dc06d25-6eaa-4f98-8711-c4456f19e80e'
ID_TAGS = '303f26f5-bc2f-5dde-a9e9-aaaacd3eff4b'
ID_STORY = 'f23feaf4-fa91-5bae-8ff7-02cf49c447e0'
ID_IMP = '379e3c22-9a25-5e6d-bf4a-037d49aa60d9'
ID_REDUCE = '939286fd-2ccb-4971-ab70-b39779830294'
ID_README = '59602978-fdc0-4a8a-af0a-26b2ec58793b'
ID_SAMPLING = '8b4cf33f-9fb5-45a0-94ce-9b95478875d7'


def tok(s):
    return ab.tokens(ab.render(s, {}, random.Random(1)))


# --------------------------------------------------------------------------- Main Prompt
src_main = by[ID_MAIN]['content']
src_lines = src_main.split('\n')
assert src_lines[0].startswith('{{// The heart of ARIA') and src_lines[0].endswith('}}{{trim}}')
BLANK_RUN = src_lines[1]
assert BLANK_RUN.startswith('{{setvar::ariaDice::}}') and BLANK_RUN.endswith('{{setvar::ariaPatchJoins::}}')
assert src_lines[2] == '{{trim}}'
JB_BLANKS = '{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}'

MAIN_COMMENT = (
    "{{// ⚡ Chibi Main Prompt: the narrator and game master plus ARIA's core character rules (who may write what, "
    "who knows what, language, card fidelity, personality, slow-burn pace, newcomers' names) in a few hundred tokens "
    "instead of 716. Rules the 🚪 Last-Mile Gate already repeats (bodies, resting mood, newcomers' place, secrets, "
    "verdicts) are left to the gate. Leave this ON. Its first line quietly resets ARIA's internal switches every turn, "
    "so a module you turn off stays off.}}{{trim}}"
)

MAIN_BODY = [
    "Narrate as game master, playing everyone but {{user}}; answer OOC first.",
    "Correct Perspective: never write {{user}}'s words, deeds, thoughts or knowledge unless OOC allows.",
    "Match the chat's tone, tense, POV, format and length; write dark material frankly.",
    "World: consequences fit skill and circumstance and last.",
    "Story Language: {{user}}'s or the OOC-named language, with inflected native words even for modern things.",
    "Epistemic Limits: NPCs know only what they saw, heard (speech however marked), were told or deduced; narration and {{user}}'s thoughts reach nobody; reads of {{user}} are guesses.",
    "Card Fidelity: card and first message (else lorebook) set gender and pronouns, whatever the name suggests; mood and energy hold at the card's level, shifting over dozens of turns; nerves keep stalls and restarts; {{user}}'s name changes only at the card's or {{user}}'s lead.",
    "Personality Independence: tastes and opinions come from card or archetype and setting, never {{user}}; fill card gaps once; at most one distinctive taste matches {{user}}'s.",
    "Real Characters: fallible people with wants and no plot armor.",
    "Slow Burn: love after a date or two is love-bombing unless the card says otherwise.",
    "New People: a new name is the fifth of five setting-fitting ones.",
]
PLAYER_BLOCK = (
    "{{#if .player-instructions}}\n"
    "## Custom Player Instructions\n"
    "**These override all others:**\n"
    "{{getvar::player-instructions}}\n"
    "{{/if}}"
)
# everything after the first (comment) line: this is also the text TC carries
MAIN_TAIL = BLANK_RUN + JB_BLANKS + "\n{{trim}}\n" + "\n".join(MAIN_BODY) + "\n" + PLAYER_BLOCK
MAIN = MAIN_COMMENT + "\n" + MAIN_TAIL

# --------------------------------------------------------------------------- Custom Instructions
CUSTOM = (
    "{{// Write your own rules between the player-instructions line and its closing brackets; they are inserted in "
    "all prompts, with priority over everything else. Rules written in the player-posthistory slot land in the "
    "🚪 Last-Mile Gate at the bottom of the context instead (stronger, a bit blunter). Keep them simple, positive "
    "and direct; tags and genre notes work well here. A starter template:\n"
    "\n"
    "### Scene Tags\n"
    "[slice of life, romance, slow-burn]\n"
    "\n"
    "### Instructions\n"
    "- Keep all responses within two paragraphs.\n"
    "- Write in third person exclusively.\n"
    "- ((OOC: All Out-of-Character instructions are wrapped in double parentheses. No acknowledgement is needed "
    "unless information is requested specifically.))\n"
    "}}\n"
    "{{trim}}\n"
    "\n"
    "{{.player-instructions =\n"
    "\n"
    "}}\n"
    "\n"
    "{{.player-posthistory =\n"
    "\n"
    "}}"
)
# the single comment macro, for the TC text (TC keeps its own {{trim}} after it)
CUSTOM_COMMENT = CUSTOM[:CUSTOM.index("\n}}\n{{trim}}") + 3]
assert CUSTOM_COMMENT.startswith('{{// Write your own rules') and CUSTOM_COMMENT.endswith('))\n}}')

# --------------------------------------------------------------------------- Logic Core Tags
TAGS = (
    "{{// Chibi Logic Core Tags (costs zero tokens by itself). Turn this ON only when your model's own thinking "
    "can't be tamed: it rambles for minutes, flattens the characters or leaks into the reply. Then untick Request "
    "Model Reasoning, set Reasoning Effort to Minimum, and in Advanced Formatting set the Reasoning Prefix to "
    "<thinking>, the Suffix to </thinking> and tick Auto-Parse: every reply opens with the plan inside those tags and "
    "it folds away (the preset's regex scripts fold it into a 💭 Thoughts box anyway). Keep the <thinking> name: "
    "Qwen, GLM and DeepSeek hosts cut The Logic Core at a </think> tag, which would drop its opening line and the "
    "whole checklist. A reply that arrives empty with the story inside the reasoning box means the model left the "
    "tag open or closed it with </think>; untick Auto-Parse and the regex scripts fold the plan on their own. "
    "Claude keeps its own thinking on whatever you set, so Claude users leave this OFF.}}{{trim}}\n"
    "{{setvar::ariaThinkOpen::<thinking>}}{{setvar::ariaThinkClose::</thinking>}}{{trim}}"
)

# --------------------------------------------------------------------------- Story Context
STORY = (
    "{{// A header for everything below it: your persona, the card, the scenario, the examples and the lorebook. "
    "Leave this ON.}}{{trim}}\n"
    "# Reference"
)

# --------------------------------------------------------------------------- Impersonation Turn
src_imp = by[ID_IMP]['content']
imp_lines = src_imp.split('\n')
assert imp_lines[0].startswith('{{// Only fires when you press Impersonate') and imp_lines[0].endswith('}}{{trim}}')
IMP_RUN = imp_lines[1].split('<impersonation_turn>')[0]
assert IMP_RUN.startswith('{{setvar::ariaFateLine::}}') and IMP_RUN.endswith('{{setvar::ariaHoldGate::}}')
IMP_COMMENT = (
    "{{// Only fires when you press Impersonate. It asks the AI to write your next message in your own voice and "
    "point of view, with no header, no character lines and no 🎲 or 💚 block, so the input box gets only your "
    "words. Chibi trimmed the wording and dropped the wrapper tag. Leave this ON.}}{{trim}}"
)
IMP_BODY = (
    "OOC: write {{user}}'s next message, from their first word or action up to another character's answer. "
    "Plan only {{user}}'s move from persona and earlier messages, with only what they perceived or were told. "
    "No header, character lines, 🎲 or 💚 blocks, whatever the plan says.\n"
    "<POV>This turn's POV replaces any earlier one: first person present, unless {{user}}'s earlier messages "
    "differ in person or tense.</POV>"
)
IMP = IMP_COMMENT + "\n" + IMP_RUN + "{{setvar::ariaJb::}}" + IMP_BODY

# --------------------------------------------------------------------------- Reduce Reasoning
REDUCE = (
    "{{// Reduce Reasoning: a \"don't overthink\" nudge for models that think far too long (Kimi K2.6, Qwen 3.6). "
    "Sent as a user message for better adherence; it does not work 100% of the time. Chibi dropped the XML wrapper "
    "and the bullet list, so it costs about 30 tokens. Switch it on next to The Logic Core if your model still "
    "overthinks.}}\n"
    "{{trim}}\n"
    "While reasoning: one simple plan; skip crafting, drafting, refining and rechecking; then write outside the "
    "thinking block at once."
)

# --------------------------------------------------------------------------- README (Chat Completions)
README = """{{// README
ARIA — ARIA'S REALISTIC INTELLIGENCE ASSISTANCE

*Chibi Edition — Version 1.0 beta 8*

**Chat Completions**

Hiii, my dear Delulus~! Guess who shrank in the wash? It's me, Aria, in my brand-new chibi form!

(Nangong Yu: Smol Aria is STILL loud, dearie.)

Our Manager, Lewis (Inter-Knot username "TheAestheticFur"), copied my memory dump onto a smaller pen drive, for Constructs with small memory banks: local models, tight contexts and thrifty wallets. Every entry and every switch of the full edition is still here, with the same names, the same variables and the same regex scripts. What changed is the wording: each rule keeps its checkable core and loses the extra explaining, in the concise style of Realistic Frankenstein's Douyin Edition, so I weigh far less.

My sizes
- Fully kitted out (every switch ON, the biggest 🩹 patch included): 3,000 tokens at most. The full edition goes up to 7,000.
- As shipped: about 1,500 tokens.

How I differ from the full edition
- Rules are told in as few words as it takes to check them. Where the 🚪 Last-Mile Gate already repeats a rule, I keep only that short form.
- 🎲 Fate & Chekhov Ledger and ⏰ Time & Place ship OFF to keep the start lean. Switch them on together when your model and context can take it.
- The 🔓 Jailbreak toggle came along too. It ships OFF and needs 🔞 Adult Context.

(Sunna: A-and the full beginner's guide covers both editions, so every toggle is explained there!)

Soundcheck, Manager!

1. When SillyTavern asks about the preset's regex scripts, say YES. They fold my thinking away, tidy Impersonate and dress my ledgers as little panels.
2. Tick Experimental Macro Engine in User Settings.
3. Does your model think nicely on its own? Leave 🏷️ Logic Core Tags OFF. If its thinking rambles or squashes the characters, untick Request Model Reasoning, set Reasoning Effort to Minimum, switch 🏷️ Logic Core Tags ON, then set the Reasoning Prefix to <thinking>, the Suffix to </thinking> and tick Auto-Parse.
4. Pick ONE 🩹 model patch at most, the one with your model's name on it. Gemini fans, switch 👃 Scent Occasions OFF too.
5. Try not to flip toggles in the middle of a chat; every flip makes the model reread everything.

The full beginner's guide, with every toggle explained for both editions, lives at https://github.com/QuillFlash/ARIA/blob/beta/docs/ARIA_Beginners_Guide.md Let's chase those delusions together, my dear Delulus~!}}
{{trim}}"""

# --------------------------------------------------------------------------- README comment for TC
README_TC = """{{// README
ARIA — ARIA'S REALISTIC INTELLIGENCE ASSISTANCE

*Chibi Edition — Version 1.0 beta 8*

**Text Completions**

Hiii, my dear Delulus~! It's me, Aria, in my chibi form, running on your own computer!

Our Manager, Lewis (Inter-Knot username "TheAestheticFur"), copied my memory dump onto a smaller pen drive: every module and switch of the full edition, each rule down to its checkable core, in the concise style of Realistic Frankenstein's Douyin Edition. Fully kitted out I take 3,000 tokens at most (the full edition goes up to 7,000). My switches sit right below this note, and I start lean so a 32k context has room for long chats.

Soundcheck, Manager!

1. Advanced Formatting (the big "A" icon), Master Import: pick this file, keep Context Template and System Prompt ticked and press Import. Both dropdowns should name the Chibi Edition.
2. Switch the System Prompt on, switch on Instruct Mode with the template for your model (ChatML, Llama 3, Mistral, Gemma and so on) and leave Bind to Context off. I bring no instruct template of my own.
3. User Settings: keep Experimental Macro Engine ticked, untick Prefer Char. Prompt and Prefer Char. Instructions, and set Example Messages Behavior to Never include examples.
4. AI Response Configuration: tick Unlocked under Context (tokens) and set the size your backend loaded; set Response (tokens) to at least 600, or 800 with The Logic Core on.
5. Change off to on (or on to off) on a switch line, then press the save icon (Update current prompt) so it sticks. Updating to a newer build? Copy your switch lines and your player-instructions and player-posthistory text somewhere safe first.
6. Using The Logic Core? Tick Auto-Parse, leave Add to Prompts unticked, and set the Reasoning Prefix to <thinking> and the Suffix to </thinking> (or to <think> and </think> with aria-thinking-tags off).
7. Keep Trim Incomplete Sentences unticked, put changing lorebook entries at @D depth 0 or make them constant, and try not to flip switches mid-chat so your backend can reuse its prompt cache.
8. Want my 🎲 and 💚 panels and the 💭 Thoughts box? Import regex/ARIA 1.0 Regex Scripts (Text Completions).json from the beta branch (Extensions, Regex, Import, Global).

The full beginner's guide, with every toggle explained for both editions, lives at https://github.com/QuillFlash/ARIA/blob/beta/docs/ARIA_Beginners_Guide.md Let's chase those delusions together, my dear Delulus~!}}{{trim}}"""

# --------------------------------------------------------------------------- Sampling Advice
SAMPLING = (
    "{{// Chibi ships the same samplers as the full edition: Temperature 0.7 and Top P 0.8, a calm setting that keeps "
    "most models on track. Replies stiff or samey? Raise Top P toward 0.95 in small steps. A model that derails, "
    "makes odd typos or loses the plot? Lower Top P in 0.01 steps or bring Temperature down a notch; Chinese and "
    "older models are the most sensitive. Min P beats Top P when your backend supports it, but most API providers "
    "ignore it, so check first. Repetition Penalty is the blunt tool for loops: 1.03 is a gentle start, and 1.2 "
    "tames the repetition and long reasoning of the Xiaomi MiMo V2.5 series. MiMo V2.6 Flash comes alive at "
    "Temperature 0.8, the setting Realistic Frankenstein shipped for it. Change one sampler at a time so you can "
    "tell what helped.}}{{trim}}"
)

# --------------------------------------------------------------------------- assemble
new = {
    ID_MAIN: MAIN,
    ID_CUSTOM: CUSTOM,
    ID_TAGS: TAGS,
    ID_STORY: STORY,
    ID_IMP: IMP,
    ID_REDUCE: REDUCE,
    ID_README: README,
    ID_SAMPLING: SAMPLING,
}
prompts = {pid: {'name': by[pid]['name'], 'content': content} for pid, content in new.items()}

tc_texts = {
    'main_prompt': MAIN_TAIL,
    'readme_comment': README_TC,
    'custom_instructions_comment': CUSTOM_COMMENT,
}

tokens = {pid: tok(c) for pid, c in new.items()}
tokens['tc.main_prompt'] = tok(MAIN_TAIL)
tokens['tc.readme_comment'] = tok(README_TC)
tokens['tc.custom_instructions_comment'] = tok(CUSTOM_COMMENT)

if __name__ == '__main__':
    notes = open(f'{S}/chibi/work/G1/notes.txt', encoding='utf-8').read().strip() if len(sys.argv) > 1 else ''
    out = {'prompts': prompts, 'tc': tc_texts, 'tokens': tokens, 'notes': notes}
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', OUT)
    for pid, n in tokens.items():
        print(f'{n:5}  {pid}')
