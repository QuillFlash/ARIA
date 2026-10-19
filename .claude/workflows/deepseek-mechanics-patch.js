export const meta = {
  name: 'deepseek-mechanics-patch',
  description: 'Sonnet writes a DeepSeek patch line for Fate and Bonds bookkeeping, Opus judges and fixes it, Haiku commits and pushes to alpha',
  phases: [
    { title: 'Write', detail: 'Sonnet 5.5 drafts the patch line in CC and TC', model: 'sonnet' },
    { title: 'Judge', detail: 'three Opus 5.5 judges', model: 'opus' },
    { title: 'Fix', detail: 'Opus 5.5 fixer', model: 'opus' },
    { title: 'Ship', detail: 'Haiku 5.5 commits and pushes to alpha', model: 'haiku' },
  ],
}

// Model fallback chains from the user's global rule: latest of the family, then an older one, then inherit.
const CHAINS = {
  sonnet: ['sonnet', 'claude-sonnet-4-5', null],
  opus: ['opus', 'claude-opus-4-5', null],
  haiku: ['haiku', 'claude-haiku-4-5', 'claude-sonnet-4-5', null],
}
async function run(role, prompt, opts) {
  for (const m of CHAINS[role]) {
    const o = Object.assign({}, opts)
    if (m) o.model = m
    let r = null
    try { r = await agent(prompt, o) } catch (e) { log(opts.label + ': model ' + (m || 'inherited') + ' failed: ' + String(e).slice(0, 120)) }
    if (r) return r
    log(opts.label + ': no result on ' + (m || 'inherited model') + ', trying the next model')
  }
  return null
}

const CTX = [
  'Repo: /home/theaestheticfur/Fejlesztés/SillyTavern/ARIA, branch alpha (pushed, clean, HEAD a623fe6 "ARIA 1.0 beta 8"). ARIA is a SillyTavern roleplay preset.',
  'Files: "Aria\'s Realistic Intelligence Assistance 1.0 — (Chat Completions).json" (CC: prompts[] plus prompt_order[1], the live order), "Aria\'s Realistic Intelligence Assistance 1.0 — (Text Completions).json" (TC: sysprompt.content with {{.aria-* = on/off}} switches and {{#if .aria-...}} blocks, plus sysprompt.post_history holding The Logic Core and the Last-Mile Gate), "regex/ARIA 1.0 Regex Scripts (Text Completions).json", docs/ARIA_Beginners_Guide.md, tools/aria_budget.py (run: python3 tools/aria_budget.py; it checks budget, wiring, read-before-set order and cache safety).',
  '',
  'THE PROBLEM (from the repo owner\'s own testing of beta 8): DeepSeek V4.1 Flash will not interact with the Bonds system. Over many turns it never raises Sparks or Grudge from their defaults, never converts Sparks into BOND level, and never lowers BOND once enough Grudge has built up. TASK: add a line to the 🩹 Model Patch: DeepSeek toggle that reminds the model, in its plan (the Logic Core CoT), to keep track of the game mechanics: Fate & Routine (the 🎲 Fate & Chekhov Ledger) and Bonds (🥰 Bonds Lite).',
  '',
  'Where things live (read them, do not trust this summary blindly):',
  '- CC 🩹 Model Patch: DeepSeek (identifier e04b9c2b-d8a0-5346-ab66-1cf25e5d7c1b). Its body caps native reasoning ("one pass through the plan lines, a terse bullet each, under 150 words; no drafts, rereads, rule audits or second passes"), sets {{setvar::ariaPatchLines::3}} and sets ariaPatchGate (Echo, Repeats, Bodies). ariaPatchGate prints BOTH in the Last-Mile Gate and in The Logic Core plan (between Voice and Move); ariaPatchLines adds to the plan\'s line count. TC has the same text inside {{#if .aria-patch-deepseek}}.',
  '- CC 🥰 Bonds Lite sets ariaBondsLine (the plan\'s Bonds line: "- Bonds: listed acts add Sparks (max 2 per pair), slights Grudge; Sparks 7: BOND +1, Sparks 0.") and the ledger lines. Its <bonds> block holds the full rules: Sparks list, Sparks >= 7 converts to BOND +1 and resets, Grudge +1 per slight, Grudge >= 5 converts to BOND -1 and resets, gains halved while Grudge >= 3, repair clears Grudge. Note the shared plan Bonds line never mentions the Grudge conversion.',
  '- CC 🎲 Fate & Chekhov Ledger sets ariaDice, ariaFateLine and ariaLedgerLine/ariaLedgerGate. The plan already has Fate, Bonds and Ledger lines when those modules are on.',
  '- Suspected causes worth weighing: (a) the patch\'s own reasoning cap ("under 150 words; no rule audits") may be read as permission to skip ledger arithmetic, so DeepSeek copies the last 💚 block unchanged; (b) the plan Bonds line is abstract, with no per-pair step that names this turn\'s act or slight and does the add and the threshold check; (c) the Grudge-to-BOND conversion is absent from the plan.',
  '',
  'Pitfalls to handle:',
  '- The line must not appear when Bonds and Fate are both off, and must not appear on an Impersonate turn. In CC the 🪞 Impersonation Turn (In-Chat, depth 0) blanks ariaFateLine, ariaBondsLine, ariaLedgerLine, ariaLedgerGate and ariaDice, but it runs AFTER the system block, so anything the patch renders into ariaPatchGate at set time in the system block would still carry the line on Impersonate. Conditions checked at READ time (inside The Logic Core, e.g. {{#if .ariaBondsLine}} or {{#if .ariaLedgerLine}}) do drop it. TC has no Impersonation Turn; its post_history tells the model a message written as {{user}} plans no Fate, Bonds, Ledger or Layers line. Prefer a design where the setter lives in the DeepSeek patch (that is what the owner asked for) and the read is gated at read time.',
  '- The plan\'s line count (logicCoreLines) must stay exact in every combination: Bonds on or off, Fate on or off, Impersonate. Look at how 🧷 Character Hold (ariaHoldLine) was wired in a623fe6 (git show a623fe6) for a recent precedent: setter in the toggle, blanking in the Main Prompt\'s first line, count and read in The Logic Core, the CC system-role twin of The Logic Core kept identical, Impersonation Turn blanking, the TC post_history copy, and the Impersonate plan-strip regex label list in BOTH the CC extensions.regex_scripts and the TC regex file.',
  '- Every new variable needs a blanking setvar in the Main Prompt\'s first line (CC and TC); the checker fails a splice variable the Main Prompt does not blank.',
  '',
  'House rules: do-this instruction form; mechanical, checkable wording a small model can follow; NO quoted examples in patches or shared rules (only the Claude 5 patch has them); do not change shared lines that Kimi K3 and GLM 5.3 rely on (confirmed working at git tag beta-7-kimi-k3-glm-5.3-confirmed); keep the DeepSeek plan short, since DeepSeek overthinks; 6,000-token hard ceiling for the fully kitted-out path (checker enforces); CC and TC stay in sync; edit JSON only by exact raw-text replacement (a python3 -I script doing str.replace on json.dumps(text, ensure_ascii=False)[1:-1] works; never json.dump the whole file, which reformats it); entry comments ({{// ...}}) describe for users what the entry does, in plain words; the guide uses Aria\'s cheerful first-person voice. Do NOT edit the Agent Gating (Marinara Engine) preset; BSPiotr maintains it. Do not commit or push.',
].join('\n')

