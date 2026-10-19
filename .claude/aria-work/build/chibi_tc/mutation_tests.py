"""Mutation tests for verify_chibi_tc.py: each mutant of the built file must be caught."""
import json, sys, tempfile, os
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/build/chibi_tc')
import verify_chibi_tc as v

STRIDE = int(sys.argv[sys.argv.index('--stride') + 1]) if '--stride' in sys.argv else 9
SKIP = int(sys.argv[sys.argv.index('--skip') + 1]) if '--skip' in sys.argv else 0
SRC = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Text Completions).json"
d0 = json.load(open(SRC, encoding='utf-8'))


def mutant(name, fn, glue='capped'):
    d = json.loads(json.dumps(d0, ensure_ascii=False))
    fn(d['sysprompt'])
    path = os.path.join(tempfile.gettempdir(), 'mut_chibi_tc.json') if False else '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/build/chibi_tc/out/mutant.json'
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    total, nbad, problems = v.verify(path, glue=glue, jobs=4, quiet=True, stride=STRIDE)
    caught = bool(problems)
    kinds = sorted({re_kind(e) for k, e in problems})[:3]
    print(f'{"CAUGHT " if caught else "MISSED "} {name:62} ({total} renders, {nbad} bad, {len(problems)} problem kinds) {kinds}')
    return caught


def re_kind(e):
    import re
    return re.sub(r'\d+', 'N', e)[:70]


def rep(key, old, new, count=1):
    def f(sp):
        assert sp[key].count(old) == count, (key, old, sp[key].count(old))
        sp[key] = sp[key].replace(old, new)
    return f


def main():
    ok = True
    if SKIP == 0:
        ok &= mutant('unmutated file (must pass)', lambda sp: None) is False  # expects NOT caught
    muts = [
        ('plan count off by one (logicCoreLines 7 -> 6)', rep('post_history', '{{setvar::logicCoreLines::7}}', '{{setvar::logicCoreLines::6}}')),
        ('JB counter removed', rep('post_history', '{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}', '')),
        ('literal backslash-n between the JB lines', rep('content', 'tone.\n- Frank:'.replace('tone.', 'trait, tone.') if False else '\n- Frank: sex stays', '\\n- Frank: sex stays')),
        ('Echo note prints with the Logic Core on (wrapper removed)', rep('post_history', '{{getvar::ariaEchoGate}}{{#if !.aria-logic-core}} A message written as {{user}} skips it.{{/if}}', '{{getvar::ariaEchoGate}} A message written as {{user}} skips it.')),
        ('Ledger note lost for the Logic Core off state', rep('post_history', '{{getvar::ariaLedgerGate}}{{#if !.aria-logic-core}} A message written as {{user}} carries none.{{/if}}', '{{getvar::ariaLedgerGate}}')),
        ('closing sentence reverted to the finals', rep('post_history', 'Role, Frank, Own words or POV line.', 'Role or Frank line.')),
        ('a word changed in the Scent block', rep('content', 'Taste needs mouth contact', 'Taste needs mouth contacts')),
        ('a word changed in the GLM patch', rep('content', 'stammers stay.', 'stammers stays.')),
        ('Mode line changed', rep('content', '- Mode: freaky; escalate.', '- Mode: freaky; escalates.')),
        ('a macro broken ({{getvar::ariaJb}} loses a brace)', rep('post_history', '{{getvar::ariaJb}}\n{{/if}}', '{{getvar::ariaJb}\n{{/if}}')),
        ('Fate dice lost from the gate', rep('post_history', '{{#if .ariaDice}}{{getvar::ariaDice}}\n{{/if}}', '')),
        ('a gate line reworded (Count)', rep('post_history', 'a third goes or becomes an act', 'a third goes or becomes acts')),
        ('Time block header changed', rep('content', "moved on by each reply's span", "moved on by each replys span")),
        ('Own words codex line reworded', rep('content', 'answers show in acts or changes of course', 'answers show in acts or changes of courses')),
    ]
    for name, fn in muts[SKIP:]:
        ok &= mutant(name, fn)
    print('ALL MUTANTS CAUGHT AND THE UNMUTATED FILE PASSES' if ok else 'SOME CHECK FAILED')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
