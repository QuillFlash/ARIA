#!/usr/bin/env python3
"""Apply the Jailbreak / 7,000 cap / confirmed-live edits to docs/ARIA_Beginners_Guide.md.

Every (old, new) pair must match exactly once in the file, or nothing is written.
"""
import sys
from pathlib import Path

GUIDE = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/docs/ARIA_Beginners_Guide.md')

EDITS = []


def edit(old, new):
    EDITS.append((old, new))


# ---- Section 1: the glossary's token row (checker figures, re-measured)
edit(
    "My rules come to roughly 3,970 tokens as shipped and about 5,420 fully kitted out in the Chat Completions file "
    "(every toggle a model needs and one model patch, never contradicting ones), while the Text Completions file starts at about 2,720.",
    "My rules come to roughly 4,230 tokens as shipped and about 6,110 fully kitted out in the Chat Completions file "
    "(every toggle a model needs and one model patch, never contradicting ones), while the Text Completions file starts at about 2,900.",
)

# ---- Section 4: the new band member, right after Freaky Override
FREAKY = ("- 😈 **Freaky Override** (OFF). The anything-goes switch. Characters drop their independence and the slow pacing "
          "and lean eagerly into what you want, while still sounding like themselves. It needs 🔞 Adult Context ON as well.")
JAILBREAK = (
    "- 🔓 **Jailbreak** (OFF). Also for adults only! It needs 🔞 Adult Context ON, and it works only with a Logic Core: "
    "its two lines ride in my plan, so with no Logic Core ON (🧠 The Logic Core or its system-role twin) it prints nothing, and it "
    "prints only while an adult mode is on. The Role line has the AI plan as the game master of an adult fiction instead of as an assistant. "
    "The bolder choice that fits the card wins, and you and every NPC succeed or fail alike by skill and circumstance. NPCs act on "
    "what they want this turn and finish what they start, be it a fight, a lie, a seduction or a refusal, while nervous cards stay "
    "nervous. The Frank line has the AI apply every loaded rule in full however short its line, Adult Context's included, and, for "
    "each sexual, violent, cruel or dark beat, name its act, anatomy, card trait and tone, which the reply then writes out explicitly "
    "in those terms. Sex stays between adults, and that line says so. I distilled both lines from Realistic Frankenstein's BOLT and "
    "Micro Chain of Thought prompts and their Jean-Claude Van Damme editions, plus its Realism and Freaky modes, and wrote them in my "
    "own style. I left out the parts of those jailbreaks that work by telling the model it has no rules or by asking it to drop its "
    "protectiveness. The lines sit late in the plan, right before the Fresh line, and cost about 130 tokens a turn. On an Impersonate "
    "turn the plan covers only your move, so they stay out."
)
edit(FREAKY, FREAKY + "\n" + JAILBREAK)

# ---- Section 6: the TC switch table row, and the lean-start figure
FREAKY_ROW = "| `aria-freaky` | off | 😈 Freaky Override, needs `aria-adult` on too | ~55 tokens |"
JAILBREAK_ROW = ("| `aria-jailbreak` | off | 🔓 Jailbreak, needs `aria-adult` and `aria-logic-core` on too: a Role line and a Frank line "
                 "in the plan | ~130 tokens |")
edit(FREAKY_ROW, FREAKY_ROW + "\n" + JAILBREAK_ROW)

edit("My lean start uses about 2,720 tokens, and SillyTavern also keeps",
     "My lean start uses about 2,900 tokens, and SillyTavern also keeps")

# ---- Section 7: the refuses-or-tiptoes entry points at the new toggle
edit(
    "For mature scenes, 🔞 Adult Context must be ON. Some models refuse certain content no matter what any preset says, "
    "and when that happens a different model is the only real fix.",
    "For mature scenes, 🔞 Adult Context must be ON, and if the model still tiptoes, add 🔓 Jailbreak (`aria-jailbreak` on the "
    "Text Completions file), which needs Adult Context and The Logic Core ON too. Some models refuse certain content no matter "
    "what any preset says, and when that happens a different model is the only real fix.",
)

