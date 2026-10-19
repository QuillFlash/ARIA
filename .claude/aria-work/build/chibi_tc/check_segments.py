"""Independent check of the built Chibi TC against the finals: every tc text sits verbatim in the built file, in its wrapper; the
post-history equals G3's Logic Core plus G2's gate once the recorded glue is undone. (That nothing else moved is audited by the
line-level diff against ARIA TC and by build_chibi_tc.py's expected-object check.)"""
import json, re, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
R = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA'
W = R + '/.claude/aria-work'
built = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json", encoding='utf-8'))
aria = json.load(open(R + "/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json", encoding='utf-8'))
F = {g: json.load(open(f'{W}/chibi/final/{g}.json', encoding='utf-8')) for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'JB')}
c, ph = built['sysprompt']['content'], built['sysprompt']['post_history']
n = 0


def once(text, label):
    global n
    assert c.count(text) == 1, f'{label}: found {c.count(text)} times'
    n += 1


# G1
for k in ('main_prompt', 'readme_comment', 'custom_instructions_comment'):
    once(F['G1']['tc'][k], 'G1.' + k)
# G2 anti-slop block
once(F['G2']['tc']['anti_slop_block'], 'G2.anti_slop_block')
# G4 scene engine and the if blocks (text between the {{#if}} and its own {{/if}})
once(F['G4']['tc']['scene_engine'], 'G4.scene_engine')


def body_of(open_tag):
    i = c.index(open_tag)
    bs = i + len(open_tag)
    then, els, end = ab.split_if(c, bs)
    assert els is None and c.count(open_tag) == 1
    return then


for sw in ('adult', 'freaky', 'hybrid-pov', 'npc-voice', 'anthro', 'scent'):
    assert body_of('{{#if .aria-%s}}' % sw) == F['G4']['tc']['if_aria-' + sw], 'G4 if_aria-' + sw
    n += 1
for key, sw in (('time_place_block', 'time-place'), ('fate_block', 'fate'), ('bonds_block', 'bonds')):
    assert body_of('{{#if .aria-%s}}' % sw) == F['G5']['tc'][key], 'G5 ' + key
    n += 1
# G6 modules, whole
for sw in ('aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro', 'aria-patch-mimo-flash', 'aria-patch-deepseek', 'aria-flash-gate', 'aria-character-hold'):
    once(F['G6']['tc']['module_' + sw], 'G6.module_' + sw)
    # and it is a complete block: it opens with its tag and ends with its own closing {{/if}}
    t = F['G6']['tc']['module_' + sw]
    then, els, end = ab.split_if(t, t.index('}}') + 2)
    assert end == len(t), 'module ' + sw + ' is not one whole block'
# the JB block
jb = F['JB']
jb_block = ('{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::' + jb['lines'][0] + '\n' + jb['lines'][1] + '}}{{/if}}{{/if}}')
once(jb_block, 'JB block')
# switch comments: supplied ones verbatim, each right before its own switch tag
supplied = {'aria-time-place': F['G5']['tc']['switch_comment_time_place'], 'aria-fate': F['G5']['tc']['switch_comment_fate'],
            'aria-bonds': F['G5']['tc']['switch_comment_bonds'], 'aria-jailbreak': jb['tc_switch_comment']}
for sw in ('aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro', 'aria-patch-mimo-flash', 'aria-patch-deepseek', 'aria-flash-gate', 'aria-character-hold'):
    supplied[sw] = F['G6']['tc']['switch_comment_' + sw]
for sw, text in supplied.items():
    assert re.search(re.escape(text) + r'\{\{\.%s = (on|off)\}\}' % re.escape(sw), c), 'comment before ' + sw
    n += 1
# post_history: undo the recorded glue and compare with G3's Logic Core + G2's gate
NOTE = ' A message written as {{user}} skips it.'
NOTE_NONE = ' A message written as {{user}} carries none.'
undo = ph
for var, note in (('ariaEchoGate', NOTE), ('ariaPovGate', NOTE), ('ariaLedgerGate', NOTE_NONE), ('ariaHoldGate', NOTE)):
    new = '{{getvar::%s}}{{#if !.aria-logic-core}}%s{{/if}}\n{{/if}}' % (var, note)
    assert undo.count(new) == 1, var
    undo = undo.replace(new, '{{getvar::%s}}%s\n{{/if}}' % (var, note))
assert undo.count('with no Fate, Bonds, Ledger, Layers, Role, Frank, Own words or POV line.') == 1
undo = undo.replace('with no Fate, Bonds, Ledger, Layers, Role, Frank, Own words or POV line.', 'with no Fate, Bonds, Ledger, Layers, Role or Frank line.')
assert undo == F['G3']['tc']['post_history_logic_core'] + F['G2']['tc']['post_history_gate'], 'post_history differs from G3 + G2'
n += 2
print('segment texts found verbatim:', n)
print('OK: every final tc text sits verbatim in its wrapper; post_history = G3 Logic Core + G2 gate with the recorded glue only')
