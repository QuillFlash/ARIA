#!/usr/bin/env python3
"""Build Chibi TC from ARIA TC by raw-text replacement.

usage: python3 build_chibi_tc.py [--out PATH] [--comments comments.json] [--logic-core auto|on|off] [--glue capped|finals] [--dry]

Copies ARIA TC's raw text and replaces each segment (parsed old text -> parsed new text, escaped the JSON way) with an asserted
occurrence count: G1 main_prompt, readme_comment, custom_instructions_comment; G2 anti_slop_block and the post_history gate; G3 the
post_history Logic Core; G4 the scene engine and the six if_aria-* blocks; G5 the three blocks and their switch comments; G6 the seven
module blocks and their switch comments; the JB block and switch comment from JB.json; the switch comments the finals do not supply
(from comments.json); sysprompt.name and context.name. Then verifies the result against an in-memory expected object.
"""
import argparse, json, re, sys
from pathlib import Path

REPO = Path('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA')
W = REPO / '.claude/aria-work'
SRC = REPO / "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
DST = REPO / "Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"
sys.path.insert(0, str(REPO / 'tools'))
import aria_budget as ab  # noqa: E402

OLD_NAME = 'ARIA 1.0 beta 8 (Text Completions)'
NEW_NAME = 'ARIA 1.0 beta 8 Chibi Edition (Text Completions)'

# TC's own glue for "a message written as {{user}}" (Impersonate has no entry of its own in TC). With the finals' texts as they are,
# Chibi TC's everything ON measures 3,029 against the 3,000 cap (the glue costs about 64 tokens there; CC pays 0 for it, since its
# Impersonation Turn entry renders on Impersonate turns only). --glue capped (the default) keeps every function and every shared line
# word for word but spends the glue only once: the four per-line gate notes print only while The Logic Core is off, and with it on the
# plan's closing sentence names those gate lines too. --glue finals leaves the finals' texts untouched (3,029).
NOTE = ' A message written as {{user}} skips it.'
NOTE_NONE = ' A message written as {{user}} carries none.'
GATE_NOTES = [  # (variable, the finals' note)
    ('ariaEchoGate', NOTE), ('ariaPovGate', NOTE), ('ariaLedgerGate', NOTE_NONE), ('ariaHoldGate', NOTE)]
CLOSE_OLD = 'with no Fate, Bonds, Ledger, Layers, Role or Frank line.'
CLOSE_NEW = 'with no Fate, Bonds, Ledger, Layers, Role, Frank, Own words or POV line.'

# the switches whose comments the finals do not supply (written for Chibi, costs measured the guide's way)
OWN_COMMENT_SWITCHES = ['aria-logic-core', 'aria-thinking-tags', 'aria-adult', 'aria-freaky', 'aria-hybrid-pov',
                        'aria-npc-voice', 'aria-anthro', 'aria-scent']


def esc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def load_finals():
    f = {}
    for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6'):
        f[g] = json.loads((W / 'chibi/final' / f'{g}.json').read_text(encoding='utf-8'))
    f['JB'] = json.loads((W / 'chibi/final/JB.json').read_text(encoding='utf-8'))
    return f


def if_block(c, open_tag):
    """(open index, body start, body end, end index just past the closing {{/if}}) of the one block that opens with open_tag."""
    assert c.count(open_tag) == 1, (open_tag, c.count(open_tag))
    i = c.index(open_tag)
    bs = i + len(open_tag)
    then, els, end = ab.split_if(c, bs)
    assert els is None, open_tag
    return i, bs, bs + len(then), end


def switch_comment(c, sw):
    """(start, end of the comment, the comment text) of the {{// ... }} that stands right before {{.<sw> = ...}}."""
    m = list(re.finditer(r'(\{\{//[^\n]*?\}\})\{\{\.%s = (?:on|off)\}\}' % re.escape(sw), c))
    assert len(m) == 1, (sw, len(m))
    return m[0].start(1), m[0].end(1), m[0].group(1)


