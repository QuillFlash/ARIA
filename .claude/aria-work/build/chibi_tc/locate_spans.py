"""Scratch: locate the spans of live ARIA TC that the finals replace."""
import json, re, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab

R = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA'
tc = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
c = tc['sysprompt']['content']
ph = tc['sysprompt']['post_history']

def block(open_tag):
    assert c.count(open_tag) == 1, (open_tag, c.count(open_tag))
    i = c.index(open_tag)
    body_start = i + len(open_tag)
    then, els, end = ab.split_if(c, body_start)
    assert els is None
    return i, body_start, body_start + len(then), end

for sw in ['aria-adult', 'aria-freaky', 'aria-jailbreak', 'aria-hybrid-pov', 'aria-npc-voice', 'aria-anthro', 'aria-scent',
           'aria-time-place', 'aria-fate', 'aria-bonds', 'aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro',
           'aria-patch-mimo-flash', 'aria-patch-deepseek', 'aria-character-hold']:
    i, bs, be, end = block('{{#if .%s}}' % sw)
    print(f'{sw:24} open@{i:6} body {bs}-{be} ({be-bs} chars) end@{end}; after: {c[end:end+40]!r}; before: {c[max(0,i-30):i]!r}')
i, bs, be, end = block('{{if .aria-flash-gate}}')
print(f'aria-flash-gate          open@{i} body {bs}-{be} end@{end}; after {c[end:end+40]!r}; before {c[max(0,i-30):i]!r}')
# special spans
a = c.index('{{// README')
b = c.index('}}{{trim}}\n{{// 🎛️ ARIA SWITCHES') + len('}}{{trim}}')
print('README', a, b, repr(c[b:b+30]))
a = c.index('{{// If you have any additional')
b = c.index('}}{{trim}}\n{{.player-instructions =')
print('custom comment', a, b+2, repr(c[b:b+30]))
a = c.index('{{setvar::ariaDice::}}')
b = c.index('{{/if}}', c.index('{{getvar::player-instructions}}')) + len('{{/if}}')
print('main', a, b, repr(c[b:b+40]), 'count of ariaDice blank', c.count('{{setvar::ariaDice::}}'))
a = c.index('<scene_engine>'); b = c.index('</scene_engine>') + len('</scene_engine>')
print('scene', a, b, repr(c[b:b+30]), c.count('<scene_engine>'), c.count('</scene_engine>'))
a = c.index("{{setvar::ariaEchoGate::- "); b = c.index('</anti_slop>') + len('</anti_slop>')
print('anti_slop', a, b, repr(c[b:b+30]), c.count("{{setvar::ariaEchoGate::- "), c.count('</anti_slop>'))
print('post_history gate split', ph.index('<final_gate>'), len(ph), repr(ph[-30:]), repr(ph[ph.index('<final_gate>')-30:ph.index('<final_gate>')+14]))
print('names:', tc['context']['name'], tc['sysprompt']['name'])
