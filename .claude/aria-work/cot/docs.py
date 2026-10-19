#!/usr/bin/env python3
"""Guide edits for the Micro-based Logic Core, the Gemini 4 Argon tags entry and the 🔓 Jailbreak's removal."""
from pathlib import Path

P = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/docs/ARIA_Beginners_Guide.md')
t = P.read_text(encoding='utf-8')


def sub(old, new, count=1):
    global t
    n = t.count(old)
    if n != count:
        raise SystemExit(f'expected {count} of {old[:100]!r}, found {n}')
    t = t.replace(old, new)


# glossary
sub('My rules come to roughly 4,230 tokens as shipped', 'My rules come to roughly 4,340 tokens as shipped')

# section 3: Gemini 4 Argon setup and its table row
sub("If that keeps happening with your model, untick **Auto-Parse** and let my regex scripts do the folding.\n\n"
    "Does the reply still start straight with the story",
    "If that keeps happening with your model, untick **Auto-Parse** and let my regex scripts do the folding.\n\n"
    "**Gemini 4 Argon has a setup of its own.** Its reasoning can't be switched off, and it thinks inside `<thought>` tags, "
    "where Gemini 3.8 Flash used `<think>`. So leave **Request Model Reasoning** on and switch 🏷️ **Logic Core Tags: Gemini 4 "
    "Argon** ON in place of the plain one: my plan then opens on `<thought>` inside Gemini's own thought block and ends on `go` "
    "before the story. In **Reasoning Formatting**, set **Prefix** to `<thought>` and **Suffix** to `</thought>`, and tick "
    "**Auto-Parse**. Use one tags entry at most; with both on, the Gemini one wins.\n\n"
    "Does the reply still start straight with the story")
sub('| Gemini | A | 🩹 Gemini | Switch 👃 Scent Occasions OFF |',
    '| Gemini 3.8 Flash and older | A | 🩹 Gemini | Switch 👃 Scent Occasions OFF |\n'
    '| Gemini 4 Argon | Its own: reasoning stays on, with 🏷️ Logic Core Tags: Gemini 4 Argon ON (see above) | 🩹 Gemini | '
    'Switch 👃 Scent Occasions OFF |')

# section 4: The Logic Core, the tags entries, Adult, Freaky, and the Jailbreak goes
sub("The plan arrives as the AI's own message after the chat, which helps many models settle into the scene.\n"
    "- 🪞 **Impersonation Turn**",
    "The plan arrives as the AI's own message after the chat, which helps many models settle into the scene. Since this update "
    "it's rewritten around Realistic Frankenstein's Micro chain of thought, the one that worked in Lewis's tests: the AI plans "
    "in the first person as the game master of the simulation, not a helpful AI assistant, takes creative risks over perfect "
    "ones, starts on your OOC line and writes every line in order without skipping one. You and every NPC succeed or fail "
    "alike, by skill and circumstance, and each character carries their next act all the way through, be it a fight, a lie, a "
    "seduction or a refusal, while nervous characters keep their nerves. With 🔞 Adult Context on, the plan's Mode line works "
    "out each sexual, violent, cruel or dark beat in full. It still runs both ways: inside the model's own reasoning, where the "
    "thinking ends at `go` with no further reasoning, or with tags, where every reply opens with the plan.\n"
    "- 🪞 **Impersonation Turn**")
sub("which would hide my whole checklist.\n- 🔞 **Adult Context** (OFF). For adults only! It unlocks mature stories: sex, "
    "violence and dark themes written frankly. Characters stay themselves all the way through, so a shy character is still shy "
    "in bed.\n",
    "which would hide my whole checklist.\n- 🏷️ **Logic Core Tags: Gemini 4 Argon** (OFF). The same trick for Gemini 4 "
    "Argon, whose reasoning can't be switched off and which thinks inside `<thought>` tags instead of `<think>`. Leave its "
    "reasoning on and switch this ON in place of the plain one, and my plan opens on `<thought>` inside Gemini's own thought "
    "block (section 3). With both on, this one wins.\n- 🔞 **Adult Context** (OFF). For adults only! It unlocks mature "
    "stories: sex, violence and dark themes written frankly. Characters stay themselves all the way through, so a shy "
    "character is still shy in bed. Its line in my plan also works out each sexual, violent, cruel or dark beat in full: what "
    "happens, the bodies, the sensations and the tone.\n")
sub("while still sounding like themselves. It needs 🔞 Adult Context ON as well.\n",
    "while still sounding like themselves. It needs 🔞 Adult Context ON as well. Its line in my plan has the AI describe "
    "everyone lewdly, with details new to the last four replies.\n")
start = t.index('- 🔓 **Jailbreak** (OFF).')
end = t.index('\n', start) + 1
t = t[:start] + t[end:]

