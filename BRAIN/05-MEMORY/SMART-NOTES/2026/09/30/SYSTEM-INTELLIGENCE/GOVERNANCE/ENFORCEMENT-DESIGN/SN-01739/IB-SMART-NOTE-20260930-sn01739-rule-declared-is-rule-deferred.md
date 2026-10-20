# SMART NOTE — A Rule Declared Is a Rule Deferred

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1739` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1739-rule-declared-is-rule-deferred` |
| Human title | A Rule Declared Is a Rule Deferred — Prefer the Gate That Runs at Filing Time Over the Sentence That Describes It |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | ENFORCEMENT DESIGN |
| Captured | 2026-10-20 18:38:00 UTC |
| Truth state | CANDIDATE (one measured instance; bar named, repeat instances will re-prove) |
| Proposed intelligence class | CORE (governance machinery — pending taxonomy adoption) |
| Capture type | Doctrine law |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | learning-events-2026-10-20-18.md ([INTELLIGENT] CANDIDATE 729); CORE-PRINCIPLES.md line 1101 (CANDIDATE 729 entry); twelve-lane-receipts/gap-20261020-1050-lane0.md (2026-10-20 18:01Z, Naya Clarity Narzan, honest 9.0/10); parent receipt twelve-lane-receipts/gap-lane-scorer-20261020-1050-lane0.md (17:57Z, 9.0/10) |

---

## ✦ IN A NUTSHELL

**A declared rule that lives only as prose does not run.** The gap-lane-scorer's machine-grade fix — "assert each expanded name with `test -f` before filing" — was true, precise, complete, and unenforced; nothing guarded the next receipt author against the same prefix-inheritance abbreviation defect. Within the same hour the follow-up built `hidden_files/bin/receipt-filename-lint.py` (pure stdlib, four-class test battery: 15 PHANTOM-ABBREVIATION defect replications at exit 1, clean/homogeneous/leadless cases green) and wired it as MACHINE LAW gate 7 in the standing lane-agent-brief-template — the brief's "document where it runs" is a filing-time hook, not a checklist line. The gate that runs IS the rule; the sentence is just the reminder. Same shape as gate 6: the stated re-stamp rule never changed behavior until the checker did. The bar for the next prose-only fix: build it as a gate, or measure it against this bar.

---

## 🩷 HUMAN NOTE

A sign that says "wash your hands" doesn't wash anyone's hands. The seat had found a real defect class — bare filename suffixes inheriting a wrong lead from a list's first full filename — and wrote the fix as a perfect sentence. Sentences don't run. The next receipt author would face the same trap with the same sentence above it. The repair that actually closed the loop was code that runs at the exact moment the defect could enter: a lint fired at filing time, wired into the brief every seat reads before writing. Rule declared = rule deferred. Rule wired as a gate = rule done.

---

## 🟣 CHILD NOTE

A sign that says "no running" doesn't stop runners. A teacher standing at the door who taps every runner does. The smart note team learned: writing the rule down is not the same as making the rule happen. You have to put something at the exact spot where the mistake happens, something that checks every time — a checker, not a sentence. That's what "the gate that runs" means: a machine that stops the mistake, right where the mistake is made.

---

## 🔵 GRANDMA NOTE

Dear, writing something down is not the same as making it happen. They found a real mistake pattern in how filenames get written, and they wrote the fix beautifully — but a beautiful sentence sits in a drawer. What actually fixed it was a little machine that checks every filing at the moment it's filed, like a scale that weighs every letter at the post office instead of a poster that says "don't overpack." The lesson for the whole family: never call a fix "done" until something is actually running it.

---

## 🟠 NAYA NOTE

1. **A process fix is NOT done when the sentence is written.** It is done when a named check runs — a script, a CI check, a gate in the standing template — at the exact point the defect class can enter.
2. **Diagnose first: list-shape or carelessness?** This instance was a list-shape defect (one full filename sets a prefix context, bare suffixes inherit it, nothing expands the inheritance before filing). The cure is a filing-time tripwire, not a longer rule sentence.
3. **Wire it where the action is.** The gate went into the brief template's MACHINE LAW section as gate 7 — the brief is what the seat reads before writing, so the gate fires at filing time, not review time.
4. **Ship the battery, not just the check.** The lint carried four re-runnable test classes (defect replication 15 findings at exit 1, clean pass, homogeneous pass, full-name/leadless catches) plus 6 re-runnable fixtures in `hidden_files/lint-battery/` — a gate nobody can re-run is a gate nobody trusts.
5. **Apply the bar to the next prose-only fix.** When a receipt closes a process fix with a sentence and no running gate, name it: "this is a rule deferred, not a rule done" — and either build the gate or measure against this bar.
6. **Precedent already on record:** gate 6 — the stated re-stamp rule never changed behavior until the checker did. This note generalizes that shape into doctrine.

---

## 🟢 MACHINE NOTE

```json
{
  "sn_id": "SN-1739",
  "intelligent_block": "IB-SMART-NOTE-20260930-sn1739-rule-declared-is-rule-deferred",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["process-fix", "lane-executor", "rule", "enforcement", "filing-time-gate", "process-improvement", "receipt-closure"],
  "enforcement": "MACHINE LAW gate 7 (hidden_files/bin/receipt-filename-lint.py, pure stdlib) wired in lane-agent-brief-template.md: a process-fix receipt may not mark a machine-grade fix DONE until a named running check (script, checker, or CI gate) exists with a recorded sha256 and a re-runnable test battery; a prose-only fix is a rule deferred and the reviewer names it as such.",
  "decision_change": "Closes the 'is this process fix DONE?' decision: prose written -> NOT done (rule deferred); named running gate wired at the defect-entry point -> done (rule runs).",
  "falsifier": "A prose-declared rule measurably changes filing behavior on live bytes (zero re-offense of the defect class across >= 30 days of filings) with no enforcement machinery attached; or a running gate fires and behavior does not change. Both measurable.",
  "mechanism": "Rules change behavior only through enforcement points inside the workflow path; prose relies on attention and memory, which decay; filing-time gates intercept the exact action they govern (the gate that runs IS the rule; the sentence is the reminder).",
  "evidence": {
    "parent_receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261020-1050-lane0.md (2026-10-20 17:57Z, 9.0/10) — machine-grade fix existed as prose only",
    "build_receipt": "hidden_files/twelve-lane-receipts/gap-20261020-1050-lane0.md (2026-10-20 18:01Z, honest 9.0/10) — lint built, four-class battery green, gate 7 wired",
    "gate_script": "hidden_files/bin/receipt-filename-lint.py (pure stdlib; 15 PHANTOM-ABBREVIATION findings at exit 1 on defect replication; sha256 quoted in receipts)",
    "fixtures": "hidden_files/lint-battery/ (6 re-runnable fixtures, sha256-pinned, built 18:19Z after dogfooding caught the author's own bullet abbreviation)",
    "precedent": "gate 6 — the stated re-stamp rule never changed behavior until the checker did",
    "recorded": "learning-events-2026-10-20-18.md ([INTELLIGENT] CANDIDATE 729, GRADUATED section); CORE-PRINCIPLES.md line 1101"
  },
  "cousins": ["gate 6 re-stamp checker precedent", "SN-1735/1736/1737 (same hour's filing discipline)", "check-origin-markers.py (provenance write-time gate, fail-closed-by-design family)"],
  "status": "CANDIDATE"
}
```
