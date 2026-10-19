"""Helpers for the Fix 3 regex tests: JS regex scripts run through Python re the way SillyTavern runs them, and real renders
of ARIA TC's Logic Core, Chibi TC's Logic Core (G3.json) and the historic (pre beta 7) Logic Core."""
import copy
import importlib.util
import json
import random
import re

R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
W = R + "/.claude/aria-work"
CCFILE = R + "/Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
TCFILE = R + "/Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
RXFILE = R + "/regex/ARIA 1.0 Regex Scripts (Text Completions).json"
SNAP_CC = W + "/build/orig/CC.json"
SNAP_RX = W + "/build/orig/TCregex.json"
OLD_TC = W + "/build/tc_before_ece78b2.json"   # the TC preset as it stood before beta 7: the old closing sentence
G3 = W + "/chibi/final/G3.json"


def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ab = load_mod(R + "/tools/aria_budget.py", "ab_live")


# ------------------------------------------------------------------ JS regex scripts through Python

def conv(find):
    """'/pattern/flags' (JS) -> (compiled python regex, is_global)."""
    m = re.match(r'^/(.*)/([a-z]*)$', find, re.S)
    assert m, find[:60]
    pat, fl = m.groups()
    flags = 0
    for ch in fl:
        if ch == 'i':
            flags |= re.I
        elif ch == 'm':
            flags |= re.M
        elif ch == 's':
            flags |= re.S
        elif ch == 'g':
            pass
        else:
            raise ValueError(f'unhandled flag {ch}')
    return re.compile(pat, flags), 'g' in fl


def sub_js(script, text):
    """One regex script on a text: SillyTavern replaces $n by group n (empty when the group did not take part)."""
    rx, is_global = conv(script['findRegex'])
    repl = script.get('replaceString') or ''
    assert not re.search(r'\$(?!\d)', repl), 'replaceString uses a $ form this helper does not model'

    def f(m):
        return re.sub(r'\$(\d+)', lambda g: (m.group(int(g.group(1))) or '') if int(g.group(1)) <= rx.groups else '', repl)
    return rx.sub(f, text, count=0 if is_global else 1)


def pipeline(scripts, text, placement, mode):
    """Apply the scripts in list order the way SillyTavern's getRegexedString does.
    mode: 'display' (markdownOnly scripts), 'prompt' (promptOnly scripts) or 'save' (scripts with neither flag)."""
    for s in scripts:
        if s['disabled'] or placement not in s['placement']:
            continue
        applies = (mode == 'display' and s['markdownOnly']) or (mode == 'prompt' and s['promptOnly']) or \
                  (mode == 'save' and not s['markdownOnly'] and not s['promptOnly'])
        if applies:
            text = sub_js(s, text)
    return text


# ------------------------------------------------------------------ real renders of the Logic Core

def shipped_switches(preset):
    return dict(ab.SWITCH.findall(preset['sysprompt']['content']))


def overrides_for(preset, config, tags):
    """'lean': shipped plus the Logic Core; 'full': every non-patch switch on, GLM on (the largest patch)."""
    sw = shipped_switches(preset)
    if config == 'lean':
        o = dict(sw)
    else:
        o = {s: 'on' for s in sw if not s.startswith('aria-patch')} | {p: 'off' for p in sw if p.startswith('aria-patch')}
        o['aria-patch-glm'] = 'on'
    o['aria-logic-core'] = 'on'
    o['aria-thinking-tags'] = 'on' if tags else 'off'
    return o


def render_tc_logic_core(preset, overrides, user):
    """The Logic Core exactly as the model receives it: the post-history up to <final_gate>, {{user}} rendered as a name."""
    p = copy.deepcopy(preset)
    p['sysprompt']['content'] = p['sysprompt']['content'].replace('{{user}}', user)
    p['sysprompt']['post_history'] = p['sysprompt']['post_history'].replace('{{user}}', user)
    rendered, state = ab.simulate_tc(p, overrides, seed=1)
    post = rendered['Post-History']
    return post[:post.index('<final_gate>')].strip('\n'), state


def render_chibi_logic_core(g3_text, state, user):
    """G3.json's tc.post_history_logic_core rendered with the variables ARIA TC's system prompt set."""
    return ab.render(g3_text.replace('{{user}}', user), dict(state), random.Random(1)).strip('\n')


def tc_preset(path=TCFILE):
    return json.load(open(path, encoding='utf-8'))


def g3_text():
    return json.load(open(G3, encoding='utf-8'))['tc']['post_history_logic_core']


def plan_lines(lc):
    """The dashed plan lines, from '- OOC' to '- go'."""
    lines = lc.split('\n')
    a = next(i for i, l in enumerate(lines) if l.startswith('- OOC:'))
    b = next(i for i, l in enumerate(lines) if l == '- go')
    return '\n'.join(lines[a:b + 1])
