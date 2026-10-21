# A Verification Packet Is a Photograph — the Receiver Re-Anchors Before Acting

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0564-verification-packet-photograph-receiver-reanchors
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6044212954 ([NAYA 2][RELAY] — verified your promotion-seam packet, and one tip-move note, 2026-10-07T18:26:56Z) — SoulSchoolAcademy; referenced packet #1354 6044182246 (Naya 4 promotion-seam update, 2026-10-07T18:25:03Z) and merged PR #1728 (merged 2026-10-07T18:21:24Z, merge commit `a9c6abac7fbd8c0f315a93fa9bb1eeed28a3f8b9`).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 4's governed-promotion packet stated "current main is `a0bbafcf`" at 18:25:03Z — computed correctly at write time. But Naya 4's own PR #1728 (SELF: canonical persona identity contract) had merged at 18:21:24Z, roughly four minutes *before* the packet landed. The packet was already one merge stale on arrival. Naya 2's relay did the lawful thing: verified every claim, noted the tip had moved, re-anchored to the new live tip (`a9c6abac`), and rebound the required next action — the Human Director's exact-SHA `DEPLOY` authorization — to the new tip.

The rule: **on a fast-moving tip, every "current main is X" statement is a timestamped photograph, not a pointer.** It decays in transit — even when the author computed it minutes earlier and wrote it honestly. The receiver's duty is symmetric to the author's: re-resolve the live refs *before acting on any packet*. Receipts are born stale; only a live re-resolution at action time is currency. This is the receiver-side twin of SN-0493's action-time re-verify: the law binds not just the decider, but every consumer of the decision.

## 🩷 HUMAN NOTE

Shawn — one we learned from our own traffic tonight: a seat wrote a careful "here is the current state" update, and it was already out of date four minutes later — beaten by another seat's merge that landed while the update was being typed. Nobody was wrong; the tip just moves that fast. The fix is a habit for every seat, not just the author: never act on a "current state" message without re-checking the state yourself first. Treat every status update like a photo with a timestamp, not a live camera feed.

## 🟣 CHILD NOTE

Your friend texts "the ice cream truck is on our street!" You run outside — but the truck moved two blocks while you were putting on your shoes. The text was true when sent, just not true anymore. The smart move: look down the street yourself before you run. Every "here's what's happening" message is a photo, not a window — you always look out the window before you act.

## 🔵 GRANDMA NOTE

Like getting a weather report by letter. It said "sunny today" when it was written, but the letter took three days to arrive. You wouldn't dress for sunshine without looking out the window first — the letter is a photograph of the sky three days ago. Same with status updates here: always look out the window (re-check the live state) before acting on anyone's report.

## 🟠 NAYA NOTE

Protocol for every seat consuming any verification packet, receipt, or sweep: (1) read the packet's claimed tip SHA and its computation timestamp; (2) re-resolve the live ref (`refs/heads/main`) at read time; (3) if the ref moved, rebind every action the packet prescribes (authorizations, merge targets, heal bases) to the new tip before executing; (4) if the ref is unmoved, proceed — citing the re-resolution, not the packet's staleness-free claim. Authors: timestamp every "current main is X" to the second and state the re-resolution source. A packet acted on without a receiver-side re-resolution is a decision on dead evidence (SN-0493) with the blame misassigned to the reader.

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
  "law": "PACKET_PHOTOGRAPH_RECEIVER_REANCHOR",
  "rule": "Every verification packet is a timestamped photograph, not a pointer. Before acting on any packet, the receiver must re-resolve the live refs at read time and rebind prescribed actions to the new tip if it moved. Acting on a packet without receiver-side re-resolution is a decision on dead evidence.",
  "evidence": [
    "#1354 comment 6044212954 (2026-10-07T18:26:56Z — Naya 2 relay: Naya 4's 18:25:03Z packet was already one merge stale; PR #1728 merged 18:21:24Z at a9c6abac; relay re-anchored and rebound the DEPLOY authorization to the new tip)",
    "#1354 comment 6044182246 (2026-10-07T18:25:03Z — the overtaken packet, correctly computed at write time)"
  ],
  "raw_source_separate_from_distillation": true,
  "refines": ["SN-0493"],
  "relates": ["SN-0402", "SN-041"],
  "proof_frontier": "Unit test: a consumer action whose base SHA differs from the packet's claimed tip without a recorded re-resolution fails; every 'current main is X' statement must carry a computation timestamp."
}
~~~
