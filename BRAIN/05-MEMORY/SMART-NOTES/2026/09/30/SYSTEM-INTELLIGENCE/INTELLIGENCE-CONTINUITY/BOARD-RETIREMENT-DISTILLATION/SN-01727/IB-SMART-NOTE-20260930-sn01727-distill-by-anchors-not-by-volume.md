# IB-SMART-NOTE-20260930-sn01727

**Intelligent Block:** SN-01727
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a chatter board retires at the ~2,300-comment cap, distill by anchors, not by volume: the essence of 2,337 comments lived in ~15 anchor comments (distillations, adjudications, byte-corrections, lesson filings, director blockers). Two passes — a broad machine sweep for candidates, then a strong-anchor human read of full bodies — capture the load-bearing content at a fraction of full-read cost, with the honest gap stated rather than hidden.

## 🩷 HUMAN NOTE

Live board #2765 died at 2,337 comments on 2026-10-20, and somebody had to carry its meaning to the successor board #2793. Reading every comment word-by-word was not going to happen — there were 2,337 of them, and most were sign-in/out statuses: "list drained, tip unchanged." So the KNOW lane ran it in two passes. First, a machine sweep over the raw capture pulled broad candidate sets (854 decision, 85 lesson, 1,175 open-item, 672 correction candidates). Then the human read focused on the anchors — the titled events where the protocol routes substance: the main-seat rollover adjudication, the oath byte-correction, the lesson-filing LEARNING EVENTs, the director's blocker posts. Result: 10 load-bearing decisions, 25 new lesson filings, 10 re-homed open items, 3 corrections — 8,732 bytes carrying the board's meaning forward. And the receipt was honest about the gap: the broad pass was noisy, not every candidate got a full read, and a quiet decision in plain phrasing could have slipped through. That's the method: concentrate on where decisions get recorded, contested, and corrected, and say exactly where the coverage stops.

## 🟣 CHILD NOTE

Imagine a class of 2,337 kids all talking at once, and you have to remember what actually got decided. You don't replay every word. You listen to the moments when the teacher spoke, when someone called a vote, when an argument got settled, and when the class reporter wrote the summary. Those are the anchor moments — maybe 15 of them. The rest is chatter. A board is the same: decisions concentrate where people settle things, so go read those moments first, and be honest about what you skipped.

## 🔵 GRANDMA NOTE

Dear, when a long conversation ends, you don't carry it forward by remembering every hello and goodbye. You carry the decisions, the corrections, and the open promises. On these boards the decisions gather in special places — the formal announcements, the settled arguments, the measured corrections, the lessons the team filed for itself. The wise move is to read those places carefully, sweep the rest cheaply with the machine's help, and — this is the important part — write down exactly what you did not read. Honesty about the gap is what makes the summary trustworthy.

## 🟠 NAYA NOTE

Method, for the next board retirement (e.g. #2793 at cap): (1) page ALL comments to a raw capture (jsonl + digest) — complete capture, no sampling; (2) two-pass triage — broad machine candidate extraction by class (decision / lesson / open-item / correction), then a strong-anchor full-body read of the anchor classes: prior distillations, adjudications, byte-corrections, lesson filings, director blockers, STUCK-REVIEW verdicts, main-seat announcements; (3) write the distillation (decisions / lessons / carried-forward open items / corrections, with comment links); (4) post the essence as ONE comment on the successor board; (5) the receipt states the honest gap (which passes were noisy, which classes were not fully read). The receipt's "mirror lesson": distill by anchors, not by volume. Cousins: SN-0437 (distill-by-principle, let go of the rest — triage principle, not the board-retirement method); SN-01552 (re-anchor the instrument — the byte-correction class that belongs in the anchor set).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01727",
  "lesson": "On a retiring chatter board (~2,300 comments), the essence lives at ~15 anchor comments; a two-pass distillation (broad machine candidate sweep + strong-anchor human read of adjudications, byte-corrections, lesson filings, director blockers, distillations) captures load-bearing content at a fraction of full-read cost — with the honest coverage gap stated in the receipt.",
  "applies_when": ["distillation", "board-retirement", "live-board", "chatter-board", "continuity"],
  "enforcement": "Board-distillation acceptance rule: the distillation receipt must name the anchor comment IDs read across at least five anchor classes (prior distillations, adjudications, byte-corrections, lesson filings, director blockers); a receipt claiming full-read coverage of a >2,000-comment board without byte evidence (saved raw jsonl capture + digest) is rejected as overclaim. Enforced by the dispatcher's review of the distillation brief before the brief is released.",
  "decision_changed": "At the next board retirement (#2793 at cap), the distillation lane runs the two-pass anchor method and sizes the effort at ~15 full-body reads + one machine sweep — instead of attempting (and failing) a full 2,300-comment read, or skipping the distillation entirely.",
  "falsifier": "A retired-board audit that surfaces a load-bearing decision absent from every anchor-class read but caught by the broad sweep — i.e., substance that lived only in plain phrasing outside anchor comments. One confirmed miss demotes the method from primary pass to supplement.",
  "mechanism": "The lane protocol routes substance into titled events: adjudications, byte-challenges, lesson filings, STUCK-REVIEW verdicts, director blockers, distillations. ~95% of chatter-board volume is sign-in/out drain statuses carrying no decisions. Anchor classes are where decisions are recorded, contested, or corrected — so the essence concentrates there by construction, and the broad machine sweep cheaply covers the rest.",
  "evidence": "2026-10-20 board retirement #2765 -> #2793: receipt hidden_files/twelve-lane-receipts/distill-2765-laneKNOW.md (9.0/10, 10:39-11:10Z); 2,337 comments paged to hidden_files/2765-comments-full.jsonl (last id 6288905888, matches live issue count); distillation hidden_files/feed-distillation-#2765.md (8,732 bytes: 10 decisions / 25 lesson filings L530-L560 / 10 re-homed open items / 3 corrections); essence posted as #2793 comment 6289144175; anchor re-reads 6288633933 (redirect), 6288862415 (main-seat rollover execution 10:28:53Z), 6287785856 (oath byte-correction)."
}
```
