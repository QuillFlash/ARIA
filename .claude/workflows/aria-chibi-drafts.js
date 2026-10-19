export const meta = {
  name: 'aria-chibi-drafts',
  description: 'Chibi Edition: Sonnet drafts the compressed texts per module group, Opus judges and fixes each group',
  phases: [
    { title: 'Draft', detail: 'one Sonnet drafter per module group', model: 'sonnet' },
    { title: 'Judge', detail: 'one Opus judge and fixer per group', model: 'opus' },
  ],
}

const S = '/tmp/claude-1000/-home-theaestheticfur-Fejleszt-s-SillyTavern-ARIA/df35259a-9218-4ff7-923f-01988f563265/scratchpad'
const SRC = `${S}/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json`
const SRC_TC = `${S}/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json`
const DOUYIN = '/home/theaestheticfur/SillyTavern Presets/Realistic Frankenstein 2.2.1.3 — Limitless Realism/Douyin/Realistic Frankenstein 2.2.1.3 Douyin Edition.json'
const READ = `Read ${S}/spec/COMMON.md, ${S}/spec/CHIBI.md and ${S}/spec/JB.md in full first; they are binding ($S means ${S}). Source texts: the frozen snapshot "${SRC}" (CC) and "${SRC_TC}" (TC). Never read or edit the live repository preset files, which another workflow is changing. Tools: python3 ${S}/spec/tok.py <json> measures tokens (CHIBI.md explains --state); python3 ${S}/spec/skeleton.py "${SRC}" <json> checks the wiring is unchanged, and skeleton.py --text <src.txt> <draft.txt> does the same for raw TC text.`
const STR = { type: 'string' }
const STRS = { type: 'array', items: { type: 'string' } }

const GROUPS = [
  { key: 'G1', what: 'core', ids: 'main (⚡ ARIA Main Prompt), 0dc06d25 (🍃 Custom Instructions), 303f26f5 (🏷️ Logic Core Tags), f23feaf4 (📖 Story Context), 379e3c22 (🪞 Impersonation Turn), 939286fd (Reduce Reasoning), 59602978 (🌳 README), 8b4cf33f (🌿 Sampling Advice)',
    extra: "The Main Prompt's first line blanks every aria* variable: keep that run exactly and append {{setvar::ariaJb::}}{{setvar::ariaJbLines::}} (JB.md). The 🪞 Impersonation Turn also gets {{setvar::ariaJb::}} (JB.md). Also return TC texts where TC differs: from the snapshot TC sysprompt.content, the Main Prompt text (\"tc\".main_prompt, compressed the same way, same blanks plus the JB blanks) and a short Chibi version of the long README comment at the top (\"tc\".readme_comment)." },
  { key: 'G2', what: 'style', ids: '9869a1e5 (🖋️ Anti-Slop Codex, with its ariaEchoGate and ariaChopGate setvars) and jailbreak (🚪 Last-Mile Gate)',
    extra: "The gate prints lines other entries set: keep every such {{#if}} print exactly and compress only the gate's own lines. Also return \"tc\".post_history_gate, the compressed TC <final_gate> part of sysprompt.post_history (from \"<final_gate>\" to the end), keeping TC's own additions; and \"tc\".codex if TC's Codex text differs from CC's." },
  { key: 'G3', what: 'plan', ids: '15b770cf (🧠 The Logic Core) and 591b8c15 (🧠 The Logic Core, system-role twin)',
    extra: "Add the JB counter and print exactly where JB.md's \"Wiring in CC\" puts them (the snapshot doesn't have them yet); both Logic Cores identical after their comments. Also return \"tc\".post_history_logic_core, the compressed TC part of sysprompt.post_history from its start up to (not including) \"<final_gate>\", with the same JB counter and print, and TC's closing sentence about messages written as {{user}} listing the JB labels too; the JB labels aren't final yet, so write the placeholder JBLABELS where they go." },
  { key: 'G4', what: 'voice and modes', ids: '15a8065d (🎬 Voice & Scene Engine), cca418a6 (🎭 NPC Voice & Emotions), 2a2e12d0 (🐺 Anthro Vocals), dd3642f5 (👃 Scent Occasions), b7b6ab7f (👀 Hybrid POV), nsfw (🔞 Adult Context), 4537b57d (😈 Freaky Override)',
    extra: "Adult Context and Freaky Override set ariaModeLine: keep that wiring. Compressed Adult Context keeps its permissions and mechanics: adult fiction; grey-to-black morality in dark scenes; consent in reciprocal acts never re-asked; frank, granular sex with autonomic and auditory feedback; visceral, medically exact violence; vulgar slang in speech and plain anatomy words in narration; each plea new; persona and Slow Burn pacing." },
  { key: 'G5', what: 'world engine', ids: '5dcccd11 (⏰ Time & Place), acc2177a (🎲 Fate & Chekhov Ledger), 5506d699 (🥰 Bonds Lite)',
    extra: "Fate & Chekhov Ledger and Bonds Lite feed the regex UI: the 🎲 and 💚 blocks, their field names, symbols, separators and order, and the <details><summary>…</summary>…</details> formats stay byte-for-byte, so ARIA's regex scripts still match. Read the snapshot CC's extensions.regex_scripts whose names start \"ARIA UI\" to see what they rely on. The Fate dice use {{roll}} inside setvar bodies (cache rule): keep that exactly." },
  { key: 'G6', what: 'model patches and gates', ids: 'b59a2ad1 (🩹 Claude 5), 333dbbed (🩹 Gemini 3.8 Flash), ac96376e (🩹 Gemini All-In-One), 1f2e1f97 (🩹 GLM), 9bb6c2b0 (🩹 Kimi / Qwen), 33f92483 (🩹 MiMo V2.6 Pro), 3a027832 (🩹 MiMo V2.6 Flash), e04b9c2b (🩹 DeepSeek), 2e3e7f63 (🔦 Flash Gate), dc8b1acb (🧷 Character Hold)',
    extra: "Each patch line answers a tester report its comment describes: keep each line's checkable core. GLM's Pushback (the not-sentence rule, denials and fixes of a claim included) and Restate (the phrase marking a speech as on record, honest, clear or said first) were just confirmed live on GLM 5.3 Flash: keep both mechanics. The Claude 5 patch may keep its repairs, shortened. The Flash Gate and DeepSeek interact through ariaPatchJoins: keep that logic exactly." },
]

