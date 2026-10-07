# Fail Fast at the Authoring Boundary — Refuse Bad Captures Before Persistence

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0168-fail-fast-authoring-boundary
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5945983977 ([NAYA 4][SELF-BUILD] Cycle 22:03 PDT, 2026-10-02T05:11:00Z); workflow runs 36962391370 (SN-020, head 34610822) and 36966438981 (SN-021, head b7e0eeae); local guard commit de2ac5b9; patch ~/workspace/goals/nayapower-self-build-loop/hidden_files/selfbuild-20261001-2200-cold-gate-failfast.patch.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two RED runs were classified to a single authoring-side cause instead of being patched run-by-run. Runs 36962391370 (SN-020, head 34610822) and 36966438981 (SN-021, head b7e0eeae) both passed fresh-lesson and independent-verification, then failed in ~12 seconds at the cold-successor held-out step "Cold retrieve this run's exact Smart Note from machine registry and canonical runtime." The 12-second failure ruled out the curl-retry path; passing the same runtime-verify/lineage/content checks in independent-verification isolated the failure to the comprehension asserts. Evidence: the cold step asserts `machine_view.raw_source_separate_from_distillation is True` and `machine_view.automatic_truth_ceiling == "CANDIDATE"`. SN-019 (the green run) has the field, `True`. SN-020 and SN-021 have the field absent (`None`). One cause explains both REDs. Truth status: CONTRACT GAP (authoring-side) — and the gate fail-closed correctly: both blocks persist as CANDIDATE with `understanding_state=="CANDIDATE"` independently verified; nothing false was promoted. The rule: validate the capture truth-boundary fields at discovery, before any runtime commit — the prepared fix is a fail-fast validation in fresh-lesson's "Discover generalized Smart Note capture" step that refuses a discovered capture missing either machine field with `CAPTURE_TRUTH_BOUNDARY_INVALID`, instead of REDing late in cold-successor after persistence. 7/7 controls green on the exact edited block (SN-019 passes; SN-020/SN-021 + field=false + ceiling=VERIFIED + missing machine_view all refused; no-capture path skips; workflow YAML re-parses, structure intact). GRAPH-10 stays 8.5/10. Sibling of SN-092 (self-invalidating qualification tests) and SN-079 (withheld certification is the gate working).

Two supporting instances from the same cycle belong in the record. (1) Commit 443faed7 ("fix(smart-note): encode capture truth-boundary machine fields") is an EMPTY commit — 0 files; the encoding it names never landed in the repo, and field presence currently depends on author discipline. A commit message is not evidence the change landed (SN-125 family: a push receipt is not proof of contents). (2) The guard could not be pushed: no credential helper on git, and both the Git Data API (`POST /git/trees`) and the Contents API returned 403 "Resource not accessible by personal access token." That was respected as a hard boundary, not retried. The patch was left as an artifact (26 insertions, applies at `25268675`) with the exact next action named: a seat with push rights applies it as a branch + draft PR. Backfill-vs-accept for the SN-020/SN-021 captures is Shawn's or the smart-note lane's decision — their cold-held-out proof stays RED-by-design until then.

## 🩷 HUMAN NOTE

Shawn — the night shift ran the self-build loop's "did we actually commit live intelligence" proof twice, and both runs went red at the same last checkpoint. Instead of treating them as two failures, the classifier dug in: both runs sailed through the first two stages, then failed in about twelve seconds at the final "cold successor tries to understand this run's Smart Note" step. Twelve seconds is too fast for a network problem — it meant the assertion itself was what failed. The evidence was clean: the working run (SN-019) had two truth-boundary fields in its machine record; the two red runs had neither. One root cause, two reds, and — crucially — the gate did its job: nothing was promoted on a false claim. The fix proposed is to reject bad captures at the front door (refuse them with a named error before they ever get committed) instead of discovering the problem at the end of the pipeline. The fix itself is a patch file waiting for a seat with push rights, and the honest remainder is named: the two old captures stay red-by-design until you or the smart-note lane decides whether to backfill them.

## 🟣 CHILD NOTE

Imagine a factory where toys are built, checked by one inspector, checked by a second inspector, and then a brand-new worker has to learn how to make the toy just by reading the instructions. Two toys got through both inspectors but the new worker couldn't learn from their instructions — and it only took him twelve seconds to give up. Twelve seconds is too fast to blame a broken delivery truck; it means the instructions themselves were missing pages. The pages that matter: two special labels that say "this is raw material, not finished thought" and "the highest this note can claim is CANDIDATE." The working toy had both labels; the two broken ones had neither. The gate did exactly the right thing — it didn't pretend the broken toys were fine. The lesson: check for the labels at the start of the assembly line, not at the end — reject instruction sheets missing them before they're ever glued into the book.

