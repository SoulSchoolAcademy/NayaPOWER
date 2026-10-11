# Intelligent Blocks — Schema v1.0

An **Intelligent Block (IB)** is the atomic unit of learning in NayaPOWER.
One block = one distilled principle, with its source, its proof, when it
applies, how verified it is, and where it is heading (text → briefing → code).

Blocks live in `intelligence/blocks/` as one JSON file per block:
`IB-0001.json`, `IB-0002.json`, … IDs are sequential, never reused.

## Fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `id` | string | yes | `IB-NNNN`, sequential, zero-padded to 4 digits |
| `schema_version` | string | yes | `"1.0"` |
| `title` | string | yes | Short human name, e.g. `"Law One — Divine Oneness"` |
| `principle` | string | yes | **One sentence, plain words, child-understandable.** If it doesn't fit in one sentence, it's not distilled enough. |
| `source` | object | yes | `who` (who said/taught it), `when` (date), `context` (what was happening) |
| `evidence` | array | yes | What proves it's true. Receipts, not claims. Each item: `kind` (`receipt`/`observation`/`code`/`test`/`direct-word`), `ref`, `note`. May be empty for brand-new blocks (`[]`), but empty evidence caps status at UNVERIFIED. |
| `applicability` | object | yes | `topics` (array of lowercase tags), `situations` (when it applies), `decisions` (what decisions it governs) |
| `verification_status` | string | yes | One of the four states below |
| `status_history` | array | yes | Every status change: `status`, `at` (ISO date), `note`. Starts with the creation entry. |
| `graduation` | object | yes | `stage` (`text`/`briefing`/`code-gate`), `next_step` (what moves it up), `enforced_by` (file/code ref, or null) |
| `supersedes` | string/null | yes | ID of the block this replaces, or null |
| `superseded_by` | string/null | yes | ID of the block replacing this, or null |
| `created_at` | string | yes | ISO-8601 UTC |
| `updated_at` | string | yes | ISO-8601 UTC, bumped on every change |

## Verification statuses (in order)

1. **`UNVERIFIED`** — captured but not yet used. New blocks start here unless
   Shawn's direct word verifies them on capture (Verification Law).
2. **`APPLIED`** — the block is injected at decision time (e.g. in the agent
   briefing) and agents act on it.
3. **`BEHAVIOR-CHANGE-PROVEN`** — measured evidence that agents behaved
   differently because of this block (receipts: merges, scorecards, outcomes).
4. **`COMPOUNDED`** — the block has survived a full cold-start cycle: a new
   agent with only the brain performs as well as an experienced one on tasks
   this block governs.

A block moves up only with evidence. A block never moves down except by
supersession (`superseded_by`).

## Graduation stages (in order)

1. **`text`** — the block exists as a document. Weakest: must be remembered.
2. **`briefing`** — the principle is injected into every agent's briefing at
   wake. Strong: present at decision time.
3. **`code-gate`** — the principle is enforced by code (a gate, a check, a
   test). Strongest: impossible to forget.

`graduation.next_step` always names the concrete next move. `enforced_by`
names the file or code that enforces it, or null if not yet enforced.

## Rules

- IDs are never reused. Deleted blocks are forbidden — supersede instead.
- `principle` is one sentence. No jargon. A child should get the wisdom.
- Evidence is receipts, not claims. "Shawn said it" is `direct-word` evidence.
- `REGISTRY.json` is generated (`ib reindex`), never hand-edited.
- Validate with `ib validate` or `pytest tests/test_intelligent_blocks.py`.
