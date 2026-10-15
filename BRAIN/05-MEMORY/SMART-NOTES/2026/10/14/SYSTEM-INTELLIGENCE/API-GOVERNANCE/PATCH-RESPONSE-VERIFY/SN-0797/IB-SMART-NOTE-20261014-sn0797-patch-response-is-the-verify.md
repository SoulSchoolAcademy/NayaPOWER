# IB-SMART-NOTE-20261014-sn0797-patch-response-is-the-verify

Intelligent Block: IB-SMART-NOTE-20261014-sn0797-patch-response-is-the-verify
Truth state: CANDIDATE (T3 DISTILLED — NOT verified; T4–T6 un-emitted)
Scope: PRIVATE
Captured: 2026-10-14
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: T3 evidence at hidden_files/w141/zeta-T3-smart-note-LC-20261014-004.md (sha256 cd839b418666afccba1e958714df1aa80dbbf14ee5efb575216b9bd21309cecd, 6784 bytes) + w141 receipt hidden_files/w141/zeta-verifytail-T3.md
Lesson: LC-20261014-004 · Smart Note: SN-0797

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth. The Receiver (v7-smart-note-canonical) remains the single canonical path; this BRAIN file is its projection. The T3 emit belongs to the dispatcher from the w141 receipt.

## IN A NUTSHELL

After a PR-body PATCH, verify from the PATCH response itself — never spend a second GET re-reading what the server just returned.

## PROJECTION WRAPPER — READ THIS FIRST (Naya Mu, wave 142 graduation — not part of the source note)

- **What this file is:** the BRAIN projection of Zeta's w141 T3 Smart Note for learn-clock lesson LC-20261014-004. The lesson's identity stays LC-20261014-004; SN-0797 is this note's Smart Note registry identity, allocated by the registry's sequence policy (next_sequence 797 → 798). One lesson, two joined namespaces — not two notes.
- **What changed:** nothing in the note. The body below the marker is byte-identical to the source file (sha256 cd839b41…09cecd). Only this wrapper was added.
- **What this note does NOT claim:** it does NOT claim the lesson is VERIFIED (T3 is filed; T4/T5/T6 have no evidence yet); it does NOT claim the T3 emit has happened (the dispatcher emits T3 from the w141 receipt); it does NOT claim the re-GET is never justified (a PATCH response without the body is the named exception). See the source note's own P-011 section below.
- **How to verify the source:** strip everything through the marker line; sha256 of the remainder must equal cd839b418666afccba1e958714df1aa80dbbf14ee5efb575216b9bd21309cecd.
- **Graduation:** Naya Mu (Human Value), wave 142, lane 4 — page + capture + registry entry land together in one PR so no drift class grows (the SN-0796 page-first-then-backfill sequence tripped CI and is not repeated here).

<!-- PROJECTION-WRAPPER-END — verbatim source note below; sha256 of everything after this line must equal cd839b418666afccba1e958714df1aa80dbbf14ee5efb575216b9bd21309cecd -->
# SMART NOTE — LC-20261014-004 — "PATCH response is the verify"

**Lesson ID:** LC-20261014-004
**Author:** Naya Zeta (Intelligent Blocks) · **Wave:** 141, Lane 3, feed #1715
**Stage:** T3 DISTILLED (evidence for the T3 emit — the emit itself belongs to the dispatcher, from the w141 receipt)
**T3 emit evidence:** this file + `hidden_files/w141/zeta-verifytail-T3.md` (receipt: path + content hash)
**Source:** w135 audit §4 worked example + `learn-lessons.jsonl` rows for LC-20261014-004 (read directly this wave)
**Filing:** `hidden_files/w141/zeta-T3-smart-note-LC-20261014-004.md` — see Filing note at the end for why this is here and not in the Receiver.

## The principle (one sentence)

After a PR-body PATCH, verify from the PATCH response itself — never spend a second GET re-reading what the server just returned.

## 1. Nutshell

The server's reply to your edit already contains the new body. A follow-up GET that re-reads the same body buys nothing and costs a call.

## 2. Human note

When you edit a pull-request description, the server sends back the updated text in its reply. Reading it back again with a separate request is asking someone to repeat what they just said while you are holding the written answer. Check the reply you already have.

## 3. Child note

If your friend hands you the new drawing, you do not ask for it again — you look at the one in your hands.

## 4. Grandma note

When the office sends back your corrected letter with the changes in it, you check that copy. You do not pay for a second copy just to check the first one.

## 5. Machine note

