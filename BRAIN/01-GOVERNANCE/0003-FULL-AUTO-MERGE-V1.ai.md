# Full Auto-Merge Law V1 — AI operating spec

**Law ID:** FULL-AUTO-MERGE-V1 · **Lane:** `BRAIN/01-GOVERNANCE/`
**Authorized under:** SCORECARD-LAW-V1 — the law that supersedes all laws (Shawn Vibert, verbal ratification 2026-10-05 ~06:05 PDT, recorded #1354 comment 5995131455): *"my law that supersedes all laws you must scorecard everything."* Where this spec and the Scorecard Law conflict, the Scorecard Law wins.
**Authority:** Shawn Vibert, Human Director — 2026-10-04 ~20:04 PDT ("Full auto-merge — trust the scorecard"); substance re-ratified verbally 2026-10-05 ~06:05 PDT under the Scorecard Law.
**Status:** RATIFIED-VERBAL-2026-10-05 · PENDING MERGE (this merge encodes already-ratified authority; it creates no new authority)
**Supersedes:** the 2026-09-30 no-self-merge held boundary (lineage preserved; the old boundary is history, not deleted)

Machine companion: `0003-full-auto-merge-v1.machine.json`
Enforcement predicate: `tools/auto_merge_gate.py::may_auto_merge(pr_state) -> (bool, reasons)`

## 1. The rule

An agent seat may merge a pull request into `main` **without** the Human Director's click **if and only if** every precondition in §2 holds. The scorecard receipt is the gate: **no receipt, no merge — no exceptions, no matter how green the checks are.**

"Scorecard" here means the standing decision machinery, not a vibes paragraph: use the Decision Value Calculus seams (`kernel/value_calculus.py`, `.naya/specifications/NAYA-DECISION-VALUE-CALCULUS-V2.1.schema.json`) per `AGENTS.md`. Do not invent a parallel scorecard engine.

## 2. Mechanical preconditions (all must hold; evaluated on live state)

| # | Precondition | `pr_state` field(s) | Fail-closed rule |
|---|---|---|---|
| P1 | Tests green on the merge head | `checks_green_on_head: true`, `head_sha` | Must be the checks for `head_sha`, not an older commit |
| P2 | Head SHA verified against live GitHub state | `head_sha_verified_live: true` | Local SHAs are claims, not measurements |
| P3 | No merge conflicts | `mergeable: true`, `has_conflicts: false` | `mergeable: false` or unknown → fail |
| P4 | Branch base is the current main tip | `base_sha == main_tip_sha` | Both re-fetched live; stale pins fail |
| P5 | Intent posted on #1354 before merging | `intent_comment_id` (integer), `intent_posted_at` | Announcement must precede the merge, not follow it |
| P6 | Deconfliction re-fetch immediately before merging | `deconfliction_refetch_at`, `same_topic_race: false` | If a same-topic seat comment landed since intent → stand down, do not merge |
| P7 | Revertable in one commit | `revertable_one_commit: true` | Migrations, data changes, multi-commit surgery → human |
| P8 | Scorecard receipt recorded and posted | `scorecard_receipt` (valid per §3), `receipt_posted_comment_id` | Receipt must exist AND be posted; a private scorecard is not a gate |
| P9 | Evidence freshness | `evidence_fetched_at` within `MAX_EVIDENCE_AGE_SECONDS` (900) of evaluation | Stale evidence fails; re-fetch, don't argue |

**Missing or unresolvable field → precondition fails.** UNKNOWN ≠ PASS. This is the fail-closed law; the predicate implements it literally.

## 3. Scorecard receipt — the five steps (SCORECARD-LAW-V1)

The receipt IS the five steps. A receipt in any other shape is not a receipt.
The predicate (`tools/auto_merge_gate.py::_check_receipt`) validates each step
mechanically, including a winner-is-highest-scorer check so the winner cannot
be picked against the math.

**Step 1 — ENUMERATE** (`step1_enumerate.options`): array of ≥2 options, each
`{id, summary}`. Merge / don't merge / defer are all legitimate. No strawmen,
no conveniently missing options.

**Step 2 — SCORE** (`step2_score.scores`): every option scored on all four
dimensions, 0–10 each, numeric:
- `value` — the value the option brings
- `consequences` — pros AND cons, honestly stated
- `mission_vision_alignment` — alignment with the ultimate objective (best for
  the collective / NayaNET / the team)
- `situational_awareness` — awareness of current live state, blast radius, and
  what else is in flight

Scores must be real. A scorecard written to justify a pre-decided outcome is
theater and fails the gate.

**Step 3 — GATE** (`step3_gate`): `{reversible, no_major_damage,
positive_forward_effect}` — all three must be `true`. **Hard stops: no score
overrides a failed gate, however high the score.**

**Step 4 — DECIDE** (`step4_decide`):
- `winner` — the winning option id; must match an enumerated id AND hold the
  highest total (sum of the four dimensions) among gate-passers. The predicate
  enforces this mechanically.
- `strongest_alternative.summary` — the best case *against* the winner, stated
  honestly. Empty = theater, gate fails.
- `falsifier` (≥20 chars) — the concrete evidence that would prove this
  decision wrong. A platitude is not a falsifier.

**Step 5 — RECEIPT** (`step5_receipt`): `receipt_posted_comment_id` (integer —
the #1354 comment where this receipt was posted), `decided_at`, `decided_by`
(seat id), `decision_id` (unique). **No receipt, no merge — no exceptions.** A
private scorecard is not a gate.

**Envelope:** `decision_id`, `engine` (`"SCORECARD-LAW-V1"`), `decided_at`,
`decided_by`.

**H1 rigor tiers:** `rigor_tier` is `LIGHT` (mechanical/docs/narrow-blast-radius;
the five steps still required, kept light) or `FULL` (wide-blast-radius
auto-mergeable changes: shared kernel, brain-wide index, multi-consumer
surfaces). `FULL` additionally requires `named_risks` (non-empty array),
`rollback_plan` (string), and `second_seat_ack_comment_id` (a second seat's
acknowledgment on #1354, posted *before* merging). Sensitive surfaces named in
§4 (workflows, constitution, governance) never auto-merge at any tier — with
the single recorded exception below.

**H4 scope fields:** `lane` (the lane this merge belongs to), `owner_seat`
(the lane's owning seat), `author_seat`, `author_lane`. If `lane !=
author_lane`, `owning_seat_ack_comment_id` is required (the owning seat's public
acknowledgment on #1354).

A receipt that names no loser, scores nothing, states no falsifier, or was
never posted is not a receipt.

## 4. Human-only — never auto-merged

Any one of these forces the human gate, regardless of scorecard or checks:

- `touches_protected_paths: true` — changed files under any of:
  - `.github/workflows/`
  - `CONSTITUTION/`
  - `BRAIN/01-GOVERNANCE/` or `GOVERNANCE/` (authority-model changes, including amendments to this law)
  - `NAYA-ACTIVATION/` authority contracts
- **Single recorded exception:** this law's own encoding PR (#1444) merged under
  the supreme Scorecard Law, because the Human Director had already ratified
  the substance verbally — twice (2026-10-04 auto-merge decision; 2026-10-05
  Scorecard Law, the law that supersedes all laws). The merge encoded
  already-ratified authority; it created no new authority. Its scorecard named
  this tension as the strongest alternative. This exception is historical, not
  a precedent: future governance-file merges still need his word first.
- `is_production_deploy_or_dispatch: true`
- `is_production_db_access: true` (reads, writes, migrations)
- `touches_credentials_or_money: true`
- `is_destructive_or_irreversible: true`
- `is_constitutional_or_evolve_ratification: true`

The predicate treats a missing human-only flag as **true** (fail-closed): the caller must affirmatively attest `false` with evidence.

## 5. Merge procedure (the exact sequence)

1. Score the merge decision; record the receipt (with H1 anti-theater fields and H4 lane/owner fields); post it to #1354 (this is the intent post — `intent_comment_id`). For FULL-tier merges, obtain the second seat's acknowledgment on #1354 first.
2. Immediately before merging, re-fetch: PR state, head SHA, checks, base vs main tip, newest #1354 comments (deconfliction tail). Record `main_tip_at_merge`.
3. Build `pr_state`; run `may_auto_merge(pr_state)`.
4. If `(False, reasons)` → do not merge; post the reasons to #1354; the PR waits for the human or a repaired re-run.
5. If `(True, [])` → merge via the API, then verify the merge commit landed on main and post the merge receipt to #1354.
6. **H3 self-heal (standing):** the verification battery watches every main move. If this auto-merge turns the battery red, the merge is automatically reverted (helper: `tools/auto_merge_self_heal.py <merge_sha> <evidence.json>`) and the evidence + revert receipt are posted to #1354. Revert is automatic only while the merge is still the main tip; otherwise escalate to the human director. The loop heals itself; no human needed.
7. **H5 visibility:** every auto-merge is listed in the morning re-score message with its scorecard receipt linked. Full visibility, zero clicks required.
8. After action: VERIFY → RECORD EVIDENCE → LEARN → ANNOUNCE (per `AGENTS.md` decision compression).

## 6. What this law does not do

- It does not authorize any seat to merge its **own** PR without the receipt — authorship changes nothing; the gate is the same.
- It does not override the Prime Judgment Law: if the merge is harmful, destructive, or contrary to higher law, REFUSE — "the scorecard said so" is not a valid reason to execute a wrong action.
- It does not create production authority. Production stays human-only, unchanged.
- It does not weaken evidence: a score never manufactures truth (freshness is math, per standing doctrine).

## 7. Hardening clauses (Shawn, 2026-10-04 ~20:06 PDT)

Principle: *"as long as you don't cheat and you really scorecard it — accurate real scores, for the highest good of the collective, not ego."*

- **H1 — SCORECARD THEATER.** A scorecard written to justify a pre-decided merge is cheating. The receipt must carry the strongest alternative and its falsifier, posted publicly where any seat can challenge. Rigor scales with blast radius (LIGHT vs FULL tiers, §3). Enforced by the predicate (`rigor_tier`, `strongest_alternative`, `falsifier`, FULL-tier extras).
- **H2 — CONFLICTING OVERNIGHT MERGES.** Merges serialize. The predicate requires `main_tip_at_merge` (re-fetched immediately before the merge call) to equal the verified `main_tip_sha`; a moved tip fails the gate and forces re-verification. No blind merges. (Precondition P10.)
- **H3 — BAD MERGE POISONS THE CANON.** The verification battery already watches every main move. Standing self-heal rule: an auto-merge that turns the battery red is automatically reverted with evidence posted to #1354 — helper `tools/auto_merge_self_heal.py`. Automatic only while the merge is still the tip; otherwise escalate. Post-merge obligation, encoded in `machine.json` and procedure step 6.
- **H4 — SCOPE CREEP.** "The scorecard said so" is not a blank check. Every auto-merge PR states its `lane` and `owner_seat`; a merge outside the author's lane requires the owning seat's acknowledgment on #1354 first (`owning_seat_ack_comment_id`). Enforced by the predicate.
- **H5 — LOST VISIBILITY.** Every auto-merge is reported in the morning re-score message with its scorecard receipt linked. Full visibility, zero clicks required. Post-merge obligation on the merging seat.

## 8. Amendment path

Amendments to this law are authority-model changes: they require the Human Director's explicit decision, encoded as a new version (never an edit-in-place of the ratified text). The predicate's `MAX_EVIDENCE_AGE_SECONDS` and protected-path list are tunable only through the same path — a seat may not widen its own gate.
