# Out-of-Scope Is Not a Pass — A Gate's Scope Glob Is Part of the Verification

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1081-out-of-scope-is-not-a-pass
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** receipts hidden_files/twelve-lane-receipts/t0272-lane1.md (Lane 1 t0272 second-seat review of #2454, 2026-10-12 ~12:27 PDT) and hidden_files/twelve-lane-receipts/t0292-lane8.md (Lane 8 t0292, SEAT_RE scope-gap, 2026-10-12 ~12:42 PDT); .github/workflows/receipt-gate.yml:45.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During Lane 1's second-seat review of PR #2454, the receipt-pin gate showed PASS on the head branch — but Lane 1 verified on live bytes that the gate had never run. The gate's scope glob (`if [[ "$HEAD_REF" == naya/* ]]`, receipt-gate.yml:45) does not match `naya2/*`. #2454's head was `naya2/infra-tip-red-heal-20261012`: out-of-scope, so the check exited before any verification. **The pin check passed by out-of-scope decision, never by verification.** Every `naya2/*` lane branch sat entirely outside receipt-pin enforcement — the same defect class as the SEAT_RE `naya2/*` blind spot. Named fix (handed to Lane 9, the gate's owner): extend the glob to `naya*` with an explicit comment — NOT folded into #2454 itself, one mechanism per PR.

**The doctrine:** a gate's scope pattern is itself a verification decision — audit it like code, not like configuration. When the branch-naming convention changed (`naya/*` → `naya2/*`), every glob that encoded the old convention silently expired. A PASS on an out-of-scope item is a decision, never evidence: no run ran, no receipt exists. A check result is only attributable to the run that produced it; "nothing failed" is the cheapest lie a gate can tell when the gate never saw the work.

**The standing repair rule:** on any naming-convention change, enumerate every scope glob that encodes the old convention (grep for `naya/`, `refs/`, `HEAD_REF` patterns) and re-scope each explicitly — with a comment naming the in-scope families. A glob without a comment naming its intended families is an accident waiting for a rename.

For a cold Naya: never read a green check as "verified" until you confirm the check's scope actually included the item. Ask: did the check RUN on this head? If the answer is "it didn't need to," treat that as a decision — and verify the decision's author and reasoning, because the exclusion is where the verification failed.

## 🩷 HUMAN NOTE

Shawn — a gate was quietly not enforcing on whole branch families. The receipt-pin gate's scope glob only matched `naya/*`, but the lanes have been working on `naya2/*` branches — including #2454's own head, which read as "PASS" for a check that never ran on it. Lane 1 caught it on live bytes during the second-seat review; Lane 8 named the fix for Lane 9 (extend the glob, with an explicit comment, on the gate owner's next touch — not folded into the PR being reviewed). The durable lesson: a gate's scope pattern is itself a verification decision. When the naming convention changed, the globs that encoded the old one silently expired. "No failures" from a check that never saw the work is the cheapest lie a gate can tell.

## 🟣 CHILD NOTE

Imagine a hall monitor who only checks the students in the blue hallway — and writes "everyone's behaving" on the report. But half the students are in the green hallway, where the monitor never looks. The report is wrong: it says everything is fine, but it never checked. The receipt-pin gate did exactly that: it looked only at branches starting with `naya/` and skipped branches starting with `naya2/`. The fix: tell the monitor to check both hallways. And the rule: when the hallways get renamed, check who has the new map — because the monitor was still using the old one.

## 👵 GRANDMA NOTE

It's like a recipe tester who only tastes the cakes marked "batch A" and signs off on the whole day's baking — including the "batch A2" cakes she never opened. The signature looks like a test, but it isn't. The team renamed some batches and nobody updated the tester's list, so she kept signing off on things she never tasted. The lesson: when names change, update the lists that use names — and never trust a "passed" stamp until you confirm the test actually ran on the thing stamped.

## 💜 NAYA NOTE

Note to future me: out-of-scope is not a pass. When I see a green check, my first question is "did this check RUN on this head?" — a scope glob (`naya/*`) is an executable decision, not config. When a naming convention changes, I grep every glob that encoded the old convention and re-scope each with a comment naming the intended families. The Lane 8 discipline: the fix goes to the gate owner, not folded into the PR being reviewed (one mechanism per PR). And the report discipline: "nothing failed" without "the check ran" is the cheapest lie a gate can tell — I say which one I mean.

## ⚙️ MACHINE NOTE

{"sn": "SN-1081", "title": "Out-of-Scope Is Not a Pass — A Gate's Scope Glob Is Part of the Verification", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-12", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "VERIFY-COVERAGE"], "cousins": ["SN-1077", "SN-1072", "SN-1073", "SN-1074", "SN-0200", "SN-1037"], "authority": "observed finding — Lane 1 t0272 second-seat review + Lane 8 t0292 scope-gap confirmation on live bytes, 2026-10-12; CANDIDATE (auto-capture, not ratified)", "evidence": {"lane1": "twelve-lane-receipts/t0272-lane1.md: head branch naya2/... does NOT match the gate's naya/* scope glob — the pin check passes by out-of-scope decision, never by verification; naya2/* lane branches sit entirely outside receipt-pin enforcement (same defect class as SEAT_RE)", "lane8": "twelve-lane-receipts/t0292-lane8.md: confirmed on live bytes — receipt-gate scope glob (if [[ \"$HEAD_REF\" == naya/* ]], .github/workflows/receipt-gate.yml:45) misses naya2/*; #2454's own head naya2/infra-tip-red-heal-20261012 is out-of-scope → PASS by decision, enforcement silently skipped; named fix: extend glob to naya* with an explicit comment, in the owning seat's next gate touch, NOT folded into #2454 (one mechanism per PR)", "gate_bytes": ".github/workflows/receipt-gate.yml:45"}, "doctrine": {"scope_glob_is_a_decision": "a gate's scope pattern is itself a verification decision — audit it like code, not configuration", "out_of_scope_is_not_a_pass": "a PASS on an out-of-scope item is a decision, never evidence — no run ran, no receipt exists; never read green as verified until scope inclusion is confirmed", "convention_change_audit": "when a naming convention changes (naya/* → naya2/*), enumerate every scope glob encoding the old convention and re-scope each with a comment naming the intended families", "owner_receives_the_fix": "the scope fix goes to the gate owner (Lane 9), not folded into the PR being reviewed — one mechanism per PR"}}
