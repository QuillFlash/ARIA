#!/usr/bin/env python3
"""Regenerate ARIA's ready-made model configs from their Base presets.

Every file in presets/<format>/<model folder>/ is a Base preset with a few settings of its own. This script keeps
those settings and takes everything else from the matching Base file (same format, same edition: full or Chibi), so
a change to a Base reaches every config in one run:

  Chat Completions   the config keeps its connection settings (every top-level key besides prompts and prompt_order)
                     and the ON/OFF state of each entry; entries the config has never seen take the Base's state.
  Text Completions   the config keeps its name (both name fields, plus the README line that quotes it) and its
                     {{.aria-* = on/off}} switch values; switches it has never seen take the Base's value.
  Marinara           the config keeps its name, its default choices and the ⚙️ paragraph that opens its
                     description; the rest of the description, the sections, groups and choice blocks come from
                     the Base. CHOICE_MIGRATIONS renames retired choice values.

Usage: python3 tools/regen_configs.py           rewrite every config whose regenerated form differs
       python3 tools/regen_configs.py --check   only list the configs that would change (exit 1 if any)

Run tools/aria_budget.py and tools/marinara_parity.py on the Base files first; a config is only as good as its Base.
"""
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRESETS = ROOT / 'presets'
SWITCH = re.compile(r'\{\{\.(aria-[\w-]+) = (on|off)\}\}')
# Marinara choice values that were renamed, old -> new, per choice variable.
CHOICE_MIGRATIONS = {
    'logic_core': {'MICRO': 'JAILBREAK'},
}
# Option labels a Marinara config's own ⚙️ paragraph may still use, old -> new (the Chat Completions entry names).
LABEL_MIGRATIONS = [
    ('🏷️ Think Tags', '🏷️ Logic Core Tags'),
    ('✂️ Reduce Reasoning', 'Reduce Reasoning'),
    ('picks 🩹 Gemini and', 'picks 🩹 Gemini All-In-One and'),
]


def _version(name):
    m = re.search(r'(\d+(?:\.\d+)+)', name)
    return tuple(int(x) for x in m.group(1).split('.')) if m else ()


def bases(fmt):
    """{'full': path, 'chibi': path} for one format, the highest version of each edition in its Base folder."""
    out = {}
    for f in (PRESETS / fmt / 'Base').iterdir():
        if f.suffix != '.json' or ' — ' not in f.name:
            continue
        edition = 'chibi' if 'Chibi Edition' in f.name else 'full'
        if edition not in out or _version(f.name) > _version(out[edition].name):
            out[edition] = f
    return out


def configs(fmt):
    for f in sorted((PRESETS / fmt).rglob('*.json')):
        if f.parent.name != 'Base':
            yield f


def dump(obj, like):
    """Serialise the way the repository's files are written: the indent and key order of the file being replaced."""
    text = like.read_text(encoding='utf-8') if like.exists() else ''
    indent = 4 if text.startswith('{\n    "') else 2 if text.startswith('{\n  "') else None
    out = json.dumps(obj, ensure_ascii=False, indent=indent, separators=(',', ':') if indent is None else None)
    return out + ('\n' if text.endswith('\n') else '')


# ---------------------------------------------------------------- per format

def regen_cc(base, cfg):
    new = copy.deepcopy(base)
    for key, value in cfg.items():
        if key not in ('prompts', 'prompt_order'):
            new[key] = copy.deepcopy(value)
    state = {}
    for block in cfg.get('prompt_order', []):
        for row in block['order']:
            state[(block['character_id'], row['identifier'])] = row['enabled']
    for block in new['prompt_order']:
        for row in block['order']:
            row['enabled'] = state.get((block['character_id'], row['identifier']), row['enabled'])
    return new


TC_NOTE = re.compile(r' ⚙️ This copy is for [^}]*?(?=\}\})')  # a config's own note inside the switch block's intro
TC_NOTE_ANCHOR = "Each line's note says what it does."


def regen_tc(base, cfg):
    new = copy.deepcopy(base)
    base_name, cfg_name = base['sysprompt']['name'], cfg['sysprompt']['name']
    new['context']['name'] = cfg['context']['name']
    new['sysprompt']['name'] = cfg_name
    switches = dict(SWITCH.findall(cfg['sysprompt']['content']))
    note = TC_NOTE.search(cfg['sysprompt']['content'])
    for field in ('content', 'post_history'):
        text = new['sysprompt'][field].replace(base_name, cfg_name)
        if note and field == 'content':
            if TC_NOTE_ANCHOR not in text:
                raise ValueError(f'{cfg_name}: the Base lost the anchor for the config note')
            text = text.replace(TC_NOTE_ANCHOR, TC_NOTE_ANCHOR + note.group(0), 1)
        new['sysprompt'][field] = SWITCH.sub(
            lambda m: '{{.%s = %s}}' % (m.group(1), switches.get(m.group(1), m.group(2))), text)
    return new


def regen_marinara(base, cfg):
    new = copy.deepcopy(base)
    p, c = new['data']['preset'], cfg['data']['preset']
    p['name'] = c['name']
    own = c['description'].split('\n\n', 1)[0] if c['description'].startswith('⚙️') else ''
    for old, new_label in LABEL_MIGRATIONS:
        own = own.replace(old, new_label)
    p['description'] = (own + '\n\n' + p['description']) if own else p['description']
    choices = json.loads(c['defaultChoices'])
    for var, renames in CHOICE_MIGRATIONS.items():
        if var in choices and choices[var] in renames:
            choices[var] = renames[choices[var]]
    known = {cb['variableName']: {o['value'] for o in json.loads(cb['options'])} for cb in new['data']['choiceBlocks']}
    base_choices = json.loads(p['defaultChoices'])
    for var, value in list(choices.items()):
        values = value if isinstance(value, list) else [value]
        if var not in known or any(v not in known[var] for v in values):
            raise ValueError(f'{c["name"]}: default choice {var}={value} is not an option of the Base')
    for var, value in base_choices.items():
        choices.setdefault(var, value)
    p['defaultChoices'] = json.dumps(choices, ensure_ascii=False, separators=(',', ':'))
    return new


REGEN = {'Chat Completions': regen_cc, 'Text Completions': regen_tc, 'Marinara Engine Edition': regen_marinara}


def main():
    check = '--check' in sys.argv
    changed = []
    for fmt, fn in REGEN.items():
        if not (PRESETS / fmt / 'Base').is_dir():
            continue
        edition_bases = {k: json.loads(v.read_text(encoding='utf-8')) for k, v in bases(fmt).items()}
        for f in configs(fmt):
            cfg = json.loads(f.read_text(encoding='utf-8'))
            base = edition_bases['chibi' if 'Chibi Edition' in f.name else 'full']
            text = dump(fn(base, cfg), f)
            if text != f.read_text(encoding='utf-8'):
                changed.append(f)
                if not check:
                    f.write_text(text, encoding='utf-8')
    verb = 'would change' if check else 'regenerated'
    for f in changed:
        print(f'{verb}: {f.relative_to(ROOT)}')
    print(f'{len(changed)} config(s) {verb}')
    sys.exit(1 if (check and changed) else 0)


if __name__ == '__main__':
    main()