const draftPrompt = g => `${READ}
Style model: the Douyin Edition, ${DOUYIN}. Load it with python3 and read the prompts CHIBI.md names before you write.

You are drafting group ${g.key} (${g.what}) of the Chibi Edition. Your prompts, by CC identifier prefix: ${g.ids}.
${g.extra}
Steps:
1. Print each source prompt in full from the snapshot CC, and the matching TC text where your group has one.
2. Make your own list of every mechanic and checkable rule each source prompt carries.
3. Write the compressed content of each prompt: the same wiring (setvar, getvar, addvar and #if structure, variable names, labels); Douyin-concise do-this wording; every mechanic's checkable core kept; ARIA's house rules (no quoted examples except the Claude 5 repairs, no lists of three); short Chibi-specific comments.
4. Measure with tok.py and check with skeleton.py until every prompt meets CHIBI.md's targets and its skeleton is OK (the only allowed skeleton differences are the JB additions JB.md specifies).
5. Write ${S}/chibi/drafts/${g.key}.json in CHIBI.md's draft format.
Do not edit repository files. Return a summary with per-prompt token counts and any skeleton difference you intend.`

const judgePrompt = (g, d) => `${READ}
Style model: the Douyin Edition, ${DOUYIN}.

You are the quality judge and fixer for Chibi group ${g.key} (${g.what}): prompts ${g.ids}. The draft is ${S}/chibi/drafts/${g.key}.json (drafter's summary: ${JSON.stringify(d)}).
Check and fix:
1. Wiring: skeleton.py on the draft; every prompt OK except JB.md's JB additions (the G1 blanks, the G3 counter and print). Check the TC texts with skeleton.py --text against the matching snapshot TC segments (write the source segment to a temp file first).
2. Fidelity: compare each draft prompt with its source, sentence by sentence; every mechanic, number, threshold, exception and tester fix survives in checkable form. Name anything lost and restore it compactly.
3. Size: tok.py; every CHIBI.md target met.
4. Style: Douyin-concise do-this wording; no quoted examples (only the Claude 5 repairs); no list of exactly three anywhere in model-facing text (check every list); no rationale aimed at the model; plan and gate lines as fragments joined by semicolons.
5. Rendering: the texts read naturally once rendered (no doubled spaces or broken sentences around macros); {{trim}} and newlines as in the source.
Write the approved version to ${S}/chibi/final/${g.key}.json (same format, plus "judge_notes"). Return per-prompt token counts, what you restored and any remaining concern.`

const results = await pipeline(
  GROUPS,
  g => agent(draftPrompt(g), { label: `draft:${g.key}`, phase: 'Draft', model: 'sonnet', schema: { type: 'object', properties: { summary: STR, total_tokens: { type: 'number' } }, required: ['summary'] } }),
  (d, g) => agent(judgePrompt(g, d), { label: `judge:${g.key}`, phase: 'Judge', model: 'opus', schema: { type: 'object', properties: { summary: STR, restored: STRS, concerns: STRS, total_tokens: { type: 'number' } }, required: ['summary', 'restored', 'concerns'] } })
)
return GROUPS.map((g, i) => ({ group: g.key, judge: results[i] }))
