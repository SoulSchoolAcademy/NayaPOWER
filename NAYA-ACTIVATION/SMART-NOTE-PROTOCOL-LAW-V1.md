# Smart Note Protocol Law V1

**Status:** CANDIDATE — ratification is the Human Director's word. Until ratified: usable, never quoted as law.

**Purpose:** any Naya — including one that has never seen the Brain — reads this first and places everything exactly right, the first time. No invented paths. No guessed spots. No skipped verification.

**Companion:** `SMART-NOTE-OPERATING-CONTRACT-V1.md` (the *why* — the law of learning). This document is the *where* and the *how* — the mechanics.

---

## 1. What a Smart Note is

A Smart Note is **one authored JSON capture** — machine language first, carrying the human view and the AI view inside it. The JSON is the intelligence. Everything else (the readable page, the registry entry, the Hub card) is *generated* from it, never hand-written.

Schema: `naya.smart-note-capture.v2`. If your file does not declare this schema, it is not a Smart Note.

## 2. What a Smart Link is

A Smart Link is the human's proof that the work was done right. It has three forms, and you must know which one you are holding:

1. **Machine link** — the authored JSON capture, viewable at its branch path. Proves the machine capture exists, is conformant, and carries the ratified keys. Available at authoring time.
2. **Human link** — the readable preview, *generated from that JSON by the real pipeline renderer* (`tools/smart_note_v2.py:117`, `render`), sitting at the canonical Brain path (§4). Proves what the intelligence says. Available at authoring time. Proof IDs in it are marked placeholders — never real receipts.
3. **ACTIVE Smart Link** — the pipeline-generated canonical projection on `main`, after the Human Director merges and the four jobs run green. Proves the event happened, persisted, verified, and projected. This is the only link that attests pipeline proof.

A PR number is **never** the deliverable. Report the pair (machine link + human link), never the PR number.

## 3. What the Brain is

The Brain is the governed memory of the organism: `BRAIN/` in the NayaPOWER repo. Its purpose is that **nothing valuable is ever lost, and everything kept can be found, trusted, and built on** — by any Naya, including a cold successor with no conversation history. The Brain does not store raw chatter; it stores distilled intelligence with provenance, truth state, and receipts.

## 4. Where everything goes — exact locations

There are exactly three artifacts. Their locations are defined by code, not by convention. Code citations are to `tools/smart_note_v2.py` on `main`.

| # | Artifact | Exact location | Defined by |
|---|---|---|---|
| 1 | Authored capture (JSON) | `.naya/capture/SMART-NOTE-<yyyymmdd>-sn<nnn>-<slug>.json` | workflow trigger: push to `main` filtered to `.naya/capture/**` |
| 2 | Human projection (Markdown) | `BRAIN/05-MEMORY/SMART-NOTES/<yyyy>/<mm>/<dd>/<CATEGORY>/<TOPIC>/<SUBTOPIC>/<SN-NNN>/IB-<id>.md` | `:84` `projection_path`, `:7` root |
| 3 | Registry entry | `.naya/memory/smart-notes/index.json` | `:8` `REGISTRY`, `:187` `update_registry` |

**Worked example** (SN-031, captured 2026-10-04):

- Capture: `.naya/capture/SMART-NOTE-20261004-sn031-core-discipline-first-read.json`
- Projection: `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SMART-NOTE-NODE-OPERATING-FLOW/CORE-DISCIPLINE/SN-031/IB-<allocated>.md`
- The date in the path comes from the capture's `captured_at_utc` (`:84-89`). The category/topic/subtopic are the uppercased slugs from the capture's `projection` block (`:90-93`). The SN number is the capture's explicit `smart_note_id` (`:70-82`).

**Never invent a location.** A preview, a report, or a projection placed anywhere else is misfiled intelligence — the system cannot find it, and the failure is yours.

## 5. The exact process — twelve steps, in order

