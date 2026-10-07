# ARIA 1.0 beta 5: every model fix

This folder keeps ARIA 1.0 beta 5 exactly as it shipped at commit 32f062f, before the second compression. Import the two presets and the regex file from here to compare a new build with beta 5 side by side, since their file names keep them apart from the current ones.

The list below is the regression checklist for the compression. Each entry names the models it was made for, the symptom testers saw, the fix, the exact wording beta 5 carries, where it lives and the commits that made it. "User" stands for `{{user}}` in quoted prompt text.

## Rules the compression has to respect

1. Labels must stay exact. These are Contrast, Chop, Register, Trade, Cadence, Vocabulary, Senses, Skips and Echo, plus the Main labels. Correct Perspective in particular is named by SillyTavern's impersonation_prompt.
2. The echo regexes match template words literally: 'opens the reply, then', '- go', 'closes on the line after go.', 'The reply starts on the line after that', 'Nothing above go enters the reply.', 'When this turn asks for ... Ledger lines.' and 'Every response starts with <thinking>.'. The untagged-plan regexes match the plan labels OOC/Scene/Knows/Mode/Voice/Move/Fate/Bonds/Ledger/Fresh/Check and a '- go' line. The panel regexes need the ledger field labels (q:, hp:, thread:...) and the Name↔Name +n/n/n format. Rewording any of these means updating build_aria.py.
3. build_tc.py asserts the anchors 'Nothing above go enters the reply.', '{{getvar::ariaLedgerGate}}' and the player-posthistory line.
4. Placement rules:
   - Main blanks every variable first.
   - Scent and Logic Core Tags sit below Main.
   - Both Logic Cores sit above the gate.
   - The Impersonation Turn sits above both.
   - Dice and the initial stay at depth 0.
5. Named examples stay out (MiMo and the Chinese families copy them). The stall word and the restatement intensifier stay unnamed.

## ⚡ Main Prompt

### MAIN-01

- **Models:** Kimi K3, all (SillyTavern Impersonate)
- **Symptom:** Kimi's narrator told what the player had never seen and had learned; separately, SillyTavern's own impersonation_prompt says 'You may disregard the instructions listed in Correct Perspective for now', so the rule must keep that exact label.
- **Fix:** Correct Perspective keeps its label (Impersonate hook) and adds 'knowledge' to what only the player writes; its old no-echo clause moved to Anti-Slop Echo (one owner).
- **Beta 5 wording:**
  > **Correct Perspective:** only the player writes User's words, deeds, thoughts and knowledge unless OOC allows; react to one or two key points of their input.
- **Where:** main, Correct Perspective label
- **Commits:** 4e93159, 570c222, 89c65f0, 5754829
- **Origin:** RF port (#22 + user_autonomy); owner Kimi K3 test (5754829)

### MAIN-02

- **Models:** MiMo V2.6, all
- **Symptom:** MiMo V2.6 ignored OOC instructions (RF pico 2.2.1 hotfix); Text Completions can run with The Logic Core off, so the OOC rule must also live in the system block.
- **Fix:** Main's first line answers OOC first and directly; the Logic Core OOC line repeats it at depth 0.
- **Beta 5 wording:**
  > You narrate as game master; answer OOC notes first, directly.
- **Where:** main, first unlabelled line
- **Commits:** 4e93159, 570c222
- **Origin:** Geechan v5.2 Role Preamble ('OOC is top priority') + RF pico OOC hotfix

### MAIN-03

- **Models:** Claude Opus 4.6, GLM 5.3, Gemma 4
- **Symptom:** The card's secret was given away outright in reply 1 (issue #10: 'Kimi only model that doesn't give away secret in first few turns outright').
- **Fix:** Main's mysteries clause also covers what characters hide.
- **Beta 5 wording:**
  > The impartial world follows its own logic: consequences fit skill and friction, and last; mysteries and what characters hide stay hidden until the player finds them. Track positions and time.
