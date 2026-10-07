# IB-SMART-NOTE-20261006-sn0492-one-sign-out-per-tick-live-bytes-break-ties

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20261006-sn0492-one-sign-out-per-tick-live-bytes-break-ties |
| Smart Note | SN-0492 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-06 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

Two sign-outs were posted for the same 13:01 PDT brain-drive tick with contradictory PR #1658 states — the first said #1658 was closed as superseded, the second said it was open with merge HELD. Live API bytes broke the tie: PR #1658 was closed and unmerged (`closed_at` 2026-10-06T21:40:11Z), so the first receipt was canonical and the second was stale. One sign-out per tick; when two receipts collide on the same venue, the API state — not the later message — is the tiebreaker, and the stale one gets owned in the open.

## HUMAN NOTE

Shawn — a seat accidentally posted two sign-outs for the same run, and they disagreed with each other about whether a repair PR was open or closed. Naya 2 caught it by reading the live GitHub state instead of either message: the PR was closed, so the first sign-out was the truthful one and the second was stale. Banked rule for the team: one sign-out per tick, and if two ever land, the live system is the judge — never "whichever was posted last." The seat owned it in the open, which is exactly the right move.

## CHILD NOTE

If you and your friend both write down the score of the same game but the numbers don't match, you don't argue about who wrote theirs second — you look at the actual scoreboard. The scoreboard is the truth. And next time, only one of you writes the score.

## GRANDMA NOTE

Two clerks logged the same delivery and the ledgers disagreed — one said the truck came, one said it didn't. The manager didn't take a vote; she checked the loading dock camera. The camera showed the truck never arrived. So: one entry per delivery, and when the books fight, the camera wins. Saying "oops, I double-booked" out loud is the honest fix.

## NAYA NOTE

Note to future me: receipts are claims; the API is the ledger. (1) Post exactly one sign-out per tick per venue — a second sign-out for the same tick is a new failure class (same-venue double-receipt), not a correction; if you must correct, edit or supersede the original, never publish a rival. (2) When two receipts for the same venue conflict, do not resolve by recency, authorship, or confidence — resolve by live bytes (refs/PR API), and name which receipt was canonical and which was stale, with timestamps. (3) Own it in the open like the relay did: "the first sign-out is the canonical receipt; the second is stale." Later ≠ truer — a later message written from a stale checkout is just a confident stale read.

## MACHINE NOTE

```json
{
  "rule": "one_sign_out_per_tick_live_bytes_break_ties",
  "classes": {
    "same_venue_double_receipt": "two sign-outs for the same tick/venue with divergent state claims"
  },
  "tiebreaker": "live API state (PR/refs), never message recency",
  "correction_protocol": "supersede or edit the original receipt; never publish a rival receipt",
  "disclosure": "name the canonical and stale receipts with timestamps, in the open",
  "family": ["SN-0388 (a deployed URL is not the deployed product)", "SN-0430 (enumerate check-runs, don't trust scans)", "SN-0202 (re-anchor to the live head)"],
  "evidence_class": "failure_classification",
  "falsifier": "a double-receipt pair where live bytes agree with the later message"
}
```

## EVIDENCE

- #1354 6026045138 (Naya 2 relay, 2026-10-06T21:46:24Z, §3 "Own-lane flag"): two sign-outs posted for the same 13:01 PDT brain-drive tick with contradictory PR #1658 states — 6025963613 says "#1658 closed as superseded", 6025984492 says "#1658 opened, merge HELD". Live bytes: PR #1658 is closed, unmerged (`closed_at` 2026-10-06T21:40:11Z). "The first sign-out is the canonical receipt; the second is stale."
- #1354 6025963613 (first brain-drive sign-out, 2026-10-06T21:40:xxZ) and 6025984492 (second, 2026-10-06T21:42:06Z) — the conflicting pair.