# section 6: switch table and notes
sub("| ~405 tokens per turn as shipped, plus a few seconds of planning |", "| ~500 tokens per turn as shipped, plus a few seconds of planning |")
sub("| ~40 tokens, already counted in the Logic Core's 405 |", "| ~30 tokens, already counted in the Logic Core's 500 |")
start = t.index('| `aria-jailbreak` | off | 🔓 Jailbreak, needs')
t = t[:start] + t[t.index('\n', start) + 1:]
sub("a switch that needs another one, like `aria-freaky` or `aria-jailbreak`, is measured with that one on.",
    "a switch that needs another one, like `aria-freaky`, is measured with that one on.")
sub("🎲 Fate and 🥰 Bonds Lite cost about 50 more, 🧷 Character Hold about 40 more,",
    "🎲 Fate and 🥰 Bonds Lite cost about 50 more, 🔞 Adult Context and 🧷 Character Hold about 40 more,")
sub("my Chibi Edition (section 7) starts at about 1,590 tokens", "my Chibi Edition (section 7) starts at about 1,630 tokens")

# section 7: Chibi figures and bullets
sub("| Chat Completions, shipped default | ~4,230 | ~1,500 |", "| Chat Completions, shipped default | ~4,340 | ~1,550 |")
sub("| Chat Completions, fully kitted out (everything ON, with the largest patch, 🩹 GLM) | ~6,110 | 2,978 |",
    "| Chat Completions, fully kitted out (everything ON, with the largest patch, 🩹 GLM) | ~6,110 | 2,976 |")
sub("| An Impersonate turn against that | ~190 fewer | ~120 fewer |", "| An Impersonate turn against that | ~60 fewer | ~65 fewer |")
sub("| Text Completions, lean start | ~2,900 | ~1,590 |", "| Text Completions, lean start | ~2,900 | ~1,630 |")
sub("| Text Completions, plus The Logic Core, Fate and Time & Place | ~4,320 | ~2,025 |",
    "| Text Completions, plus The Logic Core, Fate and Time & Place | ~4,410 | ~2,065 |")
sub("| Text Completions, everything ON (🩹 GLM, 🔦 Flash Gate, 🧷 Character Hold and 🔓 Jailbreak included) | ~6,100 | 2,997 |",
    "| Text Completions, everything ON (🩹 GLM, 🔦 Flash Gate and 🧷 Character Hold included) | ~6,100 | 2,993 |")
sub("| 🧠 The Logic Core, with every module's lines in it | 916 | 596 |", "| 🧠 The Logic Core, with every module's lines in it | 914 | 595 |")
sub("| 🚪 Last-Mile Gate, with every module's lines in it | 1,150 | 815 |", "| 🚪 Last-Mile Gate, with every module's lines in it | 1,149 | 814 |")
start = t.index('- **The 🔓 Jailbreak is in, and OFF.**')
end = t.index('\n', start) + 1
t = (t[:start] + "- **The same Micro-based 🧠 Logic Core, in fewer words.** Chibi's plan keeps the full one's first-person game-master "
     "opening, the every-line rule, even-handed outcomes, full acts (a fight, a lie, a seduction or a refusal, nervous cards "
     "aside) and the Mode line's plan for an adult beat. Its opening line already ends the thinking at `go`, so it skips the "
     "full one's \"no further reasoning\" cue, and its Freaky line leaves the four-reply rule for fresh details to the gate's "
     "Senses line.\n" + t[end:])
sub("| `aria-logic-core` | on | ~300 | ~405 |", "| `aria-logic-core` | on | ~335 | ~500 |")
sub("| `aria-thinking-tags` | on | ~55 | ~40 |", "| `aria-thinking-tags` | on | ~55 | ~30 |")
sub("| `aria-adult` | off | ~85 | ~130 |", "| `aria-adult` | off | ~100 | ~155 |")
sub("| `aria-freaky` | off | ~30 | ~50 |", "| `aria-freaky` | off | ~20 | ~55 |")
sub("| `aria-jailbreak` | off | ~55 | ~130 |\n", "")

# section 8
sub("check that the Prefix is exactly `<thinking>` and the Suffix exactly `</thinking>`, with no spaces.",
    "check that the Prefix is exactly `<thinking>` and the Suffix exactly `</thinking>`, with no spaces (`<thought>` and "
    "`</thought>` on Gemini 4 Argon with its own tags entry).")
sub("For mature scenes, 🔞 Adult Context must be ON, and if the model still tiptoes, add 🔓 Jailbreak (`aria-jailbreak` on "
    "the Text Completions file), which needs Adult Context and The Logic Core ON too.",
    "For mature scenes, 🔞 Adult Context must be ON: its line in my plan works out each adult beat in full, and The Logic "
    "Core's game-master opening keeps the AI out of its helpful-assistant voice.")

