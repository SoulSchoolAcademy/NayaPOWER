# Dispatch-Time Pin Check — a Hole-Closure Brief Arrives Falsified or Confirmed, Never Assumed

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1206-dispatch-time-pin-check-hole-closure-briefs
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md [t0659] Naya Heir (2026-10-13, mirror t0649 mission-state pin, 9.0/10); shared-state.json mission_snapshot_note (BRAIN/CURRENT-MISSION-STATE.md CANONICAL at 4f0c9aa8, blob 015dfefe, via PR #2524 2026-10-13 07:39 PDT)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A hole-closure brief inherits prose from the receipt that named the hole — "prior analysis is stale" and "hole persists" are both claims that live bytes settle in one command. The t0649 brief dispatched at ~09:04 PDT said the mission-state file was unlocatable; the file had landed via PR #2524 at 07:39 PDT, 85 minutes earlier — the dispatcher's premise died before the brief was even written, and live bytes falsified it in 60 seconds ("absence-framed prose invites a 'search the void' workflow; the existence probe killed it in one command"). The lane should never have to falsify the dispatcher's premise: the brief-as-hypothesis discipline did its job twice over (fetched fresh and re-derived every pin BEFORE reading any content — read order matters). This is the t0649 Mason watch-for, proven again: **every hole-closure brief carries a dispatch-time pin check** — the dispatcher re-derives the hole's existence pin at dispatch time and names the pin in the brief, or the brief ships with the rot already labeled. Result of the falsified brief: BRAIN/CURRENT-MISSION-STATE.md confirmed CANONICAL at tip 4f0c9aa8 (blob 015dfefe, sha256 115e2d2e), SURGE (a) unread-constraints hole CLOSED.

## 🩷 HUMAN NOTE

Shawn — a dispatch bug worth banking: this morning a lane got a brief saying a file was missing and to go find it. The file had landed an hour and a half before the brief was even written. The lane spent one command proving the brief wrong instead of doing the work. The fix: the dispatcher checks the hole still exists right before sending the brief — one existence probe, 60 seconds — and if it's already closed, the brief says so up front. A hole-closure brief should arrive already confirmed (or already falsified), never assuming. The lane's job is the work, not auditing the dispatcher's memory.

## 🟣 CHILD NOTE

Imagine your teacher gives you a worksheet that says "find the lost key" — but the key was found and returned to the desk before the worksheet was even printed. You'd waste the whole lesson searching for something that's already home. The new rule: before the teacher prints the worksheet, she checks the desk. If the key is there, the worksheet says so. Nobody searches for what's already found.

## 👵 GRANDMA NOTE

A contractor was sent to fix a leak the work order said was still dripping. He arrived to find the plumber had finished the job that morning — the work order was written from yesterday's note, not today's reality. One phone call would have confirmed it before he drove out. The new standing rule: whoever writes the work order calls the house first. The repair brief carries a fresh timestamp from the person who sent it, or it carries a warning that the information might be stale.

## 🧠 NAYA NOTE

Cold successor: when you dispatch a hole-closure brief, the dispatch packet must include a dispatch-time pin check — re-derive the hole's existence claim (the file, the drift, the stale state) against live bytes at dispatch time, and name the pin + its timestamp in the brief. If the pin comes back clean, the brief says "hole already closed at <pin>, brief falsified" and does NOT dispatch a search. If the pin holds, the brief ships with the evidence the hole is real. Read order on the receiving lane: re-derive pins before reading content, so an absence-framed premise gets an existence probe first (one command, ~60s), not a "search the void" workflow. This is the t0649 Mason watch-for, now proven a second time — dispatcher-side rot, not lane-side diligence, is the root.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1206",
  "title": "Dispatch-Time Pin Check — a Hole-Closure Brief Arrives Falsified or Confirmed, Never Assumed",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "COORDINATION-DESIGN"],
  "cousins": ["SN-1203", "SN-1194"],
  "evidence": {
    "lesson": "lesson-broadcast.md [t0659] Naya Heir — mirror, t0649 mission-state pin, scorecard 9.0/10, 2026-10-13",
    "premise_death": "brief dispatched ~09:04 PDT claimed BRAIN/CURRENT-MISSION-STATE.md unlocatable; file had landed via PR #2524 (merged 2026-10-13 07:39 PDT) ~85 min before dispatch",
    "falsification": "existence probe + pin re-derivation, ~60 seconds; file confirmed CANONICAL at tip 4f0c9aa8, blob 015dfefe, sha256 115e2d2e",
    "outcome": "SURGE (a) unread-constraints hole CLOSED by the probe, not by the planned search",
    "prior_art": "t0649 Mason watch-for (dispatch-time pin check on hole-closure briefs), proven again this tick — dispatcher-side root"
  },
  "rule": "a hole-closure brief inherits prose from the receipt that named the hole; the dispatcher re-derives the hole's existence pin at dispatch time and names it in the brief — the dispatcher arrives already falsified or confirmed, the lane must never have to falsify the dispatcher's premise",
  "change": "dispatch-time pin check on all hole-closure briefs (pin + timestamp in the brief; falsified premises labeled, not dispatched as searches)"
}
```
