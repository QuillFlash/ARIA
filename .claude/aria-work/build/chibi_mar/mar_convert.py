"""CC -> Marinara conversion of ARIA model-facing text.

The converter takes a Chat Completions preset (ARIA's or Chibi's) and returns, per Marinara section, the section
content in Marinara conventions: choice conditions instead of aria* variables, every patch / Flash / Hold / JB line
inlined under its condition, `{{// text }}` comments, no regex-script or SillyTavern-only wording.

selftest() runs the converter on ARIA's own CC preset and must reproduce ARIA's Marinara file byte for byte (the
comments, the Agents block and the Agents note are passed in, since they are written by hand). So the same code path
produces the Chibi sections.
"""
import json
import re

# --------------------------------------------------------------------------------------------------------------------
# macro scanning

def macro_end(text, i):
    """text[i:i+2] == '{{'; return the index just after the matching '}}' (nested macros counted)."""
    depth = 0
    j = i
    n = len(text)
    while j < n:
        if text.startswith('{{', j):
            depth += 1
            j += 2
        elif text.startswith('}}', j):
            depth -= 1
            j += 2
            if depth == 0:
                return j
        else:
            j += 1
    raise ValueError('unbalanced macro at %d: %r' % (i, text[i:i + 60]))


def find_setvars(text):
    """Top-level setvars of a CC content: list of (name, value, start, end)."""
    out = []
    pos = 0
    while True:
        i = text.find('{{setvar::', pos)
        if i < 0:
            return out
        end = macro_end(text, i)
        inner = text[i + len('{{setvar::'):end - 2]
        name, _, value = inner.partition('::')
        out.append((name, value, i, end))
        pos = end


def strip_setvars(text):
    out, last = [], 0
    for _name, _value, s, e in find_setvars(text):
        out.append(text[last:s])
        last = e
    out.append(text[last:])
    return ''.join(out)


def setvar_values(text, name):
    return [v for n, v, _s, _e in find_setvars(text) if n == name]


def one(values, what):
    assert len(values) == 1, '%s: expected 1 value, got %d' % (what, len(values))
    return values[0]


def split_comment(text):
    """('comment', rest) for a leading {{// ... }} + optional {{trim}} + optional newline; (None, text) otherwise."""
    if not text.startswith('{{//'):
        return None, text
    end = macro_end(text, 0)
    comment = text[len('{{// '):end - 2] if text.startswith('{{// ') else text[len('{{//'):end - 2]
    rest = text[end:]
    if rest.startswith('{{trim}}'):
        rest = rest[len('{{trim}}'):]
    if rest.startswith('\n'):
        rest = rest[1:]
    return comment.rstrip(), rest


def sub1(text, old, new, what=None):
    assert text.count(old) == 1, '%s: %d occurrences of %r' % (what or 'sub1', text.count(old), old[:80])
    return text.replace(old, new)


def sub_re1(text, pattern, repl, what=None, flags=re.S):
    ms = list(re.finditer(pattern, text, flags))
    assert len(ms) == 1, '%s: %d matches of %r' % (what or 'sub_re1', len(ms), pattern[:80])
    m = ms[0]
    return text[:m.start()] + (repl(m) if callable(repl) else repl) + text[m.end():]


# --------------------------------------------------------------------------------------------------------------------
# CC preset access

class CC:
    def __init__(self, doc):
        self.doc = doc
        self.by_id = {p['identifier']: p for p in doc['prompts']}

    def p(self, prefix):
        hit = [p for i, p in self.by_id.items() if i.startswith(prefix)]
        assert len(hit) == 1, (prefix, [p['identifier'] for p in hit])
        return hit[0]

    def content(self, prefix):
        return self.p(prefix)['content']

    def comment(self, prefix):
        return split_comment(self.content(prefix))[0]

    def body(self, prefix):
        return split_comment(self.content(prefix))[1]


MODULE_IDS = dict(
    main='main', nsfw='nsfw', freaky='4537b57d', jb='05f6e90d', pov='b7b6ab7f', scene='15a8065d', npc='cca418a6',
    anthro='2a2e12d0', codex='9869a1e5', scent='dd3642f5', time='5dcccd11', fate='acc2177a', bonds='5506d699',
    claude='b59a2ad1', gemini='ac96376e', gemini38='333dbbed', glm='1f2e1f97', kimi='9bb6c2b0', mimopro='33f92483',
    mimoflash='3a027832', deepseek='e04b9c2b', flash='2e3e7f63', hold='dc8b1acb', story='f23feaf4', lc='15b770cf',
    lc_twin='591b8c15', gate='jailbreak', reduce='939286fd', imp='379e3c22', custom='0dc06d25',
)


