import sys
sys.path.insert(0, '.')
import importlib, final_texts as F
importlib.reload(F)

def tc_segments():
    # TC wrapper keeps the source's whitespace: Time and Fate blocks end with a newline before {{/if}}; Bonds ended with the closing tag,
    # so without it the block needs its own closing newline (the next module's text follows {{/if}} directly).
    time_seg = F.TIME_BODY + "\n"
    fate_seg = F.FATE_SETVARS + "\n".join(F.FATE_LINES) + "\n"
    bonds_seg = F.BONDS_SETVARS.rstrip("\n") + "\n" + "\n".join(F.BONDS_LINES) + "\n"
    return time_seg, fate_seg, bonds_seg

if __name__ == '__main__':
    ts, fs, bs = tc_segments()
    open('tc_time_draft.txt', 'w', encoding='utf-8').write(ts)
    open('tc_fate_draft.txt', 'w', encoding='utf-8').write(fs)
    open('tc_bonds_draft.txt', 'w', encoding='utf-8').write(bs)
    print('written')
