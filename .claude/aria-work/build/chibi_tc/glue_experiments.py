"""Scratch: what does TC's own glue cost, and what do restructurings save (in-memory only)."""
import json, sys, copy
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/tools')
import aria_budget as ab
tc = json.load(open(sys.argv[1], encoding='utf-8'))

def totals(p, name='Chibi Edition x.json'):
    t, e = ab.analyse_tc(p, name)
    return t, e

def variant(f):
    p = copy.deepcopy(tc)
    p['sysprompt']['post_history'] = f(p['sysprompt']['post_history'])
    return p

NOTE_SKIP = ' A message written as {{user}} skips it.'
NOTE_NONE = ' A message written as {{user}} carries none.'
CLOSE = "For a message written as {{user}}, plan only {{user}}'s move, with no Fate, Bonds, Ledger, Layers, Role or Frank line."

def v_b(ph):
    # remove the Echo, POV, Hold notes and the Ledger note; add one sentence to the last gate line
    ph = ph.replace('{{getvar::ariaEchoGate}}' + NOTE_SKIP, '{{getvar::ariaEchoGate}}')
    ph = ph.replace('{{getvar::ariaPovGate}}' + NOTE_SKIP, '{{getvar::ariaPovGate}}')
    ph = ph.replace('{{getvar::ariaLedgerGate}}' + NOTE_NONE, '{{getvar::ariaLedgerGate}}')
    ph = ph.replace('{{getvar::ariaHoldGate}}' + NOTE_SKIP, '{{getvar::ariaHoldGate}}')
    old = 'Follow these over earlier replies; the card outranks all but Humour.'
    assert ph.count(old) == 1
    return ph.replace(old, old + ' A message written as {{user}} skips Own words, POV, Ledger and Layers.')

def show(label, p):
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        t, e = totals(p)
    print(f'{label:46} all-ON {t["everything ON"]}  lean {t["shipped (lean, 32k)"]}  roomy {t["+ Logic Core, Fate, Time"]}  errors {e}')

show('as the finals (V_A)', tc)
show('V_B notes -> one gate sentence', variant(v_b))
def v_c(ph):
    ph = v_b(ph)
    return ph.replace(CLOSE, "For a message written as {{user}}, plan only {{user}}'s move: no Fate, Bonds, Ledger, Layers, Role or Frank line.")
show('V_C = V_B + tightened closing', variant(v_c))
def v_none(ph):
    ph = v_b(ph)
    ph = ph.replace(' A message written as {{user}} skips Own words, POV, Ledger and Layers.', '')
    return ph
show('V_none: notes removed, nothing added', variant(v_none))
def v_nonotes_noclose(ph):
    ph = v_none(ph)
    return ph.replace(' ' + CLOSE, '')
show('V_none2: notes and closing removed', variant(v_nonotes_noclose))

print()
print('--- single-sentence variants (closing sentence moved out of the Logic Core into the gate)')
def strip_glue(ph, keep_tally=True):
    ph = v_none(ph)                       # four gate notes gone
    ph = ph.replace(' ' + CLOSE, '')      # closing sentence gone from the Logic Core
    return ph
def with_gate_sentence(s, keep_tally=True):
    def f(ph):
        ph = strip_glue(ph)
        old = 'Follow these over earlier replies; the card outranks all but Humour.'
        assert ph.count(old) == 1
        return ph.replace(old, old + ' ' + s)
    return f
cands = {
 'S1 plans only {{user}}\'s move and skips 9 labels': "A message written as {{user}} plans only {{user}}'s move and skips Fate, Bonds, Tally, Ledger, Layers, Role, Frank, Own words and POV.",
 'S2 same with "its move"': "A message written as {{user}} plans only its move and skips Fate, Bonds, Tally, Ledger, Layers, Role, Frank, Own words and POV.",
 'S3 no Tally (Tally keeps its own note)': "A message written as {{user}} plans only its move and skips Fate, Bonds, Ledger, Layers, Role, Frank, Own words and POV.",
}
for k, s in cands.items():
    show(k, variant(with_gate_sentence(s)))

print()
print('--- (12): closing sentence stays in the Logic Core, extended; one fallback sentence in the gate while the Logic Core is off')
CLOSE2 = "For a message written as {{user}}, plan only {{user}}'s move, with no Fate, Bonds, Tally, Ledger, Layers, Role, Frank, Own words or POV line."
OFFS = "{{#if !.aria-logic-core}} For a message written as {{user}}, skip the Own words, POV, Ledger and Layers lines.{{/if}}"
def v12(ph):
    ph = v_none(ph)
    # Tally note gone, closing sentence extended
    tn = '{{getvar::ariaPatchTally}}' + NOTE_SKIP
    assert ph.count(tn) == 1
    ph = ph.replace(tn, '{{getvar::ariaPatchTally}}')
    assert ph.count(CLOSE) == 1
    ph = ph.replace(CLOSE, CLOSE2)
    old = 'Follow these over earlier replies; the card outranks all but Humour.'
    return ph.replace(old, old + OFFS)
p12 = variant(v12)
show('(12) closing extended + LC-off fallback', p12)
# lean with Logic Core on
import io, contextlib
def lean_lc_on(p, tags='on'):
    shipped = dict(ab.SWITCH.findall(p['sysprompt']['content']))
    ov = dict(shipped) | {'aria-logic-core': 'on', 'aria-thinking-tags': tags}
    r, _ = ab.simulate_tc(p, ov, 1)
    return sum(ab.tokens(t) for t in r.values())
print('lean start with the Logic Core ON (tags on / off): finals glue', lean_lc_on(tc), lean_lc_on(tc, 'off'), '| (12)', lean_lc_on(p12), lean_lc_on(p12, 'off'))