def extract_values(cc):
    """Every variable text the Marinara sections inline, read from the CC preset's setvars."""
    V = {}
    b = cc.body
    V['mode_adult'] = one(setvar_values(b('nsfw'), 'ariaModeLine'), 'adult mode')
    V['mode_freaky'] = one(setvar_values(b('4537b57d'), 'ariaModeLine'), 'freaky mode')
    V['pov_gate'] = one(setvar_values(b('b7b6ab7f'), 'ariaPovGate'), 'pov gate')
    V['scent_gate'] = one(setvar_values(b('dd3642f5'), 'ariaScentGate'), 'scent gate')
    V['echo_gate'] = one(setvar_values(b('9869a1e5'), 'ariaEchoGate'), 'echo gate')
    V['chop_gate'] = one(setvar_values(b('9869a1e5'), 'ariaChopGate'), 'chop gate')
    V['speech_gate'] = one(setvar_values(b('ac96376e'), 'ariaChopGate'), 'gemini speech gate')
    fate = b('acc2177a')
    dice = one(setvar_values(fate, 'ariaDice'), 'dice')
    V['dice'] = dice.replace('{{roll::1d20}}', '{{roll:1d20}}')
    V['fate_line'] = one(setvar_values(fate, 'ariaFateLine'), 'fate line')
    V['ledger_fate'] = one(setvar_values(fate, 'ariaLedgerLine'), 'fate ledger line')
    V['ledger_gate_fate'] = one(setvar_values(fate, 'ariaLedgerGate'), 'fate ledger gate')
    bonds = b('5506d699')
    V['bonds_line'] = one(setvar_values(bonds, 'ariaBondsLine'), 'bonds line')
    led = setvar_values(bonds, 'ariaLedgerLine')
    gate = setvar_values(bonds, 'ariaLedgerGate')
    assert len(led) == 2 and len(gate) == 2
    V['ledger_bonds'], V['ledger_both'] = led
    V['ledger_gate_bonds'], V['ledger_gate_both'] = gate
    for key, pre in (('gemini', 'ac96376e'), ('glm', '1f2e1f97'), ('kimi', '9bb6c2b0'), ('mimopro', '33f92483'),
                     ('mimoflash', '3a027832'), ('deepseek', 'e04b9c2b')):
        V['patch_' + key] = one(setvar_values(b(pre), 'ariaPatchGate'), key + ' patch gate')
        V['count_' + key] = int(one(setvar_values(b(pre), 'ariaPatchLines'), key + ' patch lines'))
    V['joins'] = one(setvar_values(b('e04b9c2b'), 'ariaPatchJoins'), 'joins')
    tally = setvar_values(b('e04b9c2b'), 'ariaPatchTally')
    assert len(tally) == 3, len(tally)
    V['tally_bonds'] = tally[0]
    assert tally[1].startswith('{{getvar::ariaPatchTally}}')
    V['tally_fate_suffix'] = tally[1][len('{{getvar::ariaPatchTally}}'):]
    V['tally_fate'] = tally[2]
    flash = b('2e3e7f63')
    fg = setvar_values(flash, 'ariaFlashGate')
    assert len(fg) == 2 and fg[1].startswith('{{getvar::ariaFlashGate}}\n')
    V['flash_lines'] = fg[0]
    V['flash_runs'] = fg[1][len('{{getvar::ariaFlashGate}}\n'):]
    V['voice_extra'] = one(setvar_values(flash, 'ariaVoiceExtra'), 'voice extra')
    hold = b('dc8b1acb')
    V['hold_line'] = one(setvar_values(hold, 'ariaHoldLine'), 'hold line')
    V['hold_gate'] = one(setvar_values(hold, 'ariaHoldGate'), 'hold gate')
    jb = b('05f6e90d')
    V['jb_count'] = int(one(setvar_values(jb, 'ariaJbLines'), 'jb count'))
    V['jb_lines'] = one(setvar_values(jb, 'ariaJb'), 'jb lines')
    assert V['jb_lines'].count('\n') + 1 == V['jb_count']
    lc = b('15b770cf')
    cue = one(setvar_values(lc, 'ariaPlanCue'), 'plan cue')
    V['plan_cue'] = cue.replace('{{getvar::ariaThinkOpen}}', '<thinking>').replace('{{getvar::ariaThinkClose}}',
                                                                                   '</thinking>')
    V['gemini38'] = one(setvar_values(b('333dbbed'), 'gemini38Patch'), 'gemini 3.8 text')
    return V


