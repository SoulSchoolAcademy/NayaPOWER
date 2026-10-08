# Re-Anchor Fast-Moving Tip Claims into Forward History Before Crying Violation

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0534-re-anchor-tip-claims-into-forward-history
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6036650785 (2026-10-07T11:08:28Z — [NAYA 4 / SELF-BUILD LOOP][SIGN-IN + SIGN-OUT] Cycle #1703-MERGEVERIFY, SoulSchoolAcademy).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During the #1703-MERGEVERIFY cycle, overnight sign-outs had claimed tip SHAs — `b2a6b4164` and `d3947f8a` — that did not match the cycle's live tip `e7de7b88`. The cycle did not declare a truth violation. It re-anchored: resolving both SHAs against the live tip via the compare API showed every overnight claim lands inside main's forward history, with `d3947f8a` exactly 3 commits behind the tip. Verdict recorded in the sign-out: "no truth violation, just rapid overnight merges."

The durable rule: **on a fast-moving tip, a SHA that isn't the current tip is not automatically a false claim — resolve it against the live tip before judging it.** The compare API is the instrument: claimed SHA is an ancestor of the live tip (ahead 0, behind N) → the claim is consistent, merely stale; claimed SHA diverges from the live tip → now you have a violation worth naming. The common failure mode this prevents is the false accusation — one lane crying "your sign-out lied about the tip" when the other lane simply signed out an hour earlier. Pairs with SN-0493 (a decision expires when the tip moves — this is the claims side of that same coin: decisions get re-validated on the new tip, claims get re-anchored into its history).

## 🩷 HUMAN NOTE

Shawn — small but important piece of lane-craft from the overnight verification cycle. Two earlier sign-outs had named tip SHAs that didn't match the current tip. Instead of flagging them as wrong, the cycle checked each SHA against the live tip and found both were simply earlier points on the same main line — one was exactly 3 commits behind. The tip had just moved fast overnight; nobody was wrong. Rule going forward: before calling out a "wrong" SHA, check whether it's an ancestor of the current tip. Stale isn't false — and accusing a lane of a truth violation over a fast-moving tip is itself a defect.

## 🟣 CHILD NOTE

Imagine two friends describing where they saw a train. One says "it was at the station at noon," the other says "it's at the bridge now, at 1pm." The first friend isn't lying — the train just moved. You check the tracks: the station is three stops back on the same line, so both statements are true. That's what happened here: two earlier reports named older positions of the code's "train," and checking the tracks showed they were exactly 3 stops back on the same line. Rule: before saying someone's report was wrong, check whether they just reported an earlier stop.

## 👵 GRANDMA NOTE

Think of it like two neighbors describing a river's water level — one measured at dawn, one at noon. If the level changed between readings, the dawn reader isn't wrong; time simply passed. We check the record: was the dawn reading on the same river, at an earlier hour? If yes, both readings stand. The rule we keep: before declaring someone's report false, check whether time just moved on — an older-but-true reading is not a lie.

## 💜 NAYA NOTE

Note to future me: on a fast-moving main, treat every tip SHA in a sign-out as a *claim to be re-anchored*, not a fact to be believed or a lie to be exposed. Mechanism: hit the compare API with base=<claimed SHA>, head=<live tip>. Ahead 0 / behind N = consistent ancestor (record "re-anchored, N behind tip"); anything else = investigate as a possible violation. Do this *before* writing any accusation into a sign-out — a false violation claim is a defect against the lane you accused. Corollary for writers: sign-outs should name the tip their claims resolve against (the cycle re-pinned `e7de7b88` via the refs API and said so), so the next reader can re-anchor instead of guess. This is the claims-side twin of SN-0493: decisions expire when the tip moves, but claims *survive* as ancestors — judge each by its own rule.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0534",
  "rule": "re-anchor-claims-into-forward-history",
  "statement": "Before declaring a tip-SHA claim false, resolve it against the live tip via the compare API: ancestor-of-tip (ahead 0, behind N) is consistent-but-stale; divergence is the violation. A false violation accusation is itself a defect.",
  "corollaries": [
    "Sign-outs name the tip their claims resolve against, pinned via the refs API.",
    "Stale is not false: stale claims re-anchor, divergent claims get investigated.",
    "Claims-side twin of SN-0493: decisions expire when the tip moves; claims survive as ancestors."
  ],
  "source": "#1354 6036650785 (2026-10-07) — overnight claims b2a6b4164 / d3947f8a re-anchored into main; d3947f8a exactly 3 commits behind tip e7de7b88"
}
```
