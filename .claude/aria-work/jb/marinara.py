#!/usr/bin/env python3
"""Wire the 🔓 Jailbreak into the Marinara "Agent Gating" preset (JB.md, "Wiring in Marinara").

CC is the source of truth: the plan lines and their count are read from CC's JB prompt, so the rendered text cannot drift.
Marinara is the only file this edits; CC, TC and the docs are never touched, and nothing is staged or committed.

What it changes, under the condition  logic_options contains "JAILBREAK" && adult_mode != "NONE":
  - both Logic Core sections (assistant and system-role twin): the counter after the Ledger counter, and the plan
    lines between the Ledger block and "- Fresh:", the way CC prints {{getvar::ariaJb}} there
  - the Last-Mile Gate: the same counter, because the gate recomputes logicCoreLines for its plan cue
    ("Begin with <thinking>, then N dashed lines ...") and would otherwise disagree with the plan
  - the logic_options choice block: the option (a fresh opt_ id, left out of defaultChoices) and one question sentence
  - the preset description (one note), preset.updatedAt and the export's exportedAt

The file round-trips as json.dumps(d, ensure_ascii=False, indent='\t') with no trailing newline; that is checked before
and after writing. Every replacement asserts how often its anchor occurs. The script refuses to run when JAILBREAK is
already wired in, so it cannot apply twice.

usage: python3 marinara.py [--dry]
"""
import argparse
import json
import re
import secrets
import string
import sys
from pathlib import Path

REPO = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
CC_FILE = REPO / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
MAR_FILE = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Agent Gating.json"

JB_ID = '05f6e90d-b30b-48d5-b2bf-26a6e45faffa'      # CC's 🔓 Jailbreak (needs Adult Context)
STAMP = '2026-10-16T12:00:00.000Z'                   # preset.updatedAt and the export's exportedAt
COND = 'logic_options contains "JAILBREAK" && adult_mode != "NONE"'
OPTION_LABEL = '🔓 Jailbreak (needs Adult Context)'
OPTION_VALUE = 'JAILBREAK'

LOGIC_CORE = '🧠 The Logic Core'
LOGIC_TWIN = '🧠 The Logic Core (system-role twin)'
GATE = '🚪 Last-Mile Gate'

# Labels the JB must not reuse (JB.md, "Form")
TAKEN_LABELS = {
    'OOC', 'Scene', 'Knows', 'Mode', 'Voice', 'Move', 'Fate', 'Bonds', 'Ledger', 'Fresh', 'Check', 'Person', 'Replies',
    'Filler', 'Gemini', 'Contrast', 'Negation runs', 'Flow', 'Card details', 'Echo', 'Repeats', 'Bodies', 'Layers',
    'Tally', 'Pushback', 'Restate', 'Joins',
}
NUMBER_WORDS = {2: 'two', 4: 'four'}


def dump(doc):
    """The exact round-trip format of the Marinara export."""
    return json.dumps(doc, ensure_ascii=False, indent='\t')


def compact(value):
    """The format of a choice block's `options` string."""
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def cc_jb():
    """(N, lines) from CC's JB prompt: ...{{#if .ariaModeLine}}{{setvar::ariaJbLines::N}}{{setvar::ariaJb::<lines>}}{{/if}}"""
    cc = json.loads(CC_FILE.read_text(encoding='utf-8'))
    hit = [p for p in cc['prompts'] if p['identifier'] == JB_ID]
    assert len(hit) == 1, f'CC has {len(hit)} prompts with identifier {JB_ID}'
    prompt = hit[0]
    assert prompt['name'] == OPTION_LABEL, f"CC's JB is named {prompt['name']!r}, not {OPTION_LABEL!r}"
    m = re.search(r'\{\{#if \.ariaModeLine\}\}\{\{setvar::ariaJbLines::(\d+)\}\}\{\{setvar::ariaJb::(.*)\}\}\{\{/if\}\}\s*$',
                  prompt['content'], re.S)
    assert m, "CC's JB content does not end in the expected setvar block"
    n, lines = int(m.group(1)), m.group(2).split('\n')
    assert n in NUMBER_WORDS and len(lines) == n, f'JB must have 2 or 4 lines; CC says {n} and holds {len(lines)}'
    labels = []
    for ln in lines:
        lm = re.match(r'- ([^:]+): \S', ln)
        assert lm, f'plan line does not start with "- Label: ": {ln[:40]!r}'
        labels.append(lm.group(1))
    assert len(set(labels)) == len(labels), f'duplicate labels {labels}'
    assert not TAKEN_LABELS & set(labels), f'labels already in use: {TAKEN_LABELS & set(labels)}'
    tokens = len('\n'.join(lines)) / 4
    assert tokens <= 130, f'JB lines are {tokens:.0f} tokens, over the 130 cap'
    assert '{{' not in re.sub(r'\{\{user\}\}', '', '\n'.join(lines)), 'a macro other than {{user}} sits in the JB lines'
    return n, lines


