#!/usr/bin/env python3
"""Discard the 🔓 Jailbreak, rewrite The Logic Core around Realistic Frankenstein's Micro CoT in pico style, and add the
Gemini 4 Argon <thought> copy of 🏷️ Logic Core Tags, in all six presets and both regex sets.

usage: python3 build.py SRC_DIR OUT_DIR
SRC_DIR and OUT_DIR each hold the six preset files and regex/ARIA 1.0 Regex Scripts (Text Completions).json.
CC and TC are edited by raw-text replacement of JSON-escaped field values (every replacement asserts its count);
Marinara is loaded, edited and re-dumped, since it round-trips exactly.
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

JB_ID = '05f6e90d-b30b-48d5-b2bf-26a6e45faffa'
TAGS_ID = '303f26f5-bc2f-5dde-a9e9-aaaacd3eff4b'
G4_ID = '7c9e2b41-5d8a-4f3e-b6c1-0a2d4e8f9b37'
G4_NAME = '🏷️ Logic Core Tags: Gemini 4 Argon (native reasoning ON)'
G4_OPT_ID = 'opt_g4ArgonThTag'
STAMP = '2026-10-16T20:30:00.000Z'


def esc(s):
    return json.dumps(s, ensure_ascii=False)[1:-1]


def sub(text, old, new, count=1, label=''):
    n = text.count(old)
    if n != count:
        raise SystemExit(f'{label}: expected {count} of {old[:90]!r}, found {n}')
    return text.replace(old, new)


# ------------------------------------------------------------------ the new text, full edition and Chibi

FULL = dict(
    hdr=('Reasoning writes {{getvar::logicCoreLines}} dashed lines, then go; the reply follows.',
         'Reasoning opens on the OOC line and writes {{getvar::logicCoreLines}} dashed lines, then go; the reply follows.'),
    lines=('Lines are fragments that paraphrase what anyone said, never reply sentences or drafts, each building on the last '
           'and settled once written, all shorter than one reply paragraph',
           'I am the game master running this immersive simulation, not a helpful AI assistant: creative risk is welcome and '
           'perfection is unnecessary.\nI write every line, in order and none skipped, as telegraphic fragments that paraphrase '
           'what anyone said, never reply sentences or drafts, each building on the last and settled once written, all shorter '
           'than one reply paragraph'),
    move=("- Move: one beat; each character's next act, helping or holding still included; the result; the moment it stops on.",
          "- Move: one beat; {{user}} and every NPC succeed or fail alike, by skill and circumstance; each character's next act "
          "taken in full toward what they want, a fight, a lie, a seduction or a refusal, helping or holding still included, "
          "while nervous cards keep their nerves; the result; the moment it stops on."),
    end=('Reasoning ends at go. The reply:', 'Reasoning ends at go, with no further reasoning. The reply:'),
    tc_close=('with no Fate, Bonds, Ledger, Layers, Role or Frank line.', 'with no Fate, Bonds, Ledger or Layers line.'),
    adult=('- Mode: realism; persona-true; each plea new.',
           '- Mode: realism; persona-true; each plea new; a sexual, violent, cruel or dark beat gets its act, anatomy, '
           'sensations and tone planned in full.'),
    freaky=('- Mode: freaky; escalate.',
            "- Mode: freaky; escalate; characters described lewdly, each detail new to the last four replies; the beat's act, "
            'anatomy, sensations and tone planned in full.'),
)
CHIBI = dict(
    hdr=('Reasoning: {{getvar::logicCoreLines}} lines; go ends it.', 'Reasoning: {{getvar::logicCoreLines}} lines; go ends it.'),
    lines=('Fragments paraphrase speech, no reply drafts, settled and built on, all under a reply paragraph',
           "I'm the GM, not a helpful AI assistant: every line, none skipped; fragments paraphrase speech, no drafts; "
           'settled, built on; under a reply paragraph; creative risk over perfection'),
    move=("- Move: one beat; each NPC's next act, help/hold too; result; stop point.",
          '- Move: one beat; {{user}}/NPCs succeed or fail alike; each NPC acts fully (fight, lie, seduce, refuse; help/hold '
          'too), nervous cards aside; result; stop point.'),
    end=('{{else}}Reply:{{/if}}', '{{else}}Reply:{{/if}}'),
    tc_close=('skip any Fate, Bonds, Ledger, Layers, Role, Frank, Own words or POV line.',
              'skip any Fate, Bonds, Ledger, Layers, Own words or POV line.'),
    adult=('- Mode: realism, persona-true.',
           '- Mode: realism, persona-true; a sexual/violent/cruel/dark beat: act, anatomy, sensation, tone in full.'),
    freaky=('- Mode: freaky; escalate.', '- Mode: freaky, escalating lewdly; act, anatomy, sensation, tone in full.'),
)

FULL_CORE_COMMENT = (
    "{{// ARIA's planning step, named after the Logic Core inside every Intelligent Construct, rewritten from Realistic "
    "Frankenstein's Micro chain of thought. The AI plans in the first person as the game master of the simulation instead of "
    "a helpful assistant, takes creative risks, writes every line in order without skipping one, keeps you and every "
    "character on the same footing so anyone's act can succeed or fail, and carries each character's act all the way "
    "through, while nervous cards keep their nerves. With 🔞 Adult Context on, its Mode line plans how a sexual, violent, "
    "cruel or dark beat plays out. The lines stay pico-style fragments: what you asked out of character, where everyone is, "
    "what each character knows, how your last move lands on them given their usual mood, the one beat that happens next, "
    "which fresh details the reply brings in, and a last check for lists of three and punchline jokes. It works with the "
    "model's own reasoning (🏷️ Logic Core Tags off, where it ends the thinking at go with no further reasoning) and without "
    "it (Tags on, or the Gemini 4 Argon entry, where every reply opens with the plan inside the tags). It arrives as the AI's "
    "own message after the chat, which helps many models settle into the scene; in tags mode it starts on the opening tag, "
    "so a model that copies its own last message starts its reply on the tag SillyTavern folds away. Leave this ON. If your "
    "model still overthinks, switch Reduce Reasoning on alongside it. With a tags entry on, it also hands the gate a "
    "one-line reminder of the plan rule, which becomes the last line the model reads; keep both Logic Cores above the gate "
    "in the list.}}{{trim}}"
)
CHIBI_CORE_COMMENT = (
    "{{// 🧠 Chibi Logic Core: ARIA's planning step, rewritten from Realistic Frankenstein's Micro chain of thought in Chibi "
    "size. The AI plans in the first person as the game master instead of a helpful assistant, takes creative risks, writes "
    "every line in order, keeps you and every NPC on the same footing, and carries each NPC's act through, nervous cards "
    "aside; with 🔞 Adult Context on, its Mode line plans a sexual, violent, cruel or dark beat in full. Lines that other "
    "modules add (Mode, Fate, Bonds, Ledger, Layers, patch lines, Tally, Joins) join the plan and its line count; the wiring "
    "is the full edition's. With Logic Core Tags off the AI plans inside its own reasoning and stops at go. With them on, or "
    "with the Gemini 4 Argon entry, every reply opens with the plan inside the tags (The Logic Core itself starts on that "
    "tag, so a model that copies its own last message starts its reply on the tag SillyTavern folds away) and the gate gets "
    "a one-line reminder, which becomes the last line the model reads. The phrases the echo-cleaning regex scripts match "
    "(opens the reply, then / closes on the line after go / The reply starts on the line after that / Nothing above go "
    "enters the reply / Every response starts with) stay word for word. Leave this ON; if your model still overthinks, switch "
    "Reduce Reasoning on alongside it. Keep both Logic Cores above the gate in the list.}}{{trim}}"
)
FULL_G4_COMMENT = (
    "{{// For Gemini 4 Argon. Its reasoning can't be switched off, and it thinks inside <thought></thought> tags, where "
    "Gemini 3.8 Flash used <think></think>. Leave native reasoning ON and switch this on in place of 🏷️ Logic Core Tags: The "
    "Logic Core then opens the plan on <thought>, so the plan lands in Gemini's own thought block, ends it on go, closes the "
    "tag and only then writes the story. In Advanced Formatting, set the Reasoning Prefix to <thought> and the Suffix to "
    "</thought> and tick Auto-Parse; if you skip that, the preset's regex scripts fold a <thought> plan into a 💭 Thoughts box "
    "anyway. Use one tags entry at most; with both on, this one wins. This entry costs zero tokens by itself.}}{{trim}}"
)
CHIBI_G4_COMMENT = (
    "{{// Chibi Logic Core Tags for Gemini 4 Argon (zero tokens by itself). Gemini 4 Argon can't switch its reasoning off "
    "and thinks inside <thought></thought>, where Gemini 3.8 Flash used <think></think>. Leave native reasoning ON and switch "
    "this on instead of 🏷️ Logic Core Tags: the plan then opens on <thought> inside Gemini's own thought block and ends on go. "
    "Set the Reasoning Prefix to <thought>, the Suffix to </thought> and tick Auto-Parse; the regex scripts fold a <thought> "
    "plan anyway. Use one tags entry at most; with both on, this one wins.}}{{trim}}"
)
G4_BODY = '\n{{setvar::ariaThinkOpen::<thought>}}{{setvar::ariaThinkClose::</thought>}}{{trim}}'
TAGS_NOTE = ('Claude keeps its own thinking on whatever you set, so Claude users leave this OFF.',
             'Claude keeps its own thinking on whatever you set, so Claude users leave this OFF. Gemini 4 Argon, which thinks '
             'in <thought> tags and never switches its reasoning off, takes the 🏷️ Logic Core Tags: Gemini 4 Argon entry '
             'instead.')
ADULT_NOTE = (
    "It also tells The Logic Core which mode it's in.",
    "It also hands The Logic Core its Mode line, where the plan works out the act, anatomy, sensations and tone of a sexual, "
    "violent, cruel or dark beat.")
CHIBI_ADULT_NOTE = (
    "and its Mode line leaves the fresh-plea rule to this text. Only switch it on if you're an adult and want that kind of "
    "story. It also tells The Logic Core which mode it's in.",
    "and its Mode line leaves the fresh-plea rule to this text. Only switch it on if you're an adult and want that kind of "
    "story. It also hands The Logic Core its Mode line, where the plan works out the act, anatomy, sensation and tone of a "
    "sexual, violent, cruel or dark beat.")
FREAKY_NOTE = ('since it carries no explicit rules of its own.',
               'since it carries no explicit rules of its own. Its Mode line has the plan describe characters lewdly, with '
               'details new to the last four replies.')


def core(t, T, tc=False, mar=False, comment=None):
    """Rewrite one Logic Core (CC prompt, TC post_history block or Marinara section)."""
    if mar:
        t = sub(t, '{{#if logic_options contains "JAILBREAK" && adult_mode != "NONE"}}{{addvar::logicCoreLines::2}}{{/if}}',
                '', 1, 'mar jb counter')
        t, n = re.subn(r'\{\{#if logic_options contains "JAILBREAK" && adult_mode != "NONE"\}\}- Role:[^\n]*\n- Frank:[^\n]*\n'
                       r'\{\{/if\}\}', '', t)
        assert n == 1, 'mar jb lines'
    else:
        t = sub(t, '{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}', '', 1, 'jb counter')
        t = sub(t, '{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}', '', 1, 'jb print')
    for key in ('hdr', 'lines', 'move', 'end'):
        t = sub(t, *T[key], 1, key)
    if tc:
        t = sub(t, *T['tc_close'], 1, 'tc close')
    if mar:
        t = sub(t, *T['adult'], 1, 'mar adult')
        t = sub(t, *T['freaky'], 1, 'mar freaky')
    if comment:
        start = t.index('{{//')
        t = t[:start] + comment + t[t.index('{{trim}}', start) + len('{{trim}}'):]
    return t


# ------------------------------------------------------------------ Chat Completions

def cc_file(name, T, chibi):
    raw = (SRC / name).read_text(encoding='utf-8')
    doc = json.loads(raw)
    by = {p['identifier']: p for p in doc['prompts']}

    def edit(ident, fn):
        nonlocal raw
        old = by[ident]['content']
        new = fn(old)
        raw = sub(raw, esc(old), esc(new), 1, f'{name[-35:]} {ident[:8]}')

    edit('main', lambda t: sub(t, '{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}', '', 1, 'main blanks'))
    edit('379e3c22-9a25-5e6d-bf4a-037d49aa60d9', lambda t: sub(t, '{{setvar::ariaJb::}}', '', 1, 'impersonate blank'))
    lc = '15b770cf-6049-5f3b-b25d-be09728a65d5'
    edit(lc, lambda t: core(t, T, comment=CHIBI_CORE_COMMENT if chibi else FULL_CORE_COMMENT))
    edit('591b8c15-9858-5a96-a77b-6f58b5ba29e9' if '591b8c15-9858-5a96-a77b-6f58b5ba29e9' in by else
         [i for i in by if i.startswith('591b8c15')][0],
         lambda t: core(t, T) if not chibi else sub(core(t, T), 'the same plan in the same size (about 220 tokens)',
                                                     'the same plan in the same size', 1, 'chibi twin size'))
    edit('nsfw', lambda t: sub(sub(t, *T['adult'], 1, 'adult mode'), *(CHIBI_ADULT_NOTE if chibi else ADULT_NOTE), 1, 'adult note'))
    edit('4537b57d-e00a-4f7d-ae4e-7b5f04f4c9fb' if '4537b57d-e00a-4f7d-ae4e-7b5f04f4c9fb' in by else
         [i for i in by if i.startswith('4537b57d')][0],
         lambda t: sub(sub(t, *T['freaky'], 1, 'freaky mode'), *FREAKY_NOTE, 1, 'freaky note'))
    edit(TAGS_ID, lambda t: sub(t, *TAGS_NOTE, 1, 'tags note'))
    if chibi:
        edit('59602978-fdc0-4a8a-af0a-26b2ec58793b', lambda t: sub(
            t, '- The 🔓 Jailbreak toggle came along too. It ships OFF and needs 🔞 Adult Context and a Logic Core.\n',
            '- My 🧠 Logic Core is rewritten from Realistic Frankenstein\'s Micro chain of thought, and Gemini 4 Argon gets its '
            'own 🏷️ Logic Core Tags entry, since it thinks in <thought> tags and never switches its reasoning off.\n',
            1, 'chibi readme'))

    # regex scripts: <thought> joins every tag alternation, and Role|Frank leave the plan-strip labels
    raw = fix_regex_scripts(raw, doc['extensions']['regex_scripts'], name)

    # drop the JB prompt object and its order row
    start = raw.index(f'        {{\n            "identifier": "{JB_ID}"')
    end = raw.index('\n        }', start) + len('\n        }')
    assert raw[end:end + 2] == ',\n', 'JB object is not followed by a comma'
    raw = raw[:start] + raw[end + 2:]
    row = f'                {{\n                    "identifier": "{JB_ID}",\n                    "enabled": false\n                }},\n'
    raw = sub(raw, row, '', 1, 'JB order row')

    # the Gemini 4 Argon copy of Logic Core Tags, right after the original in prompts[] and prompt_order
    start = raw.index(f'        {{\n            "identifier": "{TAGS_ID}"')
    end = raw.index('\n        }', start) + len('\n        }')
    assert raw[end:end + 2] == ',\n'
    tags_obj = raw[start:end]
    tags_content = json.loads(raw)['prompts'][[p['identifier'] for p in json.loads(raw)['prompts']].index(TAGS_ID)]['content']
    g4 = tags_obj.replace(TAGS_ID, G4_ID)
    g4 = sub(g4, esc('🏷️ Logic Core Tags (native reasoning OFF)'), esc(G4_NAME), 1, 'g4 name')
    g4 = sub(g4, esc(tags_content), esc((CHIBI_G4_COMMENT if chibi else FULL_G4_COMMENT) + G4_BODY), 1, 'g4 content')
    raw = raw[:end + 2] + g4 + ',\n' + raw[end + 2:]
    row = f'                {{\n                    "identifier": "{TAGS_ID}",\n                    "enabled": false\n                }},\n'
    raw = sub(raw, row, row + row.replace(TAGS_ID, G4_ID), 1, 'tags order row')
    json.loads(raw)
    (OUT / name).write_text(raw, encoding='utf-8')


def fix_regex(f):
    f = f.replace('(?:thinking|think|logic_core|go)', '(?:thinking|think|thought|logic_core|go)')
    f = f.replace('(?:thinking|think|logic_core)', '(?:thinking|think|thought|logic_core)')
    f = f.replace('(?:thinking|think|details)', '(?:thinking|think|thought|details)')
    f = f.replace('(?:thinking|think)', '(?:thinking|think|thought)')
    f = f.replace('|Role|Frank)', ')')
    return f


def fix_regex_scripts(raw, scripts, label):
    """Apply fix_regex to every distinct findRegex once, asserting it occurs as often as scripts carry it."""
    from collections import Counter
    counts = Counter(s['findRegex'] for s in scripts)
    for old, n in counts.items():
        new = fix_regex(old)
        if new != old:
            raw = sub(raw, esc(old), esc(new), n, f'{label[-30:]} regex')
    return raw


# ------------------------------------------------------------------ Text Completions

def tc_file(name, T, chibi):
    raw = (SRC / name).read_text(encoding='utf-8')
    sp = json.loads(raw)['sysprompt']
    c, ph = sp['content'], sp['post_history']
    c2 = c
    sw = re.search(r'\{\{// 🔓[^}]*\}\}\{\{\.aria-jailbreak = off\}\}\n', c2)
    assert sw, 'TC JB switch'
    c2 = c2[:sw.start()] + c2[sw.end():]
    c2 = sub(c2, '{{setvar::ariaJb::}}{{setvar::ariaJbLines::}}', '', 1, 'tc blanks')
    blk = re.search(r'\{\{#if \.aria-jailbreak\}\}\{\{#if \.ariaModeLine\}\}\{\{setvar::ariaJbLines::2\}\}\{\{setvar::ariaJb::'
                    r'- Role:[^\n]*\n- Frank:[^\n]*\}\}\{\{/if\}\}\{\{/if\}\}', c2)
    assert blk, 'TC JB block'
    c2 = c2[:blk.start()] + c2[blk.end():]
    c2 = sub(c2, '{{setvar::ariaModeLine::' + T['adult'][0] + '}}', '{{setvar::ariaModeLine::' + T['adult'][1] + '}}', 1, 'tc adult')
    c2 = sub(c2, '{{setvar::ariaModeLine::' + T['freaky'][0] + '}}', '{{setvar::ariaModeLine::' + T['freaky'][1] + '}}', 1,
             'tc freaky')
    assert 'Jailbreak' not in c2 and 'ariaJb' not in c2 and 'jailbreak' not in c2, 'TC content still names the JB'
    ph2 = core(ph, T, tc=True)
    raw = sub(raw, esc(c), esc(c2), 1, 'tc content')
    raw = sub(raw, esc(ph), esc(ph2), 1, 'tc post_history')
    json.loads(raw)
    (OUT / name).write_text(raw, encoding='utf-8')


def regex_file():
    raw = (SRC / RGX).read_text(encoding='utf-8')
    raw = fix_regex_scripts(raw, json.loads(raw), RGX)
    json.loads(raw)
    (OUT / RGX).parent.mkdir(parents=True, exist_ok=True)
    (OUT / RGX).write_text(raw, encoding='utf-8')


# ------------------------------------------------------------------ Marinara

TAGS = 'logic_options contains "THINKTAGS" || logic_options contains "THOUGHTTAGS"'
SETTAG = ('{{#if logic_options contains "THOUGHTTAGS"}}{{setvar::thinkTag::thought}}'
          '{{else if logic_options contains "THINKTAGS"}}{{setvar::thinkTag::thinking}}{{/if}}')
OLDIF = '{{#if logic_options contains "THINKTAGS"}}'
NEWIF = '{{#if ' + TAGS + '}}'


def mar_tags(t, label):
    t = sub(t, '{{setvar::logicCoreLines::7}}', SETTAG + '{{setvar::logicCoreLines::7}}', 1, label + ' settag')
    t = sub(t, OLDIF + '<thinking> opens the reply', NEWIF + '<{{getvar::thinkTag}}> opens the reply', 1, label + ' open')
    t = sub(t, OLDIF + '</thinking> closes on the line after go.', NEWIF + '</{{getvar::thinkTag}}> closes on the line after go.',
            1, label + ' close')
    t = sub(t, OLDIF + '\nEvery response starts with <thinking>.', NEWIF + '\nEvery response starts with <{{getvar::thinkTag}}>.',
            1, label + ' every')
    t = sub(t, OLDIF + '; go ends the thinking{{/if}}', NEWIF + '; go ends the thinking{{/if}}', 1, label + ' go ends')
    assert OLDIF not in t and '<thinking>' not in t.split('{{trim}}', 1)[1], label + ' leftover thinking tag'
    return t


def mar_file(name, T, chibi):
    raw = (SRC / name).read_text(encoding='utf-8')
    d = json.loads(raw)
    assert json.dumps(d, ensure_ascii=False, indent='\t') == raw
    secs = {s['name']: s for s in d['data']['sections']}
    for nm in ('🧠 The Logic Core', '🧠 The Logic Core (system-role twin)'):
        s = secs[nm]
        comment = None
        if nm == '🧠 The Logic Core':
            src = CHIBI_CORE_COMMENT if chibi else FULL_CORE_COMMENT
            comment = (src.replace('🏷️ Logic Core Tags', 'Think Tags').replace('the Gemini 4 Argon entry', 'the Gemini 4 Argon '
                       'Thought Tags option').replace('with the Gemini 4 Argon entry', 'with Thought Tags')
                       .replace('}}{{trim}}', ' }}{{trim}}'))
        t = core(s['content'], T, mar=True, comment=comment)
        if chibi and nm != '🧠 The Logic Core':
            t = sub(t, 'the same plan in the same size (about 220 tokens)', 'the same plan in the same size', 1, 'mar chibi twin')
        s['content'] = mar_tags(t, nm)
    g = secs['🚪 Last-Mile Gate']
    t = sub(g['content'], '{{#if logic_options contains "JAILBREAK" && adult_mode != "NONE"}}{{addvar::logicCoreLines::2}}{{/if}}',
            '', 1, 'gate jb counter')
    t = sub(t, '{{setvar::logicCoreLines::7}}', SETTAG + '{{setvar::logicCoreLines::7}}', 1, 'gate settag')
    t = sub(t, '{{#if logic_core != "NONE" && logic_options contains "THINKTAGS"}}\nBegin with <thinking>, then '
               '{{getvar::logicCoreLines}} dashed lines, go and </thinking>; the reply follows.{{/if}}',
            '{{#if logic_core != "NONE" && (' + TAGS + ')}}\nBegin with <{{getvar::thinkTag}}>, then '
            '{{getvar::logicCoreLines}} dashed lines, go and </{{getvar::thinkTag}}>; the reply follows.{{/if}}',
            1, 'gate cue')
    g['content'] = t
    for nm, (old, new) in (('🔞 Adult Context', CHIBI_ADULT_NOTE if chibi else ADULT_NOTE), ('😈 Freaky Override', FREAKY_NOTE)):
        if old in secs[nm]['content']:
            secs[nm]['content'] = sub(secs[nm]['content'], old, new, 1, nm)
    lo = [c for c in d['data']['choiceBlocks'] if c['variableName'] == 'logic_options'][0]
    opts = json.loads(lo['options'])
    opts = [o for o in opts if o['value'] != 'JAILBREAK']
    i = [o['value'] for o in opts].index('THINKTAGS')
    opts.insert(i + 1, {'id': G4_OPT_ID, 'label': '🏷️ Thought Tags: Gemini 4 Argon (native reasoning ON)', 'value': 'THOUGHTTAGS'})
    lo['options'] = json.dumps(opts, ensure_ascii=False, separators=(',', ':'))
    lo['question'] = sub(lo['question'],
                         ' Jailbreak: two extra plan lines for frank adult fiction (sex stays between adults); they print only '
                         'while Adult Context is on.',
                         ' Thought Tags: the same with Gemini 4 Argon\'s <thought> tags, for its reasoning that can\'t be '
                         'switched off (keep it on); pick one tags option, and with both ticked Thought Tags wins.', 1, 'question')
    pr = d['data']['preset']
    pr['description'] = sub(pr['description'],
                            'Includes the 🔓 Jailbreak Logic Core option (off by default; needs Adult Context): two extra plan '
                            'lines for frank adult fiction between adults.',
                            "The Logic Core is rewritten from Realistic Frankenstein's Micro chain of thought, and its Thought "
                            'Tags option fits Gemini 4 Argon, whose reasoning uses <thought> tags and stays on.', 1, 'description')
    pr['updatedAt'] = STAMP
    if 'exportedAt' in d:
        d['exportedAt'] = STAMP
    out = json.dumps(d, ensure_ascii=False, indent='\t')
    for bad in ('JAILBREAK', 'Jailbreak', '🔓', '- Role:', '- Frank:'):
        assert bad not in out, f'{name}: still has {bad}'
    (OUT / name).write_text(out, encoding='utf-8')


cc_file(CC, FULL, chibi=False)
cc_file(CCC, CHIBI, chibi=True)
tc_file(TC, FULL, chibi=False)
tc_file(CTC, CHIBI, chibi=True)
regex_file()
mar_file(MAR, FULL, chibi=False)
mar_file(CMAR, CHIBI, chibi=True)
for n in (CC, CCC, TC, CTC):
    t = (OUT / n).read_text(encoding='utf-8')
    for bad in ('ariaJb', 'Jailbreak (needs', '🔓', 'aria-jailbreak', '- Role:', '- Frank:', '|Role|Frank'):
        assert bad not in t, f'{n}: still has {bad}'
print('built into', OUT)
