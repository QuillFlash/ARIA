"""Write the judged G3 to $S/chibi/final/G3.json: build_final.build() plus final notes and judge_notes.

usage: python3 finalize.py [OUT.json]   (default: $S/chibi/final/G3.json)
"""
import json, sys
import build_final as bf

S = bf.S
OUT = sys.argv[1] if len(sys.argv) > 1 else S + "/chibi/final/G3.json"

NOTES = (
    "FINAL G3 TEXTS (judge-approved; the drafter's notes described their draft, which this replaces). Both CC Logic Cores "
    "(15b770cf plain, 591b8c15 system-role twin, identical after their comments) and the TC post_history Logic Core part "
    "(the comment, {{trim}} and the {{#if .aria-logic-core}} block; G2's post_history_gate starts at <final_gate> and joins it "
    "directly). The head, the fragments sentence, the seven base lines (OOC, Scene, Knows, Voice, Move, Fresh, Check) and the "
    "reply line are Douyin-style fragments joined by semicolons. Every setvar, getvar, addvar and #if of the source is unchanged, "
    "plus JB.md's two additions: the counter {{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}} right "
    "after the plain Ledger counter (before Hold), and the print {{#if .ariaJb}}{{getvar::ariaJb}} newline {{/if}} right after "
    "the Ledger block, before '- Fresh:'. "
    "SIZES (characters / 4, comments stripped, no module lines): 220.0 with Tags off (880 characters; ARIA 337), 253.25 with Tags "
    "on (ARIA 357); TC part 248.0 with aria-logic-core on and aria-thinking-tags off, 281.25 with tags on (ARIA 362 and 382), 0 "
    "with aria-logic-core off; ariaPlanCue 20.5, unchanged. "
    "KEPT VERBATIM for the regex scripts: 'opens the reply, then', 'closes on the line after go.', 'The reply starts on the line "
    "after that:', 'Nothing above go enters the reply.', 'Every response starts with <open>.'; also '; go ends the thinking', "
    "the plan labels and the <logic_core> wrapper for Tags off. TC-only text kept: 'A message written as {{user}} skips it.' "
    "after the Tally print, the closing sentence '...with no Fate, Bonds, Ledger, Layers, Role or Frank line.' (JB.md) and the "
    "{{#if .aria-logic-core}} wrapper. "
    "WHAT WENT, and where it still lives: the four pointers (Personality Independence), (Epistemic Limits), (Card Fidelity) and "
    "(Story Language), since the Main Prompt states each rule under that label every turn; 'card-true' on jokes (G2's gate "
    "Humour line: rare small card-true jokes); 'prose in flowing paragraphs' (G2's gate Paragraphs line: one flowing scene; this "
    "Core keeps the plan-specific half of that fix, 'plan blended in, never a paragraph per plan line', and is now its only "
    "home); 'resting' before mood (card mood is the card's baseline; Main and the gate's Card line keep temperament); 'acting' "
    "before character in Knows (scope only); 'dashed' in the Tags-off head (the template, the Tags-on head and the plan cue show "
    "the dashes); 'new to the chat' (new details); 'once written' (settled); 'sentences' in 'never reply sentences or drafts' "
    "(Fragments rules out sentences; a reply sentence written in the plan is a reply draft). "
    "RESTORE MENU (tokens; the row sits at its 220 ceiling with no slack, so each restore needs an equal cut): 'NPC' after 'what "
    "each' in Knows 1.0, or 'acting character' 4.25; 'small card-true jokes' for 'jokes small' 2.5; 'still' after 'help/hold' "
    "1.5; 'dashed' in the Tags-off head 1.75; 'plan blended into prose' 2.0; 'one' for 'a' reply paragraph 0.5. "
    "REPRODUCE: $S/chibi/work/G3judge (build_final.py builds the texts from the draft with the judge's edits; finalize.py writes "
    "this file; wirecheck.py, render_scan.py, regex_test.py and checker_test.py are the checks)."
)

