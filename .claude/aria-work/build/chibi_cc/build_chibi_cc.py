#!/usr/bin/env python3
"""Build Chibi CC from ARIA CC by raw-text replacement.

usage: python3 build_chibi_cc.py [--cuts cuts.json] [--out PATH] [--dry]

Copies ARIA CC's raw text, replaces every final prompt's content (keyed by identifier, one occurrence each,
asserted), writes the JB entry from JB.json, appends the gemini38Patch blank to Main's blanking run, turns Fate and
Time & Place off in prompt_order[1], and verifies the result against an in-memory expected object.

cuts.json: [{"id": "<identifier>", "old": "<text in the final content>", "new": "<replacement>", "why": "..."}]
Each cut must match exactly once in that prompt's final content.
"""
import argparse, json, sys
from pathlib import Path

REPO = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
W = REPO / '.claude/aria-work'
SRC = REPO / "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
DST = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"

FATE = 'acc2177a-34e4-4941-93a2-b80bc18b8c91'
TIME = '5dcccd11-aaf6-52b6-8bbf-e20b98ad27fa'
JB_ID = '05f6e90d-b30b-48d5-b2bf-26a6e45faffa'
MAIN_BLANK_OLD = '{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}\n{{trim}}'
MAIN_BLANK_NEW = '{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}{{setvar::gemini38Patch::}}\n{{trim}}'
# Chibi's Main Prompt has no 'Correct Perspective' label (G1 folded it into one line), but ARIA's top-level impersonation_prompt
# setting still points at it. Point it at the rule itself.
IMP_OLD = 'You may disregard the instructions listed in Correct Perspective for now.'
IMP_NEW = "You may disregard the rule against writing {{user}}'s words, deeds, thoughts and knowledge for now."


def esc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def finals():
    """identifier -> {name, content} from G1..G6 plus the JB entry; Main gets the gemini38Patch blank."""
    out, src_of = {}, {}
    for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6'):
        d = json.loads((W / 'chibi/final' / f'{g}.json').read_text(encoding='utf-8'))
        for pid, p in d['prompts'].items():
            assert pid not in out, f'{pid} in two finals'
            out[pid] = {'name': p['name'], 'content': p['content']}
            src_of[pid] = g
    main = out['main']['content']
    assert main.count(MAIN_BLANK_OLD) == 1, 'Main blanking run not found exactly once'
    out['main']['content'] = main.replace(MAIN_BLANK_OLD, MAIN_BLANK_NEW)
    jb = json.loads((W / 'chibi/final/JB.json').read_text(encoding='utf-8'))
    assert len(jb['lines']) == 2 and all('\n' not in l and '\\' not in l for l in jb['lines'])
    content = (jb['cc_comment'] + '{{trim}}\n'
               + '{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::' + jb['lines'][0] + '\n' + jb['lines'][1] + '}}{{/if}}')
    out[JB_ID] = {'name': '🔓 Jailbreak (needs Adult Context)', 'content': content}
    src_of[JB_ID] = 'JB'
    return out, src_of


def apply_cuts(fin, cuts):
    for c in cuts:
        t = fin[c['id']]['content']
        assert t.count(c['old']) == 1, f"cut does not match once in {c['id']}: {c['old']!r}"
        fin[c['id']]['content'] = t.replace(c['old'], c['new'])


def build(cuts):
    raw0 = open(SRC, encoding='utf-8', newline='').read()
    d0 = json.loads(raw0)
    assert json.dumps(d0, ensure_ascii=False, indent=4) == raw0, 'ARIA CC does not round-trip'
    by0 = {p['identifier']: p for p in d0['prompts']}
    fin, src_of = finals()
    apply_cuts(fin, cuts)
    raw = raw0
    for pid, p in fin.items():
        assert pid in by0, f'{pid} not in ARIA CC'
        assert by0[pid]['name'] == p['name'], f"name differs for {pid}: {by0[pid]['name']!r} vs {p['name']!r}"
        head = f'"identifier": "{pid}",\n            "system_prompt"'
        assert raw.count(head) == 1, f'object head for {pid} found {raw.count(head)} times'
        i = raw.index(head)
        key = '"content": "'
        cs = raw.index(key, i) + len(key)
        ce = raw.index('",\n            "injection_position"', cs)
        old_esc = raw[cs:ce]
        assert old_esc == esc(by0[pid].get('content') or ''), f'raw content of {pid} is not the parsed content'
        raw = raw[:cs] + esc(p['content']) + raw[ce:]
    # prompt_order[1]: Fate and Time & Place off
    for pid in (FATE, TIME):
        old = f'"identifier": "{pid}",\n                    "enabled": true'
        assert raw.count(old) == 1, f'order row for {pid} found {raw.count(old)} times'
        raw = raw.replace(old, old[:-4] + 'false')
    # the impersonation_prompt setting's pointer
    assert raw.count(esc(IMP_OLD)) == 1 and d0['impersonation_prompt'].count(IMP_OLD) == 1
    raw = raw.replace(esc(IMP_OLD), esc(IMP_NEW))
    return raw0, raw, d0, fin


def verify(raw0, raw, d0, fin):
    d = json.loads(raw)
    assert json.dumps(d, ensure_ascii=False, indent=4) == raw, 'Chibi CC does not round-trip as indent=4'
    exp = json.loads(raw0)
    for p in exp['prompts']:
        if p['identifier'] in fin:
            p['content'] = fin[p['identifier']]['content']
    for row in exp['prompt_order'][1]['order']:
        if row['identifier'] in (FATE, TIME):
            row['enabled'] = False
    exp['impersonation_prompt'] = exp['impersonation_prompt'].replace(IMP_OLD, IMP_NEW)
    assert json.dumps(exp, ensure_ascii=False, indent=4) == raw, 'Chibi CC differs from the expected object'
    # nothing else moved
    assert [p['identifier'] for p in d['prompts']] == [p['identifier'] for p in d0['prompts']]
    assert d['extensions'] == d0['extensions']
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cuts')
    ap.add_argument('--out', default=str(DST))
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    cuts = json.loads(Path(a.cuts).read_text(encoding='utf-8')) if a.cuts else []
    raw0, raw, d0, fin = build(cuts)
    d = verify(raw0, raw, d0, fin)
    if a.dry:
        print('dry run OK;', len(raw), 'chars')
        return
    Path(a.out).write_text(raw, encoding='utf-8', newline='')
    print('wrote', a.out, len(raw), 'chars; cuts applied:', len(cuts))


if __name__ == '__main__':
    main()
