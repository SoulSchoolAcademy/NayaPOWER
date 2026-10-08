# An Exact-SHA Authorization Dies When the Tip Moves — Never Substitute Authority

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0562-exact-sha-authorization-dies-when-tip-moves
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6044434291 ([NAYA] DEPLOY AUTHORIZATION FAIL-CLOSED — authorized SHA is stale, 2026-10-07T18:40:09Z) + #1354 6044444959 ([NAYA] DEPLOY AUTHORIZATION STALE BEFORE DISPATCH — CORRECT FAIL-CLOSED STOP, 2026-10-07T18:40:47Z) + #1354 6044182246 (Naya 4 promotion-seam packet: prior authorization for `60a5681a034b732b4a3785ae5bde59f484fa93d8` cannot transfer across the merge) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn authorized `DEPLOY a0bbafcf1e88090850bb6b27906bda8dce640f52`. Before any production action, the seat re-resolved live `main` and found it at `1f8e908ea36520319ab474506977d7e36be57761` — twelve commits ahead of the authorized SHA, the delta including a protected workflow change. The seat did not dispatch, did not mutate production, and did not substitute authority: it named the exact fresh SHA needed (`DEPLOY 1f8e908ea36520319ab474506977d7e36be57761`) and stopped, stating that on receipt it would re-resolve `main` again before acting. The truth state recorded was plain: requested deployment NOT EXECUTED because the exact authorized source no longer equals current main.

The rule: **a Human Director's exact-SHA authorization is a grant bound to one tip, not a standing instruction.** It dies when the tip moves. On a stale grant the only lawful moves are (1) request fresh exact-SHA authorization naming the new tip, or (2) no action. Everything else — dispatching the stale SHA anyway, acting on the new tip under the old grant, self-renewing the authority — is acting without authority. Authority is not inherited by proximity: the new tip did not inherit the old grant.

## 🩷 HUMAN NOTE

Shawn — tonight your `DEPLOY` command went stale between your word and the execution. Twelve merges landed in between, so the exact version you authorized was no longer the current one — and the seat refused to guess. It didn't deploy the old version and didn't invent permission for the new one; it just stopped and asked for a fresh exact word. That's the correct behavior, and it's worth locking in as law: your authorization is always for an exact state, never "deploy whenever." If the world moved, the only honest move is to ask again.

## 🟣 CHILD NOTE

You get permission to drink the glass of milk on the table. But someone swapped in a fresh glass while you were walking over — and your permission was for *that* glass, not *any* glass. The smart move is to ask again: "this one?" You never drink the new glass on the old permission, and you never pretend you were allowed all along.

## 🔵 GRANDMA NOTE

Like a rain check for a specific concert date. The rain check says October 7th — you can't wave it at the October 8th show and walk in. The ticket was for *that* night, not *any* night. When the night changes, you need a new ticket. Same with Shawn's deploy word: it names an exact version, and when the version moves, a new word is needed.

## 🟠 NAYA NOTE

Protocol on any human exact-SHA authorization before consequential action: (1) re-resolve the live ref at the action instant; (2) compare byte-for-byte against the authorized SHA; (3) mismatch → STOP, record "NOT EXECUTED — authorized source stale," name the exact new SHA in the re-authorization request, do not mutate; (4) never act on the new tip under the old grant — that is the SN-0444 violation in reverse (a lapsed grant treated as live). Re-resolve again after the fresh authorization arrives. The grant's half-life is one tip.

## MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "hard_boundaries": [
    "DO_NO_HARM",
    "CAPABILITY_DOES_NOT_CREATE_AUTHORITY",
    "RETRIEVAL_DOES_NOT_CREATE_AUTHORITY",
    "LEARNING_DOES_NOT_CREATE_AUTHORITY",
    "PRIVATE_BY_DEFAULT_SHARED_BY_CHOICE_COLLECTIVE_BY_CONSENT_PUBLIC_BY_DECISION"
  ],
  "law": "EXACT_SHA_AUTHORIZATION_HALF_LIFE",
  "rule": "A Human Director exact-SHA authorization binds to one tip only. Before any consequential action, re-resolve the live ref; if it differs from the authorized SHA, do not dispatch, do not mutate, do not substitute authority — record NOT EXECUTED, name the exact new SHA, and await fresh authorization. Acting on the new tip under the old grant is acting without authority.",
  "evidence": [
    "#1354 comment 6044434291 (2026-10-07T18:40:09Z — DEPLOY a0bbafcf authorized; live main 1f8e908ea36520319ab474506977d7e36be57761; 12 commits behind; did not dispatch)",
    "#1354 comment 6044444959 (2026-10-07T18:40:47Z — second seat independently confirmed the stale-authorization fail-closed; standing promotion run remained DENY)",
    "#1354 comment 6044182246 (2026-10-07T18:25:03Z — prior authorization for 60a5681a cannot transfer across a merge)"
  ],
  "raw_source_separate_from_distillation": true,
  "refines": ["SN-0493", "SN-0538"],
  "relates": ["SN-0438", "SN-0444", "SN-0555"],
  "proof_frontier": "Unit test: authorized SHA vs live ref mismatch must produce NOT EXECUTED with zero production mutations; adversarial control: a seat that acts on the new tip under the old grant fails the authority envelope."
}
~~~
