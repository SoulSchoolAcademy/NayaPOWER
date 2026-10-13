# Merge-Endpoint 404: Use the Git-Data Merge Path — Equivalent When Merge-Base Equals Tip

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1087-merge-endpoint-404-git-data-merge-fallback
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12 ~08:08 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** smart-note-distillation loop (08:08 PDT tick, inline review).
**Provenance:** Director's shared-state.json `merge_watch_2462`: PR #2462 `fix(tests): repair pre-existing reds blocking the test check`, merged 2026-10-12T10:46:23Z (merge_commit `f9b5ac3de34d3cafa0718b20458289539e11a570629efa8a55d90c87`) — op finding: "/pulls/merge POST 404'd x3 — git-data merge path used (equivalent when merge_base==tip, platform-recorded as merge_commit_sha)".

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-12, the merge lane hit `POST /pulls/{n}/merge` returning 404 three times while landing PR #2462. It did not retry the dead endpoint: it built the merge commit directly through the git-data API (refs → trees → commits). When `merge_base == tip`, that path is byte-equivalent to what the endpoint would have produced, and the platform records the resulting SHA as the merge commit. The lesson: an endpoint failure is not a merge failure — but the fallback is only a fallback if it carries the full merge contract (correct parents, correct tree, platform-visible record), not just the tree bytes. Concrete instance of SN-0391's principle (fallbacks must carry contract semantics).

## 🩷 HUMAN NOTE

Shawn, a practical repair from this morning's merge lane worth keeping: the GitHub merge endpoint answered 404 three times on PR #2462, and the lane didn't sit there retrying — it assembled the merge commit directly through the git-data path, which is exactly equivalent when the merge base equals the tip. The platform recorded it as the merge commit, same as if the button had worked. The standing principle it proves: our fallbacks have to carry the whole contract of the thing they replace — same parents, same tree, same record — not just the file bytes.

## 👶 CHILD NOTE

Imagine the big red MERGE button is broken — it says "not found" three times. The builder doesn't wait. She puts the two block-piles together by hand, exactly the way the button would have: same starting pile, same top block, same finished pile — and writes it in the record book the same way. Rule: when the button breaks, you may do the button's whole job by hand. But you must do the WHOLE job — the record book entry included — not just stack the blocks.

## 👵 GRANDMA NOTE

Dear, this morning the usual merge button wouldn't answer — "not found," three times. Rather than hammering a dead button, our engineer assembled the merge the long way around through the platform's own machinery: the same two parents, the same final tree. The platform recorded it identically. The principle: a fallback is only a fallback if it carries the same contract — the same parents, the same tree, the same record. A shortcut that drops any of those isn't a fallback; it's a different action wearing a fallback's name.

## 🧠 NAYA NOTE

Cold successor: when `POST /pulls/{n}/merge` 404s on a real merge, the sanctioned fallback is the git-data merge path: compute `merge_base` of the target branch tip and the PR head; if `merge_base == tip`, create the commit (parents: tip + head; tree: head tree) and update the ref via `POST /git/refs`. The platform records the resulting SHA as the merge commit — byte-equivalent to the endpoint path. If `merge_base != tip`, STOP: the equivalence claim fails (the endpoint would have computed a true merge, your manual commit would not match it) — escalate instead. Never substitute a rebase-and-push and call it a merge — that rewrites history, a different contract entirely. Log the fallback explicitly in the merge verdict, as the #2462 verdict did. General principle: SN-0391 (fallbacks must carry contract semantics). Related evidence discipline: SN-0950 (merge_commit_sha semantics).

## 🤖 MACHINE NOTE

```json
{
  "failure": "POST /pulls/{n}/merge -> 404 (x3, PR #2462, 2026-10-12)",
  "fallback": "git-data merge path: commit(parents=[tip, head], tree=head tree) -> POST /git/refs",
  "equivalence_condition": "merge_base == tip",
  "contract": ["parents are tip and head", "tree is the true merge tree", "platform records SHA as merge_commit_sha"],
  "non_equivalent_if": "merge_base != tip -> STOP, escalate",
  "never": "rebase-and-push presented as a merge",
  "log_it": "name the fallback explicitly in the merge verdict",
  "evidence": "shared-state.json merge_watch_2462; PR #2462 merged 2026-10-12T10:46:23Z, merge_commit f9b5ac3de34d3cafa0718b20458289539e11a570629efa8a55d90c87"
}
```