JUDGE_NOTES = (
    "VERDICT: approved with fixes; this file replaces the draft. "
    "WIRING. skeleton.py against the snapshot: both CC prompts differ only by JB.md's two additions; skeleton.py --text against "
    "the snapshot's TC segment (post_history up to <final_gate>, saved as $S/chibi/work/G3judge/tc_lc_src.txt) the same. An exact "
    "check (wirecheck.py) inserts the counter and print into the source at JB.md's positions and finds the skeletons equal; the "
    "counter, print and TC closing sentence match the JB workflow's own audit strings character for character; the twins are "
    "identical after their comments; the TC body equals the CC body plus TC's two own texts; the sequence of macros and "
    "newlines, {{trim}} included, equals the source's plus the additions. Frozen checker on in-memory copies of the snapshot "
    "with a stand-in JB wired per JB.md: TC no errors; CC only 'everything ON is 6007, over the 6000 budget', which is the full-"
    "size ARIA prompts plus the JB against the frozen checker's old cap (JB.md raises it to 7,000). With the G1 and G2 finals "
    "swapped in as well: no errors in CC (everything ON 4785) or TC (5770). In every shape the count equals the dashed lines "
    "printed before go (18 and 18 with everything on and the JB, 11 and 11 on Impersonate, where ariaJb is blanked). "
    "FIDELITY, sentence by sentence against the source. The draft kept every base-line item and every tester fix I traced "
    "with git log -S (ece78b2: card-true wants, help or hold, one beat, stop point, 1-2 lists, small jokes none when sincere, "
    "the move landing first as an act; 6993aed: secrets kept and the plan-line paragraph fix; 570c222: questions get only an "
    "OOC answer with no header or ledger). It had lost four "
    "things, now restored within the same 220: (1) the Tags-off reasoning stop, source 'Reasoning ends at go.' from the beta 2 "
    "echo fix (dd8cc5f), the Tags-off twin of 'closes on the line after go'; the draft kept only 'Reasoning: N lines, then go.' "
    "and 'Reply:'. Now 'Reasoning: N lines; go ends it.', matching Tags-on's '; go ends the thinking'. (2) 'all' on the length "
    "cap: the source caps the whole plan at one reply paragraph ('all shorter than'); the draft's 'under one reply paragraph' "
    "could be read per fragment. (3) 'each building on the last' (in the plan since 279bb31's 'a written line is settled and "
    "the next builds on it'): now "
    "'settled and built on', the same length as the draft's 'settled once written'. (4) Fresh's noun: the draft's '1-2 new' had "
    "lost 'details'. Paid for by 'not reply sentences/drafts' -> 'no reply drafts' (Fragments already rules out sentences, and a "
    "reply sentence in the plan is a draft) and 'one' -> 'a' reply paragraph. Checked and approved as compression, with where "
    "each rule still lives: the four pointers (Main states the rules under those labels), card-true jokes and the flowing scene "
    "(G2's final gate), resting (card mood), acting (scope only), dashed (template, Tags-on head and cue), and "
    "each NPC's next act for each character's (ARIA's own term in Freaky and Bonds, the JB's and the Douyin CoT's; it also "
    "keeps {{user}}'s act out of Move). G2 dropped 'plan line' from the gate, so 'never a paragraph per plan line' now lives "
    "only here; it stays. "
    "SIZE. Exactly 220.0 with Tags off (880 characters), the row's ceiling, both prompts; never both on, so the group is 220.0. "
    "Tags on 253.25, TC 248.0 and 281.25. "
    "STYLE. No quoted examples. Lists checked one by one: OOC 2 (2+2), Scene 5, Knows 2, Voice 4 (5 with the Flash Gate's "
    "ariaVoiceExtra), Move 4, Fresh 4, Check 2, fragments sentence 4, reply line 2 (2+2 with a ledger), ariaPlanCue 4, TC "
    "closing sentence 6. The draft's Tags-on head 'X opens the reply, then N dashed lines, then go.' was a three-part run; it is "
    "now 'then N dashed lines and go.' The regex anchors only 'opens the reply, then ', and the echo clean-up gives identical "
    "results. No rationale aimed at the model; the plan lines are fragments joined by semicolons. "
    "RENDERING. 6,144 renders (CC plain, twin and TC, Tags on and off, every on/off mix of the ten spliced variables with real "
    "values) show no doubled space, no space before punctuation, no blank line, no line ending on a separator and no leftover "
    "macro, and the head's count always equals the printed lines. "
    "REGEX. The snapshot's Logic Core scripts (CC and the TC file are identical) run on echoed Tags-on templates, an echoed "
    "Tags-off block and a leaked untagged plan leave the same remainder for source and final. The only difference is 'ARIA "
    "Impersonate - strip an untagged plan' meeting the JB's Role and Frank lines; with JB.md's alternation (...|Joins|Role|"
    "Frank) it disappears. "
    "REMAINING CONCERNS. (a) Pre-existing in the snapshot, unchanged here: in TC the echo regexes still expect an older "
    "'When this turn asks for ... Ledger lines.' after 'Nothing above go enters the reply.', so an echoed TC template leaves "
    "the 'For a message written as {{user}} ...' sentence and the 'Every response starts with' line behind; the fix belongs to "
    "ARIA's regex scripts, which Chibi copies unchanged. (b) The row has zero slack: any later change to these lines must be "
    "paid for inside them. (c) 'help/hold too' is the draft's compression of 'helping or holding still'; 'hold' could be read as "
    "holding something, and 'help/hold still' costs 1.5 tokens if a later pass frees them."
)


if __name__ == '__main__':
    d = bf.build()
    tags = {"ariaThinkOpen": "<thinking>", "ariaThinkClose": "</thinking>"}
    off, _ = bf.exact(d['prompts'][bf.P]['content'], {})
    twin, _ = bf.exact(d['prompts'][bf.T]['content'], {})
    on, st = bf.exact(d['prompts'][bf.P]['content'], tags)
    tc_off, _ = bf.exact(d['tc']['post_history_logic_core'], {"aria-logic-core": "on"})
    tc_on, _ = bf.exact(d['tc']['post_history_logic_core'], dict(tags, **{"aria-logic-core": "on"}))
    tc_none, _ = bf.exact(d['tc']['post_history_logic_core'], {})
    assert off == twin == 220.0 and tc_none == 0
    d['tokens'] = {
        bf.P: off,
        bf.T: twin,
        'tc.post_history_logic_core': tc_off,
        'tc.post_history_logic_core with aria-logic-core off': tc_none,
        'Logic Core with Logic Core Tags on (either prompt)': on,
        'tc.post_history_logic_core with aria-thinking-tags on': tc_on,
        'ariaPlanCue (Tags on, unchanged from ARIA)': len(st['ariaPlanCue']) / 4,
        'group G3 (ceiling 220; Tags off, no module lines; plain and twin never run together)': off,
    }
    d['notes'] = NOTES
    d['judge_notes'] = JUDGE_NOTES
    open(OUT, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2))
    print('wrote', OUT)
    print(json.dumps(d['tokens'], ensure_ascii=False, indent=1))
