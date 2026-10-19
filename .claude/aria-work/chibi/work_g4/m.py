#!/usr/bin/env python3
"""Scratch harness for G4: measure candidate texts (chars, tokens, gate lines) against the ceilings.

usage: python3 m.py cand.py     (cand.py defines CAND = {key: {"name":..., "content":...}})
"""
import importlib.util, json, random, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab  # noqa: E402

CEIL = {  # key: (module ceiling, set-var name, set-var ceiling)
    '15a8065d': (110, None, None),
    'cca418a6': (120, None, None),
    '2a2e12d0': (50, None, None),
    'dd3642f5': (40, 'ariaScentGate', 25),
    'b7b6ab7f': (25, 'ariaPovGate', 20),
    'nsfw': (60, 'ariaModeLine', 12),
    '4537b57d': (30, 'ariaModeLine', 8),
}


def measure(text, state=None):
    st = dict(state or {})
    out = ab.render(text, st, random.Random(1))
    return out, st


def main():
    spec = importlib.util.spec_from_file_location('cand', sys.argv[1])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cand = mod.CAND
    tot = 0
    for key, (ceil, var, vceil) in CEIL.items():
        full = next((k for k in cand if k.startswith(key)), None)
        if full is None:
            print(f'-- {key}: missing')
            continue
        out, st = measure(cand[full]['content'])
        n = len(out)
        tk = ab.tokens(out)
        tot += tk
        flag = 'OK ' if tk <= ceil else 'OVER'
        line = f'{flag} {key:9} {tk:4}/{ceil:<4} chars {n:4}  {cand[full]["name"]}'
        if var:
            v = st.get(var, '')
            vt = ab.tokens(v)
            line += f'   | {var} {vt}/{vceil}{"" if vt <= vceil else " OVER"} ({len(v)} chars)'
        print(line)
    print('module total', tot, 'of 435')
    if len(sys.argv) > 2 and sys.argv[2] == '-v':
        for key in CEIL:
            full = next((k for k in cand if k.startswith(key)), None)
            out, st = measure(cand[full]['content'])
            print('=' * 70)
            print(cand[full]['name'])
            print(out)
            for k, v in st.items():
                print(f'   [{k}] {v}')


if __name__ == '__main__':
    main()
