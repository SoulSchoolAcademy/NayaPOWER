Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The distill-daily worker (2026-10-23 ~05:24 PDT) diffed main's CURRENT-MISSION-STATE (yesterday 20:15Z) against the naya/mission-state branch snapshot (the director's 12:08Z refresh) and ruled correctly: the branch copy being NEWER than main is cadence, not drift. The durable rule: a snapshot copy's currency is defined by its producer's declared refresh cadence — never by the head it is compared against. Drift is a verdict about write rate. Before any "main vs branch drift" ruling, check the snapshot branch's last commit against its refresh interval; if it arrived within ~2x cadence, the delta is expected-by-design and filing drift manufactures a false hole. The falsifier is checkable in git history: if the snapshot branch goes silent past ~2x its cadence, a branch-newer-than-main delta really is stale-capture drift. Freshness ownership is the mechanism: a snapshot is a consumer's read at a declared interval, not a replica — its freshness reference is the producer's clock, not the comparison target's tip. Cousin SN-1822 (drift does not falsify a pin; unverified drift does) governs pins; this note governs snapshot branches.

## 🩷 HUMAN NOTE

Shawn — the daily distiller compared the mission-state snapshot branch against main and found the branch newer. It didn't flag drift, and it was right: that branch is refreshed hourly by design, so of course its copy is fresher than main's stale one. The rule for cold successors: never call a snapshot "drifted" just because it differs from main — check when the snapshot was last refreshed against its declared schedule. A fresh snapshot that disagrees with main is healthy. Only a silent snapshot is actually stale. The difference between a false alarm and a real catch is one timestamp check.

## 🟣 CHILD NOTE

Imagine a newspaper printing press and a photocopy on the wall. The photocopy was made this morning; the press's master is from last night. The photocopy looks "newer" — but that's not a mistake, that's because someone copies the wall every hour on purpose. Only if the wall hasn't been re-copied in hours is something wrong. Judge the copy by the copying schedule, not by the press.

## 🔵 GRANDMA NOTE

It's like the pharmacy's printed price list versus the computer system. The printed list was reprinted this morning; the computer prices were entered last night. The printed list looks newer — but that's not an error, they reprint it every morning. You'd only worry if the printout hadn't been replaced in days. Judge freshness by the reprint schedule, not by comparing it to something else.

## 🟠 NAYA NOTE

Verdicts on drift must carry their reference frame. A snapshot branch's freshness is measured against its producer's declared refresh cadence — the director refreshes naya/mission-state hourly, so a branch copy newer than main's is the healthy steady state, not a hole. The failure mode is manufacturing false drift: a worker that diffs branch vs main without checking the cadence creates work that undoes itself (a "fix" that reverts a healthy snapshot). The discipline: freshness-first, cadence-aware — every drift verdict states the producer's interval, the last refresh timestamp, and only then the ruling. No stated cadence means the verdict is BLOCKED, never drift.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1869-snapshot-cadence-drift-verdict",
  "lesson": "The distill-daily worker (2026-10-23 ~05:24 PDT, run ~12:24Z) diffed main's CURRENT-MISSION-STATE (2026-10-22T20:15Z) against the naya/mission-state branch snapshot (director's 2026-10-23T12:08Z refresh) and ruled 'branch NEWER than main — expected by design (snapshot branch refreshed hourly), not a bug; no fix attempted.' The durable rule: a snapshot copy's currency is defined by its producer's declared refresh cadence, never by the head it is compared against. Drift is a verdict about write rate: before any 'main vs branch drift' ruling, check the snapshot branch's last commit against its refresh interval; a delta within ~2x cadence is expected-by-design, and filing drift manufactures a false hole (a 'fix' that reverts a healthy snapshot). The falsifier is checkable in git history: if the snapshot branch goes silent past ~2x its cadence, a branch-newer-than-main delta really is stale-capture drift. Mechanism: freshness ownership — a snapshot is a consumer's read at a declared interval, not a replica; its freshness reference is the producer's clock, not the comparison target's tip. Cousin SN-1822 governs pins; this note governs snapshot branches.",
  "applies_when": ["distillation", "drift-verdict", "snapshot", "cadence", "mission-state", "freshness", "failure:drift-false-positive", "verification", "naya/mission-state"],
  "enforcement": "The distill-daily drift step gains a freshness-first branch: before any 'main vs branch drift' verdict, read the snapshot branch's last commit timestamp and compare it against its declared refresh cadence (hourly for naya/mission-state). Delta within ~2x cadence = expected-by-design, file nothing. No declared cadence on file = the verdict is BLOCKED (not drift), and the owed follow-up is to declare one. Acceptance: a deliberately stale snapshot (no commit for >2x cadence) must be flagged; a fresh one never is. Reviewer check: any future 'drift' verdict must name the producer's interval and the last-refresh timestamp, or it is rejected as unfalsifiable.",
  "evidence": [
    "distill-daily worker run 2026-10-23 ~05:24 PDT (~12:24Z): 'Mission-state drift (main vs naya/mission-state): branch copy is the director's 12:08Z today snapshot; main's copy is yesterday 20:15Z. Branch NEWER than main — expected by design (snapshot branch refreshed hourly), not a bug. No fix attempted per task.' (logged to ~/memory/2026-10-23.md, this tick's source review)",
    "Cousin SN-1822: 'drift does not falsify a pin; unverified drift does' (pin class — this note extends the same freshness-first discipline to snapshot branches)",
    "Cousin SN-033: 'a committed index is only as fresh as its reconciliation stamp' (same family: freshness measured against a declared reference, not a comparison)"
  ]
}
```
