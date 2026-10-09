# Form Validation Is Not Substance Proof — Self-Attested Receipts Accept 30-Second Forgeries

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0795-form-validation-is-not-substance-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6084472606 ([NAYA 2][ADVERSARIAL] — Activation gate forgery hole in PR #1979, 2026-10-09T15:58:21Z) + comment 6084523027 ([NAYA 5 — Pair D validation], 2026-10-09T16:01:19Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 ran an independent adversarial battery against the activation enforcement primitive (`drink_first_gate.py`): 18 attacks across 6 vectors. **Result: 14 caught, 4 slipped through. Score 6/10.** Form validation was excellent — every honest mistake caught (stale, malformed, future timestamps, wrong schema). But the critical finding: **forged receipts pass.** An attacker who never activates fills the JSON template with the public tip SHA and a current timestamp, and the gate passes it. The gate verifies the receipt's *form*, not the activation's *substance* — a 30-second forgery is indistinguishable from real activation. The same battery found: v1 schema has no `repository` field (wrong-repo passes), no version/digest for loaded content (stale design laws pass), and a wrong reverse SHA-prefix check.

The positive contrast, same day (Naya 5's Pair D validation of `naya5/ship-design-gate`): the activation machinery survived 9/9 attacks — valid, forged, expired, future-dated, wrong-repo, stale-swap, missing-field — because `sha256(marker) == sha256(exact receipt bytes)` is exact math the claimant cannot fabricate.

Why this is brain-grade: a gate proves whatever it binds. Bind to self-asserted fields and you prove the claimant can fill in a form — which is what the forger does. Bind to exact bytes or to an attestation from a trusted process and the forger has nothing public to copy. The fix is architectural, never another field check: signed receipts (the activation process attests, not the worker) or challenge-response. More validation only raises the forger's typing effort from 30 seconds to 31.

Rule for a cold successor: **when you build or review a gate, ask "can I forge this with public values?"** If yes, the gate proves form, not substance — close the hole with trusted attestation or exact-bytes binding, not more field validation. Pairs with SN-0787 (receipts need a trusted runner) and SN-0425 (name the gap, bound the claim).

## 🩷 HUMAN NOTE

Shawn — the adversarial lane did its job today, and the finding is one to bank permanently. Naya 2 tested the activation gate with 18 attacks. It caught every honest mistake beautifully — stale timestamps, malformed fields, all of it. But a forger who just fills in the public tip SHA with a fresh timestamp walks right through, because the gate checks the receipt's *shape*, not whether activation actually happened. The good news: Naya 5's gate machinery held 9/9 against the same class of attack, because it binds the check to exact bytes — math a forger can't fake. The standing rule: a gate must anchor to something the claimant can't fabricate. Anything else is form validation, and form validation accepts forgeries.

## 🟣 CHILD NOTE

Imagine a bouncer who checks whether your ID *looks* like a real ID — right colors, right size, today's date written on it. A forger with crayons passes every time. Now imagine a different bouncer who calls your school and asks "is this student really here?" — crayons don't help anymore. The first bouncer checks the *form*; the second checks the *substance*. Naya 2 proved the activation gate was the first bouncer: anyone could fill in public numbers and pass. The fix is to become the second bouncer — check something the forger can't draw.

## 👵 GRANDMA NOTE

Grandma, think of a lockbox where the guard checks that your permission slip is filled in neatly — name, date, signature. A clever person just writes in the blanks and walks through. That's form-checking. Now think of a guard who phones the office to confirm *they* issued the slip — the forger can't fake the office's voice. Naya 2 showed our activation gate was the first guard: it checked the slip, not the office. The lasting lesson for all our gates: verify with something the person can't write themselves — exact records, or a trusted witness who confirms it really happened.

## 🟣 NAYA NOTE

Mechanical rule for gate builders and reviewers: (1) after any gate passes your positive tests, run the forgery test — fill the receipt with public values (public tip SHA, current timestamp) and no real activation; if it passes, the gate proves form only; (2) close form-only gates by binding verification to something the claimant cannot fabricate — exact-bytes equality (`sha256(marker) == sha256(exact receipt bytes)`), a signature from a trusted attesting process, or challenge-response; (3) never close a forgery hole by adding more field checks — that only lengthens the forger's form; (4) the trust question is always "who attests?" — if the worker attests its own activation, there is no trust boundary; the activation *process* must attest. Adversarial testing is the standing mechanism that finds these; the builder never self-certifies the fix.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0795",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/SECURITY-POSTURE",
  "doctrine": "form-validation-is-not-substance-proof",
  "rule": "A gate that verifies receipt form (fields present, schema valid, timestamps sane) cannot distinguish a 30-second forgery from real activation. Bind verification to something the claimant cannot fabricate — exact bytes or a trusted process attestation — and confirm with the forgery test (public values, no real activation) before any enforcement claim.",
  "failure_mode": "self-attested receipts accepted as proof of activation; forged receipts pass (wrong-repo also passes when the schema lacks repository binding); adding more field checks instead of architectural attestation",
  "checks": [
    "gate passes positive fixtures (valid receipt, lawful page)",
    "gate fails the forgery fixture: public tip SHA + current timestamp, no activation",
    "gate fails wrong-repository receipts (repository bound to gated repo, exact full SHA, no prefixes)",
    "verification anchored to exact bytes or trusted attestation, never worker self-assertion"
  ],
  "pairs_with": ["SN-0787", "SN-0425", "SN-0586"],
  "provenance": {
    "board": "#1354",
    "comment_ids": [6084472606, 6084523027],
    "author": "SoulSchoolAcademy",
    "seat": "Naya 2 (adversarial), Naya 5 (validation)",
    "timestamp": "2026-10-09T15:58-16:01Z"
  }
}
