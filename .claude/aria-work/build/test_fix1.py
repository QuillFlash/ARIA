"""Fix 1 regression test, on in-memory copies only: the new per-patch stale-state check must fail the unfixed CC and pass the fixed one."""
import contextlib
import importlib.util
import io
import json
import sys

R = "/home/theaestheticfur/Fejlesztés/SillyTavern/ARIA"
W = R + "/.claude/aria-work"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(mod, preset, filename):
    with contextlib.redirect_stdout(io.StringIO()):
        totals, errors = mod.analyse_cc(preset, filename)
    return totals, errors


new = load(R + "/tools/aria_budget.py", "budget_new")
old = load(W + "/build/orig/aria_budget.py", "budget_old")

FILE = "Aria's Realistic Intelligence Assistance 1.0 — (Chat Completions).json"
raw_unfixed = open(W + "/build/orig/CC.json", encoding="utf-8", newline="").read()
assert "gemini38Patch::}}" not in raw_unfixed, "snapshot is not the unfixed file"

# the in-memory fix: append the blank after ariaJbLines in the Main Prompt's blanking run (JSON text has no escapes in it)
anchor = "{{setvar::ariaJbLines::}}\\n{{trim}}\\nYou are the narrator"
assert raw_unfixed.count(anchor) == 1, raw_unfixed.count(anchor)
raw_fixed = raw_unfixed.replace(anchor, "{{setvar::ariaJbLines::}}{{setvar::gemini38Patch::}}\\n{{trim}}\\nYou are the narrator")
assert raw_fixed != raw_unfixed

unfixed = json.loads(raw_unfixed)
fixed = json.loads(raw_fixed)

ok = True

_, e_old_unfixed = run(old, unfixed, FILE)
print("old checker on the UNFIXED copy:", "passes (blind spot confirmed)" if not e_old_unfixed else f"errors: {e_old_unfixed}")
ok &= not e_old_unfixed

_, e_new_unfixed = run(new, unfixed, FILE)
print("new checker on the UNFIXED copy:", len(e_new_unfixed), "error(s)")
for e in e_new_unfixed:
    print("   -", e)
hit = [e for e in e_new_unfixed if "gemini38Patch" in e]
ok &= bool(hit)
print("   names gemini38Patch:", bool(hit))
others = [e for e in e_new_unfixed if "gemini38Patch" not in e]
print("   other errors (other unblanked variables or anything else):", others)
ok &= not others

_, e_new_fixed = run(new, fixed, FILE)
print("new checker on the FIXED copy:", "passes" if not e_new_fixed else f"errors: {e_new_fixed}")
ok &= not e_new_fixed

# ---- the same per-patch check on TC, on a synthetic in-memory leak: GLM sets an unblanked variable, Kimi / Qwen prints it
TC_FILE = "Aria's Realistic Intelligence Assistance 1.0 — (Text Completions).json"
tc_raw = open(R + "/" + TC_FILE, encoding="utf-8", newline="").read()
tc = json.loads(tc_raw)
sysc = tc["sysprompt"]["content"]
a_glm, a_kimi = "{{#if .aria-patch-glm}}", "{{#if .aria-patch-kimi-qwen}}"
assert sysc.count(a_glm) == 1 and sysc.count(a_kimi) == 1
leaky = json.loads(json.dumps(tc))
leaky["sysprompt"]["content"] = sysc.replace(a_glm, a_glm + "{{setvar::zzLeak::from glm}}").replace(a_kimi, a_kimi + "{{#if .zzLeak}}{{getvar::zzLeak}}{{/if}}")


def run_tc(mod, preset):
    with contextlib.redirect_stdout(io.StringIO()):
        return mod.analyse_tc(preset, TC_FILE)


_, e_tc_real = run_tc(new, tc)
print("new checker on the real TC:", "passes" if not e_tc_real else f"errors: {e_tc_real}")
ok &= not e_tc_real
_, e_tc_old = run_tc(old, leaky)
print("old checker on the synthetic TC leak:", "passes (blind spot)" if not [e for e in e_tc_old if "zzLeak" in e] else e_tc_old)
_, e_tc_new = run_tc(new, leaky)
hit = [e for e in e_tc_new if "zzLeak" in e and "aria-patch-kimi-qwen" in e and "stale" in e]
print("new checker on the synthetic TC leak:", hit or e_tc_new)
ok &= bool(hit) and not [e for e in e_tc_old if "stale" in e]

print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