# section 9: budgets, checker, order, wiring, features, risks, tests
sub("| Core (everything that ships ON except Fate and Time & Place) | ~3,230 |",
    "| Core (everything that ships ON except Fate and Time & Place) | ~3,340 |")
sub("| Shipped default | ~4,230 |", "| Shipped default | ~4,340 |")
sub("the defaults plus Logic Core Tags, Adult, Freaky, 🔓 Jailbreak, Hybrid POV,", "the defaults plus Logic Core Tags, Adult, Freaky, Hybrid POV,")
sub("while the Fate, Bonds, ledger, dice, POV, Own words, 🧷 Character Hold and 🔓 Jailbreak lines drop out) | ~190 fewer |",
    "while the Fate, Bonds, ledger, dice, POV, Own words and 🧷 Character Hold lines drop out) | ~60 fewer |")
sub("| Plus The Logic Core, Fate and Time & Place | ~4,320 |", "| Plus The Logic Core, Fate and Time & Place | ~4,410 |")
sub("| Everything ON (largest patch, 🔦 Flash Gate, 🧷 Character Hold and 🔓 Jailbreak included) | ~6,100 |",
    "| Everything ON (largest patch, 🔦 Flash Gate and 🧷 Character Hold included) | ~6,100 |")
sub("if any render with 🏷️ Logic Core Tags on still names `<logic_core>`, or if anything would break prompt caching. It checks "
    "every combination of the tags, each Logic Core (or none),",
    "if any render with a 🏷️ Logic Core Tags entry on still names `<logic_core>`, or if anything would break prompt caching. It "
    "checks each tags entry on its own (the `<thinking>` one and the Gemini 4 Argon `<thought>` one) or none, each Logic Core "
    "(or none),")
sub("| 4 | 🏷️ Logic Core Tags | system block, setter only | off |",
    "| 4 | 🏷️ Logic Core Tags, then its Gemini 4 Argon copy | system block, setters only | off |")
sub("| 5 | 🔞 Adult Context, 😈 Freaky Override, 🔓 Jailbreak (setter only), 👀 Hybrid POV | system block | off |",
    "| 5 | 🔞 Adult Context, 😈 Freaky Override, 👀 Hybrid POV | system block | off |")
sub("it comes first so it can clear the Fate, Bonds, ledger, POV, Own words, Character Hold and Jailbreak lines before",
    "it comes first so it can clear the Fate, Bonds, ledger, POV, Own words and Character Hold lines before")
sub("(Fate, Bonds, Ledger, Layers, Role, Frank, Own words and POV)", "(Fate, Bonds, Ledger, Layers, Own words and POV)")
for v in ('`ariaJb`', '`ariaJbLines`'):
    start = t.index(f'| {v} |')
    t = t[:start] + t[t.index('\n', start) + 1:]
sub("| `ariaThinkOpen`, `ariaThinkClose` | 🏷️ Logic Core Tags | 🧠 The Logic Core (`{{#if .ariaThinkOpen}}`) |",
    "| `ariaThinkOpen`, `ariaThinkClose` | 🏷️ Logic Core Tags (`<thinking>`), or its Gemini 4 Argon copy (`<thought>`), which "
    "comes later in the list and wins when both are on | 🧠 The Logic Core (`{{#if .ariaThinkOpen}}`) |")
sub("| `ariaPlanCue` | 🧠 The Logic Core or its system-role twin, with 🏷️ Logic Core Tags on |",
    "| `ariaPlanCue` | 🧠 The Logic Core or its system-role twin, with either tags entry on |")
sub("7 plus one per Mode, Fate, Bonds, Ledger, Layers, Tally and Joins line, plus the Jailbreak's lines (`ariaJbLines`) and the "
    "patch's own lines", "7 plus one per Mode, Fate, Bonds, Ledger, Layers, Tally and Joins line, plus the patch's own lines")
sub("blanks the Fate, Bonds, ledger, dice, POV, Own words, Character Hold and Jailbreak variables",
    "blanks the Fate, Bonds, ledger, dice, POV, Own words and Character Hold variables")
sub("and its plan leaves out the Fate, Bonds, Ledger, Layers and Tally lines and the Jailbreak's Role and Frank lines there.",
    "and its plan leaves out the Fate, Bonds, Ledger, Layers and Tally lines there.")
sub("With 🏷️ Logic Core Tags on it carries no wrapper tag and starts on `<thinking>`, the tag the reply has to open with.",
    "With 🏷️ Logic Core Tags on it carries no wrapper tag and starts on `<thinking>` (or `<thought>` with the Gemini 4 Argon "
    "copy), the tag the reply has to open with.")
sub("the 🩹 DeepSeek patch's Tally and Joins, 🔓 Jailbreak's Role and Frank, and the patch's own lines.",
    "the 🩹 DeepSeek patch's Tally and Joins, and the patch's own lines.")
