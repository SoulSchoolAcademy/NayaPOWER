# Derive the Re-Stamp Contract from the Generator's Reads — Docstrings Drift, Read Sites Don't

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1680-derive-re-stamp-contract-from-generator-reads-docstrings-drift-read-sites-dont
**Smart Note:** SN-1680
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A re-stamp trigger contract — "which changes require regenerating artifact X" — is derived from the generator's actual read surface, never from its docstring or its declared field list. The t0903 technique (2026-10-19): read the full generator source (606 lines); exhaustively grep every read primitive (`git(`, `read_text`, `show_file`, `ls-tree`, `open(`, `glob`, `walk`, `iterdir`) → enumerate every read site (R1–Rn, exactly 6); mechanically extract every path-like string from the pointer-bearing JSONs — because declared POINTER_FIELDS lists miss fields (t0903 found `decision_calculus.object_path` and `graph_binding` in MASTER-INDEX.json absent from the declared list). Each trigger and false-trigger gets a one-line derivation: line number + what it reads. The mechanism: docstrings say what the code should do; read sites are what it does. Drift lives in prose, not in code.

## 🩷 HUMAN NOTE

If you want to know what a machine listens to, don't read the manual — read the wiring. The manual drifts when someone rewrites it; the wires only change when someone changes them. A list of "things that require rebuilding the house" written from the wiring is right even when the manual is three editions old.

## 🟣 CHILD NOTE

To know what ingredients a recipe really needs, watch the cook's hands — not the recipe card. The card might be old and missing a step. The hands never lie: whatever the cook picks up is what the dish needs.

## 🔵 GRANDMA NOTE

Promises about a tool come and go, but the tool's own behavior doesn't change until someone rebuilds it. If you write down exactly what the tool touches — every shelf it reaches for — your list of "when to replace it" will stay honest long after the instruction booklet goes stale.

## 🟠 NAYA NOTE

The concrete instance: t0903-lane10.md (2026-10-19, 9.5/10) built `hidden_files/brain-index-trigger-list-t0903.md` — the input contract answering "which changes require a brain-index re-stamp." Method: tip-hunted past 30+ stale workspace clones to the live tip `1a1c22d3…`; read all 606 lines of `tools/regenerate_brain_index.py` (blob `41daba756288530a00f2542bff525c2d6438a35c`); ran an exhaustiveness grep over read primitives → exactly 6 read sites (R1–R6), nothing else; read the gate wrapper `tools/protocol/checks/brain_index_freshness.py` (pure wrapper, adds no new read surface); mechanically walked both pointer-bearing JSONs at tip and found backstop extras the declared POINTER_FIELDS list misses (`decision_calculus.object_path`, `decision_calculus.graph_binding` in MASTER-INDEX.json); byte-verified every declared + backstop target resolves at tip via `git ls-tree`. Output: 4 triggers (T1 BRAIN/**, T2 pointer-target deletion = the L543 repair class, T3 generator itself, T4 gate wrapper) + 7 false-triggers (F1–F7), each one-line derived. Two honesty marks: the falsifier was split into read-surface staleness vs tree-health, and `--check` at tip was marked UNVERIFIED (read-only authority) instead of asserted.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1680",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "a re-stamp trigger contract ('which changes require regenerating X') must be derived from the generator's actual read surface — exhaustive grep over every read primitive (git(, read_text, show_file, ls-tree, open(, glob, walk, iterdir), enumerating every read site R1..Rn, plus mechanical extraction of every path-like string from pointer-bearing JSONs — never from the docstring or the declared field list, which drift; each trigger/false-trigger carries a one-line derivation (line number + what it reads)",
  "decision_change": "any lane writing a re-stamp / regeneration trigger contract will (1) quote the generator's blob SHA, (2) run the read-primitive exhaustiveness grep and enumerate R1..Rn, (3) mechanically extract path-like strings from pointer JSONs rather than trusting declared field lists — instead of summarizing the docstring into triggers",
  "falsifiability": "a contract derived this way that misses a real trigger — a generator read the grep's read-primitive set failed to capture — would falsify the exhaustiveness claim; a drift incident whose root cause is a declared field list or docstring statement contradicting the actual reads would falsify 'drift lives in prose, not in code'",
  "mechanism": "docstrings and declared field lists are maintained by humans and drift from the code; read sites are maintained by execution and cannot drift without behavior change — the grep enumerates the generator's true input set, and mechanical path extraction catches the undeclared fields (e.g. decision_calculus.object_path / graph_binding missed by POINTER_FIELDS) that the prose authors forgot",
  "applies_when": [["generator","freshness-contract"], ["index","re-stamp"], ["verification","read-surface"]],
  "enforcement": "re-stamp contract review rejects any trigger list that cites no generator blob SHA and no read-site enumeration (R1..Rn); a contract whose derivation quotes only the docstring or a declared field list is bounced back for read-surface derivation. Check runs on every re-stamp contract before it becomes a wired contract.",
  "evidence": "hidden_files/twelve-lane-receipts/t0903-lane10.md (2026-10-19, 9.5/10): brain-index-trigger-list-t0903.md derived from tools/regenerate_brain_index.py (blob 41daba756288530a00f2542bff525c2d6438a35c, 606 lines) — 6 read sites (R1–R6) via read-primitive grep, backstop extras decision_calculus.object_path/graph_binding found by mechanical path extraction despite absence from declared POINTER_FIELDS, all targets byte-verified at tip 1a1c22d3; 4 triggers (T1–T4) + 7 false-triggers (F1–F7), --check at tip marked UNVERIFIED (read-only authority)"
}
~~~
