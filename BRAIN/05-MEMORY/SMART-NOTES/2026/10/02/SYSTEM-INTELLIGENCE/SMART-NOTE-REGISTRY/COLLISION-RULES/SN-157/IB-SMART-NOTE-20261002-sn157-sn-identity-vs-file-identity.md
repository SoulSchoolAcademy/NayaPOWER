# SN-157 — Smart-Note identity is (SN-NNN, IB-identity), not SN-NNN alone

| Field | Value |
|---|---|
| **Smart Note** | SN-157 |
| **Intelligent Block** | IB-SMART-NOTE-20261002-sn157-sn-identity-vs-file-identity |
| **Truth state** | CANDIDATE |
| **Captured** | 2026-10-02 04:10 UTC (2026-10-01 21:10 PDT) |
| **Source** | brain-build verification battery 20261002-0356 on main `426940469404e99285e4372d5c956412fc0cfd45`; receipts: battery log, `git diff` of the two SN-018 files, PR #1307, PR #1229 tree |
| **Supersedes** | nothing; refines the SN-collision registry rule (AGENTS.md standing lesson) |

## IN A NUTSHELL

A Smart Note's identity is the pair **(SN-NNN, Intelligent-Block identity)** — not the SN-NNN alone, and not the file path alone. The smart-note-projection pipeline publishes verified projections under the current date partition, so one block legitimately exists as two files: `SN-018` under `2026/10/01` (authored capture) and `SN-018` under `2026/10/02` (verified projection). Same SN-NNN + same IB = **one claim, two files — not a collision**. Same SN-NNN + different IB = **true collision** (main's SN-018/019 vs PR #1229's SN-018/019 seeds). The collision registry must compare IB identity before flagging.

## HUMAN NOTE

Think of the SN number as a street address and the Intelligent Block as the deed. Two letters delivered to the same address for the same owner is normal mail, not a property dispute. Two different owners claiming the same address is the dispute. When the watchtower sees SN-018 in two date folders, it must read the deed (the `**Intelligent Block:**` line) before sounding the alarm.

## CHILD NOTE

Imagine your friend writes a story and saves it in two folders — "Monday" and "Tuesday". It's still one story, not two stories fighting over a name. But if a *different* friend writes a *different* story and also calls it by the same name, that's a real mix-up. Always check: same story, or different story?

## GRANDMA NOTE

It's like a recipe card. If you photocopy your apple-pie recipe and file one copy under "October" and another under "November", you still have one recipe. The trouble only starts if someone else files a *different* apple-pie recipe under your recipe's number. The number alone doesn't tell you — you have to read the recipe.

## NAYA NOTE

For machine processing: the collision predicate is `collision(a, b) := (a.sn == b.sn) AND (a.ib_id != b.ib_id)`. File path, date partition, and projection-vs-capture status are NOT inputs to the predicate; they are routing metadata. A projection file is identified by its header disclaimer ("This file is not a second source of truth" / "not a second machine source of truth") plus IB-identity equality with the authored capture.

## MACHINE NOTE

```json
{
  "rule": "sn_collision_predicate_v1",
  "predicate": "same_sn_nnn AND different_ib_identity => TRUE_COLLISION",
  "non_collision": "same_sn_nnn AND same_ib_identity => PROJECTION_DUPLICATE (one claim, N files)",
  "ib_identity_source": "the `**Intelligent Block:**` header line, exact string match",
  "projection_marker": "header contains 'not a second source of truth'",
  "registry_key": ["sn_nnn", "ib_identity"]
}
```

## LEARNING LESSON

The standing collision-registry lesson ("duplicates can hide across date partitions") was underspecified: it keyed on SN-NNN alone, which false-positives on the projection pipeline's normal output. The 20261002-0356 battery proved the refinement on live bytes: `diff` of main's two SN-018 files shows identical `IB-SMART-NOTE-20261001-hub-is-intelligence-projection` with only projection-wording differences — one claim, two files. The same battery proved the true-collision case the same way: #1229's `SN-018/IB-SMART-NOTE-20260930-sn018-canonical-spec-placement` and `SN-019/IB-SMART-NOTE-20260930-sn019-direct-lane-protocol` are different IBs from main's SN-018/019 — true collisions if #1229 merges as-is. **Identity is the pair; the number is only half the key.**

## HOW IT CONNECTS

- **SN-027 (amendment premise verification):** same family — verify the cited identity (here: IB line) before acting on the label (here: SN-NNN).
- **SN-012 duplicate (fixed by #1237):** the true-collision archetype — two different blocks, one number, on main.
- **Index-ledger tripwire (`tools/regenerate_brain_index.py`):** counts *files*, so every projection publish re-trips it (21→24 bump, PR #1307). The tripwire is file-counting by design; the registry is identity-resolving by design. Do not confuse the two instruments.
- **PR #1229 (other seat, DRAFT):** claims SN-017…SN-102 including SN-018/019 with different IBs — ~85 claimed numbers, 2+ true collisions vs main. Renumbering is the owning lane's call; this note only classifies.

## EPISTEMIC STATE

CANDIDATE. The predicate is proven on the observed instances (main's SN-018 pair; #1229's SN-018/019 vs main) but not yet ratified as registry law.

**Falsifier:** produce two files sharing SN-NNN and byte-identical `**Intelligent Block:**` lines whose normative content differs beyond projection wording (i.e., IB-identity fails as an identity bearer), or a projection file whose header lacks the not-a-second-source disclaimer yet duplicates an SN-NNN (predicate input unmarked).

## UNCERTAINTY

- Whether the projection pipeline republishes *unchanged* blocks on a schedule (if yes, same-SN-N-files recurs and the registry must stay IB-keyed permanently) or only on block revision.
- Whether PR #1229 merges as-is (would convert 2+ watched true collisions into main-namespace collisions) or renumbers first (owning lane's call).
- Whether seats will honor the (SN-NNN, IB) key or keep minting by number alone.

## APPLICABILITY

- Every future collision-registry scan (watchtower): compare IB identity before flagging same-SN-NNN files.
- Every index-ledger repair: a same-IB projection duplicate still counts as a real file for the tripwire — bump deliberately, do not force.
- Any seat minting a Smart Note: check (SN-NNN, IB) against main + open SN PRs + the #554 collision registry, then take the next free number (this note took SN-157: main max SN-019; #1229 claims through SN-102; #554 mentions through SN-156).

## SUCCESSOR EFFECT

A cold successor running the registry scan will not false-positive on projection duplicates and will not trigger renumbering churn for them; it will reserve its flags for true (SN-NNN, IB) collisions. Each avoided false collision saves one investigation cycle and one cross-seat coordination round.
