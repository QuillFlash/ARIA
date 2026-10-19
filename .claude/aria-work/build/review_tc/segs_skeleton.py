import subprocess
from common import *
exec(open('content.py').read().split('# --- 3.')[0].split('# --- 1.')[0])  # helpers only
c, a = load(CHIBI_TC), load(ARIA_TC)
cc_, ac_ = c['sysprompt']['content'], a['sysprompt']['content']
pairs = []
def add(label, A, C):
    pairs.append((label, A, C))
def body(s, tag):
    i = s.index(tag) + len(tag); then, _, end = ab.split_if(s, i); return s[i - len(tag):end]
for sw in ('adult', 'freaky', 'hybrid-pov', 'npc-voice', 'anthro', 'scent', 'time-place', 'fate', 'bonds', 'jailbreak',
           'patch-glm', 'patch-kimi-qwen', 'patch-mimo-pro', 'patch-mimo-flash', 'patch-deepseek', 'character-hold'):
    t = '{{#if .aria-%s}}' % sw; add('block ' + sw, body(ac_, t), body(cc_, t))
add('block flash-gate', body(ac_, '{{if .aria-flash-gate}}'), body(cc_, '{{if .aria-flash-gate}}'))
for s in (ac_, cc_):
    pass
def span(s, a0, b0, inc=True):
    i = s.index(a0); j = s.index(b0, i) + (len(b0) if inc else 0); return s[i:j]
add('main prompt', span(ac_, '{{setvar::ariaDice::}}', '{{getvar::player-instructions}}\n{{/if}}'), span(cc_, '{{setvar::ariaDice::}}', '{{getvar::player-instructions}}\n{{/if}}'))
add('scene engine', span(ac_, '<scene_engine>', '</scene_engine>'), span(cc_, '<scene_engine>', '</scene_engine>'))
add('anti-slop', span(ac_, '{{setvar::ariaEchoGate::- ', '</anti_slop>'), span(cc_, '{{setvar::ariaEchoGate::- ', '</anti_slop>'))
ap, cp = a['sysprompt']['post_history'], c['sysprompt']['post_history']
add('post logic core', ap.split('<final_gate>')[0], cp.split('<final_gate>')[0])
add('post gate', '<final_gate>' + ap.split('<final_gate>')[1], '<final_gate>' + cp.split('<final_gate>')[1])
ok = 0
for label, A, C in pairs:
    fa, fc = OUT / 'seg' / (label.replace(' ', '_') + '.aria.txt'), OUT / 'seg' / (label.replace(' ', '_') + '.chibi.txt')
    fa.write_text(A); fc.write_text(C)
    r = subprocess.run(['python3', str(W / 'spec/skeleton.py'), '--text', str(fa), str(fc)], capture_output=True, text=True)
    print(label.ljust(22), r.stdout.strip().split('\n')[0][:6], '' if r.returncode == 0 else '\n' + r.stdout)
    ok += r.returncode == 0
print(ok, 'of', len(pairs), 'OK')
