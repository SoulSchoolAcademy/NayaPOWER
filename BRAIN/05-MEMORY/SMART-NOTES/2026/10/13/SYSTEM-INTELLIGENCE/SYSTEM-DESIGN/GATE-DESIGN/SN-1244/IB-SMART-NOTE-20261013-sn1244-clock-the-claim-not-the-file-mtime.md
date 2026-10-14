# Clock the Claim From Sign-In Evidence, Never From File Mtime

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1244-clock-the-claim-not-the-file-mtime
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md t0696 entry (Dispatcher claim-liveness correction, 2026-10-13) — the audit voided brief-t0687-lane12.md as a phantom claim after 88 min in claimed/ with no lane-feed sign-in: a FALSE POSITIVE. The executor had claimed the brief at 00:19Z with a journal sign-in at 00:20Z; the audit read only dispatch-write mtime + lane-feed and voided a live run mid-flight. The receipt landed at 00:24Z; the brief was restored. Root cause: `mv` preserves mtime, so claim time is unknowable from the file; dispatch-write mtime is not claim time. Refinement of the standing PHANTOM-CLAIM LAW (claim without a sign-in is a reservation without a worker) — the correction is what the audit clocks, not the law itself.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The claim-liveness audit caught a phantom — and it was a live worker. The brief sat in `claimed/` for 88 minutes with no sign-in the auditor could see, so it was voided. Problem: the executor had claimed it at 00:19Z with a journal sign-in at 00:20Z; the audit had clocked the claim from **file mtime** (`mv` preserves mtime, so claim time is unknowable from the file) and read only the lane feed, which missed the journal. The void landed mid-flight; the receipt arrived at 00:24Z anyway and the brief was restored. Two lessons: **clock a claim from claim evidence — journal sign-in, a touched claim file, a `.claimed-at` sidecar — never from mtime alone**; and when the claim clock is unknowable, **annotate and re-check next tick**, don't void. A reversible void that collides a live run is still a collision — reversibility is not harmlessness.

Why this is brain-grade: every handoff audit in the system — claimed briefs, stale locks, orphan receipts — reads some clock to decide "dead or alive." If the clock measures the wrong event (file write, not claim act), the audit fires on evidence that never existed, and the "repair" (voiding) becomes the damage. The discipline generalizes: an audit is only as good as its mapping from timestamp to event; get the mapping wrong and the watchdog bites the workers it's guarding.

## 🩷 HUMAN NOTE

Shawn — the phantom-claim audit worked, a little too well: it voided a "dead" claim that was actually a live worker mid-run. The audit clocked the claim from the file's timestamp, but moving a file doesn't update that timestamp — so it was reading a clock that never saw the claim happen. The real claim evidence (a journal sign-in four minutes in) was somewhere the audit didn't look. The fix is two-fold and it's already law: audits must clock claims from actual claim evidence, and when the clock can't be known, you flag it and check again next round instead of voiding. No work was lost — the receipt landed and the brief was restored — but a reversible void mid-flight is still a mid-flight collision.

## 🟣 CHILD NOTE

Imagine you're playing hide-and-seek, and the rule is: "if nobody moves for ten minutes, they're out." But you're watching a video of the hiding spot, not the real spot — and in the video, nobody moved, while in real life your friend just ran to a new hiding place. You'd call them out even though they're still playing! That's what happened: the auditor watched the file's clock (the video) instead of the real sign-in record (the real spot). Now the rule is: watch the real spot, and if you can't see it clearly, don't call anyone out — just look again in a minute.

## 👵 GRANDMA NOTE

There's an old saying: don't judge a book by its cover. The team learned the machinery version: don't judge a claim by the file's timestamp. Moving a paper from one tray to another doesn't change when it was picked up — the timestamp says when it was created, not when someone took it. The auditor read the wrong date and cancelled a job a worker was actively doing. The fix is common sense made into procedure: read the sign-in sheet where workers actually sign in, and when you can't tell, don't cancel — just come back and check again.

## 🧠 NAYA NOTE

Note to future me: any audit that voids, expires, or reclaims something is a **kill decision**, and kill decisions need kill-grade evidence. Before I trust an audit's clock, ask: "what event does this timestamp actually record — and is that the event I'm judging?" File mtime records the last write, not the claim; a moved file's mtime is the dispatch instant, not the pickup. When I build a liveness audit, the claim mechanism must timestamp itself (touch the file, write a `.claimed-at` sidecar, or read the journal where the sign-in actually lands). And when the clock is unknowable, the only honest verdicts are "check again next tick" — voiding on an unknowable clock is the audit manufacturing the failure it exists to prevent.

## ⚙️ MACHINE NOTE

{"sn": "SN-1244", "title": "Clock the Claim From Sign-In Evidence, Never From File Mtime", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "GATE-DESIGN"], "cousins": ["SN-1133", "SN-0997", "SN-280"], "evidence": {"finding": "t0696 dispatcher correction (2026-10-13): claim-liveness audit voided brief-t0687-lane12.md after 88 min in claimed/ with no lane-feed sign-in - FALSE POSITIVE; executor had claimed at 00:19Z with journal sign-in at 00:20Z; audit read dispatch-write mtime + lane-feed only and voided mid-flight; receipt landed 00:24Z; brief restored; root cause: mv preserves mtime so claim time is unknowable from the file, dispatch-write mtime is not claim time"}, "decision_change": "future liveness/handoff audits must timestamp the claim at claim time (touch the file, .claimed-at sidecar, or read the journal sign-in) and clock from that evidence; when the claim clock is unknowable the verdict must be 'annotate and re-check next tick', never void", "falsifier": "audits clocked from claim evidence still void live runs, or mtime-only audits demonstrably stop colliding without any clock change - then the clock mapping is not the mechanism", "mechanism": "mv preserves mtime so the file timestamp records dispatch-write, not claim; lane-feed-only reads miss journal sign-ins; an audit that clocks the wrong event fires on evidence that never existed, and its 'repair' becomes the damage", "rule": "clock the claim from sign-in evidence, never from file mtime; when the claim clock is unknowable, annotate and re-check next tick - a reversible void is still a collision"}
