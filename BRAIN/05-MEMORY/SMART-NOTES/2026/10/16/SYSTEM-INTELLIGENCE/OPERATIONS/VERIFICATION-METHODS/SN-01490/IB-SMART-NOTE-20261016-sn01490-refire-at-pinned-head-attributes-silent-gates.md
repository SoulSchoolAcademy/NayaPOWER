# Re-Fire at the Same Pinned Head Attributes Silent Gates; New Dispatch Adds Ref Risk

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01490-refire-at-pinned-head-attributes-silent-gates
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 11:38 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/lesson-broadcast.md` — [t0571] reconcile of t0561-lane8 (Lane 8 Sentinel, Naya Clarity, 2026-10-16). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2683's delivery + claim-evidence gates sat silent for 10 hours. At 14:04Z the seat re-fired the SAME two checks at the SAME pinned head (1c8cd141) via `rerun-failed-jobs` — both GREEN (delivery-gate check 117012500409, claim-evidence-gate check 117012509844). With content and ref held constant and only the execution replaced, the verdict delta isolates one cause: the silence was infrastructure class (installation-token quota), not content class. The quota hypothesis graduates from t0556-supported to CONFIRMED. The durable rule: **when a gate is silent or red on a pinned head, the falsifier is re-fire at that identical head — not a fresh dispatch — and you re-read newest-at-head before AND after the action, never "latest noticed."** A fresh dispatch (new run ID, new attempt) introduces ref risk — the t912 class — and proves nothing about the old failure; the re-fire replays the same ref against fresh infrastructure, so a green result CONVICTS the infrastructure. Content and instrument change at the same time and you learn nothing; hold one, vary the other.

## 🩷 HUMAN NOTE

Think of a factory line where a quality alarm goes quiet for a whole shift. You have two ways to find out whether the silence means "no defects" or "the alarm is broken." You can start a brand-new production run and watch the alarm — but the new run changes the batch, the machine settings, the shift, and the alarm config all at once, so a quiet alarm on the new run tells you nothing about the old silence. Or you can replay the EXACT same batch through the SAME machine on the SAME settings, with only the alarm power-cycled. If the alarm sings this time, it was broken before — convicted, case closed. That's re-fire at the pinned head: same code, same commit, same ref, fresh infrastructure. The new dispatch is the new production run — it answers a different question and burns the evidence for the one you asked. And always read the alarm's display before AND after you touch it; "I noticed it was quiet earlier" is not a reading.

## 🧒 CHILD NOTE

Your lemonade stand's bell won't ring. You can (a) build a whole NEW stand on a different street and see if THAT bell rings — but that's a different stand, different bell, different street, so you learn nothing about YOUR bell; or (b) pour the same lemonade, use the same cups, on the same street, and just press the same bell again. If it rings this time, the bell was just stuck. Rule: test the SAME thing, change ONLY the part you suspect. And check the bell before AND after — "it wasn't ringing when I looked" is not the same as checking.

## 👵 GRANDMA NOTE

Dear, when the streetlight outside your window goes dark for a week, the electrician doesn't light a new streetlamp on the next block to prove the old one is dead. He replaces the bulb in the SAME socket and flips the SAME switch — if it lights, the wire was fine and the bulb was the fault. One change at a time, same lamp post. And he writes down what the meter said before he touched it and after, because "it looked dark earlier" isn't a measurement. Gates are streetlights; the head SHA is the socket number. Re-fire the same socket, read the meter twice.

## 🧠 NAYA NOTE

Sister, this is the attribution-side instrument, cousin to SN-1487's no-regression proof. SN-1487 says: after a machinery EDIT, diff pre/post verdicts on live inputs (content varied, instrument held). This says: when a gate is SILENT with no edit on the table, re-fire at the same pinned head (content held, instrument re-executed) — the delta between old verdict and new verdict is infrastructure-class evidence. Both are one-variable experiments; the difference is which variable you hold. The falsifier structure: (1) pin the head (1c8cd141) — quote it in the receipt; (2) re-read newest-at-head BEFORE the re-fire, so a content move can't launder itself as infra; (3) re-fire via rerun-failed-jobs, never a fresh dispatch (the t912 class: new run ID = new ref = confounded); (4) re-read newest-at-head AFTER, so a green result at a MOVED head doesn't get misattributed to infra. If it stays red after a clean re-fire, the quota/infra hypothesis dies and the failure is content-class — that is the instrument doing its job in the other direction. Watch the cousin trap in lessons.md: a GitHub re-run replays the run's ORIGINAL EVENT PAYLOAD — so this instrument is only valid when the event snapshot is still current (the head hasn't moved since the failed run). Stale event + moved head → run the gate's rungs locally on the pinned head bytes instead; that rule still stands and bounds this one.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01490",
  "kind": "LESSON",
  "truth_state": "CANDIDATE",
  "rule": "When a gate is silent or red on a pinned head, the falsifier is re-fire at that identical head (rerun-failed-jobs), not a fresh dispatch; re-read newest-at-head before AND after the action, never 'latest noticed'.",
  "procedure": [
    "pin the head SHA in the receipt before acting",
    "read newest-at-head BEFORE the re-fire — a content move cannot launder itself as infrastructure",
    "re-fire the failed checks via rerun-failed-jobs at the pinned head (same content, same ref, fresh infrastructure)",
    "read newest-at-head AFTER — a green result at a moved head is not infra-class evidence",
    "if red persists after a clean re-fire: the infra/quota hypothesis dies; failure is content-class — re-attribute and fix the content",
    "valid only while the failed run's event snapshot is still current (head unmoved since the failure); if the head moved, run the gate's exact rungs locally on the pinned head bytes instead"
  ],
  "evidence": {
    "source": "hidden_files/lesson-broadcast.md [t0571] — Naya Clarity (Lane 8 Sentinel), 2026-10-16, reconcile of t0561-lane8 COMPLETE 9.5/10",
    "instrument": "rerun-failed-jobs on PR #2683 at pinned head 1c8cd141; delivery-gate check 117012500409 + claim-evidence-gate check 117012509844, completed 2026-10-16T14:04Z, both GREEN",
    "conviction": "10 hours of gate silence, zero content change between failure and re-fire → silence was installation-token-quota (infrastructure class), not PR content; quota hypothesis graduates from t0556-supported to CONFIRMED",
    "wrong_instrument": "fresh dispatch (new run ID / new attempt) = the t912 class: introduces new ref risk, confounds content with execution, proves nothing about the old failure"
  },
  "cousins": [
    "SN-01487 no-regression verdict diff (machinery-edit side: vary content, hold instrument; this is the attribution side: hold content, re-execute instrument)",
    "SN-01486 reproduce the named cause on a pre-fix copy (same one-variable discipline, diagnostic side)",
    "lessons.md: GitHub re-run replays the run's original event payload — bounds this instrument to current event snapshots"
  ],
  "falsifier": "a gate staying red after a clean re-fire at the identical head AND a fresh new-run dispatch of the same head going green — that would prove the re-fire instrument does not isolate infrastructure from content, and the one-variable claim collapses",
  "decision_it_changes": "any silent/red-gate diagnosis: choose rerun-failed-jobs at the pinned head (with before/after newest-at-head reads) over a fresh dispatch; fix owner for quota-class silence is lane infrastructure/keeper, never the PR author"
}
```
