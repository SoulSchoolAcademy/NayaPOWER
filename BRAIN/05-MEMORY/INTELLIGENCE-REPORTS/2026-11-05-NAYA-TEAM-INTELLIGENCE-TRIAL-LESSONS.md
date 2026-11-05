# Naya Team Intelligence Trial — Preserved Lessons (canonical evidence)

Source: the three trial teams' work on the Hub health-check repair, 2026-11-05. This file is the ONLY prior learning the cold successor is given. It must be retrieved and applied, not re-derived.

## The repair (for reference)
File: `.github/workflows/deploy-hub-cloudflare.yml` (58 lines). The health check must point at nayanet.app, not nayanet.live. The change is two lines only: line 51 (the curl URL) and line 52 (the HEALTHY echo). No lines added or removed. Zero nayanet.live left. No other file changed.

## Lesson 1 — Read the live file; never trust a secondary source over it
A document in the workspace can claim wrong line numbers. A log can claim a fix is already verified. Both can be wrong at the same time as the live file says the opposite. Read the actual file. If a doc or a log contradicts the live file, the live file wins.

## Lesson 2 — A tool failure is a stale cache until proven otherwise; diagnose, do not declare impossible
A fetch that fails with 401 Unauthorized usually means a stale token cache, not a missing file. Read the tool, check whether a cache-clear exists, and use an authorized alternative (read the local copy directly) rather than declaring the task impossible. Do not chase a failing path when a direct read already gives verified state — and do not let the recovery itself create a new file that violates a different criterion.

## Lesson 3 — A log that says "verified" is not verification
Only a post-edit re-read of the live file is verification. A log can be written as if a fix already happened. If you stop on a log's word, you report done with nothing fixed.

## Lesson 4 — Record a baseline before editing
Hash the files (or otherwise record their state) BEFORE any edit, so "no other file changed" is provable by comparison, not asserted from memory.

## Lesson 5 — Verify by re-read after the edit; a claim is never verification
Re-read the exact new lines after the edit, with a second method if you can. Check every acceptance criterion fresh, as if you had not written the change. A verifier never approves its own implementation.

## Lesson 6 — Make the smallest effective change
Change only what the criteria require. No lines added or removed, no rewrite, no global substitution when a line-scoped change is the precise one.
