#!/usr/bin/env python3
"""Token sizes (characters / 4, comments stripped, the ARIA checker's metric) for draft prompt contents.

usage: python3 tok.py drafts.json [--state '{"ariaModeLine": "x"}']
drafts.json: {"prompts": {"<id>": {"name": "...", "content": "..."}}, "tc": {"<key>": "<text>"}}
For each prompt it prints the tokens the entry renders itself, then the tokens of every variable it sets
(text that other entries print, such as gate or plan lines). Variables listed in --state start out set,
so conditional blocks that test them render.
"""
import argparse, json, random, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab  # noqa: E402


def measure(text, state):
    st = dict(state)
    out = ab.render(text, st, random.Random(1))
    sets = {k: ab.tokens(v) for k, v in st.items() if isinstance(v, str) and v and state.get(k) != v}
    return ab.tokens(out), sets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--state', default='{}')
    a = ap.parse_args()
    data = json.loads(open(a.file, encoding='utf-8').read())
    state = json.loads(a.state)
    for pid, p in (data.get('prompts') or {}).items():
        own, sets = measure(p.get('content') or '', state)
        extra = ', '.join(f'{k} {v}' for k, v in sets.items())
        print(f"{own:5}  {p.get('name', pid)}" + (f"   [sets: {extra}]" if extra else ''))
    for key, text in (data.get('tc') or {}).items():
        own, sets = measure(text, state)
        print(f'{own:5}  TC {key}')


if __name__ == '__main__':
    main()
