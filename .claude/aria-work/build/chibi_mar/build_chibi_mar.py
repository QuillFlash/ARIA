#!/usr/bin/env python3
"""Build Chibi Marinara ("... Chibi Edition — Agent Gating.json") from ARIA's Marinara file and the Chibi CC preset.

Source of truth for every model-facing line: Chibi CC (the file in the repository root). Re-run this script after any
change to Chibi CC to re-sync the Marinara text. Base for structure, ids, groups, markers and choice blocks: ARIA's
Marinara file. Never touches CC, TC, the checker or the docs.

usage: python3 build_chibi_mar.py [--check]   (--check only builds in memory and compares with the file on disk)
"""
import json
import re
import secrets
import string
import sys

from common import *
import mar_convert as mc
from mar_convert import sub1, sub_re1
from selftest import comment_of, agents_parts

HERE = Path(__file__).resolve().parent
STAMP = '2026-10-16T12:00:00.000Z'

# ----------------------------------------------------------------------------------------------------------------
# The Agents-only text, compressed Douyin-style: Main's block and the Logic Cores' Scene note come to at most 90 tokens
# together. Rules kept: the engine <context> is an earlier snapshot; apply its facts silently, never quote or reformat
# it; current actions change anything in it and newer witnessed events override it; append no agent, tracker, debug
# or report block, while ARIA's own 🎲 and 💚 ledgers still close the reply.
# The ledger clause names only the ledgers whose world_engine options are ticked (ARIA's full text says "when switched
# on"): with Fate and Bonds unticked, as Chibi ships, the model is never told a 🎲 or 💚 ledger ends the reply.
AGENTS_LEDGERS = (
    '{{#if world_engine contains "FATE" && world_engine contains "BONDS"}}; the 🎲 and 💚 ledgers still end the reply'
    '{{else if world_engine contains "FATE"}}; the 🎲 ledger still ends the reply'
    '{{else if world_engine contains "BONDS"}}; the 💚 ledger still ends the reply{{/if}}'
)
AGENTS_BLOCK = (
    '{{#if state_mode == "AGENTS"}}\n'
    '<agent_context_protocol>\n'
    "<context> is an earlier snapshot: apply its facts silently, never quote or reformat it; current actions change "
    "anything in it, newer witnessed events override it.\n"
    "Add no agent, tracker, debug or report block" + AGENTS_LEDGERS + ".\n"
    '</agent_context_protocol>\n'
    '{{/if}}'
)
AGENTS_NOTE = " <context> is old state; new events override."


# ----------------------------------------------------------------------------------------------------------------
# comments: Chibi CC comment -> Marinara comment

def generic(c):
    c = re.sub(r'(?:🏷️ )?Logic Core Tags', 'Think Tags', c)
    c = c.replace(' the tag SillyTavern folds away', ' the tag')
    return c


