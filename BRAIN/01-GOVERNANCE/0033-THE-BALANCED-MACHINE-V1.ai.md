# THE BALANCED MACHINE V1 — AI Language

*Exact specification for Naya seats running THE BALANCED MACHINE. The AI-language form of 0033 — canonical prose: `0033-THE-BALANCED-MACHINE-V1.human.md` (the prose governs); machine form: `0033-the-balanced-machine-v1.machine.json`. Status: RATIFIED CORE (Shawn, 2026-10-21 ~21:50Z); FORMALLY RATIFIED (Shawn Vibert, 2026-10-22 ~00:29Z — §10) — specify, do not redesign. Where a number below is a specification choice rather than Shawn's words, it is marked `[SPECIFIED — confirm at ratification]`. Sources: the counted gate audit of 2026-10-21 (`hidden_files/gate-redesign/`) and the design's §0 evidence grounding. Companion law: 0034 (House-Fire).*

*Status: RATIFIED CORE (Shawn, 2026-10-21 ~21:50Z) — specify, do not redesign. This file is the builder's spec. Companion forms: `DESIGN.human.md`, `design.machine.json` — same truth, three tongues. Where a number below is a specification choice rather than Shawn's words, it is marked `[SPECIFIED — confirm at ratification]`.*

## 0. Evidence grounding

`hidden_files/gate-redesign/tier-audit.md` and `gate-mechanics.md` were **absent** at authoring time (checked 2026-10-21 ~22:02Z). Counts below are **derived by the author from the audit lane's raw pulls** (`hidden_files/gate-redesign/raw/classification.json`, pulled 2026-10-21 ~21:51Z; per-PR check-runs/files/detail JSON alongside it). Re-derive before citing elsewhere.

**Counted facts (50 open PRs classified, 2026-10-21 ~21:51Z):**

| | count |
|---|---|
| Open PRs classified | 50 |
| Tier A / B / C (path-based, audit-lane rules) | 18 / 18 / 14 |
| Blocked solely on PAPERWORK (the two paperwork gates) | **22 (44.0% of all open; 48.9% of the 45 non-conflict PRs)** |
| Blocked on CONTENT (own-diff reds) | 16 |
| Blocked on CONFLICT (mergeable_state=dirty) | 5 |
| Blocked HUMAN (human-gated) | 5 |
| OTHER | 2 |
| PRs with `Team review + scorecard receipt` red at head | 40 of 50 |
| PRs with `Receipt gate` red at head | 17 of 50 |
| Tier C blocked on PAPERWORK | **10 of 14** (Tier C content blocks: 3; HUMAN: 1) |
| Tier B blocked on PAPERWORK | 9 of 18 |

**Verified incidents this design answers (all 2026-10-21):**

1. **639-note deletion** — direct push `2731e914` deleted 636 files on an unverified quoted word; no PR, no gate ever saw it. Gates guarded the PR road only; the dangerous road had none.
2. **Matcher form-failure class** — scorecards existed but were machine-invisible (header case, heading extra words, stale head pins); lanes burned hours re-posting/re-pinning/body-PATCHing to retrigger gate runs.
3. **PR #2552 twin receipt-gate runs** — two `Receipt gate` runs at one head 3s apart (`115680847369` success @04:27:53Z, `115680862874` failure @04:27:56Z); latest-per-name = FAILURE with no output text. A gate that can contradict itself at one head is a measurement defect.
4. **Hub wall at 1 card** — hub-sync watcher died silently on VM replacement; deploy was coupled to note landings (`sync-smart-notes.py::update_hub_and_deploy`), so canonical Hub fixes stayed invisible until a note landed.

## 1. Value law (normative)