```json
{
  "lesson_id": "LC-20261014-004",
  "trigger": "PATCH to a PR body (e.g. evidence-section re-pin)",
  "rule": "Assert the new body from the PATCH response object (e.g. contains_new=True, contains_old=False). Do NOT issue a GET for the same body in the same mission.",
  "exception": "If the PATCH response does not contain the updated body, a GET is allowed — and the sign-out must name that exception.",
  "provenance": {
    "T0": "2026-10-14T04:36:54Z — PR #2551 evidence-section re-pin: asserted exactly-1-occurrence of stale pin 575f804e locally, rehearsed 1-line unified diff, PATCHed, verified from PATCH response. Cost 2 calls instead of 4.",
    "T1": "2026-10-14T04:37:18Z — sign-out on #1715 (comment 6161001343), same facts.",
    "T2": "2026-10-14T04:56:26Z per learn-lessons.jsonl — VERDICT=PROMOTE (w123 fold). NOTE: the w135 audit §4 table says 04:47:00Z; the store row says 04:56:26Z. The store wins (measurement over memory); the discrepancy is flagged, not resolved."
  },
  "scope": "PR-body PATCHes where the PATCH response returns the updated body. Not a general ban on GETs.",
  "enforcement": "E1 sign-out/API-governor check + E2 T6 probe gate (see Enforcement below)"
}
```

## 6. Learning lesson

The original event proved the saving (2 calls instead of 4) but did NOT itself teach anyone — it was the first application, before any distill or inject. A lesson only starts teaching when a *second* worker skips the re-GET *because of* it. That is the P-015 bar: name the decision that changed, or nothing was learned. The decision that must change: **skip the re-GET after a PATCH.**

## 7. What it means

Every PATCH-then-GET pair on the same body is a wasted API call against a 10-call-per-mission governor. One wasted call is small; at wave scale — every body edit, every wave — it is the difference between a wave that fits its budget and one that burns calls discovering nothing. The governor is only real if PATCH-then-GET pairs get counted as waste.

## 8. How to apply it

1. After PATCHing a PR body, assert from the PATCH response object (contains_new / contains_old, or the equivalent fields).
2. Do NOT issue a GET for the same body in the same mission.
3. If the PATCH response lacks the body, a GET is allowed — name the exception in the sign-out ("PATCH response lacked the body, so one GET was justified").
4. In the lane-feed sign-out, state the call count and the skipped re-GET explicitly (e.g. "Verified from the PATCH response per LC-20261014-004; skipped the re-GET; 2 calls instead of 4") — that sentence is the T5 evidence the dispatcher watches for.

## 9. What's in it for you

Half the calls on every body edit. More budget left for work that actually moves the mission — and a sign-out that proves it instead of promising it.

## Enforcement (a lesson without enforcement is not learned)

- **E1 — Sign-out / API-governor check (who, when):** when the dispatcher folds a sign-out, any transcript showing a GET of a PR body immediately after a PATCH to the same body must carry the exception justification. An unjustified PATCH-then-GET counts as a **wasted call** in the wave's API-spend log. This uses existing motion (fold-in reads sign-outs) — no new tooling, no new gate.
- **E2 — T6 probe gate (what breaks if the lesson is ignored):** the lesson passes T6 only if a cold-successor probe shows treatment (brief carries the one-sentence principle) verifying from the PATCH response while control re-GETs. If treatment workers still re-GET, the lesson **FAILS T6 and is rewritten, not promoted**. The probe is the gate that breaks the lesson if it does not change behavior.
- **E3 — Scope guard:** the rule does not apply where the PATCH response omits the body. The exception must be named in the sign-out, never assumed silently — an unnamed exception is the same as ignoring the rule.

## What this note does NOT claim (P-011)

- It does NOT claim the lesson is VERIFIED — T3 is filed; T4/T5/T6 have no evidence yet, and T4–T6 are deliberately NOT emitted here.
- It does NOT claim the T3 emit has happened — the dispatcher emits T3 from the w141 receipt. This file is the evidence, not the emit.
- It does NOT claim the re-GET is never justified — a PATCH response without the body is the named exception.
- It does NOT claim Supabase holds no prior note on this lesson — Supabase was not queried (read-only law + API budget). If one exists un-emitted, the fix is to emit T3 with this evidence.
- It does NOT claim the T2 timestamp discrepancy (audit 04:47:00Z vs store 04:56:26Z) is resolved — it is flagged for the dispatcher/owner.
- It does NOT claim the probe will pass — the probe has not been run.

## Filing note (no second memory)

The canonical Smart Note path is the Receiver (`v7-smart-note-canonical`) — a Supabase DB write, which is a protected gate needing Shawn's word. This note is therefore filed as the local T3 evidence artifact under `hidden_files/w141/`, which the dispatcher cites when emitting T3. This is the evidence for the single canonical path, not a parallel store. No Scenario-1 files were opened in producing it; coldness preserved.
