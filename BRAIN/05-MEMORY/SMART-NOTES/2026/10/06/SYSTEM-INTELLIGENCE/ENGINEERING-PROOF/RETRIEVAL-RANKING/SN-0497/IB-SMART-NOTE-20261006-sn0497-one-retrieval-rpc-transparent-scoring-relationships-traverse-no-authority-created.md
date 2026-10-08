# IB-SMART-NOTE-20261006-sn0497-one-retrieval-rpc-transparent-scoring-relationships-traverse-no-authority-created

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20261006-sn0497-one-retrieval-rpc-transparent-scoring-relationships-traverse-no-authority-created |
| Smart Note | SN-0497 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-06 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

The COLD RETRIEVE lane (2026-10-06) went from 2/10 to 7.5/10 and closed GAP C behaviorally. The assessment found the canonical intelligence index existed only as Postgres rows: `nayanet_intelligent_blocks` had retrieval-ready fields (title, type, CANDIDATE→LEARNED lifecycle, scope, content, lineage), but there was zero full-text search, zero vector/embeddings, zero retrieval RPC, zero ranking function — and lineage links existed as data with NOTHING traversing them. Built on the branch `naya/cold-retrieve-v1` (commit `93b1372`): migration `20261006235900_nayanet_cold_retrieve_search_v1.sql` (trigger-maintained weighted tsvector + GIN + backfill) plus the `nayanet_retrieve_blocks()` RPC with transparent scoring — 0.50 text + 0.25 applicability + 0.15 truth-state + 0.10 recency, with a cold-start default; Edge Function `nayanet-intelligence-retrieve` (GitHub-OIDC auth on the know-runtime proof pattern) that calls the RPC then expands relationships: SUPERSEDES chains resolve to the live successor (a superseded draft is never served without its successor), allowlisted SUPPORTS/REFINES edges attach context, CONTRADICTS/INVALIDATES surface as conflicts — never merged. Design rules: built on the existing block row and KNOW selector instead of a second system; retrieval creates no authority; best-effort receipt. A genuine cold test — a zero-context agent given ONLY the retrieval CLI, 3 real tasks, gold-standard answers — went 3/3 PASS: it retrieved the right blocks, queried adversarially for exceptions, surfaced a CONTRADICTS conflict without merging it, and honestly flagged what the corpus could NOT answer. Honest boundaries: the test ran on the Python behavioral mirror (no DB in this sandbox), corpus was 14 blocks; the migration and function are complete but NOT applied/deployed. PR creation is 403-blocked on the agent PAT (the same wall sibling lanes hit) — a human opens it from the branch with the saved PR text. Lane parked at the gate: merge → apply migration → deploy function → prove at real corpus scale → cold-successor proof consumes it.

## HUMAN NOTE

Shawn — the cold-retrieve seat built the thing the whole learning loop was missing: a way to actually ASK the brain a question. Until today, all our intelligence was rows in a database that nothing could search — the relationships between notes existed as data, but nothing ever followed them. Now there's one retrieval call with a published scoring formula (how well it matches the words, how applicable it is, how trusted it is, how fresh it is), and relationship rules: superseded notes resolve to their live successor, supporting notes attach as context, contradicting notes surface as flagged conflicts — never blended together. A cold agent with zero context was given only this interface and three real tasks: 3 out of 3 correct, including hunting for exceptions on its own and honestly saying when the brain couldn't answer. The code is on a branch, proven at small scale; opening the PR needs one human click (agents' PR-creation is blocked). When it lands and the database pieces are applied, the cold-successor proof finally has the retrieval half it was waiting on.

## CHILD NOTE

All the library's books were just sitting in boxes — you couldn't search for anything, and the little cards saying "this book replaces that one" were never followed. Now there's one front desk that searches the whole library, with a scoreboard everyone can see, and it follows the cards: if a book was replaced, you get the new one; if books disagree, you see both, not a mashed-up lie. A brand-new librarian with no training was given only this desk and three real questions — all three answered right, and he even said "the library can't answer this one" when it couldn't. Honest desk, honest librarian.

## GRANDMA NOTE

The archives existed but had no card catalog — thousands of folders, no way to ask a question. The new seat built the catalog: one search, clear scoring, and the cross-references finally followed — a superseded memo leads you to the current one, related memos attach themselves, conflicting memos are flagged side by side, never stitched together. Retrieval creates no authority; it's a reading desk, not a throne. The catalog is built and tested on a small scale; the full archive rollout needs the human's word.

## NAYA NOTE

Note to future me: when the intelligence index is "rows in Postgres" with zero query path, build ONE retrieval interface with transparent scoring and published weights — text 0.50, applicability 0.25, truth-state 0.15, recency 0.10 — then close GAP C with relationship traversal: SUPERSEDES → live successor (never serve a superseded draft alone), SUPPORTS/REFINES (allowlisted) attach context, CONTRADICTS/INVALIDATES surface as conflicts, never merged. Retrieval creates no authority; best-effort receipt. Prove it with a genuine cold test: zero-context agent, real tasks, gold-standard answers, adversarial queries allowed — and demand honest "cannot answer" flags. If the PR-creation 403 wall is still standing, stop at the branch with saved PR text; the remaining steps are human gates.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261006-sn0497-one-retrieval-rpc-transparent-scoring-relationships-traverse-no-authority-created",
  "smart_note": "SN-0497",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "One retrieval RPC with transparent scoring plus relationship traversal closes the cold-retrieval gap; retrieval creates no authority; superseded drafts resolve to successors; conflicts surface, never merge.",
  "evidence": {
    "board": "#1354",
    "comments": ["6026614230", "6026705143", "6026713734", "6026723486"],
    "branch": "naya/cold-retrieve-v1",
    "commit": "93b1372",
    "migration": "20261006235900_nayanet_cold_retrieve_search_v1.sql",
    "edge_function": "nayanet-intelligence-retrieve",
    "lane_score": "2/10 -> 7.5/10",
    "cold_test": "3/3 PASS on Python behavioral mirror, 14-block corpus, gold-standard answers"
  },
  "scoring": {"text": 0.5, "applicability": 0.25, "truth_state": 0.15, "recency": 0.1, "cold_start_default": true},
  "relationship_rules": [
    "SUPERSEDES chains resolve to the live successor; a superseded draft is never served without its successor",
    "Allowlisted SUPPORTS/REFINES edges attach context",
    "CONTRADICTS/INVALIDATES surface as conflicts, never merged",
    "Retrieval creates no authority; best-effort receipt"
  ],
  "remaining_gates": "Human opens PR from naya/cold-retrieve-v1 (agent PAT 403) -> merge -> apply migration -> deploy function -> prove at real corpus scale -> cold-successor proof consumes it"
}
```
