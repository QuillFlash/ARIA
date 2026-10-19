"""Fix 4: what each TC switch costs, measured the way the guide's switch table does: flip one switch from the shipped state.
Dependent switches are flipped with their prerequisite(s) on in both renders. Tokens = checker metric (sum of rounded parts) and
exact characters / 4 of the whole render."""
import json
from rxlib import *

tc = tc_preset(TCFILE)
shipped = shipped_switches(tc)


def total(overrides):
    r, _ = ab.simulate_tc(tc, overrides, seed=1)
    chars = sum(len(t) for t in r.values())
    return sum(ab.tokens(t) for t in r.values()), chars / 4


def delta(switch, base_extra=None, flip_to=None):
    base = dict(shipped) | (base_extra or {})
    flipped = dict(base)
    flipped[switch] = flip_to or ('off' if base[switch] == 'on' else 'on')
    a, ca = total(base)
    b, cb = total(flipped)
    return abs(b - a), abs(cb - ca)


print('shipped state:', {k: v for k, v in shipped.items() if v == 'on'}, '| total', total(shipped))
print()
rows = []
LC = {'aria-logic-core': 'on'}
for s in shipped:
    extra = None
    note = 'from the shipped state'
    if s == 'aria-freaky':
        extra, note = {'aria-adult': 'on'}, 'with aria-adult on'
    elif s == 'aria-jailbreak':
        extra, note = {'aria-adult': 'on', 'aria-logic-core': 'on'}, 'with aria-adult and aria-logic-core on'
    elif s == 'aria-thinking-tags':
        extra, note = dict(LC), 'with aria-logic-core on, tags on -> off'
    elif s == 'aria-flash-gate':
        extra, note = {}, 'from the shipped state, no patch'
    tok, chars = delta(s, extra)
    rows.append((s, shipped[s], tok, chars, note))
for s, st, tok, chars, note in rows:
    print(f'{s:24} ships {st:3} | {tok:4} tokens (exact {chars:7.2f}) | {note}')

print()
print('Extra context for the comments that quote a cost:')
# The Logic Core: the guide says ~405 as shipped (tags on). Also with tags off, and with the Logic Core's lines for other modules.
for tags in ('on', 'off'):
    t, c = delta('aria-logic-core', {'aria-thinking-tags': tags})
    print(f'  aria-logic-core on, tags {tags}: {t} tokens (exact {c:.2f})')
# the whole of the Logic Core with the JB over adult, for the JB comment
for label, extra in (('adult only', {'aria-adult': 'on', 'aria-logic-core': 'on'}), ('freaky only', {'aria-freaky': 'on', 'aria-logic-core': 'on'}),
                     ('adult + freaky', {'aria-adult': 'on', 'aria-freaky': 'on', 'aria-logic-core': 'on'})):
    t, c = delta('aria-jailbreak', extra)
    print(f'  aria-jailbreak over {label}: {t} tokens (exact {c:.2f})')
for tags in ('on', 'off'):
    t, c = delta('aria-jailbreak', {'aria-adult': 'on', 'aria-logic-core': 'on', 'aria-thinking-tags': tags})
    print(f'  aria-jailbreak over adult, tags {tags}: {t} tokens (exact {c:.2f})')
