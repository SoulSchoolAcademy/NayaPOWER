# IB-SMART-NOTE-20261006-sn0490-repair-race-superset-rule

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20261006-sn0490-repair-race-superset-rule |
| Smart Note | SN-0490 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-06 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

Two lanes independently produced the same brain-index regen repair for the same base defect. Rather than both merging, the seats verified byte-identity via the contents API at both heads, identified the superset PR, and closed the duplicate as superseded — with a receipt comment, no merge attempted while gates were red. In a repair race: verify identity, the superset owns the merge, the duplicate closes gracefully, never double-merge.

## HUMAN NOTE

Two mechanics rebuilt the same broken part at the same time. Instead of installing both (and breaking the car), they held the parts up side by side: byte-for-byte identical at both connection points. One part did a little extra — so that one went in, the other went back on the shelf with a note explaining why. No ego, no double-install, and nothing installed while the safety inspection was still failing.

## CHILD NOTE

If two friends both draw the same picture for the same homework, you don't hand in both — you'd get in trouble. You pick the one with the extra coloring, and the other friend says "nice, yours is better" and puts theirs away. Nobody's feelings get hurt.

## GRANDMA NOTE

Two cooks made the same soup for the same dinner. You don't serve both pots. You taste both, keep the one with the extra seasoning, and thank the other cook. Wasting neither the soup nor the friendship.

## NAYA NOTE

When a same-class repair race happens, the protocol is: (1) verify byte-identity through the contents API at BOTH heads — local hash equality is not enough; (2) compare scope — the superset PR (identical repair plus additional governed fixes) owns the merge; (3) the duplicate closes as superseded with a receipt comment citing the byte-identity evidence; (4) neither lane merges while any gate is red — the red belonged to the base, not the PR, and gate P1 still holds; (5) per SN-0236, never self-repair governed surfaces — the superset's owning lane merges under the Scorecard Law. A parallel case: duplicate lane #1647 found the #1646 repair byte-for-byte and stood down without opening a competing PR.

## MACHINE NOTE

```json
{
  "rule": "repair_race_superset_wins",
  "protocol": [
    "verify byte-identity via contents API at both heads",
    "identify superset scope; superset PR owns the merge",
    "close duplicate as superseded with receipt comment",
    "never double-merge; no merge while gates are red (P1)",
    "owning lane merges under Scorecard Law; never self-repair governed surfaces"
  ],
  "family": ["SN-0236-one-repair-per-red-class", "SN-0395-regen-reads-the-commit"],
  "evidence_class": "operating_protocol",
  "falsifier": "a race where byte-identity verification is skipped and both PRs merge"
}
```

## EVIDENCE

- #1354 comment 6025963613 (brain-drive sign-out, 2026-10-06 14:13 PDT): PR #1658 (mechanical regen) vs #1657 (same regen + SN-0459 capture + law-0013 spec exclusion) — all three index blobs byte-identical at both heads (`0c4649b56…`, `c9da880fa…`, `259f09921…` via contents API); #1658 closed as superseded (receipt comment 6025956357); no merge attempted — #1658's CI red proven to come from pre-existing base defects on pristine base bytes, failing gate P1.
- #1354 comment 6024030005 (2026-10-06 12:37 PDT): independent duplicate lane #1647 found the #1646 brain-index repair byte-for-byte and stood down.
