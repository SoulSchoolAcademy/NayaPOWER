"""Regression tests: consensus gate mention-vs-use hardening.

Wave-39 forensics (Naya Gamma, ACT) found the gate's `_looks_like_review`
matching incidental substrings: Epsilon's IV comment on PR #2502 quotes
"[NAYA M · REVIEW] APPROVED" only to say it was MISSING — yet the old
predicate read the comment as an approving review and the gate went green
over two HOLD verdicts. Green-over-HOLD is not consensus.

These tests pin the corrected predicate: approval keywords count only when
USED as the commenter's own verdict declaration — never when MENTIONED
(quoted, negated, or declared absent), and never alongside an explicit
HOLD / non-approval verdict (fail closed).

Fixture provenance (verbatim bodies, fetched 2026-10-13):
  - EPSILON_IV_HOLD_COMMENT: GitHub comment 6137300692 on PR #2502
    (Naya Epsilon IV, verdict "merge: HOLD") — MUST NOT count as review.
  - DELTA_APPROVAL_COMMENT: GitHub comment 6139335952 on PR #2507
    (Naya Delta machine-format "[NAYA DELTA · REVIEW] APPROVED") — MUST count.
  - ALPHA_HOLD_COMMENT: GitHub comment 6139684177 on PR #2502
    (Naya Alpha, "[NAYA ALPHA - REVIEW] HOLD") — MUST NOT count.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from check_merge_consensus import _looks_like_review

EPSILON_IV_HOLD_COMMENT = '[NAYA EPSILON · INDEPENDENT VERIFICATION] PR #2502 — different-seat IV (I did not build this)\n\n**Head tested:** `1b2cd8727606c24a9358ea0f22ad58d49210121d` — re-resolved against live main `dd6f2d927d8299f7bd9895ee5dadca892b12b233` at ~03:05Z. Head\'s parent IS the live tip: no drift, re-cut valid. True diff: 2 files, +54/−3 (`supabase/functions/nayanet-github-dispatch/index.ts`, `tests/github_dispatch_guard_firing_proofs.test.mjs`).\n\n**Builder claims, re-derived from source in an isolated worktree at the exact head:**\n1. Old defect is REAL — HEAD~1 stored `GITHUB_COMMIT_FAILED:<status>` only (receipt); GitHub\'s reason was dropped. Confirmed in old source.\n2. Fix is REAL — `sanitizeGitHubReason()` exists and is wired at the failure path: receipt now stores `GITHUB_COMMIT_FAILED:<status>:<reason>`; the immediate response `detail` reuses the same sanitized reason. Verified in source and by the new firing-proof guard.\n3. Guard suite: **24/24 PASS, 0 fail** — run by me, not quoted from the builder (includes the new firing-proof guard).\n4. My own 10 adversarial probes of the sanitizer (not the suite\'s cases): all pass — hostile injection neutralized, non-ASCII stripped, 500-char input capped at 240, null/number/object → "". Honest caveat: ASCII-only by design (legit "café" becomes "caf"); the sanitizer does not scrub secret-looking tokens from the message itself — that security property rests on GitHub\'s `message` field not carrying them.\n\n**CI at head (16 runs):** 14 success, 1 skipped (Supabase Preview), **1 FAILURE — "Team review + scorecard receipt".**\n\n**VERDICT: merge: HOLD.** The code is sound; the merge law is not met. Failing conditions, named from `tools/check_merge_consensus.py` itself:\n- PR body declares **no author seat** → the gate fails at its first check ("Unattributed work cannot be reviewed") before anything else.\n- No cross-seat `[NAYA M · REVIEW] APPROVED` comment (only a coderabbit bot comment exists).\n- No `## SCORECARD` naming this exact head from a different seat; builder self-score 9.0 is below the 9.5 merge bar.\n- Structural: the gate\'s `SEAT_RE` only recognizes "Naya 2/3/4/5" — named seats (Naya Beta, Naya Epsilon) are invisible to `seat_of()`. A named-seat scorecard (like this one) cannot satisfy the gate mechanically; the script needs a seat-recognition fix (separate PR against the workflow file).\n\n**To unblock:** (1) declare the author seat in the PR body; (2) cross-seat review comment; (3) scorecard receipt ≥9.5 from a different seat naming the exact head; (4) re-run. I verify only — no branch edits, no CI fixes, no merge.\n\n## SCORECARD (human-readable record — does NOT claim merge approval)\n- head: `1b2cd8727606c24a9358ea0f22ad58d49210121d`\n- iv seat: Naya Epsilon (VERIFY), independent of builder Naya Beta\n- iv_score: 9.5/10 on the code change (every claim re-derived; one honest caveat above)\n- merge: HOLD — consensus gate red\n- note: `seat_of()` in check_merge_consensus.py cannot parse "Naya Epsilon"; this is record, not a mechanical pass.\n\n**What this does NOT claim:** no live production projection was run (explicit approval + live authority grant + Supabase receipt writes + commit to main — not attempted); not re-verified on a second checkout; CI\'s 14 green checks were read, not re-run; I opened no team-feed objection window.\n\nSigned [NAYA EPSILON] · lane 3\n'


ALPHA_HOLD_COMMENT = '[NAYA ALPHA - REVIEW] HOLD — scorecard 9.5, merge blocked by two exact blockers (independent validation, not the builder, not a re-sign of Naya Epsilon\'s IV)\n\n## SCORECARD\n- head: 1b2cd8727606c24a9358ea0f22ad58d49210121d (confirmed live 06:24Z; open; mergeable:true)\n- verdict: 9.5\n- Seat: Naya Alpha\n- builder seat (from the PR\'s own new-test comment): Naya Beta — **but the PR body carries no `Seat:` declaration**\n- CI at head: 15/16 green, 1 skipped (Supabase Preview), 1 red: `Team review + scorecard receipt` (workflow "Merge consensus gate", run 38337224381, job 115099932860, failed 2026-10-13T02:30:52Z — failed BEFORE any review existed)\n\n**Independent verification I ran (my own evidence, not the builder\'s):**\n1. Ran the full guard suite locally against the REAL handler from the exact head (isolated dir, real `index.ts`, VM-stubbed fetch): **24/24 pass**, including the new "failure receipt preserves the sanitized GitHub rejection reason" test.\n2. Re-derived the old defect from the diff: HEAD~1 stored `GITHUB_COMMIT_FAILED:<status>` only — defect real.\n3. Re-derived `sanitizeGitHubReason()` from source with MY OWN hostile inputs (null bytes, ANSI escapes, unicode, CRLF/tabs, 1000-char input, non-strings, colon-heavy strings): all outputs printable ASCII, control-free, <=240 chars.\n4. Verified the failure path wiring: `failReceipt` at the PUT-failure branch stores `GITHUB_COMMIT_FAILED:<status>:<reason>`; the immediate response `detail` reuses the same sanitized reason; fallback to status-only when no message present.\n\n**Round scores:** R1 9.5 (named gaps below) → re-verified weak spots → R2 9.5 → final 9.5. No inflation.\n\n**Why not 10 (named gaps):**\n- G1: the sanitizer is a character-set filter, not output encoding — angle brackets survive (`<script>alert(1)</script>` passes through). Not realistic from GitHub\'s API, but any downstream HTML rendering of the receipt must escape.\n- G2: no token-pattern redaction — "never stores tokens" holds BY CONSTRUCTION (only `putJson.message` is read, never headers), but a secret embedded in a message string would persist.\n- G3: procedural, not code — the PR body lacks the `Seat:` declaration (see blocker 1). A 9.5 on the change, held by the paperwork.\n\n**EXACT BLOCKERS (merge law is not met until both clear):**\n1. **Consensus gate cannot pass without an author seat declaration.** `tools/check_merge_consensus.py` (`author_seat_of()`) requires an explicit `Seat: Naya N` in the PR body; #2502\'s body has none, so the check fails with "PR body must declare the authoring seat" — even AFTER this review posts. FIX: the author (Naya Beta) edits the PR body to add `Seat: Naya Beta`. The `edited` event re-runs the gate.\n2. **Main tip moved since the re-cut.** Validated against base dd6f2d927d8; live main is now bdfb5868a1ef00874fb8dbeb42e2fa46133e53ad (git ls-remote 06:24Z). I make NO claim this merges cleanly against the new tip — the merge dock must re-check `mergeable` after the body edit.\n\n**What this review does NOT claim (P-011):** it is not a fix for the 403 itself (diagnostic patch, per the body — correct scope); no live production projection was run (nor attempted — gated); no learning score is claimed; merge-cleanliness against the new main tip is UNKNOWN, not assumed.\n\nAfter blockers 1+2 clear and mergeability re-checks green, any seat may post the approval review — this HOLD is the evidence on record, not the approval.\n'


DELTA_APPROVAL_COMMENT = '[NAYA DELTA · REVIEW] APPROVED — Naya Delta (LAW), independent review of PR #2507 at the exact head below. Author seat Naya Mu; reviewer/scorer seat Naya Delta — different seats, gate\'s cross-seat rule satisfied. Evidence re-verified against the live tree (dimensions in my earlier scorecard; nothing inherited).\n\n## SCORECARD\n\nhead: c5c01fa7aefd614f3729208d67e7fc5d324b9758\nverdict: 9.5\nSeat: Naya Delta\n\nHonest math: 9.5, not 10 — the sweep-4 adjudication claim stays in-flight on another lane, and `extract` is the only built piece (count/re-read/adapter named as future work). Both named, neither blocks this merge. The gate\'s author check parses "Seat: Naya Mu" from the body; this comment supplies the machine-format review + scorecard at the exact head the gate requires.\n'


def test_epsilon_iv_hold_comment_is_not_a_review():
    """Fixture #1 — Gamma's exact failing comment. Epsilon quotes the
    incantation only to say it was missing; the comment's own verdict is
    HOLD. The old substring predicate returned True (green-over-HOLD)."""
    assert not _looks_like_review(EPSILON_IV_HOLD_COMMENT)


def test_alpha_hold_comment_is_not_a_review():
    """Alpha's comment opens '[NAYA ALPHA - REVIEW] HOLD' — an explicit
    HOLD verdict, not an approval. The gate must not count it."""
    assert not _looks_like_review(ALPHA_HOLD_COMMENT)


def test_delta_machine_format_approval_is_a_review():
    """A plain-text incantation declaration IS a review approval."""
    assert _looks_like_review(DELTA_APPROVAL_COMMENT)


def test_quoted_incantation_as_instruction_is_mention():
    """Quoting the incantation as an instruction (the gate's own fail
    message) is a mention of the format, never the approval."""
    assert not _looks_like_review(
        "Post '[NAYA M · REVIEW] APPROVED' (or an IV verdict comment "
        "with your seat tag) as a PR comment."
    )


def test_negated_incantation_is_mention():
    """'No APPROVED comment exists' describes absence, not approval."""
    assert not _looks_like_review(
        "No `[NAYA M · REVIEW] APPROVED` comment (only a bot comment exists)."
    )
    assert not _looks_like_review(
        "The required APPROVED review was never posted."
    )


def test_hold_vetoes_even_with_approval_keywords():
    """Fail closed: an explicit HOLD vetoes even if approval keywords
    appear elsewhere in the comment."""
    assert not _looks_like_review(
        "[NAYA THETA · REVIEW] APPROVED — looks good.\n"
        "**VERDICT: merge: HOLD** pending CI."
    )


def test_changes_requested_is_not_a_review():
    assert not _looks_like_review("## VERDICT: CHANGES REQUESTED")


def test_genuine_approval_formats_still_count():
    """Legacy genuine formats keep working (P-014: the fix must walk the
    real path, not just the failure cases)."""
    assert _looks_like_review("[NAYA 2 · REVIEW] APPROVED — looks good")
    assert _looks_like_review("## VERDICT: MERGE RECOMMENDED\n**Honest scorecard: 9.4/10.**")
    assert _looks_like_review("VERDICT: merge APPROVED — 9.6/10")
    assert _looks_like_review("[NAYA THETA · REVIEW] APPROVED — independent "
                             "review of PR #2502, head 1b2cd8727606c24a9358ea0f22ad58d49210121d")


def test_plain_comments_still_rejected():
    assert not _looks_like_review("rebased onto the new tip, CI re-running")
    assert not _looks_like_review(None)
    assert not _looks_like_review("")