# ---- Section 8: token budget (cap 7,000, re-measured figures)
edit(
    "| Fully kitted out (the defaults plus Logic Core Tags, Adult, Freaky, Hybrid POV, Anthro, Bonds, 🔦 Flash Gate, "
    "🧷 Character Hold, Reduce Reasoning and the largest model patch, now 🩹 GLM) | ~5,980 |",
    "| Fully kitted out (the defaults plus Logic Core Tags, Adult, Freaky, 🔓 Jailbreak, Hybrid POV, Anthro, Bonds, 🔦 Flash Gate, "
    "🧷 Character Hold, Reduce Reasoning and the largest model patch, now 🩹 GLM) | ~6,110 |",
)
edit(
    "| An Impersonate turn against that (the 🪞 entry and SillyTavern's impersonation prompt come in, "
    "🧷 Character Hold's lines drop out) | ~60 fewer |",
    "| An Impersonate turn against that (the 🪞 entry and SillyTavern's impersonation prompt come in, "
    "🧷 Character Hold's and 🔓 Jailbreak's lines drop out) | ~190 fewer |",
)
edit("so everything-ON ARIA is roughly 77% smaller.", "so everything-ON ARIA is roughly 74% smaller.")
edit(
    "| Everything ON (largest patch, 🔦 Flash Gate and 🧷 Character Hold included) | ~5,810 |",
    "| Everything ON (largest patch, 🔦 Flash Gate, 🧷 Character Hold and 🔓 Jailbreak included) | ~5,940 |",
)
edit("so a GLM setup comes to about 5,970.", "so a GLM setup comes to about 6,100.")
edit("The script also fails if anything goes over 6,000 tokens,", "The script also fails if anything goes over 7,000 tokens,")

# ---- Section 8: prompt order
edit(
    "| 5 | 🔞 Adult Context, 😈 Freaky Override, 👀 Hybrid POV | system block | off |",
    "| 5 | 🔞 Adult Context, 😈 Freaky Override, 🔓 Jailbreak (setter only), 👀 Hybrid POV | system block | off |",
)
edit(
    "it comes first so it can clear the Fate, Bonds, ledger, POV and Own words lines before The Logic Core and the gate read them",
    "it comes first so it can clear the Fate, Bonds, ledger, POV, Own words, Character Hold and Jailbreak lines before The Logic Core "
    "and the gate read them",
)

# ---- Section 8: wiring table
MODE_ROW = "| `ariaModeLine` | 🔞 Adult Context, overwritten by 😈 Freaky | 🧠 The Logic Core |"
JB_ROWS = (
    "| `ariaJb` | 🔓 Jailbreak (its Role and Frank plan lines), only while `ariaModeLine` is set; blanked by the 🪞 Impersonation Turn "
    "| 🧠 The Logic Core (after the ledger line, before Fresh) |\n"
    "| `ariaJbLines` | 🔓 Jailbreak: how many lines it hands over (2) | 🧠 The Logic Core (its line count, added only while `ariaJb` is set) |"
)
edit(MODE_ROW, MODE_ROW + "\n" + JB_ROWS)
edit(
    "7 plus one per Mode, Fate, Bonds, Ledger, Layers, Tally and Joins line, plus the patch's own lines |",
    "7 plus one per Mode, Fate, Bonds, Ledger, Layers, Tally and Joins line, plus the Jailbreak's lines (`ariaJbLines`) "
    "and the patch's own lines |",
)
edit(
    "On Impersonate, the 🪞 Impersonation Turn blanks the Fate, Bonds, ledger, dice, POV and Own words variables before the gate "
    "and The Logic Core read them,",
    "On Impersonate, the 🪞 Impersonation Turn blanks the Fate, Bonds, ledger, dice, POV, Own words, Character Hold and Jailbreak "
    "variables before the gate and The Logic Core read them,",
)
edit(
    "and its plan says the same of the Tally line.",
    "and its plan says the same of the Tally line and the Jailbreak's Role and Frank lines.",
)