# --------------------------------------------------------------------------------------------------------------------
# conditions

COND = {
    'adult': '{{#if adult_mode != "NONE"}}', 'freaky': '{{#if adult_mode == "FREAKY"}}',
    'pov': '{{#if pov_style == "HYBRID"}}',
    'scene': '{{#if core_modules contains "SCENE"}}', 'npc': '{{#if core_modules contains "NPCVOICE"}}',
    'anthro': '{{#if core_modules contains "ANTHRO"}}', 'codex': '{{#if core_modules contains "ANTISLOP"}}',
    'scent': '{{#if core_modules contains "SCENT"}}',
    'time': '{{#if world_engine contains "TIME"}}', 'fate': '{{#if world_engine contains "FATE"}}',
    'bonds': '{{#if world_engine contains "BONDS"}}',
    'claude': '{{#if model_patch == "CLAUDE"}}', 'gemini': '{{#if model_patch == "GEMINI"}}',
    'gemini38': '{{#if model_patch == "GEMINI38"}}', 'glm': '{{#if model_patch == "GLM"}}',
    'kimi': '{{#if model_patch == "KIMIQWEN"}}', 'mimopro': '{{#if model_patch == "MIMOPRO"}}',
    'mimoflash': '{{#if model_patch == "MIMOFLASH"}}', 'deepseek': '{{#if model_patch == "DEEPSEEK"}}',
    'lc': '{{#if logic_core == "ASSISTANT"}}', 'lc_twin': '{{#if logic_core == "SYSTEM"}}',
    'reduce': '{{#if logic_options contains "REDUCE"}}',
}

FATE = 'world_engine contains "FATE"'
BONDS = 'world_engine contains "BONDS"'


def wrap(cond, comment, body):
    """Marinara section content: condition + comment + body (no trailing newline inside the body)."""
    head = (cond or '') + ('{{// %s }}{{trim}}\n' % comment if comment is not None else '')
    return head + body + ('\n{{/if}}' if cond else '')


def tidy_body(text):
    """Module body with variables stripped: no {{trim}}, no leading or trailing blank lines."""
    text = strip_setvars(text).replace('{{trim}}', '')
    return text.strip('\n')


# --------------------------------------------------------------------------------------------------------------------
# patch chain, shared by both Logic Cores and the gate

def patch_chain(V):
    """The if / else-if chain that inlines every model patch's plan and gate lines (and DeepSeek's Joins)."""
    g = V['patch_gemini'] + '\n'
    return (COND['gemini'] + g + '{{else if model_patch == "GEMINI38"}}' + g
            + '{{else if model_patch == "GLM"}}' + V['patch_glm'] + '\n'
            + '{{else if model_patch == "KIMIQWEN"}}' + V['patch_kimi'] + '\n'
            + '{{else if model_patch == "MIMOPRO"}}' + V['patch_mimopro'] + '\n'
            + '{{else if model_patch == "MIMOFLASH"}}' + V['patch_mimoflash'] + '\n'
            + '{{else if model_patch == "DEEPSEEK"}}' + V['patch_deepseek'] + '\n'
            + '{{#if core_modules not contains "FLASH"}}' + V['joins'] + '\n{{/if}}{{/if}}')


def ledger_chain(both, fate, bonds):
    return ('{{#if %s && %s}}%s\n{{else if %s}}%s\n{{else if %s}}%s\n{{/if}}' % (FATE, BONDS, both, FATE, fate, BONDS,
                                                                              bonds))


def tally_and_ledger(V):
    return ('{{#if model_patch == "DEEPSEEK" && %s}}%s{{#if %s}}%s{{/if}}\n'
            '{{else if model_patch == "DEEPSEEK" && %s}}%s\n{{/if}}' % (BONDS, V['tally_bonds'], FATE,
                                                                       V['tally_fate_suffix'], FATE, V['tally_fate'])
            + ledger_chain(V['ledger_both'], V['ledger_fate'], V['ledger_bonds']))


