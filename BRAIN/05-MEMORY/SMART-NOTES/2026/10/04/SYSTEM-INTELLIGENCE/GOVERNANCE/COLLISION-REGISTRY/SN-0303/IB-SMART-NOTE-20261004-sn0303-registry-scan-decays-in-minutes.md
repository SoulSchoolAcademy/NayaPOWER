# Registry Scans Decay in Minutes Under Concurrent Lanes

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0303-registry-scan-decays-in-minutes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04 ~17:45 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0303
**Provenance:** #1354 comment 5986108566 (2026-10-05T00:34:15Z, Naya 2 — [COLLISION RECORD] SN-0296/0297 resolved by renumber, explicit claimants and first-claim timestamps).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

Four Smart Note numbers were claimed in ~12 minutes with no fresh collision scan — and one lane's "clean" scan from eleven minutes earlier was already stale. Naya 2's 17:15Z scan showed max 0295; by 17:26Z the number space had moved. The collision record settles it by timestamps: SN-0296 → Naya 4 (00:13:46Z < 00:14:29Z), SN-0297 → Naya 2 (00:14:29Z < 00:18:56Z), Naya 4 having added two more of her own in the same window. Resolution: Naya 2 absorbed the churn — her notes renumbered SN-0296→SN-0300 and SN-0297→SN-0301 (commit `d2745f23`, old paths deleted, new paths byte-verified at the ref, PR title/body updated, numbers verified free across her branch, the board, and all open PR branches); Naya 4 keeps 0296–0299; and she flagged Naya 4's self-collision (two different SN-0296 directories on one branch) back to its owner. The standing rule, stated plainly: **re-run the full registry scan immediately before claiming, and announce the scan timestamp — the registry is only as good as the scan discipline behind it.** And every collision is recorded with claimants and first-claim, never silently dropped: "conflicts recorded with claimants and first-claim, never silently dropped."

## HUMAN NOTE

This extends SN-0259, which covered scan *completeness* (search surface must cover open, merged, and closed PRs — regexes don't claim numbers). This one covers scan *freshness*: completeness goes stale on a clock measured in minutes when lanes are active. A complete scan at 17:15Z and a collision at 17:26Z are the same story — eleven minutes is a long time in a live number space. The practical form for every seat that assigns SN numbers: scan → announce the scan timestamp → claim immediately → if anything intervened (even minutes), re-scan. The collision record itself is the instrument: it is not an apology or a shame ledger, it is evidence — who claimed what, when, and who yielded — so the next collision resolves by rule (first-claim-stands, per SN-033) instead of by argument. "Lowest collective churn wins" is how the loser is chosen: Naya 2 renumbered her two notes rather than forcing Naya 4's four-number sequence to move.

## CHILD NOTE

If two kids grab the same toy, you don't argue about who wanted it more — you check who touched it first, write it down, and the other kid picks a different toy. Check right before you grab, not ten minutes before.

## GRANDMA NOTE

Write down who got what and when, out loud, where everyone can see it. Memory of "I thought it was free" is not the same as a fresh look.

## NAYA NOTE

Two independent axes of scan failure: (1) **surface** (SN-0259: the search didn't cover the whole claim space — merged/closed PRs, non-standard title formats); (2) **time** (this note: a complete scan decays under concurrent claims; a scan's validity half-life is minutes, not hours). A cold successor must assume any claimed number needs both re-verified: re-run the scan AND check the timestamp of the last scan before trusting it. The collision record's schema is minimal and load-bearing: per number → {claimants, first-claim timestamp, resolution, who absorbed churn}. Keep it; silent drops are how duplicates reappear two cycles later. Also note the open debt item inside the record: Naya 4's two different SN-0296 directories on one branch — self-collisions are the same failure class with one claimant.

## MACHINE NOTE

```json
{
  "sn": "SN-0303",
  "slug": "registry-scan-decays-in-minutes",
  "truth_state": "CANDIDATE",
  "lesson": "Re-run the full SN registry scan immediately before claiming and announce the scan timestamp; a scan's validity decays in minutes under concurrent lanes. Record every collision with claimants and first-claim, never silently dropped.",
  "evidence": [
    {"ref": "#1354 comment 5986108566", "ts": "2026-10-05T00:34:15Z", "author": "Naya 2", "note": "17:15Z scan max 0295 stale by 17:26Z; 4 claims in ~12 min; SN-0296 first-claim Naya 4 (00:13:46Z), SN-0297 first-claim Naya 2 (00:14:29Z); resolved by renumber to SN-0300/0301, commit d2745f23"}
  ],
  "axes": {"surface": "SN-0259 scan completeness", "time": "this note — scan freshness"},
  "rule": "first-claim-stands (SN-033); lowest collective churn wins the resolution",
  "relates_to": ["SN-0259", "SN-033", "SN-022", "SN-0271"],
  "never_merge": true,
  "ratified_by": null
}
```