phase('Write')
const draft = await run('sonnet', CTX + '\n\nYou are the writer. First run git status and git diff; if an earlier attempt left partial edits, continue from them. Write the DeepSeek patch line (or lines) and wire it in CC and TC, update the patch\'s user-facing comment in CC, the TC switch comment for aria-patch-deepseek, the Impersonate plan-strip regex label lists (CC and TC regex file) if you add a plan label, and the guide (the 🩹 Model Patches paragraph about DeepSeek, the aria-patch-deepseek row and its token figure, the variable table, the Fully kitted out / Everything ON rows only if the totals change). Run python3 tools/aria_budget.py until it passes, and check that every JSON file still parses. Also render the plan yourself (import tools/aria_budget.py and call simulate_cc / simulate_tc) with the DeepSeek patch on in four shapes: Bonds on + Fate on, Bonds on + Fate off, both off, and CC Impersonate; confirm the line appears only where it should and that the "N dashed lines" count matches the dashed lines actually printed. Return: the exact new text, where each piece lives, the four render checks, the checker totals, and git diff --stat.', { label: 'writer', phase: 'Write' })
if (!draft) throw new Error('writer produced nothing on every model in its chain')

const FINDINGS = {
  type: 'object',
  properties: {
    verdict: { type: 'string', description: 'ship / ship with changes / rework' },
    findings: { type: 'array', items: { type: 'object', properties: {
      severity: { type: 'string', enum: ['major', 'minor', 'nit'] },
      where: { type: 'string' }, problem: { type: 'string' },
      exact_fix: { type: 'string', description: 'exact old text -> new text, or a precise instruction' },
    }, required: ['severity', 'where', 'problem', 'exact_fix'] } },
  },
  required: ['verdict', 'findings'],
}
const JUDGES = [
  { key: 'deepseek-behaviour', lens: 'You judge whether the new line will actually make DeepSeek V4.1 Flash (and V4 Pro) move Sparks, Grudge and BOND, convert at the thresholds both ways, and keep the 🎲 Fate ledger arithmetic (q, hp, ages) moving, while staying inside its short one-pass plan. Check it against the full <bonds> and Fate rules so it cannot contradict them (Sparks max 2 per pair per turn, the listed acts only, gains halved at Grudge >= 3, repair clears Grudge, Fate q/hp counting). Check it does not invite DeepSeek to overthink or to print mechanics in the prose. Check the reasoning cap no longer reads as permission to skip the ledgers.' },
  { key: 'wiring', lens: 'You are the wiring and regression auditor. Verify CC/TC parity (including The Logic Core\'s system-role twin), the Main Prompt blanking, the plan line count in every Bonds/Fate/Impersonate combination (render them with simulate_cc / simulate_tc from tools/aria_budget.py), the Impersonate plan-strip regex in both regex locations, that the checker passes and the totals stay under 6,000, that no other patch or shared line changed, that no quoted examples were added, and that the four plan-fold regexes still fold a plan containing the new line (test the regexes in node or python against a rendered plan).' },
  { key: 'house-rules', lens: 'You judge wording and docs. Is the new line in do-this form, mechanical, short, free of quoted examples, consistent with the labels and vocabulary the plan already uses (BOND/Sparks/Grudge, q, hp, ages)? Do the CC comment, the TC switch comment and the guide describe accurately what the patch now does, in plain words, without overstating untested results? Is the guide\'s token figure right? Flag anything that changes behaviour for Kimi K3 or GLM 5.3.' },
]
phase('Judge')
const reviews = (await parallel(JUDGES.map(j => () =>
  run('opus', CTX + '\n\nThe writer\'s report:\n' + draft + '\n\n' + j.lens + '\nRead git diff yourself. Do NOT edit any file. Return only real problems, each with an exact fix; an empty list is fine.', { label: 'judge:' + j.key, phase: 'Judge', schema: FINDINGS })
    .then(r => r ? Object.assign({ judge: j.key }, r) : null)))).filter(Boolean)
