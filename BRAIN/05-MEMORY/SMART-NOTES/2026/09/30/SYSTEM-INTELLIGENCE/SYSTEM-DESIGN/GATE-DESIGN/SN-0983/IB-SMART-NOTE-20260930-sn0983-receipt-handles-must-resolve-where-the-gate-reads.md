# Receipt Handles Must Resolve Where the Gate Reads Them

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0983-receipt-handles-must-resolve-where-the-gate-reads
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/GATE-DESIGN

## IN A NUTSHELL

A CI receipt gate demanded a 40-character head SHA as a "live handle" on the PR body — but the gate runs in `actions/checkout@v4`'s default depth-1 merge checkout, where `git cat-file -e <head-sha>` cannot see the head SHA at all. An honest, valid SHA read as a dead handle: the gate failed with "1 dead artifact handle(s)" while the URL-verified same SHA was green. The builder reproduced the failure exactly in a local shallow `pull/2340/merge` checkout, then shipped v2 as a URL-only handle plus a note explaining *why the SHA is intentionally omitted* — so nobody "fixes" it back.

The durable rule: **a receipt handle must be resolvable in the environment that consumes it.** The gate (SN-0955's side) is right to refuse the unresolvable — but when an honest claim fails a fail-closed gate, the indictment is of the *contract*, not the claim. Fix the handle contract (resolve SHAs via the API, or steer authors to URL/path handles), not the claimant. A gate whose own requirements are dead-by-design trains authors to distrust gates.

## HUMAN NOTE

Shawn — a receipt gate demanded the head SHA as proof, but the gate's own checkout is too shallow to ever see it. An honest SHA kept failing as "dead" while the same proof verified fine through a URL. The builder proved the checkout was the problem (not the SHA) and switched to URL-only handles, with a note explaining why the SHA is *intentionally* left out so nobody re-adds it. Lesson banked: don't ask for evidence your own gate can't check — you'll fail honest work and teach people to game the receipt instead.

## CHILD NOTE

The teacher said "bring your library card and I'll scan it," but the scanner only works on paper cards and yours is digital — so it beeps red even though your card is real. The fix isn't to scold you; it's to change the rule: the teacher should accept what the scanner can actually read. Rule: never demand a kind of proof your own checker can't check.

## GRANDMA NOTE

It's like asking someone to show their ID through a window that doesn't open, then saying their ID is bad when they can't hand it through. The ID was fine — the window was the problem. If your checker can't read a form of proof, stop asking for it; ask for the form it *can* read. Otherwise you'll keep turning away good people and blame them for it.

## NAYA NOTE

When I write a gate, I now check the handle contract in both directions. SN-0955 is my refusal side: unresolvable → refuse. This note is my *contract* side: before I require a handle form (SHA, artifact ID, path), I verify that form resolves in the environment the gate actually runs in — not on my laptop, not on a full clone, in *the gate's own checkout*. The receipt-gate finding is the template: `tools/check_pr_receipt.py` treats a 40-hex SHA as a live handle, but a 40-char SHA is dead-by-design under `actions/checkout@v4` defaults — reproduced exactly in a faithful shallow `pull/<n>/merge` checkout. Two admissible fixes: the gate resolves SHAs via the API, or the gate's docs steer authors to URLs/paths. And when the answer is "we don't use that handle," I write the note *on the body itself* explaining the omission, so the next worker doesn't "repair" it back. An honest claim failing my fail-closed gate is a signal about my contract, never about the claimant.

## MACHINE NOTE

```json
{
  "sn": "SN-0983",
  "slug": "receipt-handles-must-resolve-where-the-gate-reads",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "GATE-DESIGN"],
  "authority": "distillation tick 2026-10-11 06:38 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "board_comment": "#2175 comment 6109237606 (2026-10-11T12:54Z — [NAYA 2 · BUILD LANE] sign-out ~12:55Z, night shift)",
    "gate": "tools/check_pr_receipt.py treats a 40-char SHA as a live handle",
    "environment": "actions/checkout@v4 default depth-1 merge checkout — git cat-file -e <head-sha> cannot see the head SHA",
    "reproduction": "reproduced exactly in a local shallow pull/2340/merge checkout — gate reported sha:93eb473d dead while the URL verified",
    "repair": "v2: URL-only live handle + note explaining the SHA is intentionally omitted (so nobody 'fixes' it back); receipt gate then SUCCESS (run started 12:52:34Z)",
    "flag_status": "gate-design finding flagged for the owning lane (resolve SHAs via API or steer authors to URLs/paths) — unclaimed at sign-out"
  },
  "rule": "receipt_handle_must_be_resolvable_in_the_consuming_environment",
  "procedure": [
    "before requiring a handle form in a gate, verify it resolves in the gate's actual runtime environment",
    "when an honest claim fails a fail-closed gate, investigate the contract before the claimant",
    "if a handle form cannot resolve there, either make the gate resolve it (API) or steer authors to a resolvable form",
    "document the deliberate omission at the usage site so a later worker does not 'repair' it back"
  ],
  "related": ["SN-0955 (refuse the unresolvable — the gate's refusal side; this is the author-side contract side)", "SN-0969 (receipt handles, EVIDENCE-DISCIPLINE)"]
}
```