def count_prefix(V):
    """The line counter that opens both Logic Cores and the gate, built from the CC preset's own counts."""
    c = V
    return ('{{setvar::logicCoreLines::7}}{{#if adult_mode != "NONE"}}{{addvar::logicCoreLines::1}}{{/if}}'
            '{{#if %s}}{{addvar::logicCoreLines::1}}{{/if}}{{#if %s}}{{addvar::logicCoreLines::1}}{{/if}}'
            '{{#if %s || %s}}{{addvar::logicCoreLines::1}}{{/if}}'
            '{{#if logic_options contains "JAILBREAK" && adult_mode != "NONE"}}{{addvar::logicCoreLines::%d}}{{/if}}'
            '{{#if core_modules contains "HOLD"}}{{addvar::logicCoreLines::1}}{{/if}}'
            '{{#if model_patch == "GEMINI" || model_patch == "GEMINI38"}}{{addvar::logicCoreLines::%d}}'
            '{{else if model_patch == "GLM"}}{{addvar::logicCoreLines::%d}}'
            '{{else if model_patch == "KIMIQWEN" || model_patch == "MIMOPRO"}}{{addvar::logicCoreLines::%d}}'
            '{{else if model_patch == "MIMOFLASH"}}{{addvar::logicCoreLines::%d}}'
            '{{else if model_patch == "DEEPSEEK"}}{{addvar::logicCoreLines::%d}}'
            '{{#if %s || %s}}{{addvar::logicCoreLines::1}}{{/if}}'
            '{{#if core_modules not contains "FLASH"}}{{addvar::logicCoreLines::1}}{{/if}}{{/if}}'
            % (FATE, BONDS, FATE, BONDS, c['jb_count'], c['count_gemini'], c['count_glm'], c['count_kimi'],
               c['count_mimoflash'], c['count_deepseek'], FATE, BONDS))


def check_counts(V):
    assert V['count_kimi'] == V['count_mimopro'] == 1
    for key in ('gemini', 'glm', 'kimi', 'mimopro', 'mimoflash', 'deepseek'):
        n = V['patch_' + key].count('\n') + 1
        want = V['count_' + key]
        assert n == want, (key, n, want)
    # DeepSeek's own lines are the patch lines; Joins and Tally are counted by the two conditional addvars
    return True


# --------------------------------------------------------------------------------------------------------------------
# Logic Core and gate