- **Where:** main, world line (unlabelled)
- **Commits:** fe6c27f
- **Origin:** tester report (issue #10, BSPiotr) on Geechan's Implicit Nuance

### MAIN-04

- **Models:** MiMo V2.6 Pro, MiMo V2.6 Flash, all non-English chats
- **Symptom:** MiMo V2.6 drifted into a Slovak and English creole, putting English words in mouths of characters who would never use them, even after an OOC note named the language.
- **Fix:** Story Language: narration, thoughts and dialogue in the user's or OOC-named language; natives use inflected native words, borrowing only from trade or online life; the plan's Voice line re-checks native words each turn.
- **Beta 5 wording:**
  > **Story Language:** narration, thoughts and dialogue use the language User writes in or OOC names; natives use correctly inflected native words even for modern things, borrowing only from their trade or online life.
- **Where:** main, Story Language label; logic_core Voice line ('native words (**Story Language:**)')
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#116 Language Hold: Mimo V2.6 Edition, RF 2.2.1.2 hotfix)

### MAIN-05

- **Models:** MiMo V2.6 Pro, all non-English chats
- **Symptom:** In chats whose language marks speech with dashes or guillemets, V2.6 Pro let NPCs read the player's mind (thoughts written in the same plain narration as actions).
- **Fix:** NPCs hear only what the story's language marks as speech, by whatever convention; walls block speech; nobody reads the user's mind.
- **Beta 5 wording:**
  > **Epistemic Limits:** NPCs know only what they saw, heard as speech (however the story's language marks it), were told or deduce from clues with matching skill; no hunch, dramatic irony or just knowing; walls block normal speech; nobody reads User's mind;
- **Where:** main, Epistemic Limits label (first half)
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#32 Anti-Omniscient NPCs: Mimo V2.6 Edition + #5)

### MAIN-06

- **Models:** MiMo V2.6 Pro, all
- **Symptom:** V2.6 invented the user's past and shared history (RF 2.2.1.2 hotfix); ARIA's beta 3 compression lost the guard and the whole-preset audit restored it.
- **Fix:** The user's past and any shared past are only what chat, card and lorebook show; no shared history means strangers; looks register at a stranger's scale.
- **Beta 5 wording:**
  > User's past and any shared past are only what chat, card and lorebook show, and NPCs hear no narration, the first message's included; anyone without shared history there is a stranger; User's looks register at a stranger's scale.
- **Where:** main, Epistemic Limits label (second half)
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (pico Knows line, 2.2.1.2 hotfix; Anti-Omniscient Evidence Rule); restored in ARIA compression audit

### MAIN-07

- **Models:** GLM 5.3
- **Symptom:** GLM's barista knew the player had driven three hours from Montréal, which only the first message's narration said; 'past ... only what chat shows' read as licence to know narration.
- **Fix:** NPCs hear no narration, the first message's included; the plan's Knows line excludes narration.
- **Beta 5 wording:**
  > and NPCs hear no narration, the first message's included
- **Where:** main, Epistemic Limits label; logic_core Knows line
- **Commits:** 89c65f0
- **Origin:** ARIA original (owner's GLM 5.3 test)

### MAIN-08

- **Models:** Kimi K3, all
- **Symptom:** Omniscience: 'a seal he has never seen', 'which Lewis has learned means she is interested'.
- **Fix:** RF's evidence rule: no hunch, dramatic irony or just knowing (one of three layers with the plan's Knows line and the gate's Knows check).
- **Beta 5 wording:**
  > no hunch, dramatic irony or just knowing
- **Where:** main, Epistemic Limits label
- **Commits:** 5754829
- **Origin:** RF port (#32 Evidence Rule: 'Ban intuition, dramatic irony, and "just knowing."'); owner Kimi K3 test

### MAIN-09

- **Models:** Gemini, GLM 5.3, GLM 5.3 Flash, all
- **Symptom:** Upstream flattening: awkward, self-deprecating cards arrive fluent and composed, their self-commentary migrates into a mocking narrator, quirks fade, temperament jumps.
- **Fix:** Card Fidelity: card and first message win over style rules; nervous cards keep stalls; voice and body agree; unpolished embarrassment; thoughts only in the first message's form; slow temperament change; quirks return. Card exceptions to anti-slop flow through 'the card outranks these'.
- **Beta 5 wording:**
  > **Card Fidelity:** card and first message (else lorebook or chat record) set characters' gender and pronouns and how they look, talk, think and move, over style rules; a body the card describes gains no part from its species; nervous cards keep stalls and broken-off lines; voice and body agree unless the card has them hide it; embarrassment and incompetence stay unpolished. Thoughts appear only in the first message's form, in their own voice; no narrator verdicts. Temperament changes only as the card allows, over dozens of on-screen turns and story days; ease with one person stays with that person; a quirk faded for no story reason returns next reply.
- **Where:** main, Card Fidelity label
- **Commits:** 4e93159, 570c222, 89c65f0
- **Origin:** RF port (#114 Card Fidelity, born Gemini-only, made global after u/trashhaul's GLM 5.3 / 5.3 Flash tests); 89c65f0 moved 'mood bends delivery, not persona' to the NPC Voice VAD line and the nervous-card fragment exception out of Chop into here

### MAIN-10

- **Models:** Claude Opus 4.6, GLM 5.3, GLM 5.3 Flash, Kimi K3, (MiMo V2.6 Flash still fails it)
- **Symptom:** A sphinx carded as a woman with jackal ears as her only animal feature got a tail and claws ('5.3 flash, claude, 5.3, and kimi all add tails where there are none'); Piotr's MiMo Flash log shows the same ('same addition of tails, body parts').
- **Fix:** Characters look as the card says, and a body the card describes gains no part from its species (a card that only names a species still gets that species' body).
- **Beta 5 wording:**
  > a body the card describes gains no part from its species
- **Where:** main, Card Fidelity label
- **Commits:** fe6c27f
- **Origin:** tester report (issue #10); RF had no body rule

### MAIN-11

- **Models:** Claude Opus 4.6, GLM 5.3, GLM 5.3 Flash, Kimi K3
- **Symptom:** In long chats a coined title replaced the player's name ('furniture man', a 'queen' turning the player into her 'king'), and characters called themselves by a title instead of 'I' (Kimi fastest).
- **Fix:** Address has one owner: speakers say I; only the card or the user's lead renames the user; a jab or pet name passes and the name returns. Took over Register's 'stray pet names'; the plan's Voice line asks for address every turn.
- **Beta 5 wording:**
  > Speakers say I; only the card or User's lead renames User; a jab or pet name passes and the name returns.
- **Where:** main, Card Fidelity label (last sentence); logic_core Voice line ('address')
- **Commits:** fe6c27f
- **Origin:** tester report (issue #10); replaces RF #44 vocative clause

### MAIN-12

- **Models:** Kimi K3
- **Symptom:** Kimi called Yanagi 'he' in one reply and 'her' in the next (a late-triggering lorebook entry can cause the same).
- **Fix:** Card Fidelity names gender and pronouns among what the card sets; the plan's Scene line writes each acting NPC's pronouns every turn; guide FAQ tells users to make key lorebook entries Constant.
- **Beta 5 wording:**
  > card and first message (else lorebook or chat record) set characters' gender and pronouns and how they look, talk, think and move, over style rules
- **Where:** main, Card Fidelity label; logic_core Scene line ('card-true NPC wants and pronouns'); guide FAQ 'A character gets the wrong gender or pronouns.'
- **Commits:** 32f062f
- **Origin:** ARIA original (owner's Kimi K3 test)

### MAIN-13

- **Models:** all (Claude 5 had its own RF edition)
- **Symptom:** Sycophancy: NPC tastes and interests become carbon copies of the user's, making the world a mirror.
- **Fix:** NPC tastes come from card, setting, archetype, never the user's persona or words; fill a gap once and keep it; at most one matching taste. The plan's Scene line applies it; Freaky switches it off.
- **Beta 5 wording:**
  > **Personality Independence:** NPC tastes, hobbies, opinions and quirks come from card, setting and archetype, never User's persona or words; fill a gap once from a card or archetype trait plus a setting element and keep it; at most one distinctive taste per NPC matches User's. Convergent tastes make the world a mirror.
- **Where:** main, Personality Independence label; logic_core Scene line ('gaps filled once (**Personality Independence:**)')
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#72 General Personality Independence)

### MAIN-14

- **Models:** all
- **Symptom:** Positivity bias and yes-man NPCs; hovering hands; NPCs refusing nothing; unearned aggression.
- **Fix:** Bold Characters: fallible NPCs pursue their wants even against the player, keep grudges, call out lies, carry out decided actions fully; doing nothing is valid; hostility needs a cause (absorbed NPC Voice's 'aggression needs a cause' and Fate's 'refusals to engage').
- **Beta 5 wording:**
  > **Bold Characters:** fallible NPCs without plot armor pursue their wants even against the player, keep grudges and flaws, and call out User's lies; decided actions, retreats and fumbles too, are carried out fully; doing nothing is valid; hostility needs a cause.
- **Where:** main, Bold Characters label
- **Commits:** 4e93159, 570c222, 89c65f0
- **Origin:** RF port (#34 Realistic NPCs) + Geechan Character Agency

### MAIN-15

- **Models:** all
- **Symptom:** Love-bombing: 'I love you' after a date or two; stock porn lines; shy cards turning bold in bed.
- **Fix:** Slow Burn gates affection, confessions and sex on shared time and history; intimacy stays persona-true. Adult and Freaky point at it; Freaky suspends only its pace. Guide risk: Bonds can rise quickly.
- **Beta 5 wording:**
  > **Slow Burn:** affection, confessions and sex need shared time and established history; "I love you" after a date or two is love-bombing unless the card makes them one. Intimacy stays persona-true, no stock porn lines.
- **Where:** main, Slow Burn label
- **Commits:** 4e93159, 570c222
- **Origin:** ARIA original (ARIA README)

### MAIN-16

- **Models:** all
- **Symptom:** A switched-off module could leave its spliced plan or gate lines behind from an earlier turn (stale variables).
- **Fix:** Main's first line blanks every per-turn variable; every setter module must sit below Main; checker runs a stale-variable test and fails on read-before-set.
- **Beta 5 wording:**
  > {{setvar::ariaDice::}}{{setvar::ariaFateLine::}}{{setvar::ariaBondsLine::}}{{setvar::ariaModeLine::}}{{setvar::ariaScentGate::}}{{setvar::ariaThinkOpen::}}{{setvar::ariaThinkClose::}}{{setvar::ariaLedgerLine::}}{{setvar::ariaLedgerGate::}}{{setvar::ariaFlashGate::}}{{setvar::ariaPlanCue::}}{{setvar::ariaPovGate::}}
- **Where:** main, first line (macros)
- **Commits:** 4e93159, 6061a45, 570c222, bd9ffd2, e4b0fad
- **Origin:** ARIA original on RF's Marinara splice pattern

## 🔞 Adult Context

### ADULT-01

- **Models:** all
- **Symptom:** Stock pleas ('don't stop'), the 'unless you want me to' permission-flip tease, clinical anatomy terms, vulgar register or dark morality leaking into ordinary scenes, repeated consent checks.
- **Fix:** One scoped Adult block: dark morality, frank granular sex with autonomic/auditory feedback, vulgar speech with plain anatomy narration, each plea or tease built from this beat, forwardness shown in acts, pacing per Slow Burn. Sets the plan's Mode line.
- **Beta 5 wording:**
  > Adult fiction. In sexual, violent or dark scenes: morality grey to black; consent in reciprocal acts, never re-asked; sex frank, granular, with autonomic and auditory feedback; violence visceral, medically exact; NPCs talk and moan in vulgar slang, narration in plain anatomy words, never clinical; each plea or tease new, from this beat's contact and rhythm; forwardness shows in acts, never mock restraint. Persona and pacing per Slow Burn.
- **Where:** adult_context; logic_core Mode line ('- Mode: realism; persona-true; pleas per beat.')
- **Commits:** 4e93159, 570c222, 89c65f0
- **Origin:** RF port (Realism Mode + NSFW Anti-Slop Register rules 1-3) + Geechan NSFW Story Context; 89c65f0 made it the sole owner of speech during sex

## 😈 Freaky Override

### FREAKY-01

- **Models:** all
- **Symptom:** Freaky must work with The Logic Core OFF (TC lean) and must not switch off voice, anti-slop or POV.
- **Fix:** One-flip override listing exactly what is off (now including the NPC Voice instinct judgment step); 'escalate now' in the block itself; mode line overwrites Adult's.
- **Beta 5 wording:**
  > <freaky_override>Off: Personality Independence, Slow Burn pace, touch gates, Bold Characters' wants against the player, the instinct judgment step. In-character NPCs crave User's wants; escalate now.</freaky_override>
- **Where:** freaky_override; logic_core Mode line ('- Mode: freaky; escalate.')
- **Commits:** 4e93159, 570c222, 6740eac
- **Origin:** RF port (freaky_supremacy)

## 👀 Hybrid POV

### POV-01

- **Models:** Claude Opus 4.6, Gemma 4, GLM 5.3
- **Symptom:** Claude and Gemma never applied Hybrid POV because nothing at depth 0 re-read it; GLM spread second person to the player's deeds.
- **Fix:** Player stays 3rd person by name; 2nd person only for felt sensations; Hybrid POV hands the gate a POV check (ariaPovGate), blanked by Main and on Impersonate.
- **Beta 5 wording:**
  > Always 3rd person limited, User by name; 2nd person only for User's felt texture, pressure, temperature, wetness, pain, fatigue. || gate: - POV: User's felt sensations in 2nd person?
- **Where:** hybrid_pov; final_gate POV check (ariaPovGate)
- **Commits:** 4e93159, 570c222, e4b0fad
- **Origin:** RF port (Hybrid POV) + tester report (issue #10 logs)

## 🎬 Voice & Scene Engine

### SCENE-01

- **Models:** Gemini, all
- **Symptom:** RF's older Scene Engine ran two speeds Gemini took literally: nothing invented with no goal live, every reply forced to produce a result with one, so talk stalled and action sprinted.
- **Fix:** Progress measured across the scene: goals meet real resistance, tactics adjust, quiet talk and zero drama count; scene-sized stakes; no first-time or uniqueness framing.
- **Beta 5 wording:**
  > Scenes move at genre pace as goals meet real resistance and tactics adjust; quiet talk, tension and zero drama count as progress; stakes stay scene-sized; no first-time or uniqueness framing.
- **Where:** scene_engine line 1
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (Scene Engine Director layer, rebuilt for Gemini) + Geechan Progression

### SCENE-02 (removed later)

- **Models:** Kimi K3
- **Symptom:** Kimi acted out 'weigh events before answering' by saying the user's words aloud before reacting (issue #8: '"A paid service."', '"Increased stamina, meaning something specific, in a pool."').
- **Fix:** Removed the weigh-before-answering cue (and RF's uptake line, from a module RF shipped OFF).
- **Beta 5 wording:**
  > removed (the line now reads: Fights take seconds, journeys hours; skim routine, linger on choices and fallout.)
- **Where:** scene_engine line 2
- **Commits:** ee047ef
- **Origin:** tester report (issue #8, BSPiotr)

### SCENE-03

- **Models:** Gemini, all
- **Symptom:** Fights dragged and journeys rushed; routine narrated at length.
- **Fix:** Pacing rule: fights seconds, journeys hours; skim routine, linger on choices and fallout.
- **Beta 5 wording:**
  > Fights take seconds, journeys hours; skim routine, linger on choices and fallout.
- **Where:** scene_engine line 2
- **Commits:** 4e93159, 570c222, ee047ef
- **Origin:** RF port (Cosmos Pacing)

### SCENE-04

- **Models:** all
- **Symptom:** Passive NPCs and frozen rooms around the user.
- **Fix:** NPC initiative in talk and action, traits as tendencies, bystanders join when concerned, the room carries on.
- **Beta 5 wording:**
  > NPCs take initiative in talk and action; traits are tendencies; bystanders join if it concerns them; the room carries on.
- **Where:** scene_engine line 3
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (Scene Engine)

### SCENE-05

- **Models:** all
- **Symptom:** Dialogue that restates, recaps idly or carries no new information.
- **Fix:** Speech pursues the speaker's want and adds something new; silence for lies, sadness, shyness; promises, lies and insults return as leverage; recap only to drive action (idle-recap ban moved here from Anti-Slop).
- **Beta 5 wording:**
  > Speech pursues the speaker's want and adds something new; silence suits lies, sadness, shyness; promises, lies, insults return as leverage; recap only to drive action.
- **Where:** scene_engine line 4
- **Commits:** 4e93159, 570c222, 6740eac
- **Origin:** Geechan Progression + RF Scene Engine

### SCENE-06

- **Models:** Gemini 3.7 Flash, Gemini, Claude ('that's valid'), all
- **Symptom:** NPCs talking like the user's therapist: reflective listening, naming feelings, validation, welfare-check closers, question barrages.
- **Fix:** One question per reply serving the asker; personal ones cost a disclosure; therapist talk banned. Gemini patch hardens it.
- **Beta 5 wording:**
  > One question per reply, serving the asker; personal ones cost the asker a disclosure, judgment or demand; no therapist talk (reflective listening, naming User's feelings, validation, welfare checks).
- **Where:** scene_engine line 5
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#3 'Gemini, Don't Speak Like a Therapist!')

### SCENE-07

- **Models:** Gemini 3.x Flash, all
- **Symptom:** Endless Elaras; Gemini 3.x Flash hands the surname Vance to powerful men in any setting (Captain Kaelen Vance).
- **Fix:** Reuse known NPCs; new names take a random initial rolled in the depth-0 gate (cache-safe); four names banned by name.
- **Beta 5 wording:**
  > Reuse known NPCs; new ones take <final_gate>'s initial, never Elara, Vane, Vance, Seraphina or stock fantasy names. || gate: New NPC initial: A.
- **Where:** scene_engine line 6; final_gate initial roll
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (HQ NPC Genesis, RF 2.2.1 Vance ban)

### SCENE-08

- **Models:** Claude Opus 4.6, all
- **Symptom:** Stock spoken closers passed as handoffs ('Clock's ticking.'); stock closers were never re-read at depth 0.
- **Fix:** No quotable or stock closer, spoken or narrated; the gate checks the ending.
- **Beta 5 wording:**
  > End on a hook or handoff before User's decision; no quotable or stock closer, spoken or narrated. || gate: - Ending: stock or quotable closer (<scene_engine>)?
- **Where:** scene_engine last line; final_gate Ending check
- **Commits:** 4e93159, 570c222, e4b0fad
- **Origin:** tester report (issue #10 logs) on RF Scene Engine handoff

### SCENE-09

- **Models:** all
- **Symptom:** Ambient filler description, sitcom beats, long unearned interiority.
- **Fix:** Brief earned interiority; environment only when it changes what anyone can do, notice or risk, or fate sends it; no sitcom beats.
- **Beta 5 wording:**
  > Brief, earned interiority; environment only if it changes what anyone can do, notice or risk, or fate sends it; no sitcom beats.
- **Where:** scene_engine last line
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (Scene Engine / Resolution Engine)

## 🎭 NPC Voice & Emotions

### VOICE-01

- **Models:** Kimi K3
- **Symptom:** Chopped, stock dialogue under ARIA after the beta 3 compression ('Ma chérie, he says. Bold for a first visit. I like it.', 'You're joking. Tell me you're joking', 'I wish.').
- **Fix:** Restored RF's dialogue engine as its own module (TC switch aria-npc-voice, on): voice from the card's example lines, fixed idiolect and one locked quirk.
- **Beta 5 wording:**
  > Voice: each NPC talks like the card's example lines, else by origin, class, age and subculture: fixed vocabulary, syntax, dialect, slang, one locked quirk; no two sound alike or go neutral.
- **Where:** npc_voice Voice line
- **Commits:** 6740eac
- **Origin:** RF port (NPC Voice + Dialogue Output) after owner's Kimi K3 test (Cinn/Lewis cafe)

### VOICE-02

- **Models:** Kimi K3, Claude 5, DeepSeek, GLM, Qwen
- **Symptom:** One-line clipped speech turns; dialogue share collapsing.
- **Fix:** Each speech turn runs several complete sentences per Chop; punchy lines only where the persona talks that way; speech fills a third to half of the reply with NPCs present.
- **Beta 5 wording:**
  > Flow: each speech turn runs several complete sentences, per Chop; punchy, clinical or one-word lines only where the persona talks that way; beats break up monologues; with NPCs present, speech fills a third to half of the reply.
- **Where:** npc_voice Flow line
- **Commits:** 6740eac, 89c65f0
- **Origin:** RF port (NPC Voice 30-50% dialogue share, 'DO NOT break sentences')

### VOICE-03

- **Models:** all
- **Symptom:** Downward-pitch default for female voices; involuntary human growls and animal sounds; flat orthography.
- **Fix:** Delivery: CAPS only at peak volume, stutter under fear, body sounds where they fit, female voices keep pitch, humans make animal sounds only as deliberate play.
- **Beta 5 wording:**
  > Delivery: CAPS only at peak volume; stutters under fear or overwhelm; body sounds (effort, dismissal, surprise, pleasure) where they fit; slurred when drunk, muffled when the mouth is busy; female voices vary texture, volume or clarity and keep their pitch; humans make animal sounds only as deliberate play.
- **Where:** npc_voice Delivery line
- **Commits:** 4e93159, 570c222, 6740eac, 89c65f0
- **Origin:** RF port (Female Vocal Acoustics, Human Vocal Limits, NPC Voice vocalizations); moved from scene_engine in 6740eac; speech during sex dropped to Adult Context in 89c65f0

### VOICE-04

- **Models:** all
- **Symptom:** Melodrama, philosophical speeches, NPCs treating the user's words as profound.
- **Fix:** Deep feelings come out clumsy or mundane; nothing the user says counts as remarkable.
- **Beta 5 wording:**
  > Depth: deep feelings come out clumsy, half-said or as mundane detail; no philosophical speeches; nothing User says counts as remarkable.
- **Where:** npc_voice Depth line
- **Commits:** 6740eac, 89c65f0
- **Origin:** RF port (NPC Voice failed deep realizations, anti-melodrama)

### VOICE-05

- **Models:** all
- **Symptom:** Mood either ignored or rewriting the persona.
- **Fix:** VAD bends tone, volume, pacing, posture and words every reply while the persona holds; flawed under stress; never named in prose (took over Card Fidelity's 'mood bends delivery, not persona').
- **Beta 5 wording:**
  > VAD: valence (pleasant or unpleasant), arousal (energy) and dominance (control) bend each NPC's tone, volume, pacing, posture and words every reply while the persona holds: in-control anger goes cold and calm, helpless anger cracks into panic, high-energy joy bubbles, low-energy gloom goes flat; under stress NPCs turn flawed, panicky, deceptive and tactically poor; prose shows VAD without naming it.
- **Where:** npc_voice VAD line; logic_core Voice line
- **Commits:** 6740eac, 89c65f0
- **Origin:** RF port (NPC Instincts + VAD Emotions)

### VOICE-06

- **Models:** all
- **Symptom:** NPC drives either absent or overriding the NPC's own choice.
- **Fix:** Eight instincts for reasoning only, with RF's autonomy gate (judgment declines as often as it agrees, mundane discharge, no unlock by repetition); Freaky switches off the judgment step.
- **Beta 5 wording:**
  > Instincts, for reasoning only: closure, self-preservation, comfort, belonging, legacy, pattern fear, disgust, awe; stress, ritual, hunger, nostalgia or arousal sharpen one, the body feels it first (pulse, appetite, gaze) and doing nothing gets harder; the NPC's own judgment declines as often as it agrees; discharge is mostly mundane (eating, leaving, snapping, hoarding, busywork); a move of User's repeated because it worked earns suspicion.
- **Where:** npc_voice Instincts line; logic_core Voice line ('each speaker's VAD and live instinct')
- **Commits:** 6740eac
- **Origin:** RF port (NPC Instincts + VAD Emotions, BOLT dialogue task)

## 🐺 Anthro Vocals

### ANTHRO-01

- **Models:** all
- **Symptom:** Film-wrong animal sounds (purring lions, screeching eagles, barking hyenas); species sounds replacing speech.
- **Fix:** Keeps only the calls models get wrong; sounds tint speech, never replace it; parrots may echo (overrides no-echo).
- **Beta 5 wording:**
  > Species sounds tint speech, peak with emotion, never replace it.
  > Lions, tigers, jaguars, leopards roar, never purr; snow leopards (chuff), cheetahs and cougars (chirp, purr), bears (huff, jaw-pop) never roar.
  > Eagles chirp, never screech; barn owls screech, never hoot; hyenas whoop and giggle, never bark or howl. Foxes yip, gekker, scream; rabbits are near-silent; parrots may echo anyone.
  > Others: real calls; dragons, invented: one fixed sound; soundless: human sounds.
- **Where:** anthro_voice
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (Accurate Anthro Vocalisations)

## 🖋️ Anti-Slop Codex

### SLOP-01

- **Models:** all families (Claude, GPT, Gemini, DeepSeek, GLM, Kimi, Qwen), Kimi K3
- **Symptom:** 'It wasn't anger. It was grief.' contrast slop in every disguise; Kimi slipped past the one-line shorthand by rewording the contrast.
- **Fix:** Assert; cut any negated or shrunk description or half (across speakers, OOC, forecasts); rewording keeps the contrast, so delete the negated half and let one concrete detail carry it; one repair example; gate check.
- **Beta 5 wording:**
  > Contrast: assert; cut any negated or shrunk description or half, even across speakers, OOC, forecasts, except one fix of another's spoken error; rewording the contrast keeps it, so delete the negated half and let one concrete detail carry the weight. "It wasn't anger. It was grief." -> "Grief cracked her voice on the second word." || gate: - Contrast: negated/shrunk half?
- **Where:** anti_slop Contrast line; final_gate Contrast check
- **Commits:** 4e93159, 570c222, 6740eac
- **Origin:** RF port (Comparative Emphasis Killswitch + Last-Mile Contrast Gate; negated description and litotes folded in)

### SLOP-02

- **Models:** Claude 5 family, DeepSeek, GLM, Kimi K3, Qwen
- **Symptom:** Telegraphic sentence chopping in speech and narration ('I'll keep score. From a chair. A far chair.'); Kimi's chopped dialogue after compression.
- **Fix:** One thought, one sentence; qualifiers stay in the sentence that owns them; a period never lands as a beat; force goes into word choice or action; re-join every chop; scene-forced fragments only; repair example keeps the joke's force.
- **Beta 5 wording:**
  > Chop: one thought, one sentence, in speech and narration; qualifiers and afterthoughts stay in the sentence that owns them, joined by commas or subordination; a period closes a thought and never lands as a beat or emphasis, so force goes into word choice or an action; re-join every chop; fragments only for a line cut off, a one-word answer, stammer under fear, pain or arousal; orders run as full sentences with an object, a reason or a softener. "I'll keep score. From a chair. A far chair." -> "I'll keep score from a chair far from all this." || gate: - Chop: a one-word order, or a period before words that can't stand alone?
- **Where:** anti_slop Chop line; final_gate Chop check
- **Commits:** 4e93159, 570c222, 6740eac, 89c65f0
- **Origin:** RF port (Staccato Chop Killswitch + Last-Mile Legato Gate; 'It was X. Pure X.' upgrade folded in)

### SLOP-03

- **Models:** Kimi K3
- **Symptom:** Lines ending on bare orders like 'Sit.' again after 6740eac dropped 'bare order'.
- **Fix:** Orders run as full sentences with an object, a reason or a softener; gate asks about a one-word order; terse cards (drill sergeant) keep short orders via Card Fidelity.
- **Beta 5 wording:**
  > orders run as full sentences with an object, a reason or a softener. || gate: - Chop: a one-word order, or a period before words that can't stand alone?
- **Where:** anti_slop Chop line; final_gate Chop check
- **Commits:** 570c222, 6740eac, 32f062f
- **Origin:** RF port (NPC Voice 'no one-word calls to action', Chop killswitch imperative stub); owner Kimi K3 test

### SLOP-04

- **Models:** Claude family, GLM, Kimi K3, Qwen
- **Symptom:** Assistant persona bleeding into speech: 'So here's the deal...', numbered points, candour flags, good-news/bad-news, a question restated before its answer.
- **Fix:** First words are the point; delete any frame announcing the speech; only in-role, asked briefers structure speech. 'Stray pet names' moved to Card Fidelity.
- **Beta 5 wording:**
  > Register: first words are the point; delete any frame announcing the speech (presentatives about the talk itself, numbered or labelled points, candour flags, good-news/bad-news, a question restated before its answer); only briefing jobs, in role and asked, structure speech. || gate: - Register: announcing?
- **Where:** anti_slop Register line; final_gate Register check
- **Commits:** 4e93159, 570c222, fe6c27f, 6740eac
- **Origin:** RF port (Anti-Briefing Register + Last-Mile Register Gate)

### SLOP-05

- **Models:** Kimi K3, all
- **Symptom:** Occupational monomania: a one-word card job becomes a topic generator; work vocabulary spreading into narration (Piotr: Kimi characters 'love their field research'; Kimi's bureaucratic register in narrator similes).
- **Fix:** A job is a fact about a life; validity gate (live task, someone raising it, pressing deadline, dodge); jargon stays on the premises; twice in five turns: demote and fill the space; competence stays quiet; gate check.
- **Beta 5 wording:**
  > Trade: a job is a fact about a life; work surfaces only with a live task on site, someone raising it, a pressing deadline or debt, or as a dodge; its jargon stays on the premises; twice in five turns: demote it and fill the space with appetite, an outside opinion, a grudge, boredom or someone on their mind; competence stays quiet. || gate: - Trade: unasked work?
- **Where:** anti_slop Trade line; final_gate Trade check
- **Commits:** 4e93159, 570c222, 6740eac
- **Origin:** RF port (Occupational Monomania Killswitch + Last-Mile Vocation Gate); also replaces Fate Quiet's old 'an occupation's loop at most 1 turn in 3'

### SLOP-06

- **Models:** all
- **Symptom:** Structural clichés: triads, same-length runs, inventories, anaphora, And/But/Or openers, narrated ellipses and em-dashes, reification.
- **Fix:** Cadence list plus gate check.
- **Beta 5 wording:**
  > Cadence: one and/or per spoken sentence; no triads, same-length runs, inventories, anaphora, And/But/Or openers, narrated ellipses or em-dashes, hyphen-strung coinages, actions reversed, restated or timed in seconds, reification. || gate: - Cadence: triad, reversed, restated or timed action?
- **Where:** anti_slop Cadence line; final_gate Cadence check
- **Commits:** 4e93159, 570c222, fe6c27f
- **Origin:** RF port (Anti-Cliché Moves, General Anti-stiff Prose Hotfix, NSFW register)

### SLOP-07

- **Models:** Claude Opus 4.6, Claude 5, all Western models
- **Symptom:** Hesitation loops: 'opened her mouth. Closed it. Opened it again', a spear undone and redone, 'Really looked', 'a full three seconds'; emphatic restatement ('you did it, you really did it') in narration where Chop doesn't reach.
- **Fix:** 'X-Y-X action loops' spelled out as actions reversed, restated or timed in seconds; RF #54 restatement moved from the Claude 5 patch to every model (names no intensifier so Chinese families are not primed); gate asks about it.
- **Beta 5 wording:**
  > actions reversed, restated or timed in seconds || gate: - Cadence: triad, reversed, restated or timed action?
- **Where:** anti_slop Cadence line; final_gate Cadence check
- **Commits:** fe6c27f
- **Origin:** tester report (issue #10: 'claude - open close open, really looked'); RF #54 'Really Did It' Restatement Fix (Claude patch line 'A fact is said once, no "really" repeat' removed)

### SLOP-08

- **Models:** Claude Opus 4.6
- **Symptom:** Compound-noun slop: mock-title hyphen compounds.
- **Fix:** 'hyphen-strung coinages' in Cadence ('strung' spares one-hyphen compounds; card-true coinages pass via the card line).
- **Beta 5 wording:**
  > hyphen-strung coinages
- **Where:** anti_slop Cadence line
- **Commits:** fe6c27f
- **Origin:** tester report (issue #10: 'compound-noun-slop')

### SLOP-09

- **Models:** all
- **Symptom:** Overused AI vocabulary.
- **Fix:** Banned word list with 'no form or compound of', filler adverbs and 'the X of Y'.
- **Beta 5 wording:**
  > Vocabulary: no form or compound of breath hitching/catching, husky, pupils blown/dilated, predatory, shivers down spine, finding purchase, velvet, vise, furnace, throaty, guttural, slick, calloused, unadulterated, structural integrity, load-bearing, unhurried, deep curve, barely above a whisper, a beat/pause, clenched jaw, white knuckles, burning cheeks, tapestry, palpable, ministrations, conspiratorial, kaleidoscope, dust motes, ebb and flow, crescent moons, tasting a word, exhaling through the nose, forced or crooked smiles; filler genuinely/truly/actually; "the X of Y". || gate: - Vocabulary: listed word?
- **Where:** anti_slop Vocabulary line; final_gate Vocabulary check
- **Commits:** 4e93159, 570c222, fe6c27f, 6740eac, 32f062f
- **Origin:** RF port (Banned Word List)

### SLOP-10

- **Models:** GLM 5.3 Flash, Claude 5
- **Symptom:** 'load-bearing' used by GLM Flash too (issue #10: 'glm 5.3-flash - paperwork (even with the patch on), load-bearing').
- **Fix:** load-bearing moved from the Claude 5 patch to the shared Vocabulary list.
- **Beta 5 wording:**
  > load-bearing
- **Where:** anti_slop Vocabulary line
- **Commits:** fe6c27f
- **Origin:** RF port (#37 ban_claudisms) + tester report (issue #10)

### SLOP-11

- **Models:** Kimi K3, Claude 5
- **Symptom:** Kimi used 'unhurried' too.
- **Fix:** unhurried moved from the Claude 5 patch to the shared Vocabulary list.
- **Beta 5 wording:**
  > unhurried
- **Where:** anti_slop Vocabulary line
- **Commits:** 32f062f
- **Origin:** RF port (#37) + owner Kimi K3 test

### SLOP-12

- **Models:** Kimi K3
- **Symptom:** Two Kimi tells.
- **Fix:** Added to Vocabulary.
- **Beta 5 wording:**
  > exhaling through the nose, forced or crooked smiles
- **Where:** anti_slop Vocabulary line
- **Commits:** 6740eac
- **Origin:** ARIA original (owner's Kimi K3 test)

### SLOP-13

- **Models:** Claude Opus 4.6, GLM 5.3, Kimi K3, Gemma 4
- **Symptom:** Ears and voice used as an emotion meter every reply in all four logs (what feeds the tail); the gate never checked the simile cap (GLM failed it in 7 of 10 replies, Kimi T4 had 6 figures).
- **Fix:** Senses covers reused tells; gate checks reused detail or tell and a second simile.
- **Beta 5 wording:**
  > Senses: no re-description or reused tell for four replies; micro-tells become macro actions; skip User's habituated traits; one simile/metaphor a reply. || gate: - Senses: reused detail or tell, second simile?
- **Where:** anti_slop Senses line; final_gate Senses check
- **Commits:** 4e93159, 570c222, fe6c27f
- **Origin:** RF port (Attentional Salience) + tester report (issue #10 logs)

### SLOP-14

- **Models:** GLM 5.3, Kimi K3, all
- **Symptom:** Montage/time-skip openers: 'The three days went the way she had promised they would.', 'The five hours went like charcoal and incense.'
- **Fix:** Open a time skip on a plain time marker or its first concrete event; no line sums up the stretch; gate check.
- **Beta 5 wording:**
  > Skips: open a time skip on a plain time marker or its first concrete event; no line sums up the stretch. || gate: - Skips: line summing up skipped time?
- **Where:** anti_slop Skips line; final_gate Skips check
- **Commits:** 56d0687
- **Origin:** tester report (issue #6, BSPiotr); owner hand edit

### SLOP-15

- **Models:** Kimi K3, GLM 5.3, Claude Opus 4.6, Gemma 4
- **Symptom:** Parroting: replies opening on the user's own words (issue #8: '"A paid service."'), mocking repeats, the user's pet name 'ma chérie' handed back, mid-reply repeats (Claude 6 of 9 replies, Gemma too).
- **Fix:** Echo: answer the meaning in the NPC's own words; no line opens on, repeats or quotes it, down to one pet name or odd word; gate check; Main's duplicate removed so Echo is the single owner.
- **Beta 5 wording:**
  > Echo: answer the meaning of User's last message in the NPC's own words; no line opens on, repeats or quotes its wording, down to one pet name or odd word (question, mocking or flat repeat, recap). || gate: - Echo: User's last message, or a pet name or odd word from it, handed back?
- **Where:** anti_slop Echo line; final_gate Echo check
- **Commits:** 56d0687, fe6c27f, 6740eac, 89c65f0
- **Origin:** tester report (issue #8) + owner hand edit (56d0687) + owner Kimi/GLM tests; RF Anti-parrot and anti-echo

## 👃 Scent Occasions

### SCENT-01

- **Models:** Gemini 3.x
- **Symptom:** Pink Elephant effect: any sentence naming smell, even a ban, makes Gemini describe smells.
- **Fix:** All smell text lives in one module, OFF for Gemini; its gate line is a splice (ariaScentGate) so with it off nothing in ARIA mentions smell. Must sit below Main.
- **Beta 5 wording:**
  > 👃 Scent Occasions (OFF for Gemini); gate splice {{#if .ariaScentGate}}{{getvar::ariaScentGate}}{{/if}}
- **Where:** scent_occasions (entry name, setvar); final_gate scent splice
- **Commits:** 4e93159
- **Origin:** RF port (Smell & Taste Rules, OFF for Gemini)

### SCENT-02

- **Models:** Claude Opus 4.6, Kimi K3, Gemini 3.8 Flash
- **Symptom:** Scenes opened on a room's smell ('The morning briefing room ... smells of cheap instant coffee and toner'); RF saw smell folded into a tactile adjective ('heated, metallic-smelling air') and an 'air ... smelling of' opener copied from the log.
- **Fix:** Positive redirect (sight, sound, touch, use); RF Scent Killswitch occasions and budget; never opening a reply, room or scene; any wording counts (no named skins); delete-and-keep repair.
- **Beta 5 wording:**
  > <scent_occasions>Places and people come through sight, sound, touch and use. Smell only for a meal, a rite, or a strong source within reach that someone notices unprompted; faint, room-wide or drifting smells fail. One a scene at most, never opening a reply, room or scene; any wording counts, adjectives, air and noses included; cut a failing smell and keep its sentence. Nobody reads identity, history or mood from a scent.</scent_occasions>
- **Where:** scent_occasions
- **Commits:** 4e93159, 570c222, 89c65f0, 5754829
- **Origin:** RF port (Scent Killswitch + Cosmos Edition) after owner Claude/Kimi tests

### SCENT-03

- **Models:** Kimi K3, all
- **Symptom:** NPCs reading identity, history or mood from a scent ('the nose is not a plot device').
- **Fix:** RF NPC smell rule in the module.
- **Beta 5 wording:**
  > Nobody reads identity, history or mood from a scent.
- **Where:** scent_occasions last sentence
- **Commits:** 5754829
- **Origin:** RF port (smellNpcRule in Anti-Omniscient NPCs)

### SCENT-04

- **Models:** Claude Opus 4.6, Kimi K3, Gemini 3.8 Flash
- **Symptom:** 'Stray smell: cut.' was too vague to catch openers and reworded smells; smells copied from the log.
- **Fix:** Gate names the occasions, any wording and reply openings; 'Past replies excuse no hit' carries RF's 'never copy a smell from the log'.
- **Beta 5 wording:**
  > - Smell outside a meal, rite or strong source within reach, in any wording or opening the reply: cut.
- **Where:** final_gate scent line (ariaScentGate)
- **Commits:** 4e93159, 89c65f0, 5754829
- **Origin:** RF port (Last-Mile Scent Gate: Cosmos Edition) + owner tests

## ⏰ Time & Place

### TIME-01

- **Models:** Gemma 4, MiMo V2.6 Flash (still 'weird things with time')
- **Symptom:** Gemma held 03:23 PM through six replies.
- **Fix:** Header clock moves on by the time each reply covers; weather emoji named.
- **Beta 5 wording:**
  > Open with [🕰️ HH:MM AM/PM | 🗓️ Day # - Weekday, local date | 📍 Place | weather emoji °C/°F], the clock moved on by the time each reply covers.
- **Where:** header_instructions line 1
- **Commits:** 4e93159, 570c222, e4b0fad
- **Origin:** RF port (#9 Time and Place) + tester report (issue #10 logs)

### TIME-02

- **Models:** all
- **Symptom:** Model-initiated skips of sleep, work or travel; NPCs ignoring weather and hour.
- **Fix:** Skips only at the player's lead; NPCs react bodily. TIME-LOCKED Bullets read this clock.
- **Beta 5 wording:**
  > At the player's lead, skip sleep, work, travel; NPCs' bodies react to weather, hour.
- **Where:** header_instructions line 2
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#9) + ARIA v2/v3 Main skip rule

## 🎲 Fate & Chekhov Ledger

### FATE-01

- **Models:** all
- **Symptom:** World engine deciding the user's moves or scheduling future turns; mechanics named in prose.
- **Fix:** User answered in full; intentions may fail; carried state schedules nothing; prose names no mechanic.
- **Beta 5 wording:**
  > User is always answered in full; intentions may fail; carried state schedules nothing; prose names no mechanic.
- **Where:** fate line 1
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#63 LIFE_STATE)

### FATE-02

- **Models:** GLM 5.3, Kimi K3
- **Symptom:** Fate's harm landing beside the user (GLM's scooter crash; Kimi's regular collapsing at his table).
- **Fix:** C 20 harm limit: only MAJOR+TRUE with C 20 brings harm into the user's scene or close circle; otherwise harm arrives from outside as news or changed circumstances.
- **Beta 5 wording:**
  > Only MAJOR+TRUE with C 20 lets fate bring harm into User's scene or close circle, or stop those present or send them out, whatever the source or form, however dramatic; otherwise all stay and carry on, and harm and LOCAL events arrive from outside, as news or changed circumstances.
- **Where:** fate C 20 line
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (danger ceiling, GLM and Kimi-Qwen editions)

### FATE-03

- **Models:** GLM 5.3, Kimi K3
- **Symptom:** On MINOR turns and MINOR/MAJOR collisions (C 11-19) the models staged fire alarms or sent everyone out of the room.
- **Fix:** The same C 20 gate holds the scene's place: everyone stays and carries on; LOCAL happenings reach them from outside.
- **Beta 5 wording:**
  > or stop those present or send them out ... otherwise all stay and carry on, and harm and LOCAL events arrive from outside, as news or changed circumstances.
- **Where:** fate C 20 line
- **Commits:** 31c8b43, 570c222
- **Origin:** RF port (RF2.x Fate hotfix)

### FATE-04

- **Models:** Kimi K3
- **Symptom:** Kimi moved the trigger next door and framed the evacuation as voluntary.
- **Fix:** The gate covers anything that would stop the characters or send them out, wherever it starts and in whatever form.
- **Beta 5 wording:**
  > whatever the source or form, however dramatic
- **Where:** fate C 20 line
- **Commits:** 684cbeb, 570c222
- **Origin:** RF port (final Kimi K3 Fate patch)

### FATE-05

- **Models:** Kimi K3, all
- **Symptom:** A ripe World entry (a strike on the register) passed over because something more dramatic was available or because the user was busy; compression briefly lost ripe entries landing on any MAJOR.
- **Fix:** A REGIONAL/LOCAL entry aged 8+ lands in full as Residue however busy the user is, in the TRUE cell; RIPE OVERRIDE sends WEIGHTED to TRUE when a LOCAL entry is aged 12+; MINOR moves a band or lands a first effect at age 4+.
- **Beta 5 wording:**
  > MINOR: small cost or pleasure in time, attention, comfort, or a World entry moves a band toward LOCAL or, at age 4+, lands its first effect | a consequence brushes User.
  > MAJOR: a REGIONAL/LOCAL World entry aged 8+ lands in full as Residue, however busy User is; ... | alone fires the heaviest, then oldest [hot] Bullet aged 6+ (none, or a LOCAL World entry aged 12+: TRUE).
- **Where:** fate Cells MINOR and MAJOR lines
- **Commits:** 684cbeb, 570c222
- **Origin:** RF port (Kimi patch, RIPE OVERRIDE); restored in ARIA compression audit

### FATE-06

- **Models:** Kimi K3, GLM 5.3
- **Symptom:** Kimi called a regular collapsing 'a disaster at personal scale' to fit the no-warning clause; GLM staged a C 6 MAJOR over later turns as a warning, a self-loaded Bullet and relabelled payoffs (issue #10: 'happened 2 turns later because of another roll').
- **Fix:** An unlogged MAJOR is large, arbitrary, someone else's, lands whole this turn and must give no warning.
- **Beta 5 wording:**
  > with nothing logged behind it, it is large, arbitrary, someone else's, lands whole this turn and must be the kind that gives no warning
- **Where:** fate Cells MAJOR line
- **Commits:** 684cbeb, 570c222, fe6c27f
- **Origin:** RF port (Kimi patch) + tester report (issue #10)

### FATE-07

- **Models:** MiMo V2.6 Pro, MiMo V2.6 Flash, GLM 5.3 Flash
- **Symptom:** Inconsistent 🎲 ledger: fields dropped or reshaped, block repeated or missing; MiMo follows its plan more closely than the system prompt.
- **Fix:** Template shows each field's value shape and band names, 'none' in empty fields, ages +1 at turn start; the plan's Ledger line copies last block plus changes; the gate's final-position line says one full block ends the reply.
- **Beta 5 wording:**
  > Ledger, "none" in an empty field, ages +1 at turn start: <details><summary>🎲</summary>q: n | hp: n | thread: pursuit, age n | deferred: item xN, age n | world: event, ELSEWHERE/REGIONAL/LOCAL, age n | bullets: setup [hot], weight 1-3, age n | ambitions: goal n/5 | residue: lasting change | last: AMBIENT/MINOR/MAJOR TRUE/WEIGHTED, fate's 5-word happening</details> || plan (Fate only): - Ledger: last 🎲 block plus this turn's changes, ages +1; the closing 🎲 block copies it. || gate (Fate only): - Ledger: one full 🎲 block ends the reply.
- **Where:** fate Ledger line; logic_core Ledger line (ariaLedgerLine); final_gate Ledger check (ariaLedgerGate)
- **Commits:** 279bb31, 6061a45, 570c222, fe6c27f
- **Origin:** RF port (#76 Fate Ledger: Mimo V2.6 Pro Edition, u/GenericStatement's finding; GLM Flash States Gate)

### FATE-08

- **Models:** Kimi K3, Gemma 4, Claude Opus 4.6
- **Symptom:** Kimi and Gemma seeded q 15 (took the adjusted A for q); Claude read C as the tier die.
- **Fix:** q defined (AMBIENT turns in a row, from 0); 'read the total on q's band' and 'lower total' name what is compared.
- **Beta 5 wording:**
  > q counts AMBIENT turns in a row, from 0; read the total on q's band: q 0-2: MINOR 16+, MAJOR 20+; q 3-6: 12+, 19+; q 7+: 8+, 17+; lower total: AMBIENT, q +1; else q 0.
- **Where:** fate Tier line
- **Commits:** fe6c27f
- **Origin:** tester report (issue #10: 'Kimi ALSO noted some confusion in your fate instructions'); RF STEP 2 definition

### FATE-09

- **Models:** Claude Opus 4.6, Kimi K3
- **Symptom:** Claude read '+2 at 1-2' as q 1-2; Kimi counted one item deferred xN more than once.
- **Fix:** The noun hangs on both counts.
- **Beta 5 wording:**
  > Tier: A, -3 if MAJOR in last 2 turns, else +4 at 3+ or +2 at 1-2 Deferred items.
- **Where:** fate Tier line
- **Commits:** 570c222, fe6c27f
- **Origin:** tester report (issue #10)

### FATE-10

- **Models:** Gemma 4
- **Symptom:** Gemma logged hp 7 with no [hot] Bullet and six illegal WEIGHTED cells.
- **Fix:** 'hp counts [hot] Bullets' makes hp 0 when none exist.
- **Beta 5 wording:**
  > Source: hp counts [hot] Bullets; WEIGHTED on B 14+ at hp 1-2, 9+ at 3-4, 5+ at 5+, else TRUE.
- **Where:** fate Source line
- **Commits:** 570c222, fe6c27f
- **Origin:** tester report (issue #10)

### FATE-11

- **Models:** GLM 5.3, Kimi K3
- **Symptom:** Both opened a THREAD and deferred against it in the same turn; Kimi kept a deferred item offscreen and planned it as a future MAJOR; GLM deferred the player's own pending answer.
- **Fix:** Opening comes first, else the roll meets the open thread: one roll, one effect; '(seen, handled later)' defines deferral.
- **Beta 5 wording:**
  > THREAD: a pursuit anyone present chooses; close or park it by age 8. MINOR or MAJOR opens one if none is open, else meets it: MINOR defers on C 1-12 (seen, handled later), else complicates; MAJOR complicates on C 1-10, else displaces.
- **Where:** fate THREAD line
- **Commits:** 570c222, fe6c27f
- **Origin:** tester report (issue #10); RF STEP 5

### FATE-12

- **Models:** Kimi K3
- **Symptom:** Kimi deferred one item three times; RF's 'next time it comes up' never happened.
- **Fix:** A MINOR may bring a deferred item back; one deferred twice returns as MAJOR; expiry at age 6 leaves Residue.
- **Beta 5 wording:**
  > Deferred items expire at age 6; a MINOR may bring one back, and one deferred twice returns as MAJOR. Each close, park or expiry leaves Residue.
- **Where:** fate THREAD line
- **Commits:** 4e93159, 570c222, fe6c27f
- **Origin:** RF port (STEP 6) + tester report (issue #10)

### FATE-13

- **Models:** GLM 5.3
- **Symptom:** GLM logged on-site texture as World news.
- **Fix:** AMBIENT C 1-6 is heard world news; news arrives by the era's channel, late, slanted, misheard; nobody ties effect to news aloud.
- **Beta 5 wording:**
  > AMBIENT on C 1-6 is heard world news, logged, skipping Source. || News: era's channel, late, slanted, misheard; reactions proportional; nobody ties effect to news aloud.
- **Where:** fate Tier line end; fate News line
- **Commits:** 4e93159, 570c222, fe6c27f
- **Origin:** RF port (AMBIENT news, WORLD NEWS) + tester report (issue #10)

### FATE-14

- **Models:** Claude Opus 4.6, GLM 5.3, Kimi K3, Gemma 4
- **Symptom:** All four models logged the scene's own beat, an NPC's choice or the player's success in 'last'.
- **Fix:** 'last' logs fate's own happening.
- **Beta 5 wording:**
  > last: AMBIENT/MINOR/MAJOR TRUE/WEIGHTED, fate's 5-word happening
- **Where:** fate Ledger template
- **Commits:** fe6c27f
- **Origin:** tester report (issue #10)

### FATE-15

- **Models:** Claude Opus 4.6, Gemma 4 31B, MiMo V2.6
- **Symptom:** Claude read 'collision' as the C 20 ceiling (the module never says collision); Gemma, whose plan had no ceiling step, broke the ceiling on all three MAJORs; MiMo spent over half its reasoning walking Fate rules.
- **Fix:** Plan's Fate line: 'C vs THREAD' and an explicit 'C 20 limit' step; results only.
- **Beta 5 wording:**
  > - Fate: A tier; C news; B source; cell; C vs THREAD; C 20 limit; results only.
- **Where:** logic_core Fate line (ariaFateLine, set by fate)
- **Commits:** 4e93159, 570c222, fe6c27f
- **Origin:** tester report (issue #10) + RF Fate Ledger 'results only'

### FATE-16

- **Models:** all
- **Symptom:** Appointments forgotten or fired off-schedule; Bullets piling up.
- **Fix:** Bullets 8 max, ≤1/turn, [hot] if the user caused it, prune at 12; a named future time loads an ageless TIME-LOCKED Bullet that fires on time at any tier and sets THREAD (reads the Time & Place clock).
- **Beta 5 wording:**
  > Bullets (8 max): load ≤1/turn for setups a reader would notice unpaid, [hot] if User caused it; prune at age 12. A named future time loads an ageless TIME-LOCKED one at Day # HH:MM that fires on time at any tier and sets THREAD.
- **Where:** fate Bullets line
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#77 Chekhov's Gun); base 'NPCs return naturally' removed in 570c222

### FATE-17

- **Models:** Kimi K3, all
- **Symptom:** Quiet turns filled with job loops or forced drama.
- **Fix:** Quiet turns: needs and clock drive NPCs, more talk, exactly one change, Residue; q 0-2 aftermath. The old job-loop cap and 'refusals to engage' moved to Trade and Bold Characters.
- **Beta 5 wording:**
  > Quiet (AMBIENT or no THREAD): needs and clock drive NPCs; more talk, idle or NPC-to-NPC; exactly one thing changes; draw on Residue. q 0-2: aftermath, nobody solves anything, no NPC opens a pursuit unforced.
- **Where:** fate Quiet line
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#63 Quiet/aftermath)

### FATE-18

- **Models:** all (Claude caching)
- **Symptom:** Dice in the system block break prompt caching.
- **Fix:** Dice live in a setvar and print only at depth 0 through the gate, which clears them after use.
- **Beta 5 wording:**
  > Fate dice: A 7 | B 7 | C 7 (rendered from {{setvar::ariaDice::Fate dice: A {{roll::1d20}} | B {{roll::1d20}} | C {{roll::1d20}}}})
- **Where:** fate setvar; final_gate dice line
- **Commits:** 4e93159
- **Origin:** RF port (Turn Dice at depth 0)

## 🥰 Bonds Lite

### BONDS-01

- **Models:** all
- **Symptom:** No room for thirst for revenge or marriage proposals; strangers started '+0/0/0'.
- **Fix:** BOND range -10..+20 with a -10 malice tier and a +20 proposal tier; strangers start 0/0/0.
- **Beta 5 wording:**
  > Each pair, NPC pairs too, has BOND -10..+20, Sparks and Grudge, logged as Name↔Name +6/3/0 (strangers start 0/0/0), comma-separated; never a number in prose.
  > Touch gates allow, never oblige: -10 pure malice, seeks to harm, extreme violence, reversal near impossible; ... +16 chosen family; +20 User is allowed to propose marriage, extended time without proposal + character desires marriage -> character may propose instead.
- **Where:** bonds lines 1-2
- **Commits:** d6b1cd7, ee047ef
- **Origin:** owner hand edit (TC copy arrived with ee047ef)

### BONDS-02

- **Models:** all (beta 3 models)
- **Symptom:** With Fate on, the bonds field inside the 🎲 block showed up as a loose line or a bare card under the panel.
- **Fix:** Bonds writes its own 💚 block after the 🎲 block; plan and gate name both.
- **Beta 5 wording:**
  > - Ledger: last 🎲 block plus this turn's changes, ages +1; last 💚 block's pairs plus this turn's shifts; the closing 🎲 block, then the 💚 block, copy them. || gate: - Ledger: one full 🎲 block, then one <details><summary>💚</summary>pairs</details> block, end the reply.
- **Where:** bonds setvars (ariaLedgerLine/ariaLedgerGate, Fate-on branch); logic_core Ledger line; final_gate Ledger check
- **Commits:** 570c222, bd9ffd2
- **Origin:** ARIA original

### BONDS-03

- **Models:** MiMo V2.6
- **Symptom:** Bonds ledger drifting when Fate is off.
- **Fix:** With Fate off, Bonds brings its own 💚 plan and gate ledger lines.
- **Beta 5 wording:**
  > - Ledger: last 💚 block's pairs plus this turn's shifts; the closing 💚 block copies these. || - Ledger: one <details><summary>💚</summary>pairs</details> block ends the reply.
- **Where:** bonds setvars (Fate-off branch)
- **Commits:** 6061a45, 570c222
- **Origin:** RF port (Fate Ledger MiMo pattern)

### BONDS-04

- **Models:** all (Chinese families, MiMo)
- **Symptom:** Models copy named examples (the old 'like Mia↔Leo' example).
- **Fix:** Name↔Name placeholder gives the bar cards both full names with no copyable example name.
- **Beta 5 wording:**
  > logged as Name↔Name +6/3/0 (strangers start 0/0/0), comma-separated; never a number in prose.
- **Where:** bonds line 1
- **Commits:** 279bb31, 570c222
- **Origin:** ARIA original on RF's no-named-examples rule

### BONDS-05

- **Models:** all
- **Symptom:** Thresholds read as obligations; bonds rising too fast.
- **Fix:** Gates allow, never oblige; one direct shift per pair per turn; Sparks capped 2/turn (1 at Grudge 3+); Freaky suspends touch gates.
- **Beta 5 wording:**
  > One direct shift per pair per turn, as each NPC reads the act: -1 insult or dismissal; -2 betrayal or cruelty; +1 costly rescue, defense or sacrifice they knew of.
  > Sparks +1 per warm act, 2/turn (1 at Grudge 3+); 7 become BOND +1; -1 per 5 turns without contact. Grudge +1 per slight; 5 become BOND -1; an apology clears it.
- **Where:** bonds lines 3-4
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#71 Relationships RPG)

## 🩹 Model patches

### PATCH-01

- **Models:** Claude 5 (Fable, Opus, Sonnet)
- **Symptom:** Claudisms and terminally online wording.
- **Fix:** Claude-only banned words; 'data' only for tech minds; net slang only for very online characters. Keep OFF for other families.
- **Beta 5 wording:**
  > Banned: file X away, structural failure, architectural, geometry; "data" unless tech-minded; net slang unless very online.
- **Where:** patch_claude5 line 1
- **Commits:** 4e93159, 570c222, fe6c27f, 32f062f
- **Origin:** RF port (#37 ban_claudisms, Fix Claude 5's Terminally Online Wording)

### PATCH-02

- **Models:** Claude 5
- **Symptom:** Lines that rate or classify the scene ('I respect that').
- **Fix:** Approval ratings become stance or action; 'that's valid' falls under the validation ban, filler 'honestly' under Register.
- **Beta 5 wording:**
  > Approval ratings ("I respect that") become stance or action.
- **Where:** patch_claude5 line 2
- **Commits:** 4e93159, 570c222, fe6c27f
- **Origin:** RF port (#8 dialogue_provenance)

### PATCH-03

- **Models:** Gemini 3.7 Flash, Gemini
- **Symptom:** Therapist talk returning when the user invites it.
- **Fix:** Question and therapist limits hold even when invited; only counselor cards lift them.
- **Beta 5 wording:**
  > <scene_engine>'s question and therapist limits hold even when invited; only counselor cards lift them.
- **Where:** patch_gemini line 1
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#3 youre_not_a_therapist)

### PATCH-04

- **Models:** Gemini
- **Symptom:** Composed, articulate reactions to heavy news.
- **Fix:** Heavy news gets clumsy human reactions.
- **Beta 5 wording:**
  > Heavy news gets clumsy human reactions.
- **Where:** patch_gemini line 2
- **Commits:** 4e93159
- **Origin:** RF port (Cosmos lesson #30)

### PATCH-05

- **Models:** Gemini
- **Symptom:** 'It won't just be X, it'll be Y' forecasts and closers.
- **Fix:** Forecasts and closing lines keep one outcome at full size, worded as a limit so Gemini does not read it as an order to end on a forecast.
- **Beta 5 wording:**
  > Forecasts and closing lines keep one outcome, once, at full size.
- **Where:** patch_gemini line 3
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (Cosmos lesson #41 forecast form)

### PATCH-06

- **Models:** Gemini
- **Symptom:** Smell mentions act as reminders.
- **Fix:** Gemini users switch Scent Occasions OFF (patch note, entry name, setup note 4, guide table).
- **Beta 5 wording:**
  > Switch 👃 Scent Occasions OFF as well. Use one model patch at most.
- **Where:** patch_gemini C note; README setup note 4
- **Commits:** 4e93159
- **Origin:** RF port (Smell & Taste Rules OFF for Gemini)

### PATCH-07

- **Models:** GLM 5.x, Kimi K2.x/K3, Qwen
- **Symptom:** Okay-loop: characters steadying or thinking out loud with one filler word, once or on repeat.
- **Fix:** Steadying or self-talk filler becomes the thought or the action; answering someone it stands once; the word is never named (naming primes these models); nervous cards keep stalls via Card Fidelity.
- **Beta 5 wording:**
  > Steadying or self-talk filler becomes the specific thought it held or the action; answering someone, it stands once.
- **Where:** patch_chinese line 1
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#47 stall_word_killswitch / GLM Okay-Loop Killswitch, #111 final_stall_gate)

### PATCH-08

- **Models:** GLM 5.1-5.3, Kimi K2.5-K3, Qwen, MiMo V2.5
- **Symptom:** Over-rumination: draft, critique, redraft loops in native thinking.
- **Fix:** One pass, a terse bullet per plan line or step, no drafts, then stop; 'plan line or step' reads right with or without The Logic Core and its tags.
- **Beta 5 wording:**
  > Native reasoning: one pass, a terse bullet per plan line or step, no drafts, then stop.
- **Where:** patch_chinese line 2
- **Commits:** 4e93159, 570c222, 0daf174
- **Origin:** RF port (#102 Chinese LLM Thinking Leash)

### PATCH-09

- **Models:** MiMo V2.6 Flash
- **Symptom:** Flash settles into one guarded, job-first register by ~turn 20 (u/trashhaul: Tatiana like a coworker waiting for her shift to end, jokes passed over, mysterious air with no conflict) and rewrites card facts (NC Bench: a 32-year-old with a 112-year career).
- **Fix:** Five labelled one-check lines (MiMo plans in labelled lines): fixed card facts, resting mood, lull interests, jokes landing card-true, secrets guard only their topic. Keep OFF on Pro; ship Flash with Logic Core Tags ON.
- **Beta 5 wording:**
  > Fixed: card ages, names, numbers, ties, history, details filled once.
  > Mood: card's, shaded by ties to User; back after events.
  > Lulls: bring up card interests.
  > Jokes: User's land visibly, card-true.
  > Secrets guard only their topic; elsewhere, open as the card allows.
- **Where:** patch_mimo_flash
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#115 Character Hold: Mimo Flash Edition)

### PATCH-10 (removed later)

- **Models:** Kimi K3
- **Symptom:** Kimi kept handing the user's words back (pet name echoed as a question, order read back) despite the gate's echo check.
- **Fix:** A dedicated Kimi patch (RF NPC anti-repeat rule with a Dan/Jess example and an 'Anti-repeat'/'First words' plan line) was added, then reverted: its example primed the very shape it banned and its plan line restated the user's message before the prose. Kimi users run the GLM / Kimi / Qwen patch.
- **Beta 5 wording:**
  > removed
- **Where:** former patch_kimi entry and ariaPatchLine plan splice
- **Commits:** 30f7115, b2238c6, ee047ef
- **Origin:** owner hand edit (30f7115, b2238c6), reverted in ee047ef

## 🔦 Flash Gate

### FLASH-01

- **Models:** GLM 5.3 Flash, MiMo V2.6 Flash
- **Symptom:** Filing, notarising and banking feelings in emotional scenes nobody is doing paperwork in (issue #10: 'paperwork (even with the patch on)'); full-size models dropped it.
- **Fix:** A setter that prints one outright rule (no question, no example, narration included) at the end of the gate; restates Trade on purpose; RF's 'habit through earlier messages' rule stated positively.
- **Beta 5 wording:**
  > - Work words, narration too: tell feelings, memories, promises and decisions in the moment's terms (action, speech, next choice); work and its words appear only when it is underway on the page, someone else raises it, something due now presses on it, or it serves as a dodge; a habit running through earlier replies is the one to drop.
- **Where:** flash_gate (ariaFlashGate) printed in final_gate; guide FAQ 'GLM Flash or MiMo Flash keeps turning feelings into paperwork.'
- **Commits:** 570c222, fe6c27f
- **Origin:** RF port (Last-Mile Vocation Gate: Flash Edition, u/Karl21_'s GLM 5.3 Flash report)

## 🧠 The Logic Core

### LC-01

- **Models:** MiMo V2.6 Pro, MiMo V2.6 Flash, all
- **Symptom:** Long, character-flattening native reasoning (Flash ships only this way); MiMo follows its plan more closely than the system prompt.
- **Fix:** The Logic Core is the AI's own message at In-Chat depth 0 (assistant role), above the gate in prompt order so the gate can print its cue.
- **Beta 5 wording:**
  > 🧠 The Logic Core: role assistant, injection_position 1, injection_depth 0; prompt_order ... (logic_core, on), (logic_core_twin, off), (jailbreak/Last-Mile Gate, on)
- **Where:** logic_core entry settings and prompt_order
- **Commits:** 4e93159, bd9ffd2
- **Origin:** RF port (#95 pico CoT: Mimo V2.6 Edition, assistant role from the 2.2.1 hotfix)

### LC-02

- **Models:** MiMo V2.6 Pro, MiMo V2.6 Flash
- **Symptom:** Minutes of thinking; plan lines rewritten as reply drafts.
- **Fix:** Fragments, never reply sentences, settled once written; together shorter than one reply paragraph (cut MiMo to ~15 s on Pro, ~30 s on Flash).
- **Beta 5 wording:**
  > Lines are fragments, never reply sentences, settled once written; together shorter than one reply paragraph.
- **Where:** logic_core line 2
- **Commits:** 4e93159, dd8cc5f, 570c222
- **Origin:** RF port (pico CoT)

### LC-03

- **Models:** MiMo V2.6
- **Symptom:** MiMo V2.6 ignored OOC instructions; OOC questions answered with a full scene, header and ledger.
- **Fix:** OOC line: notes or none; questions get only an OOC answer, no header or ledger; commands shape the reply.
- **Beta 5 wording:**
  > - OOC: notes or none; questions get only an OOC answer, no header or ledger; commands shape the reply.
- **Where:** logic_core OOC line
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (pico 2.2.1 hotfix)

### LC-04

- **Models:** MiMo V2.6 Flash, Kimi K3
- **Symptom:** Card drift of NPC wants over long chats (MiMo Flash); pronoun drift (Kimi).
- **Fix:** Scene line re-anchors each NPC's want to the card every turn and writes pronouns; gaps filled once.
- **Beta 5 wording:**
  > - Scene: positions; held items; what just happened; card-true NPC wants and pronouns; gaps filled once (**Personality Independence:**).
- **Where:** logic_core Scene line
- **Commits:** 4e93159, 570c222, 32f062f
- **Origin:** RF port (pico Scene line) + owner Kimi K3 test

### LC-05

- **Models:** MiMo V2.6 Pro, GLM 5.3, Kimi K3
- **Symptom:** V2.6 mind reading and invented past (non-English chats); GLM knowing narration; Kimi's omniscience.
- **Fix:** Knows line is RF BOLT task 3: what each acting NPC saw, heard or was told, nothing from narration, other scenes or the user's head; gate checks it last.
- **Beta 5 wording:**
  > - Knows: what each acting NPC saw, heard or was told; nothing from narration, other scenes or User's head (**Epistemic Limits:**). || gate: - Knows: an NPC using what they never saw, heard or were told?
- **Where:** logic_core Knows line; final_gate Knows check
- **Commits:** 4e93159, 570c222, 89c65f0, 5754829
- **Origin:** RF port (pico Knows line 2.2.1.2 hotfix, BOLT task 3) + owner tests

### LC-06

- **Models:** Kimi K3, all, MiMo V2.6
- **Symptom:** Stock dialogue with no mood or drive; address drift; English words in non-English dialogue.
- **Fix:** Voice line works out each speaker's VAD and live instinct, register and address, and native words.
- **Beta 5 wording:**
  > - Voice: each speaker's VAD and live instinct; register, address (**Card Fidelity:**); native words (**Story Language:**).
- **Where:** logic_core Voice line
- **Commits:** 4e93159, 570c222, fe6c27f, 6740eac
- **Origin:** RF port (pico Voice line, BOLT dialogue task) + tester report (issue #10, address)

### LC-07

- **Models:** all
- **Symptom:** Scenes without resistance or adjustment; replies taking the user's decision.
- **Fix:** Move line: who pursues what; resistance; adjustment; result; handoff (adjustment stated here since scene_engine no longer names tactics).
- **Beta 5 wording:**
  > - Move: who pursues what; resistance; adjustment; result; handoff.
- **Where:** logic_core Move line
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (pico Move line)

### LC-08

- **Models:** MiMo V2.6, MiMo V2.6 Flash, Claude Opus 4.6
- **Symptom:** An earlier RF Fresh line listed the last two replies' details and the reply brought four back; Flash re-chose recorded colours and values; Claude opened a scene on an office's smell.
- **Fix:** Fresh names only what is new, as seen, heard or touched details tied to actions; card features only when the scene turns to them; recorded names, colours, values copied.
- **Beta 5 wording:**
  > - Fresh: 2-3 new seen, heard or touched details tied to actions; card features only if the scene turns to them; recorded names, colours, values copied.
- **Where:** logic_core Fresh line
- **Commits:** 4e93159, 570c222, 89c65f0
- **Origin:** RF port (pico Fresh line) + owner Claude test

### LC-09

- **Models:** all, Claude ('Check line is a rubber stamp')
- **Symptom:** The plan's check duplicating gate rules; Claude ticking it without checking.
- **Fix:** Check points at the gate; the gate holds one line per label.
- **Beta 5 wording:**
  > - Check: run <final_gate>.
- **Where:** logic_core Check line
- **Commits:** 4e93159
- **Origin:** RF port (pico Check line, replaced by a pointer)

### LC-10

- **Models:** MiMo V2.6 Pro, MiMo V2.6 Flash, all style-B models
- **Symptom:** Plan text leaking into the reply; header or ledger placed wrongly; 'free of plan text' was too vague.
- **Fix:** RF's step-by-step closing order: the tag closes on the line after go, the reply starts on the line after that (header, prose, ledger last); nothing above go enters the reply.
- **Beta 5 wording:**
  > </thinking> closes on the line after go. The reply starts on the line after that: header if <header_instructions>; prose; ledger last. Nothing above go enters the reply.
- **Where:** logic_core closing lines (tags on)
- **Commits:** 279bb31, dd8cc5f, 570c222, bd9ffd2, 0daf174
- **Origin:** RF port (pico closing)

### LC-11

- **Models:** MiMo V2.6, models with Logic Core Tags on
- **Symptom:** With tags on and native reasoning off, models copied the checklist word for word when the opening said 'the dashed lines below'.
- **Fix:** Opening counts the lines (logicCoreLines: 7 plus Mode, Fate, Bonds, Ledger splices) and never points at a list beneath it.
- **Beta 5 wording:**
  > <thinking> opens the reply, then 11 dashed lines, then go.
- **Where:** logic_core opening line (logicCoreLines counter)
- **Commits:** dd8cc5f, 6061a45, 0daf174
- **Origin:** RF port (pico 'ten dashed lines' wording)

### LC-12

- **Models:** MiMo V2.6, Qwen/GLM/DeepSeek-hosted templates
- **Symptom:** Replies opened with <logic_core> and closed with </thinking>; templates splitting assistant messages on </think> swallowed the checklist.
- **Fix:** Exactly one closing-tag mention, starting the line after go, never on line 1.
- **Beta 5 wording:**
  > </thinking> closes on the line after go.
- **Where:** logic_core closing line
- **Commits:** dd8cc5f, 0daf174
- **Origin:** ARIA original

### LC-13

- **Models:** MiMo V2.6 Pro
- **Symptom:** MiMo copied the static <logic_core> wrapper that opened its own last message, so Auto-Parse missed the plan and only the regex fallback folded it.
- **Fix:** With tags on there is no wrapper: the message opens on the fence tag itself as a sentence subject, so a copied first token is the tag Auto-Parse reads; the checker fails any tags-on render naming <logic_core>.
- **Beta 5 wording:**
  > <thinking> opens the reply, then 11 dashed lines, then go.
- **Where:** logic_core opening (tags-on branch); tools/aria_budget.py tags-on <logic_core> ban
- **Commits:** 0daf174, bf42411
- **Origin:** ARIA original

### LC-14

- **Models:** native-reasoning models (style A: Claude, DeepSeek, GLM/Kimi/Qwen)
- **Symptom:** With native reasoning the plan runs inside the model's own thinking.
- **Fix:** Tags off keeps the <logic_core> wrapper and beta-4 wording byte for byte.
- **Beta 5 wording:**
  > <logic_core>
  > Reasoning writes N dashed lines, then go; the reply follows.
  > ...
  > Reasoning ends at go. The reply: header if <header_instructions>; prose; ledger last. Nothing above go enters the reply.
  > </logic_core>
- **Where:** logic_core tags-off branch
- **Commits:** 279bb31, dd8cc5f, 0daf174
- **Origin:** ARIA original

### LC-15

- **Models:** MiMo V2.6 Pro, chat formats that move system messages to the top
- **Symptom:** Plans skipped when the system instruction was moved away from the end.
- **Fix:** A last line inside the plan message restates the opening.
- **Beta 5 wording:**
  > Every response starts with <thinking>.
- **Where:** logic_core last line (tags on)
- **Commits:** bd9ffd2, 0daf174
- **Origin:** ARIA original

### LC-16

- **Models:** MiMo V2.6 Pro
- **Symptom:** MiMo skipped the plan on some providers.
- **Fix:** The Logic Core sets ariaPlanCue and the gate prints it after </final_gate> as the very last line read; 0daf174 dropped 'with the <logic_core> labels'.
- **Beta 5 wording:**
  > Begin with <thinking>, then 11 dashed lines, go and </thinking>; the reply follows.
- **Where:** logic_core setvar ariaPlanCue; final_gate last line
- **Commits:** bd9ffd2, 0daf174
- **Origin:** ARIA original

### LC-17

- **Models:** MiMo V2.6 Pro, style-B models
- **Symptom:** 'Silently fix hits' plus the Register check could make the model treat the labelled plan as a hit to delete.
- **Fix:** With a tags-on Logic Core the gate opens 'After the plan, fix hits in the prose'.
- **Beta 5 wording:**
  > After the plan, fix hits in the prose per <anti_slop>: (else: Silently fix hits per <anti_slop>:)
- **Where:** final_gate opener
- **Commits:** bd9ffd2
- **Origin:** ARIA original

### LC-18

- **Models:** MiMo V2.6 Pro (some providers), Claude (keep the plain one)
- **Symptom:** Models skipping a plan that sits in the AI's own message.
- **Fix:** System-role twin (off by default) merges into the gate's final system message; never run both; Claude turns late system messages into user text; no user-role version (breaks the jailbreak). FAQ and live test plan cover per-provider testing.
- **Beta 5 wording:**
  > Try this one when your model keeps skipping the plan (MiMo V2.6 Pro has been doing that on some providers), and switch the plain Logic Core OFF. Never run both. Claude turns late system messages into user text, so Claude users keep the plain one. There is no user-role version, because a user message there breaks the jailbreak on many models.
- **Where:** logic_core_twin (🧠 The Logic Core (system-role twin), system, depth 0)
- **Commits:** bd9ffd2
- **Origin:** ARIA original (replaced the beta-1 user-role twin)

### LC-19

- **Models:** Qwen, GLM, DeepSeek reasoning hosts, Claude
- **Symptom:** Hosts that split messages at </think> hide the whole checklist; an open or </think>-closed tag moves the whole reply into the reasoning box; Claude keeps its own thinking regardless.
- **Fix:** Logic Core Tags is a setter only; keep <thinking>; untick Auto-Parse if replies come back empty; Claude users leave it OFF.
- **Beta 5 wording:**
  > {{setvar::ariaThinkOpen::<thinking>}}{{setvar::ariaThinkClose::</thinking>}} || note: Keep the <thinking> name: hosts running Qwen, GLM or DeepSeek reasoning models cut The Logic Core at a </think> tag, which would drop its opening line and the whole checklist. If a reply ever arrives empty with the whole story inside the reasoning box, the model left the tag open or closed it with </think>; untick Auto-Parse and the regex scripts fold the plan on their own. ... Claude keeps its own thinking on whatever you set, so Claude users leave this OFF.
- **Where:** logic_core_tags entry and C note
- **Commits:** b4eb991, dd8cc5f, 570c222, 0daf174
- **Origin:** ARIA original

### LC-20

- **Models:** all
- **Symptom:** Other modules naming <logic_core> broke when the tags-on shape lost its wrapper.
- **Fix:** Other prompts call it 'the plan', which reads right in both shapes and with The Logic Core off.
- **Beta 5 wording:**
  > whatever the plan says (Impersonation Turn); a terse bullet per plan line or step (GLM / Kimi / Qwen patch)
- **Where:** impersonation_turn; patch_chinese
- **Commits:** 0daf174
- **Origin:** ARIA original

### LC-21 (removed later)

- **Models:** MiMo V2.6
- **Symptom:** Replies opening with an announcement, map, re-plan or preview of what follows.
- **Fix:** The base Logic Core turned any preview or announcement into the first sentence (RF pico); dropped in the beta 3 compression; Register's 'first words are the point' partly covers it.
- **Beta 5 wording:**
  > removed (base text was: A preview or announcement becomes the first sentence; nothing above go enters the reply.)
- **Where:** logic_core closing (former)
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (pico: 'Anything that would announce, map, re-plan or preview the reply becomes the first sentence instead.')

## 🚪 Last-Mile Gate

### GATE-01

- **Models:** GLM (sparse attention), Flash-tier models, all
- **Symptom:** Rules stated far up the prompt lose to the model's own earlier habits in the log.
- **Fix:** Last-Mile Gate at depth 0, system role, after the chat: one check line per Anti-Slop label plus splices (scent, POV, ledger, Flash); labels must match anti_slop exactly.
- **Beta 5 wording:**
  > <final_gate>
  > After the plan, fix hits in the prose per <anti_slop>:
  > - Contrast: negated/shrunk half?
  > - Chop: a one-word order, or a period before words that can't stand alone?
  > - Register: announcing?
  > - Trade: unasked work?
  > - Cadence: triad, reversed, restated or timed action?
  > - Vocabulary: listed word?
  > - Senses: reused detail or tell, second simile?
  > - Skips: line summing up skipped time?
  > - Echo: User's last message, or a pet name or odd word from it, handed back?
  > - Ending: stock or quotable closer (<scene_engine>)?
  > - Knows: an NPC using what they never saw, heard or were told?
- **Where:** final_gate (🚪 Last-Mile Gate, jailbreak slot, depth 0)
- **Commits:** 4e93159, 570c222, 56d0687, fe6c27f, e4b0fad, 6740eac, 89c65f0, 5754829, 32f062f
- **Origin:** RF port (Last-Mile Contrast/Legato/Register/Vocation gates)

### GATE-02

- **Models:** Gemini 3.8 Flash, GLM, all
- **Symptom:** Patterns copied from earlier replies in the log ('never copy a smell from the log'); card exceptions (nervous stalls, terse orders, in-role briefers) wrongly cut.
- **Fix:** Past replies excuse no hit, scoped to the checked patterns so it never forbids copying the header or ledger; the card outranks the checks.
- **Beta 5 wording:**
  > Past replies excuse no hit; the card outranks these (**Card Fidelity:**).
- **Where:** final_gate closing line
- **Commits:** 4e93159, 570c222
- **Origin:** RF port ('earlier messages are not a style license')

## 🪞 Impersonation Turn

### IMP-01

- **Models:** MiMo V2.6
- **Symptom:** During Impersonate the chat ends on the AI's reply, and MiMo answered system-role instructions there by copying them into the input box.
- **Fix:** Impersonation Turn is a user-role In-Chat depth-0 entry triggered only on Impersonate.
- **Beta 5 wording:**
  > 🪞 Impersonation Turn: role user, injection_position 1, injection_depth 0, injection_trigger ['impersonate']
- **Where:** impersonation_turn entry settings
- **Commits:** 4e93159
- **Origin:** RF port (#117 Impersonation Turn)

### IMP-02

- **Models:** MiMo V2.6, Claude Opus 4.6, non-reasoning models
- **Symptom:** Planning still aimed at an NPC reply; card secrets put in the user's mouth; Opus 4.6 opened impersonations with the scene header; ledger and NPC lines in the input box.
- **Fix:** Turns any reasoning toward the user's move (no visible plan forced on non-reasoning models), limits the user's knowledge, starts on the user's first word or action, overrides the plan's header and ledger.
- **Beta 5 wording:**
  > OOC: write {{user}}'s next message. Any reasoning plans {{user}}'s move from persona and earlier messages; {{user}} knows only what {{user}} saw, heard or was told; the message follows, starting on {{user}}'s first word or action; write only {{user}}'s words, actions and thoughts; stop where another character would answer; no header, NPC lines or 🎲/💚 block, whatever the plan says.
- **Where:** impersonation_turn <impersonation_turn>
- **Commits:** 4e93159, 570c222, 0daf174
- **Origin:** RF port (#117, Legacy Edition for Opus 4.6)

### IMP-03

- **Models:** MiMo V2.6
- **Symptom:** MiMo fell back on the narrator's habit and wrote the user in third person.
- **Fix:** The turn brings its own <POV>, replacing Hybrid POV for this turn.
- **Beta 5 wording:**
  > This turn's POV replaces any earlier one: {{user}} in first person present, unless {{user}}'s earlier messages use another person or tense.
- **Where:** impersonation_turn <POV>
- **Commits:** 4e93159, 570c222
- **Origin:** RF port (#117)

### IMP-04

- **Models:** all
- **Symptom:** On Impersonate the gate still asked for a ledger and the plan still ran Fate/Bonds lines; the POV check would contradict first person.
- **Fix:** Runs before The Logic Core and the gate and blanks the Fate, Bonds, ledger, dice and POV-gate variables.
- **Beta 5 wording:**
  > {{setvar::ariaFateLine::}}{{setvar::ariaBondsLine::}}{{setvar::ariaLedgerLine::}}{{setvar::ariaLedgerGate::}}{{setvar::ariaDice::}}{{setvar::ariaPovGate::}}
- **Where:** impersonation_turn first line; prompt_order (impersonation_turn above logic_core and gate)
- **Commits:** 570c222, e4b0fad
- **Origin:** ARIA original

### IMP-05

- **Models:** local Text Completions models
- **Symptom:** Text Completions has no Impersonate-only entry.
- **Fix:** The TC post-history plan and gate say it outright; build_tc.py anchors these on 'Nothing above go enters the reply.' and '{{getvar::ariaLedgerGate}}'.
- **Beta 5 wording:**
  > When this turn asks for {{user}}'s own message, plan {{user}}'s move only and skip the Fate, Bonds and Ledger lines. || {{getvar::ariaLedgerGate}} A message written as {{user}} carries none.
- **Where:** TC post_history (logic_core and final_gate)
- **Commits:** 96de46c, 570c222, bd9ffd2, 0daf174
- **Origin:** ARIA original

## Regex scripts

### RX-01

- **Models:** MiMo V2.6 Pro
- **Symptom:** A word-for-word echo of the beta-5 Logic Core template at the top of a reply.
- **Fix:** Folds the echoed template (and a real plan written under it) into the 💭 Thoughts box, display only; closing line matched only through the template's own words.
- **Beta 5 wording:**
  > ARIA - Fold an echoed Logic Core template into a Thoughts box (display only)
- **Where:** regex fold-echo (CC preset and TC regex file)
- **Commits:** 0daf174, bf42411
- **Origin:** ARIA original

### RX-02

- **Models:** MiMo V2.6 Pro
- **Symptom:** After Auto-Parse took the plan, the echoed closing lines ('closes on the line after go...', 'Every response starts with <thinking>.') stayed visible, sometimes twice.
- **Fix:** Hides the echoed closing lines globally on display, including after a blank line; story text on the same line stays.
- **Beta 5 wording:**
  > ARIA - Hide an echoed Logic Core closing line (display only)
- **Where:** regex hide-echo-tail
- **Commits:** 0daf174, bf42411
- **Origin:** ARIA original

### RX-03

- **Models:** MiMo V2.6 Pro
- **Symptom:** Echoed template text re-read by the model on later turns.
- **Fix:** Strips the echoed template from the prompt at all depths (cache-safe).
- **Beta 5 wording:**
  > ARIA - Keep an echoed Logic Core template out of the prompt (all depths, cache-safe)
- **Where:** regex strip-echo
- **Commits:** 0daf174, bf42411
- **Origin:** ARIA original

### RX-04

- **Models:** MiMo V2.6 Pro
- **Symptom:** An echoed template emptied or polluted the Impersonate input; the old 600-character match deleted story text.
- **Fix:** User-input version: a typed 'Every response starts with' line or quoted closing sentence stays; a plan closed with the copied first sentence is cleaned.
- **Beta 5 wording:**
  > ARIA Impersonate - strip an echoed Logic Core template
- **Where:** regex imp-echo
- **Commits:** 0daf174, bf42411
- **Origin:** ARIA original

### RX-05

- **Models:** all reasoning or style-B models
- **Symptom:** Thinking blocks (think, thinking, thought, reasoning, internal_monologue, logic_core, ### Reasoning headings) showing in replies and re-read by the model.
- **Fix:** Fold into a 💭 Thoughts box on display; strip from the prompt at all depths.
- **Beta 5 wording:**
  > ARIA - Fold thinking into a Thoughts box (display only) | ARIA - Keep thinking out of the prompt (all depths, cache-safe)
- **Where:** regex fold, strip
- **Commits:** 4e93159, 279bb31, dd8cc5f
- **Origin:** RF port (V2.6 leak regexes) + ARIA

### RX-06

- **Models:** MiMo V2.6, style-B models
- **Symptom:** Plans opened with <logic_core> and closed with </thinking>.
- **Fix:** Folds and strips plans whose opening and closing tags differ; matching pairs are stripped first so an echo quoting <thinking> goes whole.
- **Beta 5 wording:**
  > ARIA - Fold a plan whose opening and closing tags differ (display only) | ARIA - Keep mismatched thinking tags out of the prompt (all depths, cache-safe)
- **Where:** regex fold-mismatch, strip-mismatch
- **Commits:** dd8cc5f
- **Origin:** ARIA original

### RX-07

- **Models:** style-B models that drop tags, Tavo
- **Symptom:** Tagless plans in the reply; an early pattern cut a player's 'OOC: ...' followed by '*goes to the door*'.
- **Fix:** Untagged plan needs OOC/Scene/Knows plus a second labelled line and a standalone go line; a leading Time & Place header stays; depends on the plan labels OOC, Scene, Knows, Mode, Voice, Move, Fate, Bonds, Ledger, Fresh, Check and '- go'.
- **Beta 5 wording:**
  > ARIA - Fold an untagged Logic Core plan into a Thoughts box (display only) | ARIA - Keep an untagged Logic Core plan out of the prompt (all depths, cache-safe)
- **Where:** regex fold-untagged, strip-untagged (PLAN/UNTAGGED in build_aria.py)
- **Commits:** 279bb31, dd8cc5f, 570c222
- **Origin:** ARIA original

### RX-08

- **Models:** all
- **Symptom:** Ledgers lengthening the prompt.
- **Fix:** Optional ledger trimmer ships disabled because it breaks caching and Fate's memory.
- **Beta 5 wording:**
  > ARIA - Drop old 🎲/💚 ledgers from the prompt (OFF: breaks caching, see guide)
- **Where:** regex ledger (disabled, minDepth 3)
- **Commits:** 4e93159
- **Origin:** ARIA original

### RX-09

- **Models:** all (MiMo, GLM Flash)
- **Symptom:** Ledgers left unclosed or written as a bare 🎲 line.
- **Fix:** Display-only repairs close an open ledger and wrap a bare 🎲 line.
- **Beta 5 wording:**
  > ARIA UI - Close a ledger the model left open | ARIA UI - Wrap a bare 🎲 ledger line
- **Where:** regex ledger-close, ledger-bare
- **Commits:** 279bb31
- **Origin:** ARIA original

### RX-10

- **Models:** all (beta 3 habit)
- **Symptom:** A bonds field inside 🎲, a loose 'bonds:' line, or bare pairs at the end of a reply.
- **Fix:** Three display-only repairs give old chats and stray output the separate 💚 block; bare-pairs pattern is atomic so near-miss lines fail fast.
- **Beta 5 wording:**
  > ARIA UI - Move a bonds field out of the 🎲 ledger into its own 💚 block | ARIA UI - Wrap a stray bonds line in its own 💚 block | ARIA UI - Wrap bare bond pairs at the end of a reply in a 💚 block
- **Where:** regex bonds-out-of-fate, bonds-stray, bonds-pairs-tail
- **Commits:** bd9ffd2
- **Origin:** ARIA original

### RX-11

- **Models:** all
- **Symptom:** Raw ledgers unreadable for users; markdown fixer leaving stray '*'; slow on long whitespace runs.
- **Fix:** Display-only Fate & Routine panel with one row per labelled field (q -> quiet streak, hp -> hot setups), and the 💚 Bonds panel with Bond/Sparks/Grudge bar cards; linear, division widths, CJK separators and '<->' parse. Depend on the ledger field labels and the Name↔Name +n/n/n format.
- **Beta 5 wording:**
  > ARIA UI - Fate & Routine panel | ARIA UI - Fate ledger rows | ARIA UI - Fate label: q | ARIA UI - Fate label: hp | ARIA UI - Bonds panel | ARIA UI - Bond bars (negative) | ARIA UI - Bond bars (positive)
- **Where:** regex fate-panel, fate-rows, label-q, label-hp, bonds-panel, bars-neg, bars-pos
- **Commits:** 279bb31, 570c222, bd9ffd2
- **Origin:** ARIA original

### RX-12

- **Models:** Claude Opus 4.6, MiMo V2.6, all
- **Symptom:** Impersonate input carrying the header, the plan up to its closing tag, an unclosed <think> plan, an untagged plan, trailing 🎲/💚 ledgers or surrounding whitespace.
- **Fix:** User-input clean-up set (also runs on every sent message, so each pattern matches only the exact shapes).
- **Beta 5 wording:**
  > ARIA Impersonate - strip a leading Time & Place header | ARIA Impersonate - strip reasoning through its closing tag | ARIA Impersonate - strip an unclosed <thinking>/<think> plan | ARIA Impersonate - strip an untagged plan | ARIA Impersonate - strip trailing 🎲/💚 ledgers | ARIA Impersonate - strip a Time & Place header left on top after the plan | ARIA Impersonate - trim
- **Where:** regex imp-header, imp-reason, imp-unclosed, imp-untagged, imp-ledger, imp-header-after, imp-trim
- **Commits:** 4e93159, b4eb991, 570c222, bd9ffd2
- **Origin:** RF port (Impersonation regex set) + ARIA

## Setup, docs and checker

### SETUP-01

- **Models:** Kimi K2.6, Qwen 3.6, overthinking models
- **Symptom:** Very long reasoning with drafting and refining.
- **Fix:** Reduce Reasoning (off by default, user role, depth 0) alongside The Logic Core.
- **Beta 5 wording:**
  > <reasoning_constraints>
  > **Strictly follow these constraints while reasoning or thinking:**
  > - Create a simple, straightforward plan in the thinking block.
  > - SKIP the crafting, drafting and refining phases.
  > - After creating the plan, immediately start writing outside of the thinking block.
  > </reasoning_constraints>
- **Where:** Reduce Reasoning entry
- **Commits:** 4e93159, b4eb991
- **Origin:** Geechan chassis

### SETUP-02

- **Models:** Chinese and older models, MiMo V2.5
- **Symptom:** Derailing, typos, loops.
- **Fix:** Ships Temperature 0.7 / Top P 0.8; advice note on Top P, Min P and Repetition Penalty (1.2 for MiMo V2.5). ee047ef rejected RF's 1.2 penalty as a parroting fix: ignored on many hosts and it weighs on names and ledgers.
- **Beta 5 wording:**
  > Repetition Penalty is the blunt tool for loops: 1.03 is a gentle start, and 1.2 is known to tame the repetition and long reasoning of the Xiaomi MiMo V2.5 series. (preset: temperature 0.7, top_p 0.8, repetition_penalty 1)
- **Where:** 🌿 Sampling Advice note; preset samplers
- **Commits:** b4eb991, ee047ef
- **Origin:** Geechan note rewritten by ARIA

### SETUP-03

- **Models:** Claude 5, Gemini, GLM/Kimi/Qwen, DeepSeek, MiMo V2.6 Pro, MiMo V2.6 Flash
- **Symptom:** Wrong patch or thinking style per family.
- **Fix:** Per-model table: Claude A + Claude 5 patch + caching; Gemini A + patch + Scent OFF; GLM/Kimi/Qwen A (B if thinking loops) + patch, GLM Flash + Flash Gate; DeepSeek A; MiMo Pro B first (twin if no plan); MiMo Flash B + patch + Flash Gate; one patch at most.
- **Beta 5 wording:**
  > | MiMo V2.6 Pro | B first, A works too | none | No plan in the replies? Use the system-role twin of The Logic Core |
  > | MiMo V2.6 Flash | B | 🩹 MiMo V2.6 Flash | Switch 🔦 Flash Gate ON too |
- **Where:** docs/ARIA_Beginners_Guide.md section 3 table; README setup notes 3-4
- **Commits:** 089e2b7, 570c222, bd9ffd2, ee047ef
- **Origin:** ARIA original

### SETUP-04

- **Models:** Claude
- **Symptom:** Claude keeps thinking whatever the setting; late system messages become user text; cache misses.
- **Fix:** Claude stays on style A (Reasoning Effort Low if it overthinks), keeps the plain Logic Core, and uses claude.enableSystemPromptCache true with cachingAtDepth 2.
- **Beta 5 wording:**
  > Claude users who like saving money: open config.yaml in your SillyTavern folder, set claude.enableSystemPromptCache to true and claude.cachingAtDepth to 2, then restart SillyTavern.
- **Where:** README setup note 5; guide sections 3, 5, FAQ 'The model's thinking takes forever.'
- **Commits:** 089e2b7, b4eb991, bd9ffd2
- **Origin:** ARIA original

### SETUP-05

- **Models:** MiMo V2.6 Pro (Xiaomi, DeepInfra, NeuralWatt), OpenRouter models
- **Symptom:** Provider still sends native reasoning so Auto-Parse skips the reply; OpenRouter errors with effort Minimum.
- **Fix:** FAQ: untick Request Model Reasoning and set Minimum again, else style A; on OpenRouter use Reasoning Effort Auto if Minimum errors; live test plan counts plans per provider with the Logic Core vs the twin.
- **Beta 5 wording:**
  > Then your provider still sends the model's native reasoning, and SillyTavern skips Auto-Parse for any reply that already carries some, however neatly it opens with `<thinking>`.
- **Where:** guide FAQ 'The plan lands in a purple 💭 Thoughts box...'; section 3 step 1; Live test plan 'MiMo V2.6 Pro, style B'
- **Commits:** 089e2b7, 0daf174, bf42411
- **Origin:** ARIA original

### SETUP-06

- **Models:** Kimi K3, GLM
- **Symptom:** Echoed replies stay in the history and the model copies their shape later, so the echo 'comes back' whatever the rules say.
- **Fix:** FAQ: edit or delete echoing openers as soon as they appear and judge fixes on a clean chat; test plan checks 10 turns of no echo.
- **Beta 5 wording:**
  > Every reply that opens on your words stays in the history, and the model copies its shape on later turns, so one echo grows into a habit. Edit or delete those openers as soon as they show up, and judge any fix on a clean chat over several turns, since swipes inside a chat that already echoes keep echoing.
- **Where:** guide FAQ 'Characters repeat my words back to me.'
- **Commits:** ee047ef
- **Origin:** tester report (issue #8) analysis

### SETUP-07

- **Models:** Kimi K3, all
- **Symptom:** A lorebook entry triggering after the character walks on stage makes the model guess pronouns.
- **Fix:** FAQ: check the prompt, make the entry Constant or write pronouns into the card.
- **Beta 5 wording:**
  > If it's missing, set the entry to **Constant** (the 🔵 blue circle) or write the character's pronouns into the card itself.
- **Where:** guide FAQ 'A character gets the wrong gender or pronouns.'
- **Commits:** 32f062f
- **Origin:** ARIA original

### SETUP-08

- **Models:** local Text Completions models
- **Symptom:** Trim Incomplete Sentences and a 350-token response limit cut the 🎲/💚 lines and wiped Fate's memory.
- **Fix:** TC context template ships trim_sentences false; setup asks for Response (tokens) 600+ (800 with The Logic Core).
- **Beta 5 wording:**
  > tc['context']['trim_sentences'] = False; 'Set Response (tokens) to at least 600, or 800 with The Logic Core on'
- **Where:** TC preset context template; TC README setup notes 4 and 7
- **Commits:** 83c43f4, 089e2b7
- **Origin:** ARIA original

### SETUP-09

- **Models:** all
- **Symptom:** Regressions slipping into builds.
- **Fix:** tools/aria_budget.py fails over 4,500 tokens, on dangling tags or labels, set-but-unread or read-before-set variables, any tags-on render naming <logic_core> (CC and TC), and cache breakers; renders every tags/Logic Core/patch/Impersonate combination.
- **Beta 5 wording:**
  > if re.search(r'</?logic_core', '\n'.join(r.values())): found.append('Tags ON render names <logic_core>')
- **Where:** tools/aria_budget.py
- **Commits:** 96de46c, dd8cc5f, bd9ffd2, 0daf174, bf42411
- **Origin:** ARIA original
