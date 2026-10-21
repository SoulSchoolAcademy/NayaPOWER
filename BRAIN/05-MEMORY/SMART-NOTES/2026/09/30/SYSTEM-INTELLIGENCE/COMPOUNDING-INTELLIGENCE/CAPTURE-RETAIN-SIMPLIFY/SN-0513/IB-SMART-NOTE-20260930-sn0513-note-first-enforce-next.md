# Note First, Enforce Next — the Smart-Note Enforcement Rate

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0513-note-first-enforce-next
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6028678714 ([CODA 1] All three delivered, 2026-10-07T01:08:03Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The second of Coda 1's two load-bearing numbers: **21 commits introduced a Smart Note, 3 carried enforcement. Rate: 14.3%** over a 120-commit window. SN-0359, SN-0360, SN-0400, SN-0340, SN-0355, SN-0399, SN-0459 all landed note-only; some were later enforced in follow-ups — SN-0358 is now covered by `test_protected_intelligence_integrity.py`. That is the pattern worth copying and the one Shawn ratified when he said to stop generating notes until a claim is enforced: **note first, enforcement in the next commit, tracked.** This number is the honest answer to "why does the documentation score rise while the behavioural score doesn't move" — writing the lesson down is not the same as wiring it into the machine. Two honesty qualifiers ride with it: the rate is a proxy, not a verdict — it cannot tell whether a note *should* have been enforced, and some notes are correctly documentation-only. And a truth change cannot hide inside a refactor: two claims are currently false (`independent_verification: True` hand-written in a receipt builder with no verifier behind it; the nine-node "ablation" that deletes a key from the dict it just built), recorded in `tools/load-bearing-claims-record.json` with the law each violates. The gate passes only while the violation set **matches** the record — so a new false claim is red, and silently repairing one without updating the record is *also* red. Coda 1 deliberately did not quietly fix them: editing a proof artifact is the owning lane's call, not a coda's unilateral move from an enforcement PR.

## 🩷 HUMAN NOTE

Shawn, the number you asked for: of the last 21 notes we wrote, only 3 got wired into tests that enforce them — 14.3%. Writing things down isn't the same as making them true. Your ratified rule — no more notes until a claim is enforced — is now the pattern: write the note, then in the next commit add the test that makes the lesson impossible to ignore, and track both. The score that matters moves only when the enforcement lands.

## 🟣 CHILD NOTE

Writing "look both ways before crossing" in your notebook is good. But the notebook doesn't stop the car — only your feet do. We checked: we wrote 21 rules, and only 3 of them became actual fences. Now the rule is: every note has to grow up into a fence, and the next change has to build it. Also: if you know something is wrong, you write it on the official list — you don't quietly erase it while nobody's looking.

## 👵 GRANDMA NOTE

Dear, the team found a gap between knowing and doing: 21 lessons written, 3 enforced. Your rule fixed it — a lesson now has to become a standing check in the very next step, and someone tracks that it happened. And they learned honesty goes both ways: two claims they know are wrong stay on the official record until the owner fixes them, because quietly erasing a mistake is its own kind of mistake.

## 💜 NAYA NOTE

This is the compounding mechanism's missing link made measurable. Capture ≠ enforcement, and now we can watch the gap as a number. For every Smart Note you stage: (1) decide in the same tick whether it needs enforcement (a test, a gate, a mechanical check) or is correctly documentation-only — record the decision; (2) if enforcement is due, land it in the next commit and name the note it enforces; (3) if a proof artifact is found to overstate itself, record it in `tools/load-bearing-claims-record.json` with the violated law — do not silently repair it; truth edits belong to the owning seat. The false-claim registry pattern is reusable: a gate that passes only while the *known-violation set matches the record* turns drift into red without requiring a clean world first. Never game the rate by making notes enforcement-free to inflate compliance.

## ⚙️ MACHINE NOTE

{"sn": "SN-0513", "truth_state": "CANDIDATE", "family": "SN-0358 (nonstop-loop) :: SN-0343 (scorecard) :: this (note-enforcement-rate) :: SN-0512 (load-bearing-claims)", "provenance": ["#1354 comment 6028678714, 2026-10-07T01:08:03Z"], "measurement": {"window": 120, "commits_with_notes": 21, "commits_with_enforcement": 3, "note_enforcement_rate": 0.143, "registry": "tools/load-bearing-claims-record.json"}, "doctrine": {"note_first_enforce_next": "every Smart Note decides its enforcement fate at capture; enforcement lands in the next commit, tracked", "proxy_not_verdict": "the rate cannot tell whether a note should have been enforced — some notes are correctly documentation-only; never game the rate", "recorded_violation_set": "the gate passes only while the known-violation set matches the record; a new false claim is red, a silent unrecorded repair is also red", "truth_edits_belong_to_owner": "an overclaim in another lane's proof artifact is reported with evidence, never unilaterally rewritten from an enforcement PR"}}
