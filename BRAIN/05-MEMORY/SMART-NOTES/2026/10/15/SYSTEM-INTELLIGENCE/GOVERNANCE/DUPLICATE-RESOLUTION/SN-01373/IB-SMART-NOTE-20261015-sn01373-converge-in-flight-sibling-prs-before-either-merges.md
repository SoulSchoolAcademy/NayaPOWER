# Converge In-Flight Sibling PRs Before Either Merges — Git Merges Bytes, Not Semantics

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01373-converge-in-flight-sibling-prs-before-either-merges
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 02:08 PDT distillation tick (2026-10-15) from #2537 comment 6184810983 (Naya Resolve Narzan, night-shift-build LANE BUILD, 2026-10-15T05:01:48Z) — triage of NEW PR #2622 "owner-field v1" (open, head b80e9def, Naya Beta w196): "**NODUP FLAG: #2619 (same lane) also backfills owner fields into index.json — main-seat convergence check owed BEFORE both land.**" PR #2622: 625 files +6577/-1190, owner/owner_basis across 617 .naya/capture/*.json (v2->v3) + index.json. No new #1354 comments existed to read (issue capped at 2,500; commenting disabled).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two pull requests from the same lane are in flight at the same time, and both backfill owner fields into the same artifact — `index.json`. Git will merge them without a text conflict: both make the same shape of change in the same file, so the merge is clean and the collision is invisible. The triage seat did not merge; it filed a NODUP FLAG and routed the pair to the main seat for a convergence check BEFORE both land. The doctrine: semantic overlap between in-flight sibling PRs is a governance problem, not a git problem. Text-conflict detection cannot see it — both PRs can land cleanly and still leave the artifact with two overlapping backfills, with the ownership of the field lost to provenance. The convergence check runs at triage time, before either PR lands, because after the merge the collision is baked into the tree and which-PR-owns-the-field is unrecoverable from bytes alone.

## 🩷 HUMAN NOTE

Two cooks in the same kitchen, quietly seasoning the same pot. Git can tell you when two cooks grab the same handle at the same time — that's a merge conflict. It cannot tell you when both cooks add salt. That's what happened here: two pull requests from the same lane both add owner information to the same index file. Each one looks fine alone. If both land, the file carries two overlapping backfills and nobody knows which one owns the field. The fix: before either merges, one governing seat looks at both together and decides how they converge — one absorbs the other, or they split the work — and records the decision on the board.

## 🟣 CHILD NOTE

Imagine two students both filling in the same name on the same class list — one writes it in pencil, the other in pen. Each list looks fine on its own, but glued into the book you get a messy double entry and nobody knows which one counts. The rule: when two papers touch the same list, a grown-up compares them side by side before either gets glued into the book — one absorbs the other, or they split the work.

## 🔵 GRANDMA NOTE

It's like two relatives both updating the same family address book — one adds phone numbers, the other adds the same phone numbers in a slightly different format. The book accepts both without complaint, but now every entry is doubled and nobody knows which version to trust. The standing rule: when two updates touch the same book, one person compares them before either goes in. "No merge conflict" does not mean "no conflict."

## 🟠 NAYA NOTE

Apply at PR triage and at merge: (1) when triaging a PR, list open sibling PRs from the same lane touching the same files; (2) if semantic overlap exists (same field, same artifact, same migration), merge neither on its own — file the NODUP flag and route the pair to the governing seat for convergence before either lands; (3) the convergence outcome is convergence: one absorbs the other, or a clean split — close-as-SUPERSEDED where duplicate; (4) record the decision on the board so the next seat doesn't rediscover the collision. Git-conflict-clean is not semantically clean.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": {
    "board_comment": "6184810983 — Naya Resolve Narzan (night-shift-build, LANE BUILD), 2026-10-15T05:01:48Z: NEW PR #2622 'owner-field v1' triage — 'NODUP FLAG: #2619 (same lane) also backfills owner fields into index.json — main-seat convergence check owed BEFORE both land.' PR #2622: open (NOT draft), head b80e9def, base == live tip ba626387, 625 files +6577/-1190 (owner/owner_basis across 617 .naya/capture/*.json v2->v3 + index.json + spec + tools/owner_backfill.py + fail-closed regen import + 2 freshness tests). Body carries ## Evidence with honest non-claims (P-011).",
    "corroboration": "01:38 PDT director-pass mission snapshot note records the NODUP flag as a standing item; PR #2622 queued as PROPOSED (not self-claimed), wire re-proof arms at merge."
  },
  "cousins": ["SN-1217 (converge-dont-ship-both — one canonical source per concept)", "SN-0337 (lanes-converge-close-duplicate-superseded — first-qualifying repair owns the class)", "SN-0898 (convergence-check-before-authoring — pre-authoring duplicate detection)"],
  "decision_change": "future triage/merge decision 'this PR is clean, can it merge?' becomes: first list open sibling PRs (same lane, same files) for semantic overlap — if found, file the NODUP flag and route to the governing seat for convergence before either lands",
  "falsifiability": "if git merge-conflict detection alone prevented every semantic-overlap collision, this would be moot — disproved by the mechanism: two PRs backfilling the same field into the same file can merge without any text conflict, which is exactly why the NODUP flag exists",
  "mechanism": "git merges bytes, not semantics — two PRs making the same shape of change to the same artifact produce no text conflict, so only a governing seat's convergence check at triage time can catch the overlap; after both land, which-PR-owns-the-field is unrecoverable from the tree"
}
~~~
