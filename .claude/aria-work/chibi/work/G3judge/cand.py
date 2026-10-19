"""Apply wording edits (old -> new, each must occur exactly once in the shared body) to the G3 draft and measure."""
import json, random, sys
S = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work"
sys.path.insert(0, S + "/spec/frozen")
import aria_budget as ab
D = json.load(open(S + "/chibi/drafts/G3.json", encoding='utf-8'))
P, T = '15b770cf-6049-5f3b-b25d-be09728a65d5', '591b8c15-985e-59f1-8c90-59e7cae236ae'
TAGS = {"ariaThinkOpen": "<thinking>", "ariaThinkClose": "</thinking>"}

def apply(text, edits):
    for old, new in edits:
        n = text.count(old)
        assert n == 1, (old, n)
        text = text.replace(old, new)
    return text

def build(edits):
    d = json.loads(json.dumps(D))
    for pid in (P, T):
        d['prompts'][pid]['content'] = apply(d['prompts'][pid]['content'], edits)
    d['tc']['post_history_logic_core'] = apply(d['tc']['post_history_logic_core'], edits)
    return d

def rend(text, st):
    st = dict(st)
    return ab.render(text, st, random.Random(1))

def measure(d, show=False):
    c = d['prompts'][P]['content']
    off, on = rend(c, {}), rend(c, TAGS)
    tc = rend(d['tc']['post_history_logic_core'], {"aria-logic-core": "on"})
    if show:
        print(off); print(); print(on); print()
    return len(off), ab.tokens(off), len(on), ab.tokens(on), ab.tokens(tc)

if __name__ == '__main__':
    print('draft', measure(D))