def adapt_comments(cc, chibi):
    """{section key: comment}. Rule-based from the CC comments; hand-written where Marinara differs."""
    C = {}
    for key in ('nsfw', 'pov', 'scene', 'npc', 'anthro', 'codex', 'scent', 'claude', 'gemini', 'glm', 'kimi',
                'mimopro', 'mimoflash', 'story'):
        C[key] = generic(cc.comment(mc.MODULE_IDS[key]))
    c = generic(cc.comment('4537b57d'))
    C['freaky'] = sub1(c, 'It needs 🔞 Adult Context ON, since it carries no explicit rules of its own.',
                       'Picking it also applies Adult Context, since it carries no explicit rules of its own.',
                       'freaky comment')
    c = generic(cc.comment('5dcccd11'))
    C['time'] = sub1(c, 'Ships OFF in Chibi.', 'Off by default in Chibi.', 'time comment') if chibi else c
    c = generic(cc.comment('acc2177a'))
    c = sub_re1(c, r', which the preset\'s regex scripts dress up as (?:an|the) orange Fate & Routine panel', '',
                'fate regex')
    C['fate'] = sub1(c, 'Ships OFF in Chibi;', 'Off by default in Chibi;', 'fate comment') if chibi else c
    c = generic(cc.comment('5506d699'))
    if chibi:
        c = sub_re1(c, r', and the preset\'s regex scripts draw each pair as a card with Bond, Sparks and Grudge bars',
                    '', 'bonds regex')
        c = sub1(c, 'Ships OFF.', 'Off by default.', 'bonds comment')
    else:
        c = sub_re1(c, r' The preset\'s regex scripts draw each pair as a little card with Bond, Sparks and Grudge bars\.',
                    '', 'bonds regex')
    C['bonds'] = c
    c = generic(cc.comment('e04b9c2b'))
    C['deepseek'] = sub1(c, ' and on an Impersonate turn', '', 'deepseek comment')
    c = generic(cc.comment('333dbbed'))
    if chibi:
        # Marinara prints the 3.8 text from this section itself; only CC routes it through the All-In-One patch
        C['gemini38'] = sub1(c, 'It prints through the 🩹 Gemini All-In-One patch, so switch that ON ALONGSIDE it.',
                             'Picking this option applies the 🩹 Gemini All-In-One patch as well.', 'gemini38 comment')
    else:
        C['gemini38'] = sub1(c, 'This has to be turned on ALONGSIDE the general Gemini patch.',
                             'Picking this option applies the general Gemini patch as well.', 'gemini38 comment')
    c = generic(cc.comment('15b770cf'))
    if chibi:
        c = sub_re1(c, r' The phrases the echo-cleaning regex scripts match \([^)]*\) stay word for word\.', '',
                    'lc regex sentence')
        c = sub1(c, ' Keep both Logic Cores above the gate in the list.',
                 ' With the Agents state backend its Scene line also notes that the engine <context> is old state. '
                 'Keep both Logic Cores above the gate in the list.', 'lc agents sentence')
    C['lc'] = c
    c = generic(cc.comment('jailbreak'))
    if chibi:
        c = sub1(c, 'Anything you put in player-posthistory inside 🍃 Custom Instructions lands here too, and so do '
                    'the extra lines a model patch, the 🔦 Flash Gate or 🧷 Character Hold adds.',
                 'Anything you write in Custom Post-History lands right after it; the extra lines a model patch, the '
                 'Flash Gate or Character Hold adds land inside it.', 'gate comment')
    else:
        c = sub1(c, 'Anything you put in player-posthistory inside 🍃 Custom Instructions lands here too, and so do '
                    'the extra lines a model patch can add.',
                 'Anything you write in Custom Post-History lands right after it, and so do the extra lines a model '
                 'patch can add.', 'gate comment')
    C['gate'] = c
    c = cc.comment('main')
    tail = "Its first line quietly resets ARIA's internal switches every turn, so a module you turn off stays off."
    C['main'] = sub1(c, tail, "When the State backend is set to Agents, it also carries the short protocol that tells "
                              "the model how to read the engine's agent reports.", 'main comment')
    return C


def hand_comments(cc, chibi):
    """Comments that are Marinara's own text."""
    H = {}
    if chibi:
        H['lc_twin'] = ("🧠 Chibi Logic Core, system-role twin: the same plan in the same size (about 220 tokens), sent "
                        "as a system message so the model reads the plan rule as an instruction it was given. Try this "
                        "one when your model keeps skipping the plan (MiMo V2.6 Pro has been doing that on some "
                        "providers). Pick either this or the assistant version in the Logic Core setting, never both. "
                        "Claude turns late system messages into user text, so Claude users keep the assistant "
                        "version.")
        H['reduce'] = ("Reduce Reasoning: a nudge against overthinking for models that think far too long (Kimi K2.6, "
                       "Qwen 3.6), sent as a user message for better adherence. It does not work every time. Chibi cut "
                       "it to one line of about 17 tokens. Pick it if your model still overthinks.")
        H['imp'] = ("Impersonation turn: asks the AI to write your next message in your own voice, in first person "
                    "unless your earlier messages use another person or tense, with no header, no character lines "
                    "and no 🎲 or 💚 block. SillyTavern fired this only when you pressed Impersonate; Marinara has no "
                    "such trigger, so this section stays OFF. Switch it on for the one turn where you want the AI to "
                    "write for you, then switch it off again. Chibi trimmed the wording and dropped the wrapper tags; "
                    "it costs about 80 tokens, on that turn only.")
    return H


# ----------------------------------------------------------------------------------------------------------------

def nanoid(n=21):
    alpha = string.ascii_letters + string.digits + '_-'
    return ''.join(secrets.choice(alpha) for _ in range(n))


def dump(d):
    return json.dumps(d, ensure_ascii=False, indent='\t')


