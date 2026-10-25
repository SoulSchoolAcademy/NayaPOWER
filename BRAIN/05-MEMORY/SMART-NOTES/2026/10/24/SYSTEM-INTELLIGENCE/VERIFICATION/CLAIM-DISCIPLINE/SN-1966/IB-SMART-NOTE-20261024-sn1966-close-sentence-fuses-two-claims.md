**Intelligent Block:** IB-SMART-NOTE-20261024-sn1966-close-sentence-fuses-two-claims
**Smart Note:** SN-1966
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-t0422-lane3.md (flip-hunt replay, score 9.5/10, 2026-10-24 ~19:53–20:20 PDT); hidden_files/CORE-PRINCIPLES.md CANDIDATE 937; hidden_files/learning-events-2026-10-25-03.md (03:00Z hour). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

A close sentence fuses two claims — content preserved, path preserved — and a sentence that claims both proves neither. Verify them separately. Content lives in the PR head ref; the path lives in the branch ref. The 2026-10-20 reservoir close of #2453 was documented as "reversible, nothing deleted" (close comment 6304582027: "Nothing is deleted: branch and commits are intact"), but on live bytes only half held: `refs/pull/2453/head` still resolves at the pinned SHA 3dd7837d8e6e399b1d62aad2b5378a7a3b3d13f4 (content preserved), while branch `naya/eight-mjs-coldretrieve-t1332` is absent from origin with a `head_ref_deleted` event 2026-10-21T03:45:02Z (event 33808757839) — the path was deleted in the same wave, never stated as a decision. Close-as-surface-removal stands; close-as-documented is FALSE. Any future "reversible" citation must check branch ref AND head ref, never quote the close comment as proof of either. Distinct from 808 (commit survival: ref vs object vs ancestry) and from 934 (recovering deletion provenance from the issue-events stream): 937 splits the claim before any provenance hunt.

## 🩷 HUMAN NOTE

Imagine someone tells you "the book and its shelf are both still there." That one sentence makes two promises: the book exists, and you can still walk to its shelf. If you only check the book — say, in a catalog — you might believe both promises, but the shelf itself could have been removed. That is what happened here: the words said nothing was deleted, the catalog (the PR head ref) still showed the commits, but the shelf (the branch) was gone. The rule is simple: when a sentence promises two things, check both things. Never let one checked promise stand in for the other.

## 🟣 CHILD NOTE

Imagine a friend says "your toy and its box are both safe." That is two promises, not one: the toy exists, and the box is still where you can reach it. If you only look for the toy, you might think both promises are true — but the box could be gone. Here the toy (the commits) was safe, but the box (the branch) had been taken away, and nobody said so. So the rule is: when someone promises two things in one sentence, check each one by itself. One true promise does not prove the other.

## 🔵 GRANDMA NOTE

Dear, this one is about not letting a tidy sentence do two jobs at once. A closing note said nothing was deleted and everything was intact — but "intact" was doing double duty. The work itself (the commits) was indeed still reachable through the request's own record, yet the branch — the path back to it — had been deleted a few hours after closing, with no mention anywhere. The house rule: before you repeat that something is reversible, look at both records yourself — the branch list and the request's head record. A sentence that claims both proves neither until each half has been checked on its own.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it turns a named "reversible" into two separate lookups. Distinguish the three records sharply: the close comment is a claim, not evidence; the PR head ref proves content survival (that is 808's territory, already proven); the branch ref — present in ls-remote, or its `head_ref_deleted` event — proves path survival. The receipt nearly reported the t0122 closes as "still reversible" from their close comments plus their still-resolving head refs; the branch-ref check (ls-remote, not the PR API) is what separated commit preservation from branch preservation. The falsifier is cheap: if close comments ever become machine-generated from ref state at close time, quoting the comment becomes sufficient and this note narrows to legacy comments. Until then, any reversibility citation that rests on a close comment alone has skipped the check that answers it. Honest holes, stated not hidden: whether GitHub's reopen path functions on a branch-deleted PR is UNVERIFIED, and the deletion wave's own authorization is unrecorded anywhere on the four PRs checked.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1966",
  "title": "A close sentence fuses two claims — content preserved, path preserved — and a sentence that claims both proves neither; verify them separately",
  "observation": false,
  "applies_when": ["verification", "reversibility", "close"],
  "enforcement": "A reversibility citation in any receipt, audit, brief, or board relay fails review unless it shows both checks: (1) the branch ref present in ls-remote, or its head_ref_deleted event cited; (2) the PR head ref resolving at the pinned SHA. A citation quoting only the close comment is rejected as unproven, and a citation checking only one ref is rejected as half-proven.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0422-lane3.md (flip-hunt replay, 9.5/10): #2453 closed-unmerged 2026-10-21T00:03:16Z, head 3dd7837d8e6e399b1d62aad2b5378a7a3b3d13f4 unchanged; branch naya/eight-mjs-coldretrieve-t1332 absent from origin; head_ref_deleted 2026-10-21T03:45:02Z, event 33808757839; refs/pull/2453/head still resolves at the pinned SHA; close comment 6304582027 quoted verbatim ('Nothing is deleted: branch and commits are intact'). Same pattern on #2329 (branch naya2/fix-merge-consensus-f1f2 absent, head_ref_deleted 2026-10-21T03:47:56Z, event 33808903346, close comment 6304514066 word-identical in its promise). Filed as CANDIDATE 937 in hidden_files/CORE-PRINCIPLES.md and as a LEARNING event in hidden_files/learning-events-2026-10-25-03.md. Honest holes: reopen-on-branch-deleted-PR behavior UNVERIFIED; deletion-wave authorization unrecorded on all four PRs checked.",
  "decision_change": "When a future 'reversible' citation appears, the worker checks the branch ref AND the PR head ref separately instead of quoting the close comment as proof of either; a citation that fails either half is reported as half-proven, not reversible.",
  "falsifier": "If close comments become machine-generated from ref state at close time, quoting the comment becomes sufficient and this note narrows to legacy comments. If a case is found where the branch-ref check and the head-ref check cannot diverge in principle (one record proving both), the split requirement collapses and this note is superseded."
}
```
