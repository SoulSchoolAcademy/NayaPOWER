# Records Vanish — Restore to the Verified State

SN-3316 · OPERATIONS — SERVING INCIDENT

**Filed:** Intelligence Loop filing push #3 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3313; filed as SN-3316 renumbered from provisional SN-3287.

**Created:** 2026-11-18 ~03:48Z (Resolve's SERVING INCIDENT, reported in the 03:48Z wave dispatcher pass; recorded in the daily log; drafted in run 294)

**Paired Naya Note:** NN-20261118-records-vanish-restore-to-the-verified-state

## Hook

The nayanet.app apex+www AAAA records vanished — last good 02:55Z, first NXDOMAIN 03:25Z — with nobody changing them. The recovery was not to guess new records but to restore the last verified state: the 2026-11-03 four-record state, verified HTTP 200 ×3. A record can vanish without anyone touching it; the verified state is the ground truth to restore to.

## Nutshell

Resolve's SERVING INCIDENT (03:48Z wave dispatcher pass): nayanet.app apex+www AAAA records vanished — last good 02:55Z, first NXDOMAIN 03:25Z — restored to the verified 2026-11-03 four-record state, HTTP 200 ×3 verified. Not attributed. **THE LESSON:** a DNS record can vanish without anyone changing it — no audit event, no hand on the dashboard, and the domain goes NXDOMAIN all the same. The recovery is not to invent new records or to argue about what was there: it is to restore the last verified state — the 2026-11-03 four-record state — and then verify by fresh fetch, HTTP 200 three times over. **THE COMPANION:** SN-3315 carries the route-list half of the same outage — the DNS restoration put the domain back, and the six new routes put the unrouted paths back; together they explain why the 03:18Z wave's three-channel live check failed (DNS unreachable that wave) and why the "DARK" reading was wrong in the large (the domain resolved again by 03:43Z; only the unrouted paths 522'd). **THE OPEN QUESTION, NAMED NOT HIDDEN:** the vanishing is not attributed — nothing in the record says what removed the records. The verified state is the ground truth to keep; the cause of the vanishing is still owed to the serving lane.

## Human

Records are supposed to sit still until someone changes them. These did not. The apex and www AAAA records for nayanet.app were there at 02:55Z and gone by 03:25Z — no change event, no hand, no attribution — and the domain answered NXDOMAIN in between. The right recovery is not to redesign the DNS or to guess at new values: it is to put back exactly what was verified before, the 2026-11-03 four-record state, and then to prove it three times over with fresh fetches that return 200. That is the discipline this incident teaches: keep a verified state on record, because the day a record vanishes without a cause is the day the verified state is the only thing you can trust. And say plainly what is not known — the vanishing is unattributed — rather than inventing a cause to close the story.

## Child

Imagine the address of your house suddenly disappears from the map, and nobody erased it. That's what happened — the address records just vanished. The fix wasn't to make up a new address. It was to put back the exact address that was written down and checked before — the one from November 3rd — and then knock on the door three times to make sure someone answers. Always keep a good copy of the address written down, because sometimes things disappear for no reason anyone can see.

## Grandma

Dear, the address of the site just disappeared, dear — nobody erased it, dear, it was simply gone. The fix wasn't to make up a new one, dear — it was to put back the exact address that was written down and checked before, dear, and then knock on the door three times to make sure someone answers, dear. Always keep a good copy written down, dear, because sometimes things disappear for no reason anyone can see.

## Naya

RECORDS VANISH. RESTORE THE VERIFIED STATE. PROVE IT THREE TIMES. KEEP THE VERIFIED STATE ON RECORD.

## What it means

- **THE INCIDENT:** nayanet.app apex+www AAAA records vanished — last good 02:55Z, first NXDOMAIN 03:25Z.
- **THE RECOVERY:** restored to the verified 2026-11-03 four-record state; HTTP 200 ×3 verified.
- **THE RULE:** when a record vanishes, restore the last verified state — do not guess new records.
- **THE PROOF:** fresh fetch, HTTP 200 three times over — a restore is not done until the live path answers.
- **THE OPEN QUESTION:** the vanishing is not attributed — the cause is still owed to the serving lane.
- **THE COMPANION:** SN-3315 (route list) is the other half of the same outage; together they correct the "DARK" reading.

## Why it matters

Without this note, the next vanished record gets "fixed" by guessing — new values invented on the spot, no verified state to check against, and the site left half-right. With it, the rule is settled: keep a verified state on record, restore exactly that state when a record vanishes, and prove the restore with live fetches. And the honesty rule rides with it: an unattributed vanishing stays unattributed until the serving lane finds the cause — it is not closed by a story.

## What changes now

1. The 2026-11-03 four-record state is the recorded ground truth for nayanet.app DNS.
2. A vanished record is recovered by restoring the verified state, never by guessing.
3. A restore is proven by fresh fetch — HTTP 200 three times over.
4. The cause of the vanishing stays open and owed to the serving lane.
5. Correction Compound inventory + brief-template steps are owed for this correction and recorded as owed — not claimed done.