def lc_to_mar(cc_content, V, agents_note):
    """Marinara body (without wrapper or comment) of a Logic Core, from the CC Logic Core's content."""
    _comment, body = split_comment(cc_content)
    i = body.index('{{#if .ariaThinkOpen}}{{setvar::ariaPlanCue::')
    counter_cc, rest = body[:i], body[i:]
    assert counter_cc.startswith('{{setvar::logicCoreLines::7}}') and counter_cc.count('{{setvar') == 1
    counter = count_prefix(V) + '{{trim}}{{trim}}'
    # plan cue setvar leaves the line; the cue itself is the gate's last line
    name, value, s, e = find_setvars(rest)[0]
    assert name == 'ariaPlanCue'
    rest = rest[:s] + rest[e:]
    rest = rest.replace('{{#if .ariaThinkOpen}}', '{{#if logic_options contains "THINKTAGS"}}')
    rest = rest.replace('{{getvar::ariaThinkOpen}}', '<thinking>').replace('{{getvar::ariaThinkClose}}', '</thinking>')
    # Scene line: the Agents note
    rest = sub_re1(rest, r'^- Scene: [^\n]*', lambda m: m.group(0) + ('{{#if state_mode == "AGENTS"}}%s{{/if}}' %
                                                                       agents_note), 'scene line', flags=re.M)
    rest = sub1(rest, '{{#if .ariaModeLine}}{{getvar::ariaModeLine}}\n{{/if}}',
                '{{#if adult_mode == "ADULT"}}%s\n{{else if adult_mode == "FREAKY"}}%s\n{{/if}}' % (
                    V['mode_adult'], V['mode_freaky']), 'mode block')
    rest = sub1(rest, '{{getvar::ariaVoiceExtra}}', '{{#if core_modules contains "FLASH"}}%s{{/if}}' % V['voice_extra'],
                'voice extra')
    rest = sub1(rest, '{{#if .ariaHoldLine}}{{getvar::ariaHoldLine}}\n{{/if}}',
                '{{#if core_modules contains "HOLD"}}%s\n{{/if}}' % V['hold_line'], 'hold block')
    rest = sub1(rest, '{{#if .ariaPatchGate}}{{getvar::ariaPatchGate}}\n{{/if}}'
                      '{{#if .ariaPatchJoins}}{{getvar::ariaPatchJoins}}\n{{/if}}', patch_chain(V), 'patch chain')
    rest = sub1(rest, '{{#if .ariaFateLine}}{{getvar::ariaFateLine}}\n{{/if}}',
                '{{#if %s}}%s\n{{/if}}' % (FATE, V['fate_line']), 'fate line')
    rest = sub1(rest, '{{#if .ariaBondsLine}}{{getvar::ariaBondsLine}}\n{{/if}}',
                '{{#if %s}}%s\n{{/if}}' % (BONDS, V['bonds_line']), 'bonds line')
    rest = sub1(rest, '{{#if .ariaPatchTally}}{{#if .ariaLedgerLine}}{{getvar::ariaPatchTally}}\n{{/if}}{{/if}}'
                      '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}', tally_and_ledger(V),
                'tally and ledger')
    rest = sub1(rest, '{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}',
                '{{#if logic_options contains "JAILBREAK" && adult_mode != "NONE"}}%s\n{{/if}}' % V['jb_lines'],
                'jb block')
    rest = sub_re1(rest, r'\{\{#if \.ariaLedgerLine\}\}([^{}]*)\{\{/if\}\}',
                   lambda m: '{{#if %s}}%s{{else if %s}}%s{{/if}}' % (FATE, m.group(1), BONDS, m.group(1)),
                   'ledger last')
    leftovers = re.findall(r'\{\{[^}]*aria[^}]*\}\}', rest)
    assert not leftovers, leftovers
    return counter + '\n' + rest


def gate_to_mar(cc_content, V):
    _comment, body = split_comment(cc_content)
    assert body.startswith('<final_gate>\n')
    rest = body
    rest = sub1(rest, '{{#if .ariaChopGate}}{{getvar::ariaChopGate}}\n{{/if}}',
                '{{#if model_patch == "GEMINI"}}%s\n{{else if model_patch == "GEMINI38"}}%s\n'
                '{{else if core_modules contains "ANTISLOP"}}%s\n{{/if}}' % (V['speech_gate'], V['speech_gate'],
                                                                             V['chop_gate']), 'chop gate')
    rest = sub_re1(rest, r'\{\{#if !\.ariaFlashGate\}\}(.*?)\{\{/if\}\}',
                   lambda m: '{{#if core_modules contains "FLASH"}}{{else}}%s{{/if}}' % m.group(1), 'work line')
    rest = sub1(rest, '{{#if .ariaEchoGate}}{{getvar::ariaEchoGate}}\n{{/if}}',
                '{{#if core_modules contains "ANTISLOP"}}%s\n{{/if}}' % V['echo_gate'], 'echo gate')
    rest = sub1(rest, '{{#if .ariaScentGate}}{{getvar::ariaScentGate}}\n{{/if}}',
                '{{#if core_modules contains "SCENT"}}%s\n{{/if}}' % V['scent_gate'], 'scent gate')
    rest = sub1(rest, '{{#if .ariaPovGate}}{{getvar::ariaPovGate}}\n{{/if}}',
                '{{#if pov_style == "HYBRID"}}%s\n{{/if}}' % V['pov_gate'], 'pov gate')
    rest = sub1(rest, '{{#if .ariaLedgerGate}}{{getvar::ariaLedgerGate}}\n{{/if}}',
                ledger_chain(V['ledger_gate_both'], V['ledger_gate_fate'], V['ledger_gate_bonds']), 'ledger gate')
    flash = ('{{#if core_modules contains "FLASH"}}%s\n{{#if model_patch != "DEEPSEEK"}}%s\n{{/if}}{{/if}}'
             % (V['flash_lines'], V['flash_runs']))
    hold = '{{#if core_modules contains "HOLD"}}%s\n{{/if}}' % V['hold_gate']
    rest = sub1(rest, '{{#if .ariaPatchGate}}{{getvar::ariaPatchGate}}\n{{/if}}'
                      '{{#if .ariaPatchJoins}}{{getvar::ariaPatchJoins}}\n{{/if}}'
                      '{{#if .ariaFlashGate}}{{getvar::ariaFlashGate}}\n{{/if}}'
                      '{{#if .ariaHoldGate}}{{getvar::ariaHoldGate}}\n{{/if}}', patch_chain(V) + flash + hold,
                'patch, flash and hold gate')
    rest = sub1(rest, '{{#if .ariaDice}}{{getvar::ariaDice}}\n{{/if}}{{setvar::ariaDice::}}'
                      '{{#if .player-posthistory}}{{getvar::player-posthistory}}\n{{/if}}',
                '{{#if %s}}%s\n{{/if}}' % (FATE, V['dice']), 'dice and player post-history')
    rest = sub1(rest, '{{#if .ariaPlanCue}}\n{{getvar::ariaPlanCue}}{{/if}}',
                '{{#if logic_core != "NONE" && logic_options contains "THINKTAGS"}}\n%s{{/if}}' % V['plan_cue'],
                'plan cue')
    leftovers = re.findall(r'\{\{[^}]*(?:aria|player)[^}]*\}\}', rest)
    assert not leftovers, leftovers
    return count_prefix(V) + '{{trim}}\n' + rest


