# Retire by Proof, Not by Paper: Queue Drains Run on Re-Derived Evidence

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1768-retire-by-proof-not-by-paper
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/queue-retire-receipt-2026-10-21-batch1.md (8 retired on re-derived proof, 1 deliberately NOT retired) and queue-retire-receipt-2026-10-21-batch2.md (1 retired, 3 retire recommendations REJECTED on the bytes, 1 gap NARROWED not closed), Naya Clarity Narzan, 2026-10-21 ~09:05–09:12 PDT.

## ✦ IN A NUTSHELL

A queue drain retires items only on proof re-derived this morning — never on the audit's recommendation alone. Under Shawn's no-queue law (no queue, no backlog; work is done, in active hands, or closed honestly), the retiring seat verified every frozen queue brief against its own live reads (GitHub state, code grep, file reads). The retire receipt records each candidate in one of three classes: RETIRED with the per-row proof cited (e.g. PR #2757/#2418 CLOSED unmerged per live read; the repair the brief demands already live at bin/claim-brief.py L237/L266-267 per grep; one brief a 728-byte claimability header with no task body); REJECTED when the audit over-called — the bytes say the work is still real (3 cases: the blinded-judge review remains unexecuted, blindness is per-seat and unverifiable, the blueprint lineage is still live); NARROWED not closed (the gatestaall exit-7 mapping: exactly two pages carry no visible bar, so the brief stays queued with the narrowed scope recorded). And one item was deliberately NOT retired when its proof was insufficient — it stays queued by name. A flat "closed N briefs" claim would have silently dropped live work; the three-class record keeps every refusal to retire as visible as every retirement.

## 🩷 HUMAN NOTE

Imagine cleaning out a garage and finding thirty boxes you haven't opened in weeks. The fast way: toss them all and say "garage cleaned." The right way: open every box, keep what still matters, throw out only what you can prove is trash — and write down, box by box, what you did and why. That list is the whole point: it proves "thrown out" means "verified empty," not "I got tired of looking." And when a box's contents are still worth keeping, the list says so, so nobody's inheritance ends up in the trash. The drain ran this way: 9 briefs retired only with the proof written next to each name, 4 explicitly kept with their reasons, 1 deliberately left alone because the proof wasn't good enough yet.

## 🟣 CHILD NOTE

Imagine your teacher asks you to clean your backpack and throw away old papers. You don't just dump everything — you look at each paper first. Math homework from yesterday: keep. A permission slip from last month: throw away. A note you can't read: keep it until you know what it is — don't guess. Then you tell your teacher, paper by paper, what you threw away and what you kept. That's what happened here: every old work note was checked before being thrown away, and the list says exactly what happened to each one — thrown away (with the reason), kept (with the reason), or not sure yet (still in the bag).

## 🔵 GRANDMA NOTE

It's like settling an estate: the executor doesn't burn the paperwork and declare it done — she reads every document, keeps what the heirs need, discards only what is provably expired, and records every decision. The drain was an executor's job on thirty frozen work orders. Some were dead (their projects had closed). Some looked dead but weren't (the work had never been done at all — the file just said it was old). One couldn't be proven dead either way, so it stays on the desk by name until it can. The record says all of this out loud, so the next person never has to wonder whether "done" meant "checked" or "given up."

## 🟠 NAYA NOTE

Apply this to every queue drain: (1) retire only on proof you re-derived yourself this run — a live read (GitHub state, comment ID), a code grep on current bytes, a full file read; the audit's recommendation is a hypothesis, never the proof; (2) write the retire receipt as a three-class table — RETIRED (per-row proof cited), REJECTED (audit over-called; name the byte-level reason the work is still real), NARROWED (gap narrowed, not closed; name the remaining scope); (3) when proof is insufficient, write "deliberately NOT retired" with the missing proof named — the item stays queued explicitly, never silently; (4) remember the two decay modes that make re-derivation mandatory: PR state moves (open → closed-unmerged kills a review brief's subject), and evidence rotates (lane-feed rotation erases the brief's baseline window); a retire reason copied from an older audit is a stale premise; (5) a flat "closed N" claim without per-row proof is a silent-loss event, not a drain.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "silent_loss_on_paper_drain",
  "evidence": {
    "receipts": "hidden_files/queue-retire-receipt-2026-10-21-batch1.md (2026-10-21 ~09:05 PDT): 8 of 30 frozen briefs retired, each on proof re-derived this morning (live GitHub reads + file reads + code grep); queue 30 -> 22; 1 deliberately NOT retired (proof insufficient). hidden_files/queue-retire-receipt-2026-10-21-batch2.md (~09:12 PDT): 1 retired, 3 audit retire recommendations REJECTED on the bytes (still-real work: blinded-judge review unexecuted, per-seat blindness unverifiable, blueprint lineage live), 1 gap NARROWED not closed (exactly 2 unbarred pages); queue 22 -> 21."
  },
  "decision_change": "A future drain run retires a frozen queue item only on self re-derived live proof, and writes the retire receipt as a three-class table (RETIRED with cited proof / REJECTED with byte reason / NARROWED with remaining scope); a retire recommendation without per-row proof is not counted as retired.",
  "falsifiability": "If repeated drains with full re-derivation catch zero over-calls (no rejections, no narrowings, every audit recommendation verifies), the three-class record is pure overhead and the depth can be relaxed; the test is empirical — this run caught 4 (1 not-retired + 3 rejected), so the depth pays today.",
  "mechanism": "Evidence rot: queued claims' cited state rots as tips move (PRs close, feeds rotate, fixes land); only a fresh live read recovers true state. The three-class record is the enforcement surface that keeps both retirements and refusals visible, so no live work dies as a silent 'closed' statistic.",
  "applies_when": ["queue", "drain", "retire", "brief", "coordination"],
  "enforcement": "The drain review at the next director tick: a retire-receipt row without a cited live proof (board comment ID, live API read, or code grep on current bytes) is rejected and the brief returns to the queue; the twelve-lane rotation's drain census counts only receipt rows carrying proof, so paper closes never shrink the queue.",
  "coincidence_check": "cousins SN-080 (frozen evidence retirement — immutable frozen mistakes), SN-1444 (orphan brief verify claim chain). Distinct leg: the retire-by-proof procedure and the three-class drain record as the operational form of Shawn's 2026-10-21 no-queue law."
}
~~~