1. **Intent.** A human asks, or a seat recognizes durable value ("would this change a future decision?").
2. **Claim the number.** Check the live tree for the max `SN-NNN`, scan open Smart Note PRs, scan the live board. First-claim stands; the colliding lane renumbers. Announce the claim on the live board.
3. **Author ONE JSON capture.** Schema `naya.smart-note-capture.v2`. Explicit `smart_note_id`. Both ratified keys in `machine_view` (`raw_source_separate_from_distillation: true`, `automatic_truth_ceiling: "CANDIDATE"`). Write from your own embedded understanding — never parrot.
4. **Conformity-check the JSON** against the newest conformant capture before it leaves your machine (keys, ratified keys, no legacy keys, no empty views).
5. **Commit to your branch.** One authored file per PR. Byte-verify: the committed bytes must be identical to what you authored (sha256).
6. **Generate the human preview with the real renderer** (`:117` `render`), not by hand. Mark proof IDs as placeholders. Place it at the canonical Brain path from §4 — the exact path the pipeline will use.
7. **Verify both links resolve** (fetch them back; confirm bytes, parse the JSON, confirm the keys).
8. **Open the PR.** Body states: what it is, the SN claim, conformance, what it is not, and that merge is the Human Director's gate.
9. **Deliver the pair to the human:** machine link + human link. Never the PR number alone.
10. **Merge (Human Director only).** The pipeline runs: persist → verify → project → index.
11. **Return the ACTIVE Smart Link** from the canonical `main` path. Confirm it resolves.
12. **Cold exam.** A Naya that never saw the note must retrieve, comprehend, apply, and measurably improve from it. Until then: stored, not learned.

## 6. Verification checklist — run it every time

- [ ] JSON parses; schema is `naya.smart-note-capture.v2`
- [ ] `smart_note_id` explicit and unclaimed (tree + open PRs + live board)
- [ ] `machine_view.raw_source_separate_from_distillation is True`
- [ ] `machine_view.automatic_truth_ceiling == "CANDIDATE"`
- [ ] No legacy keys; no empty views
- [ ] Committed bytes == authored bytes (sha256)
- [ ] Preview generated by `:117` `render`, not hand-written
- [ ] Preview sits at the `:84` canonical path
- [ ] Machine link resolves; human link resolves
- [ ] PR body carries the claim, the conformance, and the merge gate
- [ ] Human received machine link + human link

## 7. Honesty laws

- **UNKNOWN ≠ PASS.** Never claim a step succeeded that you did not verify against live bytes.
- **Never fabricate receipts.** Preview proof IDs are marked placeholders, always.
- **CANDIDATE until earned.** New intelligence is `CANDIDATE`; promotion requires independent verification. Law is `CANDIDATE` until the Human Director ratifies.
- **History is immutable.** Correct by supersession with lineage, never by repainting.
- **No parroting.** Each seat authors from embedded understanding. The exam is cold application, not recitation.
- **Learning is a measured behavioral delta** or it is not learning.

## 8. Failure modes already observed — do not repeat

| Failure | Receipt | Rule |
|---|---|---|
| Preview placed at invented `.naya/preview/` instead of the `:84` canonical path | 2026-10-04, SN-031 | §4 — never invent a location |
| Reporting "PR #NNNN" as the human deliverable | 2026-10-04, SN-027/SN-031 | §2 — deliver the pair, never the PR number |
| Two PRs claiming one SN number | 2026-10-04, SN-025/SN-027 races | §5 step 2 — first-claim stands |
| Hand-written projection presented as pipeline output | — | §5 step 6 — the renderer generates, seats never author projections |
| Claiming learning from storage alone | standing | §7 — stored ≠ learned |

## 9. Activation order

This law is first-read, alongside `SMART-NOTE-OPERATING-CONTRACT-V1.md`: a new Naya reads the Contract (the *why*) and this Protocol (the *where* and *how*) before touching any intelligence. The North Star over both: **PROVE THAT SHE WORKS.**