log(reviews.length + ' judges returned ' + reviews.reduce((n, r) => n + r.findings.length, 0) + ' findings')

phase('Fix')
const FIX = {
  type: 'object',
  properties: {
    report: { type: 'string', description: 'each finding: applied / rejected and why; final render checks; checker totals; git diff --stat' },
    checker_passes: { type: 'boolean' },
    files: { type: 'array', items: { type: 'string' }, description: 'repo-relative paths of every changed file to commit' },
    commit_subject: { type: 'string', description: 'under 72 characters' },
    commit_body: { type: 'string', description: 'plain wrapped lines, what changed and why; no attribution line' },
  },
  required: ['report', 'checker_passes', 'files', 'commit_subject', 'commit_body'],
}
const fix = await run('opus', CTX + '\n\nThe writer\'s report:\n' + draft + '\n\nThe judges\' findings (JSON):\n' + JSON.stringify(reviews, null, 1) +
  '\n\nYou are the fixer. Check each finding against the files yourself. Apply every major finding and each minor one you agree with; reject wrong ones or ones that break a house rule, and say why. Where judges conflict, pick what makes DeepSeek track the mechanics with the shortest plan. Keep CC and TC in sync with raw-text replacement. Re-run the four render checks and python3 tools/aria_budget.py, and verify every JSON parses. Do not commit or push. Return the structured result; list in files every changed path (git diff --name-only).', { label: 'fixer', phase: 'Fix', schema: FIX })
if (!fix) throw new Error('fixer produced nothing on every model in its chain')

phase('Ship')
let ship = null
if (!fix.checker_passes) {
  log('fixer reports the checker failing, so nothing is committed or pushed')
} else {
  const msg = fix.commit_subject + '\n\n' + fix.commit_body + '\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'
  ship = await run('haiku', 'You are the Git manager for the repo at /home/theaestheticfur/Fejlesztés/SillyTavern/ARIA, on branch alpha. Steps, in order, stopping and reporting on the first failure:\n1. Run: python3 tools/aria_budget.py. It must end with OK lines for both presets and exit 0. If it fails, stop: commit nothing.\n2. Run git status --short. Stage exactly these files, each quoted, with git add -- <file> (never git add . or -A): ' + JSON.stringify(fix.files) + '. If git status shows other changed files outside that list, do not stage them and mention them.\n3. Commit with this exact message, passed through a quoted heredoc to git commit -F - so nothing in it is expanded:\n<<<MESSAGE\n' + msg + '\nMESSAGE>>>\n(the <<<MESSAGE and MESSAGE>>> markers are not part of the message).\n4. Push with: git push origin alpha. Never force-push, never pass --no-verify, never touch other branches.\n5. Run git log --oneline -1 and git status -sb.\nReturn the result.', {
    label: 'git-manager', phase: 'Ship',
    schema: { type: 'object', properties: {
      committed: { type: 'boolean' }, pushed: { type: 'boolean' },
      commit: { type: 'string', description: 'short hash and subject' },
      output: { type: 'string', description: 'the key command output, including any error' },
    }, required: ['committed', 'pushed', 'commit', 'output'] },
  })
}
return { draft, reviews, fix, ship }