def edit(text, old, new, expect, what):
    found = text.count(old)
    assert found == expect, f'{what}: anchor found {found} times, expected {expect}'
    return text.replace(old, new)


def fresh_option_id(raw):
    alphabet = string.ascii_letters + string.digits + '_-'
    while True:
        oid = 'opt_' + ''.join(secrets.choice(alphabet) for _ in range(12))
        if oid not in raw:
            return oid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true', help='report what would change; write nothing')
    a = ap.parse_args()

    raw = MAR_FILE.read_text(encoding='utf-8')
    doc = json.loads(raw)
    assert dump(doc) == raw, 'Marinara file does not round-trip exactly before the edit'
    assert OPTION_VALUE not in raw and 'ariaJb' not in raw, 'the JB is already wired into the Marinara file; nothing to do'
    n, lines = cc_jb()
    word = NUMBER_WORDS[n]

    data = doc['data']
    sections = {s['name']: s for s in data['sections']}
    for name in (LOGIC_CORE, LOGIC_TWIN, GATE):
        assert name in sections, f'section {name!r} not found'

    # 1. The counter, right after the Ledger counter and before Character Hold's, in all three places that compute
    #    logicCoreLines (the two Logic Cores and the gate's plan cue)
    hold_ctr = '{{#if core_modules contains "HOLD"}}{{addvar::logicCoreLines::1}}{{/if}}'
    jb_ctr = '{{#if ' + COND + '}}{{addvar::logicCoreLines::' + str(n) + '}}{{/if}}'
    for name in (LOGIC_CORE, LOGIC_TWIN, GATE):
        s = sections[name]
        s['content'] = edit(s['content'], hold_ctr, jb_ctr + hold_ctr, 1, f'{name} counter')

    # 2. The plan lines in both Logic Cores: right after the Ledger block's {{/if}}, before "- Fresh:", in CC's newline pattern
    fresh = '- Fresh: one or two details new to the chat'
    jb_print = '{{#if ' + COND + '}}' + '\n'.join(lines) + '\n{{/if}}'
    for name in (LOGIC_CORE, LOGIC_TWIN):
        s = sections[name]
        s['content'] = edit(s['content'], '{{/if}}' + fresh, '{{/if}}' + jb_print + fresh, 1, f'{name} plan lines')

    # 3. The option, one question sentence, and a note in the description
    blocks = [c for c in data['choiceBlocks'] if c['variableName'] == 'logic_options']
    assert len(blocks) == 1, 'logic_options choice block not found exactly once'
    lo = blocks[0]
    options = json.loads(lo['options'])
    assert compact(options) == lo['options'], "logic_options' options string is not in compact JSON format"
    assert [o['value'] for o in options] == ['THINKTAGS', 'REDUCE'], f"unexpected logic options {[o['value'] for o in options]}"
    oid = fresh_option_id(raw)
    options.append({'id': oid, 'label': OPTION_LABEL, 'value': OPTION_VALUE})
    lo['options'] = compact(options)

    q_tail = ' Deselect all options to disable.'
    q_new = ' Jailbreak: ' + word + ' extra plan lines for frank adult fiction (sex stays between adults); they print only while Adult Context is on.'
    lo['question'] = edit(lo['question'], q_tail, q_new + q_tail, 1, 'logic_options question')

    preset = data['preset']
    d_anchor = ' Recommended samplers (set in your connection'
    d_note = (' Includes the 🔓 Jailbreak Logic Core option (off by default; needs Adult Context): ' + word
              + ' extra plan lines for frank adult fiction between adults.')
    preset['description'] = edit(preset['description'], d_anchor, d_note + d_anchor, 1, 'description')
    assert OPTION_VALUE not in json.loads(preset['defaultChoices']).get('logic_options', []), 'JB must stay out of defaultChoices'

    # 4. Stamps
    doc['exportedAt'] = STAMP
    preset['updatedAt'] = STAMP

    out = dump(doc)
    assert json.loads(out) == doc and dump(json.loads(out)) == out, 'new file does not round-trip'
    print(f'JB: {n} lines from CC prompt {JB_ID[:8]}; option id {oid}; condition: {COND}')
    print(f'file size {len(raw)} -> {len(out)} characters (+{len(out) - len(raw)})')
    if a.dry:
        print('dry run: nothing written')
        return
    MAR_FILE.write_text(out, encoding='utf-8')
    back = MAR_FILE.read_text(encoding='utf-8')
    assert back == out and dump(json.loads(back)) == back and not back.endswith('\n'), 'round trip failed after writing'
    print('written; round trip OK, no trailing newline')


if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print('ABORTED:', e, file=sys.stderr)
        sys.exit(1)
