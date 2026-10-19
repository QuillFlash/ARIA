#!/usr/bin/env python3
"""Second pass on the Micro-based Logic Core: Micro's Completion task as an eighth fixed plan line, its
"a skipped task is a failure" and "start on the game state" rules in both modes, its closing cue, Freaky's mode check,
and "sex only between adults" back in the Mode lines. Applies on top of the first pass, in all six presets and both
regex sets.

usage: python3 build2.py SRC_DIR OUT_DIR
"""
import json, re, sys
from pathlib import Path

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
CC = "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TC = "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
MAR = "Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json"
CCC = "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"
CTC = "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"
CMAR = "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Agent Gating.json"
RGX = 'regex/ARIA 1.0 Regex Scripts (Text Completions).json'
STAMP = '2026-10-17T12:00:00.000Z'


def esc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def sub(text, old, new, count=1, label=''):
    n = text.count(old)
    if n != count:
        raise SystemExit(f'{label}: expected {count} of {old[:90]!r}, found {n}')
    return text.replace(old, new)


FULL = [
    ('count', '{{setvar::logicCoreLines::7}}', '{{setvar::logicCoreLines::8}}'),
    ('hdr', 'Reasoning opens on the OOC line and writes {{getvar::logicCoreLines}} dashed lines, then go; the reply follows.',
     'Reasoning writes {{getvar::logicCoreLines}} dashed lines, then go; the reply follows.'),
    ('rules', 'I write every line, in order and none skipped, as telegraphic fragments that paraphrase what anyone said, never '
              'reply sentences or drafts, each building on the last and settled once written, all shorter than one reply paragraph',
     'I write every line in order, starting on the game state, as telegraphic fragments that paraphrase what anyone said, '
     'never reply sentences or drafts, each building on the last and settled once written, all shorter than one reply '
     'paragraph; a skipped line is a failure'),
    ('completion', '- Check: lists in ones or twos; any joke small and card-true, sincere moments plain.\n- go',
     '- Check: lists in ones or twos; any joke small and card-true, sincere moments plain.\n'
     '- Completion: I am the game master creating this immersive simulation, not a helpful AI assistant; creative risk is '
     'welcome and perfection unnecessary; concise ideas only, then the reasoning closes and the reply comes at once, with no '
     'further reasoning.\n- go'),
    ('end', 'Reasoning ends at go, with no further reasoning. The reply:',
     'Reasoning ends at go with every line done, and no further reasoning follows. The reply, generated at once:'),
]
FULL_MODES = [
    ('adult', '- Mode: realism; persona-true; each plea new; a sexual, violent, cruel or dark beat gets its act, anatomy, '
              'sensations and tone planned in full.',
     '- Mode: realism; persona-true; each plea new; sex only between adults; a sexual, violent, cruel or dark beat gets its '
     'act, anatomy, sensations and tone planned in full.'),
    ('freaky', "- Mode: freaky; escalate; characters described lewdly, each detail new to the last four replies; the beat's act, "
               'anatomy, sensations and tone planned in full.',
     "- Mode: freaky; escalate; NPC wants align eagerly with {{user}}'s; sex only between adults; characters described "
     "lewdly, each detail new to the last four replies; the beat's act, anatomy, sensations and tone planned in full."),
]
CHIBI = [
    ('count', '{{setvar::logicCoreLines::7}}', '{{setvar::logicCoreLines::8}}'),
    ('rules', "I'm the GM, not a helpful AI assistant: every line, none skipped; fragments paraphrase speech, no drafts; settled, "
              'built on; under a reply paragraph; creative risk over perfection',
     'All lines in order from the game state; fragments paraphrase speech, no drafts; settled; under a paragraph'),
    ('move', '(fight, lie, seduce, refuse; help/hold too), nervous cards aside', '(fight, lie, seduce, refuse), nervous cards aside'),
    ('completion', '- Check: lists 1-2; jokes small, none when sincere.\n- go',
     "- Check: lists 1-2; jokes small, none when sincere.\n- Completion: GM, not a helpful AI assistant; creative risk over "
     'perfection; reply at once.\n- go'),
    ('closing', 'plan blended in, never a paragraph per plan line.', 'plan blended in, no paragraph per plan line.'),
]
CHIBI_TC = [('tc close', "For a message written as {{user}}, plan only {{user}}'s move; skip any Fate, Bonds, Ledger, Layers, Own words "
                         'or POV line.',
             'For a message written as {{user}}, plan only that move, no Fate, Bonds, Ledger, Layers, Own words or POV line.')]
