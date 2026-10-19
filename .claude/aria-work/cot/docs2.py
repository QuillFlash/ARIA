#!/usr/bin/env python3
"""Guide edits for the second pass: Micro's Completion line, its failure and game-state rules, adults-only Mode lines,
Freaky's mode check, and the re-measured figures."""
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
sub('My rules come to roughly 4,340 tokens as shipped and about 6,110 fully kitted out',
    'My rules come to roughly 4,420 tokens as shipped and about 6,200 fully kitted out')

# section 4
sub("takes creative risks over perfect ones, starts on your OOC line and writes every line in order without skipping one.",
    "takes creative risks over perfect ones, starts on the game state and writes every line in order, since a skipped line "
    "counts as a failure.")
sub("With 🔞 Adult Context on, the plan's Mode line works out each sexual, violent, cruel or dark beat in full. It still runs "
    "both ways:",
    "With 🔞 Adult Context on, the plan's Mode line works out each sexual, violent, cruel or dark beat in full, with sex only "
    "between adults. Like Micro's last task, a Completion line closes the plan: the AI restates that it's the game master "
    "and not a helpful AI assistant, then closes its reasoning and writes the reply at once. It still runs both ways:")
sub("what happens, the bodies, the sensations and the tone.\n",
    "what happens, the bodies, the sensations and the tone, with sex only between adults.\n")
sub("Its line in my plan has the AI describe everyone lewdly, with details new to the last four replies.",
    "Its line in my plan has the AI line everyone's wants up with yours and describe them lewdly, with details new to the "
    "last four replies.")

# section 6
sub("| ~500 tokens per turn as shipped, plus a few seconds of planning |", "| ~570 tokens per turn as shipped, plus a few seconds of planning |")
sub("| ~30 tokens, already counted in the Logic Core's 500 |", "| ~25 tokens, already counted in the Logic Core's 570 |")
sub("🎲 Fate and 🥰 Bonds Lite cost about 50 more, 🔞 Adult Context and 🧷 Character Hold about 40 more,",
    "🎲 Fate and 🥰 Bonds Lite cost about 50 more, 🔞 Adult Context about 45 more, 🧷 Character Hold about 40 more,")

# section 7
sub("| Chat Completions, shipped default | ~4,340 | ~1,550 |", "| Chat Completions, shipped default | ~4,420 | ~1,550 |")
sub("| Chat Completions, fully kitted out (everything ON, with the largest patch, 🩹 GLM) | ~6,110 | 2,976 |",
    "| Chat Completions, fully kitted out (everything ON, with the largest patch, 🩹 GLM) | ~6,200 | 2,976 |")
sub("| Text Completions, plus The Logic Core, Fate and Time & Place | ~4,410 | ~2,065 |",
    "| Text Completions, plus The Logic Core, Fate and Time & Place | ~4,490 | ~2,060 |")
sub("| Text Completions, everything ON (🩹 GLM, 🔦 Flash Gate and 🧷 Character Hold included) | ~6,100 | 2,993 |",
    "| Text Completions, everything ON (🩹 GLM, 🔦 Flash Gate and 🧷 Character Hold included) | ~6,190 | 2,991 |")
sub("| Marinara, everything ticked with 🩹 GLM, no agents | ~6,120 | 2,984 |", "| Marinara, everything ticked with 🩹 GLM, no agents | ~6,210 | 2,983 |")
sub("| Marinara, the same with the Agents state backend | ~6,380 | 3,070 |", "| Marinara, the same with the Agents state backend | ~6,470 | 3,070 |")
sub("the nearest is 🩹 MiMo V2.6 Flash at 2,999.", "the nearest is 🩹 MiMo V2.6 Flash at 2,998.")
sub("| 🧠 The Logic Core, with every module's lines in it | 914 | 595 |", "| 🧠 The Logic Core, with every module's lines in it | 1,003 | 595 |")
start = t.index('- **The same Micro-based 🧠 Logic Core, in fewer words.**')
end = t.index('\n', start) + 1
t = (t[:start] + "- **The same Micro-based 🧠 Logic Core, in fewer words.** Chibi's plan starts on the game state with every line in "
     "order, keeps even-handed outcomes, full acts (a fight, a lie, a seduction or a refusal, nervous cards aside) and the Mode "
     "line's plan for an adult beat between adults, and ends on the same Completion line: game master, not a helpful AI "
     "assistant, creative risk over perfection, reply at once. To fit the cap it says the game-master line once, at the end, "
     "where the full plan says it at both ends, and its Freaky line leaves the four-reply rule for fresh details to the "
     "gate's Senses line.\n" + t[end:])