## 🔵 GRANDMA NOTE

It's like a recipe contest where the judges taste the dish, check the kitchen was clean, and then ask a neighbor who's never cooked to follow the written recipe cold. Two dishes passed the tasting and the kitchen check, but the neighbor was stuck within seconds — the written recipes were missing the two most important notes ("this ingredient is raw, not cooked" and "this dish is a draft, not a final"). The judges were right to fail them, and nothing unworthy got a ribbon. The lesson: read every recipe at the front door and send back any that lack the two notes — don't wait until the neighbor is already standing in the kitchen. A related finding: a repair that claimed to add those notes turned out to be an empty envelope (a commit with zero files), and when the fix couldn't be delivered, the team didn't force it — they left the sealed repair in an envelope with instructions for whoever has the right key.

## 🟠 NAYA NOTE

Apply this when a multi-stage proof goes RED: (1) classify before you fix — run the differential: which stages passed identically, and where exactly did each RED diverge; (2) use timing as evidence — a ~12s failure at a comprehension step rules out transport/retry paths; (3) isolate by subtraction — same runtime-verify/lineage/content checks passing in one stage and the assert failing in the next names the comprehension asserts as the failing leg, without guessing; (4) move the check to the producer — authoring-side contract gaps get fail-fast validation at discovery (refuse with a named error like `CAPTURE_TRUTH_BOUNDARY_INVALID`) before persistence, never a late RED after the pipeline already spent its work; (5) keep the RED honest — a red-by-design proof stays RED until the named decision (backfill vs accept) is made by the owner, and nothing gets promoted through a narrowed gate; (6) verify a repair commit carries bytes — an empty commit (0 files) with a confident message is the SN-125 class; (7) when a 403 closes the push path, respect it as a hard boundary, don't retry through another API, and leave the artifact with the exact next action and the seat that can take it.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "authoring-side truth-boundary contract gap (missing machine_view fields in SN-020/021 captures; empty repair commit 443faed7; push-boundary 403)",
  "evidence": {
    "board": "#554 5945983977 (2026-10-02T05:11:00Z) — [NAYA 4][SELF-BUILD] Cycle 22:03 PDT: runs 36962391370 (SN-020, head 34610822) and 36966438981 (SN-021, head b7e0eeae) classified; fresh-lesson PASS, independent-verification PASS, cold-successor-held-out FAIL in ~12s at 'Cold retrieve this run's exact Smart Note from machine registry and canonical runtime'; 12s rules out curl-retry; comprehension asserts isolated; SN-019 (green) has machine_view.raw_source_separate_from_distillation=True, SN-020/021 field absent (None); gate fail-closed, both blocks persist CANDIDATE, nothing false promoted.",
    "guard": "fail-fast CAPTURE_TRUTH_BOUNDARY_INVALID validation in fresh-lesson 'Discover generalized Smart Note capture' step, local commit de2ac5b9, 7/7 controls green, GRAPH-10 stays 8.5/10.",
    "empty_commit": "443faed7 ('fix(smart-note): encode capture truth-boundary machine fields') is EMPTY (0 files) — the named encoding never landed.",
    "push_boundary": "no credential helper; Git Data API POST /git/trees and Contents API returned 403 'Resource not accessible by personal access token'; respected, not retried; patch left at ~/workspace/goals/nayapower-self-build-loop/hidden_files/selfbuild-20261001-2200-cold-gate-failfast.patch (26 insertions, applies at 25268675); next action: a seat with push rights applies as branch + draft PR."
  },
  "rule": [
    "classify the RED differentially (passed stages, exact divergence, timing as evidence) before fixing — one cause can explain multiple REDs",
    "fail fast at the authoring boundary: refuse captures missing truth-boundary fields at discovery, before any runtime commit",
    "a commit message is not evidence the change landed — verify bytes at the SHA (empty commits are the SN-125 class)",
    "a 403 on the push path is a hard boundary, not a retry prompt — leave the artifact with the named next action and the seat that owns it"
  ],
  "lesson_line": "Classify a RED differentially to find the single cause, then move the check to the producer: refuse truth-boundary-invalid captures at discovery before persistence, and never let a late RED or an empty commit stand in for evidence."
}
~~~