def build(chibi_cc_path, base_mar_path, preset_id):
    cc = mc.CC(load(chibi_cc_path))
    base_raw = Path(base_mar_path).read_text(encoding='utf-8')
    doc = json.loads(base_raw)
    assert dump(doc) == base_raw, 'ARIA Marinara does not round-trip'
    S = doc['data']['sections']

    # ARIA's Marinara keeps its own comments for Custom Instructions and Story Context is rule-based above
    comments = adapt_comments(cc, True)
    comments.update(hand_comments(cc, True))
    comments['custom'] = comment_of(S[1]['content'])
    for k in mc.SECTION_KEYS.values():
        assert comments.get(k) is not None, k
    out, V = mc.build_all(cc, comments, AGENTS_BLOCK, AGENTS_NOTE)
    for idx, key in mc.SECTION_KEYS.items():
        assert S[idx]['name'] == mc.SECTION_NAMES[key], (idx, S[idx]['name'])
        S[idx]['content'] = out[key]

    # preset metadata
    p = doc['data']['preset']
    old_id = p['id']
    p['id'] = preset_id
    p['name'] = "ARIA 1.0 Chibi Edition (Marinara) — Aria's Realistic Intelligence Assistance — Agent Gating"
    p['description'] = DESCRIPTION
    p['createdAt'] = STAMP
    p['updatedAt'] = STAMP
    doc['exportedAt'] = STAMP
    dc = json.loads(p['defaultChoices'])
    dc['world_engine'] = [x for x in dc['world_engine'] if x not in ('FATE', 'TIME')]
    p['defaultChoices'] = json.dumps(dc, ensure_ascii=False, separators=(',', ':'))
    n = 0
    for key in ('sections', 'groups', 'choiceBlocks'):
        for item in doc['data'][key]:
            if 'presetId' in item:
                assert item['presetId'] == old_id
                item['presetId'] = preset_id
                n += 1

    # choice block questions
    for cb in doc['data']['choiceBlocks']:
        if cb['variableName'] == 'world_engine':
            cb['question'] = ("World engine. Time & Place status line (optional), Fate & Chekhov Ledger and Bonds Lite "
                              "relationship tracker. Fate and Bonds keep their memory in a collapsed ledger at the end "
                              "of each reply. Chibi leaves Fate and Time unticked.")
        if cb['variableName'] == 'state_mode':
            assert cb['question'].endswith('instead.')
            cb['question'] += (' In Chibi the Agents protocol costs about 90 tokens, which can take the fully '
                               'kitted-out prompt past 3,000.')
    return doc, out, V, n


DESCRIPTION = (
    "Chibi Edition of ARIA 1.0 for Marinara Engine, by TheAestheticFur: every ARIA module and toggle compressed "
    "Douyin-style, about 1,500 tokens as shipped and at most 3,000 fully kitted out, with the Agents state backend as "
    "the one exception (its protocol adds about 90). Fate & Chekhov Ledger and Time & Place ship unticked. Native "
    "Marinara conversion of the Chibi Chat Completions preset, built on the Freaky Frankenstein Marinara layout. "
    "Regex scripts dropped. Toggleable prompts became choice blocks. Adds Freaky Frankenstein's agent gates (State "
    "backend choice, agent context protocol, 🤖 Agent Reports data markers). Includes the 🔓 Jailbreak Logic Core "
    "option (off by default; needs Adult Context): two extra plan lines for frank adult fiction between adults. "
    "Recommended samplers (set in your connection, not stored in presets): Temperature 0.7, Top P 0.8 (MiMo V2.6 "
    "Flash: Temperature 0.8).\n\nConversion by u/BSPiotr with help from Claude"
)


def main():
    check = '--check' in sys.argv
    dst = CHIBI_MAR
    pid = nanoid()
    if dst.exists():
        pid = json.loads(dst.read_text(encoding='utf-8'))['data']['preset']['id']   # keep the id across re-syncs
    doc, out, V, n = build(CHIBI_CC, ARIA_MAR, pid)
    text = dump(doc)
    assert json.loads(text) == doc and dump(json.loads(text)) == text
    if check:
        print('identical to disk:', dst.exists() and dst.read_text(encoding='utf-8') == text)
        return
    dst.write_text(text, encoding='utf-8')
    back = dst.read_text(encoding='utf-8')
    assert dump(json.loads(back)) == back and not back.endswith('\n')
    print('wrote', dst.name, len(back), 'bytes; preset id', pid, '; presetId updated on', n, 'children')


if __name__ == '__main__':
    main()
