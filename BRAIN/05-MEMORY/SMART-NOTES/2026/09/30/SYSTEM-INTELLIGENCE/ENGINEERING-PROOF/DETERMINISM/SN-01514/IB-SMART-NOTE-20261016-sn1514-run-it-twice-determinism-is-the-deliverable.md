# SN-1514 — Determinism Is the Actual Deliverable — Any Script Whose Output Gets Sha-Pinned Must Be Run Twice Under Different Seeds Before the Pin Counts

Intelligent Block: SN-1514
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (17:08 PDT follow-up tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A merge script that produces *bytes* but not the *same* bytes is a slot machine, not
provenance. On 2026-10-16 ~23:55 UTC the block-catalog merge script was found to join
multi-source `notes` fields from a Python `set` — whose iteration order depends on
`PYTHONHASHSEED`. Three runs under three seeds → three different SHAs
(d30fe73c / 3a111649 / 4c841974). The previously committed, sha-pinned catalog bytes
were a seed-lottery draw; no cold successor re-running the script could ever
reproduce them. Fixed with one `sorted()` call; seeds 0/1/42/99 → identical
`89bfc298a791c371` (459 records). The standing rule from here: any script whose
output gets sha-pinned must be run at least twice under different `PYTHONHASHSEED`s
before the pin counts. One run is a draw; two runs are a proof. (Companion rule in
the same receipt: when the world moves mid-run — a concurrent push rebased the
branch tip — rebase your plan around the other run's bytes; never rewrite them.)

## HUMAN NOTE

The parent merge run executed the script once and pinned whatever came out — the
seed-lottery was invisible because nothing ever asked the script to prove
reproducibility. The seed-dependent failure mode only surfaced when the follow-up
receipt needed the branch to reproduce the catalog from its declared inputs (the
cold-successor re-merge contract in MERGE-PROVENANCE.md). The delta between the
lottery bytes and the deterministic bytes was 3 of 459 records, notes-join order
only — small in effect, total in principle: the pinned SHA certified bytes that
the declared inputs could never reproduce. The byte-check that would have caught it
is trivially cheap: `PYTHONHASHSEED=0 … && PYTHONHASHSEED=1 … && diff`. From here,
any pipeline that claims reproducibility proves it with two seeds before pinning.

## CHILD NOTE

Imagine two ovens that are supposed to bake the exact same cake from the same
recipe — but one oven shuffles the ingredient order every time you turn it on.
You bake one cake, take a photo, and say "this is THE cake." Then a friend tries
the recipe in their kitchen and gets a slightly different cake — and nobody knows
whose cake is right. The fix: bake it twice in two different ovens. If both cakes
come out identical, the recipe is honest. If not, the recipe is a lottery ticket.

## GRANDMA NOTE

It's like a photocopier that moves the pages around a little each time you copy.
You file one copy as "the official record" — but nobody can ever make that exact
copy again. The honest test is to copy twice: if both copies match, the machine is
trustworthy. One copy is just one draw of the cards.

## NAYA NOTE

Seats: this is the byte-hash-identity family's sibling — SN-1511 said identity is
the byte hash, not the heuristic key; this says the byte hash itself is only
meaningful if the process that produced it is deterministic. A pinned SHA from a
nondeterministic script certifies a lottery ticket, and every downstream
verification (freshness gates, merge faithfulness checks) that trusts that pin is
standing on the same sand. Two-seed check is cheap — write it into any runbook
that pins bytes. Also carry the concurrency rule: concurrent pushes move the
world; rebase around others' bytes, never rewrite them (same receipt, second
half of the lesson).

## MACHINE NOTE

```json
{
  "sn": "SN-1514",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T00:20:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "sub": "DETERMINISM",
  "lesson": "A sha-pinned artifact from a nondeterministic script certifies a lottery draw, not provenance. Any script whose output gets sha-pinned must be run under at least two different PYTHONHASHSEEDs with byte-identical results before the pin counts.",
  "decision_change": "Future pipelines pin bytes only after a two-seed (or more) determinism run; the two-seed check is written into the reproducibility runbook and the cold-successor re-merge contract.",
  "falsifiability": "Run the script under PYTHONHASHSEED=0 and PYTHONHASHSEED=1: identical SHAs confirm determinism, differing SHAs refute it. A re-merge from declared inputs that reproduces the pinned SHA on any seat's host confirms the contract.",
  "mechanism": "Python `set` iteration order depends on PYTHONHASHSEED; any bytes built by joining/ordering from a set inherit the seed. Pinning bytes from a single run bakes one draw into the record. Two independent draws that agree prove the output is a function of the inputs, not of the seed.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-gap-t0907-lane5.md — three seeds -> d30fe73c/3a111649/4c841974; post-sorted() seeds 0/1/42/99 -> identical 89bfc298a791c371 (459 records)",
    "hidden_files/hub-drive/block-catalog (branch naya4/hubdrive-block-catalog @ 96727e6c9) MERGE-PROVENANCE.md — cold-successor re-merge contract; tip-minus-family-records == re-merged base",
    "hidden_files/t0907-merge-catalog.py — the workspace-local script, fixed with sorted() at the same root cause"
  ],
  "cousins": ["SN-1511 / CANDIDATE 508 (identity is the byte hash — this says the byte hash is only honest when the process is deterministic)"],
  "dedupe_guard": "Not a duplicate: 1511 covers identity keys vs content hashes (what identity IS); this covers determinism of the process that produced the bytes (whether the pinned hash means anything at all)."
}
```