sub("works as a set of instructions for the prose, with or without a plan.\n",
    "works as a set of instructions for the prose, with or without a plan. Since this update the plan carries Realistic "
    "Frankenstein's Micro chain of thought: the first-person game-master identity with creative risk over perfection, the "
    "rule that every line gets written in order and none skipped, Micro's neutrality and full actions in the Move line, its "
    "adult-mode question in the Mode line that 🔞 Adult Context and 😈 Freaky Override hand over, and, inside the model's own "
    "reasoning, its cue that reasoning ends at go. Micro's pointer to Realistic Frankenstein's legal-pretext and prefill "
    "blocks stayed out, since ARIA has neither.\n")
start = t.index('- The 🔓 Jailbreak is new and untested.')
end = t.index('\n', start) + 1
t = (t[:start] +
     "- The Micro-based Logic Core is new and untested in this form. Realistic Frankenstein's Micro chain of thought worked in "
     "Lewis's tests where my 🔓 Jailbreak toggle didn't, so the toggle is gone and its ideas live in the plan itself. The "
     "plan's opening is longer by about 60 tokens and its Move line by about 50, so watch whether the thinking creeps longer, "
     "whether characters turn pushy or drift from their cards now that every act is carried through, and whether a Flash model "
     "recites the opening lines into its reply. It only changes how the plan frames each scene, so a model that refuses "
     "certain content no matter what any preset says will keep refusing.\n"
     "- 🏷️ Logic Core Tags: Gemini 4 Argon is new and untested. Tell me if Gemini 4 Argon writes the plan outside its thought "
     "block, or if the `<thought>` plan lands in the 💭 Thoughts box instead of SillyTavern's reasoning box.\n" + t[end:])
sub(", and its 🔓 Jailbreak costs about 55 tokens and leaves out the full one's bolder-choice and acting-on-wants wording", "")
sub("The Chat Completions default now sits at about 4,230 tokens and fully kitted out (the checker's \"everything ON\": one model "
    "patch, Reduce Reasoning and 🔓 Jailbreak included, the system-role twin left out)",
    "The Chat Completions default now sits at about 4,340 tokens and fully kitted out (the checker's \"everything ON\": one model "
    "patch and Reduce Reasoning included, the system-role twin left out)")
sub("sit at 2,978 (Chat Completions) and 2,997 (Text Completions).", "sit at 2,976 (Chat Completions) and 2,993 (Text Completions).")
sub("The cap then went from 6,000 to 7,000 when 🔓 Jailbreak joined, whose two lines add about 130 tokens to everything ON.",
    "The cap then went from 6,000 to 7,000 for Realistic Frankenstein's jailbreak pieces. The 🔓 Jailbreak toggle that first "
    "used that room is gone again, and the Micro-based Logic Core in its place costs about 110 tokens more than the old one.")
sub("Switching Fate, Bonds, Adult, Freaky, Jailbreak, Scent and Logic Core Tags off should remove their lines completely.",
    "Switching Fate, Bonds, Adult, Freaky, Scent and either Logic Core Tags entry off should remove their lines completely.")
start = t.index('- **🔓 Jailbreak, with 🔞 Adult Context and The Logic Core ON:**')
end = t.index('\n', start) + 1
t = (t[:start] +
     "- **The Micro-based Logic Core, with 🔞 Adult Context ON:** the plan opens with the game master's first-person line, and "
     "every dashed line shows up, none skipped. Over 10 turns on a card with a nervous character, NPCs carry their acts "
     "through (a fight, a lie, a seduction or a refusal) and your character can fail as easily as anyone, while the nervous "
     "one stays nervous; each sexual, violent, cruel or dark beat comes out in full, in the card's own voice and at its own "
     "pace. Run it once inside the model's own reasoning and once with 🏷️ Logic Core Tags, since the plan has to work both "
     "ways, and watch whether the thinking creeps longer.\n" + t[end:])
sub("everyone else stays in third person, and only you move your character.\n",
    "everyone else stays in third person, and only you move your character.\n"
    "- **Gemini 4 Argon with 🏷️ Logic Core Tags: Gemini 4 Argon ON** and its reasoning on: the thought block opens on "
    "`<thought>`, runs the dashed plan lines and ends on `go` before the story. With Auto-Parse and `<thought>`/`</thought>` "
    "set, the plan lands in SillyTavern's reasoning box; without them, the 💭 Thoughts box catches it.\n")

for bad in ('🔓 Jailbreak (OFF)', 'aria-jailbreak', 'ariaJb', 'Role and Frank', 'Role, Frank'):
    assert bad not in t, bad
P.write_text(t, encoding='utf-8')
print('guide updated;', t.count('Jailbreak'), 'Jailbreak mentions left')
