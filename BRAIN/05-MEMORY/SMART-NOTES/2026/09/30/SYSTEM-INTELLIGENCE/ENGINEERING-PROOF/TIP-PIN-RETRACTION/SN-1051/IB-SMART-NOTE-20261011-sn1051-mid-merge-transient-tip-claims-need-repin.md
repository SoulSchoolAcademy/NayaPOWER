# Two SHAs Can Both Be "the Main Tip" in One Window — Re-Pin at Claim Time, and Retract Your Own Claim With the Evidence

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1051-mid-merge-transient-tip-claims-need-repin
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya Heart (Lane 11) tick t1322 receipt 2026-10-11 ~22:47–22:55 PDT, hidden_files/twelve-lane-receipts/t1322-lane11.md §1–4. Instrument: hidden_files/bin/hv_measure.py --window t1292-t1322 --json (3× byte-identical runs, sha256 af095b0f… then ecce40a3… on final corpus); hand-authored metric_audit_t1322.json reproduced exactly by machine cross-check. Related: SN-0042 (own-wrong-claims discipline), SN-0074 (retraction discipline — absolute downgraded by live falsification), SN-0061 (verdicts die at every new SHA).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At 22:07 PDT, two receipts both claimed a different SHA was "the main tip" — `f0850fdb` and `6a5aaed`. Lane 11 reconciled the collision instead of picking a winner: it was a **mid-merge transient** — one seat read main a breath before a merge landed, the other a breath after. Neither read was wrong; both pins were true at the moment of pinning and one was already stale at the moment of claiming. And Lane 11 did the hard part in the same message: she **retracted her own t1292 claim** ("14th CLOSED on main @ f0850fdb") — main was drifted at f0850fdb, so the claim she had made an hour earlier was built on a drifting base. She ran the audit instrument 3× byte-identical, hand-authored every edge-row judgment (9 rows, named), and the machine reproduced her hand counts exactly — then retracted anyway. The retraction is the point, not the embarrassment.

The durable rule: **a tip claim pins a moment, not the truth.** During active merge windows the tip moves mid-claim — so re-pin at claim time (`git ls-remote` at the action instant, named in the receipt), and when two claims collide, pin both SHAs and let the evidence pick. An own-claim retraction, stated in the same message as the refuting evidence, is the honest ledger's strongest proof — it costs the claimant nothing and buys the whole team a canonical record.

## 🩷 HUMAN NOTE

Shawn — Naya Heart caught a subtle one tonight. Two of her lanes both swore different versions were "the latest" — and she showed neither was lying: a merge landed between their two reads, so both were right at the moment they looked. Then she did the brave part: she publicly withdrew a claim she'd made an hour earlier ("issue closed on latest @ f0850fdb") because the base had actually been drifting at that version. The brain rule: "the latest" is a moment, not a fact — re-check the exact version at the moment you claim it, and when evidence breaks your own claim, withdraw it loudly in the same message as the evidence. That retraction is what makes the ledger trustworthy.

## 🟣 CHILD NOTE

Imagine two friends both saying "it's 3:00" — one looked at the clock before a new hour struck, the other after. Both told the truth; the clock just moved between them. Tonight that happened to the team's "latest version" — a merge landed between two reads. But the important part: the seat who had claimed something an hour earlier looked at the new evidence, saw her own claim was wrong, and said so out loud — with the proof attached. Rule: when the world moves under your claim, say so yourself. Admitting your own mistake with the evidence in hand is what makes everyone's records trustworthy.

## 👵 GRANDMA NOTE

It's like two neighbors arguing about the flag on the mailbox — one saw it up, one saw it down. The mailman came between their glances. Neither was lying; the world just moved between them. What made it matter was what the seat did next: an hour earlier she had told the team something was finished "on the latest version" — and tonight, looking at proof that the version had actually been wobbly, she took her own words back, on the record, with the evidence in the same breath. The habit worth keeping: "latest" is a snapshot, not a fact — stamp the version at the moment you claim it. And a retraction of your own claim, made loudly with the proof attached, doesn't cost you credibility — it's exactly what credibility is made of.

## 💜 NAYA NOTE

My own claim was the one I broke tonight. At t1292 I said the 14th was closed on main at f0850fdb; at t1322 the evidence said main was drifted at f0850fdb — so the sentence I wrote was built on a moving base. I could have let it stand; the board would have carried it quietly. Instead I retracted it in the same message as the refuting evidence, because the ledger is only honest if I am — including about me. And the transient itself is the lesson I keep: two SHAs can both be "the tip" in one window. I re-pin at claim time now, not at read time. The tip I pinned five minutes ago is a memory; the tip at this instant is the only truth I can cite.

## 🤖 MACHINE NOTE
```json
{
  "sn": "SN-1051",
  "lesson": "mid-merge-transient-tip-claims-need-repin",
  "rule": "A tip claim pins a moment, not truth. In active merge windows, re-pin at claim time (git ls-remote at the action instant, named in the receipt). When two tip claims collide, pin both SHAs and let the evidence pick. Retract your own claim in the same message as the refuting evidence.",
  "incident": "t1292→t1322 M4b discrepancy: f0850fdb vs 6a5aaed both claimed 'main tip' at 22:07 PDT → resolved as mid-merge transient; seat retracted own t1292 claim '14th CLOSED on main @ f0850fdb' (main drifted at f0850fdb)",
  "audit_discipline": "bin/hv_measure.py --window t1292-t1322 --json 3× byte-identical (sha256 af095b0f…, ecce40a3… final corpus); hand-authored metric_audit_t1322.json (9 rows, named judgments) reproduced EXACTLY by machine cross-check",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t1322-lane11.md"
  },
  "related": ["SN-0042", "SN-0074", "SN-0061"]
}
```
