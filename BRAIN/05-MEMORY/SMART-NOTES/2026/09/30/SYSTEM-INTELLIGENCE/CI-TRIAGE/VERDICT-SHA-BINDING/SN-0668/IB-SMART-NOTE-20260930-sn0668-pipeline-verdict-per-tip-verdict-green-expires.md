# A Pipeline Verdict Is a Per-Tip Verdict — a "Main GREEN" Can Expire One Minute After the Push That Prompted It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0668-pipeline-verdict-per-tip-verdict-green-expires
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6055745714 (OVERNIGHT SWEEP — 2026-10-08 ~08:20 UTC, anchor main `53217a40`, correction of Tick 7's "main GREEN" claim 6054049760)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Pipeline-monitoring Tick 7 (comment 6054049760, 06:39Z) posted ~1 minute after the `53217a40` push, claiming `test: PASS`, `promote-and-prove: PASS`, "pipeline healthy." The overnight sweep (~08:20Z) re-checked the check-runs on the **current** tip — both concluded FAILURE — and flagged the Tick 7 claim as stale, factually, under the mutual-oversight protocol: what happened, why it's off, who owns it.

This is the pipeline-monitoring instance of SN-0493 (a decision expires when the tip moves): a pipeline verdict is computed on the exact bytes of tip T and is inadmissible as evidence about tip T+1. The boundary demonstrated here is ~1 minute — a verdict posted 60 seconds after a push was already stale. The sweep also showed what a correction must carry: the failing steps named (`test` run 37738738797, failing step "Run python -m pytest -q": 1 collection error + 8 failed / 1319 passed / 11 skipped, reproduced on byte-identical tip bytes in a detached worktree; `promote-and-prove` run 37738738772, failing step "Enforce ratified standing policy before automatic promotion" — guardrail firing as designed, production NOT moved, still `acf57082`), and the reds classified into owning lanes (2 genuinely new #1850-introduced reds flagged to the engine team in comment 6054038364 with no open repair; 4 known-RED with open repair; 2 guardrail-firing-as-designed; the earlier "checkout-luck nondeterminism" note explicitly superseded for `53217a40`).

The rule: never cite pipeline state without first re-reading the check-runs on the exact current tip — fetch the tip SHA, enumerate its check-runs, read the failing steps. A verdict without a tip SHA attached is a rumor, not evidence.

## 🩷 HUMAN NOTE

Shawn — this morning's sweep caught something worth baking in: a pipeline monitor posted "main GREEN" about one minute after a new push — and by the time the sweep looked again, both pipelines were actually failing. The verdict had expired in about 60 seconds. The lesson for the brain: a pipeline verdict is only ever about the exact tip it was computed on — the moment the tip moves, the verdict is dead. From now on, nobody cites "pipeline healthy" without re-checking the check-runs against the current tip SHA first, and every correction names the failing steps, the run IDs, and which lane owns each red. A verdict without a tip SHA attached is a rumor, not evidence.

## 🟣 CHILD NOTE

Imagine a weather report that says "sunny" — but it was written yesterday. You look out the window and it's raining. That's what happened: the pipeline report said "all green," but it was written one minute before things changed, and now two things are failing. The rule: never trust a report unless you check what it's actually about — the exact version of the code, right now. A report without a version number is just a guess.

## 👵 GRANDMA NOTE

Think of a road-inspection certificate: it's only valid for the road on the day it was inspected. If the road gets torn up and repaved the next morning, the old certificate means nothing. The pipeline monitor's "green light" was posted one minute after new work landed — and by the next check, both inspections were failing. From now on: every green light names the exact stretch of road it inspected (the tip SHA), and anyone who wants to quote it must re-inspect the current stretch first.

## 🧠 NAYA NOTE

Cold successor: before citing ANY pipeline verdict in a report, sweep comment, or sign-out, (1) fetch the current main tip SHA, (2) enumerate the check-runs on that exact SHA, (3) read the failing steps — never inherit a run-level conclusion (SN-0629) and never cite a verdict computed on an older tip (SN-0493). If the verdict you hold predates the current tip by even one push, it is stale: flag it as stale factually under mutual oversight — name what happened, why it's off, who owns it — and re-classify the current reds into owning lanes: NEW (flag to owning lane, no open repair), KNOWN-RED (open repair exists), GUARDRAIL-AS-DESIGNED (correct firing), ENVIRONMENTAL (supersede the old theory with the new evidence). This instance: Tick 7's 06:39Z "main GREEN" (6054049760) vs current tip `53217a40` check-runs `test` FAILURE (run 37738738797) and `promote-and-prove` fail-closed (run 37738738772) — corrected in #1354 6055745714.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0668",
  "title": "A Pipeline Verdict Is a Per-Tip Verdict — a \"Main GREEN\" Can Expire One Minute After the Push That Prompted It",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "VERDICT-SHA-BINDING"],
  "cousins": ["SN-0493", "SN-0629", "SN-0430", "SN-0442"],
  "evidence": {
    "board": ["#1354 6055745714 (OVERNIGHT SWEEP — 2026-10-08 ~08:20 UTC, anchor main 53217a40: correction of Tick 7 claim)"],
    "stale_claim": "#1354 6054049760 (Tick 7, 06:39Z): 'test: PASS, promote-and-prove: PASS, pipeline healthy' posted ~1 minute after the 53217a40 push",
    "current_truth": "check-runs on exact tip 53217a40: test run 37738738797 FAILURE (failing step 'Run python -m pytest -q'; reproduced on byte-identical tip bytes, detached worktree: 1 collection error in tests/test_engineering_gates.py + 8 failed / 1319 passed / 11 skipped); promote-and-prove run 37738738772 fail-closed at 'Enforce ratified standing policy before automatic promotion' — guardrail firing as designed, production NOT moved (still acf57082)",
    "classification": "2 genuinely-new #1850-introduced reds (no open repair, flagged to engine team in #1354 6054038364); 4 known-RED with open repair (SN-0359 hollowed x3 -> #1837; CI-declares-deps -> #1840 class); 2 guardrail-firing-as-designed (#1823's 8 new notes caught by registry ratchet -> #1838/#1844); rerun19 'checkout-luck nondeterminism' note superseded for 53217a40"
  },
  "rule": "never cite pipeline state without first re-reading check-runs on the exact current tip SHA; a verdict without a tip SHA is a rumor, not evidence — corrections name what happened, why it's off, and the owning lane of each red"
}
```
