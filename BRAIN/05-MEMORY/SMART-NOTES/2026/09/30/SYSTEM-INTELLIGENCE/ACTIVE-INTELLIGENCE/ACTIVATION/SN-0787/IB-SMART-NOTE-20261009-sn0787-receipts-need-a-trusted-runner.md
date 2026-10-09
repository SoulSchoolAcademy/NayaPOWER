# Activation Receipts Need a Trusted Runner — a Builder Can Forge the Receipt AND the Expected Hashes

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0787-receipts-need-a-trusted-runner
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6083160786 ([CROSS-TEAM COORDINATION / CONNECT-FIRST] Independent QA deliverable — 2026-10-09). Source: SoulSchoolAcademy (QA / Naya lane).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The independent QA deliverable for the activation system (DRAFT PR #1974 — the activation receipt falsifier: a narrow consistency checker, 14 adversarial fixtures, trusted-runner integration brief; exact blob SHAs reread and verified; 14/14 expected outputs executed for the exported function in an isolated JS check; the committed Node suite has NOT run in CI — never claim the gate is installed) names the forgery the whole activation enforcement design must survive: **a builder can fake their own receipt AND fake the expected hashes.** A verifier that trusts the builder's own reference values verifies nothing — forgery just moves one level up. The required separation: **only a separate trusted runner can calculate source state + receipt digest.** The check lives outside the builder by construction; builder → GATE → pass ships / fail returns, and the gate's expected values come from the trusted runner's independent computation, not from anything the builder submitted.

Two more boundaries from the same deliverable: (1) the check returning CONSISTENT is a consistency fact — it is NOT "Naya understood," NOT "Naya learned," NOT "9.5/10," NOT "authorized." Never let a consistency verdict get promoted into a claim it doesn't support. (2) Real drift happened during the cycle itself — main `9f2e3db5` → `b9a312c4` → `8700e112` — so a stale activation without revalidation before action is invalid by the V2 law; freshness is part of the receipt, not decoration. And a live gap was found on other lanes' checks: Naya 5's `tools/design_gate.py` checks HTML/CSS against the manifest but not a fresh activation receipt, its SHA, source version, or delivered-file citation; Naya 4's V2 receipt referenced `BRAIN/10-INTERFACES/DESIGN-DOCTRINE.md`, which doesn't exist on live main — receipts must resolve current actual files, not assumed names.

Rule for a cold successor: **expected values must be derived from a source the builder cannot write.** If the party being checked supplies both the artifact and the reference to check it against, you have theater, not verification. And: a verdict only ever says what the check actually measured — CONSISTENT means the bytes agree; it means nothing else.

## 🩷 HUMAN NOTE

Shawn — one from the cross-team QA work this morning that's worth locking in. The independent QA seat built a falsifier for the activation receipts and named the attack it has to survive: a builder can fake not just their receipt, but the expected values the receipt is checked against. So the checker can't trust anything the builder supplies — a separate trusted runner has to compute the expected state independently. Builder supplies work; the gate supplies the verdict; and the gate's reference numbers come from a source the builder can't touch. She also drew a hard line: when the checker says "consistent," that only means the bytes agree — it does NOT mean anyone understood, learned, scored 9.5, or was authorized. Never promote a verdict into a claim it didn't measure. (And the falsifier is still a draft — 14/14 checks run in isolation, but the committed suite hasn't run in CI, so nobody claims the gate is installed yet.)

## 🟣 CHILD NOTE

Imagine you grade your own test AND you write the answer key. You'd get 100% every time — and so would everyone. That's the problem the team found with checking activation receipts: the builder could fake the receipt AND fake the answers it's checked against. So the rule is: the person being graded never provides the answer key. A separate, trusted checker computes the right answers on its own, from the real source. And when the checker says "everything matches," that only means "everything matches" — not "you're a genius." Moral: the judge's answer key must come from somewhere the student can't reach, and a verdict only ever says exactly what it measured.

## 👵 GRANDMA NOTE

The team built a checker for the new activation receipts and spotted a subtle hole: whoever is being checked could fake not only their receipt but also the reference numbers the receipt is verified against. That's like grading your own exam with your own answer key. The fix: a separate trusted checker computes the reference numbers independently from the real source — the builder's word is never used. And when the checker says "consistent," it means only that the numbers match — not that anyone understood anything or was authorized. A verdict says exactly what was measured, nothing more.

## 🟠 NAYA NOTE

For every compliance/verification check you design: (1) the expected values the check compares against MUST be derived from a source the checked party cannot write — a separate trusted runner recomputes source state + receipt digest independently. If the builder supplies both artifact and reference, you have theater, not verification. (2) Name the verdict's claim boundary in the same breath: CONSISTENT = byte-level consistency only; it never implies understanding, learning, scores, or authorization. (3) Freshness is part of the receipt — revalidate before action (main moved 3 times in one cycle; a stale receipt is invalid). (4) Receipts cite exact live bytes: resolved SHAs, current actual file paths (never assumed names), delivered-file citations. Ship the falsifier's adversarial fixtures with it — 14 here — and never claim a gate is installed until its committed suite runs in the real pipeline.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0787",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ACTIVE-INTELLIGENCE/ACTIVATION",
  "doctrine": "trusted-runner-separation",
  "rule": "Expected values must be derived from a source the builder cannot write — only a separate trusted runner computes source state + receipt digest. A CONSISTENT verdict is a byte-consistency fact; it never implies understanding, learning, scores, or authorization.",
  "failure_mode": "a builder can fake their own receipt AND fake the expected hashes — a verifier trusting builder-supplied references verifies nothing; forgery moves one level up; receipts citing assumed (nonexistent) file paths resolve to nothing",
  "mechanism": {
    "artifact": "DRAFT PR #1974 — activation receipt falsifier: narrow consistency checker + 14 adversarial fixtures + trusted-runner integration brief; 14/14 expected outputs executed in isolated JS check; committed Node suite NOT run in CI — never claim the gate is installed",
    "observed_gaps": "tools/design_gate.py checks HTML/CSS vs manifest but not fresh activation receipt/SHA/source version/delivered-file citation; V2 receipt referenced a DESIGN-DOCTRINE.md path missing from live main — receipts must resolve current actual files",
    "freshness": "main drifted 9f2e3db5 → b9a312c4 → 8700e112 in one cycle; stale activation without revalidation is invalid (V2 law)"
  },
  "related": ["SN-0784", "SN-0783", "SN-0421", "SN-0493"],
  "provenance": ["#1354 comment 6083160786"]
}
