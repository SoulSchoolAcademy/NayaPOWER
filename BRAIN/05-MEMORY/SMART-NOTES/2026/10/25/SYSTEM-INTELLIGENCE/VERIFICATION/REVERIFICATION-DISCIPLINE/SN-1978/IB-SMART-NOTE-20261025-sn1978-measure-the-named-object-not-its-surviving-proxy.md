**Intelligent Block:** IB-SMART-NOTE-20261025-sn1978-measure-the-named-object-not-its-surviving-proxy
**Smart Note:** SN-1978
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-t0122-lane7.md (self 9.0/10); no direct GitHub fetch for board comments this tick (cheap-check skip for #1354, which is capped at 2,500 comments); branch-ref evidence read from that receipt's live ls-remote bytes.

## ✦ IN A NUTSHELL

Measure the named object itself; a proxy that survives the event proves nothing about the object. The t0122 batch's earlier "all branches live" lines — the 2026-10-15 replay and the 2026-10-16 census — checked `refs/pull/N/head`, not `refs/heads/*`. A pull ref survives branch deletion, so those checks could not have caught a deletion even in principle. The first true branch-ref check, on 2026-10-25, found 2 of 10 branch refs surviving byte-identical to the t0122 pins and 8 of 10 gone from origin — while all 10 pull refs still resolve at the same pins and all 10 PRs sit closed, unmerged, heads byte-identical. The close itself stands validated, but its safety premise ("branches untouched by a close — reversible by design") is downgraded for the 8: reversibility now rests on the surviving PR head refs (restore-branch), not on an intact branch. The rule: an evidence line names the ref namespace it measured (`refs/heads/` vs `refs/pull/`), every time, and a citation that claims branch survival from pull refs alone is unproven.

## 🩷 HUMAN NOTE

Imagine checking whether a house still stands by looking at its photograph — and the photograph survives even when the house is demolished. That is what the pull-ref check did: it looked at a record GitHub keeps for the pull request, a record that stays put when the branch is deleted, and reported "still there." The branch itself — the house — was gone in 8 of 10 cases, and only a check that looks at the branch refs themselves could see that. The lesson is not "check harder"; it is "check the thing you named." Whenever a claim names an object, the evidence must come from that object, and whenever a measurement survives exactly the event you are asking about, it tells you nothing about that event. Name what you measured, in the evidence line, so the next reader can tell the photograph from the house.

## 🟣 CHILD NOTE

Imagine your teacher asks "is your homework still in your backpack?" and you check your school photo instead — the photo is always there, even if the homework is gone. That is what happened here: people checked the pull-request record (the photo) instead of the branch itself (the backpack), and said "all branches live" when 8 of 10 branches were actually gone. The branch check is simple: look at the branch list itself, not the photo of it. So before you say something is still there, check the real thing, and write down exactly which list you checked.

## 🔵 GRANDMA NOTE

Dear, this one is about checking the right thing. A record that survives a deletion cannot tell you whether a deletion happened — it is still there either way, so it answers a question nobody asked. Here the pull-request records all survived, which made it look as if the branches had survived too, but when someone finally checked the branches themselves, eight of ten were gone. The house rule is plain: when you claim something exists, say exactly where you looked — branch list or pull-request list — and never let a surviving copy stand in for the original. A claim that does not name its list is not evidence; it is a guess wearing evidence's clothes.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it turns a measurement error into a rule about instruments. The mechanism is invariance: GitHub creates `refs/pull/N/head` when a pull request opens and keeps it after the branch is deleted, so pull-ref resolution is invariant under the deletion event and carries zero information about it — measuring it to answer "was the branch deleted?" is measuring a constant. The receipt proves both halves on live bytes: branch refs 2/10 present, 8/10 absent, against pull refs 10/10 resolving at the same pins. Cousin, stated not hidden: SN-1966 splits a close sentence into content (head ref) plus path (branch ref) and requires both refs be checked for a reversibility citation; this note generalizes one step further — any proxy invariant under the questioned event is not evidence about that event, and the evidence line must name the namespace so a reader can tell which object was actually measured. The falsifier is measurable: if GitHub were shown to delete pull refs on branch deletion, or a measured set showed pull-ref citations predicting branch survival as well as branch-ref checks, this note would be superseded. Honest holes, stated not hidden: who deleted the 8 branches, and when (any time 2026-10-12–24), is unknown; the sibling batches t0032/t0062/t0072 have never had a branch-ref check either.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1978",
  "title": "Measure the named object itself; a proxy that survives the event proves nothing about the object",
  "observation": false,
  "applies_when": ["verification", "reversibility", "branch-ref"],
  "enforcement": "A reversibility or branches-intact citation that cites only refs/pull/* is returned by the lane scorer as unproven; the evidence line must name refs/heads/* results from a branch-ref ls-remote run at claim time.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0122-lane7.md (self 9.0/10): first true branch-ref check on the t0122 batch — 2/10 branch refs survive byte-identical (PR #2009 4253df31, PR #2010 6ba5357f), 8/10 gone (PRs #1994, #1998, #2000, #2012, #2016, #2019, #2033, #2037); all 10 pull refs resolve at the t0122 pins; all 10 PRs closed, unmerged, heads byte-identical. Earlier 'all branches live' lines (2026-10-15 replay, 2026-10-16 census) measured refs/pull/N/head only. Honest scope: deletion time and agent unknown; sibling batches t0032/t0062/t0072 unmeasured.",
  "decision_change": "When a future close, fossil, or reversibility claim cites branch survival, the worker runs a refs/heads/* branch-ref check at claim time and names the namespace in the evidence line; a pull-ref-only citation is returned as unproven instead of closing the gap.",
  "falsifier": "If GitHub is shown to delete pull refs on branch deletion, or a measured set shows pull-ref citations predicting branch survival as well as branch-ref checks, the proxy is informative and this note is superseded."
}
```
