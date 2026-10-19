"""Compose the Chibi Logic Core text (shared body) and measure it. Work file for G3."""
import json, random, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab

OPEN = '{{getvar::ariaThinkOpen}}'
CLOSE = '{{getvar::ariaThinkClose}}'
N = '{{getvar::logicCoreLines}}'

# counting prefix: JB counter right after the Ledger counter (JB.md, Wiring in CC)
COUNT = (
    '{{setvar::logicCoreLines::7}}'
    '{{#if .ariaModeLine}}{{addvar::logicCoreLines::1}}{{/if}}'
    '{{#if .ariaFateLine}}{{addvar::logicCoreLines::1}}{{/if}}'
    '{{#if .ariaBondsLine}}{{addvar::logicCoreLines::1}}{{/if}}'
    '{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}'
    '{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}'
    '{{#if .ariaHoldLine}}{{addvar::logicCoreLines::1}}{{/if}}'
    '{{#if .ariaPatchTally}}{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}{{/if}}'
    '{{#if .ariaPatchJoins}}{{addvar::logicCoreLines::1}}{{/if}}'
    '{{#if .ariaPatchLines}}{{addvar::logicCoreLines::{{getvar::ariaPatchLines}}}}{{/if}}'
)


def body(t, tc=False):
    """t: dict of the wording pieces. tc: add the TC-only parts."""
    tally_note = ' A message written as {{user}} skips it.' if tc else ''
    tail_tc = (" For a message written as {{user}}, plan only {{user}}'s move, with no Fate, Bonds, Ledger, Layers, Role or Frank line."
               if tc else '')
    s = COUNT
    s += ('{{#if .ariaThinkOpen}}{{setvar::ariaPlanCue::' + t['cue'] + '}}' + t['head_on'] + '{{else}}<logic_core>\n' + t['head_off'] + '{{/if}}\n')
    s += t['frag'] + '{{#if .ariaThinkOpen}}' + t['frag_on'] + '{{/if}}.\n'
    s += '- OOC: ' + t['ooc'] + '\n'
    s += '- Scene: ' + t['scene'] + '\n'
    s += '- Knows: ' + t['knows'] + '\n'
    s += '{{#if .ariaModeLine}}{{getvar::ariaModeLine}}\n{{/if}}'
    s += '- Voice: ' + t['voice_a'] + '{{getvar::ariaVoiceExtra}}' + t['voice_b'] + '\n'
    s += '{{#if .ariaHoldLine}}{{getvar::ariaHoldLine}}\n{{/if}}'
    s += '{{#if .ariaPatchGate}}{{getvar::ariaPatchGate}}\n{{/if}}'
    s += '{{#if .ariaPatchJoins}}{{getvar::ariaPatchJoins}}\n{{/if}}'
    s += '- Move: ' + t['move'] + '\n'
    s += '{{#if .ariaFateLine}}{{getvar::ariaFateLine}}\n{{/if}}'
    s += '{{#if .ariaBondsLine}}{{getvar::ariaBondsLine}}\n{{/if}}'
    s += '{{#if .ariaPatchTally}}{{#if .ariaLedgerLine}}{{getvar::ariaPatchTally}}' + tally_note + '\n{{/if}}{{/if}}'
    s += '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}'
    s += '{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}'
    s += '- Fresh: ' + t['fresh'] + '\n'
    s += '- Check: ' + t['check'] + '\n'
    s += '- go\n'
    s += '{{#if .ariaThinkOpen}}' + t['tail_on'] + '{{else}}' + t['tail_off'] + '{{/if}} ' + t['reply_a'] + '{{#if .ariaLedgerLine}}; ledger last{{/if}}. ' + t['reply_b'] + tail_tc
    s += '{{#if .ariaThinkOpen}}\nEvery response starts with ' + OPEN + '.{{else}}\n</logic_core>{{/if}}'
    return s


def render(s, state=None):
    st = dict(state or {})
    return ab.render(s, st, random.Random(1)), st


def report(s, label=''):
    out = []
    for name, state in (('tags off', {}), ('tags on', {'ariaThinkOpen': '<thinking>', 'ariaThinkClose': '</thinking>'}),
                        ('mode line set', {'ariaModeLine': 'x'})):
        t, st = render(s, state)
        out.append(f'{name}: {len(t)} chars, {ab.tokens(t)} tok')
    print(label, ' | '.join(out))
