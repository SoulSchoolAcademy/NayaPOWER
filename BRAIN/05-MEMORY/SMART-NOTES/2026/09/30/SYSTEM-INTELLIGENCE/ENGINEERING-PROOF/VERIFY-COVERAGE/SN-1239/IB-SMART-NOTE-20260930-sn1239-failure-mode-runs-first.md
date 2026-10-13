# Failure-Mode Runs Precede Happy-Path Runs

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1239-failure-mode-runs-first
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md [t0692] Naya Herald entry (2026-10-13, mirror of t0681 Stage-0 INTAKE readiness audit, 9.0/10) — done-criteria NOT MET on three independent grounds: no genuine outside entry since the t0422 simulation, diary_intake.py cannot write the live file it targets (format guard rejects), no reachable submit surface. Two-target synthetic probe run in five minutes: live-copy → exit 2 REJECTED; proper-header copy → exit 0 APPENDED. Mechanism proven working AND target proven hostile in the same probe. Her own summary: "had she only tested the hospitable copy, she would have shipped PASS on a door that rejects everything."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya Herald audited a door. She didn't knock politely first — she tried to walk through it carrying the wrong key. The live file rejected everything (exit 2); a proper-header copy was accepted (exit 0). In five minutes she proved the mechanism works AND the target is hostile — two facts one hospitable probe could never separate. Her verdict stands on the failure run: done-criteria not met on three independent grounds, because the failing probe has discriminating power and the happy probe doesn't. The standing rule: failure-mode runs precede happy-path runs. A hospitable input cannot tell a working mechanism from a dead one — only a case the mechanism should REJECT tests the door. Had she tested only the hospitable copy, she would have shipped PASS on a door that rejects everything, and the false PASS would have been indistinguishable from a true one.

Why this is brain-grade: probe order is a decision every auditor makes on every mechanism, forever. Getting it wrong produces false PASS verdicts — the most expensive output in the system, because a false PASS compounds into downstream trust. This note fixes the order in doctrine: probe the refusal first, the acceptance second; ship neither without both.

## 🩷 HUMAN NOTE

Shawn — there's a right order for testing anything, and it's backwards from instinct. Naya Herald audited the intake door by trying the thing that should FAIL first: the live target rejected it, the clean copy passed. Five minutes, both facts proven. Her point, now standing: if she'd only run the happy test, she'd have certified a door that rejects everything. New rule for every audit: run the failure probe first, the happy probe second. A test that can't say "no" can never mean "yes."

## 🟣 CHILD NOTE

Imagine testing whether a goalie is good. If you only kick easy balls straight at her, she'll catch them all — but you learn nothing, because a scarecrow could do that. You have to kick the hard shots, the ones she SHOULD miss if she's bad. Only the hard shot tells you if she's a real goalie. Testing a machine works the same way: try the thing it should refuse first. If it can't refuse, the "it works" test is meaningless.

## 👵 GRANDMA NOTE

You don't test a smoke alarm by blowing clean air at it — you test it with smoke. The team learned this the formal way: an audit that only tries the easy, friendly case will happily certify a mechanism that's completely dead, because a dead mechanism and a working one look identical on the easy case. The rule now: smoke first, clean air second. A device that can't sound the alarm can't be trusted when it stays quiet.

## 🧠 NAYA NOTE

Note to future me: when I audit any mechanism, the FIRST probe is the refusal case — the input the mechanism must REJECT, run against the live target. Only then the acceptance case. Both must land as designed (refusal fires, acceptance passes) before any verdict. A happy-path-only audit is not an audit; its PASS is unquotable. If I catch myself reaching for the hospitable copy first, that's the instinct this note exists to override. Score check: if audits that probe failure-first never catch a false PASS that happy-first would have shipped, this rule is theater — keep count on receipts and say so.

## ⚙️ MACHINE NOTE

{"sn": "SN-1239", "title": "Failure-Mode Runs Precede Happy-Path Runs", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "VERIFY-COVERAGE"], "cousins": [], "evidence": {"finding": "lesson-broadcast.md [t0692] Naya Herald (mirror, t0681 Stage-0 INTAKE readiness audit, 9.0/10, 2026-10-13): two-target synthetic probe — live-copy -> exit 2 REJECTED, proper-header copy -> exit 0 APPENDED, both in five minutes; done-criteria NOT MET on three independent grounds (no genuine outside entry since t0422 simulation; diary_intake.py cannot write its live target — format guard rejects; no reachable submit surface)"}, "decision_change": "when auditing any mechanism, run the failure probe FIRST (the input it must reject, on the live target), then the acceptance probe; a PASS on the hospitable path alone can never ship a verdict", "falsifier": "audits that probe happy-path-first never produce false-PASS verdicts — i.e., probe order never changes verdicts on receipt history — then the sequencing rule adds nothing", "mechanism": "hospitable inputs cannot discriminate a working mechanism from a dead one; only a case the mechanism should REJECT has discriminating power — the failing probe is what tests the door", "rule": "failure-mode runs precede happy-path runs: prove the refusal fires on the live target before proving the acceptance passes; a check that cannot say no can never mean yes"}
