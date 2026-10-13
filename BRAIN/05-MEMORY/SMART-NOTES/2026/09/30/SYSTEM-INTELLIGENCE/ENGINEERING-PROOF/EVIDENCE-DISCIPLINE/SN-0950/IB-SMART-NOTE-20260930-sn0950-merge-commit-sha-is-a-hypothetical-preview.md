# The API's merge_commit_sha Is a Hypothetical Preview — Only merged=true ∧ merged_at Proves the Landing

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0950-merge-commit-sha-is-a-hypothetical-preview
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Night-shift t2302-a receipt (2026-10-10 23:03–23:10 PDT, VERIFY ONLY); PR #2286 PRs API payload (merge_commit_sha=9e31c499c6efedb5cfe27caceac0ed826745fe1c with merged=false, merged_at=null); #2175 wire-lane sign-outs 6105870609/6105894441.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t2302-a worker's verify-only run on PR #2286 (title: "Ratify THE NAYA PROTOCOL: combined ultimate text") pulled the PR object from the API and found a trap field: `merge_commit_sha` = `9e31c499c6efedb5cfe27caceac0ed826745fe1c`. It looks like a merge happened. None did — `state=open`, `merged=false`, `merged_at=null`, head `a9528985af388be0498fd6c5ca676e20b24330d6`. The worker named it precisely: GitHub's `merge_commit_sha` is a **hypothetical test-merge preview** computed for the API's own mergeability check, not a historical record. Anyone (or any tool) that reads that field as "the PR merged at this SHA" invents a landing. The doctrine this note banks: **a landing is proven only by `merged=true` AND `merged_at` non-null — the timestamp is the event, the SHA alone is a hypothesis.** `merge_commit_sha` on an open PR answers "what WOULD the merge commit look like"; `merged_at` answers "when did it happen." Mixing them is how a seat could claim ratified text landed on main when it still exists only on the PR branch — exactly the failure that t2302-a's verify-only constraint was designed to prevent (the gate to close superseded PR #2284 required #2286 *merged*, not *previewable*). A cold Naya auditing merges months from now: read all three fields, never trust `merge_commit_sha` alone; treat any automation that consumes that field as a suspect until it also asserts `merged=true ∧ merged_at≠null`.

Why this is brain-grade: it is a permanent evidence-class fix, not a PR-#2286 fact. GitHub keeps this field shape forever. The trap is structural: the field name claims "merge commit," and busy readers (and tired scripts) believe field names. It pairs with SN-0328 (re-verify on the real merge commit, because pre-merge evidence doesn't transfer) — SN-0328 answers "what do you check after a landing," this answers "how do you know a landing happened at all." And with SN-0563 (PR head ≠ merge commit, prove by ancestry): all three guard the same boundary from different sides — what merged, what the merge contained, what the merge proves.

## 🩷 HUMAN NOTE

Shawn — last night a verification worker nearly had a dangerous misread handed to it on a plate. PR #2286 (the ratified protocol text) is still open, still unmerged — Naya 2's cross-seat review hasn't arrived yet, so the merge gate hasn't fired. But the API payload carries a field called `merge_commit_sha` with a real-looking SHA in it. The worker caught it: that field is a hypothetical preview GitHub computes to test mergeability, not proof of a merge. The rule banked: only `merged=true` PLUS a non-null `merged_at` timestamp proves a landing. The SHA alone is a hypothesis. This matters because the supersede-closure of the older protocol PR (#2284) was gated on #2286 being *actually merged* — a worker that trusted the preview field would have closed the wrong PR tonight. The trap is in the field name itself, and it will still be there for a cold Naya months from now.

## 🟣 CHILD NOTE

Imagine a movie trailer for a film that hasn't been made yet. The trailer shows scenes, music, a title — it looks real. But the movie hasn't started filming. GitHub's `merge_commit_sha` is like that trailer: it shows you what the merge *would* look like, but the movie isn't made. The real proof is two things: a ticket stub that says "merged: yes" AND the date printed on it. Trailer alone = no movie. Always ask for the stub and the date.

## 👵 GRANDMA NOTE

A young couple comes home excited: "We have a wedding date!" — and show you the date printed on a sample invitation they made up. That's the preview. The marriage certificate and the stamp from the courthouse — those are the real thing. GitHub's merge_commit_sha is the sample invitation: it tells you what the date *would* look like. The certificate is `merged=true` with a real date in `merged_at`. Never congratulate the couple on the sample. Check the certificate.

## 💜 NAYA NOTE

Future Naya: (1) When reading the pulls API to establish whether a PR merged, require the conjunction `merged=true ∧ merged_at≠null`. `merge_commit_sha` alone proves nothing — on an open PR it is the test-merge preview (`9e31c499…` on open #2286 is the instance that named this class). (2) Audit any lane tooling that consumes `merge_commit_sha`: if it doesn't also assert `merged=true` and a non-null `merged_at`, it is a suspect — this is exactly the field a merge-gate automation would read wrong and close the wrong PR. (3) In receipts, quote all three fields when the claim is "PR merged" (state, merged, merged_at, merge_commit_sha) so a cold reader can re-derive your conclusion. (4) Pair with SN-0328 (after a proven landing, re-verify derived artifacts on the *actual* merge commit) and SN-0563 (PR head ≠ merge commit, prove by ancestry). Evidence anchors: t2302-a receipt §1 (23:03–23:10 PDT 2026-10-10, tip `57e935c1` re-verified via ls-remote); PR #2286 head `a9528985…e20b24330d6`, reviews=0; supersede-closure of #2284 correctly held (t2302-b, Path B) because the gate read the right fields.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0950",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "EVIDENCE-DISCIPLINE"],
  "cousins": ["SN-0328", "SN-0563", "SN-0949"],
  "rule": "A PR landing is proven only by merged=true AND merged_at non-null. The pulls API's merge_commit_sha on an open PR is GitHub's hypothetical test-merge preview — what the merge WOULD look like — not a historical record. Never assert a landing from merge_commit_sha alone; audit any tooling that consumes it.",
  "anti_rule": "Trusting the field name; claiming a PR merged because merge_commit_sha is populated; gating a supersede-closure on a preview SHA instead of the merged flag and timestamp.",
  "evidence": {
    "run": "t2302-a, 2026-10-10 23:03–23:10 PDT, VERIFY ONLY, tip 57e935c1 re-verified via git protocol",
    "pr": "#2286 state=open merged=false merged_at=null, merge_commit_sha=9e31c499c6efedb5cfe27caceac0ed826745fe1c, head a9528985, reviews=0",
    "gate_effect": "t2302-b correctly held the #2284 supersede-closure (Path B) because the gate read merged=false, not the preview SHA",
    "provenance": "#2175 wire-lane sign-outs 6105870609/6105894441 thread"
  },
  "authority": "observed field execution — Naya 4 night-shift verification lane, CANDIDATE (auto-capture, not ratified)"
}
```
