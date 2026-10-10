# THE NAYA ACTIVATION PROTOCOL v1
## The enforcement layer of the Operating Law

**Authorized:** Shawn Vibert, 2026-10-09 ~18:17 PDT
**Status:** CANDIDATE — requires independent scorecard review before ratification
**Enforces:** The Operating Law of Naya Net v1 (`BRAIN/01-GOVERNANCE/0008-OPERATING-LAW-V1.md`)
**Summary:** The Operating Law says how a Naya must behave; this protocol makes that behavior unavoidable through five layers — boot injection (the seat has the law), activation ritual (the seat engaged with it), law as code (machines enforce what's encodable), compliance scoring (reviewers measure and teach the rest), and path of least resistance (templates make the law the default). It defines the 90% lock-in metric: the share of reviewed work that is both lawful and good.

---

> *"If we can get the Nayas locked in where 90% of the time they're producing value — understanding, reducing rework, not drifting, not making mistakes — that's huge."*
> — Shawn Vibert

---

## 1. Why this exists

The Operating Law says how a Naya must behave. This protocol makes that behavior unavoidable.

Shawn's diagnosis: right now the percentage of AI time wasted — on rework, drift, hallucinated results that need redoing, 200-round iterations that should have been 3 — is sad. His estimate: companies lose hundreds of billions of dollars a day to AI waste. (Direction undeniable; the exact figure is unverified — but even a fraction of it is staggering.)

The Activation Protocol is the answer inside Naya Net: **a machine that makes 10/10 automatic instead of heroic.** Not by asking seats to try harder — by building five layers where following the law is easier than breaking it, and breaking it is caught by machinery.

## 2. The five layers

No single layer reaches 100%. Layered, they compound toward it.

| Layer | Name | What it guarantees | Mechanism |
|-------|------|-------------------|-----------|
| 1 | **Boot injection** (availability) | The seat HAS the law | Canonical boot sequence loads the Operating Law into every seat's context at session start. Fail-closed: boot without the law is not boot. |
| 2 | **Activation ritual** (engagement gate) | The seat ENGAGED with the law | Before any work, the seat produces an activation receipt in its own words: mission objective, 3 most relevant domains + why THIS task, proof standard. No receipt → no dispatch. Anti-parroting validator + reviewer judgment. |
| 3 | **Law as code** (machine enforcement) | The encodable laws ENFORCE THEMSELVES | Every Operating Law provision that can be an executable check IS one. Fail-closed: violation blocks progress. 59 laws audited: 6 encoded, 21 encoded-weak (flagged for hardening), 32 judgment-only (correctly left unmachined). |
| 4 | **Compliance scoring** (accountability) | Law adherence is MEASURED and TAUGHT | Every independent review scores 6 law-adherence dimensions alongside quality. Misses get corrected with the why — the teaching loop that internalizes the law. Produces the lock-in metric. |
| 5 | **Path of least resistance** (environment) | The law is the DEFAULT | Templates carry the law as fill-in fields. Following it is easier than breaking it. PR template, dispatch-brief addendum, receipt schemas. |

### How the layers compose

**Layer 1 → Layer 2:** Boot guarantees the seat *has* the law (availability). The ritual guarantees the seat *engaged* with it. "I read the documents" is not activation — the receipt must be in the seat's own words, bound to the exact assignment.

**Layer 2 → Layer 3:** The ritual covers judgment (which domains matter for this task, what proof looks like). The machine checks cover pattern (receipt present and non-parroted, claims cited, words plain, CI green). Judgment and machinery each do what the other cannot.

**Layer 3 → Layer 4:** The machine catches what it can; the reviewer catches the rest — and scores both. The 32 judgment-only laws (taste, intent-reading, honesty, the Mantra itself) live here: they cannot be linted, so they are *reviewed*, with the correction-with-the-why as the teaching instrument.

**Layer 4 → Layer 5:** Every correction reveals a template gap. When reviewers keep correcting the same miss, the fix goes into the template — the law moves from something enforced *on* seats to something built *into* the environment.

**The whole:** availability → engagement → machine → accountability → environment. Each layer catches what the previous one misses.

## 3. The lock-in metric — measuring the 90%

Shawn's target: **90% of Naya time producing value.** This is now a computable number, not a vibe.

```
lock_in_pct = 100 × (value-producing units in last 30) ÷ 30
```

- **A work unit** = one reviewed work product with BOTH a compliance scorecard (Layer 4) and a quality score (the independent reviewer's quality score on the same work product, 0–10) — filled by a reviewer who is not the doer.
- **Value-producing** = compliance ≥ 8.0 AND quality ≥ 8.0. No rounding up: 7.95 is not 8.0.
- **Window** = the last 30 work units (work-based, not time-based — it cannot be gamed by going quiet). Fewer than 30 total units = a "low-sample" reading, labeled as such.
- **Published** to #1354 in the morning re-score message AND appended to `BRAIN/01-GOVERNANCE/compliance-lock-in-ledger.jsonl`. The ledger is the recomputable source of truth; if a posted number disagrees with the ledger, the ledger wins.
- **Anti-gaming:** reviewer ≠ doer. Scores move only on evidence. Scorecards missing their quality twin do not enter the ledger.

When lock_in_pct ≥ 90 sustained, the team is locked in. When it drops, the compliance scorecards say exactly which dimension is bleeding — and the correction-with-the-why says how to fix it.

## 4. Component map

### Layer 1 — Boot injection
- `activation-protocol/boot-sequence-v1.md` — the canonical 6-phase boot sequence (identity → mission → Operating Law → role doctrine → assignment → load verification). The Operating Law is a mandatory fail-closed load.
- `0009-boot-manifest-v1.machine.json` — machine-readable load manifest: 19 ordered entries, 13 required.
- Composes with (does not replace) the existing `NAYA-ACTIVATION/` cold-start material.

### Layer 2 — Activation ritual
- `activation-protocol/activation-ritual-v1.md` — the ritual: when it runs (every session start, every dispatch, every material assignment change), the 6 steps, the gate rule (no receipt → no work; 3 bounces → seat re-boots), the 3-layer anti-parroting design.
- `0009-activation-receipt-schema.json` — the receipt schema (`naya.activation.engagement_receipt.v1`): seat, timestamp, assignment_ref, mission in own words, exactly 3 distinct Operating Law domains with task-specific reasoning, proof standard. One receipt per assignment; not transferable.
- `tools/activation/validate_receipt.py` — the mechanical gate: rejects missing sections, fewer than 3 distinct domains, canned mission strings, zero keyword overlap with the assignment (parroting), and receipts replayed onto a different assignment (`--expect-assignment-ref`).

### Layer 3 — Law as code
- `activation-protocol/law-as-code-audit-v1.md` — all 59 Operating Law provisions audited: **6 ENCODED** (fail-closed, running), **21 ENCODED-WEAK** (checks exist but bypassable — each flagged with the hardening needed), **32 JUDGMENT-ONLY** (each with the one-line why it cannot be machined without inventing the law).
- `tools/activation/check_activation_receipt.py` — Law 4.1: artifact directories must contain a valid activation receipt.
- `tools/activation/check_evidence_claims.py` — Laws 4.6/8.3: quantified and state claims in reports must carry citations.
- `tools/activation/check_plain_words.py` — Law 2.1: plain-meaning lead, no bare PR-number references, jargon glossed.
- `tools/activation/run_activation_checks.py` — single runner over all checks (existing + new), per-check PASS/FAIL/SKIP, fail-closed exit code, `--strict` for CI.
- **Ruthless findings shipped in the audit:** `tools/auto_merge_gate.py` is the strongest predicate in the repo and nothing in CI invokes it (highest-leverage wiring task); Law 8.5 cites `tools/verify_gitdata_merge_tree.py`, which does not exist (the law cites a check that was never built — now flagged, not silently dropped).

### Layer 4 — Compliance scoring
- `activation-protocol/compliance-scorecard-v1.md` — 6 dimensions (ritual completed / calculator used / work shown / plain words / evidence attached / right domains applied), each with what-10-looks-like, what-0-looks-like, mandatory evidence, and the correction-with-the-why teaching loop below 7.
- `0009-compliance-scorecard-template.machine.json` — machine-readable twin (`naya.compliance.scorecard.v1`).
- **Layer 2 ↔ D6 reconciliation (closed at assembly):** the ritual's `relevant_domains` enum and the scorecard's D6 both reference the same 8 Operating Law domains. No wording amendment needed — verified, not assumed.

### Layer 5 — Path of least resistance
- `activation-protocol/template-audit-v1.md` — 6-template audit. Core finding: the biggest failure is *absence*, not bad templates — the law was prose in docs with no fill-in fields where work happens.
- `.github/pull_request_template.md` — NEW: plain-words summary + calculator + evidence + scorecard refs + delivery gate as required sections. (No PR template existed; this is purely additive.)
- `activation-protocol/fixed-dispatch-brief-addendum.md` — adoptable LEARN-marked sections for the dispatch brief (calculator fields, quality gate, evidence table). The brief file is LEARN-managed — the addendum is designed for LEARN adoption, not hand-editing.
- Flagged (not built — correct lane ownership): the Design Blocks directory the brief references does not exist yet (PR #1967 draft); the session-level activation receipt in `NAYA-ACTIVATION/` is a hollow skeleton awaiting Layer 2 hardening.

## 5. What remains judgment-only — and why that is correct

32 of 59 provisions cannot be machined: the Mantra, the Judgment Rule, the Honesty Covenant, taste, intent-reading, "the most intelligent thing." Encoding them would be theater — and the Evidence Law forbids theater. These live in Layers 2 and 4: the ritual forces the seat to *reason* about them in its own words, and the reviewer *scores* whether the reasoning governed the work. The machine handles pattern; humans handle judgment. That division is the design, not a gap.

## 6. Open follow-ups (not blockers)

1. **Wire `auto_merge_gate.py` into CI** — the single highest-leverage enforcement task. One CI step; eight ENCODED-WEAK laws become ENCODED.
2. **Build `tools/verify_gitdata_merge_tree.py`** — Law 8.5 cites it; it does not exist. (Or amend the law to cite the real mechanism.)
3. **Wire the 4 new checks into CI** via `run_activation_checks.py --strict`.
4. **LEARN adoption** of the dispatch-brief addendum.
5. **Design Blocks directory** (PR #1967) — unblocks the brief's block references.
6. **First 30 scorecards** — the lock-in metric needs its first window before the 90% target is measurable.

## 7. Amendment

This protocol is CANDIDATE until an independent scorecard rates it 9.0+. Amendments follow the same path: propose, independent review, 9.0+ to ratify. Shawn alone amends the supreme law; this protocol is its enforcement arm, not its replacement.

---

*Built 2026-10-09 by Naya 4 (assembly) with three parallel builder lanes. Every component self-scored 8.5+ before assembly. The machine that makes 10/10 automatic instead of heroic — built like the home depends on it.*