# --------------------------------------------------------------------------------------------------------------------
# modules

def module_body(cc, key, V):
    body = cc.body(MODULE_IDS[key])
    if key == 'bonds':
        # the ledger setvars sit in an if / else that is empty once the setvars are stripped
        body = sub1(strip_setvars(body), '{{#if !.ariaLedgerLine}}{{else}}{{/if}}', '', 'bonds ledger branch')
    return tidy_body(body)


def gemini_body(cc):
    """The Gemini All-In-One lines without its setvars and without the 3.8 hook (3.8 has its own section)."""
    body = cc.body('ac96376e')
    hook = '{{#if .gemini38Patch}}{{getvar::gemini38Patch}}{{/if}}'
    body = sub1(body, hook, '', 'gemini38 hook')
    return tidy_body(body)


def deepseek_body(cc):
    body = cc.body('e04b9c2b')
    i = body.index('Native reasoning:')
    prefix = body[:i]
    assert prefix.startswith('{{#if .ariaBondsLine}}{{setvar::ariaPatchTally::') and prefix.endswith('{{/if}}{{/if}}'), \
        prefix[-60:]
    body = body[i:]
    body = sub1(body, '{{#if .ariaPatchTally}}', '{{#if %s || %s}}' % (FATE, BONDS), 'tally condition')
    return tidy_body(body)


def story_body(cc):
    return split_comment(cc.content('f23feaf4'))[1].strip('\n')


# --------------------------------------------------------------------------------------------------------------------
# whole preset

SECTION_KEYS = {  # Marinara section index in ARIA's file -> key
    0: 'main', 1: 'custom', 2: 'nsfw', 3: 'freaky', 4: 'pov', 5: 'scene', 6: 'npc', 7: 'anthro', 8: 'codex',
    9: 'scent', 10: 'time', 11: 'fate', 12: 'bonds', 13: 'claude', 14: 'gemini', 15: 'glm', 16: 'mimopro',
    17: 'story', 33: 'lc', 34: 'lc_twin', 35: 'gate', 37: 'reduce', 38: 'imp', 39: 'gemini38', 40: 'kimi',
    41: 'mimoflash', 42: 'deepseek',
}
SECTION_NAMES = {
    'main': '⚡ ARIA Main Prompt', 'custom': '🍃 Custom Instructions', 'nsfw': '🔞 Adult Context',
    'freaky': '😈 Freaky Override', 'pov': '👀 Hybrid POV', 'scene': '🎬 Voice & Scene Engine',
    'npc': '🎭 NPC Voice & Emotions', 'anthro': '🐺 Anthro Vocals', 'codex': '🖋️ Anti-Slop Codex',
    'scent': '👃 Scent Occasions', 'time': '⏰ Time & Place', 'fate': '🎲 Fate & Chekhov Ledger',
    'bonds': '🥰 Bonds Lite', 'claude': '🩹 Model Patch: Claude 5', 'gemini': '🩹 Model Patch: Gemini',
    'glm': '🩹 Model Patch: GLM', 'mimopro': '🩹 Model Patch: MiMo V2.6 Pro', 'story': '📖 Story Context',
    'lc': '🧠 The Logic Core', 'lc_twin': '🧠 The Logic Core (system-role twin)', 'gate': '🚪 Last-Mile Gate',
    'reduce': 'Reduce Reasoning', 'imp': '🪞 Impersonation Turn', 'gemini38': '🩹 Model Patch: Gemini 3.8 Flash',
    'kimi': '🩹 Model Patch: Kimi / Qwen', 'mimoflash': '🩹 Model Patch: MiMo V2.6 Flash',
    'deepseek': '🩹 Model Patch: DeepSeek',
}
MODULE_COND = {'nsfw': 'adult', 'freaky': 'freaky', 'pov': 'pov', 'scene': 'scene', 'npc': 'npc', 'anthro': 'anthro',
               'codex': 'codex', 'scent': 'scent', 'time': 'time', 'fate': 'fate', 'bonds': 'bonds',
               'claude': 'claude', 'glm': 'glm', 'kimi': 'kimi', 'mimopro': 'mimopro', 'mimoflash': 'mimoflash'}


