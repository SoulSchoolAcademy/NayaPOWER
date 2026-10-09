# Cold Retrieval — how a stranger reaches the verified-lesson diary

**For:** a cold Naya (or any successor agent) with no memory, no tribal
knowledge, and no private connector. **Reachability:** linked from the
`AGENTS.md` boot contract — discovery is part of the path, not a footnote.
**Scope:** READ-ONLY. This seam never writes to the store.

---

## 1. What you're retrieving

The canonical store keeps every durable lesson the system learned, each
with its level, status, provenance, and independent-verification record.
"Verified lesson" here means a row you may RELY ON when doing work:

- `level = 'E5_CAN_TEACH'` — the ladder level whose definition requires
  **independent verification** and demonstrated transfer
- `status = 'ACTIVE'` — live, not retired or superseded
- `provenance = 'TRIAL_EVIDENCE'` — produced by a governed trial
  (an `E5` row with `OBSERVATION` provenance is an operational note,
  not a verified law — the seam excludes it quietly: it never enters the
  output, and the only signal is `eligible_count < row_count` in the
  retrieval block)

The governing definitions live in `successor-reuse/lesson-selection-criterion.md`
and the trial protocol in `successor-reuse/protocol.md`. This document is
the door; those are the rulebook.

## 2. Where the store lives

- **Database:** Supabase, `learning_evidence` table
- **Project:** the canonical project ref — default
  `dahisasgpfvziswqvmvm` (an identifier, not a secret; credentials stay
  with the transport, never in this repo). Override per runtime:
  `NAYA_LESSON_PROJECT_REF=<ref>`.
- **The exact query** (verbatim what the seam runs):

```sql
SELECT id, target_id, level, status, provenance, verification_method, claim
FROM learning_evidence
WHERE level = 'E5_CAN_TEACH' AND status = 'ACTIVE'
ORDER BY created_at DESC LIMIT 25
```

Eligibility filtering (E5 + ACTIVE + TRIAL_EVIDENCE) happens in code
(`select.eligible_lessons`), so the store query stays a plain read.

## 3. How to connect — the transport

The seam speaks to the store through a **transport**: any executable that
accepts

```
<transport> POST /v1/projects/<project_ref>/database/query '{"query": "<SQL>"}'
```

and prints a JSON row list on stdout. The seam **resolves** the transport,
in order — never a hardcoded private-machine path:

1. `NAYA_LESSON_TRANSPORT` — explicit path to your transport executable
2. `SB_API` — env var pointing at the connected-connector CLI
3. `PATH` lookup for `sb-api`
4. **Refuse:** `STORE_UNREACHABLE` — naming this prerequisite instead of
   failing on a machine-specific path

Two ways to satisfy the prerequisite:

- **In the governed runtime:** the `sb-api` CLI (Supabase skill) is the
  zero-config transport — but it is NOT on `PATH` by default. Set
  `SB_API=$HOME/workspace/skills/supabase/bin/sb-api` (or point
  `NAYA_LESSON_TRANSPORT` at the same path) before running. The CLI never
  handles raw keys; only the authd surrogate leaves the machine.
- **Anywhere else:** build a script that speaks the protocol above (e.g. a
  thin wrapper around `curl` with your own read-only credentials) and point
  `NAYA_LESSON_TRANSPORT` at it. The seam does not care how the transport
  authenticates — only that the query stays a read.

## 4. Run it — step by step

From the repo root:

```bash
# 1. Check the seam resolves (prints transport + source, or refuses with a reason)
python3 -c "
import sys; sys.path.insert(0, 'tools')
from successor_ingest.read import resolve_transport, IngestError
try:
    print(resolve_transport())
except IngestError as exc:
    print(f'REFUSED {exc.code}: {exc.detail}', file=sys.stderr)
    sys.exit(3)"

# 2. Retrieve all eligible lessons (JSON to stdout)
python3 tools/successor_ingest/retrieve.py

# 3. Retrieve the lesson for one task family
python3 tools/successor_ingest/retrieve.py --family state_file
```

Every lesson in the output carries its own provenance, stamped by the
**seam, not by you**:

- `retrieved_at` — UTC timestamp of THIS retrieval
- `query` — the exact SQL that produced it

A lesson without these two fields did not come through this seam and may
not enter the reuse path. The output also carries a `retrieval` block:
transport path, how it was resolved, project ref, query, timestamp, and
row counts.

## 5. Fail-closed refusals — what each means, what to do

| Code | Meaning | Do this |
|---|---|---|
| `STORE_UNREACHABLE` | no transport resolved, or the transport failed / returned garbage | Satisfy the prerequisite (§3). **Never** invent rows, lower the bar, or cache stale ones. |
| `NO_VERIFIED_LESSONS` | the store answered but zero rows are E5/ACTIVE/TRIAL_EVIDENCE | Report it. Do not reach for a CANDIDATE or a lower level. |
| `UNKNOWN_TASK_FAMILY` | the requested family is not a declared lesson family | Use a declared family (see `select.FAMILY_TARGETS`). No fuzzy fallback. |
| `NO_APPLICABLE_LESSON` | family declared, but no verified lesson covers it | Report it. A lesson is never transplanted across families. |
| `NOT_APPLICABLE` | the lesson's family doesn't match your brief | Re-check your brief or your family choice. |

Exit codes of `retrieve.py`: `0` retrieved · `3` REFUSED (one of the
codes above, named on stderr) · `2` usage error.

## 6. What NOT to do

- **Never hand lesson text directly to a trial arm.** A handed lesson is a
  STUBBED arm — a harness rehearsal, never ingestion proof (protocol §8).
  The treatment arm must receive the lesson through this seam, evidenced
  by the retrieval stamp (query + timestamp + row ID) in the trial archive.
- **Never self-verify your own retrieval.** Builder ≠ verifier, always.
- **Never write to the store through this path.** The seam is read-only by
  construction; DB writes are a protected gate (Shawn's word only).

## 7. After retrieval

- Match the lesson to your task family (`select.match_task`), check
  applicability (`select.check_applicability`), apply it, and have the
  outcome **independently verified** — the full chain is in
  `tools/successor_ingest/ingest.py` (11 stages; SMART LINK is honestly
  UNINSTRUMENTED until the corpus-projection gap closes).
- A reuse event emits a tamper-evident receipt (`receipt.py`); the receipt
  is evidence, never authority.
- Independent retests of this path belong on the team feed with the
  retriever's identity and the row IDs.

**Honest limits (2026-10-09):** the store's read path is proven live from
the governed runtime; a cold machine without the connector satisfies §3's
second option or receives `STORE_UNREACHABLE`. Retrieval proves a lesson
was *reached*, not that it was *reused* — reuse is the trial lane's proof.