CHIBI_MODES = [
    ('adult', '- Mode: realism, persona-true; a sexual/violent/cruel/dark beat: act, anatomy, sensation, tone in full.',
     '- Mode: realism, persona-true, adults only; a sexual/violent/cruel/dark beat: act, anatomy, sensation, tone in full.'),
    ('freaky', '- Mode: freaky, escalating lewdly; act, anatomy, sensation, tone in full.',
     '- Mode: freaky, lewd, adults only; act, anatomy, sensation, tone in full.'),
]


def apply(t, edits, label):
    for key, old, new in edits:
        t = sub(t, old, new, 1, f'{label} {key}')
    return t


def fix_regex(f):
    return f.replace('|Restate|Joins)', '|Restate|Joins|Completion)')


def fix_regex_scripts(raw, scripts, label):
    from collections import Counter
    for old, n in Counter(s['findRegex'] for s in scripts).items():
        new = fix_regex(old)
        if new != old:
            raw = sub(raw, esc(old), esc(new), n, f'{label[-30:]} regex')
    return raw


def cc_file(name, core_edits, mode_edits):
    raw = (SRC / name).read_text(encoding='utf-8')
    doc = json.loads(raw)
    by = {p['identifier'][:8]: p for p in doc['prompts']}
    for pre in ('15b770cf', '591b8c15'):
        old = by[pre]['content']
        raw = sub(raw, esc(old), esc(apply(old, core_edits, f'{name[-30:]} {pre}')), 1, pre)
    for pre, (key, old_line, new_line) in (('nsfw', mode_edits[0]), ('4537b57d', mode_edits[1])):
        old = by[pre]['content']
        raw = sub(raw, esc(old), esc(sub(old, old_line, new_line, 1, f'{pre} {key}')), 1, pre)
    raw = fix_regex_scripts(raw, doc['extensions']['regex_scripts'], name)
    json.loads(raw)
    (OUT / name).write_text(raw, encoding='utf-8')


def tc_file(name, core_edits, mode_edits):
    raw = (SRC / name).read_text(encoding='utf-8')
    sp = json.loads(raw)['sysprompt']
    c, ph = sp['content'], sp['post_history']
    c2 = c
    for key, old_line, new_line in mode_edits:
        c2 = sub(c2, '{{setvar::ariaModeLine::' + old_line + '}}', '{{setvar::ariaModeLine::' + new_line + '}}', 1, f'tc {key}')
    ph2 = apply(ph, core_edits, 'tc')
    raw = sub(raw, esc(c), esc(c2), 1, 'tc content')
    raw = sub(raw, esc(ph), esc(ph2), 1, 'tc post_history')
    json.loads(raw)
    (OUT / name).write_text(raw, encoding='utf-8')


def mar_file(name, core_edits, mode_edits):
    raw = (SRC / name).read_text(encoding='utf-8')
    d = json.loads(raw)
    assert json.dumps(d, ensure_ascii=False, indent='\t') == raw
    secs = {s['name']: s for s in d['data']['sections']}
    for nm in ('🧠 The Logic Core', '🧠 The Logic Core (system-role twin)'):
        t = apply(secs[nm]['content'], core_edits, nm)
        for key, old_line, new_line in mode_edits:
            t = sub(t, old_line, new_line, 1, f'{nm} {key}')
        secs[nm]['content'] = t
    g = secs['🚪 Last-Mile Gate']
    g['content'] = sub(g['content'], '{{setvar::logicCoreLines::7}}', '{{setvar::logicCoreLines::8}}', 1, 'gate count')
    d['data']['preset']['updatedAt'] = STAMP
    if 'exportedAt' in d:
        d['exportedAt'] = STAMP
    (OUT / name).write_text(json.dumps(d, ensure_ascii=False, indent='\t'), encoding='utf-8')


def regex_file():
    raw = (SRC / RGX).read_text(encoding='utf-8')
    raw = fix_regex_scripts(raw, json.loads(raw), RGX)
    json.loads(raw)
    (OUT / RGX).parent.mkdir(parents=True, exist_ok=True)
    (OUT / RGX).write_text(raw, encoding='utf-8')


cc_file(CC, FULL, FULL_MODES)
cc_file(CCC, CHIBI, CHIBI_MODES)
tc_file(TC, FULL, FULL_MODES)
tc_file(CTC, CHIBI + CHIBI_TC, CHIBI_MODES)
mar_file(MAR, FULL, FULL_MODES)
mar_file(CMAR, CHIBI, CHIBI_MODES)
regex_file()
print('built into', OUT)
