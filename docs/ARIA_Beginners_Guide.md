# 🎤 ARIA's Beginner's Guide

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
7. [Uh-oh! moments](#7-uh-oh-moments)
8. [Manager's corner (for the curious)](#8-managers-corner-for-the-curious)

---

## 1. Wait, what IS all this?

Every idol needs to know her stage before the show, so let's learn ours! Nangong made me memorise these before my first concert, and now it's your turn~

| Word | What it means |
|---|---|
| **SillyTavern** | The app you chat in. Think of it as the concert hall, with the stage and the seats in one place. |
| **AI model** | The singer on that stage: Claude, Gemini, DeepSeek, GLM, MiMo and friends. Each one has its own voice and its own bad habits. |
| **Preset** | The setlist and stage notes the app hands the model before every single reply. ARIA is a preset! |
| **Prompt** | Everything the model reads at once: the preset's rules, your character card, the chat so far and your newest message. |
| **Token** | The little chunks models read text in, about three quarters of an English word each. Providers bill you per token, so a lean preset means cheaper, faster replies. My rules come to roughly 3,200 tokens as shipped and about 4,100 with every single toggle on. |
| **Toggle** | The on/off switch next to each entry in the preset list. ON sends that entry to the model, OFF leaves it out. |
| **Character card** | The file that describes who you're talking to: looks, personality, first message. |
| **Lorebook** (World Info) | Notes about your world that pop into the prompt when their keywords show up in the chat. |
| **Reasoning** (thinking) | Some models think quietly before they answer. I bring my own short planning checklist for that, called The Logic Core. |
| **OOC** | "Out of character." Start a message with `OOC:` or wrap a note in `((double brackets))` to talk to the AI directly instead of to the characters. |
| **Prompt caching** | When the start of the prompt is identical to last time, many providers remember it and charge you much less for it. I'm built so that start stays identical. |
| **Chat Completion and Text Completion** | The two ways SillyTavern can talk to a model. Chat Completion is for online services like Claude, Gemini or OpenRouter. Text Completion is for models running on your own computer through apps like KoboldCpp or llama.cpp. I come as one file for each! |
| **Context window** | How much text a model can hold in its memory at once, counted in tokens. A 32k window fits about 24,000 words: my rules, your character card and as much of the chat as still fits. |
| **Instruct template** | The chat format a local model was trained on, like ChatML, Llama 3, Mistral or Gemma. Text Completion setups need the right one picked by hand. |
| **Regex scripts** | Tiny find-and-replace helpers that ship inside the preset. Mine fold the AI's thinking into a neat box and tidy up after Impersonate. |

---

## 2. Install me in five steps

Sunna timed this once and finished in under two minutes, and she was also tuning her guitar at the same time. You've got this! 💪

These steps are for the Chat Completions file. Running a model on your own computer instead? Hop over to [section 6](#6-run-me-on-your-own-computer)!

1. **Download** `Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json` from this repository. On GitHub, open the file and press the "Download raw file" button.
2. **Connect and import.** Open **API Connections** (the plug icon at the top), set **API** to **Chat Completion**, pick your provider and paste your key. Then open **AI Response Configuration** (the sliders icon at the top left), press **Import preset** next to the preset dropdown and choose the file.
3. **Say YES to the regex scripts.** SillyTavern asks whether to allow the scripts that come with the preset. Allow them, or my thinking box and the Impersonate clean-up won't work.
4. **Check the macro engine.** Open **User Settings** and make sure **Experimental Macro Engine** is ticked. New versions tick it for you. If you had to tick it yourself, reload the page afterwards. My dice and switches can't work without it!
5. **Pick a character** and say hi~

That's it! Everything I need is switched on already. Sections 3 and 5 make me fit your model and your wallet even better.

---

## 3. Pick your setup

Every Construct thinks a little differently, and AI models are the same! First, choose a thinking style:

**Style A: the model thinks on its own.** This suits most models. Leave **Request Model Reasoning** and **Reasoning Effort** as they are, and keep 🏷️ **Logic Core Tags** OFF. The model plans with my checklist inside its own thinking.

**Style B: for stubborn models.** Use this when a model's own thinking rambles for minutes, flattens the characters into cardboard or spills into the reply:

1. In **AI Response Configuration**, untick **Request Model Reasoning** and set **Reasoning Effort** to **Minimum**. (Claude keeps its own thinking on whatever you set here, so Claude users stay on style A.)
2. Switch 🏷️ **Logic Core Tags** ON.
3. Open **Advanced Formatting** (the big "A" icon) and find the **Reasoning** section. Tick **Auto-Parse** and leave **Add to Prompts** unticked. Then click **Reasoning Formatting** to open it, and set **Prefix** to `<thinking>` and **Suffix** to `</thinking>`.

Now my plan folds away into a little box above each reply, and it only takes a few seconds!

Then find your model in this table:

| Your model | Thinking style | Model patch | Anything else? |
|---|---|---|---|
| Claude 5 (Fable, Opus, Sonnet) | A | 🩹 Claude 5 | Set up caching in section 5, it saves a lot! |
| Gemini | A | 🩹 Gemini | Switch 👃 Scent Occasions OFF |
| GLM, Kimi, Qwen | A, or B if the thinking loops | 🩹 GLM / Kimi / Qwen | |
| DeepSeek | A | none | |
| MiMo V2.6 Pro | B first, A works too | none | |
| MiMo V2.6 Flash | B | 🩹 MiMo V2.6 Flash | |
| Something else | A, then B if it misbehaves | none | |

**One model patch at most!** Two patches at once would be like two lead singers grabbing the same microphone. 🎤🎤

The preset ships with Temperature 0.7 and Top P 0.8, which keep most models on track. If replies get strange (typos, derailing, weird logic), the 🌿 **Sampling Advice** entry explains what to adjust. It's a note for you and costs zero tokens.

---

## 4. Meet the toggles

Time to meet my whole band, member by member! Entries marked **ON** come switched on, and the ones marked **OFF** wait until you want them.

### The core lineup

- 🍃 **Custom Instructions** (ON). Your own rules! Click the pencil icon and write between the `{{.player-instructions =` line and its closing `}}`. Those rules outrank everything else. There's a second slot, `player-posthistory`, which lands at the very end of the prompt through the Last-Mile Gate: stronger, a bit blunter.
- ⚡ **ARIA Main Prompt** (ON). My heart and soul. It makes the AI your storyteller and game master and keeps every character true to their card. Characters keep their own tastes instead of copying yours, only know what they've seen or heard, take romance at a believable pace and talk in whatever language you write in. Writing in Hungarian, Slovak or Japanese? The whole story stays in it!
- 🎬 **Voice & Scene Engine** (ON). Makes scenes move and characters sound like people. They chase their own goals, react to what just happened before answering, negotiate and remember promises and insults. It also stops them from talking like therapists, and every reply ends right where it's your turn.
- 🖋️ **Anti-Slop Codex** (ON). My style rulebook against tired AI habits: "it wasn't anger, it was grief", choppy one-word sentences, characters announcing "here's the deal", shopkeepers who only talk about their shop, and overused words like "palpable" or "a beat".
- 👃 **Scent Occasions** (ON). Stops the AI from smelling everything! Smells only appear at meals, rituals or when something strong is right there, and at most once per scene. Gemini users, switch this OFF.
- ⏰ **Time & Place** (ON). Every reply starts with a little status line showing the time, day, date, place and weather in °C and °F, so time moves realistically and characters react to the cold or the late hour.
- 🎲 **Fate & Chekhov Ledger** (ON). My world engine! Every turn I roll three hidden dice to decide whether the world does something on its own: everyday background life, a small hiccup or, rarely, a big event. I also remember setups that should pay off later, deliver news the way your setting would (a radio, a rumour, a phone notification), keep appointments and make your actions ripple outward. I never decide your next move for you. My memory lives in a tiny folded 🎲 line at the end of each reply, so please leave that line in the chat.
- 📖 **Story Context** (ON). A tiny header telling the AI that what follows is your persona, the character card, the scenario, examples and lorebook.
- 🚪 **Last-Mile Gate** (ON). The final check right before a reply goes out. It runs through the anti-slop list, picks the first letter for any brand-new character's name (no more endless Elaras!) and carries this turn's dice.
- 🧠 **The Logic Core** (ON). My planning step! Before writing, the AI jots a few quick lines: your OOC requests, where everyone is, what each character knows and wants, how they sound, what happens next, then a last check. It arrives as the AI's own message after the chat, which helps many models settle into the scene.
- 🪞 **Impersonation Turn** (ON). Only fires when you press Impersonate. It writes your next message in your own voice, without the status line or the 🎲 line, so the input box gets nothing but your words.

### Optional extras

- 🏷️ **Logic Core Tags** (OFF). Turn ON for thinking style B (section 3). If your provider expects `<think>` instead of `<thinking>`, rename both tags inside this entry and in Advanced Formatting.
- 🔞 **Adult Context** (OFF). For adults only! It unlocks mature stories: sex, violence and dark themes written frankly. Characters stay themselves all the way through, so a shy character is still shy in bed.
- 😈 **Freaky Override** (OFF). The anything-goes switch. Characters drop their independence and the slow pacing and lean eagerly into what you want, while still sounding like themselves. It needs 🔞 Adult Context ON as well.
- 👀 **Hybrid POV** (OFF). Tells the story in third person, while everything your character feels is written straight to you: "the rain soaks through your sleeves". Super immersive!
- 🐺 **Anthro Vocals** (OFF). For furry, beastfolk and talking-animal stories. Wolves howl, eagles chirp, and lions and tigers roar and can't purr. The sounds stay as flavour inside normal speech.
- 🥰 **Bonds Lite** (OFF). A hidden relationship tracker. Every pair of characters gets a bond score from cold to chosen family, so friendships and romances grow at a believable pace. Reaching a level allows a hug or a confession and never forces one. Numbers never show up in the story.
- 🩹 **Model Patches** (OFF). Small fixes for one model family each. Pick the one from the table in section 3, and only one.
- 🧠 **The Logic Core (user-role twin)** (OFF). The same planning step, sent as your message. Use it instead of the normal Logic Core only if your provider complains about the AI's own message sitting near the end. Never run both!
- **Reduce Reasoning** (OFF). A tiny "don't overthink" note for models that think far too long. Switch it on alongside The Logic Core if your model still overthinks.
- 🌳 **README** and 🌿 **Sampling Advice** (OFF). Notes for you to read. Switching them on sends nothing.

---

## 5. Save money with caching

This part saves you real credits, so listen closely, Manager! 💰

Every time you send a message, the model reads the whole prompt again from the top. Caching lets the provider reuse whatever it read last time, as long as that part is identical, letter for letter. Reused tokens cost far less and come back faster. It's like me memorising the first verses of a song so that only the new lines need rehearsal.

I'm arranged to make that easy: all my rules come first and stay identical every turn, and anything that changes, like the dice or the new-name letter, rides along at the very end after your newest message.

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

1. **Download** `Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json` from this repository.
2. **Connect.** In **API Connections** (the plug icon), set **API** to **Text Completion**, pick your backend and connect.
3. **Import.** Open **Advanced Formatting** (the big "A" icon), press **Master Import** and choose the file. It fills in the Context Template and the System Prompt for you.
4. **Finish the setup.** In the same panel, make sure the **System Prompt** is switched on, and pick the **Instruct Template** that matches your model (ChatML, Llama 3, Mistral, Gemma and so on). The model's download page usually names it. I don't bring one, because every model family speaks its own format.
5. **Check the macro engine** in **User Settings**, just like in section 2: **Experimental Macro Engine** must be ticked.

### Flip my switches

Text Completions has no toggle list, so my switches live at the very top of the **System Prompt** box in Advanced Formatting. Each one looks like this:

```
{{.aria-fate = off}}
```

Change `off` to `on` (or the other way round) and the change kicks in on your next reply. Every line carries a little note, so you can't get lost! The full list:

| Switch | Starts | What it does | What it costs |
|---|---|---|---|
| `aria-logic-core` | off | 🧠 The Logic Core's planning checklist | ~310 tokens per turn, plus a few seconds of planning |
| `aria-thinking-tags` | on | With The Logic Core on: plan inside `<thinking>` tags (on) or inside the model's own `<think>` reasoning (off) | ~13 tokens |
| `aria-adult` | off | 🔞 Adult Context, for adults only | ~165 tokens |
| `aria-freaky` | off | 😈 Freaky Override, needs `aria-adult` on too | ~60 tokens |
| `aria-hybrid-pov` | off | 👀 Hybrid POV | ~40 tokens |
| `aria-anthro` | off | 🐺 Anthro Vocals | ~300 tokens |
| `aria-scent` | on | 👃 Scent Occasions | ~70 tokens |
| `aria-time-place` | off | ⏰ Time & Place status line | ~60 tokens, plus ~30 in every reply |
| `aria-fate` | off | 🎲 Fate & Chekhov Ledger | ~630 tokens, plus ~80 in every reply |
| `aria-bonds` | off | 🥰 Bonds Lite | ~210 tokens, plus ~20 to 40 in every reply |
| `aria-patch-glm-qwen` | off | 🩹 GLM / Kimi / Qwen patch | ~95 tokens |
| `aria-patch-mimo-flash` | off | 🩹 MiMo V2.6 Flash patch | ~95 tokens |

The Claude 5 and Gemini patches live only in the Chat Completions file, since those models aren't run through Text Completion. Use one patch at most, same as always!

### Fitting into 32k

My lean start uses about 2,200 tokens. Your character card usually takes 1,000 to 3,000 more, and everything else is chat. Most switches cost their tokens once per turn, while Time & Place, Fate and Bonds also leave a small line inside every reply, and those lines stay in the chat. After 100 replies, Fate's 🎲 lines alone add up to about 8,000 tokens, a quarter of a 32k window! My advice:

- **32k:** stay lean. Turn on The Logic Core only if your model has 24B parameters or more and a few extra seconds per reply don't bother you.
- **64k or more:** switch on `aria-fate` and `aria-time-place` together for the full world engine, and add `aria-bonds` if you love relationship drama~
- **Small models (12B and below):** keep Fate off whatever your context size, because its bookkeeping asks a lot of a small model.

### Thinking on a local model

The Logic Core asks your model to plan inside `<thinking>` tags. To fold that plan away and keep it out of the model's memory, open **Advanced Formatting**, tick **Auto-Parse** in the **Reasoning** section, open **Reasoning Formatting** and set **Prefix** to `<thinking>` and **Suffix** to `</thinking>`.

Models that already think on their own, like Qwen 3 or the DeepSeek R1 distills, use `<think>` instead. For them, set `aria-thinking-tags` to `off`, and make the Prefix `<think>` and the Suffix `</think>`.

### Keep it fast

Your backend remembers the prompt it read last time and only reads the new part, which makes replies start MUCH faster. I keep my rules at the very top where they never change, and everything that changes each turn (the dice, the new-name letter, The Logic Core) comes after your newest message. Help it out:

- In **KoboldCpp**, keep **FastForwarding** and **ContextShift** on, as they are by default. ContextShift lets old messages drop out of a full context without rereading everything, as long as the start of the prompt stays the same.
- Put lorebook entries that come and go on "@D ⚙️" with depth 0, or make them constant. I already placed the lorebook after the card and the examples, right before the chat.
- Keep the Author's Note off or at depth 0.
- Try not to flip switches mid-chat, because each flip makes the backend reread everything once.

### What's different from the Chat Completions file?

- Same rules, same writing, with switches in place of toggles.
- Time & Place, Fate, Bonds and The Logic Core start off to save memory.
- No Claude 5 or Gemini patches.
- No regex scripts come with this file, so set up Reasoning Formatting as above. If Impersonate ever leaves a plan in the input box, delete it by hand.

---

## 7. Uh-oh! moments

Even idols trip on stage sometimes! These fixes get you back up:

**I see strange bits like `{{setvar`, `{{roll` or `{{.aria-fate = off}}` in the prompt or the replies.**
The macro engine is off. Tick **Experimental Macro Engine** in User Settings and reload.

**The AI's thinking shows up inside the reply.**
In Advanced Formatting, tick **Auto-Parse**, open **Reasoning Formatting** and set **Prefix** and **Suffix** to your tags (section 3, style B). Check that the preset's regex scripts are allowed too, under **Extensions** → **Regex**.

**The model's thinking takes forever.**
Switch to thinking style B, or turn on the GLM / Kimi / Qwen patch if you use one of those models. On Claude, stay on style A and set **Reasoning Effort** to **Low** instead, because Claude keeps thinking whichever setting you pick.

**The 🎲 line vanished and the world forgot what was going on.**
Make sure 🎲 Fate & Chekhov Ledger is ON and that you didn't edit the line out of the AI's last reply. If you switched on the "Drop old ledgers" regex, switch it off again in **Extensions** → **Regex**.

**A character suddenly speaks English in my Hungarian story.**
Write your own messages in your story's language, or add an OOC note like `((OOC: the story is in Hungarian))`. The Main Prompt follows whatever language you use.

**Characters feel flat, or all agree with me.**
Check that 😈 Freaky Override is OFF, because it makes everyone eager on purpose. On MiMo V2.6 Flash, switch on its model patch.

**The model refuses or tiptoes around a scene.**
Keep The Logic Core ON, since it helps a lot of models settle in. For mature scenes, 🔞 Adult Context must be ON. Some models refuse certain content no matter what any preset says, and when that happens a different model is the only real fix.

**My local model takes ages to start every reply.**
Your backend is rereading the whole prompt each turn. Go through the "Keep it fast" list in section 6, especially the lorebook and switch tips.

**My local model writes its plan right into the reply.**
Set up Reasoning Formatting as shown in section 6. If the model still struggles, set `aria-logic-core` to `off`.

**After pressing Impersonate, the input box has junk in it.**
Allow the preset's regex scripts in **Extensions** → **Regex**. They clean the Impersonate result for you.

---

## 8. Manager's corner (for the curious)

Phew, that's everything a beginner needs! This last part is for nerdy Managers who want to peek under the hood, like Lewis, who helped me pack all of this into one file. Sunna fell asleep halfway through when I explained it to her, so no pressure~ 😴

### Token budget

Measured with `python3 tools/aria_budget.py`, which counts rendered text with comments stripped (characters ÷ 4):

| Chat Completions configuration | Tokens |
|---|---|
| Core (everything that ships ON except Fate and Time & Place) | ~2,470 |
| Shipped default | ~3,180 |
| Everything ON (Adult, Freaky, Hybrid POV, Anthro, Bonds, Logic Core Tags and the largest model patch) | ~4,085 |
| Extra on an Impersonate turn (🪞 entry plus SillyTavern's impersonation prompt) | ~196 |

The Text Completions file, measured the same way:

| Text Completions configuration | Tokens |
|---|---|
| Lean start, as shipped for 32k | ~2,184 |
| Plus The Logic Core, Fate and Time & Place | ~3,217 |
| Everything ON (largest patch included) | ~4,113 |

The script also fails if anything goes over 4,500 tokens, if a tag or label is referenced and never defined, if a variable is set and never read (or the reverse), or if anything would break prompt caching. Run it after every edit.

### Prompt order (Chat Completions)

| # | Entry | Where it goes | Default |
|---|---|---|---|
| 1 | 🌳 README, 🌿 Sampling Advice | notes only | off |
| 2 | 🍃 Custom Instructions | system block | on |
| 3 | ⚡ ARIA Main Prompt | system block | on |
| 4 | 🏷️ Logic Core Tags | system block, setter only | off |
| 5 | 🔞 Adult Context, 😈 Freaky Override, 👀 Hybrid POV | system block | off |
| 6 | 🎬 Voice & Scene Engine | system block | on |
| 7 | 🐺 Anthro Vocals | system block | off |
| 8 | 🖋️ Anti-Slop Codex, 👃 Scent Occasions | system block | on |
| 9 | ⏰ Time & Place, 🎲 Fate & Chekhov Ledger | system block | on |
| 10 | 🥰 Bonds Lite, 🩹 Model Patches | system block | off |
| 11 | 📖 Story Context | system block | on |
| 12 | Persona, card, personality, scenario, examples, then World Info before and after | system block | on |
| 13 | Chat History | | on |
| 14 | 🚪 Last-Mile Gate | In-Chat depth 0, system | on |
| 15 | 🧠 The Logic Core | In-Chat depth 0, assistant | on |
| 16 | 🧠 Logic Core twin, Reduce Reasoning | In-Chat depth 0, user | off |
| 17 | 🪞 Impersonation Turn | In-Chat depth 0, user, Impersonate only | on |

### Cache-first rules

These are checked against SillyTavern's own source code:

- In-Chat entries are spliced in after the newest message. At the same depth and order, SillyTavern writes them as assistant, then user, then system, so the Last-Mile Gate reads last, right after The Logic Core.
- For Claude, every system message before the chat becomes the cached system prompt, and later system messages are sent as user messages. That's why `cachingAtDepth: 2` skips the gate (depth 0) and The Logic Core (depth 1). On OpenRouter, SillyTavern skips system messages when it counts depth, so the markers land on the AI's two previous replies instead.
- Nothing in the system block changes between turns. Dice live inside `{{setvar}}`, which prints nothing there, and only print at the end through the gate. No system-block entry has generation triggers, so Impersonate reuses the same cache.
- World Info sits after the card and examples, so a lorebook change only re-reads what comes after it.
- Chat history never gets rewritten. The ledger-trimming regex ships disabled for that reason.

### The Text Completions edition

- The switches are chat variables set at the very top of the System Prompt (`{{.aria-fate = off}}`). The macro engine reads text from top to bottom, so every block below, like `{{#if .aria-fate}}`, already sees the new value. Empty, `off`, `false` and `0` all count as off.
- Each optional module sits inside a `{{#if}}` block. The `#` keeps whitespace exactly as written, so switched-off modules leave no blank lines behind.
- SillyTavern adds the post-history block as the last user message after your newest one. It holds The Logic Core (when switched on) and the Last-Mile Gate with the dice and the new-name letter, so the System Prompt stays identical every turn.
- The story string puts the card fields and examples first and World Info last, right before the chat.

### Wiring (Chat Completions)

The Main Prompt's first line blanks seven helper variables every turn, so a switched-off module leaves nothing behind:

| Variable | Set by | Read by |
|---|---|---|
| `ariaDice` | 🎲 Fate (three d20 rolls) | 🚪 Last-Mile Gate, which also clears it |
| `ariaFateLine` | 🎲 Fate | 🧠 The Logic Core |
| `ariaBondsLine` | 🥰 Bonds Lite | 🧠 The Logic Core |
| `ariaModeLine` | 🔞 Adult Context, overwritten by 😈 Freaky | 🧠 The Logic Core |
| `ariaScentGate` | 👃 Scent Occasions | 🚪 Last-Mile Gate |
| `ariaThinkOpen`, `ariaThinkClose` | 🏷️ Logic Core Tags | 🧠 The Logic Core (`{{#if .ariaThinkOpen}}`) |

### Where each feature lives

- **Personality Independence** is a label in the Main Prompt, applied on The Logic Core's Scene line.
- **Fate and Chekhov's Gun** share one ledger: will versus world, the quiet-turn ladder, consequence Bullets tied to your actions, world news, the danger ceiling, pursuits and collisions, aftermath turns, Residue and Ambitions.
- **The double slop gates** are one labelled line per pattern in the Anti-Slop Codex, plus one check line each in the Last-Mile Gate. Contrast and Chop each carry one repair example.
- **The Scene Engine** lives in Voice & Scene Engine with its progression, causality, pacing, initiative and handoff endings.
- **Card Fidelity and the language rules** are Main Prompt labels (Card Fidelity, Story Language, Epistemic Limits). Speech counts as "heard" however the story's language marks it, so Hungarian „quotes" and dialogue dashes work.
- **The Logic Core** is sent with the assistant role after the history.

### Known risks to test

- Fate is the most compressed piece. Mid-size or quantized models may forget to age entries or let Bullets pile up, so try it on a strong model first.
- With fewer repair examples, some Claude habits may creep back. The Claude patch and the gate are the first line of defence.
- A card whose first message shows no thoughts may make the narration go a little flat.
- Gemini runs best with Scent Occasions OFF and its patch ON; check that no smells sneak back in.
- Bonds can rise quickly, so watch long slice-of-life chats for confessions arriving too early.

### Live test plan

- **Plumbing:** with everything ON, open the prompt inspector twice in a row. The system block should match exactly, the dice and the name letter should change only in the last message, and Claude should report cache reads on the second turn. Switching Fate, Bonds, Adult, Freaky, Scent and Logic Core Tags off should remove their lines completely.
- **Claude 5 with its patch,** a two-character tavern scene over 30 turns: look for banned words, "it wasn't X, it was Y", choppy dialogue and "I respect that".
- **Gemini with its patch and Scent OFF:** no smells at all, at most one question per reply, and clumsy human reactions to heavy news.
- **GLM, Kimi or Qwen with their patch:** nervous characters keep their stammer; confident ones never mutter a filler word to themselves.
- **MiMo V2.6 Flash with its patch, style B:** card facts and moods hold from turn 15 to turn 25.
- **Fate over 20 turns:** the thread counter climbs and closes by 8, World stays at five entries or fewer, "meet me at noon on Day 3" fires on time, and harm reaching the scene stays rare.
- **Card fidelity:** a shy card stays shy under Adult Context, siblings recognise each other on turn 1, a drill sergeant keeps short orders, and a Hungarian chat stays free of English words.
- **Impersonate:** the input box gets only your character's words, in their own person and tense.
- **Blind A/B against your previous preset:** same three cards, 10 turns each on Claude 5 and Gemini, ranked by a reader who doesn't know which is which.

---

That's the whole show! Thank you for sticking with me until the very end, Manager. Now go make some wonderful stories, and come cheer for us at the next concert~! 💖🎶

*Aria, lead singer of the Angels of Delusion*
