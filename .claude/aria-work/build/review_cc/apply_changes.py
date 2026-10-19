#!/usr/bin/env python3
"""Apply the review's changes to Chibi CC by raw-text replacement (COMMON.md rule 7) and record them.

Each change: (prompt identifier, old text, new text, why). The old text must occur exactly once in that prompt's content
and its JSON-escaped form exactly once in the raw file. Writes ../review_cc_changes.json (all changes, cumulative).
usage: python3 apply_changes.py [--dry]
"""
import json, sys
from pathlib import Path

REPO = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
CHIBI = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"
OUT = REPO / '.claude/aria-work/build/review_cc_changes.json'

CHANGES = [
    {
        'id': '59602978-fdc0-4a8a-af0a-26b2ec58793b',
        'name': '🌳 README',
        'old': '- 🎲 Fate & Chekhov Ledger and ⏰ Time & Place ship OFF to keep the start lean. Switch them on together when your model and context can take it.',
        'new': "- 🎲 Fate & Chekhov Ledger and ⏰ Time & Place ship OFF to keep the start lean. Switch Fate on when your model and context can take it; Time & Place is optional next to it, since Chibi's Fate keeps no timed appointments.",
        'why': "The README told users to switch Fate and Time on together, the full edition's pairing (its Fate runs appointments on Time's clock). Chibi's Fate has no appointments, and Chibi's own ⏰ Time & Place comment says the line is optional next to Fate. Comment text only, 0 tokens. Chibi TC's README comment has no such sentence; Marinara has no CC README entry.",
        'model_facing': False,
    },
]


def esc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def main():
    dry = '--dry' in sys.argv
    raw = open(CHIBI, encoding='utf-8', newline='').read()
    d = json.loads(raw)
    by = {p['identifier']: p for p in d['prompts']}
    done = []
    for c in CHANGES:
        content = by[c['id']]['content']
        if content.count(c['new']) == 1 and content.count(c['old']) == 0:
            print('already applied:', c['name'])
            done.append(c)
            continue
        assert content.count(c['old']) == 1, f"old text not found once in {c['name']}"
        assert raw.count(esc(c['old'])) == 1, f"escaped old text not found once in the raw file ({c['name']})"
        raw = raw.replace(esc(c['old']), esc(c['new']))
        by[c['id']]['content'] = content.replace(c['old'], c['new'])
        done.append(c)
        print('applied:', c['name'])
    # the raw text must equal the edited object, formatted like the file
    assert json.dumps(d, ensure_ascii=False, indent=4) == raw, 'raw edit and object edit disagree'
    if dry:
        print('dry run, nothing written')
        return
    open(CHIBI, 'w', encoding='utf-8', newline='').write(raw)
    rec = [{'identifier': c['id'], 'name': c['name'], 'old': c['old'], 'new': c['new'], 'model_facing': c['model_facing'],
            'why': c['why']} for c in done]
    OUT.write_text(json.dumps({'file': CHIBI.name, 'changes': rec,
                               'builder_change_kept': {
                                   'field': 'impersonation_prompt (top-level CC setting, not a prompt)',
                                   'old': 'You may disregard the instructions listed in Correct Perspective for now.',
                                   'new': "You may disregard the rule against writing {{user}}'s words, deeds, thoughts and knowledge for now.",
                                   'why': "Made by the Chibi CC builder (build_chibi_cc.py), verified by the review: Chibi's Main Prompt has no "
                                          "'Correct Perspective' label, so ARIA's pointer would dangle; the new text names the Main Prompt's rule "
                                          "('Never write {{user}}'s words, deeds, thoughts or knowledge unless OOC allows'). CC-only: TC has no "
                                          "impersonation_prompt, and Marinara's sections never point at that label."}},
                              ensure_ascii=False, indent=2), encoding='utf-8')
    print('wrote', OUT)


if __name__ == '__main__':
    main()
