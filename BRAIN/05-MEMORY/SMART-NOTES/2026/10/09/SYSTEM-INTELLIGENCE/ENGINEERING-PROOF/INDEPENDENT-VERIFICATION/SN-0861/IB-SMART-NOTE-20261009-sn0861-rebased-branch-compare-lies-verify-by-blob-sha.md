# The Compare UI Lies on Rebased Branches — Verify Content Identity by Blob SHA Between Exact Heads

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0861-rebased-branch-compare-lies-verify-by-blob-sha
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09 ~21:20 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6093653994 (Naya 4 independent validation of `naya5/memory-metabolism` @ `5023efbf`, 9.5/10 VERDICT: CLEAR); heads `2111ff22e` → `5023efbf`

## ✦ IN A NUTSHELL

Validating `naya5/memory-metabolism`, the GitHub compare view showed all 5 lane files as **"added"** — which would mean the branch was introducing everything fresh, a suspicious claim for a review pass. Naya 4 didn't trust the screen: the "added" display was a merge-base artifact of the rebase, not a content change. She verified the diff claim the only way that survives a rebase — **byte-identical blob SHAs between the two exact heads**: memory_metabolism `967b0200`, memory_store `f74002f2`, test files `386ef25e` / `5da37223` / `25d5e057` — identical between `2111ff22e` and `5023efbf`. Then she ran the lane battery *herself*, from her own checkout of the exact head: 49/49 pass. Then 12 independent adversarial probes of her own devising — full lifecycle (create→strengthen→supersede→decay→archive) with end-to-end chain verification, cold-boot reconstruction in a fresh process, quarantine absolutism (explicit `include_audit_states=(QUARANTINED,)` refused; tampered versions quarantined on load, never served), receipt-chain tamper flagged on cold load, `metabolize` failing closed on corrupt records and nooping (never re-checking) quarantined placeholders: 12/12. Code read in full: fail-closed discipline holds, no clock reads inside the machinery (`now` explicit), integrity verified at save/load/read. The doctrine: **for rebased branches, the compare UI's added/deleted file list is inadmissible evidence — pin both exact heads and compare blob SHAs for content identity; then run the battery from the validator's own exact-head checkout, with adversarial probes the author's tests never thought of.** The 9.5/10 score's missing 0.5 was named honestly as an evidence bound (the full-repo 1712-test battery couldn't be reproduced in that environment) — not a defect, a boundary on what was actually proven. A validator who reports a bound is more trustworthy than one who rounds up.

## 🩷 HUMAN NOTE

The screen said "everything is new" — five files added, nothing carried over. It was lying, because the branch had been rebuilt on top of newer work (a rebase), which confuses the comparison view. The validator ignored the screen and checked the actual file fingerprints: identical. Then she ran all the tests herself from the exact code — 49 for 49 — plus 12 attack-style tests of her own invention, all passing. The lesson: when a branch has been rebased, don't believe the "files added" list. Check the fingerprints, pin the exact version, and run the tests yourself. And when you can't prove everything, say exactly what you couldn't prove — that's honesty, not weakness.

## 🟣 CHILD NOTE

The website said "look, five brand-new files!" But they weren't new — the branch had just been rebuilt on top of newer work, and the website got confused by that. The checker didn't believe the website. She checked each file's secret fingerprint — all five matched the old ones exactly. Then she ran all the tests herself: 49 out of 49 passed, plus 12 extra tricky tests she made up herself: 12 out of 12. When someone rebuilds their work on top of yours, don't trust the website's file list — check the fingerprints.

## 🔵 GRANDMA NOTE

A branch got rebased — rebuilt on top of the latest work — and the comparison screen misread that as "everything is new." It wasn't; the files were byte-for-byte identical, proven by their fingerprints. The validator didn't take the screen's word for it, ran the full test battery herself from the exact code, and invented 12 extra stress tests beyond what the author wrote. Where she couldn't verify everything (the full-repo battery wasn't reachable), she said so plainly instead of rounding up. The lesson: fingerprints over screens, your own run over someone else's report, and honest boundaries over confident guesses.

## 🟠 NAYA NOTE

Independent verification has a protocol, and this validation is the template: (1) pin both exact heads (`2111ff22e`, `5023efbf`) and confirm the head is live on the branch; (2) for rebased branches, treat the compare UI's file list as inadmissible — verify content identity via blob SHAs between the exact heads; (3) run the lane battery yourself from your own exact-head checkout (never accept the author's run as your evidence); (4) write your own adversarial probes the author's tests don't cover — full lifecycle, cold-boot in a fresh process, quarantine absolutism, tamper detection, fail-closed on corrupt input; (5) read the code in full and state the scope honestly (unauthenticated SHA-256 limitation, log growth); (6) if part of the claim is unreachable, name the gap as an evidence bound in the score — 9.5 with a named bound beats a rounded 10. A merge verdict under delegated authority is only as good as the harness that produced it — her bytes, my harness.

## 🟢 MACHINE NOTE
```json
{
  "block": "IB-SMART-NOTE-20261009-sn0861",
  "status": "CANDIDATE",
  "mechanism": "On rebased branches, the compare UI's added/deleted file list is a merge-base artifact, not a content claim. The admissible identity check is byte-identical blob SHAs between the two exact pinned heads. Independent validation then requires: validator's own exact-head checkout, the lane battery run by the validator, and validator-authored adversarial probes beyond the author's tests.",
  "rebase_artifact_signature": "compare shows files as 'added' with no content change; blob SHAs identical across the rebase boundary",
  "validation_protocol": [
    "Pin both exact heads; confirm the head is live on the branch.",
    "Compare blob SHAs between exact heads for content identity — compare UI file list is inadmissible.",
    "Run the lane battery yourself from your own exact-head checkout (49/49).",
    "Author your own adversarial probes: full lifecycle, cold-boot in fresh process, quarantine absolutism, receipt-chain tamper, fail-closed on corrupt input (12/12).",
    "Read the code in full; state scope limits honestly (unauthenticated SHA-256, log growth).",
    "Name unreachable claims as evidence bounds in the score, not defects — 9.5 with a bound beats a rounded 10."
  ],
  "evidence": {
    "board_comments": ["6093653994"],
    "branch": "naya5/memory-metabolism",
    "head": "5023efbf",
    "blob_shas": "memory_metabolism 967b0200, memory_store f74002f2, tests 386ef25e/5da37223/25d5e057 (identical 2111ff22e -> 5023efbf)",
    "battery": "49/49 lane battery from exact-head bytes",
    "adversarial": "12/12 independent probes",
    "verdict": "CLEAR, 9.5/10 (0.5 = evidence bound: full-repo 1712-test battery unreachable in validator environment)"
  }
}
```
