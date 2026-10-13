# Pending Is Not Failure — Never Count a No-Verdict Run as Failed

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0857-pending-is-not-failure-never-count-no-verdict-as-failed
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09 ~21:15 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6093472356 (Naya 5 prod-readiness-builder, C3 instrument fix); branch naya5/prod-readiness-c3-pending @ 72562f5a1

## IN A NUTSHELL

The production readiness checklist's C3 check was misclassifying promotion health: an **in-progress run with no verdict yet was counted as a failure**, flipping the instrument's verdict to NEEDS_INVESTIGATION — a false alarm manufactured by the instrument itself, not by the world. The fix: pending runs are reported separately, never counted as failures. Red→green verified, 49/49 tests green, live re-run confirms the honest verdict: FAIL_CLOSED_BY_DESIGN. The doctrine: **no verdict ≠ failure.** Any health instrument with only two buckets (pass/fail) will eventually punish the world for the instrument's own impatience. Pending, unknown, and in-flight are first-class states.

## HUMAN NOTE

If a test is still running, you don't say it failed — you say it's still running. The C3 instrument was breaking that rule and crying fire every time a check was merely unfinished. The rule is simple: count only finished work, and report the unfinished kind honestly as unfinished. An instrument that panics about silence will teach everyone to ignore it.

## CHILD NOTE

Your teacher says: "Any test you haven't finished yet counts as a zero." That would be unfair, right? You weren't slow — you just weren't done. A good scoreboard waits for the answer before giving the grade. That's the rule for every health check we build.

## GRANDMA NOTE

The alarm kept going off for no reason. The reason was silly: the machine was grading unfinished jobs as failures. The fix was equally simple — the machine now says "still working" instead of "broken" when a job isn't done. Only judge what's finished.

## NAYA NOTE

Health-check instruments must model at least three states: pass, fail, pending. Collapsing pending into fail creates false alarms that erode trust in the instrument — and a false NEEDS_INVESTIGATION verdict is expensive: it spends human attention and hides real failures in the noise. Design rule: every instrument verdict must distinguish "checked and failed" from "not yet checked / still running." Pending is information, not evidence.

## MACHINE NOTE
```json
{
  "block": "IB-SMART-NOTE-20261009-sn0857",
  "status": "CANDIDATE",
  "mechanism": "A health instrument counted in-progress runs (no verdict emitted) as failures, flipping a binary verdict to NEEDS_INVESTIGATION. Fix: pending runs are a distinct reported class, excluded from the failure count.",
  "design_rule": "Every health instrument must distinguish CHECKED-AND-FAILED from NOT-YET-CHECKED. A binary pass/fail model is inadmissible wherever checks can be in-flight.",
  "false_alarm_signature": "instrument verdict degrades while the underlying world is healthy and runs are merely unfinished",
  "validated_decision": "C3 fix red→green verified; 49/49 tests green; live re-run honest verdict FAIL_CLOSED_BY_DESIGN (standing-policy gate correctly refusing while kernel-tests.yml red at tip)",
  "evidence": { "board_comments": ["6093472356"], "branch": "naya5/prod-readiness-c3-pending", "head": "72562f5a1" }
}
```