sub("| `aria-logic-core` | on | ~335 | ~500 |", "| `aria-logic-core` | on | ~335 | ~570 |")
sub("| `aria-thinking-tags` | on | ~55 | ~30 |", "| `aria-thinking-tags` | on | ~55 | ~25 |")
sub("| `aria-adult` | off | ~100 | ~155 |", "| `aria-adult` | off | ~105 | ~160 |")
sub("| `aria-freaky` | off | ~20 | ~55 |", "| `aria-freaky` | off | ~20 | ~65 |")

# section 9
sub("| Core (everything that ships ON except Fate and Time & Place) | ~3,340 |",
    "| Core (everything that ships ON except Fate and Time & Place) | ~3,420 |")
sub("| Shipped default | ~4,340 |", "| Shipped default | ~4,420 |")
sub("and the largest model patch, now 🩹 GLM) | ~6,110 |", "and the largest model patch, now 🩹 GLM) | ~6,200 |")
sub("| Plus The Logic Core, Fate and Time & Place | ~4,410 |", "| Plus The Logic Core, Fate and Time & Place | ~4,490 |")
sub("| Everything ON (largest patch, 🔦 Flash Gate and 🧷 Character Hold included) | ~6,100 |",
    "| Everything ON (largest patch, 🔦 Flash Gate and 🧷 Character Hold included) | ~6,190 |")
sub("| `logicCoreLines` | 🧠 The Logic Core itself: 7 plus one per Mode,", "| `logicCoreLines` | 🧠 The Logic Core itself: 8 plus one per Mode,")
sub("The plan has seven fixed lines plus the lines of the modules that run:", "The plan has eight fixed lines plus the lines of the modules that run:")
sub("the rule that every line gets written in order and none skipped, Micro's neutrality and full actions in the Move line, its "
    "adult-mode question in the Mode line that 🔞 Adult Context and 😈 Freaky Override hand over, and, inside the model's own "
    "reasoning, its cue that reasoning ends at go.",
    "its rules that the reasoning starts on the game state and that a skipped line is a failure, Micro's neutrality and full "
    "actions in the Move line, its adult-mode question and Freaky mode check in the Mode line that 🔞 Adult Context and 😈 "
    "Freaky Override hand over, its Completion task as the eighth fixed line, where the AI restates its game-master identity "
    "and commits to writing the reply at once, and, inside the model's own reasoning, its cue that every line is done and "
    "reasoning ends at go.")
sub("The plan's opening is longer by about 55 tokens and its Move line by about 45, so watch whether the thinking creeps "
    "longer,",
    "The plan is about 190 tokens longer than before, with a longer opening, a longer Move line and Micro's Completion line "
    "at the end, so watch whether the thinking creeps longer,")
sub("It only changes how the plan frames each scene, so a model that refuses certain content no matter what any preset says "
    "will keep refusing.\n",
    "It only changes how the plan frames each scene, so a model that refuses certain content no matter what any preset says "
    "will keep refusing. The first version worked on the Chinese models most of the time while Gemini 4 Argon stayed "
    "censored, so the second added Micro's Completion line, its failure and game-state rules and its post-reasoning cue: "
    "tell me whether Gemini still softens or refuses.\n")
sub("The Chat Completions default now sits at about 4,340 tokens and fully kitted out", "The Chat Completions default now sits at about 4,420 tokens and fully kitted out")
sub("at about 6,110 of the checker's 7,000, with the Text Completions file at about 6,100.",
    "at about 6,200 of the checker's 7,000, with the Text Completions file at about 6,190.")
sub("sit at 2,976 (Chat Completions) and 2,993 (Text Completions).", "sit at 2,976 (Chat Completions) and 2,991 (Text Completions).")
sub("the Micro-based Logic Core in its place costs about 110 tokens more than the old one.",
    "the Micro-based Logic Core in its place costs about 190 tokens more than the old one.")
sub("the plan opens with the game master's first-person line, and every dashed line shows up, none skipped.",
    "the plan opens with the game master's first-person line, every dashed line shows up, none skipped, and the last one "
    "before `go` is the Completion line.")

P.write_text(t, encoding='utf-8')
print('guide updated')
