import re
R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
G = R + "/docs/ARIA_Beginners_Guide.md"
W = R + "/.claude/aria-work/build/docs"
s = open(G, encoding='utf-8').read()
orig = s
section = open(W + "/chibi_section.md", encoding='utf-8').read().rstrip('\n') + '\n'
CHIBI = '(#7-meet-chibi-me-the-chibi-edition)'


def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:90])
    s = s.replace(old, new)


# 1. contents list
rep("7. [Uh-oh! moments](#7-uh-oh-moments)\n8. [Manager's corner (for the curious)](#8-managers-corner-for-the-curious)",
    "7. [Meet Chibi me (the Chibi Edition)](#7-meet-chibi-me-the-chibi-edition)\n8. [Uh-oh! moments](#8-uh-oh-moments)\n"
    "9. [Manager's corner (for the curious)](#9-managers-corner-for-the-curious)")

# 2. section 1 token row
rep("while the Text Completions file starts at about 2,900. |",
    "while the Text Completions file starts at about 2,900. My pocket-sized Chibi Edition (section 7) comes to about 1,500 as shipped and 3,000 at most. |")

# 3. section 2 intro
rep("Either way, you need SillyTavern 1.19.0 or newer; its version shows on the welcome screen.",
    "Either way, you need SillyTavern 1.19.0 or newer; its version shows on the welcome screen. "
    "Want my smaller Chibi Edition? It installs the same way, and [section 7]" + CHIBI + " has its file names.")

# 4. section 4 intro
rep("Entries marked **ON** come switched on, and the ones marked **OFF** wait until you want them.",
    "Entries marked **ON** come switched on, and the ones marked **OFF** wait until you want them. These notes describe the full edition. "
    "The Chibi Edition in [section 7]" + CHIBI + " keeps every one of these toggles under the same name, worded more briefly, "
    "with 🎲 Fate & Chekhov Ledger and ⏰ Time & Place switched OFF to start.")

# 5. GLM row in the TC switch table
rep('"for the record" tags | ~320 tokens |', '"for the record" tags | ~315 tokens |')

# 6. note under the TC switch table
rep("The Claude 5 and Gemini patches live only in the Chat Completions file, since those models aren't run through Text Completion.",
    "These costs come from flipping one switch from the shipped state, so The Logic Core is off. With it on, a module's plan lines print too: "
    "🎲 Fate and 🥰 Bonds Lite cost about 50 more, 🧷 Character Hold about 40 more, and the model patches a lot more, because their lines "
    "print in the plan as well as in the gate (🩹 GLM comes to about 610, 🩹 DeepSeek about 440 and 🩹 MiMo V2.6 Flash about 445).\n\n"
    "The Claude 5 and Gemini patches live only in the Chat Completions file, since those models aren't run through Text Completion.")

# 7. fitting into 32k
rep("- **64k or more:** switch on",
    "- **Tight on room anyway:** my Chibi Edition (section 7) starts at about 1,590 tokens, with The Logic Core already on.\n- **64k or more:** switch on")

# 8. new section 7, and renumbering
rep("## 7. Uh-oh! moments", section + "\n---\n\n## 8. Uh-oh! moments")
rep("## 8. Manager's corner (for the curious)", "## 9. Manager's corner (for the curious)")

# 9. token budget: TC row and paragraph
rep("| Everything ON (largest patch, 🔦 Flash Gate, 🧷 Character Hold and 🔓 Jailbreak included) | ~5,940 |",
    "| Everything ON (largest patch, 🔦 Flash Gate, 🧷 Character Hold and 🔓 Jailbreak included) | ~6,100 |")
rep("The checker sizes each patch on its own, where 🩹 MiMo V2.6 Flash comes out largest, so that's the patch in this row. "
    "With everything ON, 🩹 GLM's five lines land in the plan as well, so a GLM setup comes to about 6,100. Beta 5 measured",
    "The checker ranks the patches over a setup with every other switch on, the way it does for the Chat Completions file, so the largest one in this "
    "row is 🩹 GLM, whose five lines print in the plan as well as in the gate. (Before beta 8's checker fix it sized each patch with every other "
    "switch off, picked 🩹 MiMo V2.6 Flash and showed this row as about 5,940.) Beta 5 measured")
rep("Its presets carry their own names, so you can import them next to the current ones. Its regex file uses the same script names as mine, so on the Text Completions file swap it in only while you test beta 5 and put the current file back afterwards, the way section 6 describes.\n",
    "Its presets carry their own names, so you can import them next to the current ones. Its regex file uses the same script names as mine, so on the Text Completions file swap it in only while you test beta 5 and put the current file back afterwards, the way section 6 describes.\n\n"
    "The Chibi Edition's files are measured the same way against a cap of 3,000 tokens, which the checker gives to any preset with Chibi Edition in its file name. [Section 7]"
    + CHIBI + " lists their figures.\n")

