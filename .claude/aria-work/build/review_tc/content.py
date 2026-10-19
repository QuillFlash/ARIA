from common import *
import difflib
c, a = load(CHIBI_TC), load(ARIA_TC)
F = finals()
cc_, ac_ = c['sysprompt']['content'], a['sysprompt']['content']
cp, ap = c['sysprompt']['post_history'], a['sysprompt']['post_history']

def ifbody(s, tag):
    assert s.count(tag) == 1, (tag, s.count(tag))
    i = s.index(tag) + len(tag)
    then, els, end = ab.split_if(s, i)
    assert els is None
    return i, i + len(then), end

def comment_before(s, sw):
    m = list(re.finditer(r'(\{\{//[^\n]*?\}\})\{\{\.%s = (?:on|off)\}\}' % re.escape(sw), s))
    assert len(m) == 1, sw
    return m[0].start(1), m[0].end(1)

# --- 1. each final occurs exactly once in Chibi TC content
segs = {}  # key -> new text expected in chibi content
g1, g2, g3, g4, g5, g6, jb = (F[k] for k in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'JB'))
for k in ('main_prompt', 'readme_comment', 'custom_instructions_comment'):
    segs['G1.' + k] = g1['tc'][k]
segs['G2.anti_slop_block'] = g2['tc']['anti_slop_block']
for k, v in g4['tc'].items():
    segs['G4.' + k] = v
for k in ('time_place_block', 'fate_block', 'bonds_block', 'switch_comment_time_place', 'switch_comment_fate', 'switch_comment_bonds'):
    segs['G5.' + k] = g5['tc'][k]
for k, v in g6['tc'].items():
    segs['G6.' + k] = v
segs['JB.tc_switch_comment'] = jb['tc_switch_comment']
jbblock = ('{{#if .aria-jailbreak}}{{#if .ariaModeLine}}{{setvar::ariaJbLines::2}}{{setvar::ariaJb::'
           + jb['lines'][0] + '\n' + jb['lines'][1] + '}}{{/if}}{{/if}}')
segs['JB.block'] = jbblock
LOG = {c['id']: c for c in load(W / 'build/review_tc_changes.json')['changes']}
for key, cid in (('G5.switch_comment_fate', 'TC2'), ('G5.switch_comment_bonds', 'TC3')):
    assert segs[key] == LOG[cid]['old'], key
    segs[key] = LOG[cid]['new']
    print('expected deviation from final (logged):', key, cid)
bad = 0
for k, v in segs.items():
    n = cc_.count(v)
    if n != 1:
        bad += 1
        print('COUNT', n, k)
print('finals located in content:', len(segs) - bad, 'of', len(segs))

# --- 2. post_history = G3 lc (closing sentence changed) + G2 gate (4 notes wrapped)
lc, gate = g3['tc']['post_history_logic_core'], g2['tc']['post_history_gate']
print('G3 lc in chibi post as-is:', cp.count(lc), '; G2 gate as-is:', cp.count(gate))
CLOSE_OLD = 'with no Fate, Bonds, Ledger, Layers, Role or Frank line.'
CLOSE_NEW = 'with no Fate, Bonds, Ledger, Layers, Role, Frank, Own words or POV line.'
CLOSE_OLD2 = "move, with no Fate"; CLOSE_NEW2 = "move; skip any Fate"
lc2 = lc.replace(CLOSE_OLD, CLOSE_NEW).replace(CLOSE_OLD2, CLOSE_NEW2)
LOGD = {c['id']: c for c in load(W / 'build/review_tc_changes.json')['changes']}
lc2 = lc2.replace(LOGD['TC4']['old'], LOGD['TC4']['new'])
assert lc.count(CLOSE_OLD) == 1
gate2 = gate
for var, note in (('ariaEchoGate', ' A message written as {{user}} skips it.'), ('ariaPovGate', ' A message written as {{user}} skips it.'),
                  ('ariaLedgerGate', ' A message written as {{user}} carries none.'), ('ariaHoldGate', ' A message written as {{user}} skips it.')):
    old = '{{getvar::%s}}%s\n{{/if}}' % (var, note)
    assert gate2.count(old) == 1, var
    gate2 = gate2.replace(old, '{{getvar::%s}}{{#if !.aria-logic-core}}%s{{/if}}\n{{/if}}' % (var, note))
print('post_history == G3(close changed) + G2(notes wrapped):', cp == lc2 + gate2)
# other "A message written as" occurrences in finals
print('notes in G2 gate:', gate.count('A message written as'), '; in G3 lc:', lc.count('A message written as'), '; in chibi post:', cp.count('A message written as'))
open(OUT / 'g3_lc_final.txt', 'w').write(lc)
open(OUT / 'g2_gate_final.txt', 'w').write(gate)