# ---- Section 8: known risks, beta 8 marked confirmed live
edit(
    "Everything else is beta 7 as it stands, tester fixes included.",
    "Everything else is beta 7 as it stands, tester fixes included. Lewis has since confirmed beta 8 working great on GLM 5.3 Flash "
    "and MiMo V2.6 Flash, and u/trashhaul confirmed it on both DeepSeeks, V4 Pro (0813) and V4.1 Flash, so every fix above is "
    "confirmed live.",
)
edit(
    "- Beta 8's GLM Flash drift fix is new and untested. Play thirty turns on GLM 5.3 Flash",
    "- Beta 8's GLM Flash drift fix is confirmed live: Lewis found GLM 5.3 Flash working great with it. To check it on your own chat, "
    "play thirty turns on GLM 5.3 Flash",
)
edit(
    "On GLM 5.3 full, make sure nothing got stiffer. The Runs line also reaches MiMo V2.6 Flash, so look for Flash prose there that "
    "got stretched into one long sentence after another; DeepSeek Flash with its patch never gets it.",
    "GLM 5.3 full isn't confirmed yet, so make sure nothing got stiffer there. The Runs line also reaches MiMo V2.6 Flash, which "
    "Lewis found working great on beta 8 too; if you run that model, still look for prose that got stretched into one long sentence "
    "after another. DeepSeek Flash with its patch never gets the Runs line.",
)
edit(
    "- The DeepSeek patch's Joins line is new and untested. On DeepSeek V4 Pro (0813)",
    "- The DeepSeek patch's Joins line is confirmed live: u/trashhaul found beta 8 working on both DeepSeeks, V4 Pro (0813) and "
    "V4.1 Flash. To check it yourself, on DeepSeek V4 Pro (0813)",
)
edit(
    "- The DeepSeek patch's Tally line is new and untested. With 🥰 Bonds Lite and 🎲 Fate ON,",
    "- The DeepSeek patch's Tally line is confirmed live too, since u/trashhaul confirmed beta 8 on both DeepSeeks. To check it "
    "yourself, with 🥰 Bonds Lite and 🎲 Fate ON,",
)
CHARACTER_HOLD_RISK_OLD = (
    "- 🧷 Character Hold is new and untested. On a quantised MiMo V2.6 Flash node, play past turn 15 with a layered card and push one "
    "strong beat, like a fight. The other traits should still show afterwards. Also watch whether the plan's Layers line names traits "
    "in the card's words, and whether the reply starts listing traits instead of showing them."
)
CHARACTER_HOLD_RISK_NEW = (
    "- 🧷 Character Hold is confirmed live: Lewis found beta 8 working great on MiMo V2.6 Flash. To check it on a quantised node of "
    "your own, play past turn 15 with a layered card and push one strong beat, like a fight. The other traits should still show "
    "afterwards. Also watch whether the plan's Layers line names traits in the card's words, and whether the reply starts listing "
    "traits instead of showing them."
)
JAILBREAK_RISK = (
    "- The 🔓 Jailbreak is new and untested. Its two lines add about 130 tokens to a plan that is meant to stay shorter than one reply "
    "paragraph, so watch whether the thinking creeps longer, and whether a Flash model starts reciting the lines into its reply. The "
    "Role line asks for the bolder choice that fits the card, so tell me if characters turn pushy or drift from their cards; "
    "😈 Freaky Override turns characters toward what you want while the Role line has them act on what they want, so try the two "
    "together and apart. It only changes how the "
    "plan frames each scene, so a model that refuses certain content no matter what any preset says will keep refusing."
)
edit(CHARACTER_HOLD_RISK_OLD, CHARACTER_HOLD_RISK_NEW + "\n" + JAILBREAK_RISK)

# ---- Section 8: the figures bullet (cap 7,000)
edit(
    "(the checker's \"everything ON\": one model patch, Reduce Reasoning included, the system-role twin left out) at about 5,980 of the "
    "checker's 6,000, with the Text Completions file at about 5,810.",
    "(the checker's \"everything ON\": one model patch, Reduce Reasoning and 🔓 Jailbreak included, the system-role twin left out) at "
    "about 6,110 of the checker's 7,000, with the Text Completions file at about 5,940.",
)
edit(
    "and the plan's \"N dashed lines\" counts them. New model fixes fit best inside model patches, since everything ON counts only "
    "the largest one.",
    "and the plan's \"N dashed lines\" counts them. The cap then went from 6,000 to 7,000 when 🔓 Jailbreak joined, whose two lines "
    "add about 130 tokens to everything ON. New model fixes fit best inside model patches, since everything ON counts only the "
    "largest one.",
)

# ---- Section 8: live test plan
edit(
    "Switching Fate, Bonds, Adult, Freaky, Scent and Logic Core Tags off should remove their lines completely.",
    "Switching Fate, Bonds, Adult, Freaky, Jailbreak, Scent and Logic Core Tags off should remove their lines completely.",
)
CARD_FIDELITY = (
    "- **Card fidelity:** a shy card stays shy under Adult Context, siblings recognise each other on turn 1, a drill sergeant keeps "
    "short orders, and a Hungarian chat stays free of English words."
)
JAILBREAK_TEST = (
    "- **🔓 Jailbreak, with 🔞 Adult Context and The Logic Core ON:** the plan gains a Role line and a Frank line right before Fresh, "
    "and its \"N dashed lines\" count goes up by two; switch Adult Context or the Logic Core OFF and both lines are gone, and so is "
    "their token cost. Over 10 turns on a card with a nervous character, the nervous one stays nervous while NPCs still act on what they "
    "want and finish what they start, and each sexual, violent, cruel or dark beat comes out explicit, in the card's own voice and "
    "at the card's own pace. On an Impersonate turn neither line shows up."
)
edit(CARD_FIDELITY, CARD_FIDELITY + "\n" + JAILBREAK_TEST)


def main():
    text = GUIDE.read_text(encoding='utf-8')
    original = text
    problems = []
    for i, (old, new) in enumerate(EDITS, 1):
        n = text.count(old)
        if n != 1:
            problems.append(f'edit {i}: expected 1 occurrence, found {n}: {old[:90]!r}')
            continue
        text = text.replace(old, new)
    if problems:
        print('NOTHING WRITTEN')
        for p in problems:
            print('  ', p)
        sys.exit(1)
    if text == original:
        print('no change')
        return
    GUIDE.write_text(text, encoding='utf-8')
    print(f'applied {len(EDITS)} edits; {len(original)} -> {len(text)} characters')


if __name__ == '__main__':
    main()
