#!/bin/bash
# Re-sync Chibi Marinara from the Chibi CC file and run every check. Run from anywhere.
set -e
R="/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
W="$R/.claude/aria-work"
CCF="$R/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition (Chat Completions).json"
MARF="$R/Aria's Realistic Intelligence Assistance 1.0 — Chibi Edition — Agent Gating.json"
cd "$W/build/chibi_mar"
echo "Chibi CC sha256: $(sha256sum "$CCF" | cut -c1-16)"
python3 selftest.py
python3 -c "import selftest; selftest.comment_rules_test()"
python3 build_chibi_mar.py
python3 agents_cost.py
python3 agents_equiv.py
cd "$W/mar"
echo "--- compare.py --full (Chibi CC vs Chibi Marinara)"
python3 compare.py --full --cc-file "$CCF" --mar "$MARF" | tail -20
echo "--- verify.py --mar (Chibi Marinara)"
python3 verify.py --mar "$MARF"
echo "--- compare.py --full (ARIA, defaults)"
python3 compare.py --full | tail -20
echo "--- verify.py (ARIA, defaults)"
python3 verify.py
