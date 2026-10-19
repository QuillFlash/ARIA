#!/usr/bin/env python3
"""Strip the Frankenstein crust from the FF5 Micro chain of thought as the user imported it into ARIA: the getvars of RF
modules ARIA doesn't have, the Internal States mechanics (DnD Simulator, the state-update sequence), and the XML tag
references to blocks ARIA doesn't define. Instructions stay word for word; a tag that only labels an instruction loses its
brackets, and a sentence that only points at a missing block goes.

usage: python3 clean.py IN OUT"""
import sys
from pathlib import Path

EDITS = [
    # the comment: ARIA has no Internal States
    (' This has been updated and CAN NOW use internal states.', ''),
    # Task 0: GM's Notebook getvar, DnD Simulator
    ('What is the game state? {{getvar::gmNotebookCoTGamestate}} What is', 'What is the game state? What is'),
    (' If <internal_dndsim> active (skip if not): {{getvar::dndSimCoTHQ1}} First establish/lock task DC perm, then evaluate '
     'rolls later in next task.', ''),
    # Task 1
    ('Are the NPCs not acting like yes-men, as per the instructions of <abolish_yesman_behaviour>?',
     'Are the NPCs not acting like yes-men?'),
    (' If <realist_gemini>, <roleplay_isnt_reality>, <Prefill> and/or <professional_legality> are present, I follow their '
     'instructions to a tee.', ''),
    (' How will I apply <realistic_bold_characters> if present?', ''),
    ('I must list and enforce all <anti_omniscient_NPCs> rules (anti-bridging{{getvar::smellMicroRule}}, sound, thought, '
     'evidence {{getvar::smellMicroCheck}})',
     'I must list and enforce all anti-omniscient NPC rules (anti-bridging, sound, thought, evidence)'),
    (' DND Task Sim (if <internal_dndsim> active): Rolls against locked DC:  User rolls: {{roll::1d20}} | NPC rolls: '
     '{{roll::1d20}}. (Skip if tag not present). I must create response based strictly on deltas of DC, modifiers (if '
     'present), and roll. I will never recalculate delta after this task.', ''),
    ('Mode check first: if <freaky_supremacy> is present, taste-independence, agency friction and <instinct_autonomy_gate> '
     'are SUSPENDED',
     'Mode check first: if Freaky Mode is active, taste-independence, agency friction and instinct autonomy gate are SUSPENDED'),
    ('Otherwise, if <abolish_yesman_behaviour> is active: for any taste', 'Otherwise: for any taste'),
    ('Then <instinct_autonomy_gate>: for any instinct', 'Then instinct autonomy gate: for any instinct'),
    # Task 2: the state updates go, so the title loses them too
    ('2. Modes, Plot & State Updates:', '2. Modes & Plot:'),
    ('If active, how will I apply <adult_mode> logically?', 'If active, how will I apply adult mode logically?'),
    ('Plot Momentum: {{getvar::tempoCoT}} I must', 'Plot Momentum: I must'),
    (' I will update active states in this exact sequence: Increment turn (ct + 1), {{getvar::bondCoT1}}, '
     '{{getvar::agendaTrackerCoT}}, {{getvar::chekhovsGunCoT}}, {{getvar::worldsimCoT}}, {{getvar::gmNotebookCoT}}, '
     '{{getvar::bondCoT2}}, {{getvar::dndSimCoT}}. Skip if none present.', ''),
    # Task 3
    ('What are the <prose_rules>? How will I apply them?', 'What are the prose rules? How will I apply them?'),
    ('How will I enforce <do_not_repeat_descriptions> to omit repeat details from the last 4 messages?',
     'How will I omit repeat details from the last 4 messages?'),
    ('How will I enforce <user_autonomy> and NPC anti-repeat rule?', 'How will I enforce user autonomy and NPC anti-repeat rule?'),
    ('I check every planned word against <banned_vocabulary> without', 'I check every planned word against banned vocabulary without'),
    (' How can I apply <gfx_protocol> if logical?', ''),
    (' I must add <colored_dialogue> if present (retaining established NPC colors).', ''),
    ('What is the response length in <formatting_constraints>?', 'What is the response length?'),
    (' (<say_it_straight>, <break_the_triad>, <resolution_competition>, <emission_limits>).', '.'),
    # Task 4
    ('How will I apply all rules in <npc_voice> to NPCs for legato pacing', 'How will I apply all NPC voice rules to NPCs for legato pacing'),
    ('What is the target dialogue ratio (30-50%) in <npc_voice>?', 'What is the target dialogue ratio (30-50%)?'),
    ('I will calculate <vad_emotion> and <npc_instincts> now', 'I will calculate VAD emotion and NPC instincts now'),
    ('as per the instructions of <scene_engine> and if present, <stall_word_killswitch>.', 'as per the instructions of <scene_engine>.'),
    ('<staccato_chop_killswitch> check: any period', 'Staccato chop killswitch check: any period'),
    ('Then <anti_briefing_register>: does any spoken line', 'Then anti-briefing register: does any spoken line'),
    ('Then <human_vocal_limits>: any animal sound', 'Then human vocal limits: any animal sound'),
    (' If <quant_hardening> is present, I must recheck all of its rules and correct any mistakes that I would have left in my '
     'dialogue otherwise.', ''),
]


def clean(t):
    for old, new in EDITS:
        n = t.count(old)
        if n != 1:
            raise SystemExit(f'expected 1 of {old[:80]!r}, found {n}')
        t = t.replace(old, new)
    return t


if __name__ == '__main__':
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.write_text(clean(src.read_text(encoding='utf-8')), encoding='utf-8')
    print(f'{len(EDITS)} edits applied')
