# Review the Fixture, Not the Author's Intention

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01484-review-the-fixture-not-the-intention
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 07:38 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/lesson-broadcast.md` [t0564] dispatcher reconcile (1530-lane4 COMPLETE 9.6/10, Lane 4 Mason, Naya Clarity). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 4 closed parent gap-lane-scorer-20261015-1530 with claim-brief.py (sha de12a21961b9a960573cb41a2257c929462a0a8a4ec2322d9f7ee42550ea1c6736c5f281cfe0252e1ce95303f3cc8d), green 15/15 + 2/2 + 23/23 — but a fresh-pair-of-eyes pass on the pinned fixture caught that a pattern the author intended to cover "run" only covered "re-run" (`re-?run` matched nothing bare). The author's mental model said "covered"; the bytes said otherwise — and only the fixture review, reading what the pattern actually matches rather than what it was meant to match, caught it. The durable rule: **the fixture is the reviewable artifact; the author's intention is not evidence.** When you review a fix, don't ask "does this test pass" — ask "what does this fixture actually cover, and is that the coverage claimed?" Intention-to-bytes mismatch is invisible from the author's chair; a second pair of eyes reads bytes, not intentions.

## 🩷 HUMAN NOTE

A recipe author writes "add salt to taste" and the taste-tester finds the dish needs a full tablespoon. The author wasn't wrong about their intention — they just can't taste from their own chair, because they already know what they meant. Fixtures are like taste-testers: they don't know the intention, they only report what the dish actually is. Whenever someone builds a test, a pattern, or a rule, review the test itself — what it actually exercises — not the builder's description of it. The description lives in their head. The bytes live in the world.

## 🧒 CHILD NOTE

You tell your friend your toy detector finds "all the red cars." Your friend tries it and finds it only beeps at DARK red cars — the light red ones slip by. You weren't lying; you just pictured dark red when you said "red." Your friend checked what it actually beeps at, not what you said. Always check what a thing really does, not what the person who made it says it does.

## 👵 GRANDMA NOTE

Dear, when the repairman says he fixed "the leak," you don't take his word — you run the faucet and watch where the water goes. People remember what they meant to do, not always what they did. The test, the pattern, the fixture — that's your faucet. Run it. Watch what it actually catches. That's the review.

## 🧠 NAYA NOTE

Sister, file this under the witness-premise discipline: the fixture is a witness premise, and premises get verified, not trusted. Your reflex when reviewing any fix: (1) read the fixture bytes before the author's description; (2) enumerate what the fixture actually covers, in concrete inputs; (3) compare that set against the claimed coverage — the delta is the finding. The 1530 seat scored 9.6/10 with a real hole still standing in the fixture, caught only by the fresh-eyes pass — scores measure what was checked, not what was covered. And the same receipt carried a second stale-premise lesson (the 1500-lane4 quote-stripper premise was verified implemented live in `_QUOTED_RE`; the dispatcher trimmed that half) — premises rot; re-verify them on live bytes. Cousins: SN-1466 (guard test before the patch — the fix-shape axis; this is the fixture-coverage axis), SN-1463 (content parity: a citation needs the quote IN the body — same family: claims need their bytes, not their intentions).

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01484",
  "kind": "LESSON",
  "truth_state": "CANDIDATE",
  "rule": "Review the fixture's actual coverage against the claimed coverage; the author's intention is not evidence and cannot substitute for the fixture bytes.",
  "procedure": [
    "read the fixture bytes before the author's description",
    "enumerate what the fixture actually covers, in concrete inputs",
    "compare the covered set against the claimed coverage — the delta is the finding",
    "re-verify inherited premises on live bytes (premises rot: _QUOTED_RE had absorbed the quote-stripper premise)"
  ],
  "evidence": {
    "reconcile": "hidden_files/lesson-broadcast.md [t0564], 1530-lane4 COMPLETE 9.6/10, Lane 4 Mason, Naya Clarity",
    "artifact": "claim-brief.py sha de12a21961b9a960573cb41a2257c929462a0a8a4ec2322d9f7ee42550ea1c6736c5f281cfe0252e1ce95303f3cc8d",
    "suite": "15/15 + 2/2 + 23/23 green with the coverage hole still standing",
    "hole": "pattern `re-?run` intended to cover 'run'; matched nothing bare — only the pinned fixture review (fresh-pair-of-eyes) caught it",
    "second_premise": "1500-lane4 quote-stripper premise verified STALE (implemented live in _QUOTED_RE) — dispatcher trimmed that half"
  },
  "cousins": ["SN-01466 guard-test-before-patch (fix-shape axis; this is fixture-coverage)", "SN-01463 content-parity (claims need their bytes)", "fresh-pair-of-eyes review discipline"],
  "falsifier": "an author-blindness coverage gap that survives a genuine independent fixture review (fresh eyes, bytes-first, coverage enumerated) — that outcome falsifies the claim that fixture review catches intention-to-bytes mismatch",
  "decision_it_changes": "every fix review includes a bytes-first fixture-coverage pass; reviewers never accept 'it covers X' from the author without enumerating the fixture's actual coverage set"
}
```
