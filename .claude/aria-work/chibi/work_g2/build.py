#!/usr/bin/env python3
"""Scratch builder for G2.

Reads texts from this directory:
  codex_lines.txt   the <anti_slop> block, one rule per line (tags included)
  echo.txt, chop.txt  the two gate setvar bodies (one line each)
  gate_lines.txt    the gate's own lines, one per line, keyed by label (see GATE_KEYS)
  comments.json     {"codex": "...", "gate": "..."}  comment texts (without {{// and }})
and writes a draft JSON built by editing the SOURCE CC/TC text line by line, so the wiring is preserved by construction.
"""
import json, re, sys, os

S = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work'
W = S + '/chibi/work_g2'
CC = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json", encoding='utf-8'))
TC = json.load(open(S + "/chibi/src/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
BY = {p['identifier']: p for p in CC['prompts']}
CODEX_ID = '9869a1e5-ec75-518a-a9fa-0a8db9600ee0'

# gate line index in the source gate (0 = first line of the content, the comment line)
# key -> (index, prefix macro text kept in front of the line)
GATE_KEYS = [
    ('header',     2, ''),
    ('contrast',   3, ''),
    ('balance',    4, ''),
    ('count',      5, ''),
    ('humour',     6, ''),
    ('paragraphs', 7, ''),
    ('register',   9, '{{/if}}'),
    ('work',      10, '{{#if !.ariaFlashGate}}'),
    ('card',      11, '{{/if}}'),
    ('narration', 12, ''),
    ('senses',    13, ''),
    ('knows',     15, '{{/if}}'),
    ('secrets',   16, ''),
    ('people',    17, ''),
    ('follow',    25, '{{/if}}'),
]


def read(name):
    return open(os.path.join(W, name), encoding='utf-8').read()


def build(codex_file='codex_lines.txt', gate_file='gate_lines.txt', echo_file='echo.txt', chop_file='chop.txt', comments_file='comments.json'):
    com = json.load(open(os.path.join(W, comments_file), encoding='utf-8'))
    # ---- codex
    src = BY[CODEX_ID]['content']
    m = re.match(r'\{\{//.*?\}\}\{\{trim\}\}\n', src, re.S)
    lines = read(codex_file).rstrip('\n')
    echo = read(echo_file).strip('\n')
    chop = read(chop_file).strip('\n')
    codex = ('{{// ' + com['codex'] + '}}{{trim}}\n'
             '{{setvar::ariaEchoGate::' + echo + '}}{{setvar::ariaChopGate::' + chop + '}}' + lines)
    # ---- gate
    g = BY['jailbreak']['content']
    glines = g.split('\n')
    new = read(gate_file).rstrip('\n').split('\n')
    keys = [k for k, _, _ in GATE_KEYS]
    assert len(new) == len(keys), (len(new), len(keys))
    for (k, idx, prefix), text in zip(GATE_KEYS, new):
        glines[idx] = prefix + text
    glines[0] = '{{// ' + com['gate'] + '}}{{trim}}'
    gate = '\n'.join(glines)
    # ---- tc gate: same lines plus TC's own notes
    tcl = glines[1:]  # from <final_gate>
    tcl = list(tcl)
    adds = {
        13: ' A message written as {{user}} skips it.',   # Echo print (index inside glines: 14 -> tcl 13)
        18: ' A message written as {{user}} skips it.',   # Pov print (19 -> 18)
        19: ' A message written as {{user}} carries none.',  # Ledger (20 -> 19)
        23: ' A message written as {{user}} skips it.',   # Hold (24 -> 23)
    }
    for i, t in adds.items():
        tcl[i] = tcl[i] + t
    tc_gate = '\n'.join(tcl)
    return {
        'prompts': {
            CODEX_ID: {'name': BY[CODEX_ID]['name'], 'content': codex},
            'jailbreak': {'name': BY['jailbreak']['name'], 'content': gate},
        },
        'tc': {'post_history_gate': tc_gate},
    }


if __name__ == '__main__':
    out = build()
    dest = sys.argv[1] if len(sys.argv) > 1 else W + '/draft_wip.json'
    json.dump(out, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', dest)
