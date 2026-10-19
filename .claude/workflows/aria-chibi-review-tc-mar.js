export const meta = {
  name: 'aria-chibi-review-tc-mar',
  description: 'Opus 5.5 reviews and fixes Chibi TC and Chibi Marinara, beside the running Chibi CC review',
  phases: [
    { title: 'Review', detail: 'one Opus 5.5 reviewer and fixer each for Chibi TC and Chibi Marinara', model: 'claude-opus-5-5' },
  ],
}

const CHAINS = { opus: ['claude-opus-5-5', 'opus'] }
async function run(tier, prompt, opts) {
  for (const model of CHAINS[tier]) {
    const r = await agent(prompt, { ...opts, model })
    if (r !== null && r !== undefined) return r
    log(`${opts.label}: no result on ${model}, trying the next model`)
  }
  return await agent(prompt, opts)
}

const W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
const REPO = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA'
const CHIBI_CC = `${REPO}/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json`
const CHIBI_TC = `${REPO}/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json`
const CHIBI_MAR = `${REPO}/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Agent Gating.json`
const ARIA_TC = `${REPO}/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json`
const SUB = `You are a subagent inside a workflow run. Do the task yourself with Bash, Read, Edit and Write. Do not use the Skill tool and do not try to start a workflow. Never read from or write to /tmp/claude-1000/...; your work folder is ${W} (scratch scripts in ${W}/build/). Never commit, stage or push. Never edit tools/aria_budget.py or any ARIA 1.0 file; run the checker only with a file argument. Another Opus agent is reviewing and possibly fixing Chibi CC ("${CHIBI_CC}") right now and logs its edits to ${W}/build/review_cc_changes.json; never edit Chibi CC yourself. Before you finish, read that log (if it exists) and carry every CC text change into your file where the same text appears, then re-run your checks.`
const READ = `${SUB}\nRead ${W}/spec/COMMON.md, ${W}/spec/JB.md, ${W}/spec/CHIBI.md and ${W}/spec/BUILD.md in full before anything else; they are binding ($S and $W mean ${W}; $REPO means ${REPO}).`
const MEM = `Also read ~/.claude/projects/-home-theaestheticfur-Fejleszt-s-SillyTavern-ARIA/memory/marinara-agent-gating-port.md.`
const STR = { type: 'string' }
const STRS = { type: 'array', items: { type: 'string' } }
const OUT = { type: 'object', properties: { found: STRS, fixed: STRS, remaining: STRS, changed: { type: 'boolean' }, checks: STR }, required: ['found', 'fixed', 'remaining', 'changed', 'checks'] }

const [tc, mar] = await parallel([
  () => run('opus', `${READ}

You are the reviewer and fixer for Chibi TC ("${CHIBI_TC}") only. Its builder reported: everything ON 2,996 (GLM), lean start 1,589 with aria-logic-core shipping on (1,292 off), sysprompt.name and context.name "ARIA 1.0 beta 8 Chibi Edition (Text Completions)". To fit 3,000 it made one deliberate TC-only change: the four "A message written as {{user}}" gate notes (Own words, POV, Ledger, Layers) print only while aria-logic-core is off, and with the Logic Core on the plan's closing sentence names those lines instead ("…with no Fate, Bonds, Ledger, Layers, Role, Frank, Own words or POV line.").
Verify with your own scripts:
1. Wiring: the switches (names, order, defaults), every block's condition and every setvar/getvar/addvar/#if skeleton match ARIA TC ("${ARIA_TC}") apart from the documented JB additions and the notes change above (use ${W}/spec/skeleton.py --text on matching segments).
2. Content: every segment equals its final in ${W}/chibi/final/ (G1–G6 tc keys, JB.json) and no ARIA text is left where a final replaced it; the model-facing text of each shared module equals Chibi CC's rendered module text.
3. The notes change: sound, no rule lost on a Logic-Core-off setup, and the Fix 3 cleanup regexes in "${REPO}/regex/ARIA 1.0 Regex Scripts (Text Completions).json" still remove the echoed closing sentence and the "Every response starts with" line (test on a rendered, echoed plan, tags on and off).
4. Budget (python3 tools/aria_budget.py "${CHIBI_TC}"): everything ON at most 3,000; lean start between 1,350 and 1,650; report "+ Logic Core, Fate, Time".
5. Behaviour: a simulate_tc matrix (logic core, tags, adult, freaky, jailbreak, fate, bonds, each patch): dashed-line counts match, no leftover macros, no literal backslash-n, no doubled spaces, the system prompt identical across turns.
6. Switch comments: each Chibi cost is true (flip one switch from the shipped state), short and accurate.
7. JSON hygiene (formats like ARIA TC, round-trips), the JB boundary and the house rules.
Fix problems in Chibi TC only, by raw-text replacement, and log every change (old and new text) to ${W}/build/review_tc_changes.json. Return what you found, fixed and left, and the final checker lines.`,
    { label: 'review-tc', phase: 'Review', schema: OUT }),
  () => run('opus', `${READ}
${MEM}

You are the reviewer and fixer for Chibi Marinara ("${CHIBI_MAR}") only. Its builder reported: compare.py 0 unique section diffs (JB exercised) against Chibi CC; verify.py 0 mismatches; N figures up to 2,984 (GLM), A figures up to 3,072 (GLM; the user allowed the Agents path over 3,000). It was generated by ${W}/build/chibi_mar/mar_convert.py, which reproduces ARIA's Marinara sections byte for byte from ARIA CC (selftest.py). Regenerate through that converter rather than hand-editing where you can.
Verify with your own scripts:
1. Metadata: a fresh preset id with matching presetId on every child; name and description for Chibi; createdAt, updatedAt and exportedAt 2026-10-16T12:00:00.000Z; defaultChoices without FATE and TIME; choice blocks and options the same as ARIA's Marinara (the JAILBREAK option included).
2. Conversion: every section's text matches Chibi CC under Marinara's conventions; inlined lines in both Logic Cores and the gate under the right choice conditions; no bare {{#if name}} (true in Marinara); the JB under JAILBREAK with adult_mode not NONE.
3. The Agents text (the <agent_context_protocol> block in Main and the note in both Logic Cores): at most 90 tokens together, and it keeps the rules: earlier snapshot; facts applied silently, never quoted or reformatted; current actions change it and newer witnessed events override it; no agent, tracker, debug or report block, while the 🎲 and 💚 ledgers still close the reply.
4. Render checks from ${W}/mar: python3 compare.py --full --cc-file "${CHIBI_CC}" --mar "${CHIBI_MAR}" (0 unique section diffs (JB exercised)) and python3 verify.py --mar "${CHIBI_MAR}" (0 mismatches, N figures at most 3,000; report A).
5. Round-trip format exact; the JB boundary and the house rules.
Fix problems in Chibi Marinara only (prefer fixing the converter and regenerating), and log every change to ${W}/build/review_mar_changes.json. Return what you found, fixed and left, and the final compare and verify lines.`,
    { label: 'review-marinara', phase: 'Review', schema: OUT }),
])

return { reviewTC: tc, reviewMarinara: mar }