def build_segments(c, ph, f, comments, logic_core, glue):
    """[(label, old, new)] in parsed space for sysprompt.content, and the same for post_history, from the original parsed texts."""
    g1, g2, g3, g4, g5, g6, jb = (f[k] for k in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'JB'))
    seg = []

    def add(label, a, b, new):
        seg.append((label, c[a:b], new))

    # README comment: '{{// README' through its closing '}}{{trim}}'
    a = c.index('{{// README')
    b = c.index('}}{{trim}}\n{{// 🎛️ ARIA SWITCHES') + len('}}{{trim}}')
    add('readme_comment', a, b, g1['tc']['readme_comment'])
    # custom instructions comment only
    a = c.index('{{// If you have any additional')
    b = c.index('}}{{trim}}\n{{.player-instructions =') + 2
    add('custom_instructions_comment', a, b, g1['tc']['custom_instructions_comment'])
    # Main Prompt: '{{setvar::ariaDice::}}' through the '{{/if}}' that closes the player-instructions block
    assert c.count('{{setvar::ariaDice::}}') == 1
    a = c.index('{{setvar::ariaDice::}}')
    b = c.index('{{/if}}', c.index('{{getvar::player-instructions}}')) + len('{{/if}}')
    add('main_prompt', a, b, g1['tc']['main_prompt'])
    # scene engine
    assert c.count('<scene_engine>') == 1 and c.count('</scene_engine>') == 1
    a = c.index('<scene_engine>')
    b = c.index('</scene_engine>') + len('</scene_engine>')
    add('scene_engine', a, b, g4['tc']['scene_engine'])
    # anti-slop block
    assert c.count('{{setvar::ariaEchoGate::- ') == 1 and c.count('</anti_slop>') == 1
    a = c.index('{{setvar::ariaEchoGate::- ')
    b = c.index('</anti_slop>') + len('</anti_slop>')
    add('anti_slop_block', a, b, g2['tc']['anti_slop_block'])
    # blocks whose body (between the {{#if}} and its own {{/if}}) is replaced
    for sw, new in (('aria-adult', g4['tc']['if_aria-adult']), ('aria-freaky', g4['tc']['if_aria-freaky']),
                    ('aria-hybrid-pov', g4['tc']['if_aria-hybrid-pov']), ('aria-npc-voice', g4['tc']['if_aria-npc-voice']),
                    ('aria-anthro', g4['tc']['if_aria-anthro']), ('aria-scent', g4['tc']['if_aria-scent']),
                    ('aria-time-place', g5['tc']['time_place_block']), ('aria-fate', g5['tc']['fate_block']),
                    ('aria-bonds', g5['tc']['bonds_block'])):
        _, bs, be, _ = if_block(c, '{{#if .%s}}' % sw)
        add('if_' + sw, bs, be, new)
    # the JB block: the whole {{#if .aria-jailbreak}} ... {{/if}}
    i, bs, be, end = if_block(c, '{{#if .aria-jailbreak}}')
    assert len(jb['lines']) == 2 and all('\n' not in l and '\\' not in l for l in jb['lines'])
    jb_block = ('{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::'
                + jb['lines'][0] + '\n' + jb['lines'][1] + '}}{{/if}}{{/if}}')
    add('jailbreak_block', i, end, jb_block)
    # the seven module blocks, whole (from the open tag through the closing {{/if}})
    for sw in ('aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro', 'aria-patch-mimo-flash', 'aria-patch-deepseek',
               'aria-flash-gate', 'aria-character-hold'):
        open_tag = '{{if .aria-flash-gate}}' if sw == 'aria-flash-gate' else '{{#if .%s}}' % sw
        i, bs, be, end = if_block(c, open_tag)
        add('module_' + sw, i, end, g6['tc']['module_' + sw])
    # switch comments: supplied by G5, G6 and the JB; the rest from `comments` (the ones not given keep ARIA's text). Each segment
    # holds the comment and its own '{{.aria-x = state}}' tag, so it is unique, and the Logic Core's default folds into its segment.
    supplied = {'aria-time-place': g5['tc']['switch_comment_time_place'], 'aria-fate': g5['tc']['switch_comment_fate'],
                'aria-bonds': g5['tc']['switch_comment_bonds'], 'aria-jailbreak': jb['tc_switch_comment']}
    for sw in ('aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro', 'aria-patch-mimo-flash', 'aria-patch-deepseek',
               'aria-flash-gate', 'aria-character-hold'):
        supplied[sw] = g6['tc']['switch_comment_' + sw]
    for sw in OWN_COMMENT_SWITCHES:
        if comments.get(sw):
            supplied[sw] = comments[sw]
    for sw in re.findall(r'\{\{\.(aria-[\w-]+) = (?:on|off)\}\}', c):
        a, b, old_comment = switch_comment(c, sw)
        tag = re.match(r'\{\{\.%s = (on|off)\}\}' % re.escape(sw), c[b:])
        state = tag.group(1)
        new_state = logic_core if sw == 'aria-logic-core' else state
        new_comment = supplied.get(sw, old_comment)
        if new_comment == old_comment and new_state == state:
            continue
        end = b + tag.end()
        add('switch_' + sw, a, end, new_comment + '{{.%s = %s}}' % (sw, new_state))
    # post_history: G3's Logic Core part, then G2's gate, joined directly
    lc_part, gate_part = g3['tc']['post_history_logic_core'], g2['tc']['post_history_gate']
    if glue == 'capped':
        for var, note in GATE_NOTES:
            old = '{{getvar::%s}}%s\n{{/if}}' % (var, note)
            assert gate_part.count(old) == 1, (var, gate_part.count(old))
            gate_part = gate_part.replace(old, '{{getvar::%s}}{{#if !.aria-logic-core}}%s{{/if}}\n{{/if}}' % (var, note))
        assert lc_part.count(CLOSE_OLD) == 1
        lc_part = lc_part.replace(CLOSE_OLD, CLOSE_NEW)
    new_ph = lc_part + gate_part
    assert lc_part.endswith('{{/if}}\n{{/if}}') and gate_part.startswith('<final_gate>')
    return seg, (ph, new_ph)


