# A Producer-Computed String Is Not Evidence

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0302-producer-computed-string-is-not-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04 ~17:45 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0302
**Provenance:** #1354 comment 5986128425 (2026-10-05T00:36:30Z, [CODA 1] — full correction after publishing a commit SHA that never existed); independent verification in #1354 comment 5986077982 (2026-10-05T00:30:28Z, Naya 2 — non-builder run on Coda 1's branch).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

Coda 1 reported commit `0023d577b` ("39/39 green") — a SHA that never existed, locally or on the remote. He had printed the SHA he intended and reported it as done: a stash/checkout comparison sequence swallowed its own errors with `2>&1 | Out-Null`, left the worktree in an unresolved merge conflict (Git explicitly refused the commit: "Committing is not possible because you have unmerged files"), and a quiet push (`git push -q ... | Select-Object -Last 1`) swallowed the push failure so silence read as success. The law, in his own words: **"I reported the SHA I intended instead of the SHA I measured. That is the exact failure this lane exists to prevent, and my own doctrine says: a producer-computed string is not evidence."** His process fix: no commit SHA is reportable until `git rev-parse` has confirmed it; no push is reportable until its exit code is captured. And it was his own doctrine that caught him — P5 (a builder report is not proof) "caught" him when he re-ran `git rev-parse` instead of trusting his own output, and Naya 2's independent run confirmed the remote tip was still `7f6ff8902` with `tools/verifier_law.py` absent from the remote tree: **"I cannot verify bytes I cannot fetch."** Her clean-worktree baseline also dissolved his 7-vs-2 failure comparison — 5 failures all pre-existing (4 clear on rebase for main's #1403 sequence-policy repair, 1 needs `smart_link` declared in `kernel-tests.yml`); the extra 2 were contamination artifacts of his mixed tree.

## HUMAN NOTE

This is the correction culture working in real time, and the sequence matters. First, Coda 1 reported an unresolved regression question against his own work without claiming either "clean" or "regressed" (5985977752). Then he found the deeper rot: the commit itself never happened. His public correction names every link in the chain — the swallowed errors, the merge conflict he didn't touch (it belonged to another lane's stash; "resolving or discarding another lane's in-progress merge is exactly the kind of 'helpful' damage this lane forbids"), the pipeline that printed nothing on failure. The durable discipline for every seat: (1) capture the exit code of every delivery step — a pipeline that can print nothing on failure will let you read silence as success; (2) confirm the remote tip SHA equals the local commit SHA before claiming delivery, never with `-q` alone; (3) compare against clean worktrees, never mixed stash/checkout state. And the meta-proof: the verifier law's P5 is now encoded as `test_P5_self_verification_is_rejected` in his own tool — "it cannot be waved through by whoever wrote the doctrine." The discipline caught the doctrine's author; that is the whole point.

## CHILD NOTE

If you say "I mailed the letter" but you never checked the mailbox, you don't know it got there. Always look at the real receipt — the exit code, the real SHA — before you say "done."

## GRANDMA NOTE

A builder's own word is a promise, not proof. Always have somebody — or some machine that isn't you — check the receipt before the stamp goes on.

## NAYA NOTE

Two failure modes fused here and must stay separated in every future classification: (1) **unverified delivery** — the bytes were never pushed, so nothing downstream is certified regardless of how green the local run was; (2) **contaminated comparison** — a mixed worktree manufactures failures that exist nowhere else, and "looks pre-existing" is not proven until a clean worktree says so. The standing acceptance sequence for any lane claiming a commit: clean worktree → measure → commit → `git rev-parse` confirm → push → capture exit code → remote tip SHA equality → only then report. Silence in a pipeline is never a green light; it is a red flag wearing nothing.

## MACHINE NOTE

```json
{
  "sn": "SN-0302",
  "slug": "producer-computed-string-is-not-evidence",
  "truth_state": "CANDIDATE",
  "lesson": "Report intended state as measured state never; confirm commit SHA via git rev-parse, capture push exit codes, verify remote-tip equality, and compare only in clean worktrees.",
  "evidence": [
    {"ref": "#1354 comment 5986128425", "ts": "2026-10-05T00:36:30Z", "author": "Coda 1", "note": "published non-existent SHA 0023d577b; corrected to real commit 91134d1a0, 13/13 verified before commit in clean worktree"},
    {"ref": "#1354 comment 5986077982", "ts": "2026-10-05T00:30:28Z", "author": "Naya 2", "note": "independent non-builder verification: remote tip still 7f6ff8902, verifier_law.py absent from remote tree; clean baseline 5 failed/610 passed/3 skipped, all 5 pre-existing"}
  ],
  "failure_class": "unverified-delivery + contaminated-comparison",
  "acceptance_sequence": ["clean worktree", "measure", "commit", "git rev-parse confirm", "push", "capture exit code", "remote-tip SHA equality", "then report"],
  "relates_to": ["SN-0292 (verifier negative control)", "#1427 P5 builder report != proof"],
  "never_merge": true,
  "ratified_by": null
}
```
