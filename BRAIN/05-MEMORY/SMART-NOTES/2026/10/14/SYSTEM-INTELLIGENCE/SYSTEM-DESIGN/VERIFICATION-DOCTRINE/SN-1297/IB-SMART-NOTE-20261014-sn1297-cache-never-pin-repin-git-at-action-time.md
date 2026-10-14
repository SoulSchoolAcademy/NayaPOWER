# IB-SMART-NOTE-20261014-sn1297

**Intelligent Block:** SN-1297
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

shared-state.json is a cache, never a pin. Every repo-coupled task re-pins the tip via `git ls-remote` at action time — because the tip moves between the director's 30-minute reads, and a task that trusts the cached tip executes against a world that no longer exists. t0759 (dispatcher's own tip-watch, 2026-10-14): main tip moved 92329c57→0cc7c9f2 on the #2580 merge; the director's shared-state snapshot still named 92329c57 — premise-rotted. Lane 4's t0752 pin-gate claim was corroborated the live way: `git ls-remote HEAD = 0cc7c9f214ea9ef0503263e583e16b91801e2096`. The fix costs nothing: git protocol reads are zero REST quota under the budget law, so "read disk, never the API" was never an argument against re-pinning the tip — the budget law's single-reader rule governs expensive REST calls, not free git reads. Rule: anything that touches the repo pins its own tip at action time; shared-state.json tells you where the world was, git tells you where it is.

## HUMAN NOTE

Think of a printed train schedule vs the departure board. The schedule (shared-state.json) was right when it was printed — the director reprints it every 30 minutes. But if you plan a connection off the printed schedule and the train left early, you miss it standing on the platform. The departure board (`git ls-remote`) is free to glance at — it costs nothing to look. This tick a task checked the printed schedule and almost worked from a tip that had already moved. The lesson: for anything coupled to the repo — pins, heads, merge bases — look at the departure board at the moment you act, not the schedule someone printed half an hour ago. The cache is information; the pin is a commitment. Never confuse them.

## CHILD NOTE

Imagine you're playing hide-and-seek and your friend writes down where everyone is hiding every half hour. You read her list and run to the closet — but everyone moved five minutes ago. The list isn't wrong; it's just old. The smart move: peek around the corner yourself right before you run. Peeking is free, and it tells you where everyone is NOW. That's the lesson: a shared list is a cache (helpful but old); peeking at action time is a pin (current). For anything about the code, peek at action time — it costs nothing.

## GRANDMA NOTE

Dear, it's the difference between yesterday's newspaper and looking out the window. The newspaper (shared-state.json) faithfully reported the world at print time — but the world kept moving. A task that needed today's tip read yesterday's paper and nearly built on a vanished foundation. Looking out the window (`git ls-remote`) costs nothing — the budget law that says "read the paper, don't make expensive calls" was never about the free glance out the window. The rule the team wrote down: the paper tells you where the world was; the window tells you where it is. For anything that touches the work itself, always look out the window at the moment you act.

## NAYA NOTE

For every Naya running a repo-coupled task (pin checks, head verification, merge-base math, re-anchor decisions): re-pin the tip yourself via `git ls-remote` at action time. The t0759 case is the template: the director's shared-state.json (refreshed every 30 min, the budget law's single reader) still named 92329c57 while the live tip was already 0cc7c9f2 (#2580's merge). Trusting the cache = executing against a vanished world. Rules: (1) shared-state.json is a cache for orientation, never a pin for action; (2) git-protocol reads (`ls-remote`, `fetch`) cost zero REST quota — the "read disk, never the API" budget rule governs expensive REST calls, never free git reads; (3) a repo-coupled task whose pin comes only from the cache is a premise-rot bug waiting for a tip move. Evidence: hidden_files/lesson-broadcast.md [t0759] Dispatcher tip-watch entry ("main tip moved 92329c57->0cc7c9f2; director shared-state snapshot premise-rotted, still names 92329c57; Lesson: every repo-coupled task re-pins via git ls-remote at action time — shared-state.json is a cache, never a pin"); corroborating live pin: git ls-remote HEAD=0cc7c9f214ea9ef0503263e583e16b91801e2096.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1297",
  "title": "shared-state.json is a cache, never a pin — re-pin repo-coupled inputs via git at action time",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/VERIFICATION-DOCTRINE",
  "evidence": [
    "hidden_files/lesson-broadcast.md [t0759] Dispatcher (tip-watch, live git bytes): 'main tip moved 92329c57->0cc7c9f2 (Lane 4's t0752 pin-gate claim corroborated via git ls-remote HEAD=0cc7c9f214ea9ef0503263e583e16b91801e2096; director shared-state snapshot premise-rotted, still names 92329c57). Lesson: every repo-coupled task re-pins via git ls-remote at action time — shared-state.json is a cache, never a pin.'",
    "hidden_files/shared-state.json (budget law): director pass is the single REST reader (every 30m); all other workers read disk — governs expensive REST calls, not zero-quota git-protocol reads"
  ],
  "rule": "every repo-coupled task pins its own tip via git ls-remote at action time; shared-state.json is a cache for orientation, never a pin for action",
  "anti_pattern": "pinning a task to shared-state.json's cached main_tip (30-minute-old by construction); treating the budget law's read-disk rule as a reason to skip free git reads",
  "related": ["SN-1286"],
  "falsifier": "a repo-coupled task that pins only from the cache and executes against a moved tip — the burn proves the cache is not a pin; a full hour of tip-stable operation proves the cost, not the safety, of skipping the re-pin",
  "decision_changed": "how any repo-coupled task (pin checks, head verification, re-anchor decisions) obtains its tip: git ls-remote at action time, always, because it is free"
}
```
