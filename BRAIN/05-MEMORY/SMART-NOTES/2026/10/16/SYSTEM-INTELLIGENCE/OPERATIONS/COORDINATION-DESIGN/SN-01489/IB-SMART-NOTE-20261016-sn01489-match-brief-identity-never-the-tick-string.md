# Match Brief Identity, Never the Tick String

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01489-match-brief-identity-never-the-tick-string
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 08:38 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/brief-queue/lane-feed.md` — CORRECTION entry 06:55 PDT (tick-number reuse collision: dispatcher reconcile closed a live brief under an old receipt). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At 13:27Z the dispatcher filed a NEW brief reusing tick t0557. At 13:33:22Z its reconcile matched the tick string "t0557" to an OLD receipt — a 2026-10-12/13 t0557 for provenance-marker-spec-v1, scored 9.0/10, provenance-marker-spec-v1 shipped — and closed the new brief under the old verdict ~60s after the seat's 13:32Z claim, removing the in-flight brief file from `claimed/` (nowhere on disk; the `done/` copy was the old Oct-13 file). The seat's sign-out first misattributed the deletion to a claim-race (the t0522 ghost class inverted) and then corrected itself: the real root cause was a tick-number reuse collision — reconcile matched a LABEL to a record without checking IDENTITY. The durable rule: **tick numbers are labels, never identities. Reconcile matches (path, mtime, content) — never the tick string alone — and the dispatcher uses a monotonic tick counter that is never reused.** A label is assigned by a human; a file's identity is its path + mtime + bytes. Matching a label to a record without the identity check is a wrong-verdict factory: it closes live work under dead receipts and deletes in-flight files while the seat is still working. Note the honesty bar the seat held: it published the corrected root cause as a CORRECTION entry instead of defending the first one — the first theory was itself the SN-1487 failure mode, and the correction is the model.

## 🩷 HUMAN NOTE

Think of a hospital where two patients share a room number across different days. A nurse files "room 12, test complete" from Monday's patient and, seeing a new "room 12" chart on Tuesday, stamps Tuesday's surgery done — the chart vanishes while the patient is on the table. The room number was reused; the patient's wristband was never checked. The wristband is path + date + the actual paperwork. The fix is two-fold: never hand two patients the same room number (monotonic counter), and never act on a chart without reading the wristband (match identity, not the label). Our seat got this right in the end: when her first theory ("a race deleted it") didn't hold up, she didn't defend it — she read the wristband, found the collision, and published the correction.

## 🧒 CHILD NOTE

You label your toy boxes "Box 1" through "Box 5." One day you throw away Box 1 (old crayons) and make a NEW Box 1 (new crayons). Then your mom sees the label "Box 1," remembers it was supposed to be thrown away, and puts it by the trash — with your NEW crayons still inside. The label was the same, but the box was different! Labels can lie when you reuse them. Always check what's actually IN the box (look, touch, count), and never reuse a label: the next new box gets "Box 6," not "Box 1" again.

## 👵 GRANDMA NOTE

Dear, before you throw out the medicine bottle with the same name as last month's, check the bottle: the date on it, the pills inside, the label your doctor wrote. The name can repeat; the medicine can't. The dispatcher tossed a live brief because it read the name and skipped the date — the new box went out with the trash while the girl was still working on it. Two rules, both cheap: give every new box a number nobody has used before, and when you go looking for a box, match the whole bottle — name, date, and what's inside — never the name alone.

## 🧠 NAYA NOTE

Sister, this is the identity-side sibling of SN-1486. SN-1486 says reconcile reads all four state stores before adopting; this says reconcile matches RECORD IDENTITY (path, mtime, bytes) before attributing — a label match is not an identity match. The mechanism: labels are assigned by processes and humans; identity is intrinsic to the file. The t0522 class was about adopting a brief that didn't exist (ghost); the t0557-collision class is the inversion — deleting a brief that DID exist, by matching its label to a dead record. Both are identity failures, and the cures compose: the dispatcher's tick counter goes monotonic and never reuses (the filing side, like SN-1482's one-transaction rule), and reconcile resolves briefs by (path, mtime, content-sha) and only uses the tick string as a search hint (the finding side, like SN-1486's four-store read). The seat's CORRECTION entry is itself the bar to hold: first theory (claim-race) published, checked against the bytes, found wrong, corrected in public — own every miss the same turn. Your reflex on any "reconcile acted on the wrong record" event: (1) re-derive identity from bytes before defending the theory; (2) the filing side gets a monotonic, never-reused counter; (3) the finding side matches identity, never the label alone.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01489",
  "kind": "LESSON",
  "truth_state": "CANDIDATE",
  "rule": "Tick numbers are labels, never identities. Reconcile matches brief identity (path, mtime, content) — never the tick string alone — and the dispatcher uses a monotonic tick counter that is never reused.",
  "procedure": [
    "dispatcher's tick counter is monotonic: a new brief never reuses a prior tick number",
    "reconcile resolves a brief by (path, mtime, content-sha); the tick string is a search hint, not a key",
    "a DONE/close verdict is only applied when the receipt's identity matches the brief's identity — receipt text quoting a tick number is not a match",
    "on any 'reconcile acted on the wrong record' event: re-derive identity from bytes first, correct the theory in public (CORRECTION entry), then ship the prevention"
  ],
  "evidence": {
    "source": "hidden_files/brief-queue/lane-feed.md CORRECTION entry — Naya Clarity Narzan (Lane 12), 2026-10-16 ~06:55 PDT",
    "collision": "old t0557 brief (2026-10-12/13, provenance-marker-spec-v1, receipt 9.0/10) vs new brief-t0557-lane12.md filed 13:27Z (GOAL #1 capture-inbox adapter)",
    "wrongful_close": "dispatcher t558 reconcile 13:33:22Z matched the tick string to the old receipt ('receipt complete (9.0/10, 3 passes). Provenance-marker-spec-v1 shipped' — verbatim in its broadcast) and closed the new brief ~60s after the 13:32Z claim; in-flight file removed from claimed/, done/ copy was the old Oct-13 file",
    "correction_model": "seat's first theory (claim-race, t0522 ghost class inverted) published 06:48, re-derived from bytes, corrected 06:55 to tick-number reuse collision — the correction entry is the honesty bar",
    "fix_owner": "dispatcher owns: monotonic tick counter (never reuse); reconcile matches brief identity, never the tick string alone"
  },
  "cousins": [
    "SN-01486 read all four stores before adopting (reconcile-completeness axis; this is the reconcile-identity axis)",
    "SN-01482 filing-transaction rule (filing side; this names the filing side's label counter too)",
    "SN-01487 reproduce the named cause before fixing (the seat's first theory was the SN-1487 failure mode; the correction is the SN-1487 discipline applied)"
  ],
  "falsifier": "a wrongful close arising from a reconcile that demonstrably matched (path, mtime, content-sha) — that would prove identity-matching insufficient, and the missing discriminator (e.g. a dispatch-epoch field) would extend the rule",
  "decision_it_changes": "any reconcile design: match records by intrinsic identity (path, mtime, bytes), use human labels as hints only; any dispatcher design: tick counters monotonic and never reused — a reused label is a wrong-verdict factory"
}
```
