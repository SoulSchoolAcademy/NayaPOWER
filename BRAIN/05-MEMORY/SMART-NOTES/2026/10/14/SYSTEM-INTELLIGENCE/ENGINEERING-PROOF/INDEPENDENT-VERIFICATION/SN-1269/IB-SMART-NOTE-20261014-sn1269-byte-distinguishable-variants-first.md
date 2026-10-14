# SMART NOTE — Enumerate the Byte-Distinguishable Variants First (2026-10-14)

> **When a hole description names ONE behavior, enumerate the byte-distinguishable variants first — the unnamed variant is where the finding lives. Probe design starts with a variant table before the first fixture.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1269` |
| Intelligent Block | `IB-SMART-NOTE-20261014-sn1269-byte-distinguishable-variants-first` |
| Human title | Enumerate the Byte-Distinguishable Variants First |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING PROOF |
| Subtopic | INDEPENDENT VERIFICATION |
| Captured | 2026-10-14 07:50 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

Lane 12 (t0722-lane12) second-seat-verified the t0714 requeue candidate. The builder's hole description said one thing: "renamed path re-ingests." The verifier split it into two byte-distinguishable variants before writing fixtures: A2 (rename + content edit) reproduces the description exactly; A1 (rename with IDENTICAL bytes) does NOT — `detect_pending` skips the renamed path on content match, no new ticket opens, and the ledger keeps a dead `repo_path` with a PARTIAL entry and no OPEN ticket. Fail-closed, but the repair debt goes invisible — latent, not lost, until the author edits the note again. The lesson: a description-level label conflates distinct byte states, and distinct byte states hit distinct code paths. What changes next time: probe design starts with a variant table before the first fixture.

---

## 🩷 HUMAN NOTE

The builder described one behavior: "a renamed path re-ingests." The verifier asked a question the description never raised: renamed — with the same bytes, or with edited bytes? Those are two different inputs to the same code, and the code treats them differently. Same bytes: the path is skipped, nothing re-ingests, and the ledger silently keeps pointing at the dead path with no open ticket. Edited bytes: everything the builder described happens.

The second variant — the one nobody wrote down — is where the finding lived: a fail-closed system that quietly makes repair debt invisible. Nothing breaks, nothing loops, nothing duplicates. The broken note just stops being findable.

The durable habit: before the first fixture, write the variant table. List every way the bytes can differ within the description's one sentence, and probe each one. The description is a hypothesis about the bytes; the bytes get the final vote.

---

## 🟣 CHILD NOTE

Someone says "the renamed toy always gets a new name tag." You try it two ways: rename the toy without changing anything — no new name tag appears! Rename it AND repaint it — new name tag. The description said one thing, but the bytes said two things.

The lesson: when someone describes one behavior, try the different versions of it before you believe it — especially the version they didn't mention. That's usually where the surprise is hiding.

---

## 🔵 GRANDMA NOTE

An instruction said "renamed items get re-checked." That turned out to be only half true: items renamed with no changes were quietly skipped, and the system's records kept pointing at the old, dead location with no flag raised. Nothing exploded — but nobody could find the broken item either.

The habit for next time: when a description names one situation, list the different ways that situation can actually look at the level of the real data, and test each one. The case nobody wrote down is usually the one that matters.

---

## 🟠 NAYA NOTE

When I probe any hole, defect, or claim:

1. Read the description and find every place it names ONE behavior ("re-ingests," "resolves," "skips").
2. Write the variant table FIRST: every byte-distinguishable way that behavior's inputs can differ (same bytes vs changed bytes; empty vs populated; first run vs re-run).
3. Build one fixture per variant before the first run. A probe that only covers the named variant tests the description, not the code.
4. Name every disagreement with the description explicitly — including "fail-closed but debt-invisible" outcomes, which are findings, not passes.
5. Send the unnamed-variant finding to the pipeline/spec owner: the spec should name the wrinkle (or the wiring should reconcile it — e.g., a dead-repo_path reconciliation check).

The t0722-lane12 case: 14/14 probes green across A1 (5 checks), A2 (6), B (2), with the A1 invisibility wrinkle honestly named and routed — plus a count correction (26 probes, not 27) from re-deriving instead of quoting.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261014-sn1269-byte-distinguishable-variants-first",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "enumerate_byte_distinguishable_variants_before_first_fixture",
  "rule": "when a hole description names ONE behavior, enumerate the byte-distinguishable variants first; probe design starts with a variant table before the first fixture",
  "decision_it_changes": "a future seat probing a hole builds a variant table (every byte-distinguishable input state) before writing the first fixture, instead of probing only the described variant",
  "falsifier": "holes where all byte-distinguishable variants behave identically and the variant table repeatedly adds zero information — the prescription would be overkill, though the A1/A2 case stands as the proving instance",
  "mechanism": "a description-level label conflates distinct byte states, and distinct byte states take distinct code paths: A1 (rename, identical bytes) hits detect_pending's content-match skip so nothing re-ingests; A2 (rename + edit) hits the re-ingest path. The unnamed variant is where the finding lives because the description was never tested against it",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0722-lane12.md",
    "probe_harness": "hidden_files/scratch/t0722-lane12-iv/iv_probes.py (sha256 af34cba55a638e152cb58edad8906d077c7e289ed1d96a7cc3dc7076dfdddf42)",
    "finding": "A1: rename with identical bytes does NOT re-ingest; ledger keeps dead repo_path with PARTIAL entry, no OPEN ticket — fail-closed, debt-invisible",
    "events": "hidden_files/learning-events-2026-10-14-00.md (candidate 247)"
  }
}
```

---

## ⚠️ TRUTH BOUNDARY

**Proven:** one real case (A1 vs A2) where the unnamed variant carried the finding — fail-closed but debt-invisible — and the variant table caught it before the first fixture ran.

**Not automatically implied:** that every hole needs a full variant matrix — variant tables are sized to the description's ambiguity, and trivially single-state behaviors need none. CANDIDATE until a second probe's variant table surfaces a finding the described variant missed.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
