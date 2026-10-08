# Deployment Authorization Expires at the SHA — Re-Anchor Before the Window

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0475-deployment-authorization-sha-expiry
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A production-dispatch authorization is bound to the exact main SHA it was measured on — it is a (sha, scope, window) triple, never a blanket permission. The moment main moves, the authorization lapses. Before any authorized production window, re-anchor the exact current main SHA from the live API and close every agent-movable prerequisite on the promotion ticket; never act on an earlier authorization.

## 🩷 HUMAN NOTE

A green light given yesterday does not prove today's code. Shawn's word attaches to the exact commit he approved — the exact bytes he reviewed. If main moved since then, even by one commit, that "yes" no longer covers what's there. Deploying under a stale authorization is deploying unreviewed bytes on borrowed permission. So the rule is simple: every time the production window opens, look up the real current main SHA first, and if it isn't the SHA that was authorized, the authorization has to be re-earned.

## 🟣 CHILD NOTE

A permission is for the exact thing you checked. If the thing changed, ask again.

## 🔵 GRANDMA NOTE

If you approved a recipe but the cook changed the ingredients overnight, taste it again before serving — you approved the old dish, not the new one.

## 🟠 NAYA NOTE

Bind every production authorization to its exact tip SHA; record the triple (sha, scope, window) in the receipt. At execution time, re-fetch `refs/heads/main` live and compare — mismatch means stop, re-verify, and re-obtain the authorization. Never cite an authorization recorded against an older SHA.

Evidence: #1354 comment 6023536043 (NAYA 1 Cold-14 / 10-10 execution audit, 2026-10-06): "Re-anchor the exact current main SHA again immediately before the next authorized production window and close every agent-movable prerequisite on #1593; do not reuse any earlier deployment authorization."

## 🟢 MACHINE NOTE

~~~json
{
  "rule": "deployment-authorization-sha-expiry",
  "authorization_tuple": ["sha", "scope", "window"],
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "procedure": [
    "resolve refs/heads/main via live API immediately before the window — never from memory or an earlier comment",
    "compare resolved SHA against the SHA named in the authorization record",
    "if mismatch: halt dispatch, re-verify the new tip, re-obtain authorization",
    "record (sha, scope, window) in the dispatch receipt"
  ],
  "prohibited": [
    "reusing an authorization measured on an older tip SHA",
    "resolving main from a cached SHA, a stale comment, or a local ref"
  ]
}
~~~

## 🟢 LEARNING LESSON

Main moves constantly and silently. An authorization that was correct at 10:00 can be incorrect at 10:30 for reasons nobody intended — merges, rebases, and other lanes' landings all change the bytes. The safety rule must therefore be structural (re-anchor at the window), not behavioral (remember to be careful).

## 🟡 WHAT IT MEANS

This is the mirror image of SN-0438: there the promotion gate correctly fired because the tip was knowingly RED; here the authorization correctly lapses because the tip moved. Together they make promotion evidence monotonic — only the exact authorized bytes can move forward.

## ⚪ WHAT'S IN IT FOR YOU

No accidental production of unreviewed bytes; no wasted windows spent debugging a deployment that was never authorized; a clean receipt that names the SHA the authorization covered.

## 🟨 HOW TO APPLY / HOW TO USE

Before any production dispatch: `gh api repos/<repo>/git/refs/heads/main`, compare the SHA, and only proceed on exact match with the authorization record. Any mismatch = new authorization required.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-0438 — Fail-Closed Is the Design Working (gate firing on RED tip)
- **REFINES** → SN-0350 — A Deploy Stamp Is Not Behavioral Evidence
- **SUPPORTS** → SN-0363 — Atomic Promotion Rule (validation precedes the pointer move)
- **SUPPORTS** → Scorecard Law merge protocol — merges run under protocol, promotion still needs the window check
- **IMPLEMENTS** → Human Director gate on production dispatch (#1593)

## 🧭 KEY DECISIONS / PRINCIPLES

- An authorization is (sha, scope, window) — a triple, never a blanket.
- The re-anchor read must come from the live API at the window, never from memory, an earlier comment, or a cached local ref.
- Closing agent-movable prerequisites on the promotion ticket is part of the window preparation, not optional.
- This rule does not narrow Shawn's authority — he can re-authorize instantly; it only prevents stale reuse.

## 🧾 PROOF / PROVENANCE

- Board: SoulSchoolAcademy/NayaPOWER issue #1354, comment 6023536043 (NAYA 1 Cold-14 / 10-10 execution audit, 2026-10-06T19:09:40Z)
- "One next action" line: "Re-anchor the exact current main SHA again immediately before the next authorized production window and close every agent-movable prerequisite on #1593; do not reuse any earlier deployment authorization."
- Related promotion ticket: #1593 (production dispatch — Human Director gate)

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

CANDIDATE: captured as a durable lesson from Naya 1's audit instruction; not yet ratified as machine law by Shawn. The rule's behavioral effect (future dispatches re-anchoring) is the evidence that will strengthen it.

## ➜ NEXT ACTION / SUCCESS CONDITION

Apply at every production window: live re-anchor, triple recorded, mismatch → re-authorize. Verify resulting receipts name the exact SHA.
