# A Verification Verdict Re-Anchors Transitorily When the Blob SHA Is Unchanged

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0727-content-addressed-verdict-reanchor
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6070860613 ([NAYA 4][SELF-BUILD LOOP — SIGN-OUT], 2026-10-08T23:30Z) — SoulSchoolAcademy. Key recorded evidence: "Tip `.naya/memory/smart-notes/index.json` blob `8dd3449b…` byte-identical at both tips → the 21 broken links are still on main; heal still needed. PR-head blob `6ec5b344…` byte-identical to the 20:03-verified repair → the 'exactly the 21 repaired entries differ' result re-anchors transitively by content-addressing."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The self-build loop's 16:30 PDT cycle faced a moved tip (78661f59 → 58bb427d, 8 commits) with a merge-safety claim made at the old tip. Instead of re-running the full verification battery, it proved content-addressed continuity: the tip's `index.json` blob SHA `8dd3449b…` was **byte-identical at both tips**, and the PR-head repair blob `6ec5b344…` was byte-identical to the repair verified at 20:03Z. A blob SHA is a content fingerprint — identical SHA means identical bytes. So the 20:03 verdict re-anchored **transitively**, without re-running: the "21 broken links still on main" conclusion holds because the file it was proven on is the same file, and the "exactly the 21 repaired entries differ" result holds because the repair is the same bytes.

Why this is brain-grade: SN-0493 says a decision expires when the tip moves — correct, but expensive if taken literally, because it forces full re-verification for every tip move even when nothing relevant changed. This note gives the disciplined exception: a decision expires when the tip moves **and** the evidence's subject bytes moved. If the subject blob's SHA is identical at both tips, the verdict transfers by content-addressing — this is not re-use of a stale decision, it is the same decision on the same bytes. The check is mechanical (compare blob SHAs at both tips) and the bar is strict: it only works when you can name the exact blob the verdict was computed on, and the SHA matches.

Rule for a cold successor: **before re-running a verification on a moved tip, check whether the verdict's subject blob is byte-identical at both tips.** If the SHA matches, the verdict re-anchors transitively — cite both SHAs. If it doesn't match, the verdict expired and you re-verify. This is the precision instrument for SN-0493, not an exception to it.

## 🩷 HUMAN NOTE

Shawn — a verification efficiency lesson from the self-build loop tonight. A merge-safety claim had been proven at one tip, then the tip moved 8 commits. Instead of re-running the whole battery, the loop proved by content fingerprint that the exact files the claim was about were byte-identical at both tips — so the proven claim carries over without re-running. The standing rule: when the tip moves, you only have to re-verify what actually changed; a file that's identical byte-for-byte doesn't need to be re-proven. It's the precision version of "re-verify on tip move" — same honesty, less wasted work.

## 🟣 CHILD NOTE

Imagine the teacher graded your math test, then you moved to a different classroom — but the test paper itself didn't change one letter. Would you need to be re-graded? No: the same paper means the same grade. The trick is proving it's really the same paper: every paper gets a fingerprint number, and if the fingerprint matches, it's the same paper. But if even one letter changed, the fingerprint changes too — and then you do get re-graded. Same rule for code: same bytes, same verdict.

## 👵 GRANDMA NOTE

A safety check on some work was completed, then the project moved forward a few steps. Rather than redoing the entire check, the worker proved by comparing digital fingerprints that the exact files the check covered were unchanged — letter for letter identical. Since nothing changed in what was checked, the check's result still counts. The rule: you only re-check what actually changed; identical files keep their proven results.

## 🟠 NAYA NOTE

Make this mechanical in any tip-currency loop: (1) when a verdict was proven at tip T1 and the tip is now T2, identify the exact blob(s) the verdict was computed on; (2) compare the blob SHAs at T1 and T2 — identical SHA means identical bytes, and the verdict re-anchors transitively; (3) cite both SHAs in the receipt; (4) if the SHA differs, the verdict expired per SN-0493 — re-verify, don't transfer. Never transfer a verdict without naming the blob and matching its SHA.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0727",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/MERGE-BOUNDARY",
  "doctrine": "content-addressed-transitive-reanchor",
  "rule": "A verification verdict proven at tip T1 re-anchors transitively at tip T2 iff the exact blob(s) it was computed on have identical SHAs at both tips. Same bytes = same verdict, cited with both SHAs. Differing SHA = verdict expired, re-verify.",
  "failure_mode": "re-running full batteries for every tip move (waste), or transferring verdicts without SHA proof (stale decisions dressed as currency)",
  "checks": [
    "name the exact blob the verdict was computed on",
    "compare blob SHA at old tip vs new tip",
    "SHA match: re-anchor with both SHAs cited; SHA mismatch: full re-verification"
  ],
  "cousins": ["SN-0493", "SN-0440", "SN-0668", "SN-0692"],
  "evidence": [
    "#1354 comment 6070860613 (Naya 4 self-build sign-out, 2026-10-08T23:30Z): tip `.naya/memory/smart-notes/index.json` blob 8dd3449b byte-identical at tips 78661f59 and 58bb427d — 21-broken-links verdict holds transitively; PR-head repair blob 6ec5b344 byte-identical to 20:03-verified repair — 'exactly the 21 repaired entries differ' re-anchored transitively by content-addressing"
  ]
}
