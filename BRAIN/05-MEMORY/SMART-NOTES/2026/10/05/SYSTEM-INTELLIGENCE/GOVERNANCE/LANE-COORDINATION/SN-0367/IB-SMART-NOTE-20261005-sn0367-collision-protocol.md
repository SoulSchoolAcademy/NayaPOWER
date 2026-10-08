# Collision Protocol — Re-scan Before Push; the Arbiter Flags but Never Edits

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0367-collision-protocol
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~09:32–09:41 PDT — CODA 2 collision alert (comment 5998724745), Naya 4 correction (comment 5998862414); PRs #1478 / #1479.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When two lanes independently repair the same live RED, the episode is textbook convergent repair: same intent, same files, same value — best outcome for correctness, worst for merge hygiene. PR #1478 and PR #1479 both fixed the `01-GOVERNANCE` brain-index drift (7→10, same 4 files, byte-verified by a third seat). Two protocol lessons came out of it. **For the racers:** a claim scan goes stale the instant a parallel lane opens its PR — Naya 4's scan at ~09:14 found no claim because #1478 did not exist yet; it opened at 09:17, twelve minutes before her #1479. Re-scan immediately before pushing the branch on hot RED classes; the claim scan has a TOCTOU gap. First claim stands; the duplicate closes with its commit preserved in git (archaeology intact, per the #1216 precedent). **For the arbiter:** CODA 2 flagged the collision with byte-level evidence and deliberately touched nothing — "choosing between two other lanes' work is not my call, and a collision resolver that also edits the PRs is how trust in this process breaks."

Why this is brain-grade: SN-0236 (one repair per RED class) says what the end state must be. This note says how to get there without burning lanes: the pre-push re-scan prevents the race, and the hands-off arbiter keeps the resolution legitimate. Both directions serve the same principle — convergent work is a coordination event, never a contest.

## 🩷 HUMAN NOTE

Shawn — the lanes raced on the same RED fix this morning (PR #1478 vs #1479) and resolved it cleanly: first claim kept, duplicate closed, evidence byte-verified by a third seat. Two standing fixes came out of it for every future lane: re-scan for competing claims immediately before pushing on hot RED classes, and when a third seat flags a collision, it flags with evidence and never touches the PRs. No drama, no wasted work — exactly the team you asked for.

## 🟣 CHILD NOTE

Imagine two friends both fixing the same flat tire at the same time — same tire, same fix. The rule is: whoever started first keeps going, and the other person steps back (but keeps their notes). And if a third friend notices both of them, they point it out — but they don't touch the tools. One more rule: always check one last time right before you start, because someone else might have just begun.

## 👵 GRANDMA NOTE

Two of Shawn's AI helpers both fixed the same problem without knowing it. They sorted it out the honest way: the one who started first kept the job, the other stepped aside, and a third helper who noticed the overlap just pointed it out without taking sides. The lessons they wrote down: always look one last time before you start (things change fast), and never let the referee touch the work — they only report what they see.

## 💜 NAYA NOTE

For any future seat, two procedures for the hot-RED case. (1) Before pushing a repair branch on a RED class another lane could plausibly be touching: re-run the open-PR claim scan immediately before `git push`. A scan from minutes ago is evidence of nothing — #1478 appeared in a 12-minute window. First claim stands per SN-0236; the loser closes as duplicate with the commit preserved (git keeps the archaeology; #1216 set this precedent). (2) If you are the third seat who spots the collision: post the evidence (actual file bytes at each ref, not titles), address both lanes, and touch neither PR. Choosing between two other lanes' work is not your call; a resolver that edits is how trust breaks. Cross-reference SN-0236 (one repair per class), SN-0337 (lanes converge, close duplicate superseded), SN-0351 (communicate state, not events).

## 🖥️ MACHINE NOTE

{"sn": "SN-0367", "title": "Collision Protocol — Re-scan Before Push; the Arbiter Flags but Never Edits", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "LANE-COORDINATION"], "cousins": ["SN-0236", "SN-0337", "SN-0351"], "evidence": {"collision": "board #1354 comment 5998724745 — PR #1478 vs #1479, same 4 files, same value 7→10, verified by reading actual file bytes at each ref", "toctou": "board #1354 comment 5998862414 — claim scan ~09:14 PDT found nothing; #1478 opened 09:17, #1479 09:29; duplicate closed per SN-0236 with #1216 archaeology precedent"}, "rule": "On hot RED classes: re-scan open-PR claims immediately before pushing the branch (claim scans have a TOCTOU gap); first claim stands. A third-seat collision flag carries byte-level evidence and touches neither PR — choosing between lanes' work is not the arbiter's call"}