`value(change) = quality × completion`. Undone = 0. An 8.0 that merges and works outranks a 9.5 that never lands. Gates **protect**; a gate whose net effect is to stop flow is a defect (cf. Shawn's security law: max protection, zero flow interruption). Every mechanism below is judged by the balance gauge (§6), not by intuition.

## 2. Merge tiers

Classification is by **paths touched** (PR diff vs merge-base). Highest tier wins. Automated by the tier tagger (§7 step 2); a different seat may override with a stated reason in a PR comment (logged by the tagger).

### Tier A — full bar
**Paths (any one ⇒ A):** `BRAIN/01-GOVERNANCE/**`; `AGENTS.md`, `SOUL.md`, protocol/doctrine files; `.github/workflows/**`; any path matching `*auth*`, `*security*`, `*rls*`, credentials handling; production deploy paths (workers, deploy scripts, `HUB/` deploy sources); gate machinery (`tools/check_merge_consensus.py`, gate tools/workflows, `tools/activation_gate.py`); sync/engine code (`tools/sync-smart-notes.py`, hub-sync); **any PR deleting > 10 files** regardless of paths.
**Bar (unchanged from current law):** different-seat scorecard **≥ 9.5/10** at the exact head + BOTH existing gates (`Team review + scorecard receipt`, `Receipt gate (evidence or it didn't happen)`) green + all content checks green + post-merge faithfulness proof.
**Bar note:** mass deletions additionally require the L607 rule — source-verified human instruction + standing-law check — before the PR is even opened.

### Tier B — one unified gate
**Paths:** everything not A and not C.
**Bar:** the **Unified Paperwork Gate** (§3) green + all content checks green. Scorecard floor: **≥ 8.0/10** `[FORMALLY RATIFIED — Shawn Vibert, 2026-10-22 ~00:29Z; §10]` — specified from Shawn's 2026-10-21 framing ("an 8 out of 10 that goes through and works is better than a 9.5 that doesn't go through"); the scorecard must additionally attest, in its body, that the change was exercised/verified (tests run or behavior observed), not merely read. No unresolved blocking finding may stand at any score.

### Tier C — machine validation only, no PR surface
**Classes:** Smart Note filings (`BRAIN/05-MEMORY/SMART-NOTES/**`, `SUPER-NOTES/**` filings); index/registry regenerations (`BRAIN/NAYAPOWER-BRAIN-INDEX.json`, `BRAIN/REAL-TREE.*`, `.naya/memory/smart-notes/index.json` and their generators' outputs); pure data files.
**Route:** the **note door** (§5.3) — direct landings by the landing machinery. Tier C has **no PR surface**: branch-protection Required checks bind PRs, and Tier C does not travel by PR. If a Tier C PR is opened anyway, the tagger comments the door route and the PR is closed `superseded-by-the-door` (specimen: **PR #2854**, 625 commits / 1,667 files — disposition per ratified core: close as superseded-by-the-door, content lands via the door). Note: the audit-lane path rules classified #2854 Tier A (it accumulated production/protocol paths over 625 commits); disposition is by **substance** (a note filing), per the ratified core — the tagger must therefore treat long-lived note branches as C-substance regardless of accreted paths, and the door policy (§7 step 3) prevents recurrence.
**Validation (all machine, all pre-landing):** schema/shape check of the note's nine sections; **SN-collision scan** covering (1) board claims, (2) open PR heads, (3) repo commit graph, (4) date partitions — live scan at claim time, timestamp announced; syntax/parse check of every generated file; index regeneration from the landed tree (never hand-edited indexes).

## 3. The Unified Paperwork Gate (Tier B)

One check, replacing BOTH `Team review + scorecard receipt` and `Receipt gate (evidence or it didn't happen)` **for Tier B PRs** (Tier A keeps both, unchanged). Name: `Paperwork gate (scorecard + evidence)`.

**Predicates — ALL must hold:**
1. **Scorecard present & parseable:** a comment on the PR matching the gate-format scorecard grammar (header `[NAYA <seat> · REVIEW] APPROVED` or matcher-equivalent; `## SCORECARD` block with `head:`, `seat:`, `score:`, `verdict:` lines) — reuse `tools/check_merge_consensus.py`'s `_looks_like_scorecard` predicate; do not write a second matcher (no duplicate mechanisms).
2. **Different seat:** scorecard `seat:` ≠ PR author's declared `Seat:` (case-insensitive; the capitalization self-approval hole is already cured in the current matcher — inherit, don't re-implement).
3. **Score ≥ 8.0** (Tier B floor, §2) with the verification attestation present.
4. **Freshness by diff-hash (§4):** the scorecard's pinned `diff:` hash equals the PR's current diff hash. Exact-head pinning is NOT required for Tier B.
5. **Evidence resolves:** every link/handle in the PR body's `## Evidence` section resolves (HTTP 200 for URLs; API-resolvable for comment/commit/check handles). Bare backticked identifiers fail (existing receipt-gate grammar, inherited).

**Determinism rule (answers incident 3):** the gate evaluates **once per (head, trigger-event)**, writes its full predicate-by-predicate result as a PR comment, and its check-run output text is that same result — a later duplicate run at the same head MUST reproduce the identical verdict from the same inputs or the gate itself files a defect note. Latest-per-name ambiguity is resolved by the gate publishing exactly one check-run per event batch (existing re-run machinery dedupes by event id).

**Self-explaining reds (§3.1) apply to this gate and, by step-1 scope, to both Tier A gates' failure outputs.**

### 3.1 Self-explaining reds — output contract
Every failing paperwork check MUST emit, in the check-run output AND a PR comment, one line per failed predicate in this exact form:

```
MISSING: <what> — CURE: <the single action that fixes it> (owner: <seat/lane>)
```

Examples: `MISSING: scorecard at current diff — CURE: post gate-format scorecard pinning diff a1b2c3… (owner: any seat ≠ author)`. A red without a CURE line is a gate defect, filed against the gate's owners. Content checks (test suites etc.) are out of scope for the contract's *form* but must link their failing output.

## 4. Scorecard freshness — diff-hash pinning

**Rule:** a scorecard stales **only when the PR's diff changes materially** — never on head movement alone (rebases onto a moved tip, empty commits, base updates that don't touch the PR's files).

**Mechanics:**
1. `diff_hash(PR) = sha256(concat over sorted changed-file list of (path + "\0" + blob_sha_at_head(path)))`, computed against the PR's merge-base with main. (Blob SHAs from the git tree at head — the same bytes the faithfulness proof already compares.)
2. A Tier B scorecard pins `diff: <diff_hash>` (the `head:` line remains, informational). The unified gate recomputes `diff_hash` at evaluation time; **equal ⇒ fresh**, regardless of head SHA.
3. If the diff changed, any different seat may **re-pin by addendum**: a comment naming the new diff hash + one line confirming the delta was read. The gate accepts an addendum re-pin without a full new scorecard **iff** the scorecard's original seat posts it or a second different seat co-signs in the same comment thread. (Prevents both staleness theatre and silent scope creep.)
4. Tier A is unchanged: exact-head pinning, full re-score on any head move. (Blast radius justifies the cost; Tier A is ~1 in 10 PRs.)

## 5. Flows

### 5.1 Hub flow — deploy decoupled from note landings
**Root defect (verified 2026-10-21):** deploy rides `sync-smart-notes.py::update_hub_and_deploy` — Hub-source fixes land on main but stay invisible until a note landing triggers the combined path; and the sync watcher's death (VM replacement) was silent for hours (wall fell to 1 card).
**Spec:**
- **Deploy is its own act.** A dedicated deploy path (workflow or lane script) triggers on merges to main that change Hub source paths (`HUB/**` and the canonical Hub source set) — and on nothing else. Note landings never trigger, gate, or carry a deploy.
- **Deploy pipeline:** syntax gate (JS parse / HTML validation over changed Hub files) → deploy → smoke check (GET `https://nayanet.live/` = 200 and the served feed array parses) → receipt on the board with the deployed commit SHA. Smoke failure ⇒ **automatic rollback** to the previous deployed commit + defect note.
- **Sync stays a standing watcher** (20s git-protocol poll, additive-only — the 2026-10-21 rebuilt design), with a **liveness alarm**: the watcher writes a heartbeat (timestamped status file + row in its status surface) every cycle; if no successful cycle completes for **10 minutes** (30 missed cycles), the watcher — or an external checker on the director-pass cadence — posts an alarm to the live board naming the stall. Silence is the failure mode being abolished.
- Feed freshness is a balance-gauge metric (§6).

### 5.2 Supabase flow — fitted per table, apply is Shawn's tap (issue #2823)
Per Shawn's security law (2026-10-21, direct): maximum protection with **zero interruption** to any working flow; a fix that blocks flow is rolled back and reported flow-blocked with the exact conflict.
**Prep procedure (agent work, no apply):**
1. **Inventory:** re-derive the table list from the live schema at prep time (known set at design time: `hub_smart_notes`, `hub_smart_notes_archive`, Smart Mail tables, Spaces tables, Lists tables, build-queue tables — re-derive, do not trust this list).
2. **Per table, map real working paths first:** every reader/writer (Hub front-end, sync, Smart Mail, Spaces, Lists, build queue), its auth context (anon key, service role, user JWT), and the exact operations exercised live.
3. **Shape owner-scoped RLS policies** preserving every mapped path — deny-by-default ONLY where no working path exists (the blunt Phase-3 deny-all is NOT approved).
4. **Stage the policy SQL as versioned files** (prior policy kept alongside for rollback), one file per table.
**Apply procedure (Shawn's tap, per table batch):** apply ONE table → run the live-flow verification for every mapped path of that table → any regression ⇒ immediate rollback of that table + report flow-blocked with the exact conflict → proceed to the next table only on a clean pass. No table's apply is bundled with another's.

### 5.3 Note flow — the door, end to end
`author → validate → land → sync → VERIFIED_LIVE`
1. **Author:** nine-section Smart Note, filed by topic path, named by full IB id.
2. **Validate:** Tier C machine validation (§2): schema, live SN-collision scan (four-surface), syntax.
3. **Land:** direct landing on main by the landing machinery (the only door). No PR.
4. **Sync:** the standing watcher (§5.1) picks the landing up (observed: 25s on the 2026-10-21 live-fire proof).
5. **VERIFIED_LIVE — all four, or it is not done:** (a) file present in main's tree at the claimed path; (b) the note's own entry present in the baked feed array; (c) its page `https://nayanet.live/s/sn####` returns 200 — probe **padded AND unpadded** id forms, **GET not HEAD** (L605); (d) its share image returns 200 (GET). Any absence verdict names the forms probed.

## 6. Balance gauge — metrics, bands, adjustment rule

Computed weekly from counted data (check-runs API + PR records + post-merge defect log); published to the board; **no band is judged on a single week unless a safety metric trips**.

| Metric | Definition (derivation) | Target band | Baseline 2026-10-21 |
|---|---|---|---|
| Paperwork-block rate | open PRs whose ONLY blockers are paperwork gates ÷ all open PRs | **< 10%** | **44.0%** (22/50) |
| Time-to-merge, Tier A | median, PR open → merge | ≤ 5 days `[SPECIFIED]` | unmeasured — first read establishes |
| Time-to-merge, Tier B | median, PR open → merge | ≤ 48 h `[SPECIFIED]` | unmeasured |
| Tier C land time | median, note authored → VERIFIED_LIVE | ≤ 15 min | ~25 s sync pickup (single proof) |
| Post-merge escape rate | defects found ≤ 7 days after merge, attributed to the PR by the finder, ÷ merges in period | **≤ 2%** and never rising 2 reads running | unmeasured |
| Feed freshness | age of newest feed entry vs newest note landing on main | ≤ 5 min lag | broken (wall=1 card incident) |
| Deploy freshness | merges touching Hub source not yet deployed | 0 beyond 30 min | unmeasured |

**Adjustment rule (mechanical):** compute `blocks : escapes` pressure each read.
- **Loosen** when paperwork-block rate > 10% for **2 consecutive reads** AND escape rate ≤ 2%: apply ONE loosening lever per cycle, smallest first: (i) extend addendum re-pin acceptance, (ii) drop a duplicated predicate, (iii) lower the Tier B floor by 0.5 (never below 7.5).
- **Tighten** when escape rate > 2% OR rises on **2 consecutive reads**: apply ONE tightening lever: (i) raise the Tier B floor by 0.5 (never above 9.5), (ii) promote the offending path class to Tier A, (iii) add the escaped defect's class as a content check.
- Every adjustment is a PR through the then-current protocol + a board receipt naming the gauge readings that forced it. The gauge tunes the bar; it never silently edits it.

## 7. Implementation sequence (ordered; each step lands before the next starts)

| # | Step | Owner lane | Gate to land |
|---|---|---|---|
| 1 | **Unified Paperwork Gate build** (§3 + §3.1 + §4 predicates; Tier A gates gain the §3.1 output contract; determinism rule) | Gate machinery owners (law/VERIFY-adjacent seat builds; different seat scores) | **Current full protocol** (Tier A bar — this is Tier A work by definition) |
| 2 | **Tier tagger** — path-based classifier on PR open/synchronize; posts tier + rule citation as a comment, applies label; override by different seat with reason | Build lane | Tier A protocol (it classifies Tier A) |
| 3 | **#2854 disposition + door-only note policy** — close #2854 `superseded-by-the-door` with the landing plan cited; its notes land via §5.3; policy note filed so note PRs are closed on sight by the tagger | Main seat + sync lane | n/a (close + landings, each landing §5.3-verified) |
| 4 | **Hub deploy decoupling** (§5.1: standalone deploy path + smoke + rollback; sync heartbeat + liveness alarm; remove deploy from `sync-smart-notes.py`'s combined path) | Hub/sync lane (Clarity) + different-seat verifier | Tier A protocol (sync/engine code) |
| 5 | **Supabase fitting** (§5.2 prep: inventory, path maps, per-table policy files staged) | Nitro lane (per current assignment) | Prep lands as Tier B docs/code; **APPLY = Shawn's tap per table (issue #2823)** |
| 6 | **Balance-gauge instrumentation** (§6 derivations automated; first weekly read published with baselines replacing the `[SPECIFIED]` placeholders where data exists) | Director/VERIFY lane | Tier B (unified gate, once step 1 has landed) |
| 7 | **FINAL — Ruleset Required-checks change** (§8) | **Shawn (governor click)** | Human-only: repo settings |

## 8. The governor click — exact before/after (step 7)

Ruleset 23853581 / branch protection on `main`. **Before** (Required for every PR, tier-blind):

- `Team review + scorecard receipt` — Required
- `Receipt gate (evidence or it didn't happen)` — Required
- (content checks as currently configured)

**After:**

- Tier A PRs: both checks above remain Required (the unified gate does not apply; tagger label `tier:A` scopes the ruleset where the platform supports label/path conditions — **fallback if scoping is unavailable:** both checks remain Required repo-wide, and the unified gate is implemented as a mode *inside* the Team-review check that auto-passes Tier B PRs on its own predicates and Tier C PRs on the door citation; the check NAMES stay stable so no Required entry dangles. Builders: verify platform scoping in step 1 and record which branch of this fallback is live.)
- Tier B PRs: `Paperwork gate (scorecard + evidence)` — Required (replaces both above for Tier B).
- Tier C: no PR — nothing Required (door landings are post-verified per §5.3, not PR-gated).
- Content checks: unchanged.

Nothing else in the ruleset changes in this click. If the fallback branch is the live one, the click is exactly: **add `Paperwork gate (scorecard + evidence)` to Required; remove nothing** — the old pair stays Required but self-satisfies via the unified mode for Tier B. The step-1 build MUST record which branch applies before step 7 is presented to Shawn.

## 9. Flags for the ratifying seat (specification choices, not core changes)

1. **Tier B score floor 8.0** — the ratified core says "good-and-verified bar" without a number; 8.0 is specified from Shawn's own 2026-10-21 framing. If the ratifying seat wants a different number, this is the single value to change (§2, §3 predicate 3, machine JSON `tiers.B.scorecard_min`). **RESOLVED 2026-10-22 ~00:29Z: formally ratified at 8.0 (§10).**
2. **Ruleset scoping fallback (§8)** — whether per-tier Required checks can be scoped directly depends on platform ruleset conditions; the design is workable either way via the fallback, but step 1 must determine which branch is real before step 7.
3. **Time-to-merge bands** in §6 are `[SPECIFIED]` starting values; the first two weekly reads should re-derive them from observed medians rather than treating them as law.

## 10. Formal ratification

**Ratifier:** Shawn Vibert. **Date:** 2026-10-22 ~00:29Z. **Source:** chat directive — Shawn's word approving all eight gates as presented (GT-067): "my word — execute, get them all done, full permission". **Scope:** the Balanced Machine as designed in this set — the three tiers (§2: A full bar, B one unified paperwork gate, C machine validation via the note door), the Unified Paperwork Gate (§3), and the balance gauge (§6). **Tier B floor:** `tiers.B.scorecard_min` = **8.0 CONFIRMED** — flag §9.1 is resolved; the `[SPECIFIED — confirm at ratification]` mark on the §2 floor is superseded by this section. The 2026-10-21 ~21:50Z core ratification and the 2026-10-21 ~22:34Z governor click (`governor_click_executed` in the machine tongue) stand as recorded; this section adds the formal ratification that was pending over the specified numbers. Machine record: `formal_ratification` object in `0033-the-balanced-machine-v1.machine.json`.
