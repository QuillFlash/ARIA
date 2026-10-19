#!/usr/bin/env python3
"""Build G5 candidate texts from a variant module (texts.py style: TIME, FATE, BONDS bodies) and report exact group tokens.
usage: group.py VARIANT.py   (the variant defines TIME_BODY, FATE_BODY, BONDS_BODY; comments and wiring come from the snapshot)"""
import sys, re, json, random, importlib.util
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab
W = '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G5judge'
SRC = {n: open(f'{W}/src_{n}.txt', encoding='utf-8').read() for n in ('time', 'fate', 'bonds')}
TMPL = re.search(r'<details><summary>🎲</summary>.*?</details>', SRC['fate']).group(0)

# wiring runs, verbatim from the snapshot
FATE_SET = SRC['fate'][SRC['fate'].index('{{setvar::ariaDice'):SRC['fate'].index('{{trim}}\nFate:') + len('{{trim}}')]
BONDS_SET = SRC['bonds'][SRC['bonds'].index('{{setvar::ariaBondsLine'):SRC['bonds'].index('{{/if}}{{trim}}') + len('{{/if}}{{trim}}')]


def load_variant(path):
    spec = importlib.util.spec_from_file_location('variant', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def render(text, state=None):
    st = dict(state or {})
    out = ab.render(text, st, random.Random(1))
    return out, st


def measure(time_body, fate_body, bonds_body, verbose=True):
    rows = {}
    t_out, _ = render(time_body)
    rows['time own'] = len(t_out) / 4
    f_out, fst = render(FATE_SET + '\n' + fate_body)
    rows['fate own'] = len(f_out) / 4
    b_out, bst = render(BONDS_SET + '\n' + bonds_body, {'ariaLedgerLine': fst['ariaLedgerLine']})
    rows['bonds own'] = len(b_out) / 4
    rows['dice'] = len(fst['ariaDice']) / 4
    rows['fate plan'] = len(fst['ariaFateLine']) / 4
    rows['ledger line (F+B)'] = len(bst['ariaLedgerLine']) / 4
    rows['ledger gate (F+B)'] = len(bst['ariaLedgerGate']) / 4
    rows['bonds plan'] = len(bst['ariaBondsLine']) / 4
    total = sum(rows.values())
    if verbose:
        for k, v in rows.items():
            print(f'  {v:7.2f}  {k}')
        print(f'  {total:7.2f}  GROUP TOTAL (ceiling 605)   own {rows["time own"] + rows["fate own"] + rows["bonds own"]:.2f}')
    return rows, total, (t_out, f_out, b_out)


def per_line(label, out):
    print(f'---- {label}')
    for line in out.split('\n'):
        print(f'{len(line)/4:7.2f}  {line}')


if __name__ == '__main__':
    v = load_variant(sys.argv[1])
    fate_body = v.FATE_BODY.replace('<TMPL>', TMPL)
    rows, total, (t, f, b) = measure(v.TIME_BODY, fate_body, v.BONDS_BODY)
    if '-v' in sys.argv:
        per_line('TIME', t)
        per_line('FATE', f)
        per_line('BONDS', b)
