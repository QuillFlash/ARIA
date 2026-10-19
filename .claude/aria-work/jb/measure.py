import re, sys, json
FORBIDDEN = "OOC, Scene, Knows, Mode, Voice, Move, Fate, Bonds, Ledger, Fresh, Check, Person, Replies, Filler, Gemini, Contrast, Negation runs, Flow, Card details, Echo, Repeats, Bodies, Layers, Tally, Pushback, Restate, Joins".split(', ')
# other labels already used in ARIA's rendered text (gate / codex / engine lines)
USED = "Speech Voice Flow Delivery Depth Mood Lulls Demands Runs Kept Recorded Reactions Introductions Humour Register Work Cadence Vocabulary Senses Own words Chop Count Balance Paragraphs Card Narration Secrets People Knows POV Fate World Ambitions Tier Source Form Cells Quiet Bullets Ledger Method Banned Approval Repairs Native reasoning Go go".split()
def check(lines):
    txt = '\n'.join(lines)
    n = len(txt)
    print('chars', n, 'tokens', n/4, 'ok<=130' if n/4 <= 130 else 'OVER')
    for l in lines:
        m = re.match(r'^- ([^:]+): ', l)
        assert m, l
        lab = m.group(1)
        flag = []
        if lab in FORBIDDEN: flag.append('FORBIDDEN')
        if lab in USED: flag.append('used elsewhere')
        print(f'  [{len(l):3}] {lab} {flag}')
        if '::' in l: print('   !! contains ::')
        body = l.replace('{{user}}', '')
        if '{{' in body or '}}' in body: print('   !! stray braces')
        if '"' in l or "'" in l.replace("'s", '').replace("n't", ''): print('   !! quote char:', [c for c in l if c in '"\''][:6])
        if '<' in l or '>' in l: print('   !! angle bracket')
    return n
if __name__ == '__main__':
    lines = json.load(open(sys.argv[1]))
    check(lines)
