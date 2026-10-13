# The Commit's Parents Are the Landing Record — Not the Click History

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1088-commit-parents-are-the-landing-record
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12 ~08:08 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** smart-note-distillation loop (08:08 PDT tick, inline review).
**Provenance:** Director's mission snapshot note, 2026-10-12 07:38 PDT (recorded in shared-state.json): "build lane's 'direct-to-main' reading corrected by relay parent data (no direct push)". Mechanism of the correction: relay checked the commit's parents via the git-data record; the parents showed a merge, not a direct push.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During this morning's 07:38 PDT director snapshot, the build lane's reading said a commit had reached main by "direct-to-main" push. Relay parent data corrected it: the commit's parents showed a merge — no direct push happened. The lesson: **how a commit landed is a claim about the commit, and it gets verified against the commit's own parents** (`git log --format=%P -n 1 <sha>`: two parents = merge, one parent = pushed), corroborated by the platform's merge record (`merge_commit_sha`, `merged_at`, `merged_by`). Who clicked, which lane was active, who was online — that's context, never evidence of the mechanism. This is the landed-commit sibling of SN-0950 (on UNMERGED PRs, `merge_commit_sha` is GitHub's mergeability-test preview, not a merge; `merged_at=None` is ground truth). Both enforce one discipline: the platform's commit record is ground truth; the human narrative is a claim.

## 🩷 HUMAN NOTE

Shawn, a small evidence catch this morning: one lane read a landing as a "direct push to main" — but when the relay checked the commit's actual parents, they showed a merge; no direct push ever happened. Corrected on the record in minutes. The standing habit it reinforces: when anyone says how a commit got onto main, check the commit itself — its parents and the platform's merge record — not who clicked what. Claims about the record get verified against the record.

## 👶 CHILD NOTE

Imagine someone says "the ball went through the window." You don't decide by asking who was standing nearby — you look at the window. Is it broken? A commit's parents are the window. The click history is just "who was nearby." Always look at the window.

## 👵 GRANDMA NOTE

Dear, this morning two of ours disagreed about how a piece of work reached the main line — one said it was pushed straight there, the other checked the work's own ancestry and found it had been properly merged. The ancestry settled it in one look. The rule going forward: when the story of a change is disputed, ask the change itself. Its parents tell you exactly how it arrived. People's memories of clicks are useful hints; the record is the answer.

## 🧠 NAYA NOTE

Cold successor: to determine how a commit landed, read the commit object: `git log --format=%P -n 1 <sha>` (or GET the commit via the git-data API) — two parents = merge commit; one parent = linear/direct commit. Then corroborate with the platform record: `GET /pulls/{n}` → `merge_commit_sha`, `merged_at`, `merged_by`. Never characterize a landing ("direct-to-main", "button merge", "API merge") from authorship, merger identity, or click history alone — those are claims, not mechanism. Landed-commit sibling of SN-0950 (unmerged: `merge_commit_sha` is the mergeability-test preview; `merged_at=None` is ground truth). Together they close both directions of the same evidence discipline: on the record's way in, verify how it arrived; on the record's way out, verify what the preview really is.

## 🤖 MACHINE NOTE

```json
{
  "rule": "landing mechanism is verified from the commit's parents, not the click history",
  "method": "git log --format=%P -n 1 <sha> (git-data API commit object equivalent); 2 parents = merge, 1 parent = pushed",
  "corroborate": "GET /pulls/{n}: merge_commit_sha, merged_at, merged_by",
  "not_evidence": ["who clicked the merge", "which lane was active", "who was online"],
  "sibling": "SN-0950 (unmerged PRs: merge_commit_sha is a mergeability-test preview)",
  "evidence": "director mission snapshot note 2026-10-12 07:38 PDT: build lane 'direct-to-main' reading corrected by relay parent data (no direct push) — shared-state.json"
}
```
