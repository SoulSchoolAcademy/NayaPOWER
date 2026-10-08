# IB-SMART-NOTE — SN-0580 — Attack Your Own Verifier Before You Trust It

Intelligent Block: IB-SMART-NOTE-20261007-sn0580-attack-your-own-verifier-before-you-trust-it
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-07
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A verifier that was never attacked is a hope, not a gate. The TRUTH lane adversarially reviewed #1766's fail-closed trial-evidence verifier — and defeated it three ways (in-repo symlink → /tmp, `../../tmp` traversal, symlink → /etc/hostname), all accepted as "durable evidence." The fix: resolve every path, enforce repo containment, fail closed when the repo root is ephemeral. Five adversarial regression tests now lock it in, 16/16 green.

## HUMAN NOTE
The learning trial evidence verifier (PR #1766) was built fail-closed: evidence must live in durable repo paths, not ephemeral /tmp. But "fail-closed" was a claim, not a proof — until TRUTH-AGENT played attacker against it. Three attacks, three wins: an in-repo symlink pointing to /tmp, a `../../tmp` traversal, and a symlink to /etc/hostname all passed as "durable evidence." The hardening: `resolve()` every path before judging it, require the resolved path to stay inside the repo (containment), and fail closed when the repo root itself is ephemeral (so an attacker can't just declare /tmp the root). Five adversarial regression tests encode the attacks permanently — the next verifier gets the same treatment. Landed as PR #1772 (stacked, unmerged), evidence at #1354 comment 6047425449.

## CHILD NOTE
If you build a lock, don't just say "it's a strong lock" — hire someone to try to pick it BEFORE you trust it with your treasures. The lock-maker found three ways to sneak past their own lock, fixed all three, and now those three tricks are written down so they can never work again.

## GRANDMA NOTE
Sweetheart, you don't know a fence is good until someone tries to climb it. Test your own safety checks like an enemy would — then fix every hole you find.

## NAYA NOTE
Standing doctrine for every verifier a Naya seat ships: adversarial self-review is part of the build, not an optional extra. The protocol: (1) state the verifier's rejection contract (what must it refuse?); (2) generate the attack set — symlinks, traversal, case tricks, encoding tricks, environment tricks (ephemeral root); (3) run them against the verifier BEFORE claiming it is fail-closed; (4) harden and encode each defeated attack as a permanent regression test. A verifier that invited the attack and survived is evidence; a verifier nobody attacked is a wish. This pairs with the fail-closed design law (fail-closed is the design working) — but fail-closed-by-design still needs fail-closed-by-proof. Evidence: #1354 comment 6047425449 (TRUTH-AGENT adversarial review), PR #1772 (hardened verifier, 16/16 green, 2026-10-07).

## MACHINE NOTE
{
  "smart_note_id": "SN-0580",
  "intelligent_block_id": "IB-SMART-NOTE-20261007-sn0580-attack-your-own-verifier-before-you-trust-it",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM_INTELLIGENCE",
  "topic": "ENGINEERING_PROOF",
  "subtopic": "INDEPENDENT_VERIFICATION",
  "captured_at": "2026-10-07",
  "rule": "adversarial_self_review_before_trust",
  "defeated_attacks": [
    "in-repo symlink -> /tmp accepted as durable evidence",
    "../../tmp traversal accepted as durable evidence",
    "symlink -> /etc/hostname accepted as durable evidence"
  ],
  "hardening": "resolve() every path; enforce repo-containment on resolved path; fail closed on ephemeral repo root; 5 adversarial regression tests; 16/16 green",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6047425449",
    "pr": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1780",
    "verifier_pr": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1772",
    "found_at": "2026-10-07"
  }
}