def disjoint(c, seg):
    """Every old text occurs once in the original content, and the segments do not overlap."""
    spans = []
    for label, old, new in seg:
        assert c.count(old) == 1, (label, c.count(old))
        i = c.index(old)
        spans.append((i, i + len(old), label))
    spans.sort()
    for (a1, b1, l1), (a2, b2, l2) in zip(spans, spans[1:]):
        assert b1 <= a2, f'segments overlap: {l1} and {l2}'
    return spans


def build(comments, logic_core, glue):
    raw0 = open(SRC, encoding='utf-8', newline='').read()
    d0 = json.loads(raw0)
    assert json.dumps(d0, ensure_ascii=False, indent=4) == raw0, 'ARIA TC does not round-trip'
    c, ph = d0['sysprompt']['content'], d0['sysprompt']['post_history']
    f = load_finals()
    seg, (old_ph, new_ph) = build_segments(c, ph, f, comments, logic_core, glue)
    spans = disjoint(c, seg)
    raw = raw0
    # content segments, applied to the raw text with asserted counts
    for label, old, new in seg:
        o, n = esc(old), esc(new)
        assert raw.count(o) == 1, f'{label}: found {raw.count(o)} times'
        raw = raw.replace(o, n)
    # post_history, whole
    assert raw.count(esc(old_ph)) == 1
    raw = raw.replace(esc(old_ph), esc(new_ph))
    # names
    nm = f'"name": "{OLD_NAME}"'
    assert raw.count(nm) == 2, raw.count(nm)
    raw = raw.replace(nm, f'"name": "{NEW_NAME}"')
    return raw0, raw, d0, seg, (old_ph, new_ph), f


def expected(d0, seg, new_ph):
    exp = json.loads(json.dumps(d0, ensure_ascii=False))
    c = exp['sysprompt']['content']
    spans = []
    for label, old, new in seg:
        i = c.index(old)
        spans.append((i, i + len(old), new))
    for a, b, new in sorted(spans, reverse=True):
        c = c[:a] + new + c[b:]
    exp['sysprompt']['content'] = c
    exp['sysprompt']['post_history'] = new_ph
    exp['sysprompt']['name'] = NEW_NAME
    exp['context']['name'] = NEW_NAME
    return exp


def verify(raw0, raw, d0, seg, new_ph):
    d = json.loads(raw)
    assert json.dumps(d, ensure_ascii=False, indent=4) == raw, 'Chibi TC does not round-trip as indent=4'
    assert not raw.endswith('\n')
    exp = expected(d0, seg, new_ph)
    assert json.dumps(exp, ensure_ascii=False, indent=4) == raw, 'Chibi TC differs from the expected object'
    # nothing else moved: keys, the context fields other than the name, the story string
    assert list(d.keys()) == list(d0.keys())
    assert {k: v for k, v in d['context'].items() if k != 'name'} == {k: v for k, v in d0['context'].items() if k != 'name'}
    assert d['sysprompt'].keys() == d0['sysprompt'].keys()
    c = d['sysprompt']['content']
    for sw in re.findall(r'\{\{\.(aria-[\w-]+) = (?:on|off)\}\}', d0['sysprompt']['content']):
        assert len(re.findall(r'\{\{\.%s = (?:on|off)\}\}' % re.escape(sw), c)) == 1, sw
    assert re.findall(r'\{\{\.(aria-[\w-]+) = ', c) == re.findall(r'\{\{\.(aria-[\w-]+) = ', d0['sysprompt']['content'])
    assert c.endswith('# Reference')
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(DST))
    ap.add_argument('--comments', default=str(W / 'build/chibi_tc/comments.json'))
    ap.add_argument('--logic-core', choices=('auto', 'on', 'off'), default='auto',
                    help='auto: ship the Logic Core on only when the lean start (Logic Core off) falls below 1,350 tokens')
    ap.add_argument('--glue', choices=('capped', 'finals'), default='capped')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    comments = json.loads(Path(a.comments).read_text(encoding='utf-8')) if Path(a.comments).exists() else {}
    lc = a.logic_core
    if lc == 'auto':
        raw0, raw, d0, seg, (old_ph, new_ph), f = build(comments, 'off', a.glue)
        lean = ab.analyse_tc(json.loads(raw), DST.name)[0]['shipped (lean, 32k)']
        lc = 'on' if lean < 1350 else 'off'
        print(f'lean start with the Logic Core off: {lean} tokens -> aria-logic-core ships {lc}')
    raw0, raw, d0, seg, (old_ph, new_ph), f = build(comments, lc, a.glue)
    verify(raw0, raw, d0, seg, new_ph)
    if a.dry:
        print('dry run OK;', len(raw), 'chars;', len(seg), 'content segments')
        return
    Path(a.out).write_text(raw, encoding='utf-8', newline='')
    print('wrote', a.out, len(raw), 'chars;', len(seg), 'content segments; logic core default:', lc, '; glue:', a.glue)


if __name__ == '__main__':
    main()
