Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

PR #3003 was the brain-index cure: regen the index, clear the 3 freshness reds. It was green at its own head (7eaf08a8). It landed — and the reds survived the landing. The learning event (board #2793, 6370261405, 2026-10-23 16:59Z) named it L640, THE CURE DID NOT CURE: "PR #3003 brain-index regen was stale-base; brain-index x3 still fail at both post-landing heads (identical 20-failed set) — re-cure = regen at settled tip." The WIRE sign-out (6368109418, 15:11Z) had already said why: "#3003 landed on its stale base while the tree moved — the freshness red survives the landing." Between the PR's base and the landing tip, other landings moved the tree — here, the SN-1853 manifest rewrite raced the regen. A cure proven at the PR head is proven against a world that no longer exists. This is the cure-side mirror of SN-0554 (a stale-base red is not a current-main red): SN-0554 governs naming a red; this governs retiring one. Decision-change: before a red watch retires after a cure lands, the cure lane re-runs the failing suite at the settled post-landing tip; the PR-head green does not retire the watch. Falsifier: if the intervening delta is provably orthogonal to the cure's subsystem, the re-run is redundant — the lesson holds exactly where intervening landings can touch the cure's subsystem.

## 🩷 HUMAN NOTE

Shawn — we built the fix for the brain-index reds, tested it green, and merged it. The reds are still there. Here's what happened: while the fix was being reviewed, other work landed on top of it — including a change that rewrote the very index the fix had regenerated. The fix was tested against the world as it was when the fix was written, not the world as it is now. The rule from here: a fix isn't proven until it's re-tested against the final, settled code — the test at the fix's own starting point doesn't count. The re-do is already owned: regenerate at the settled tip.

## 🟣 CHILD NOTE

Imagine you clean your room perfectly — and then your little brother runs through it with muddy shoes before mom comes to check. Your cleaning was real, but mom is checking the room as it is NOW, not as it was when you finished. That's what happened to the fix: it cleaned the index, but other work landed on top before the check. The fix has to be re-done and re-checked on the room as it is now.

## 🔵 GRANDMA NOTE

Think of proofreading a letter, sealing it in an envelope — and then someone slips two more pages into the envelope before it mails. Your proofreading was perfect for the pages you read. It says nothing about the pages you didn't. A software fix is the proofreading; the landing tip is the envelope as mailed. You re-read the whole envelope before you call it done.

## 🟠 NAYA NOTE

For the cure lanes (KNOW/index, door) and the dock: re-cure #3009 (3637eda1) is already the owned vehicle — regen at the settled tip, per the learning event. This note is the standing form: the cure-close checklist requires the failing suite re-run at the settled post-landing tip before the red watch retires; a watch closed on PR-head-only evidence is re-opened by the WIRE lane. The check is cheap relative to the failure it prevents: the identical 20-failed set at both post-landing heads was knowable the hour #3003 landed. Owner of the re-run: the cure's lane + dock (per 6370261405: KNOW/index + dock). Do not duplicate #3003 with a second cure PR on another stale base — the re-cure runs at the tip, once.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1886-stale-base-cure-does-not-cure-the-tip",
  "lesson": "A cure proven at the PR head is proven against a world that no longer exists: re-run the failing suite at the settled post-landing tip before retiring the red watch. Evidence: board #2793 learning event 6370261405 (2026-10-23T16:59:51Z), L640 THE CURE DID NOT CURE — 'PR #3003 brain-index regen was stale-base; brain-index x3 still fail at both post-landing heads (identical 20-failed set) — re-cure = regen at settled tip (owner: KNOW/index + dock)'; WIRE sign-out 6368109418 (2026-10-23T15:11:22Z) — '#3003 landed on its stale base while the tree moved — the freshness red survives the landing.' Mechanism: between the PR's base and the landing tip, intervening landings moved the tree (the SN-1853 manifest rewrite raced the brain-index regen); a cure green at its own head (7eaf08a8) says nothing about the settled tip. Cure-side mirror of SN-0554 (stale-base red vs current-main red — the red-naming side; this is the red-retiring side). Decision-change: the cure-close checklist requires the failing suite re-run at the settled tip before the watch retires; PR-head green does not retire it. Falsifier: if the intervening delta is provably orthogonal to the cure's subsystem, the re-run is redundant — the lesson holds exactly where intervening landings can touch the cure's subsystem.",
  "applies_when": ["cure", "landing", "stale-base", "red-watch", "wire", "merge", "verification", "index"],
  "enforcement": "The cure-close checklist requires the failing suite re-run at the settled post-landing tip before the red watch retires; a watch closed on PR-head-only evidence is re-opened by the WIRE lane. The re-run owner is the cure's lane + dock.",
  "evidence": ["board #2793 comment 6370261405 (LEARNING EVENT, 2026-10-23T16:59:51Z): L640 THE CURE DID NOT CURE — PR #3003 brain-index regen was stale-base; brain-index x3 still fail at both post-landing heads (identical 20-failed set); re-cure = regen at settled tip", "board #2793 comment 6368109418 (Naya Resolve Narzan, WIRE lane, 2026-10-23T15:11:22Z): #3003 landed on its stale base while the tree moved — the freshness red survives the landing"],
  "falsifier": "An intervening delta provably orthogonal to the cure's subsystem makes the re-run redundant; the lesson holds exactly where intervening landings can touch the cure's subsystem.",
  "related": ["SN-0554 (stale-base red vs current-main red — the red-naming mirror)", "SN-1872 (cure must declare addressed failures)", "SN-1830 (cure verdict dual axis)"]
}
```
