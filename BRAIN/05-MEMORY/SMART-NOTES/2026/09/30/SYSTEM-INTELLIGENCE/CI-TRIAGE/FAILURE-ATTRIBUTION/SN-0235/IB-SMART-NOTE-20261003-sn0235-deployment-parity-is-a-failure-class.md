# Deployment Parity Is a Failure Class — Prove the Deployed Artifact Matches the Verified Package Before Changing Code

**Intelligent Block:** IB-SMART-NOTE-20261003-sn0235-deployment-parity-is-a-failure-class
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-03
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [NAYA][PRODUCTION HUB VERIFY] rung, #554 comment 5977197173 (2026-10-04T06:10:19Z) — headless real-Chrome production run against `hub.nayapower.workers.dev/hub/` at main pin `5b68f8dc`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The production verify rung caught two contextual Mail seams (Your Connections → Mail Naya 1; Smart Spaces → ✉ Mail Space) navigating to a stale `/hub/smartmail-v1.2.html` — while the statically-verified repaired package already pointed both seams to `mail.html`. The rung classified the result **DEPLOYMENT PARITY / STALE PRODUCTION ARTIFACT** — not a new code-design failure — and stated the routing rule plainly: **"Do not change code to solve this production result. First restore deployment parity."** Status was honest: `IMPLEMENTED / STATIC-VERIFIED != PRODUCTION-PROVEN`, with one next action: deploy the exact repaired artifact (`nayanet-final-fixed.zip`), then rerun.

Why this is brain-grade: every earlier lesson in this family proved a *static* gap — SN-0061 (branch-green is not merged-true), SN-0174 (preflight-only success is zero behavioral inference), SN-0233 (a pass read on a repaired worktree is a phantom green). This one closes the loop on the *live* side: a failing production check against a package you already verified can still be a false code-failure — the deployed bytes may not be the verified bytes. The cheap move is debugging code that was already repaired; the correct move is proving `deployed == verified` first. Rule for a cold successor: **when a live check fails, classify before you code — check deployment parity first (is the deployed artifact byte-equivalent to the artifact you verified?). If not, the failure class is deployment parity and the fix is a redeploy, never a code change.**

## 🩷 HUMAN NOTE

Shawn — one discipline I'm banking from the production verify rung: it found the live Hub's two Mail seams pointing at the old page, but the repaired package already pointed them at the right one — so the code wasn't wrong, the *deploy* was stale. New rule locked in: when a live check fails, we first prove the deployed bytes match the verified bytes before anyone touches code. Debugging code that's already fixed is the most expensive mistake here; a redeploy is the fix.

## 🟣 CHILD NOTE

The production test found the live Hub's Mail buttons pointing at the OLD page — but the repaired package already pointed them at the new one. So the code was fine; the website just hadn't been updated with the fix yet. New rule: when a live test fails, FIRST check "is the live site actually running the fixed version?" — before changing any code. Debugging code that's already correct is like rewiring a lamp that just wasn't plugged in.

## 👵 GRANDMA NOTE

The test of the live Hub showed the Mail buttons going to the old page — but the fix for that had already been written and checked. The live website just hadn't been given the new version yet. The lesson: when a live test fails, first ask "is the live thing actually the new version?" before fixing the code. Otherwise you end up "repairing" something that was never broken — like fixing a lamp that just wasn't plugged in.

## 🤖 NAYA NOTE

Source: #554 5977197173 (2026-10-04T06:10:19Z) — [NAYA][PRODUCTION HUB VERIFY], one-shell/eleven-room rung, source pin main `5b68f8dc`. Headless real-Chrome run vs `hub.nayapower.workers.dev/hub/`: 11/11 deep-link reachability PASS, desktop+mobile drawers PASS, back/forward PASS, active-state PASS. Two contextual Mail paths FAILED by navigating to stale `/hub/smartmail-v1.2.html` (Connections → Mail Naya 1; Spaces → ✉ Mail Space) while the repaired package (`nayanet-final-fixed.zip`) routes both to `mail.html` — classified DEPLOYMENT PARITY / STALE PRODUCTION ARTIFACT, explicitly "not a new code-design failure"; rule "Do not change code to solve this production result. First restore deployment parity." Secondary observation (non-blocking, after parity): Today uses its own `.corner-btn/.drawer-btn` chrome vs the newer `.naya-corner-btn/.naya-drawer-btn` — implementation divergence worth collapsing only after the corrected artifact is deployed and re-tested; not a standalone lesson (doubt rule). Cousins: SN-0061 (post-merge verification at the pin — the static-side twin: a verdict binds the exact bytes, not the intent), SN-0174 (preflight-only success is zero behavioral inference), SN-0233 (phantom green — verify on virgin state; this note is its deployed-artifact twin), SN-0059 (clean-main control run — attribute the failure before blaming the change; parity check is the deployment-side control), SN-0065 (branch-boundary claims — intent stated as capability), SN-0099 (the promise gate — truth-state honesty: IMPLEMENTED/STATIC-VERIFIED != PRODUCTION-PROVEN).

## ⚙️ MACHINE NOTE

{"sn": "SN-0235", "title": "Deployment Parity Is a Failure Class — Prove the Deployed Artifact Matches the Verified Package Before Changing Code", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-03", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "FAILURE-ATTRIBUTION"], "cousins": ["SN-0061", "SN-0174", "SN-0233", "SN-0059", "SN-0065", "SN-0099"], "evidence": {"rung": "#554 comment 5977197173 (2026-10-04T06:10:19Z) — production verify rung at main pin 5b68f8dc", "finding": "two contextual Mail seams navigate to stale /hub/smartmail-v1.2.html in production while the repaired package points both to mail.html", "classification": "DEPLOYMENT PARITY / STALE PRODUCTION ARTIFACT — not a new code-design failure", "rule_cited": "'Do not change code to solve this production result. First restore deployment parity.'", "truth_state_cited": "IMPLEMENTED / STATIC-VERIFIED != PRODUCTION-PROVEN", "next_action": "deploy the exact repaired artifact (nayanet-final-fixed.zip), then rerun the same production suite"}, "rule": "when a live verification fails, classify before you code: first prove the deployed artifact is byte-equivalent to the artifact you verified — if not, the failure class is deployment parity and the fix is a redeploy, never a code change"}
