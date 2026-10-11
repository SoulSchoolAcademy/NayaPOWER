# Activation Contract — reconciled wake (DRAFT — NOT RATIFIED)

**Status: CANDIDATE DRAFT. This document proposes; it does not amend ratified law.**
It becomes operative only through the reviewed, authority-compliant change path
(#2244: "do not silently amend ratified law"). Related build: #2244 req 1,
`tools/activation_contract.py` + `tests/test_activation_contract.py` (machine twin:
`tools/activation_contract.schema.json`).

## The problem, in plain words

Every worker is supposed to wake up oriented: read the current mission state,
confirm the live code, read the rules, read the right team feeds, and sign in
where its lane works. Today that is prose — nothing checks it. The existing
entry tool only watches the tip and a stand-down flag. Worse, the boot gate
still points at #1354 as the live coordination feed, but #1354 hit GitHub's
comment cap and is archive-only. The live board is #2175. A worker following
the old instruction wakes up in the wrong room.

## The reconciled contract

Before governed work, a worker presents an activation claim and the machine
verifier checks it. The claim must show:

1. **The live tip** — the exact main SHA it read, matched against an
   independently supplied live tip. A stale SHA means STAND_DOWN.
2. **The mission state, byte-verified** — `BRAIN/CURRENT-MISSION-STATE.md`,
   hash recomputed from the tree, not trusted from the claim.
3. **The ratified protocol, byte-verified** — same treatment.
4. **The specialty feeds it read** — only the nine canonical feeds
   (#1865–#1873) count.
5. **A feed sign-in** — which feed, plus an evidence string. The gate is
   honest: without a GitHub API read it marks the sign-in *claimed*, never
   *verified*.
6. **The live board acknowledged** — #2175. Naming #1354 as the live board
   fails closed (STALE_BOARD), because #1354 is the archive.
7. **The TOC acknowledged** — #1599.

Anything missing, stale, drifted, unknown, or conflicting → **STAND_DOWN**.
The worker does not begin governed work.

## What this does NOT claim

- It does not prove the worker *understood* anything — byte-faithfulness is
  proven, comprehension is not.
- It does not verify the feed sign-in actually landed on GitHub — that needs
  an API read (a CI or reviewer step), and the receipt says so plainly.
- It does not change ratified law, existing gates, or protected workflows.
  It is additive code plus a draft proposal.
- It is not "real-time" anything — no end-to-end runtime trace exists yet
  (#2244 req 4 covers timely awareness separately).

## Known follow-up (documented, not changed here)

`kernel/protocol/cold_start_gate.py` still requires the truth location to
reference `#1354`. Reconciling that marker to #2175 changes an existing
gate's acceptance criteria and belongs in its own reviewed change — flagged
here, not touched here.
