#!/usr/bin/env python3
"""Compare the macro skeleton (wiring) of draft prompt texts against their source texts.

The skeleton is the ordered list of macros, with comments, {{user}}, {{char}} and literal text left out:
setvar/addvar keep their variable names (and the skeleton of their bodies), if/else/getvar keep their conditions
and names. Two texts with equal skeletons have the same wiring, whatever their wording.

usage:
  python3 skeleton.py SRC_CC.json DRAFT.json            compare every prompt in DRAFT.json["prompts"] with SRC_CC's prompt
  python3 skeleton.py --text SRC.txt DRAFT.txt          compare two raw text files (e.g. TC post_history parts)
Prints OK or a unified diff of the skeletons for each pair.
"""
import difflib, json, sys
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
from aria_budget import take_macro  # noqa: E402

SKIP = {'user', 'char', 'trim'}


def skeleton(s):
    out, i = [], 0
    while i < len(s):
        if not s.startswith('{{', i):
            i += 1
            continue
        j = take_macro(s, i)
        m = s[i + 2:j - 2]
        if m.startswith('//') or m in SKIP:
            pass
        elif m.startswith(('setvar::', 'addvar::')):
            kind, rest = m.split('::', 1)
            name, _, body = rest.partition('::')
            out.append(f'{kind}::{name}')
            out += ['  ' + x for x in skeleton(body)]
            out.append(f'end {kind}::{name}')
        else:
            out.append(m)
        i = j
    return out


def compare(label, a, b):
    sa, sb = skeleton(a), skeleton(b)
    if sa == sb:
        print(f'OK    {label}')
        return True
    print(f'DIFF  {label}')
    for line in difflib.unified_diff(sa, sb, 'source', 'draft', lineterm='', n=1):
        print('   ', line)
    return False


def main():
    args = sys.argv[1:]
    if args and args[0] == '--text':
        a, b = (open(p, encoding='utf-8').read() for p in args[1:3])
        sys.exit(0 if compare(args[2], a, b) else 1)
    src = json.loads(open(args[0], encoding='utf-8').read())
    draft = json.loads(open(args[1], encoding='utf-8').read())
    by_id = {p['identifier']: p for p in src['prompts']}
    ok = True
    for pid, p in draft.get('prompts', {}).items():
        if pid not in by_id:
            print(f'NEW   {pid} (no source prompt to compare)')
            continue
        ok &= compare(f"{by_id[pid].get('name', pid)} [{pid[:8]}]", by_id[pid].get('content') or '', p.get('content') or '')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
