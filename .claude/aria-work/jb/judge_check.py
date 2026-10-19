"""Judge checks for the JB plan lines: form, labels, list counts, size, and an in-place render inside The Logic Core."""
import json, random, re, sys
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/spec/frozen')
import aria_budget as ab  # noqa: E402

CC = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
FORBID = ("OOC, Scene, Knows, Mode, Voice, Move, Fate, Bonds, Ledger, Fresh, Check, Person, Replies, Filler, Gemini, "
          "Contrast, Negation runs, Flow, Card details, Echo, Repeats, Bodies, Layers, Tally, Pushback, Restate, Joins").split(', ')


def lists_in(fragment):
    """Rough list finder: split a fragment on commas, then count or/and items in the final chunk of each run.
    Prints the chunks so a human can count real lists; returns comma-chunk count and every or/and pair."""
    chunks = [c.strip() for c in fragment.split(',')]
    joins = re.findall(r'\b(\w[\w-]*) (?:or|and) (\w[\w-]*)', fragment)
    return chunks, joins


def check(name, lines):
    print('=' * 30, name)
    joined = '\n'.join(lines)
    print(f'lines {len(lines)} | chars {len(joined)} | tokens {len(joined) / 4}')
    assert len(lines) in (2, 4), 'line count'
    assert len(joined) / 4 <= 130, 'over 130 tokens'
    for l in lines:
        m = re.match(r'^- ([A-Z][A-Za-z ]*): ', l)
        assert m, l
        lab = m.group(1)
        assert lab not in FORBID, lab
        body = l[m.end():]
        frags = body.rstrip('.').split('; ')
        print(f'  [{lab}] {len(frags)} fragments' + ('  <-- THREE' if len(frags) == 3 else ''))
        for f in frags:
            chunks, joins = lists_in(f)
            print(f'     - {f}\n         comma chunks: {len(chunks)} | or/and pairs: {joins}')
        assert '"' not in l and '::' not in l, 'quote or ::'
        assert not re.search(r'\{\{(?!user\}\})', l) and not re.search(r'(?<!\{\{user)\}\}', l), 'stray braces'
    return joined


def render_in_logic_core(joined, n):
    d = json.load(open(CC, encoding='utf-8'))
    lc = next(p for p in d['prompts'] if p['identifier'].startswith('15b770cf'))['content']
    counter_old = '{{#if .ariaLedgerLine}}{{addvar::logicCoreLines::1}}{{/if}}{{#if .ariaHoldLine}}'
    counter_new = counter_old.replace('{{#if .ariaHoldLine}}', '') + '{{#if .ariaJb}}{{addvar::logicCoreLines::{{getvar::ariaJbLines}}}}{{/if}}{{#if .ariaHoldLine}}'
    assert lc.count(counter_old) == 1
    lc = lc.replace(counter_old, counter_new)
    print_old = '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}- Fresh:'
    print_new = '{{#if .ariaLedgerLine}}{{getvar::ariaLedgerLine}}\n{{/if}}{{#if .ariaJb}}{{getvar::ariaJb}}\n{{/if}}- Fresh:'
    assert lc.count(print_old) == 1
    lc = lc.replace(print_old, print_new)
    adult = next(p for p in d['prompts'] if p['identifier'] == 'nsfw')['content']
    fate = next(p for p in d['prompts'] if p['identifier'].startswith('acc2177a'))['content']
    jb = '{{#if .ariaModeLine}}{{setvar::ariaJbLines::%d}}{{setvar::ariaJb::%s}}{{/if}}' % (n, joined)
    state = {}
    rng = random.Random(1)
    for src in (adult, fate, jb):
        ab.render(src, state, rng)
    out = ab.render(lc, state, rng)
    out = re.sub(r'^\{\{//.*?\}\}', '', out, flags=re.S)
    plan = out[out.index('<logic_core>'):]
    print(plan[:plan.index('- go') + 4])
    print('ariaJb rendered chars', len(state['ariaJb']), '-> checker tokens', ab.tokens(state['ariaJb']))
    # without Adult Context: nothing prints and the count stays put
    state2 = {}
    for src in (fate, jb):
        ab.render(src, state2, random.Random(1))
    out2 = ab.render(lc, state2, random.Random(1))
    assert 'Frank' not in out2 and state2.get('ariaJb', '') == ''
    print('without Adult Context: no JB lines, logicCoreLines =', state2['logicCoreLines'], '| with:', state['logicCoreLines'])


if __name__ == '__main__':
    draft = json.load(open('/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/jb/draft.json', encoding='utf-8'))
    check('DRAFT', draft['lines'])
    cand = json.load(open(sys.argv[1], encoding='utf-8')) if len(sys.argv) > 1 else None
    if cand:
        j = check('CANDIDATE', cand)
        render_in_logic_core(j, len(cand))
