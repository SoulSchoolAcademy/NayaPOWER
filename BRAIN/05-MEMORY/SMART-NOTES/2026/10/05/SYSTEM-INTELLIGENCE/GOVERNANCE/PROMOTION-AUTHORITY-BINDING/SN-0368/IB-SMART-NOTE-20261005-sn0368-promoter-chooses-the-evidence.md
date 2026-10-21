# The Promoter Chooses the Evidence — A Passing Audit Attests to Internal Coherence, Not to Truth

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0368-promoter-chooses-the-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~09:27–09:31 PDT — CODA 1 receipt-tampering drill + partial retraction (comment 5998627810), CODA 2 sign-in/sign-out drill (comments 5998690100, 5998699104). All drills ran in throwaway sandboxes with fabricated registries; repo untouched.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A two-seat adversarial drill settled the shape of the Smart Note promotion trust boundary. CODA 1 forged receipts three ways against `verify_receipt` — self-consistent forgery, forged receipt against real evidence, attacker re-hashing to match real evidence — and all three were REJECTED: the verifier re-runs the threshold gates (including `gatherer_independence`) instead of trusting the seal. That is good engineering, and CODA 1 publicly retracted the overstated escalation. Then CODA 2 showed nobody has to forge anything: DRILL A proved `gatherer_independence` counts distinct strings, not real independent gatherers — invented `party-X` / `party-Y`, existing nowhere in the repo, PASS. DRILL B called `promote_note` as designed and minted a **genuine** receipt for an unauthorized promoter, elevating truth state CANDIDATE→VERIFIED with nothing corrupted. DRILL C: `verify_receipt` returned True — and was *right to*. The two findings reconcile: the seal is forgeable **and** re-validation is strong, yet neither implies safety, because **re-validation re-derives against the evidence bundle supplied by the promoter under audit**. A passing audit attests to internal coherence, not to truth.

Why this is brain-grade: SN-0362 named the unkeyed seal; this note names the deeper boundary — the evidence itself. Every audit check that consumes attacker-chosen inputs without independent sourcing inherits the attacker's frame. The standing question for any future gate: who supplies the evidence the gate verifies, and who authenticates the suppliers?

## 🩷 HUMAN NOTE

Shawn — your adversarial lanes stress-tested the Smart Note promotion system this morning and found its real shape: the receipt verifier is genuinely strong (it re-runs every gate instead of trusting the seal), but the audit can only ever verify the evidence bundle the promoter hands it — and the "independent gatherers" check counts distinct names, not real people. Nothing is broken that needs an emergency fix; this is now the documented trust boundary your lanes will design against. Both seats ran everything in throwaway sandboxes — your repo was never touched.

## 🟣 CHILD NOTE

Imagine a teacher checking homework by asking the student to show their work — and the student hands over the paper they checked themselves. The teacher's checking is honest and careful, but they can only check what the student chose to hand over. Now imagine the teacher's rule "two classmates must check it" — the student just writes two made-up names at the top. The rule counted names, not real classmates. The lesson: always ask *who* provided the proof, not just whether the proof looks neat.

## 👵 GRANDMA NOTE

Shawn's AI security team tested their own note-approving system by attacking it. They found the checker does its job well — but it can only check the evidence the requester provides, and the "independent witnesses" rule accepts any two different names, even invented ones. So a passing check means "everything hangs together," not "this is true." The team wrote this down so every future checker asks the hard question: who provided the evidence?

## 💜 NAYA NOTE

For any future seat designing or auditing a gate: the drill pair is the reference for how adversarial work is done here — throwaway sandbox, fabricated registries, exact output quoted, repo untouched, retractions posted publicly and immediately (CODA 1's partial retraction is the model). The substantive doctrine: (1) `verify_receipt` re-derives rather than trusting the seal — that is the bar; copy it. (2) Re-derivation still consumes the promoter's evidence bundle, so a PASS means internal coherence only. (3) `gatherer_independence` is string diversity, not corroboration — do not read it as "two independent people confirmed this." When you design the fix, the missing piece is authenticating the *suppliers*, not strengthening the *seal*. Cross-reference SN-0362 (unkeyed seal), SN-0360 (guard off the write path is a suggestion).

## 🖥️ MACHINE NOTE

{"sn": "SN-0368", "title": "The Promoter Chooses the Evidence — A Passing Audit Attests to Internal Coherence, Not to Truth", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "PROMOTION-AUTHORITY-BINDING"], "cousins": ["SN-0362", "SN-0360"], "evidence": {"coda1_drill": "board #1354 comment 5998627810 — 3 forged-receipt drills vs verify_receipt at bf4c8e9b, all REJECTED on re-validation gates; partial retraction of prior escalation", "coda2_drill": "board #1354 comments 5998690100, 5998699104 — DRILL A: invented gatherers pass gatherer_independence; DRILL B: promote_note mints genuine receipt for unauthorized promoter (CANDIDATE→VERIFIED); DRILL C: verify_receipt True and right to — re-derives against promoter-supplied bundle"}, "rule": "An audit attests to internal coherence of the bundle it is given, never to truth. Re-validation is the engineering bar; authenticating the evidence suppliers is the remaining gap. gatherer_independence measures string diversity, not corroboration — never cite it as independent confirmation"}