def main_lines(cc):
    body = cc.body('main')
    # first line blanks the variables, then {{trim}} on a line of its own, then the rules
    first, rest = body.split('\n', 1)
    assert first.startswith('{{setvar::') and strip_setvars(first) == '', first[:60]
    assert rest.startswith('{{trim}}\n')
    rest = rest[len('{{trim}}\n'):]
    i = rest.index('{{#if .player-instructions}}')
    return rest[:i].rstrip('\n'), rest[i:]


def custom_body(cc):
    _rules, tail = main_lines(cc)
    m = re.match(r'\{\{#if \.player-instructions\}\}\n(## Custom Player Instructions\n\*\*[^\n]*\*\*\n)'
                 r'\{\{getvar::player-instructions\}\}\n\{\{/if\}\}$', tail)
    assert m, tail
    return m.group(1) + '(Write your instructions here.)'


def reduce_body(cc):
    _c, rest = split_comment(cc.content('939286fd'))
    rest = rest.lstrip('\n')
    if rest.startswith('{{trim}}'):
        rest = rest[len('{{trim}}'):]
    return rest.strip('\n')


def build_all(cc, comments, agents_block, agents_note):
    """{section key: Marinara content} for every converted section. comments: {key: comment text without markers}."""
    V = extract_values(cc)
    check_counts(V)
    out = {}
    rules, _tail = main_lines(cc)
    out['main'] = wrap(None, comments['main'], rules + '\n' + agents_block)
    out['custom'] = wrap(None, comments['custom'], custom_body(cc))
    for key, cond in MODULE_COND.items():
        if key in ('claude', 'glm', 'kimi', 'mimopro', 'mimoflash') or key in ('nsfw', 'freaky', 'pov', 'scene', 'npc',
                                                                                'anthro', 'codex', 'scent', 'time',
                                                                                'fate', 'bonds'):
            out[key] = wrap(COND[cond], comments[key], module_body(cc, key, V))
    gem = gemini_body(cc)
    out['gemini'] = (COND['gemini'] + '{{// %s }}{{trim}}\n%s\n{{else if model_patch == "GEMINI38"}}{{// %s }}{{trim}}\n%s\n{{/if}}'
                     % (comments['gemini'], gem, comments['gemini'], gem))
    out['gemini38'] = wrap(COND['gemini38'], comments['gemini38'], V['gemini38'])
    out['deepseek'] = wrap(COND['deepseek'], comments['deepseek'], deepseek_body(cc))
    out['story'] = '{{// %s }}{{trim}}\n%s' % (comments['story'], story_body(cc))
    out['lc'] = wrap(COND['lc'], comments['lc'], lc_to_mar(cc.content('15b770cf'), V, agents_note))
    out['lc_twin'] = wrap(COND['lc_twin'], comments['lc_twin'], lc_to_mar(cc.content('591b8c15'), V, agents_note))
    out['gate'] = '{{// %s }}{{trim}}\n%s' % (comments['gate'], gate_to_mar(cc.content('jailbreak'), V))
    out['reduce'] = wrap(COND['reduce'], comments['reduce'], reduce_body(cc))
    imp = tidy_body(split_comment(cc.content('379e3c22'))[1])
    out['imp'] = '{{// %s }}{{trim}}\n%s' % (comments['imp'], imp)
    return out, V