# 10. checker paragraph
rep("The script also fails if anything goes over 7,000 tokens, if a tag",
    "The script also fails if anything goes over its budget (7,000 tokens, or 3,000 for the Chibi Edition files), if a tag")
rep("and it sizes each patch together with any line it adds to the gate. Run it after every edit.",
    "and it sizes each patch together with any line it adds to the gate. The caching check also leaves every variable behind from an earlier turn "
    "and confirms the system block comes out the same. It runs that for everything ON and again for each model patch on its own over the shared base, "
    "because a variable that one patch sets and another patch prints stays invisible while only one patch is ever on. That's how the Gemini 3.8 Flash "
    "text kept printing through Gemini All-In-One for a turn after the 3.8 patch was switched off, until the Main Prompt's first line began blanking "
    "`gemini38Patch`. The Text Completions files get the same per-patch test. Run it after every edit.")

# 11. prompt order note
rep("| 18 | Reduce Reasoning | In-Chat depth 0, user | off |\n\n### Cache-first rules",
    "| 18 | Reduce Reasoning | In-Chat depth 0, user | off |\n\n"
    "The Chibi Edition's Chat Completions file uses the same order and the same defaults, except that 🎲 Fate & Chekhov Ledger and ⏰ Time & Place ship OFF.\n\n"
    "### Cache-first rules")

# 12. Text Completions edition bullet
rep("- The context template ships with **Trim Incomplete Sentences** off, since the 🎲 and 💚 lines end in an HTML tag that the trimmer doesn't count as the end of a sentence.\n",
    "- The context template ships with **Trim Incomplete Sentences** off, since the 🎲 and 💚 lines end in an HTML tag that the trimmer doesn't count as the end of a sentence.\n"
    "- The Chibi Text Completions file is built the same way, with two differences. `aria-logic-core` ships `on`. And the gate's \"a message written as you skips it\" "
    "notes for the Own words, POV, Ledger and Layers lines print only while The Logic Core is off. With it on, the plan's closing sentence names the lines a message "
    "written as you skips (Fate, Bonds, Ledger, Layers, Role, Frank, Own words and POV), which keeps everything ON under 3,000.\n")

# 13. known risks: budget bullet and a new Chibi bullet
rep("with the Text Completions file at about 5,940. The cap went",
    "with the Text Completions file at about 6,100. The Chibi Edition files have a cap of 3,000 and sit at 2,978 (Chat Completions) and 2,997 (Text Completions). The cap went")
rep("will keep refusing.\n- The Humour line outranks the card.",
    "will keep refusing.\n"
    "- The Chibi Edition is new, and no live model has met it yet. Every rule keeps its checkable core, but shorter wording can land differently, so compare a few scenes "
    "with the full edition on the same card and tell me what feels flatter or gets forgotten. Chibi's Fate has no timed appointments, Ambitions, World-news or Quiet-turn rules, "
    "so don't expect those from it, and its 🔓 Jailbreak costs about 55 tokens and leaves out the full one's bolder-choice and acting-on-wants wording. The Chibi Text Completions "
    "file ships The Logic Core ON and, with it on, names the lines a message written as you skips in the plan's closing sentence instead of in the gate's notes, so a real "
    "Impersonate on a local model is worth trying. Chibi Marinara's Agents path goes about 70 tokens over 3,000 with the 🩹 GLM patch, on purpose.\n"
    "- The Humour line outranks the card.")

# 14. live test plan
rep("On an Impersonate turn neither line shows up.\n- **Gemini 4 Argon with 👀 Hybrid POV,**",
    "On an Impersonate turn neither line shows up.\n"
    "- **Chibi Edition against the full edition,** the same card, 10 turns each, on the model you use: a nervous card should still be nervous, lists stay at one or two items, jokes stay small "
    "and rare, and newcomers keep to the edge. With 🎲 Fate on, the ledger writes a thread's age as n/8, a Deferred item's as n/6 and a Bullet's as n/12, and a MAJOR event stays rare. "
    "With 🥰 Bonds Lite on, BOND moves only at 7 Sparks (5 Grudge cost a point), and with the 🩹 DeepSeek patch the Tally line keeps those numbers moving. "
    "On the Chibi Text Completions file with The Logic Core on, press Impersonate and check that the input box holds only your words, with none of the plan's closing sentence.\n"
    "- **Gemini 4 Argon with 👀 Hybrid POV,**")

# 15. bug report build line
rep("- the build: ARIA 1.0 beta 8, shown in the 🌳 README entry (Chat Completions) or in the template name (Text Completions)",
    "- the build: ARIA 1.0 beta 8, full or Chibi Edition, shown in the 🌳 README entry (Chat Completions) or in the template name (Text Completions)")

assert s != orig
open(G, 'w', encoding='utf-8').write(s)
print('guide written', len(orig), '->', len(s))