# --- 3. mask the finals in chibi, mask ARIA's matching spans, compare the rest
M = lambda k: '\x01' + k + '\x02'
mc = cc_
for k, v in segs.items():
    mc = mc.replace(v, M(k))
ma = ac_
# ARIA spans located independently by anchors
spans = []
i = ac_.index('{{// README'); j = ac_.index('}}{{trim}}', i) + len('}}{{trim}}'); spans.append(('G1.readme_comment', i, j))
i = ac_.index('{{// If you have any additional'); j = take = ab.take_macro(ac_, i); spans.append(('G1.custom_instructions_comment', i, j))
i = ac_.index('{{setvar::ariaDice::}}'); k2 = ac_.index('{{getvar::player-instructions}}'); j = ac_.index('{{/if}}', k2) + 7; spans.append(('G1.main_prompt', i, j))
i = ac_.index('<scene_engine>'); j = ac_.index('</scene_engine>') + len('</scene_engine>'); spans.append(('G4.scene_engine', i, j))
assert ac_.count('{{setvar::ariaEchoGate::- ') == 1; i = ac_.index('{{setvar::ariaEchoGate::- '); j = ac_.index('</anti_slop>') + len('</anti_slop>'); spans.append(('G2.anti_slop_block', i, j))
for sw in ('adult', 'freaky', 'hybrid-pov', 'npc-voice', 'anthro', 'scent'):
    bs, be, _ = ifbody(ac_, '{{#if .aria-%s}}' % sw); spans.append(('G4.if_aria-' + sw, bs, be))
for sw, key in (('time-place', 'time_place_block'), ('fate', 'fate_block'), ('bonds', 'bonds_block')):
    bs, be, _ = ifbody(ac_, '{{#if .aria-%s}}' % sw); spans.append(('G5.' + key, bs, be))
for sw, key in (('time-place', 'switch_comment_time_place'), ('fate', 'switch_comment_fate'), ('bonds', 'switch_comment_bonds')):
    s0, s1 = comment_before(ac_, 'aria-' + sw); spans.append(('G5.' + key, s0, s1))
t = '{{#if .aria-jailbreak}}'; bs, be, end = ifbody(ac_, t); spans.append(('JB.block', bs - len(t), end))
s0, s1 = comment_before(ac_, 'aria-jailbreak'); spans.append(('JB.tc_switch_comment', s0, s1))
for sw in ('patch-glm', 'patch-kimi-qwen', 'patch-mimo-pro', 'patch-mimo-flash', 'patch-deepseek', 'flash-gate', 'character-hold'):
    t = '{{if .aria-flash-gate}}' if sw == 'flash-gate' else '{{#if .aria-%s}}' % sw
    bs, be, end = ifbody(ac_, t); spans.append(('G6.module_aria-' + sw, bs - len(t), end))
    s0, s1 = comment_before(ac_, 'aria-' + sw); spans.append(('G6.switch_comment_aria-' + sw, s0, s1))
assert sorted(k for k, *_ in spans) == sorted(segs), set(segs) ^ {k for k, *_ in spans}

for k, i, j in sorted(spans, key=lambda x: -x[1]):
    ma = ma[:i] + M(k) + ma[j:]
# non-final switch comments: mask in both, record pairs
own = {}
for sw, _ in SW.findall(ma):
    try:
        s0, s1 = comment_before(ma, sw); t0, t1 = comment_before(mc, sw)
    except AssertionError:
        continue
    own[sw] = (ma[s0:s1], mc[t0:t1])
    ma = ma[:s0] + M('own.' + sw) + ma[s1:]
    t0, t1 = comment_before(mc, sw)
    mc = mc[:t0] + M('own.' + sw) + mc[t1:]
print('masked rest equal (content):', ma == mc)
if ma != mc:
    for line in difflib.unified_diff(ma.split('\n'), mc.split('\n'), 'aria', 'chibi', lineterm='', n=0):
        print('   ', line.replace('\x01', '«').replace('\x02', '»')[:300])
print('own switch comments rewritten:')
for sw, (o, n) in own.items():
    print(' ', sw, 'CHANGED' if o != n else 'same as ARIA')
# ARIA segments with same text as Chibi? (a final that equals ARIA text means nothing replaced - flag)
for k, i, j in spans:
    if ac_[i:j] == segs[k]:
        print('final equals ARIA text (unchanged):', k)

open(OUT / 'masked_aria.txt', 'w').write(ma.replace('\x01', '«').replace('\x02', '»'))
open(OUT / 'masked_chibi.txt', 'w').write(mc.replace('\x01', '«').replace('\x02', '»'))
