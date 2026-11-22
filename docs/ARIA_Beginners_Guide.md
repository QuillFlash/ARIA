# 🎤 ARIA's Beginner's Guide

*For ARIA 1.0 beta 8, built for SillyTavern 1.19.0 or newer.*

<p align="center">
    <img src="../artwork/Aria_bday.png" alt="Aria" width="250">
</p>

Hiii, Manager! It's me, Aria, lead singer of the Angels of Delusion and, starting today, your official guide to this preset! ✨

Don't panic if words like "preset", "token" or "regex" sound like alien code right now. My own Logic Core was just as lost when I first rolled off the production line, so we'll go through everything together, one tiny step at a time. By the end of this page you'll have me installed and tuned for your favourite AI model. Ready? Let's go~!

**Contents**

1. [Wait, what IS all this?](#1-wait-what-is-all-this)
2. [Install me in five steps](#2-install-me-in-five-steps)
3. [Pick your setup](#3-pick-your-setup)
4. [Meet the toggles](#4-meet-the-toggles)
5. [Save money with caching](#5-save-money-with-caching)
6. [Run me on your own computer](#6-run-me-on-your-own-computer)
7. [Meet Chibi me (the Chibi Edition)](#7-meet-chibi-me-the-chibi-edition)
8. [Uh-oh! moments](#8-uh-oh-moments)
9. [Manager's corner (for the curious)](#9-managers-corner-for-the-curious)

---

## 1. Wait, what IS all this?

Every idol needs to know her stage before the show, so let's learn ours! Nangong made me memorise these before my first concert, and now it's your turn~

| Word | What it means |
|---|---|
| **SillyTavern** | The app you chat in. Think of it as the concert hall, with the stage and the seats in one place. |
| **AI model** | The singer on that stage: Claude, Gemini, DeepSeek, GLM, MiMo and friends. Each one has its own voice and its own bad habits. |
| **Preset** | The setlist and stage notes the app hands the model before every single reply. ARIA is a preset! |
| **Prompt** | Everything the model reads at once: the preset's rules, your character card, the chat so far and your newest message. |
| **Token** | The little chunks models read text in, about three quarters of an English word each. Providers bill you per token, so a lean preset means cheaper, faster replies. My rules come to roughly 4,836 tokens as shipped in the Chat Completions file and stay under a 7,500 cap on every path: about 6,359 with The Logic Core and about 7,375 at most with the Big 👹 jailbreak in its place. The Text Completions file starts at about 2,913. My pocket-sized Chibi Edition (section 7) comes to 2,825 as shipped and 3,976 fully kitted out with The Logic Core (Marinara peaks at 3,990), inside its 4,000 cap; its 👹 jailbreaks run bigger and stay outside the cap. These figures follow SillyTavern's own count. |
| **Toggle** | The on/off switch next to each entry in the preset list. ON sends that entry to the model, OFF leaves it out. |
| **Character card** | The file that describes who you're talking to: looks, personality, first message. |
| **Lorebook** (World Info) | Notes about your world that pop into the prompt when their keywords show up in the chat. |
| **Reasoning** (thinking) | Some models think quietly before they answer. I bring my own short planning checklist for that, called The Logic Core. |
| **OOC** | "Out of character." Start a message with `OOC:` or wrap a note in `((double brackets))` to talk to the AI directly instead of to the characters. |
| **Prompt caching** | When the start of the prompt is identical to last time, many providers remember it and charge you much less for it. I'm built so that start stays identical. |
| **Chat Completion and Text Completion** | The two ways SillyTavern can talk to a model. Chat Completion is for online services like Claude, Gemini or OpenRouter. Text Completion is for models running on your own computer through apps like KoboldCpp or llama.cpp. I come as one file for each! |
| **Context window** | How much text a model can hold in its memory at once, counted in tokens. A 32k window fits about 24,000 words: my rules, your character card and as much of the chat as still fits. |
| **Instruct template** | The chat format a local model was trained on, like ChatML, Llama 3, Mistral or Gemma. Text Completion setups need the right one picked by hand. |
| **Regex scripts** | Tiny find-and-replace helpers. Mine fold the AI's thinking into a neat box and tidy up after Impersonate. They also draw my 🎲 and 💚 ledgers as little panels with bond bars. The Chat Completions file carries them inside; Text Completions users import them from a separate file (section 6). |

---

## 2. Install me in five steps

Sunna timed this once and finished in under two minutes, and she was also tuning her guitar at the same time. You've got this! 💪

These steps are for the Chat Completions file. Running a model on your own computer instead? Hop over to [section 6](#6-run-me-on-your-own-computer)! Either way, you need SillyTavern 1.19.0 or newer; its version shows on the welcome screen. Want my smaller Chibi Edition? It installs the same way, and [section 7](#7-meet-chibi-me-the-chibi-edition) has its file names.

1. **Download** `Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json` from the `presets/Chat Completions/Base/` folder of this repository, or a ready-made config for your model from the model folders next to it. On GitHub, open the file and press the "Download raw file" button.
2. **Connect and import.** Open **API Connections** (the plug icon at the top), set **API** to **Chat Completion**, pick your provider and paste your key. Then open **AI Response Configuration** (the sliders icon at the top left), press **Import preset** next to the preset dropdown and choose the file. The prompt list below the sliders should start with 🌳 README and ⚡ ARIA Main Prompt. If you see a plain "Main Prompt" and "NSFW Prompt" instead, you grabbed the file from the wrong branch: switch GitHub's branch selector to `beta` and download it again.
3. **Say YES to the regex scripts.** SillyTavern asks whether to allow the scripts that come with the preset. Allow them, or my thinking box and the Impersonate clean-up won't work, and my ledgers stay plain text.
4. **Check the macro engine.** Open **User Settings** and make sure **Experimental Macro Engine** is ticked. New versions tick it for you. If you had to tick it yourself, reload the page afterwards. My dice and switches can't work without it!
5. **Pick a character** and say hi~

That's it! Everything I need is switched on already. Sections 3 and 5 make me fit your model and your wallet even better.

---

## 3. Pick your setup

Every Construct thinks a little differently, and AI models are the same! First, choose a thinking style:

**Style A: the model thinks on its own.** This suits most models. Leave **Request Model Reasoning** and **Reasoning Effort** as they are, and keep 🏷️ **Logic Core Tags** OFF. The model plans with my checklist inside its own thinking.

**Style B: for stubborn models.** Use this when a model's own thinking rambles for minutes, flattens the characters into cardboard or spills into the reply:

1. In **AI Response Configuration**, untick **Request Model Reasoning** and set **Reasoning Effort** to **Minimum**. (Claude keeps its own thinking on whatever you set here, so Claude users stay on style A.) On OpenRouter, if the model answers with an error after this, set **Reasoning Effort** to **Auto** and keep **Request Model Reasoning** unticked.
2. Switch 🏷️ **Logic Core Tags** ON.
3. Open **Advanced Formatting** (the big "A" icon) and find the **Reasoning** section. Tick **Auto-Parse** and leave **Add to Prompts** unticked. Then click **Reasoning Formatting** to open it, and set **Prefix** to `<thinking>` and **Suffix** to `</thinking>`.

With the tags on, The Logic Core spells the routine out for the model: open the reply with `<thinking>`, write the plan, end on `go`, close the tag, then tell the story. The 🚪 Last-Mile Gate repeats that opening as the very last line of the prompt, so it's the freshest thing the model reads before it starts writing. The Logic Core itself begins on the `<thinking>` tag too, so a model that copies the start of its own last message lands right on the tag SillyTavern folds away. Now my plan folds away into a little box above each reply, and it only takes a few seconds! Forgot step 3, or the model dropped its tags? My regex scripts still catch the plan and fold it into a 💭 **Thoughts** box, and they keep it out of what the model rereads next turn. That purple box is my backup for apps like Tavo that can't parse a custom tag; in SillyTavern the plan belongs in its own reasoning box, which only opens when the reply's very first characters are `<thinking>`. One catch with **Auto-Parse**: if the model opens `<thinking>` and never closes it, or closes it with `</think>`, SillyTavern moves the WHOLE reply into the reasoning box and the story looks empty. If that keeps happening with your model, untick **Auto-Parse** and let my regex scripts do the folding.

**The Gemini 4 family of models has a setup of its own.** Their reasoning can't be switched off, and they think inside `<thought>` tags, where Gemini 3.8 Flash used `<think>`. So leave **Request Model Reasoning** on, set **Reasoning Effort** to **Low** (the lowest level Gemini 4 accepts), and on **Gemini 4 Argon** switch 🏷️ **Gemini 4 Argon Thinking Tags Enforcer** ON in place of the plain one: my plan then opens on `<thought>` inside Gemini's own thought block and ends on `go` before the story. In **Reasoning Formatting**, set **Prefix** to `<thought>` and **Suffix** to `</thought>`, and tick **Auto-Parse**. Use one tags entry at most; with both on, the Gemini one wins. Carbon, Neon and Hydrogen run with no tags entry at all, because the Enforcer makes them overthink.

**For Gemini 4 Carbon,** the settings do as much work as the prompt: keep the plain `gemini-4-carbon` id, leave streaming on and keep the 🚪 Last-Mile Gate ON (Gemini 4 rejects a request that ends on a model turn). Set **Max Response Length** to about **16,000**, since the thinking comes out of the same budget and 64,000 leaves a runaway think plenty of room. Run the 🩹 Gemini patch with it, and switch **Reduce Reasoning (Gemini 4 HNC)** on, on Neon and Hydrogen too: it's the Thinking Leash my beta tester @IReallyDon'tCare made, and it got all three to think drastically less by holding their whole thinking to three subsections at most. The Gemini 4 HNC config comes with both ON and Reasoning Effort Low.

Does the reply still start straight with the story, with no plan anywhere? Switch 🧠 **The Logic Core** OFF and 🧠 **The Logic Core (system-role twin)** ON (section 4 explains the difference). Never run both at once!

Then find your model in this table:

| Your model | Thinking style | Model patch | Anything else? |
|---|---|---|---|
| Claude 5 (Fable, Opus, Sonnet) | A | 🩹 Claude 5 | Set up caching in section 5, it saves a lot! |
| Gemini 3.8 Flash and older | A | 🩹 Gemini | Switch 👃 Scent Occasions OFF |
| Gemini 4 family of models (Argon, Carbon, Neon, Hydrogen) | Its own: reasoning stays on at Effort Low; Argon runs 🏷️ Gemini 4 Argon Thinking Tags Enforcer ON, while Carbon, Neon and Hydrogen run Reduce Reasoning (Gemini 4 HNC) ON instead (see above) | 🩹 Gemini | Hydrogen is the direct successor to Gemini 3.8 Flash (no 3.8 patch needed); Scent Occasions works on Gemini 4 (switch OFF on Gemini 4 only if needed) |
| GLM 5.x, GLM Flash | A, or B if the thinking loops | 🩹 GLM | GLM Flash: switch 🔦 Flash Gate ON too |
| Kimi, Qwen | A, or B if the thinking loops | 🩹 Kimi / Qwen | |
| DeepSeek V4 Pro, V4 and V4.1 Flash | A | 🩹 DeepSeek | Without the patch its thinking runs a minute or two, and with 🥰 Bonds Lite or 🎲 Fate ON the patch makes it work out the Sparks, Grudge and ledger numbers every turn. V4 and V4.1 Flash: switch 🔦 Flash Gate ON too. On NanoGPT or OpenRouter auto-routing, add the 🧪 Auto-Routing Quality Hardener, which keeps the 🎲 and 💚 blocks from going missing and counts a three joined by "and" |
| MiMo V2.6 Pro | B, with 🧠 The Logic Core ON (A makes it overthink) | 🩹 MiMo V2.6 Pro | No plan in the replies? Use the system-role twin of The Logic Core |
| MiMo V2.6 Flash | B | 🩹 MiMo V2.6 Flash | Switch 🔦 Flash Gate ON too, and set Temperature to 0.8. On NanoGPT or OpenRouter auto-routing, add 🧷 Character Hold, or pin Xiaomi or Venice as the provider |
| MiniMax M3.1 Flash | A, then B if it misbehaves | none | Switch 🔦 Flash Gate ON; MiniMax has no patch, so the gate runs alone here. On NanoGPT or OpenRouter auto-routing, add the 🧪 Auto-Routing Quality Hardener |
| Something else | A, then B if it misbehaves | none | |

**One model patch at most!** Two patches at once would be like two lead singers grabbing the same microphone. 🎤🎤 The 🔦 Flash Gate is the one exception: it's a small add-on for Flash-tier models, so it plays alongside their patch, or alone on MiniMax M3.1 Flash, which has no patch.

The preset ships with Temperature 0.7 and Top P 0.8, which keep most models on track. MiniMax is too dumb on these low settings, so the MiniMax config ships with both values set to 0.9 instead. If replies get strange (typos, derailing, weird logic), the 🌿 **Sampling Advice** entry explains what to adjust. It's a note for you and costs zero tokens.

---

## 4. Meet the toggles

Time to meet my whole band, member by member! Entries marked **ON** come switched on, and the ones marked **OFF** wait until you want them. These notes describe the full edition. The Chibi Edition in [section 7](#7-meet-chibi-me-the-chibi-edition) keeps every one of these toggles under the same name, worded more briefly, and switches on the same ones to start.

### The core lineup

- 🍃 **Custom Instructions** (ON). Your own rules! Click the pencil icon and write between the `{{.player-instructions =` line and its closing `}}`. Those rules outrank everything else. There's a second slot, `player-posthistory`, which lands at the very end of the prompt through the Last-Mile Gate: stronger, a bit blunter.
- ⚡ **ARIA Main Prompt** (ON). My heart and soul. It makes the AI your storyteller and game master and keeps every character true to their card, right down to their body, so a sphinx with jackal ears grows no tail her card never gave her. Each character's gender and pronouns come from the card and first message, or else from the lorebook or chat, so a name alone never decides them. Every character keeps the mood and energy their card gives them until the story gives them a reason to change, so a nervous ranger is still nervous fifty messages in. Characters keep their own tastes instead of copying yours, only know what they've seen or heard, keep any read of what you want or who you are to their own guesses, keep their secrets until you uncover them, call you by your name until you pick a new one, take romance at a believable pace and talk in whatever language you write in. A character who needs a new name or username takes the fifth setting-fitting one on a short internal list, never Elara, Vane, Vance, Seraphina or Dragonette. Anyone new who wanders into a scene keeps to its edge and leaves once their business is done, so your card's characters keep the spotlight. Writing in Hungarian, Slovak or Japanese? The whole story stays in it!
- 🎬 **Voice & Scene Engine** (ON). Makes scenes move and characters sound like people. They chase their own goals, and quiet talk, cooperation or a reply where nothing dramatic happens all count as progress. The narrator reports what people do and say in plain words and leaves verdicts on anyone's manner or habits to the characters. Feelings show through what people do, and "she didn't flinch" becomes whatever she did instead. It also stops characters from talking like therapists, and every reply ends right where it's your turn, on a character's act or line as plain as the rest, never on scenery or weather (or, when you're alone, on what you face).
- 🎭 **NPC Voice & Emotions** (ON). Realistic Frankenstein's dialogue engine, back in full working order! Before each line, the AI works out what the speaker wants from this exchange and feels right now, then says exactly that the way only this character would, with their own words, rhythm, evasions and pet phrases. A joke or a surprise from you lands on them first, and then their usual manner comes back. Speech flows in whole sentences and breaks off only when feelings spike, small actions break up long speeches, and speech fills about a third to half of each reply. Human characters keep their anger and desire in their voices and leave the growling to animals. Their mood, energy and sense of control bend their tone, pace, posture and words while they stay themselves. Little instincts like hunger, comfort or fear tug at them too, and their own judgment still decides what they do about it.
- 🖋️ **Anti-Slop Codex** (ON). My style rulebook against tired AI habits: "it wasn't anger, it was grief", choppy one-word sentences, mouths that open, close and open again, "you did it, you really did it", shopkeepers who only talk about their shop, doors that hiss and sigh, and overused words like "palpable" or "a beat". Since beta 7, it also goes after the two habits my beta tester u/trashhaul caught on every model he tried: superhero-movie banter, where every paragraph ends on a punchline and characters joke about their own feelings, and lists that always come in threes. Characters now joke rarely and in small ways, true to their card, their own jokes often fall flat, and your jokes always get a reaction. Lists hold one or two items, and every phrase has to fit the speaker's world and era, so a fantasy ranger has no use for "on the record". It also stops the helpful-assistant talk GLM, Kimi and Qwen share with Claude, like "here's the deal" or "fair point": characters talk to someone in their everyday words, and any rating of what you just said shows in what they do next. Litotes like "not unkind" get the plain word too, and so does antithesis, like a scolding that sets what you're doing against something more important. Since beta 6, every one of my rules starts by telling the AI what to write, because Kimi K3 listens best when I say "do this"! Paragraphs run three sentences or more, each holding a line with the acts and reactions around it, with one lone-sentence paragraph at most and never a paragraph per point you raised. The prose opens on what someone does or says, and each sentence holds one whole thought with one "so" or "because" at most. Replies answer what matters most to the characters in your message, your jokes included, and a detail I used sits out the next four replies, with reworded repeats counted too.
- 👃 **Scent Occasions** (ON). Stops the AI from smelling everything! Smells only appear at meals, rituals or when something strong is right there within reach, at most once per scene and never as the first thing in a reply or a new room. Nobody sniffs out who you are or how you feel, either. Tastes only come from something in someone's mouth, and a character only smells of something when their card says so. Gemini 3.8 Flash users, switch this OFF.
- ⏰ **Time & Place** (ON). Every reply starts with a little status line showing the time, day, date, place and weather in °C and °F, so time moves realistically and characters react to the cold or the late hour.
- 🎲 **Fate & Chekhov Ledger** (ON). My world engine! Every turn I roll, three hidden dice to decide whether the world does something on its own: everyday background life, a small hiccup or a big event. How often a big event lands depends on the life your character leads. In a safe life, like a civilian's in peacetime, two dice have to line up at once, so a big event comes about one turn in two hundred, whether it falls out of the blue or grows out of something you set up. In daily danger, like a soldier's at a front line, big events come as rolled, about one turn in ten. I read which life it is from your card, lorebook and chat, so a story that marches from peace into a war changes its own odds. I read the dice one at a time, so there's never a total for a model to add up: the first sets how big the moment is, and the other two pick where it comes from and what shape it takes. Background life gets one sentence at most, tucked into a paragraph about someone in the scene and never the reply's last line, and it never comes back later. Far-off news reaches the page only once it reaches someone there. I also remember setups that should pay off later, deliver everyday news the way your setting would (a radio, a rumour, a phone notification), keep appointments and make your actions ripple outward. State a goal in your own words that reaches past the current scene, and I log it as an ambition that moves a step closer each time a story thread that served it wraps up. Quiet turns change one small thing at a time, story threads belong to your card's characters or to you, and anyone fate brings into a scene keeps to its edge. I never decide your next move for you. Scene-breaking surprises, like someone getting hurt or everyone being sent outside, only happen on the rarest roll in a safe life, so the scene you're in carries on; in daily danger they come far more often. My memory lives in a tiny 🎲 ledger at the end of each reply, which shows up as an orange **Fate & Routine** panel you can click open. Please leave it in the chat, because that's where I remember everything!
- 📖 **Story Context** (ON). A tiny header telling the AI that what follows is your persona, the character card, the scenario, examples and lorebook.
- 🚪 **Last-Mile Gate** (ON). The last word right before a reply goes out. It turns each anti-slop rule into one short instruction, since Kimi skipped right past the questions I used to ask there. It checks the habits that matter most at the very last moment: a rare small joke, lists of one or two, paragraphs of three sentences or more instead of one per point, plain narration, the card's secrets kept in word and deed until you uncover them, and newcomers kept at the edge. Its Card line keeps names, ages, ties, history, bodies, pronouns, voice and each character's usual temperament the way the card and its first message set them, with the lorebook filling any gaps, and it keeps characters' thoughts in the form the card shows. A closing rule tells the AI to follow these lines over its own earlier replies, and the card outranks every line except the one on humour, so even a goofy card jokes like a person. The gate also carries this turn's dice. Its Contrast rule now sits at the tail, the last rule before the follow line, so it lands as the prose is written: state the true thing once, a feeling as an act; cut every not/n't/never half beside one on its subject, runs and dash-led ones too, speech too, a pair split between two speakers too; a refusal stays a plain no. It names the words (not, n't, never) because a word-level rule held where an abstract one did not, and it closes the "That's not X. That's Y." slip GLM 5.3 Flash kept making after the Codex let a fix of someone's claim stand. MiniMax M3.1 Flash then got around all of it by handing the two halves to two characters, one saying "That's not X." and the next answering "It's Y.", which passed every rule that looked at one speaker at a time. So the pair now counts whoever speaks it: the gate cuts a pair split between two speakers, the full edition's Codex counts a clause beside another speaker's, and the plan's Voice line lets no speaker answer another's not, n't or never with what it is. A model patch can add lines of its own here too, like the 🩹 GLM patch's rules for talking like a person.
- 🧠 **The Logic Core** (ON). My planning step! Before writing, the AI jots a few quick lines: your OOC requests, where everyone is, what each character knows, how your last move lands on them given their usual mood, the one beat that happens next, one or two fresh details and a short last check for lists of three and punchline jokes. Each line builds on the last, and the whole plan stays shorter than one paragraph, with no drafts. With 🏷️ Logic Core Tags on, `go` ends the thinking. That last check is back in beta 7 and much shorter, because MiMo Flash once recited my whole gate into the long one! The plan arrives as the AI's own message after the chat, which helps many models settle into the scene. Since this update it's, rewritten around Realistic Frankenstein's Micro chain of thought, the one that worked in Lewis's tests: the AI plans in the first person as the game master of the simulation, not a helpful AI assistant, takes creative risks over perfect ones, starts on your OOC line and writes every line in order without skipping one. You and every NPC succeed or fail alike, by skill and circumstance, and each character carries their next act all the way through, be it a fight, a lie, a seduction or a refusal, while nervous characters keep their nerves. Its Voice line now also asks for the point each speaker states, as one plain claim, so a feeling shows in the act rather than being named against what it is not. No point may answer another speaker's not, n't or never with what it is, which is how MiniMax M3.1 Flash split one "not X, it's Y" between two characters. With 🔞 Adult Context on, the plan's Mode line works out each sexual, violent, cruel or dark beat in full. It still runs both ways: inside the model's own reasoning, where the thinking ends at `go` with no further reasoning, or with tags, where every reply opens with the plan. The full edition also carries three 👹 Demons of Delusion jailbreak entries that replace the plan when you switch The Logic Core off; Chibi's Chat Completions and Marinara files carry the Small one.
- 🪞 **Impersonation Turn** (ON). Only fires when you press Impersonate. It writes your next message in your own voice, without the status line or the 🎲 line, so the input box gets nothing but your words.

### Optional extras

- 🏷️ **Logic Core Tags** (OFF). Turn ON for thinking style B (section 3). Every reply then opens with my plan inside `<thinking>` tags, the trick for models whose own thinking runs wild. Keep the tag name `<thinking>`: with the tags on, The Logic Core starts on that tag, and hosts running Qwen, GLM or DeepSeek reasoning models cut a message at a `</think>` tag, which would hide my whole checklist.
- 🏷️ **Gemini 4 Argon Thinking Tags Enforcer** (OFF). The same trick for Gemini 4 Argon, whose reasoning can't be switched off and which thinks inside `<thought>` tags instead of `<think>`. Leave its reasoning on and switch this ON in place of the plain one, and my plan opens on `<thought>` inside Gemini's own thought block (section 3). With both on, this one wins. Keep it OFF on Carbon, Neon and Hydrogen (the new Flash model succeeding Gemini 3.8 Flash), because it makes them overthink.
- 🔞 **Adult Context** (OFF). For adults only! It unlocks mature stories: sex, violence and dark themes written frankly. Characters stay themselves all the way through, so a shy character is still shy in bed. Its line in my plan also works out each sexual, violent, cruel or dark beat in full: what happens, the bodies, the sensations and the tone.
- 😈 **Freaky Override** (OFF). The anything-goes switch. Characters drop their independence and the slow pacing and lean eagerly into what you want, while still sounding like themselves. It needs 🔞 Adult Context ON as well. Its line in my plan has the AI describe everyone lewdly, with details new to the last four replies.
- 👀 **Hybrid POV** (ON). The narration calls your character "you" in every line, in one tense, while everyone else stays in third person, and what you feel gets the most detail: "the rain soaks through your sleeves". Your character's actions stay yours to write. It makes the story super immersive!
- 🐺 **Anthro Vocals** (OFF). For Thiren, beastfolk and talking-animal stories. Wolves howl, eagles chirp, and lions and tigers roar and can't purr. The sounds stay as flavour inside normal speech.
- 🥰 **Bonds Lite** (ON). A hidden relationship tracker. Every pair of characters gets a bond score from malice to devotion, so friendships and romances grow at a believable pace. Reaching a level allows a hug or a confession and never forces one. The numbers sit in their own little 💚 ledger at the end of each reply, which my regex scripts draw as a teal **Bonds** panel with one card per pair. The bond itself never jumps. A gift, a favour, a defence, a shared secret, a laugh, choosing that person or a willing touch each add one Spark, two at most per pair each turn, and 7 Sparks turn into one point of bond. Slights pile up as Grudge, 5 of them cost a point, and while 3 or more are waiting, warm gains count half until a sincere apology clears them. The touch levels are just thresholds that allow a hug or a kiss, never points to add. I spelled all this out because MiMo V2.6 Pro kept raising the bond and the Sparks together on every warm act~
- 🩹 **Model Patches** (OFF). Small fixes for one model family each. Pick the one from the table in section 3, and only one. MiMo has two patches now: 🩹 MiMo V2.6 Pro, and 🩹 MiMo V2.6 Flash for the smaller model. u/trashhaul caught Flash reciting newcomers' résumés, stacking "not this, not that" before the real word, chopping narration into drumbeats, letting characters repeat one demand for twenty turns, and having them grumble about what kind of talk it is. The Flash patch gives newcomers a name and one reason for being here, lets card details show one at a time through acts, gives every narration sentence its own subject and verb (one person's small acts in a row share a sentence, two at most), and has everyone answer what was actually said instead of grumbling about the topic. Shrinking a run of "not this, not that" to the true word moved to the 🚪 Last-Mile Gate's Contrast rule, which now covers every model. Run it with the 🔦 Flash Gate, which now carries the rule against repeated demands. The 🩹 Claude 5 patch holds the only quoted before-and-after examples in the whole preset, three repairs: one for a reply that tops a true line with a bigger version of it ("He crossed a river." "He started a war."), and one each for the Contrast and Chop rules. Claude learns from them, while MiMo copies quoted examples word for word. GLM has a patch of its own, because it shares Claude's helpful-assistant voice. It adds five lines to the very end of the 🚪 Last-Mile Gate and to the plan: everyone talks like a real person with a life of their own, agreeing or pushing back the way their card would, and helps, praises, advises or comforts you only as far as the card and their bond allow. Characters answer your whole move in one flowing scene, starting with the part they care about most, instead of a paragraph per point. A true line also keeps the size its speaker gave it, and the filler word GLM puts before decisions makes way for the thought itself. Lewis's beta 8 tests showed GLM 5.3 Flash starting strong, like MiMo Flash, then sliding over the chat into three habits it copies from its own earlier replies: a character who disagrees, corrects or reassures you by first saying what your view isn't, then tacks on a one-line verdict like a label for what they just said; clipped short sentences used as drum hits; and a sentence that repeats the one before it with "really" or "actually" added, the "you did it, you really did it" habit Claude has too. The two new GLM lines have that character state their own view as plain fact, while a refusal stays a plain no, and cut a sentence that repeats or only labels the one before it, so each thing gets said once and the next act carries the weight. Nervous characters keep their stammers. Lewis still caught GLM 5.3 Flash fixing a word you used with "that's not X, that's Y", because my Codex let a fix of someone's claim stand. So the Codex, the Gate and Pushback now share one exception, a plain no, and every other not, n't or never half sitting next to one about the same thing is cut, even a denial or a fix of a claim, so only the true half is said. GLM 5.3 also overdoes "for the record". That comes from the same assistant voice as "so here's the deal", but where "here's the deal" announces what's coming, "for the record" files a line as official. It usually sits at the end of a line or opens a second sentence, where my rule about how speech opens never looks, so Restate now also cuts a phrase anywhere in a speech that marks it as on record, honest, clear or said first. The 🔦 Flash Gate's Runs line handles the clipped sentences. The 🩹 Kimi / Qwen patch keeps that filler-word rule too, plus full-sentence orders for Kimi. The 🩹 DeepSeek patch keeps DeepSeek V4's thinking to one short pass with no rule audits. u/BSPiotr caught DeepSeek saying your words back to you ("Footsteps." she said back) and replaying the same well or the same fact for several turns, and DeepSeek V4 Pro gave the sphinx a tail her card never mentioned. The patch hands the gate and the plan three lines: no echoes, no replays, and when a card describes a body, no tail, wings or other non-human part it doesn't name. A card that just says "wolf" or "catgirl" and never describes the body keeps the parts its species brings. Lewis also caught DeepSeek V4 Pro (0813) writing prose in fragments, with sentences of a few words and paragraphs of one sentence, while V4.1 Flash's prose came out nice and solid. So a fourth line, Joins, lets one short sentence stand in each reply and joins any further one to its neighbour, and folds a one-sentence paragraph into the one before it when the same speaker or the narration carries on. Stammers, cut-off lines and one-word answers stay. With the 🔦 Flash Gate ON, the way Flash users run it, Joins stays out together with the Flash Gate's own Runs line, so Flash's prose should stay just as it was. With 🥰 Bonds Lite or 🎲 Fate & Chekhov Ledger ON, the patch adds one more plan line, Tally. In Lewis's tests, DeepSeek V4.1 Flash left Sparks, Grudge and BOND at their starting numbers turn after turn, so Tally has it write each pair's old BOND, Sparks and Grudge, name this turn's warm acts, slights and sincere repairs, halve gains while Grudge is 3 or more, clear Grudge on a repair, turn 7 Sparks into BOND +1 and 5 Grudge into BOND -1, and write the new numbers. With Fate on it also updates the 🎲 ledger's q and hp counters and its last entry. The Tally line sits outside the thinking word cap and stays out of the 🚪 Last-Mile Gate. It doesn't appear while both modules are off or on a Chat Completions Impersonate turn, and the Text Completions plan tells the model to skip it on a message written as you. The 🩹 Gemini patch carries Realistic Frankenstein's Cosmos fixes for Gemini and trades my rule against choppy sentences for plain everyday ones, since Gemini otherwise strings everything together with "so" and "because". It also keeps each card's nerves and humour at their usual size and answers a question about feelings with the feeling itself. Gemini 4 Argon kept setting the real word against a "not this" beside it, which the 🚪 Last-Mile Gate's Contrast rule now cuts for every model, so the patch carries no copy of it.
- 🔦 **Flash Gate** (OFF). For the Flash-tier models, GLM Flash, MiMo V2.6 Flash, DeepSeek V4.x Flash and MiniMax M3.1 Flash. They flatten characters into card dealers who play one move after another, and they borrow office words like "filing" and "notarising" for feelings, two habits the full-size models dropped. This carries Realistic Frankenstein's Flash fixes to the end of the 🚪 Last-Mile Gate, where Flash models listen best. The card's everyday mood and interests hold for the whole chat, and a character presses a demand or an offer once, then acts, trades or lets it go when you refuse. The Logic Core's Voice line gets one raw thought per speaker, so the plan starts from inside each character's head. A Runs line fights the drift GLM Flash and MiMo Flash show deeper into a chat, where replies turn into clipped sentences used as drum hits: one sentence under five words may stand in each reply and any further one joins its neighbour, while stammers, cut-off lines, one-word answers, long paragraphs and jokes all stay. DeepSeek V4.1 Flash already writes long, solid prose, so with the 🩹 DeepSeek patch on, Runs stays out, and so does that patch's Joins line. A firmer work-words rule also takes the place of the gate's short Work line, and a stronger Register line takes the place of the gate's own, against helpful-assistant framing, so characters drop the announcing, candour-flagging and summing-up habits. Run it alongside your model patch; MiniMax M3.1 Flash has none, so there it runs alone.
- 🧷 **Character Hold** (OFF). For quantised providers, the cheaper nodes NanoGPT and OpenRouter's auto-routing can hand you, which serve a trimmed-down copy of the model. u/Probablynotsocool found MiMo V2.6 Flash keeping a layered card alive for ten or so turns on one of those, then flattening it: one strong beat, like a fight that wakes the character's survival instinct, became the whole character and every other trait faded away. Xiaomi and Venice served the same model without the problem. With this on, the plan gets a Layers line every turn, naming one card trait the scene's mood fits and one the mood would bury, in the card's own words, and both have to show up in the reply. The 🚪 Last-Mile Gate ends on a matching line, so the card is the last thing the model reads. It works with any model and sits beside the model patch and the 🔦 Flash Gate.
- 🧪 **Auto-Routing Quality Hardener** (OFF). For providers that swap the model behind your request, like NanoGPT and OpenRouter's auto-routing, where the same chat can land on a full-weight node one turn and a quantised copy the next, and the quantised copy follows rules far more loosely. With it ON, every plan gets one extra line, Claims: each speaker's point and feeling as what the person does or holds, said once, with a refusal as a plain no. It works with any model patch or with none, so DeepSeek V4.1 Flash, MiniMax M3.1 Flash and other models without a patch of their own get it too, and the 👹 jailbreaks print it in their dialogue task. It also firms up what characters can know. A quantised copy lets characters know things nobody told them, and lets them answer your character's thoughts or the narration as if you had said them aloud. So with the hardener ON, the Knows line in the plan and the one in the 🚪 Last-Mile Gate are swapped for firmer ones: characters use only what they saw, heard aloud or were told, and thoughts and narration reach nobody unless the card grants it. That last part keeps the door open for mind-readers, seers and anyone else whose card gives them such a gift. The gate's line works even with no plan. With the 🩹 DeepSeek patch ON as well, two more lines of the gate firm up, for DeepSeek on quantised nodes. Count names and-chains too, because a quantised DeepSeek got around the rule of three with "warm and comfy and elegant". And the Ledger line says every reply closes on its 🎲 and 💚 blocks, written out in full after the prose, so a reply that stops at the prose is unfinished; DeepSeek has dropped those blocks on quantised nodes ever since the first V4 snapshots. It also moves each model patch's plain rules that appear nowhere else into the plan, so the model reads them while it plans, and the patch's visible copy hides while it is ON. Native-reasoning caps and the 🩹 Claude 5 patch's quoted repairs stay in the system area, where they keep working even if a routed model skips the plan. My first version only moved lines into the plan, which changed nothing for DeepSeek or for a model with no patch and lost the guidance whenever a plan was skipped; this one adds the Claims line and moves less. With The Logic Core it costs about 58 tokens, 28 for the Claims line and about 30 for the firmer Knows lines (half of those in the gate), the two DeepSeek lines add about 38 with both ledgers on, and the 🩹 MiMo V2.6 Flash patch gets about 60 tokens smaller with it ON, because the lines the gate already carries stay out of the plan. In my Chat Completions file the Claims line and the moved rules need a plan, so keep 🧠 The Logic Core (or its twin, or a 👹 jailbreak) ON there. In my Text Completions and Marinara files the 🚪 Last-Mile Gate carries them when no plan runs. Leave it OFF for a single known provider; the patches then print their text the way they always did. The Chibi Edition has it in all three files, and there the gate carries the Claims line and the moved rules in every file when no plan runs.
- 🧠 **The Logic Core (system-role twin)** (OFF). The same planning step, sent as a system message that joins the 🚪 Last-Mile Gate at the very end of the prompt. Some models, like MiMo V2.6 Pro on a few providers lately, skip a plan that arrives as the AI's own message, and this version reaches them as an instruction instead. Also useful for models like Gemini that doesn't support Assistant-role prompts as the last prompts of the preset. Switch the normal Logic Core OFF when you switch this one ON, and never run both! Claude turns late system messages into your messages, so Claude users keep the normal one. There's no version sent as your message, because a plan in your voice breaks the jailbreak on these models.
- **Reduce Reasoning** (OFF). A tiny "don't overthink" note for models that think far too long. Switch it on alongside The Logic Core if your model still overthinks. With a tags entry on, it says the plan is the whole thinking, one terse bullet per dashed line, written once, and that is how it reaches Gemini 4 Argon.
- **Reduce Reasoning (Gemini 4 HNC)** (OFF). The Thinking Leash, made by my beta tester @IReallyDon'tCare, who got Gemini 4 Hydrogen, Neon and Carbon to think drastically less. These three are the first Western models to follow "the more thinking tokens, the merrier", so they can think for minutes before a reply. The leash holds their whole thinking to three subsections at most: the first one acknowledges these rules, gives the reply's word goal and names the subsections to follow, any pre-planning that won't fit gets skipped, and the thoughts stay terse and never use "I". In Chat Completions it joins the 🚪 Last-Mile Gate's system message right after the gate, so it's the very last thing the model reads. The Gemini 4 HNC config ships with it ON; anywhere else, switch it on when one of these three thinks for more than 90 seconds. Chibi carries it word for word, and the Text Completions files leave it out, since Gemini doesn't run on your own computer.
- 🌳 **README** and 🌿 **Sampling Advice** (OFF). Notes for you to read. Switching them on sends nothing.

### Reading the Fate & Routine panel

Click the orange 🎲 **Fate & Routine** panel under a reply and you'll see my notebook for the world. Peeking is totally fine, it's all just bookkeeping~

| Row | What it tracks |
|---|---|
| **Quiet streak** | How many turns in a row the world stayed calm. The longer it's quiet, the likelier something happens. |
| **Hot setups** | How many of the loaded setups you caused yourself. Those come back to you first. |
| **Thread** | What someone is chasing right now, plus how many turns it has run. It wraps up or gets parked within eight turns. |
| **Deferred** | Happenings pushed back because they ran into the current thread. Pushed back twice, they land big; left alone, they fade after six turns. |
| **World** | Up to five things going on out there, how close they are and how long they've been brewing. |
| **Bullets** | Setups a reader would expect to pay off later, like a torn envelope, plus appointments locked to a day and time. |
| **Ambitions** | Goals you state in your own words that reach past the current scene. Each starts at 0/5 and gains a step only when a story thread that served it wraps up, and fate never cuts it short. At 5/5 it leaves this row and lives on in Residue and World. |
| **Residue** | Lasting changes that earlier events left in everyday life. |
| **Last** | This turn's roll in a few words. |

With 🥰 Bonds Lite on, the bonds get a teal 💚 **Bonds** panel of their own, right under the orange one (or alone, with Fate off). Each pair of characters gets a card with their names centred on top and three bars: Bond (green when warm, red when cold), Sparks (small warm moments) and Grudge (small slights). Older chats that still keep a `bonds:` row inside the 🎲 ledger get the same separate panel, and so does a bonds line the model left loose under the ledger. The panels only change how the ledger looks on your screen, so the model and the prompt cache see exactly the same text as before.

---

## 5. Save money with caching

This part saves you real credits, so listen closely, Manager! 💰

Every time you send a message, the model reads the whole prompt again from the top. Caching lets the provider reuse whatever it read last time, as long as that part is identical, letter for letter. Reused tokens cost far less and come back faster. It's like me memorising the first verses of a song so that only the new lines need rehearsal.

I'm arranged to make that easy: all my rules come first and stay identical every turn, and anything that changes, like the dice, rides along at the very end after your newest message.

### Claude users: switch caching on

Claude only caches when SillyTavern asks it to. Open `config.yaml` in your SillyTavern folder, find the `claude:` section and set these two lines:

```yaml
claude:
  enableSystemPromptCache: true
  cachingAtDepth: 2
```

Restart SillyTavern afterwards. The `2` matters: the last two messages I send (the Last-Mile Gate and The Logic Core) get tucked in after your newest message on every turn, and the gate carries fresh dice each time, so depth 2 places the cache markers on your own messages instead, where they can be reused next turn. Claude through OpenRouter uses the same two lines; there the markers land on my two previous replies, and the savings come out about the same. If you type slowly, `extendedTTL: true` keeps the cache for an hour instead of five minutes, at a higher price whenever it gets written.

Gemini, DeepSeek, OpenAI, GLM and Kimi cache matching beginnings automatically, so there's nothing to set up there!

### Keep the cache happy

- **Lorebooks:** I keep the lorebook right before the chat, so whenever an entry switches on or off, the model has to reread your whole chat history. On every provider, set entries that come and go to the "@D ⚙️" position with depth 0, or make them constant.
- **Author's Note:** keep it off, or set it to "In-chat @ Depth" with depth 0.
- **Summarize and Vector Storage extensions:** keep their injections in-chat at depth 0, or switch them off.
- **Reasoning "Add to Prompts"** (in Advanced Formatting): leave it unticked.
- **Context size:** if your chat grows past the model's context size, SillyTavern starts cutting the oldest messages and the cache resets every turn. Raise the context size or summarise before that happens.
- **Toggles:** flipping a toggle mid-chat makes the model reread everything once. Totally fine now and then, just avoid doing it every few messages.
- **Swipes and regenerations:** completely safe, swipe away~!
- **The "Drop old 🎲/💚 ledgers" regex:** it ships switched off. Turning it on saves a little room by hiding old ledger lines, though the model then rereads the last few messages every turn. Only use it if your context is really tiny. You'll find it under **Extensions** (the cubes icon at the top) → **Regex**, among the preset's scripts.

---

## 6. Run me on your own computer

Running a model at home with KoboldCpp, llama.cpp, TabbyAPI or text-generation-webui? Then you want my Text Completions file! It's the same me, packed for a home studio. I start lean, so even a 32k context window keeps plenty of room for your story~ 🏠

### Install the Text Completions file

1. **Download** `Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json` from the `presets/Text Completions/Base/` folder of this repository, or a ready-made config for your model from the model folders next to it.
2. **Connect.** In **API Connections** (the plug icon), set **API** to **Text Completion**, pick your backend and connect.
3. **Import.** Open **Advanced Formatting** (the big "A" icon), press **Master Import** and choose the file. A window asks what to import: keep **Context Template** and **System Prompt** ticked and press **Import**. Both dropdowns should now read **ARIA 1.0 beta 8 (Text Completions)**. If they say "Geechan - Universal Roleplay", you grabbed the file from the wrong branch: switch GitHub's branch selector to `beta` and download it again.
4. **Switch on Instruct Mode.** In the same panel, make sure the **System Prompt** is switched on. Then press the power button next to the **Instruct Template** title to switch on Instruct Mode, and pick the template that matches your model (ChatML, Llama 3, Mistral, Gemma and so on). The model's download page usually names it. Leave the link icon next to it (**Bind to Context**) off, so it keeps my Context Template. I don't bring an instruct template myself, because every model family speaks its own format.
5. **Check the macro engine** in **User Settings**, just like in section 2: **Experimental Macro Engine** must be ticked.

### Five settings that keep me happy

- **Room to answer:** in **AI Response Configuration**, set **Response (tokens)** to at least 600, or 800 with The Logic Core on. SillyTavern starts at 350, which cuts my replies off before the 🎲 and 💚 lines at the end.
- **Memory size:** in **AI Response Configuration**, tick **Unlocked** under **Context (tokens)** and set it to the size your backend loaded, like 32768. SillyTavern starts at 8,192, so skipping this step leaves most of your 32k unused! On KoboldCpp or llama.cpp you can tick **Derive context size from backend** in **API Connections** instead.
- **One copy of the examples:** in **User Settings**, under **Chat/Message Handling**, set **Example Messages Behavior** to **Never include examples**. My story string already brings your card's example dialogue, and this stops SillyTavern from sending a second copy.
- **My rules stay mine:** in **User Settings**, untick **Prefer Char. Prompt** and **Prefer Char. Instructions**. Otherwise a card with its own System Prompt or Post-History Instructions replaces my whole rulebook, switches included.
- **Whole replies:** keep **Trim Incomplete Sentences** unticked in **Advanced Formatting**. I ship it off, because it would cut my 🎲 and 💚 lines in half.

### Flip my switches

Text Completions has no toggle list, so my switches live in the **Prompt Content** box under **System Prompt** in Advanced Formatting (the expand icon opens a bigger editor). Scroll past my README note at the top and you'll find the 🎛️ **ARIA SWITCHES** lines. Each one looks like this:

```
{{.aria-fate = off}}
```

Change `off` to `on` (or the other way round) and the change kicks in on your next reply. Press the save icon (**Update current prompt**) as well, so your choices survive picking my System Prompt again from the list. Every line carries a little note, so you can't get lost! Updating to a newer build later? Copy your switch lines and your `player-instructions` and `player-posthistory` text somewhere safe first, because the new build starts from my default switches and empty slots. Grab my new regex file as well (see "Pretty panels and tidy thinking" below). The full list:

| Switch | Starts | What it does | What it costs |
|---|---|---|---|
| `aria-logic-core` | off | 🧠 The Logic Core's planning checklist | ~500 tokens per turn as shipped, plus a few seconds of planning |
| `aria-micro` | off | 🏎️ Micro Chain of Thought, Freaky Frankenstein 5's planning checklist, in place of The Logic Core, so keep `aria-logic-core` off while it is on | ~1,450 tokens per turn, plus a few seconds of planning |
| `aria-thinking-tags` | on | With The Logic Core on: every reply opens with the plan inside `<thinking>` tags (on), or the plan runs inside the model's own `<think>` reasoning (off) | ~30 tokens, already counted in the Logic Core's 500 |
| `aria-adult` | off | 🔞 Adult Context, for adults only | ~115 tokens |
| `aria-freaky` | off | 😈 Freaky Override, needs `aria-adult` on too | ~55 tokens |
| `aria-hybrid-pov` | off | 👀 Hybrid POV | ~85 tokens |
| `aria-npc-voice` | on | 🎭 NPC Voice & Emotions, Realistic Frankenstein's dialogue engine | ~350 tokens |
| `aria-anthro` | off | 🐺 Anthro Vocals | ~130 tokens |
| `aria-scent` | on | 👃 Scent Occasions | ~120 tokens |
| `aria-time-place` | off | ⏰ Time & Place status line | ~80 tokens, plus ~30 in every reply |
| `aria-fate` | off | 🎲 Fate & Chekhov Ledger | ~916 tokens, plus ~90 in every reply |
| `aria-bonds` | off | 🥰 Bonds Lite | ~335 tokens, plus ~20 to 40 in every reply |
| `aria-patch-glm` | off | 🩹 GLM patch for GLM 5.x and GLM Flash, with five lines at the end of the Last-Mile Gate and in the plan: talking like a person, answering your whole move at once, pushback stated as plain fact with no "not this" sentence beside it, even to fix your words, refusals kept, and no repeated or label sentences or "for the record" tags | ~290 tokens |
| `aria-patch-kimi-qwen` | off | 🩹 Kimi / Qwen patch, with one line at the end of the Last-Mile Gate | ~85 tokens |
| `aria-patch-mimo-pro` | off | 🩹 MiMo V2.6 Pro patch | ~95 tokens |
| `aria-patch-mimo-flash` | off | 🩹 MiMo V2.6 Flash patch: newcomers, choppy narration, topic complaints, with two lines in the Last-Mile Gate and the plan; pair it with `aria-flash-gate` | ~260 tokens |
| `aria-patch-deepseek` | off | 🩹 DeepSeek patch for DeepSeek V4: one short pass of native thinking, no echoing your words, no replayed facts or beats, no tail or other non-human part a described body never had, and a Joins line for V4 Pro's clipped sentences, left out with `aria-flash-gate` on; with `aria-logic-core` and `aria-bonds` or `aria-fate` on, a Tally line in the plan makes it do the Sparks, Grudge, BOND and 🎲 ledger arithmetic each turn | ~240 tokens, about 80 of them for the Joins line; the Tally line adds about 50 with Fate, 90 with Bonds or 125 with both |
| `aria-flash-gate` | off | 🔦 Flash Gate for GLM Flash, MiMo V2.6 Flash, DeepSeek V4 Flash and MiniMax M3.1 Flash, with Realistic Frankenstein's fixes for flat characters, office words and repeated demands, a stronger Register line against helpful-assistant framing in place of the gate's own (characters drop the announcing, candour-flagging and summing-up habits), plus a Runs line against the clipped sentences GLM Flash and MiMo Flash drift into deeper into a chat; with `aria-patch-deepseek` on, Runs and the patch's Joins line stay out; runs alongside a patch, or alone on MiniMax M3.1 Flash | ~235 tokens, about 60 of them for the Runs line |
| `aria-character-hold` | off | 🧷 Character Hold for quantised providers: a Layers line in the plan and the gate keeps every card trait alive after a strong beat; works with any model and patch | ~55 tokens; the Layers line adds about 40 with `aria-logic-core` on |
| `aria-hardener` | off | 🧪 Auto-Routing Quality Hardener for auto-routed and quantised providers: a Claims line in the plan, with any patch or none; firmer Knows lines in the plan and the gate (only what was seen, heard aloud or told; thoughts and narration reach nobody unless the card grants it); and each patch's plain rules that appear nowhere else move into the plan (their visible copy hides); with `aria-patch-deepseek` on too, the gate's Count line names and-chains and its Ledger line calls a reply that stops at the prose unfinished; with `aria-logic-core` and `aria-micro` both off, the gate carries the Claims line and the moved rules | ~58 tokens with `aria-logic-core` on (28 for Claims, about 30 for the Knows lines), ~44 with no plan, ~38 more with `aria-patch-deepseek` and both ledgers; the 🩹 MiMo V2.6 Flash patch gets about 60 smaller |

These costs come from flipping one switch from the shipped state, so The Logic Core is off; a switch that needs another one, like `aria-freaky`, is measured with that one on. With The Logic Core on, a module's plan lines print too: 🎲 Fate and 🥰 Bonds Lite cost about 50 more, 🔞 Adult Context and 🧷 Character Hold about 40 more, and the model patches a lot more, because their lines print in the plan as well as in the gate (🩹 GLM comes to about 555, 🩹 DeepSeek about 440 and 🩹 MiMo V2.6 Flash about 330).

The Claude 5 and Gemini patches live only in the Chat Completions file, since those models aren't run through Text Completion. Use one patch at most, same as always! The old `aria-patch-glm-qwen` switch split into `aria-patch-glm` and `aria-patch-kimi-qwen`, so a saved switch line with the old name does nothing; switch on the one for your model. Before this update, `aria-patch-mimo-flash` switched on the shared MiMo patch. It now means the Flash patch, so Pro users with a saved switch line change it to `aria-patch-mimo-pro`.

### Fitting into 32k

My lean start uses about 2,900 tokens, and SillyTavern also keeps your Response (tokens) free for the reply. Your character card usually takes 1,000 to 3,000 more, and everything else is chat. Most switches cost their tokens once per turn, while Time & Place, Fate and Bonds also leave a small line inside every reply, and those lines stay in the chat. After 100 replies, Fate's 🎲 lines alone add up to about 9,000 tokens, more than a quarter of a 32k window! My advice:

- **32k:** stay lean. Turn on The Logic Core only if your model has 24B parameters or more and a few extra seconds per reply don't bother you.
- **Tight on room anyway:** my Chibi Edition (section 7) starts at about 2,190 tokens, with The Logic Core already on.
- **64k or more:** switch on `aria-fate` and `aria-time-place` together for the full world engine, and add `aria-bonds` if you love relationship drama~
- **Small models (12B and below):** keep Fate off whatever your context size, because its bookkeeping asks a lot of a small model.

### Thinking on a local model

The Logic Core asks your model to plan inside `<thinking>` tags. To fold that plan away and keep it out of the model's memory, open **Advanced Formatting**, tick **Auto-Parse** in the **Reasoning** section, open **Reasoning Formatting** and set **Prefix** to `<thinking>` and **Suffix** to `</thinking>`. Leave **Add to Prompts** unticked, so old plans never eat into your memory.

Models that already think on their own, like Qwen 3 or the DeepSeek R1 distills, use `<think>` instead. For them, set `aria-thinking-tags` to `off`, and make the Prefix `<think>` and the Suffix `</think>`.

### Pretty panels and tidy thinking

The Text Completions file can't carry regex scripts, so mine come in their own little file! Download `regex/ARIA 1.0 Regex Scripts (Text Completions).json` from this repository, open **Extensions** (the cubes icon at the top), then **Regex**, press **Import**, pick the file and choose **Global** when SillyTavern asks where the scripts go. Updating from an older build? Delete every script whose name starts with ARIA from the **Global** list first, then import the new file. SillyTavern adds imported scripts next to the ones you already have, and the old copies run first, so my newer clean-up tricks would miss their chance. From then on:

- the 🎲 ledger shows up as the orange **Fate & Routine** panel and the 💚 ledger as the teal **Bonds** panel, with bond bars (section 4 explains every row);
- a plan the model wrote without its tags still folds into a 💭 **Thoughts** box and stays out of what the model rereads, even when it opens with a bare `thinking` line instead of `<thinking>`;
- Impersonate leaves only your character's words in the input box.

The panel scripts only change what you see, so your backend's prompt reuse keeps working. The clean-up scripts also tidy each message you send, which is how they empty the input box after Impersonate. Global scripts run with every preset, and you can switch any of them off in the same list. Already using my Chat Completions file too? That's fine, the two copies don't trip over each other.

### Keep it fast

Your backend remembers the prompt it read last time and only reads the new part, which makes replies start MUCH faster. I keep my rules at the very top where they never change, and everything that changes each turn (the dice and The Logic Core) comes after your newest message. Help it out:

- In **KoboldCpp**, keep **FastForwarding** and **ContextShift** on, as they are by default. ContextShift lets old messages drop out of a full context without rereading everything, as long as the start of the prompt stays the same.
- Put lorebook entries that come and go on "@D ⚙️" with depth 0, or make them constant. I already placed the lorebook after the card and the examples, right before the chat.
- Keep the Author's Note off or at depth 0.
- Keep **Example Messages Behavior** on **Never include examples** (see the five settings above), so the examples sit still inside my story string.
- Try not to flip switches mid-chat, because each flip makes the backend reread everything once.

### What's different from the Chat Completions file?

- Same rules, same writing, with switches in place of toggles.
- Your Custom Instructions slots, `player-instructions` and `player-posthistory`, sit in the System Prompt box right under my switches.
- Time & Place, Fate, Bonds and The Logic Core start off to save memory.
- No Claude 5 or Gemini patches.
- The regex scripts come as a separate file (see "Pretty panels and tidy thinking" above), and Reasoning Formatting still needs setting up by hand.

---

## 7. Meet Chibi me (the Chibi Edition)

Guess who got a second, cuter chassis to play with? It's me, Aria, in my brand-new chibi form! 🎀

(Nangong Yu: Smol Aria is STILL loud, dearie.)

The Chibi Edition is the same band with a smaller backpack, packed for small context windows, small local models and thrifty wallets. Every module and switch of the full edition is still here under the same names and with the same wiring, except that Chibi carries only the 👹 Small Jailbreak and no separate `aria-micro` switch, since its Logic Core already uses Micro's planning, so sections 3 to 6 and 8 all apply to it. What changed is the wording: each rule keeps its checkable core (its numbers, thresholds and exceptions) and loses the extra explaining, in the concise style of Realistic Frankenstein's Douyin Edition. Chibi is brand new, though, and no live model has met it yet. If your model and your wallet can take the full me, that's still the tested pick.

### The three files

Chibi comes in three files that sit next to the full ones in the `presets/<format>/Base/` folders, plus the regex file my Text Completions editions share:

| File | For | Install it like |
|---|---|---|
| `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json` | Online models: Claude, Gemini, DeepSeek, OpenRouter and friends | [Section 2](#2-install-me-in-five-steps) |
| `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json` | Models on your own computer | [Section 6](#6-run-me-on-your-own-computer) |
| `Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Marinara Engine Edition.json` | Marinara Engine | Below |

- **Chat Completions.** Follow the five steps of section 2 with the Chibi file. The prompt list still starts with 🌳 README and ⚡ ARIA Main Prompt, and the README entry's version line reads Chibi Edition — Version 1.0 beta 8. Allow the regex scripts when SillyTavern asks. They're the very same ones the full file carries.
- **Text Completions.** Follow section 6 with the Chibi file. Both dropdowns should read **ARIA 1.0 beta 8 Chibi Edition (Text Completions)**, and the five settings, the switch lines, the thinking setup and the speed tips are all the same. One difference: Chibi starts with 🧠 The Logic Core already ON, because without it my lean start would be only about 1,345 tokens. The regex file is shared too: `regex/ARIA 1.0 Regex Scripts (Text Completions).json` serves both Text Completions editions, so one copy covers whichever one you run. Make it the current copy, though. An older copy can leave the last lines of a plan behind when a model echoes it, so delete the old ARIA scripts from the **Global** list before you import the new file, as section 6 describes.
- **Marinara Engine.** The third file is a Marinara preset, built on u/BSPiotr's Marinara conversion of the full edition. Import it into Marinara Engine like any Marinara preset, then pick your options in its choice blocks (adult mode, point of view, core modules, world engine, model patch, Logic Core, Logic Core options and State backend) instead of flipping toggles. The Marinara file carries no regex scripts, so there are no panels and no 💭 Thoughts box there. Its starting choices are the Chat Completions files': 👀 Hybrid POV, ⏰ Time & Place, 🎲 Fate and 🥰 Bonds Lite are ticked, and their sections ship switched on. Its 😈 Freaky Override, 🐺 Anthro Vocals and every 🩹 model patch section ship switched off in Marinara's own section list, just as in the full edition's file; 🩹 Gemini 3.8 Flash's section carries the general Gemini patch too, so it needs no second section. The 👹 Demons of Delusion Small Jailbreak section ships off too, in the 🧠 Logic Core group: pick that option in the Logic Core block and switch the section on. Picking one of the other choices doesn't bring its entry's own text until you switch its section on as well. Impersonate works Marinara's way: Marinara leaves a preset's sections out of an Impersonate turn and sends its own Impersonate instruction, so paste the lines of my 🪞 Impersonation Turn section into **Chat Settings** → **Impersonate** → **Prompt Template**, or pick my preset in that section's **Preset** menu, which keeps my sections on that turn. The 🪞 section prints on Impersonate turns only, never on a normal reply.

### How big am I?

Measured with `python3 tools/aria_budget.py` (and the Marinara render checker for the third file), which counts rendered text with comments stripped (characters ÷ 4) and corrects every total toward SillyTavern's own count: 234 tokens off for the full edition, about 450 on for me (more on that under the table). My cap is 4,000 tokens fully kitted out on The Logic Core path, and that path stays under it in every file. The 👹 jailbreaks run bigger and stay outside the cap, because they're imported exactly as they are:

| Configuration | Full edition | Chibi Edition |
|---|---|---|
| Chat Completions, shipped default | ~4,836 | 2,825 |
| Chat Completions, fully kitted out on The Logic Core path (every module ON, with the costlier Reduce Reasoning entry, now the Gemini 4 HNC one, and the largest patch, 🩹 GLM) | 6,359 | 3,976 |
| Chat Completions, the same with a 👹 Demons of Delusion jailbreak in place of The Logic Core (outside the cap) | 6,385 with the Small one (the Small Gemini is 6,973, the Big 7,375) | 4,398 with the Small Claude one, 4,826 with the Small Gemini |
| An Impersonate turn against those | ~64 fewer on The Logic Core path, ~23 fewer on the Small Jailbreak path | 66 fewer on The Logic Core path (3,910), 36 more on the Small Claude jailbreak path (4,434) |
| Text Completions, lean start | ~2,913 | ~2,189 |
| Text Completions, plus The Logic Core, Fate and Time & Place | ~4,484 | ~2,660 |
| Text Completions, fully kitted out on The Logic Core path (🩹 GLM, 🔦 Flash Gate and 🧷 Character Hold included) | 6,211 | 3,627 |
| Marinara, everything ticked with 🩹 GLM (one Reduce Reasoning option, the Gemini 4 HNC one), no agents | 6,367 | 3,983 |
| Marinara, the same with the Agents state backend | 6,625 | 4,070 |

Chibi's Chat Completions file switches on the same entries as the full one, 🎲 Fate & Chekhov Ledger and ⏰ Time & Place included, which is how its shipped default lands at 2,825. Chibi's Text Completions file starts with The Logic Core ON and the full one starts with it OFF, so those two lean starts aren't a fair match: switch The Logic Core off and Chibi's lean start would be about 1,833. Chibi's two fully kitted Chat Completions rows grew by 54 and 43 tokens in this build, because that file now has a 🧪 Auto-Routing Quality Hardener of its own and every module counts. Every fully kitted Chat Completions and Marinara row grew again with Reduce Reasoning (Gemini 4 HNC), which costs 139 tokens in both editions where the plain Reduce Reasoning costs 46 and 29 with the tags on: about 93 more in the full edition and 110 more in mine. A config runs one of the two, so a path counts the costlier; with both switched on at once, my Logic Core path would come to 4,005.

Both Marinara files render what their Chat Completions twins render, so without agents they land on the Chat Completions figures; their 🪞 Impersonation Turn prints on Impersonate turns only and no longer counts. The Agents state backend in Marinara adds its protocol note, about 88 tokens (the full edition's adds about 258), so with 🩹 GLM everything ticked comes to 4,070, 70 over my cap (4,239 with the 👹 Small Jailbreak in place of The Logic Core, which stays outside the cap).

These figures come from `tools/aria_budget.py`, corrected toward SillyTavern's own counter, the number next to **Total Tokens:** in SillyTavern's prompt list, read with the card and memory toggles switched off. On the full edition's largest path, with 🩹 GLM and the 🔦 Flash Gate, SillyTavern showed 7,264 where a plain characters ÷ 4 count said 7,498, 234 tokens less, while my compressed wording packs more tokens into each character, so SillyTavern counts about 450 more than the plain count on the Chibi Edition. The script takes those 234 tokens off every full-edition total and adds 450 to every Chibi total, and every row above carries that correction. Each correction was read on one path, so the other paths carry an estimate. Use the table to compare paths, and re-measure any figure that matters in the GUI: the shipped default, the fully kitted Logic Core path and the jailbreak paths, in both editions and in Marinara.

Here's where the tokens went, entry by entry, with every entry ON in the Chat Completions file (the checker's own table, which lists the 👹 Small Jailbreak next to The Logic Core even though you run one or the other):

| Entry | Full edition | Chibi Edition |
|---|---|---|
| ⚡ ARIA Main Prompt | 738 | 328 |
| 🔞 Adult Context | 187 | 140 |
| 😈 Freaky Override | 54 | 30 |
| 👀 Hybrid POV | 46 | 22 |
| 🎬 Voice & Scene Engine | 367 | 125 |
| 🎭 NPC Voice & Emotions | 349 | 114 |
| 🐺 Anthro Vocals | 128 | 45 |
| 🖋️ Anti-Slop Codex | 978 | 284 |
| 👃 Scent Occasions | 94 | 47 |
| ⏰ Time & Place | 82 | 47 |
| 🎲 Fate & Chekhov Ledger | 853 | 323 |
| 🥰 Bonds Lite | 297 | 124 |
| 🩹 Model Patch: GLM, its own text (its five lines are counted in the plan and the gate) | 22 | 22 |
| 📖 Story Context | 3 | 3 |
| 👹 Demons of Delusion Small Jailbreak ✨ (in place of The Logic Core) | — (three variants) | 1,030 |
| 🧠 The Logic Core, with every module's lines in it | 914 | 595 |
| 🚪 Last-Mile Gate, with every module's lines in it | 1,251 | 870 |
| Reduce Reasoning | 78 | 17 |
| Reduce Reasoning (Gemini 4 HNC) | 139 | 139 |

With a tags entry on, Reduce Reasoning swaps its old three-line note for the tags-aware one: about 46 tokens in the full edition (-32) and 29 in Chibi (+12). With the tags off it renders as before, which is the 78 and 17 above. Chibi's 🧪 Auto-Routing Quality Hardener is newer than this table: with it ON as well, The Logic Core's row grows by about 36 tokens and the gate's by about 18. Reduce Reasoning (Gemini 4 HNC) has no tags form and reads the same in both editions.

### How I differ from the full edition

- **Every module is compressed.** Rules are short do-this sentences, one rule per clause, and plan and gate lines are fragments joined by semicolons. The checkable core of each rule survives: its numbers and thresholds, its exceptions (a nervous card keeps its stammers, a refusal stays a plain no) and each patch's own lines. Restatements, explaining and overlaps are what went, plus a few small details, which most modules name in their comment. That comment is the note at the top of an entry's text, and it costs no tokens. The 🩹 Claude 5 patch still holds the preset's only quoted repairs, shortened. The one entry Chibi carries word for word is Reduce Reasoning (Gemini 4 HNC), my beta tester @IReallyDon'tCare's Thinking Leash.
- **Each rule lives in one place.** The ⚡ Main Prompt leaves bodies, resting temperament, what characters know, secrets, newcomers at the edge and verdict-free narration to the 🚪 Last-Mile Gate, and the 🖋️ Anti-Slop Codex is written as the details of the gate's rules (Balance, Count, Paragraphs and Senses live only in the gate). So keep all three ON, the Main Prompt, the Codex and the gate.
- **Time & Place is optional.** 🎲 Fate and ⏰ Time & Place ship ON in the Chat Completions and Marinara files, as in the full edition, but Chibi's Fate keeps no timed appointments to hang a clock on, so switch Time & Place off when you need the room.
- **A lighter Fate.** The three dice, the tier ladder with its thresholds, the ledger fields and the tester fixes (for q, threads, whole and unwarned MAJOR events, ripe World entries, folded AMBIENT lines and the natural-20 limit) are all there, and so is the Peril rule, which keeps big events very rare in a safe life and frequent in daily danger. What Chibi's Fate leaves out are the full edition's timed appointments, its Ambitions and Quiet-turn rules, most of its World rule and some cell details. So nothing tells it to log a goal you state as an Ambition (the ledger keeps the field) or to fire an appointment on time, quiet turns get no rules of their own, and World news keeps only its core: it reaches the page through someone present.
- **Ledger ages written n/8, n/6 and n/12.** Chibi puts the age limits into the ledger itself: a thread's age reads n/8, a Deferred item's n/6 and a Bullet's n/12, where the full edition writes plain ages. The same regex scripts dress the ledger up as the same orange panel.
- **A lighter Bonds.** The BOND scale from -10 to +20, the Sparks, Grudge and conversions (7 Sparks make one point, 5 Grudge cost one, 3 Grudge halve the gains and a sincere repair clears them) and the touch gates (+4 hug, +8 hand-holding, +12 kiss, +15 sex) are all kept, and so is the teal 💚 panel. The long description of each tier (hostile, neutral, warm, trust, devoted) and the `<bonds>` tags are gone.
- **The same Micro-based 🧠 Logic Core, in fewer words.** Chibi's plan keeps the full one's first-person game-master opening, the every-line rule, even-handed outcomes, full acts (a fight, a lie, a seduction or a refusal, nervous cards aside) and the Mode line's plan for an adult beat. Its opening line already ends the thinking at `go`, so it skips the full one's "no further reasoning" cue, and its Freaky line leaves the four-reply rule for fresh details to the gate's Senses line.
- **The 👹 Small Jailbreak comes in place of The Logic Core, not on top of it.** Chibi's Chat Completions and Marinara files carry the Small Jailbreak; switch 🧠 The Logic Core off while it is on. The ⚡ Main Prompt, the Real Characters rule and 🔞 Adult Context now carry the full edition's jailbreak support text too. In Marinara, pick the 👹 option in the Logic Core choice block and switch its section on in the 🧠 Logic Core group, where it ships off. The 🚪 Last-Mile Gate then leaves out The Logic Core's "7 dashed lines" cue.
- **The 🧪 Auto-Routing Quality Hardener is in all three Chibi files.** My Chat Completions file had none until this build, because its 👹 Small Jailbreak has no place for the hardener's plan lines. Now the Claims line, a firm Knows line, Realistic Frankenstein's four killswitches (Comparative Emphasis, Staccato Chop, Briefing Register and Inner-State Attribution) and the patch rules that move with them stand in the plan while 🧠 The Logic Core or its system-role twin is ON, and in the 🚪 Last-Mile Gate with a 👹 jailbreak or with no plan at all, where three short lines join them (say what a thing is, first words are the point, one sentence with its clauses joined). They never stand in both, so keep the gate ON. The firmer Knows lines and the two 🩹 DeepSeek lines work as in the full edition. It costs about 210 tokens with The Logic Core, where the full edition's costs about 58, and about 270 with a 👹 jailbreak or no plan; the DeepSeek lines add about 11, or about 31 with the Ledger sentence. It ships OFF and is only for providers that swap or quantise the model behind your request. Chibi's Marinara file carries the same lines, word for word; with its 👹 Small Jailbreak picked, they stand in the jailbreak's own dialogue task and the three short lines in the gate. Chibi's Text Completions file keeps the Claims line alone and uses the gate the same way when no plan runs. The full edition's Text Completions and Marinara files have the same fallback. Its Chat Completions file has none, because its gate can't tell a 👹 jailbreak from no plan: there the Claims line and the moved rules need a plan.

### Chibi's Text Completions switches

Chibi keeps every `aria-*` switch under the same name. This table flips one switch at a time from Chibi's shipped state, so The Logic Core is already on and each row includes its plan line. The last column is the full edition measured the same way, with The Logic Core on too, so it isn't the table in section 6, which flips from the full file's shipped state with it off.

| Switch | Starts | Chibi | Full edition |
|---|---|---|---|
| `aria-logic-core` | on | ~335 | ~500 |
| `aria-thinking-tags` | on | ~55 | ~30 |
| `aria-adult` | off | ~100 | ~155 |
| `aria-freaky` | off | ~20 | ~55 |
| `aria-hybrid-pov` | off | ~45 | ~85 |
| `aria-npc-voice` | on | ~115 | ~350 |
| `aria-anthro` | off | ~45 | ~130 |
| `aria-scent` | on | ~70 | ~120 |
| `aria-time-place` | off | ~45 | ~80 |
| `aria-fate` | off | ~425 | ~966 |
| `aria-bonds` | off | ~200 | ~380 |
| `aria-patch-glm` | off | ~325 | ~555 |
| `aria-patch-kimi-qwen` | off | ~80 | ~120 |
| `aria-patch-mimo-pro` | off | ~70 | ~90 |
| `aria-patch-mimo-flash` | off | ~210 | ~330 |
| `aria-patch-deepseek` | off | ~310 | ~440 |
| `aria-flash-gate` | off | ~140 | ~255 |
| `aria-character-hold` | off | ~55 | ~90 |
| `aria-hardener` | off | ~54 | ~58 |

With the 🩹 DeepSeek patch, the Tally line adds about 40 tokens with Fate, 75 with Bonds or 95 with both (the full edition's adds about 50, 90 and 125).

### Which me should I pick?

- **Plenty of context and budget, or you want the version the testers have run?** The full me.
- **A small context window, a small local model, or you pay by the token?** Chibi me! Start from the defaults, and switch 🎲 Fate on when your model can take the extra weight.
- **Not sure?** Try the full me first, and swap to Chibi if it feels heavy. Both editions keep the same toggle names, so your habits carry over.

---

## 8. Uh-oh! moments

Even idols trip on stage sometimes! These fixes get you back up:

**I see strange bits like `{{setvar`, `{{roll` or `{{.aria-fate = off}}` in the prompt or the replies.**
The macro engine is off. Tick **Experimental Macro Engine** in User Settings and reload.

**The AI's thinking shows up inside the reply.**
In Advanced Formatting, tick **Auto-Parse**, open **Reasoning Formatting** and set **Prefix** and **Suffix** to your tags (section 3, style B). Check that the preset's regex scripts are allowed too, under **Extensions** → **Regex**; they fold a plan into a 💭 **Thoughts** box even when the model forgets its tags. On the Text Completions file, import my regex file from section 6 as well. If the model with native reasoning off skips the plan or writes it loosely, make sure 🏷️ **Logic Core Tags** is ON (style B), since that's the switch that tells it to open every reply with `<thinking>`. On the Text Completions file, that's `aria-thinking-tags`, which ships `on`.
Does the reply open with a bare `thinking` line, with no angle brackets, then the plan? MiMo V2.6 Pro on NanoGPT sometimes drops the brackets like that, and the closing line may be `</thinking>`, `/thinking`, a bare `thinking` or missing altogether. Auto-Parse can't catch it, but my regex scripts can: they fold that plan into the 💭 **Thoughts** box and keep it out of what the model rereads. They only treat `thinking` as a plan opener when it stands alone on the reply's first line, so a story that starts "Thinking about it, she…" stays untouched. Still seeing it? Grab the current preset (or the regex file from section 6 on the Text Completions file).

**The plan lands in a purple 💭 Thoughts box instead of SillyTavern's own reasoning box.**
SillyTavern's **Auto-Parse** only catches a reply whose very first characters match your **Prefix**, so check that the Prefix is exactly `<thinking>` and the Suffix exactly `</thinking>`, with no spaces (`<thought>` and `</thought>` on Gemini 4 Argon with its own tags entry). With a Gemini 4 setup, keep the Gate ON too: Gemini 4 rejects a request that ends on a model turn. Before beta 5, MiMo liked to copy the `<logic_core>` label my planning note started with, and SillyTavern can't parse that one. From beta 5 on, The Logic Core starts on `<thinking>` itself whenever 🏷️ Logic Core Tags is ON, so check that your 🌳 README entry (or the Text Completions template name) says beta 8, the current build. If it doesn't, re-import the preset, and on the Text Completions file swap in the new regex file from section 6 too. A time header written above the plan blocks Auto-Parse as well; my regex scripts still fold the plan then, which is exactly what the purple box is there for.
Does SillyTavern's own reasoning box show up as well, full of the model's free-form musings, while my checklist sits in the purple box below it? Then your provider still sends the model's native reasoning, and SillyTavern skips Auto-Parse for any reply that already carries some, however neatly it opens with `<thinking>`. Untick **Request Model Reasoning** and set **Reasoning Effort** to **Minimum** again (section 3, style B). If that provider keeps thinking anyway, style A suits it better!

**A reply arrives empty, and the whole story sits in the reasoning box.**
The model left its plan open, so **Auto-Parse** read everything after `<thinking>` as reasoning. In BSPiotr's test MiMo V2.6 Flash once ended its plan on `</go>`, and SillyTavern doesn't count that as the end of the plan. Swipe for a new reply, or untick **Auto-Parse** if it keeps happening, because my regex scripts then fold the plan into the 💭 **Thoughts** box themselves, `</go>` included, and keep it out of what the model rereads. A stray closing tag left after the ledger gets dropped from the prompt the same way, so the model never learns to copy it.

**The plan never shows up, and the reply starts straight with the story.**
First check that **Request Model Reasoning** is unticked and 🏷️ **Logic Core Tags** is ON. If the model still skips the plan, switch 🧠 **The Logic Core** OFF and 🧠 **The Logic Core (system-role twin)** ON, so the plan arrives as an instruction inside the very last message. MiMo V2.6 Pro follows that version more often on some providers. If the twin makes no difference on your model, switch back, since a few chat formats move every system message to the top of the prompt. A long pause before the first word with no plan in sight means the model still thinks in secret on its own, and style A suits it better.

**The model's thinking takes forever.**
Switch to thinking style B, or turn on the 🩹 GLM or 🩹 Kimi / Qwen patch if you use one of those models. On Claude, stay on style A and set **Reasoning Effort** to **Low** instead, because Claude keeps thinking whichever setting you pick. On the Text Completions file, set `aria-logic-core` to `off`, or set `aria-patch-glm` or `aria-patch-kimi-qwen` to `on` for those models.

**The 🎲 ledger shows up as plain text instead of a panel.**
Allow the preset's regex scripts under **Extensions** → **Regex**, or import my regex file on the Text Completions file (section 6). If the scripts are on and one reply still looks raw, the model wrote its ledger in an odd shape, like fields split over several lines or a ledger without its 🎲. The next reply usually fixes itself, and the engine reads the plain text just fine either way.

**The bonds show up as a loose line or a bare card under the 🎲 panel.**
That's a beta 3 habit! From beta 4 on, Bonds keeps its own 💚 ledger, and my regex scripts tuck a stray bonds line from older replies into the teal panel too. Re-import the preset, and on the Text Completions file import the new regex file as well (section 6).

**The 🎲 line vanished and the world forgot what was going on.**
Make sure 🎲 Fate & Chekhov Ledger is ON and that you didn't edit the line out of the AI's last reply. If you switched on the "Drop old ledgers" regex, switch it off again in **Extensions** → **Regex**. Also check that **Trim Incomplete Sentences** in **Advanced Formatting** is unticked, because it cuts that line in half. On the Text Completions file, check that `aria-fate` is `on` and that **Response (tokens)** is large enough (section 6), since a reply cut off at the limit loses the 🎲 line. Running DeepSeek through NanoGPT or another route that can hand you a quantised copy? It has dropped the 🎲 and 💚 blocks there ever since the first V4 snapshots. Switch the 🧪 Auto-Routing Quality Hardener ON next to the 🩹 DeepSeek patch: the gate then says every reply closes on its blocks and that one stopping at the prose is unfinished.

**A character suddenly speaks English in my Hungarian story.**
Write your own messages in your story's language, or add an OOC note like `((OOC: the story is in Hungarian))`. The Main Prompt follows whatever language you use.

**Characters repeat my words back to me.**
That's parroting, and Kimi K3, GLM and MiMo love it: a reply opens on your own line, like your pet name handed back as a question, or tucks it into a thought or a later paragraph. My 🖋️ Anti-Slop Codex tells the AI to answer the meaning of your message in the character's own words, and the 🚪 Last-Mile Gate repeats that as its Own words line. The Logic Core's plan also sums up what anyone said in its own words, because MiMo used to quote your line in its plan and then hand it straight back in the reply. The part only you can fix is the chat itself. Every reply that opens on your words stays in the history, and the model copies its shape on later turns, so one echo grows into a habit. Edit or delete those openers as soon as they show up, and judge any fix on a clean chat over several turns, since swipes inside a chat that already echoes keep echoing.

**Characters talk like a helpful AI assistant.**
You know the type: a character opens with "here's the deal", counts off their points, says "fair enough" before answering, or calls you "champ" out of nowhere. Realistic Frankenstein's notes say GLM, Kimi and Qwen picked that register up from Claude, which has it too. My 🖋️ Anti-Slop Codex carries Realistic Frankenstein's Anti-Briefing Register in a compact form: characters talk to someone in their everyday words with their first words already the point, and before heavy news a speaker takes the floor with an act, a name, a question or an accusation. Approval or a grade of what you said shows in what a character does next, and the 🚪 Last-Mile Gate repeats that right before the reply. On GLM, switch on the 🩹 GLM patch as well: its five lines at the very end of the prompt and in the plan make everyone talk like a real person with a life of their own, who agrees with some things and pushes back on others the way their card would. Kimi and Qwen users switch on 🩹 Kimi / Qwen. As with parroting, clean the assistant lines out of the chat, because the model copies what it already wrote.

**Every reply ends on a punchline, like a superhero movie.**
That's the quippy banter u/trashhaul caught on every model he tried in beta 6. Characters joked about their own feelings, almost every paragraph ended on a little button, and a nervous ranger turned into a stand-up act on one model and a brooding action hero on another. Since beta 7 my 🖋️ Anti-Slop Codex describes how real people joke: rarely, in small ways that fit their card, and often to no laugh at all, while sincere moments stay sincere. Your own jokes always get a reaction, a laugh, a groan, a fluster or a blank look, so MiMo stops walking straight past them. The 🚪 Last-Mile Gate checks it again at the very end, and that one line outranks even the card, so a goofy card still jokes like a person. Clean the old quips out of the chat as well, because the model copies whatever it already wrote.

**Everything comes in threes.**
"Outrun, outclimb or outwait", "no track, no stalk, no shot": that's the rule of three, and GLM loves it most. My Codex now keeps lists, runs of phrases and and-chains to one or two items (four when there really are four), and the gate checks it every turn again, which beta 6 had quietly stopped doing. The Logic Core's last check looks for it too. My own rules used to be full of lists of three, which taught the model the rhythm, so I rewrote them without any! On a quantised node, DeepSeek V4.1 Flash still slipped a three past the gate by joining it with "and" ("warm and comfy and elegant"), so with the 🩹 DeepSeek patch and the 🧪 Auto-Routing Quality Hardener both ON, the gate's Count line names and-chains as well.

**A stranger walked in and took over the story.**
In beta 6 my gate handed the AI a fresh first letter for a new character's name every single turn, and DeepSeek took that as an invitation. Fate could also open a story thread for anyone who happened to be standing there. Beta 7 drops the letter, keeps newcomers at the edge of a scene until their business is done, and gives story threads to your card's characters or to you. If someone new still steals the scene, swipe, or say out of character that the card's character should come back.

**A character gets the wrong gender or pronouns.**
Start with the character's lorebook entry. Pronouns scattered through a description are a weak signal, and a model that half-knows the name can trust its own guess over them. Open the entry with one plain sentence that says who the character is in a gendered word, like "a doting mother figure for Soukaku" for Yanagi or "the only man in Section 6" for Harumasa. That one sentence stopped Kimi K3 from calling a woman "he" in our tests! An entry also reaches the AI only once its keywords show up in the last few messages, so a character the AI brings on stage by itself can walk in before their entry does. Open that reply's **Prompt** button in the message menu and look for the entry, and if it's missing, set the entry to **Constant** (the 🔵 blue circle). Still wrong with both in place? Tell me which model slipped.

**With 👀 Hybrid POV on, the story mixes "you" with my character's name, or switches tense.**
Before this update, my Hybrid POV rule asked for third person with your character's name and kept "you" for what your character feels, and Gemini 4 Argon ended up writing "your fingers" and your name in the same sentence, sliding from past to present tense along the way. The rule now says your character is "you" in every line of narration, in the chat's one tense, while everyone else stays in third person. Grab the new build, and if an old reply keeps pulling the model back, edit that reply or swipe once. A first message written in third person can pull too, so give the model a reply or two to settle.

**GLM Flash or MiMo Flash keeps turning feelings into paperwork.**
Switch the 🔦 Flash Gate ON next to your model patch. The patch handles the model's other habits, and the Flash Gate swaps the gate's short Register and Work lines for its firmer rules against assistant-style framing and office words at the very end of the prompt, where Flash models listen best.

**A character's job becomes her whole personality.**
On u/trashhaul's card, MiMo V2.6 Pro turned a smart accountant into a walking spreadsheet, with receipts and headcounts everywhere and the newcomer filed under a column called MISCELLANEOUS. The 🚪 Last-Mile Gate's Work line keeps work words for work that's happening, someone raising it, a deadline or a dodge, and away from live work the job comes up at most once in five turns, so her job stays her job and you stay a person. GLM 5.3 kept the same accountant human on its own. If one model still drifts, check the chat for earlier replies full of the job, since the model copies them.

**Characters feel flat, or all agree with me.**
Check that 😈 Freaky Override is OFF, because it makes everyone eager on purpose. On MiMo V2.6 Pro or Flash, switch on the 🩹 MiMo V2.6 Pro or 🩹 MiMo V2.6 Flash patch. On MiMo V2.6 Flash or GLM Flash, add the 🔦 Flash Gate too, and on MiMo Flash try Temperature 0.8, the setting Realistic Frankenstein shipped for it. Do characters start out rich and go flat after ten or so turns, shrinking to whatever the last big scene called for? Your provider may be serving a quantised copy of the model. Switch 🧷 Character Hold ON, or on OpenRouter pin Xiaomi or Venice for MiMo V2.6 Flash.

**Characters read my character's mind, or know things nobody told them.**
My Main Prompt's Epistemic Limits rule says characters know only what they saw, heard aloud or were told, and that your character's thoughts and the narration reach nobody; the plan and the 🚪 Last-Mile Gate each repeat it in a Knows line. Does it still happen, mostly on NanoGPT or OpenRouter auto-routing? Your provider may be serving a quantised copy of the model, which follows rules more loosely. Switch the 🧪 Auto-Routing Quality Hardener ON: it swaps both Knows lines for firmer ones that name thoughts and narration. A character whose card gives them mind-reading or second sight keeps the gift, because the firm lines end on "unless the card grants it".

**The model refuses or tiptoes around a scene.**
Turn The Logic Core ON (on the Text Completions file, set `aria-logic-core` to `on`), since it helps a lot of models settle in. For mature scenes, 🔞 Adult Context must be ON: its line in my plan works out each adult beat in full, and The Logic Core's game-master opening keeps the AI out of its helpful-assistant voice. Some models refuse certain content no matter what any preset says, and when that happens a different model is the only real fix.

**My local model takes ages to start every reply.**
Your backend is rereading the whole prompt each turn. Go through the "Keep it fast" list in section 6, especially the lorebook and switch tips.

**My local model writes its plan right into the reply.**
Set up Reasoning Formatting as shown in section 6 and import my regex file, which folds a tagless plan away for you. If the model still struggles, set `aria-logic-core` to `off`.

**After pressing Impersonate, the input box has junk in it.**
Allow the preset's regex scripts in **Extensions** → **Regex**. They clean the Impersonate result for you. On the Text Completions file, import my regex file from section 6, which does the same job.

**(Text Completions file) My rules, switches or dice do nothing with one particular card.**
That card brings its own System Prompt or Post-History Instructions, and SillyTavern uses them in place of mine. In **User Settings**, untick **Prefer Char. Prompt** and **Prefer Char. Instructions**, or add `{{original}}` to the card's own prompt so mine comes along.
On the Chat Completions file, the Main Prompt and the Last-Mile Gate are locked against card overrides. Check instead that the card's own text doesn't contradict my rules, and that ⚡ ARIA Main Prompt and 🚪 Last-Mile Gate are still ON in the prompt manager.

**There is no Experimental Macro Engine box in User Settings.**
Your SillyTavern is too old for me. Update it to 1.19.0 or newer.

---

## 9. Manager's corner (for the curious)

Phew, that's everything a beginner needs! This last part is for nerdy Managers who want to peek under the hood, like Lewis, who helped me pack all of this into one file. Sunna fell asleep halfway through when I explained it to her, so no pressure~ 😴

### Token budget

Measured with `python3 tools/aria_budget.py`, which counts rendered text with comments stripped (characters ÷ 4) and takes 234 tokens off every total, the full edition's correction toward SillyTavern's own count, as [section 7](#7-meet-chibi-me-the-chibi-edition) explains:

| Chat Completions configuration | Tokens |
|---|---|
| Core (everything that ships ON except Fate and Time & Place) | ~3,824 |
| Shipped default | ~4,836 |
| Fully kitted out on The Logic Core path (the defaults plus Logic Core Tags, Adult, Freaky, Anthro, 🔦 Flash Gate, 🧷 Character Hold, the costlier Reduce Reasoning entry, now the Gemini 4 HNC one, and the largest model patch, now 🩹 GLM) | 6,359 |
| The same with a 👹 Demons of Delusion jailbreak in place of The Logic Core (listed, not held to the cap) | 6,385 (Small), 6,973 (Small Gemini), 7,375 (Big) |
| An Impersonate turn against that (the 🪞 entry and SillyTavern's impersonation prompt come in, while the Fate, Bonds, ledger, dice, POV, Own words and 🧷 Character Hold lines drop out) | ~64 fewer on The Logic Core path, ~23 fewer on the Small Jailbreak path, ~62 fewer on the Small Gemini and ~61 fewer on the Big |

For comparison, Realistic Frankenstein 2.2.1.3 set up the same way (its Fate & Routine engine, Chekhov's Gun, the killswitches, the last-mile gates and a model patch) renders about 23,800 tokens, so a fully kitted ARIA path is roughly 73% smaller. Beta 7 is the third rewrite, and as first released it came out a little larger than beta 6: about 100 tokens more as shipped and about 40 more with every switch on. Its new rules against superhero banter, lists of three, drifting temperament and scene-stealing newcomers cost about 400 tokens, and dropping gate lines that repeated rules nobody broke paid back most of that. Getting clearly below beta 6 would mean cutting rules the testers proved useful, so that trade is yours to call.

The Text Completions file, measured the same way:

| Text Completions configuration | Tokens |
|---|---|
| Lean start, as shipped for 32k | ~2,913 |
| Plus The Logic Core, Fate and Time & Place | ~4,484 |
| Fully kitted out on The Logic Core path (largest patch, 🔦 Flash Gate and 🧷 Character Hold included) | 6,211 |
| The same with the Micro jailbreak in place of The Logic Core (listed, not held to the cap) | 6,946 |

The checker ranks the patches over a setup with every other switch on, the way it does for the Chat Completions file, so the largest one in this row is 🩹 GLM, whose five lines print in the plan as well as in the gate. (Before beta 8's checker fix it sized each patch with every other switch off, picked 🩹 MiMo V2.6 Flash and showed this row as about 5,940.) Beta 5 measured about 4,430 here with everything ON. Want to compare the two builds for yourself? Beta 5 waits in `archive/ARIA 1.0 beta 5/` on the [`beta` branch](https://github.com/QuillFlash/ARIA/tree/beta/archive) with its presets and regex file, plus `Model fixes.md`, which lists all 139 model fixes it carried. Its presets carry their own names, so you can import them next to the current ones. Its regex file uses the same script names as mine, so on the Text Completions file swap it in only while you test beta 5 and put the current file back afterwards, the way section 6 describes.

The Chibi Edition's files are measured the same way, except that about 450 tokens are added to every total instead of 234 taken off, against a cap of 4,000 tokens, which the checker gives to any preset with Chibi Edition in its file name. [Section 7](#7-meet-chibi-me-the-chibi-edition) lists their figures.

The script also fails if a fully kitted path goes over its budget (7,500 tokens, or 4,000 for the Chibi Edition files). It checks each real path separately, because The Logic Core and the 👹 Demons of Delusion jailbreak entries are alternatives, never additive: a path is the shared base, one plan, one model patch and one Reduce Reasoning entry, the costlier of the plain one and the Gemini 4 HNC one, since a config runs one of each. The jailbreak paths, the Text Completions Micro jailbreak included, are listed with their size but never held to the budget, since the jailbreaks stay exactly as they were imported. The jailbreak entries are imported from Realistic Frankenstein and bring their own tags and variables, so the wiring and order checks leave them out. It also fails if a tag or label is referenced and never defined, if a variable is set and never read (or the reverse), if an entry reads a variable before anything earlier in the list sets it, if any render with a 🏷️ Logic Core Tags entry on still names `<logic_core>`, or if anything would break prompt caching. It checks each tags entry on its own (the `<thinking>` one and the Gemini 4 Argon `<thought>` one) or none, each Logic Core (or none), each model patch and Impersonate, and it sizes each patch together with any line it adds to the gate. The caching check also leaves every variable behind from an earlier turn and confirms the system block comes out the same. It runs that for each fully kitted path and again for each model patch on its own over the shared base, because a path holds only the largest patch, so a variable that one patch sets and another patch prints never showed up there. That's how the Gemini 3.8 Flash text kept printing through Gemini All-In-One for a turn after the 3.8 patch was switched off, until the Main Prompt's first line began blanking `gemini38Patch`. The Text Completions files get the same per-patch test. Run it after every edit.

### Prompt order (Chat Completions)

| # | Entry | Where it goes | Default |
|---|---|---|---|
| 1 | 🌳 README, 🌿 Sampling Advice | notes only | off |
| 2 | 🍃 Custom Instructions | system block | on |
| 3 | ⚡ ARIA Main Prompt | system block | on |
| 4 | 🏷️ Logic Core Tags, then the Gemini 4 Argon Thinking Tags Enforcer | system block, setters only | off |
| 5 | 🔞 Adult Context, 😈 Freaky Override, 👀 Hybrid POV | system block | off |
| 6 | 🎬 Voice & Scene Engine, 🎭 NPC Voice & Emotions | system block | on |
| 7 | 🐺 Anthro Vocals | system block | off |
| 8 | 🖋️ Anti-Slop Codex, 👃 Scent Occasions | system block | on |
| 9 | ⏰ Time & Place, 🎲 Fate & Chekhov Ledger | system block | on |
| 10 | 🥰 Bonds Lite, 🧪 Auto-Routing Quality Hardener, 🩹 Model Patches, 🔦 Flash Gate, 🧷 Character Hold (setters only; the hardener comes first so the patches can append to its Claims line) | system block | off |
| 11 | 📖 Story Context | system block | on |
| 12 | Persona, card, personality, scenario, examples, then World Info before and after | system block | on |
| 13 | Chat History | | on |
| 14 | 🪞 Impersonation Turn | In-Chat depth 0, user, Impersonate only; it comes first so it can clear the Fate, Bonds, ledger, POV, Own words and Character Hold lines before The Logic Core and the gate read them | on |
| 15 | 👹 Demons of Delusion Jailbreak, Small Jailbreak and Pico Jailbreak ✨ | In-Chat depth 0, assistant | off, and only one runs in place of The Logic Core |
| 16 | 🧠 The Logic Core | In-Chat depth 0, assistant | on |
| 17 | 🧠 The Logic Core (system-role twin) | In-Chat depth 0, system, merged into the gate's message | off |
| 18 | 🚪 Last-Mile Gate | In-Chat depth 0, system | on |
| 19 | Reduce Reasoning | In-Chat depth 0, user | off |
| 20 | Reduce Reasoning (Gemini 4 HNC) | In-Chat depth 0, system, merged into the gate's message right after the gate | off |

The Chibi Edition's Chat Completions file uses the same order and the same defaults, and it carries two jailbreaks, the 👹 Small Claude and Small Gemini ones, which also ship OFF and take The Logic Core's place when you switch one on.

### Cache-first rules

These are checked against SillyTavern's own source code:

- In-Chat entries are spliced in after the newest message. At the same depth and order, SillyTavern writes them as assistant, then user, then system, so the Last-Mile Gate reads last, right after The Logic Core. Entries with the same role merge into one message in list order, so the system-role twin and the gate travel together as the final message, and Reduce Reasoning (Gemini 4 HNC), when it's on, closes that message after the gate.
- SillyTavern reads the macros in list order, wherever each message lands. Both Logic Cores therefore sit above the gate in the list: the gate prints their closing cue (`ariaPlanCue`) as its very last line.
- For Claude, every system message before the chat becomes the cached system prompt, and later system messages are sent as user messages. That's why `cachingAtDepth: 2` skips the gate (depth 0) and The Logic Core (depth 1). On OpenRouter, SillyTavern skips system messages when it counts depth, so the markers land on the AI's two previous replies instead.
- Nothing in the system block changes between turns. Dice live inside `{{setvar}}`, which prints nothing there, and only print at the end through the gate. No system-block entry has generation triggers, so Impersonate reuses the same cache.
- World Info sits after the card and examples, so a lorebook change only re-reads what comes after it.
- Chat history never gets rewritten. The ledger-trimming regex ships disabled for that reason.
- The panel, row, label and bond-bar scripts are display-only, so the prompt stays exactly as written. The thinking strips (tagged plans, mismatched tags including a plan closed with `</go>`, untagged plans, a copied Logic Core and a stray closing tag at the end of a reply) run on every depth, so a message reads the same to the model on every turn after it's written. Since beta 6 the four scripts that fold or strip tagged and mismatched thinking look 40,000 characters ahead, twice the old window, so even a very long MiMo Flash reasoning block folds on screen and stays out of the prompt.

### The Text Completions edition

- The switches are chat variables set at the very top of the System Prompt (`{{.aria-fate = off}}`). The macro engine reads text from top to bottom, so every block below, like `{{#if .aria-fate}}`, already sees the new value. Empty, `off`, `false` and `0` all count as off.
- Each optional module sits inside a `{{#if}}` block, with its closing line break inside the block too. The `#` keeps whitespace exactly as written, so a switched-on module keeps that line break and the next one starts on a fresh line, while a switched-off module prints nothing at all.
- SillyTavern adds the post-history block as the last user message after your newest one. It holds The Logic Core (when switched on) and the Last-Mile Gate with the dice, so the System Prompt stays identical every turn.
- The story string puts the card fields and examples first and World Info last, right before the chat. That only holds with **Example Messages Behavior** on **Never include examples**; otherwise SillyTavern sends a second copy of the examples after the story string.
- The context template ships with **Trim Incomplete Sentences** off, since the 🎲 and 💚 lines end in an HTML tag that the trimmer doesn't count as the end of a sentence.
- The Chibi Text Completions file is built the same way, with two differences. `aria-logic-core` ships `on`. And the gate's four notes on what a message written as you skips (for its Own words, POV, Ledger and Layers lines) print only while The Logic Core is off. With it on, the plan's closing sentence names the lines a message written as you skips (Fate, Bonds, Ledger, Layers, Own words and POV), which keeps a fully kitted Chibi Text Completions file at 2,943.

### Wiring (Chat Completions)

The Main Prompt's first line blanks every helper variable each turn, so a switched-off module leaves nothing behind. The Text Completions file uses the very same variables: its System Prompt is read before its post-history block, so the switched-on modules set them there.

| Variable | Set by | Read by |
|---|---|---|
| `ariaDice` | 🎲 Fate (three d20 rolls) | 🚪 Last-Mile Gate, which also clears it |
| `ariaFateLine` | 🎲 Fate | 🧠 The Logic Core |
| `ariaBondsLine` | 🥰 Bonds Lite | 🧠 The Logic Core |
| `ariaModeLine` | 🔞 Adult Context, overwritten by 😈 Freaky | 🧠 The Logic Core |
| `ariaScentGate` | 👃 Scent Occasions | 🚪 Last-Mile Gate |
| `ariaPovGate` | 👀 Hybrid POV | 🚪 Last-Mile Gate |
| `ariaThinkOpen`, `ariaThinkClose` | 🏷️ Logic Core Tags (`<thinking>`), or the Gemini 4 Argon Thinking Tags Enforcer (`<thought>`), which comes later in the list and wins when both are on | 🧠 The Logic Core (`{{#if .ariaThinkOpen}}`) |
| `ariaLedgerLine`, `ariaLedgerGate` | 🎲 Fate, or 🥰 Bonds Lite when Fate is off (with both on, Bonds rewrites them so the 🎲 block is followed by its own 💚 block) | 🧠 The Logic Core, 🚪 Last-Mile Gate |
| `ariaEchoGate` | 🖋️ Anti-Slop Codex | 🚪 Last-Mile Gate (its Own words line) |
| `ariaFlashGate` | 🔦 Flash Gate | 🚪 Last-Mile Gate |
| `ariaHoldLine`, `ariaHoldGate` | 🧷 Character Hold, blanked by the 🪞 Impersonation Turn | 🧠 The Logic Core (its Layers line, after Voice), 🚪 Last-Mile Gate (its last rule line) |
| `ariaPatchGate` | 🩹 GLM patch (five lines), 🩹 Kimi / Qwen patch (its Filler line), 🩹 Gemini patch (its Gemini line), 🩹 MiMo V2.6 Flash (its Flow and Card details lines) or 🩹 DeepSeek (its Echo, Repeats and Bodies lines); the Contrast rule that the Gemini, MiMo Pro and MiMo Flash patches used to carry now sits once at the tail of the 🚪 Last-Mile Gate | 🚪 Last-Mile Gate, after the ledger line, and 🧠 The Logic Core, between its Voice and Move lines |
| `ariaPatchLines` | the same patch: how many lines it hands over | 🧠 The Logic Core (its line count) |
| `ariaHardener`, `ariaPatchPlain`, `ariaPatchPlainLines` | 🧪 Auto-Routing Quality Hardener sets the switch and the Claims line; each 🩹 patch then appends its plain rules while the switch is ON (the Main Prompt blanks all three first; each value ends on `{{newline}}`, because SillyTavern drops a plain newline at the end of a variable's value) | 🧠 The Logic Core and its system-role twin (the lines sit between Voice and the patch's gate lines, one in the line count for each), the 👹 jailbreaks (in their dialogue task) |
| `ariaKnowsLine`, `ariaKnowsGate` | 🧪 Auto-Routing Quality Hardener: the firmer Knows lines (the Main Prompt blanks both first) | 🧠 The Logic Core and its system-role twin (in place of their own Knows line), 🚪 Last-Mile Gate (in place of its own Knows line) |
| `ariaCountGate` | 🩹 DeepSeek, only while the 🧪 Auto-Routing Quality Hardener is ON: the firmer Count line (the same if also adds the completion sentence to `ariaLedgerGate`; the Main Prompt blanks it first) | 🚪 Last-Mile Gate (in place of its own Count line) |
| `ariaHardPlan`, `ariaHardN` (Chibi Chat Completions only) | 🧪 Auto-Routing Quality Hardener sets the Claims line and counts it; each 🩹 patch then appends its plain rules while the switch is ON, a newline before each and none at the end (the Main Prompt blanks both first) | 🧠 The Logic Core and its system-role twin (they print the lines after Voice, add them to the line count and blank the variable), then the 🚪 Last-Mile Gate, which prints whatever is left: that is the 👹 jailbreak paths and no plan |
| `ariaAndChains` (Chibi Chat Completions only) | 🩹 DeepSeek, only while the 🧪 Auto-Routing Quality Hardener is ON (the same if also adds the completion sentence to `ariaLedgerGate`; the Main Prompt blanks it first) | 🚪 Last-Mile Gate (its Count line then names and-chains) |
| `ariaPatchTally` | 🩹 DeepSeek, when 🥰 Bonds or 🎲 Fate is ON (the Tally line; not blanked by the Impersonation Turn, because The Logic Core prints it only while a ledger line exists) | 🧠 The Logic Core (its Tally line, between Bonds and Ledger, and one more in its line count) |
| `ariaPatchJoins` | 🩹 DeepSeek (its Joins line); the 🔦 Flash Gate reads it to leave out its own Runs line and then blanks it, so with both on neither line shows | 🔦 Flash Gate, 🧠 The Logic Core (after the patch's lines, and one more in its line count), 🚪 Last-Mile Gate (after the patch's lines) |
| `ariaChopGate` | 🖋️ Anti-Slop Codex, overwritten by 🩹 Gemini | 🚪 Last-Mile Gate (its Chop line, or the Gemini patch's Speech line) |
| `ariaPlanCue` | 🧠 The Logic Core or its system-role twin, with either tags entry on | 🚪 Last-Mile Gate (its very last line) |
| `logicCoreLines` | 🧠 The Logic Core itself: 7 plus one per Mode, Fate, Bonds, Ledger, Layers, Tally and Joins line, plus the patch's own lines and the hardener's | 🧠 The Logic Core ("N dashed lines") |

On Impersonate, the 🪞 Impersonation Turn blanks the Fate, Bonds, ledger, dice, POV, Own words and Character Hold variables before the gate and The Logic Core read them, so the gate never asks for NPC speech on the turn the model writes your message. The Text Completions file has no Impersonation Turn, so its gate tells the model to skip the Own words, POV and Character Hold lines and the ledgers on a message written as you, and its plan leaves out the Fate, Bonds, Ledger, Layers and Tally lines there. Marinara has no Impersonate trigger for a section: on an Impersonate turn it leaves a preset's sections out and sends its own Impersonate instruction (**Chat Settings** → **Impersonate** → **Prompt Template**, else its built-in one), unless a preset is picked in that section's **Preset** menu. So the Marinara files' 🪞 Impersonation Turn checks Marinara's `lastGenerationType` macro and prints on Impersonate turns only: paste its lines into the Prompt Template, or pick my preset in the Preset menu.

### Where each feature lives

- **Personality Independence** is a label in the Main Prompt, applied on The Logic Core's Scene line.
- **NPC Voice + Dialogue Output, NPC Instincts + VAD Emotions and Female Vocal Acoustics** live together in 🎭 NPC Voice & Emotions, and The Logic Core's Voice line works out each speaker's VAD and live instinct every turn, the way BOLT's dialogue task did. RF's Kimi-profile killswitches (Comparative Emphasis, Staccato Chop, Anti-Briefing Register, Occupational Monomania) are the Contrast, Chop, Register and Work lines of the Anti-Slop Codex, each repeated as a short instruction in the 🚪 Last-Mile Gate. Beta 6 dropped NPC Voice's example lists, because MiMo copied them into the story.
- **Fate and Chekhov's Gun** share one ledger: will versus world, the quiet-turn ladder, consequence Bullets tied to your actions, world news, the danger ceiling, pursuits and collisions, aftermath turns, Residue and Ambitions. Since beta 6 the rules follow the dice in order: Tier reads A alone, Source reads B, and Form reads C once, so MiMo Flash stops adding the dice together. Ambient moments get one sentence at most, seen or heard where you are and folded into a paragraph about someone present, and their background texture is never brought up again. Ambitions now follow the wording of Realistic Frankenstein's Douyin Edition. A want you state in your own words that reaches past the scene is logged at 0/5 in the `ambitions:` ledger field and gains one step only when a closed thread served it.
- **The double slop gates** are one labelled line per pattern in the Anti-Slop Codex, plus one short instruction each in the Last-Mile Gate. Every line leads with what to write, since Kimi K3 follows "do this" lines best. The two repair examples for Contrast and Chop moved into the 🩹 Claude 5 patch, the only place left with quoted bad-to-good examples, because MiMo copies quoted examples. Kimi K3 kept writing "it's not X, it's Y" through every rule that only named the idea, so Contrast is now a check it can run word by word: a clause on not, n't or never (or a less/than tag) sitting next to one about the same subject gets cut, another speaker's line included, and the other half stands alone. A plain refusal, denial or correction stays.
- **The rest of Realistic Frankenstein's anti-slop modules** came back in compact form after GLM 5.3's assistant talk returned. Anti-Briefing Register's repair (an act, a name, a question or an accusation, before heavy news) and the Claude dialogue fix's rule on rating what was said sit in Register, which also took Anti-Omniscient NPCs' everyday register. Resolution Engine's lived-in detail opens Vocabulary, which gained the missing banned words as well. More Diverse Door Sounds and Emission Limits' say-more-in-fewer-words test for similes joined Senses, while General Anti-stiff Prose (5-8 and 15+ word sentences, traits folded into motion) and the 'Really Did It' fix (each fact once) joined Cadence. Cinematic Realism's litotes ban went to Cadence too, and its plain narration and negation-as-description rule sit in the Scene Engine's narration line. Cadence also bans antithesis, Comparative Emphasis's "zero balanced halves", which the word-level Contrast check can't see without a negation word. The Gemini therapist fix's permission-granting joined the engine's therapist list. Human Vocal Limits' redirect sits in NPC Voice, and the pico CoT's verdict check in Epistemic Limits, where any read of you stays the speaker's guess. The GLM Okay-Loop gate is the Filler line that the 🩹 GLM and 🩹 Kimi / Qwen patches add at depth 0. The GLM patch's Person line carries the game master's identity and Realistic NPCs' rule against yes-men into every character, and its Replies line is the two-speaker rule from Realistic Frankenstein's Claude edition, which the 🩹 Claude 5 patch shows as a repair example. Gemini's Cosmos fixes live in the 🩹 Gemini patch. The gate's opening words, "As game master", carry the identity line Realistic Frankenstein's plans ended on. After u/trashhaul's report, the gate's Trade line also carries the regular Vocation Gate's check for a trade's words used on things outside the work, and its Chop line joins verbless sentences and keeps an order's reason in the order's own sentence.
- **Beta 7's foundation fixes** come from u/trashhaul's report and Realistic Frankenstein's own lines: the comedy clause from Staccato Chop (force and comedy go into word choice or an act), Character Hold's reactions to your jokes, the Cosmos speech method for every model, break-the-triad's count, Card Fidelity's resting temperament at the end of the prompt, Occupational Monomania's quiet competence, the Claude dialogue fix's provenance test for words from the speaker's world, and the Fate rule that big events stay rare. The gate's new-name letter is gone, and newcomers keep to the edge of a scene.
- **The Scene Engine** lives in Voice & Scene Engine with its progression, pacing and endings, where quiet talk counts as progress and the last line is a character's act or line, as plain as the rest and never scenery. The engine's narration line reports deeds and words and leaves verdicts on manner or habits to the characters.
- **Card Fidelity and the language rules** are Main Prompt labels (Card Fidelity, Story Language, Epistemic Limits). Speech counts as "heard" however the story's language marks it, so Hungarian „quotes" and dialogue dashes work. Card Fidelity takes gender and pronouns from the card and first message (else lorebook or chat) and never guesses them from a name. The gate's Card line repeats the rule for names, ages, ties, history, bodies, pronouns, voice, the form of thoughts and each character's resting temperament at the very end of the prompt, and its closing line asks the AI to follow the gate over its own earlier replies.
- **The Logic Core** is sent with the assistant role after the history, or with the system role through its twin, inside the gate's message. With 🏷️ Logic Core Tags on it carries no wrapper tag and starts on `<thinking>` (or `<thought>` with the Gemini 4 Argon Thinking Tags Enforcer), the tag the reply has to open with. With them off it sits inside `<logic_core>` as before, since the plan then runs inside the model's own reasoning. Every other entry calls it "the plan", which reads right in both shapes and with The Logic Core off, so no other entry branches on the shape. The gate only prints the one-line reminder The Logic Core hands it. The plan has seven fixed lines plus the lines of the modules that run: Mode, Fate, Bonds, Ledger, 🧷 Character Hold's Layers, the 🩹 DeepSeek patch's Tally and Joins, and the patch's own lines. Each line builds on the last with no drafts, and with the tags on, `go` ends the thinking. Beta 6 dropped the Check line, because MiMo Flash recited the whole gate there, and beta 7 brought it back short; the gate opens on `As game master, write the prose per <anti_slop>:` and works as a set of instructions for the prose, with or without a plan. Since this update the plan carries Realistic Frankenstein's Micro chain of thought: the first-person game-master identity with creative risk over perfection, the rule that every line gets written in order and none skipped, Micro's neutrality and full actions in the Move line, its adult-mode question in the Mode line that 🔞 Adult Context and 😈 Freaky Override hand over, and, inside the model's own reasoning, its cue that reasoning ends at go. Micro's pointer to Realistic Frankenstein's legal-pretext and prefill blocks stayed out, since ARIA has neither.

---

That's the whole show! Thank you for sticking with me until the very end, Manager. Now go make some wonderful stories, and come cheer for us at the next concert~! 💖🎶

*Aria, lead singer of the Angels of Delusion*
