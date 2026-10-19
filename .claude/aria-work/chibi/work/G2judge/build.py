"""Build a G2 candidate from line definitions in a spec module (cand_*.py), keeping the draft's macro frame."""
import json, sys, importlib.util
sys.path.insert(0, '/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA/.claude/aria-work/chibi/work/G2judge')
from paths import *

def load_spec(p):
    spec = importlib.util.spec_from_file_location('cand', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def build(spec_path, out_path):
    c = load_spec(spec_path)
    d = json.load(open(DRAFT, encoding='utf-8'))
    codex = d['prompts'][CODEX]['content']
    gate = d['prompts'][GATE]['content']
    tcg = d['tc']['post_history_gate']
    # --- Codex: comment, setvars, body
    head, rest = codex.split('{{trim}}\n', 1)
    comment = c.CODEX_COMMENT if getattr(c, 'CODEX_COMMENT', None) else head
    body = ('{{setvar::ariaEchoGate::' + c.ECHO + '}}{{setvar::ariaChopGate::' + c.CHOP + '}}<anti_slop>\n'
            + '\n'.join(c.CODEX_LINES) + '\n</anti_slop>')
    new_codex = comment + '{{trim}}\n' + body
    # --- Gate: replace the own-line block between the header and the first print, etc.
    def swap_gate(g):
        for old, new in c.GATE_SWAPS:
            n = g.count(old)
            assert n == 1, (old, n)
            g = g.replace(old, new)
        return g
    new_gate = swap_gate(gate)
    if getattr(c, 'GATE_COMMENT', None):
        gh, gr = new_gate.split('{{trim}}\n', 1)
        new_gate = c.GATE_COMMENT + '{{trim}}\n' + gr
    new_tcg = swap_gate(tcg)
    d['prompts'][CODEX]['content'] = new_codex
    d['prompts'][GATE]['content'] = new_gate
    d['tc']['post_history_gate'] = new_tcg
    json.dump(d, open(out_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return d

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
