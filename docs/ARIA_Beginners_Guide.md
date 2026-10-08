# 🎤 ARIA's Beginner's Guide

*For ARIA 1.0 beta 6, built for SillyTavern 1.19.0 or newer.*

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
| **Token** | The little chunks models read text in, about three quarters of an English word each. Providers bill you per token, so a lean preset means cheaper, faster replies. My rules come to roughly 3,580 tokens as shipped and about 4,430 with every single toggle on in the Chat Completions file, while the Text Completions file starts at about 2,405. |
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

These steps are for the Chat Completions file. Running a model on your own computer instead? Hop over to [section 6](#6-run-me-on-your-own-computer)! Either way, you need SillyTavern 1.19.0 or newer; its version shows on the welcome screen.

1. **Download** `Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json` from this repository. On GitHub, open the file and press the "Download raw file" button.
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

Does the reply still start straight with the story, with no plan anywhere? Switch 🧠 **The Logic Core** OFF and 🧠 **The Logic Core (system-role twin)** ON (section 4 explains the difference). Never run both at once!

Then find your model in this table:

| Your model | Thinking style | Model patch | Anything else? |
|---|---|---|---|
| Claude 5 (Fable, Opus, Sonnet) | A | 🩹 Claude 5 | Set up caching in section 5, it saves a lot! |
| Gemini | A | 🩹 Gemini | Switch 👃 Scent Occasions OFF |
| GLM, Kimi, Qwen | A, or B if the thinking loops | 🩹 GLM / Kimi / Qwen | GLM Flash: switch 🔦 Flash Gate ON too |
| DeepSeek | A | none | |
| MiMo V2.6 Pro | B first, A works too | 🩹 MiMo V2.6 | No plan in the replies? Use the system-role twin of The Logic Core |
| MiMo V2.6 Flash | B | 🩹 MiMo V2.6 | Switch 🔦 Flash Gate ON too |
| Something else | A, then B if it misbehaves | none | |

**One model patch at most!** Two patches at once would be like two lead singers grabbing the same microphone. 🎤🎤 The 🔦 Flash Gate is the one exception: it's a small add-on for Flash-tier models, so it plays alongside their patch.

The preset ships with Temperature 0.7 and Top P 0.8, which keep most models on track. If replies get strange (typos, derailing, weird logic), the 🌿 **Sampling Advice** entry explains what to adjust. It's a note for you and costs zero tokens.

---

## 4. Meet the toggles

Time to meet my whole band, member by member! Entries marked **ON** come switched on, and the ones marked **OFF** wait until you want them.

### The core lineup

- 🍃 **Custom Instructions** (ON). Your own rules! Click the pencil icon and write between the `{{.player-instructions =` line and its closing `}}`. Those rules outrank everything else. There's a second slot, `player-posthistory`, which lands at the very end of the prompt through the Last-Mile Gate: stronger, a bit blunter.
- ⚡ **ARIA Main Prompt** (ON). My heart and soul. It makes the AI your storyteller and game master and keeps every character true to their card, right down to their body, so a sphinx with jackal ears grows no tail her card never gave her. Each character's gender and pronouns come from the card and first message, or else from the lorebook or chat, so a name alone never decides them. Characters keep their own tastes instead of copying yours, only know what they've seen or heard, keep their secrets until you uncover them, call you by your name until you pick a new one, take romance at a believable pace and talk in whatever language you write in. Writing in Hungarian, Slovak or Japanese? The whole story stays in it!
- 🎬 **Voice & Scene Engine** (ON). Makes scenes move and characters sound like people. They chase their own goals, negotiate and remember promises and insults, and every change in a scene has a cause you can see on the page. The narrator reports what people do and say and leaves verdicts on anyone's manner or habits to the characters. It also stops characters from talking like therapists, and every reply ends right where it's your turn.
- 🎭 **NPC Voice & Emotions** (ON). Realistic Frankenstein's dialogue engine, back in full working order! Every character talks like their card's example lines, with their own dialect, slang and quirk, in flowing full sentences instead of choppy one-liners, and speech fills about a third to half of each reply. Their mood, energy and sense of control bend their tone, pace, posture and words while they stay themselves. Little instincts like hunger, comfort or fear tug at them too, and their own judgment still decides what they do about it.
- 🖋️ **Anti-Slop Codex** (ON). My style rulebook against tired AI habits: "it wasn't anger, it was grief", choppy one-word sentences, mouths that open, close and open again, characters announcing "here's the deal", shopkeepers who only talk about their shop, and overused words like "palpable" or "a beat". Since beta 6, every one of my rules starts by telling the AI what to write, because Kimi K3 listens best when I say "do this"! The prose opens on what someone does or says. Each sentence grows out of the one before, and speech sits in the paragraph of the act it belongs to. Replies answer the one or two points of your message that move the scene most, and a detail I used sits out the next four replies, with reworded repeats counted too.
- 👃 **Scent Occasions** (ON). Stops the AI from smelling everything! Smells only appear at meals, rituals or when something strong is right there within reach, at most once per scene and never as the first thing in a reply or a new room. Nobody sniffs out who you are or how you feel, either. Gemini users, switch this OFF.
- ⏰ **Time & Place** (ON). Every reply starts with a little status line showing the time, day, date, place and weather in °C and °F, so time moves realistically and characters react to the cold or the late hour.
- 🎲 **Fate & Chekhov Ledger** (ON). My world engine! Every turn I roll three hidden dice to decide whether the world does something on its own: everyday background life, a small hiccup or, rarely, a big event. I read the dice one at a time, so there's never a total for a model to add up: the first sets how big the moment is, and the other two pick where it comes from and what shape it takes. Background life gets two sentences at most and never comes back later. I also remember setups that should pay off later, deliver news the way your setting would (a radio, a rumour, a phone notification), keep appointments and make your actions ripple outward. State a goal in your own words that reaches past the current scene, and I log it as an ambition that moves a step closer each time a story thread that served it wraps up. I never decide your next move for you. Scene-breaking surprises, like someone getting hurt or everyone being sent outside, only happen on the rarest roll, so the scene you're in carries on. My memory lives in a tiny 🎲 ledger at the end of each reply, which shows up as an orange **Fate & Routine** panel you can click open. Please leave it in the chat, because that's where I remember everything!
- 📖 **Story Context** (ON). A tiny header telling the AI that what follows is your persona, the character card, the scenario, examples and lorebook.
- 🚪 **Last-Mile Gate** (ON). The last word right before a reply goes out. It turns each anti-slop rule into one short instruction, since Kimi skipped right past the questions I used to ask there. Its Card line keeps names, ages, counts, ties, history, bodies, pronouns and voice the way the card and its first message set them, with the lorebook filling any gaps, and it keeps characters' thoughts in the form and frequency the card shows. A closing rule tells the AI to follow these lines over its own earlier replies, and the card outranks them all. The gate also picks the first letter for any brand-new character's name (no more endless Elaras!) and carries this turn's dice.
- 🧠 **The Logic Core** (ON). My planning step! Before writing, the AI jots a few quick lines: your OOC requests, where everyone is, what each character knows and wants, how they sound, the one step that happens next and which fresh details to bring in. Each line builds on the last, and the whole plan stays shorter than one paragraph, with no drafts. With 🏷️ Logic Core Tags on, `go` ends the thinking. My plan used to end on a last check, and MiMo Flash just recited my whole gate there, so I took it out! The plan arrives as the AI's own message after the chat, which helps many models settle into the scene.
- 🪞 **Impersonation Turn** (ON). Only fires when you press Impersonate. It writes your next message in your own voice, without the status line or the 🎲 line, so the input box gets nothing but your words.

### Optional extras

- 🏷️ **Logic Core Tags** (OFF). Turn ON for thinking style B (section 3). Every reply then opens with my plan inside `<thinking>` tags, the trick for models whose own thinking runs wild. Keep the tag name `<thinking>`: with the tags on, The Logic Core starts on that tag, and hosts running Qwen, GLM or DeepSeek reasoning models cut a message at a `</think>` tag, which would hide my whole checklist.
- 🔞 **Adult Context** (OFF). For adults only! It unlocks mature stories: sex, violence and dark themes written frankly. Characters stay themselves all the way through, so a shy character is still shy in bed.
- 😈 **Freaky Override** (OFF). The anything-goes switch. Characters drop their independence and the slow pacing and lean eagerly into what you want, while still sounding like themselves. It needs 🔞 Adult Context ON as well.
- 👀 **Hybrid POV** (OFF). Tells the story in third person, while everything your character feels is written straight to you: "the rain soaks through your sleeves". Super immersive!
- 🐺 **Anthro Vocals** (OFF). For furry, beastfolk and talking-animal stories. Wolves howl, eagles chirp, and lions and tigers roar and can't purr. The sounds stay as flavour inside normal speech.
- 🥰 **Bonds Lite** (OFF). A hidden relationship tracker. Every pair of characters gets a bond score from cold to chosen family, so friendships and romances grow at a believable pace. Reaching a level allows a hug or a confession and never forces one. The numbers sit in their own little 💚 ledger at the end of each reply, which my regex scripts draw as a teal **Bonds** panel with one card per pair. Here's how the numbers move: warm moments only fill Sparks, never the bond itself. The 💚 ledger opens with a little `turn n/5` counter, and on every fifth turn a pair holding 7 or more Sparks trades them for one point of bond and starts again from zero. The bond moves directly only on a big moment (an insult or dismissal, a betrayal, a costly rescue), and 5 Grudge cost it a point. The touch levels are just thresholds that allow a hug or a kiss, never points to add. I spelled all this out because MiMo V2.6 Pro kept raising the bond and the Sparks together on every warm act~
- 🩹 **Model Patches** (OFF). Small fixes for one model family each. Pick the one from the table in section 3, and only one. The 🩹 MiMo V2.6 patch covers Pro and Flash alike. The 🩹 Claude 5 patch holds the only quoted before-and-after examples in the whole preset, two repairs for the Contrast and Chop rules, since Claude learns from them while MiMo copies quoted examples word for word.
- 🔦 **Flash Gate** (OFF). For the Flash-tier models, GLM Flash and MiMo V2.6 Flash. They keep borrowing office words like "filing" and "notarising" for feelings, even in tender scenes where nobody is doing paperwork, while the full-size models dropped that habit. This swaps the gate's short Trade line for one firmer work-words rule at the end of the 🚪 Last-Mile Gate, where Flash models listen best. Run it alongside your model patch.
- 🧠 **The Logic Core (system-role twin)** (OFF). The same planning step, sent as a system message that joins the 🚪 Last-Mile Gate at the very end of the prompt. Some models, like MiMo V2.6 Pro on a few providers lately, skip a plan that arrives as the AI's own message, and this version reaches them as an instruction instead. Switch the normal Logic Core OFF when you switch this one ON, and never run both! Claude turns late system messages into your messages, so Claude users keep the normal one. There's no version sent as your message, because a plan in your voice breaks the jailbreak on these models.
- **Reduce Reasoning** (OFF). A tiny "don't overthink" note for models that think far too long. Switch it on alongside The Logic Core if your model still overthinks.
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
3. **Import.** Open **Advanced Formatting** (the big "A" icon), press **Master Import** and choose the file. A window asks what to import: keep **Context Template** and **System Prompt** ticked and press **Import**. Both dropdowns should now read **ARIA 1.0 beta 6 (Text Completions)**. If they say "Geechan - Universal Roleplay", you grabbed the file from the wrong branch: switch GitHub's branch selector to `beta` and download it again.
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
| `aria-logic-core` | off | 🧠 The Logic Core's planning checklist | ~325 tokens per turn as shipped, plus a few seconds of planning |
| `aria-thinking-tags` | on | With The Logic Core on: every reply opens with the plan inside `<thinking>` tags (on), or the plan runs inside the model's own `<think>` reasoning (off) | ~40 tokens, already counted in the Logic Core's 325 |
| `aria-adult` | off | 🔞 Adult Context, for adults only | ~110 tokens |
| `aria-freaky` | off | 😈 Freaky Override, needs `aria-adult` on too | ~55 tokens |
| `aria-hybrid-pov` | off | 👀 Hybrid POV | ~50 tokens |
| `aria-npc-voice` | on | 🎭 NPC Voice & Emotions, Realistic Frankenstein's dialogue engine | ~335 tokens |
| `aria-anthro` | off | 🐺 Anthro Vocals | ~120 tokens |
| `aria-scent` | on | 👃 Scent Occasions | ~115 tokens |
| `aria-time-place` | off | ⏰ Time & Place status line | ~70 tokens, plus ~30 in every reply |
| `aria-fate` | off | 🎲 Fate & Chekhov Ledger | ~820 tokens, plus ~90 in every reply |
| `aria-bonds` | off | 🥰 Bonds Lite | ~315 tokens, plus ~20 to 40 in every reply |
| `aria-patch-glm-qwen` | off | 🩹 GLM / Kimi / Qwen patch | ~50 tokens |
| `aria-patch-mimo-flash` | off | 🩹 MiMo V2.6 patch for Pro and Flash. The switch keeps its old name, so switch lines you saved from beta 5 still work | ~95 tokens |
| `aria-flash-gate` | off | 🔦 Flash Gate for GLM Flash and MiMo V2.6 Flash; runs alongside a patch | ~30 tokens, since it takes the place of the gate's Trade line |

The Claude 5 and Gemini patches live only in the Chat Completions file, since those models aren't run through Text Completion. Use one patch at most, same as always!

### Fitting into 32k

My lean start uses about 2,405 tokens, and SillyTavern also keeps your Response (tokens) free for the reply. Your character card usually takes 1,000 to 3,000 more, and everything else is chat. Most switches cost their tokens once per turn, while Time & Place, Fate and Bonds also leave a small line inside every reply, and those lines stay in the chat. After 100 replies, Fate's 🎲 lines alone add up to about 9,000 tokens, more than a quarter of a 32k window! My advice:

- **32k:** stay lean. Turn on The Logic Core only if your model has 24B parameters or more and a few extra seconds per reply don't bother you.
- **64k or more:** switch on `aria-fate` and `aria-time-place` together for the full world engine, and add `aria-bonds` if you love relationship drama~
- **Small models (12B and below):** keep Fate off whatever your context size, because its bookkeeping asks a lot of a small model.

### Thinking on a local model

The Logic Core asks your model to plan inside `<thinking>` tags. To fold that plan away and keep it out of the model's memory, open **Advanced Formatting**, tick **Auto-Parse** in the **Reasoning** section, open **Reasoning Formatting** and set **Prefix** to `<thinking>` and **Suffix** to `</thinking>`. Leave **Add to Prompts** unticked, so old plans never eat into your memory.

Models that already think on their own, like Qwen 3 or the DeepSeek R1 distills, use `<think>` instead. For them, set `aria-thinking-tags` to `off`, and make the Prefix `<think>` and the Suffix `</think>`.

### Pretty panels and tidy thinking

The Text Completions file can't carry regex scripts, so mine come in their own little file! Download `regex/ARIA 1.0 Regex Scripts (Text Completions).json` from the `beta` branch, open **Extensions** (the cubes icon at the top), then **Regex**, press **Import**, pick the file and choose **Global** when SillyTavern asks where the scripts go. Updating from an older build? Delete every script whose name starts with ARIA from the **Global** list first, then import the new file. SillyTavern adds imported scripts next to the ones you already have, and the old copies run first, so my newer clean-up tricks would miss their chance. From then on:

- the 🎲 ledger shows up as the orange **Fate & Routine** panel and the 💚 ledger as the teal **Bonds** panel, with bond bars (section 4 explains every row);
- a plan the model wrote without its tags still folds into a 💭 **Thoughts** box and stays out of what the model rereads, even when it opens with a bare `thinking` line instead of `<thinking>`;
- Impersonate leaves only your character's words in the input box.

The panel scripts only change what you see, so your backend's prompt reuse keeps working. The clean-up scripts also tidy each message you send, which is how they empty the input box after Impersonate. Global scripts run with every preset, and you can switch any of them off in the same list. Already using my Chat Completions file too? That's fine, the two copies don't trip over each other.

### Keep it fast

Your backend remembers the prompt it read last time and only reads the new part, which makes replies start MUCH faster. I keep my rules at the very top where they never change, and everything that changes each turn (the dice, the new-name letter, The Logic Core) comes after your newest message. Help it out:

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

## 7. Uh-oh! moments

Even idols trip on stage sometimes! These fixes get you back up:

**I see strange bits like `{{setvar`, `{{roll` or `{{.aria-fate = off}}` in the prompt or the replies.**
The macro engine is off. Tick **Experimental Macro Engine** in User Settings and reload.

**The AI's thinking shows up inside the reply.**
In Advanced Formatting, tick **Auto-Parse**, open **Reasoning Formatting** and set **Prefix** and **Suffix** to your tags (section 3, style B). Check that the preset's regex scripts are allowed too, under **Extensions** → **Regex**; they fold a plan into a 💭 **Thoughts** box even when the model forgets its tags. On the Text Completions file, import my regex file from section 6 as well. If the model with native reasoning off skips the plan or writes it loosely, make sure 🏷️ **Logic Core Tags** is ON (style B), since that's the switch that tells it to open every reply with `<thinking>`. On the Text Completions file, that's `aria-thinking-tags`, which ships `on`.
Does the reply open with a bare `thinking` line, with no angle brackets, then the plan? MiMo V2.6 Pro on NanoGPT sometimes drops the brackets like that, and the closing line may be `</thinking>`, `/thinking`, a bare `thinking` or missing altogether. Auto-Parse can't catch it, but my regex scripts can: they fold that plan into the 💭 **Thoughts** box and keep it out of what the model rereads. They only treat `thinking` as a plan opener when it stands alone on the reply's first line, so a story that starts "Thinking about it, she…" stays untouched. Still seeing it? Grab the current preset (or the regex file from section 6 on the Text Completions file).

**The plan lands in a purple 💭 Thoughts box instead of SillyTavern's own reasoning box.**
SillyTavern's **Auto-Parse** only catches a reply whose very first characters match your **Prefix**, so check that the Prefix is exactly `<thinking>` and the Suffix exactly `</thinking>`, with no spaces. Before beta 5, MiMo liked to copy the `<logic_core>` label my planning note started with, and SillyTavern can't parse that one. From beta 5 on, The Logic Core starts on `<thinking>` itself whenever 🏷️ Logic Core Tags is ON, so check that your 🌳 README entry (or the Text Completions template name) says beta 6, the current build. If it doesn't, re-import the preset, and on the Text Completions file swap in the new regex file from section 6 too. A time header written above the plan blocks Auto-Parse as well; my regex scripts still fold the plan then, which is exactly what the purple box is there for.
Does SillyTavern's own reasoning box show up as well, full of the model's free-form musings, while my checklist sits in the purple box below it? Then your provider still sends the model's native reasoning, and SillyTavern skips Auto-Parse for any reply that already carries some, however neatly it opens with `<thinking>`. Untick **Request Model Reasoning** and set **Reasoning Effort** to **Minimum** again (section 3, style B). If that provider keeps thinking anyway, style A suits it better!

**The plan never shows up, and the reply starts straight with the story.**
First check that **Request Model Reasoning** is unticked and 🏷️ **Logic Core Tags** is ON. If the model still skips the plan, switch 🧠 **The Logic Core** OFF and 🧠 **The Logic Core (system-role twin)** ON, so the plan arrives as an instruction inside the very last message. MiMo V2.6 Pro follows that version more often on some providers. If the twin makes no difference on your model, switch back, since a few chat formats move every system message to the top of the prompt. A long pause before the first word with no plan in sight means the model still thinks in secret on its own, and style A suits it better.

**The model's thinking takes forever.**
Switch to thinking style B, or turn on the GLM / Kimi / Qwen patch if you use one of those models. On Claude, stay on style A and set **Reasoning Effort** to **Low** instead, because Claude keeps thinking whichever setting you pick. On the Text Completions file, set `aria-logic-core` to `off`, or set `aria-patch-glm-qwen` to `on` for those models.

**The 🎲 ledger shows up as plain text instead of a panel.**
Allow the preset's regex scripts under **Extensions** → **Regex**, or import my regex file on the Text Completions file (section 6). If the scripts are on and one reply still looks raw, the model wrote its ledger in an odd shape, like fields split over several lines or a ledger without its 🎲. The next reply usually fixes itself, and the engine reads the plain text just fine either way.

**The bonds show up as a loose line or a bare card under the 🎲 panel.**
That's a beta 3 habit! From beta 4 on, Bonds keeps its own 💚 ledger, and my regex scripts tuck a stray bonds line from older replies into the teal panel too. Re-import the preset, and on the Text Completions file import the new regex file as well (section 6).

**The 🎲 line vanished and the world forgot what was going on.**
Make sure 🎲 Fate & Chekhov Ledger is ON and that you didn't edit the line out of the AI's last reply. If you switched on the "Drop old ledgers" regex, switch it off again in **Extensions** → **Regex**. Also check that **Trim Incomplete Sentences** in **Advanced Formatting** is unticked, because it cuts that line in half. On the Text Completions file, check that `aria-fate` is `on` and that **Response (tokens)** is large enough (section 6), since a reply cut off at the limit loses the 🎲 line.

**A character suddenly speaks English in my Hungarian story.**
Write your own messages in your story's language, or add an OOC note like `((OOC: the story is in Hungarian))`. The Main Prompt follows whatever language you use.

**Characters repeat my words back to me.**
That's parroting, and Kimi K3 and GLM love it: a reply opens on your own line, like your pet name handed back as a question. My 🖋️ Anti-Slop Codex already tells the AI to answer the meaning of your message in the character's own words, and the 🚪 Last-Mile Gate repeats that as its Echo line, so the part only you can fix is the chat itself. Every reply that opens on your words stays in the history, and the model copies its shape on later turns, so one echo grows into a habit. Edit or delete those openers as soon as they show up, and judge any fix on a clean chat over several turns, since swipes inside a chat that already echoes keep echoing.

**A character gets the wrong gender or pronouns.**
Start with the character's lorebook entry. Pronouns scattered through a description are a weak signal, and a model that half-knows the name can trust its own guess over them. Open the entry with one plain sentence that says who the character is in a gendered word, like "a doting mother figure for Soukaku" for Yanagi or "the only man in Section 6" for Harumasa. That one sentence stopped Kimi K3 from calling a woman "he" in our tests! An entry also reaches the AI only once its keywords show up in the last few messages, so a character the AI brings on stage by itself can walk in before their entry does. Open that reply's **Prompt** button in the message menu and look for the entry, and if it's missing, set the entry to **Constant** (the 🔵 blue circle). Still wrong with both in place? Tell me which model slipped.

**GLM Flash or MiMo Flash keeps turning feelings into paperwork.**
Switch the 🔦 Flash Gate ON next to your model patch. The patch handles the model's other habits, and the Flash Gate swaps the gate's short Trade line for its firmer office-word rule at the very end of the prompt, where Flash models listen best.

**Characters feel flat, or all agree with me.**
Check that 😈 Freaky Override is OFF, because it makes everyone eager on purpose. On MiMo V2.6 Pro or Flash, switch on the 🩹 MiMo V2.6 patch.

**The model refuses or tiptoes around a scene.**
Turn The Logic Core ON (on the Text Completions file, set `aria-logic-core` to `on`), since it helps a lot of models settle in. For mature scenes, 🔞 Adult Context must be ON. Some models refuse certain content no matter what any preset says, and when that happens a different model is the only real fix.

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

## 8. Manager's corner (for the curious)

Phew, that's everything a beginner needs! This last part is for nerdy Managers who want to peek under the hood, like Lewis, who helped me pack all of this into one file. Sunna fell asleep halfway through when I explained it to her, so no pressure~ 😴

### Token budget

Measured with `python3 tools/aria_budget.py`, which counts rendered text with comments stripped (characters ÷ 4):

| Chat Completions configuration | Tokens |
|---|---|
| Core (everything that ships ON except Fate and Time & Place) | ~2,650 |
| Shipped default | ~3,580 |
| Everything ON (Adult, Freaky, Hybrid POV, Anthro, Bonds, Logic Core Tags, 🔦 Flash Gate and the largest model patch) | ~4,430 |
| Extra on an Impersonate turn (🪞 entry plus SillyTavern's impersonation prompt) | ~70 |

For comparison, Realistic Frankenstein 2.2.1.3 set up the same way (its Fate & Routine engine, Chekhov's Gun, the killswitches, the last-mile gates and a model patch) renders about 23,800 tokens, so everything-ON ARIA is roughly 82% smaller. Beta 5 came to about 4,385 with everything ON, so beta 6 sits about 45 tokens above it, most of that the clearer Bonds rule, even with the Realistic Frankenstein rules it brought back.

The Text Completions file, measured the same way:

| Text Completions configuration | Tokens |
|---|---|
| Lean start, as shipped for 32k | ~2,405 |
| Plus The Logic Core, Fate and Time & Place | ~3,670 |
| Everything ON (largest patch and 🔦 Flash Gate included) | ~4,480 |

Beta 5 measured about 4,430 here with everything ON. Want to compare the two builds for yourself? Beta 5 waits in `archive/ARIA 1.0 beta 5/` with its presets and regex file, plus `Model fixes.md`, which lists all 139 model fixes it carried. Its presets carry their own names, so you can import them next to the current ones. Its regex file uses the same script names as mine, so on the Text Completions file swap it in only while you test beta 5 and put the current file back afterwards, the way section 6 describes.

The script also fails if anything goes over 4,500 tokens, if a tag or label is referenced and never defined, if a variable is set and never read (or the reverse), if an entry reads a variable before anything earlier in the list sets it, if any render with 🏷️ Logic Core Tags on still names `<logic_core>`, or if anything would break prompt caching. It checks every combination of the tags, each Logic Core (or none), each model patch and Impersonate. Run it after every edit.

### Prompt order (Chat Completions)

| # | Entry | Where it goes | Default |
|---|---|---|---|
| 1 | 🌳 README, 🌿 Sampling Advice | notes only | off |
| 2 | 🍃 Custom Instructions | system block | on |
| 3 | ⚡ ARIA Main Prompt | system block | on |
| 4 | 🏷️ Logic Core Tags | system block, setter only | off |
| 5 | 🔞 Adult Context, 😈 Freaky Override, 👀 Hybrid POV | system block | off |
| 6 | 🎬 Voice & Scene Engine, 🎭 NPC Voice & Emotions | system block | on |
| 7 | 🐺 Anthro Vocals | system block | off |
| 8 | 🖋️ Anti-Slop Codex, 👃 Scent Occasions | system block | on |
| 9 | ⏰ Time & Place, 🎲 Fate & Chekhov Ledger | system block | on |
| 10 | 🥰 Bonds Lite, 🩹 Model Patches, 🔦 Flash Gate (setter only) | system block | off |
| 11 | 📖 Story Context | system block | on |
| 12 | Persona, card, personality, scenario, examples, then World Info before and after | system block | on |
| 13 | Chat History | | on |
| 14 | 🪞 Impersonation Turn | In-Chat depth 0, user, Impersonate only; it comes first so it can clear the Fate, Bonds, ledger, POV and Echo lines before The Logic Core and the gate read them | on |
| 15 | 🧠 The Logic Core | In-Chat depth 0, assistant | on |
| 16 | 🧠 The Logic Core (system-role twin) | In-Chat depth 0, system, merged into the gate's message | off |
| 17 | 🚪 Last-Mile Gate | In-Chat depth 0, system | on |
| 18 | Reduce Reasoning | In-Chat depth 0, user | off |

### Cache-first rules

These are checked against SillyTavern's own source code:

- In-Chat entries are spliced in after the newest message. At the same depth and order, SillyTavern writes them as assistant, then user, then system, so the Last-Mile Gate reads last, right after The Logic Core. Entries with the same role merge into one message in list order, so the system-role twin and the gate travel together as the final message.
- SillyTavern reads the macros in list order, wherever each message lands. Both Logic Cores therefore sit above the gate in the list: the gate prints their closing cue (`ariaPlanCue`) as its very last line.
- For Claude, every system message before the chat becomes the cached system prompt, and later system messages are sent as user messages. That's why `cachingAtDepth: 2` skips the gate (depth 0) and The Logic Core (depth 1). On OpenRouter, SillyTavern skips system messages when it counts depth, so the markers land on the AI's two previous replies instead.
- Nothing in the system block changes between turns. Dice live inside `{{setvar}}`, which prints nothing there, and only print at the end through the gate. No system-block entry has generation triggers, so Impersonate reuses the same cache.
- World Info sits after the card and examples, so a lorebook change only re-reads what comes after it.
- Chat history never gets rewritten. The ledger-trimming regex ships disabled for that reason.
- The panel, row, label and bond-bar scripts are display-only, so the prompt stays exactly as written. The four thinking strips (tagged plans, mismatched tags, untagged plans and a copied Logic Core) run on every depth, so a message reads the same to the model on every turn after it's written. Since beta 6 the four scripts that fold or strip tagged and mismatched thinking look 40,000 characters ahead, twice the old window, so even a very long MiMo Flash reasoning block folds on screen and stays out of the prompt.

### The Text Completions edition

- The switches are chat variables set at the very top of the System Prompt (`{{.aria-fate = off}}`). The macro engine reads text from top to bottom, so every block below, like `{{#if .aria-fate}}`, already sees the new value. Empty, `off`, `false` and `0` all count as off.
- Each optional module sits inside a `{{#if}}` block, with its closing line break inside the block too. The `#` keeps whitespace exactly as written, so a switched-on module keeps that line break and the next one starts on a fresh line, while a switched-off module prints nothing at all.
- SillyTavern adds the post-history block as the last user message after your newest one. It holds The Logic Core (when switched on) and the Last-Mile Gate with the dice and the new-name letter, so the System Prompt stays identical every turn.
- The story string puts the card fields and examples first and World Info last, right before the chat. That only holds with **Example Messages Behavior** on **Never include examples**; otherwise SillyTavern sends a second copy of the examples after the story string.
- The context template ships with **Trim Incomplete Sentences** off, since the 🎲 and 💚 lines end in an HTML tag that the trimmer doesn't count as the end of a sentence.

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
| `ariaThinkOpen`, `ariaThinkClose` | 🏷️ Logic Core Tags | 🧠 The Logic Core (`{{#if .ariaThinkOpen}}`) |
| `ariaLedgerLine`, `ariaLedgerGate` | 🎲 Fate, or 🥰 Bonds Lite when Fate is off (with both on, Bonds rewrites them so the 🎲 block is followed by its own 💚 block) | 🧠 The Logic Core, 🚪 Last-Mile Gate |
| `ariaEchoGate` | 🖋️ Anti-Slop Codex | 🚪 Last-Mile Gate (its Echo line) |
| `ariaFlashGate` | 🔦 Flash Gate | 🚪 Last-Mile Gate |
| `ariaPlanCue` | 🧠 The Logic Core or its system-role twin, with 🏷️ Logic Core Tags on | 🚪 Last-Mile Gate (its very last line) |
| `logicCoreLines` | 🧠 The Logic Core itself: 6 plus one per Mode, Fate, Bonds and Ledger line | 🧠 The Logic Core ("N dashed lines") |

On Impersonate, the 🪞 Impersonation Turn blanks the Fate, Bonds, ledger, dice, POV and Echo variables before the gate and The Logic Core read them, so the gate never asks for NPC speech on the turn the model writes your message. The Text Completions file has no Impersonation Turn, so its gate tells the model to skip the Echo line and the ledgers on a message written as you.

### Where each feature lives

- **Personality Independence** is a label in the Main Prompt, applied on The Logic Core's Scene line.
- **NPC Voice + Dialogue Output, NPC Instincts + VAD Emotions and Female Vocal Acoustics** live together in 🎭 NPC Voice & Emotions, and The Logic Core's Voice line works out each speaker's VAD and live instinct every turn, the way BOLT's dialogue task did. RF's Kimi-profile killswitches (Comparative Emphasis, Staccato Chop, Anti-Briefing Register, Occupational Monomania) are the Contrast, Chop, Register and Trade lines of the Anti-Slop Codex, each repeated as a short instruction in the 🚪 Last-Mile Gate. Beta 6 dropped NPC Voice's example lists, because MiMo copied them into the story.
- **Fate and Chekhov's Gun** share one ledger: will versus world, the quiet-turn ladder, consequence Bullets tied to your actions, world news, the danger ceiling, pursuits and collisions, aftermath turns, Residue and Ambitions. Since beta 6 the rules follow the dice in order: Tier reads A alone, Source reads B, and Form reads C once, so MiMo Flash stops adding the dice together. Ambient moments stay offscreen at two sentences at most, and their background texture is never brought up again. Ambitions now follow the wording of Realistic Frankenstein's Douyin Edition. A want you state in your own words that reaches past the scene is logged at 0/5 in the `ambitions:` ledger field and gains one step only when a closed thread served it.
- **The double slop gates** are one labelled line per pattern in the Anti-Slop Codex, plus one short instruction each in the Last-Mile Gate. Every line leads with what to write, since Kimi K3 follows "do this" lines best. The two repair examples for Contrast and Chop moved into the 🩹 Claude 5 patch, the only place left with quoted bad-to-good examples, because MiMo copies quoted examples.
- **The Scene Engine** lives in Voice & Scene Engine with its progression, causality, pacing, initiative and handoff endings. Each shift is caused on the page. The engine's narration line reports deeds and words and leaves verdicts on manner or habits to the characters.
- **Card Fidelity and the language rules** are Main Prompt labels (Card Fidelity, Story Language, Epistemic Limits). Speech counts as "heard" however the story's language marks it, so Hungarian „quotes" and dialogue dashes work. Card Fidelity takes gender and pronouns from the card and first message (else lorebook or chat) and never guesses them from a name. The gate's Card line repeats the rule for names, ages, counts, ties, history, bodies, pronouns, voice and the form and frequency of thoughts at the very end of the prompt, and its closing line asks the AI to follow the gate over its own earlier replies.
- **The Logic Core** is sent with the assistant role after the history, or with the system role through its twin, inside the gate's message. With 🏷️ Logic Core Tags on it carries no wrapper tag and starts on `<thinking>`, the tag the reply has to open with. With them off it sits inside `<logic_core>` as before, since the plan then runs inside the model's own reasoning. Every other entry calls it "the plan", which reads right in both shapes and with The Logic Core off, so no other entry branches on the shape. The gate only prints the one-line reminder The Logic Core hands it. Since beta 6 the plan has six fixed lines plus the Mode, Fate, Bonds and Ledger lines of the modules that run. Each line builds on the last with no drafts, and with the tags on, `go` ends the thinking. The Check line is gone, because MiMo Flash recited the whole gate there; the gate opens on `Write the prose per <anti_slop>:` and works as a set of instructions for the prose, with or without a plan.

### Known risks to test

- Beta 6 rewrote every rule to lead with what to write and turned the gate's questions into instructions, after our beta tester found MiMo V2.6 Flash and Pro sloppy on beta 5. It still needs live re-tests on Kimi K3 and on both MiMo models: Flash with the tester's own setup (🏷️ Logic Core Tags, 🔞 Adult Context, 👀 Hybrid POV, the MiMo patch and the 🔦 Flash Gate) and Pro with no plan at all. The live test plan below lists what to look for.
- Ambitions use a compact form of the Douyin Edition's wording that no live model has run yet. Watch for counters stuck at 0/5 after a thread that served them closed, and for goals you never stated.
- In Text Completions, ticking **Prefer Char. Instructions** lets a card's own Post-History Instructions replace my post-history block, and the 🚪 Last-Mile Gate goes with it. Since beta 6 that gate carries the only copy of the thought-form rule, so keep the box unticked (section 6).
- The Chat Completions default now sits at about 3,580 tokens, 25 more than beta 5, so a rule added to any default module later should free the same number of tokens somewhere else.
- 🎭 NPC Voice & Emotions brings Realistic Frankenstein's dialogue engine back at about 335 tokens, now without the example lists MiMo copied, and Anti-Slop's Contrast, Chop, Register and Trade lines carry the working parts of RF's Kimi-profile killswitches again. Compare Kimi K3, GLM and Claude dialogue with RF 2.2.1.3 on the same card and tell me where it still falls short. On a small local model the extra rules may weigh too much; set `aria-npc-voice` to `off` there if replies turn stiff.
- Chop asks for orders as full sentences again, the way Realistic Frankenstein did. A drill sergeant or another terse card should still bark short orders, because Card Fidelity puts the card's way of talking first, so tell me if a gruff card turns polite.
- Since beta 5, The Logic Core starts on `<thinking>` whenever the tags are on, so MiMo copies the right tag. The catch: a model could read that note as thinking it already finished and skip its own plan. If plans go missing more often than in beta 4, tell me, and the opening sentence goes back to Realistic Frankenstein's wording.
- Beta 4 ends the gate with a one-line reminder to open with the plan and gives The Logic Core a system-role twin. Providers can change how they wrap a model at any time, so the twin is a lever to test per provider, and the normal Logic Core stays the default.
- Beta 3 squeezed every module by about a quarter compared with beta 2, with reviewers checking each rule against Realistic Frankenstein along the way. Beta 6 compressed the rules a second time, with the 139 fixes in the archive's `Model fixes.md` as its checklist, though a longer gate and Fate leave the shipped default about 25 tokens above beta 5. Compare a few scenes with beta 5 from `archive/ARIA 1.0 beta 5/` and report anything that feels flatter or gets forgotten.
- Fate is the most compressed piece. Mid-size or quantized models may forget to age entries or let Bullets pile up, so try it on a strong model first.
- Only the 🩹 Claude 5 patch still quotes repair examples. Claude without its patch, and every other model, gets Contrast and Chop as plain instructions, so tell me if "it wasn't X, it was Y" or choppy fragments creep back.
- A card whose first message shows no thoughts may make the narration go a little flat.
- Gemini runs best with Scent Occasions OFF and its patch ON; check that no smells sneak back in.
- Bonds can rise quickly, so watch long slice-of-life chats for confessions arriving too early. Since the Bonds clarification, warm acts should move only Sparks, and the bond should climb by one only when the 💚 counter reads `turn 5/5`; tell me if a model still raises both at once.

### Live test plan

- **Plumbing:** with everything ON, send two messages in a row and open each reply's **Prompt** button in the message menu, or install the Prompt Inspector extension from **Extensions** → **Download Extensions & Assets**. The system block should match exactly, and the dice and the name letter should change only in the last message. To confirm caching, look for cache-read tokens on the second request in the Anthropic Console logs (direct Claude) or on the OpenRouter Activity page (Claude through OpenRouter). Switching Fate, Bonds, Adult, Freaky, Scent and Logic Core Tags off should remove their lines completely.
- **Claude 5 with its patch,** a two-character tavern scene over 30 turns: look for banned words, "it wasn't X, it was Y", choppy dialogue and "I respect that".
- **Gemini with its patch and Scent OFF:** no smells at all, at most one question per reply, and clumsy human reactions to heavy news.
- **GLM, Kimi or Qwen with their patch:** nervous characters keep their stammer; confident ones never mutter a filler word to themselves; on a clean chat, no reply over 10 turns opens on, repeats or quotes your last line; every character keeps the pronouns the card or lorebook gives them, and an order reads as a full sentence like "Take a seat, you look wrecked" where Kimi used to write "Sit."
- **Kimi K3 with its patch, over 10 turns:** every contrast in speech states what a thing is through one concrete detail; the prose opens on what someone does or says; the narrator leaves verdicts on anyone's manner or habits to the characters; a woman with no lorebook entry keeps she and her, whatever her name suggests.
- **MiMo V2.6 Pro with its patch,** once with The Logic Core and once with no plan at all: speech sits woven into the paragraph of its act, each line beside the action it belongs to, and each reply answers the one or two points of your message that move the scene most.
- **MiMo V2.6 Flash with its patch and the 🔦 Flash Gate, style B:** card facts and moods hold from turn 15 to turn 25. The plan stays shorter than one reply paragraph, with no drafts and no recited gate. Nobody grows a body part their card never gave them, and counts, ages and other numbers stay the way the chat first set them.
- **MiMo V2.6 with Fate on:** exactly one 🎲 block closes every reply for 20 turns, with every field present and `none` in the empty ones.
- **Fate over 20 turns:** the thread counter climbs and closes by 8, World stays at five entries or fewer, "meet me at noon on Day 3" fires on time, and harm reaching the scene stays rare.
- **Ambitions, with Fate on:** state a goal in your own words, like "I'll open my own bakery by spring". It should log at 0/5 and move up only when a pursuit that served it closes.
- **Bodies, names and secrets:** a card that describes a body (a sphinx with jackal ears) keeps exactly that body for 30 turns; your name survives a nickname or a jab, and nobody calls themselves by a title; the card's secret holds through the first few replies.
- **Card fidelity:** a shy card stays shy under Adult Context, siblings recognise each other on turn 1, a drill sergeant keeps short orders, and a Hungarian chat stays free of English words.
- **Impersonate:** the input box gets only your character's words, in their own person and tense.
- **Thinking style B (MiMo V2.6 Flash or another stubborn model):** every reply opens with `<thinking>`, runs the dashed plan lines, ends on `go` and closes the tag before the story. With Auto-Parse on, the plan lands in the reasoning box; with it off, the 💭 **Thoughts** box catches it, tags or no tags.
- **MiMo V2.6 Pro, style B:** 20 swipes per provider (Xiaomi, DeepInfra, NeuralWatt) at turn 10 or later, first with 🧠 The Logic Core and then with its system-role twin. Count how often the plan appears, whether it lands in SillyTavern's own reasoning box (the goal) or in the purple 💭 Thoughts box (the reply opened with something else, or the provider still sent its own reasoning, which then fills SillyTavern's box with free-form thoughts; note which), and whether the tag closes before the story. An OOC question about this turn's Fate dice shows whether the gate reaches the model at all.
- **Panels:** with Fate and Bonds on, the orange 🎲 panel holds the labelled rows and the teal 💚 panel under it holds one bar card per pair, names centred; with Fate off, only the teal panel shows. A model that drops the closing `</details>`, writes `bonds:` inside the 🎲 block or leaves the pairs loose at the end should still get both panels.
- **Text Completions, local 32k:** the System Prompt and story string in the Prompt itemization should match on two turns in a row, with only the dice and the new-name letter in the last block changing. Flipping each `aria-*` switch should add or remove only its own block. The KoboldCpp console should process only the new tokens each turn. With `aria-fate` on and Response (tokens) at 600 or more, the 🎲 line should survive 20 turns. With `aria-logic-core` on, the plan should fold into the reasoning box; note whether any of it reaches the input box after Impersonate.
- **Blind A/B against your previous preset:** same three cards, 10 turns each on Claude 5 and Gemini, ranked by a reader who doesn't know which is which.

### Reporting bugs (beta)

Please open an issue on the [GitHub issues page](https://github.com/QuillFlash/ARIA/issues) and include:

- the build: ARIA 1.0 beta 6, shown in the 🌳 README entry (Chat Completions) or in the template name (Text Completions)
- your SillyTavern version
- your API source or local backend, and the model (plus the quant for local models)
- your thinking style (A or B), or your `aria-*` switch lines on the Text Completions file
- every toggle or switch you changed from the defaults
- the prompt of the failing turn (the message's **Prompt** button) or an exported chat

---

That's the whole show! Thank you for sticking with me until the very end, Manager. Now go make some wonderful stories, and come cheer for us at the next concert~! 💖🎶

*Aria, lead singer of the Angels of Delusion*
