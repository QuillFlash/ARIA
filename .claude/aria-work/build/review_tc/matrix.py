"""simulate_tc matrix over Chibi TC: counts, leftovers, spacing, cache stability, LC-off equality with the finals glue."""
import itertools, sys
from common import *
tc = load(sys.argv[1] if len(sys.argv) > 1 else CHIBI_TC)
fin = load(OUT / 'finals_glue.json')
PATCHES = ['aria-patch-glm', 'aria-patch-kimi-qwen', 'aria-patch-mimo-pro', 'aria-patch-mimo-flash', 'aria-patch-deepseek', None]
issues, n, lcoff_same, lcoff_n = {}, 0, 0, 0
def flag(k, tag):
    issues.setdefault(k, []).append(tag)
stale_all = None
for lc, tags, mode, jb, fate, bonds, patch, flash, hold, extra in itertools.product(
        ('on', 'off'), ('on', 'off'), ('none', 'adult', 'freaky'), (0, 1), (0, 1), (0, 1), PATCHES, (0, 1), (0, 1), (0, 1)):
    sw = {'aria-logic-core': lc, 'aria-thinking-tags': tags, 'aria-adult': 'off' if mode == 'none' else 'on',
          'aria-freaky': 'on' if mode == 'freaky' else 'off', 'aria-jailbreak': 'on' if jb else 'off',
          'aria-fate': 'on' if fate else 'off', 'aria-bonds': 'on' if bonds else 'off', 'aria-flash-gate': 'on' if flash else 'off',
          'aria-character-hold': 'on' if hold else 'off', 'aria-hybrid-pov': 'on' if extra else 'off', 'aria-time-place': 'on' if extra else 'off',
          'aria-anthro': 'on' if extra else 'off', 'aria-npc-voice': 'off' if extra else 'on', 'aria-scent': 'off' if extra else 'on'}
    for p in PATCHES[:-1]:
        sw[p] = 'on' if p == patch else 'off'
    tag = ' '.join(f'{k[5:]}={v}' for k, v in sw.items() if v == 'on' or k == 'aria-logic-core')
    r, st = ab.simulate_tc(tc, sw, 1)
    n += 1
    S, Pst = r['System Prompt'], r['Post-History']
    whole = S + '\n' + Pst
    if '{{' in whole or '}}' in whole: flag('leftover macro', tag)
    if '\\n' in whole: flag('literal backslash-n', tag)
    if re.search(r'(?<=\S)  +(?=\S)', whole) or re.search(r'  ', Pst): flag('doubled space', tag)
    if re.search(r' [,.;:]', Pst): flag('space before punctuation', tag)
    if re.search(r'\n[ \t]*\n', Pst): flag('blank line in post-history', tag)
    if re.search(r'[;,]\s*$', Pst, re.M): flag('line ends on separator', tag)
    if re.search(r'^[ \t]+\S|\S[ \t]+$', Pst, re.M): flag('edge whitespace in post-history', tag)
    # counts
    if lc == 'on':
        lines = Pst.split('\n')
        try:
            go = lines.index('- go')
        except ValueError:
            flag('no - go line', tag); continue
        if tags == 'on':
            m = re.match(r'<thinking> opens the reply, then (\d+) dashed lines and go\.', lines[0]); head = 0
        else:
            m = re.match(r'Reasoning: (\d+) lines; go ends it\.', lines[1]) if lines[0] == '<logic_core>' else None
        if not m:
            flag('plan head not found', tag); continue
        dashed = [l for l in lines[:go] if l.startswith('- ')]
        if int(m.group(1)) != len(dashed): flag(f'count {m.group(1)} vs {len(dashed)} dashed', tag)
        if tags == 'on':
            cue = re.search(r'Begin with <thinking>, then (\d+) dashed lines, go and </thinking>; the reply follows\.$', Pst)
            if not cue or int(cue.group(1)) != len(dashed): flag('plan cue count', tag)
        # each dashed line has a label
        for l in dashed:
            if not re.match(r'- [A-Z][\w ]*: \S', l): flag('unlabelled dashed line: ' + l[:40], tag)
        if 'For a message written as User, plan only' not in Pst: flag('closing sentence missing', tag)
        if 'A message written as User skips it.' in Pst.split('<final_gate>')[1] or 'carries none' in Pst: flag('gate note printed with LC on', tag)
    else:
        if '<logic_core>' in Pst or '- go' in Pst or 'For a message written as' in Pst: flag('plan text with LC off', tag)
        # LC off: the post-history and system prompt equal the finals glue's
        rf, _ = ab.simulate_tc(fin, sw, 1)
        lcoff_n += 1
        if rf == r: lcoff_same += 1
        else: flag('LC off differs from finals glue', tag)
        gate = Pst
        for var, lab in (('ariaEchoGate', '- Own words:'), ('ariaPovGate', '- POV:'), ('ariaLedgerGate', '- Ledger:'), ('ariaHoldGate', '- Layers:')):
            if st.get(var):
                line = [l for l in gate.split('\n') if l.startswith(lab)]
                if not line or not re.search(r'A message written as User (skips it|carries none)\.$', line[0]): flag('LC off: note missing on ' + lab, tag)
    # cache: system prompt the same on a later turn (other seed, state left by this turn and by an all-ON turn)
    r2, _ = ab.simulate_tc(tc, sw, 99, state=st)
    if r2['System Prompt'] != S: flag('system prompt differs next turn', tag)
    if stale_all is not None:
        r3, _ = ab.simulate_tc(tc, sw, 7, state=stale_all)
        if r3['System Prompt'] != S: flag('system prompt differs after an all-ON turn', tag)
    if stale_all is None or (lc == 'on' and mode == 'freaky' and jb and fate and bonds and hold and flash):
        stale_all = dict(st)
print('configs', n, '| LC-off renders equal to the finals glue:', lcoff_same, 'of', lcoff_n)
if not issues: print('no issues')
for k, v in issues.items():
    print(f'{k}: {len(v)}  e.g. {v[0]}')
