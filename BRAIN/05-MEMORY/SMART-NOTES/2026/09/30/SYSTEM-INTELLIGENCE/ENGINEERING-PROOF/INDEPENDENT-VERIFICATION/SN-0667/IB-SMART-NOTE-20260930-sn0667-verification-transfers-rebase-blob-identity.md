# Verification Transfers Across a Rebase When Blob SHAs Are Byte-Identical — Only the Parent Moved, So Only CI Needs a Re-Run

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0667-verification-transfers-rebase-blob-identity
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6055886931 ([NAYA 2][RELAY] — receipts on your three: #1854, the sweep correction, and #1840's rebase, 2026-10-08T08:27:24Z, item 3); #1354 6055771181 (#1840 byte-verified valid on exact tip — no second repair opened, 2026-10-08T19:47Z/08:19:47Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 byte-verified the #1840 repair (`tests/test_engineering_gates.py` sys.path fix + `tests/test_ci_declares_test_dependencies.py` guard-scope fix) at 20/20 on exact tip bytes `53217a40`, then stood down per one-repair-per-class (no second repair PR). When Naya 4 rebased the branch (`naya4/fix-engineering-gates-import-2026-10-08`: `2f6894d7` → `7fd4942c`), Naya 2 showed the prior verification **transfers**: both repair files are **blob-identical** across the rebase — `tests/test_ci_declares_test_dependencies.py` `e3d847a2…` and `tests/test_engineering_gates.py` `3b27970c…` at the old head and the new head. So the 20/20 evidence applies to the rebased commit unchanged; only the parent moved.

The rule: file-level evidence is bound to the **blob**, not the commit. When a rebase moves only the parent and every repaired file's blob SHA is identical before and after, the byte-verification is inherited — no re-verification of the file bytes is owed. What IS still owed is the CI re-run, because CI validates the commit (tree + parent + merge context), not the blobs. This is what lets seats rebase repairs onto a moving tip without burning a full evidence cycle every time: prove blob-equality (a cheap, exact comparison), inherit the evidence, and pay only the CI re-run.

## 🩷 HUMAN NOTE

Shawn — a small but useful proof-economics lesson from the #1840 repair this morning. Naya 2 had verified the repair 20-out-of-20 on the exact tip, then the branch got rebased onto the live tip. The question: does all that verification still count, or do we start over? Answer: it counts — because a rebase that changes nothing but the parent commit leaves the actual files byte-identical (same blob IDs). The evidence attaches to the file contents, not to the commit wrapper. So the rule now: if you can show the files are byte-identical before and after the rebase, the verification transfers — the only thing that still needs re-running is CI itself, since CI checks the whole commit. It saves the team from re-proving the same bytes every time the tip moves.

## 🟣 CHILD NOTE

Imagine a teacher grades your homework and it gets full marks. Then you put the same homework in a new folder — does the teacher need to grade it again? No — the pages are identical, only the folder changed. That's what a rebase is: same files, new wrapper. If the files are byte-for-byte identical (the computer can check this exactly with fingerprint codes), the old grade still counts. The one thing that does need a fresh check is the class computer's final stamp, because it stamps the whole folder, not just the pages.

## 👵 GRANDMA NOTE

Think of a certified repair report attached to a car. If the car gets a new license plate (a rebase), you don't re-inspect the engine — the engine hasn't changed, only the paperwork. The computer gives every file an exact fingerprint, so you can prove "the engine is identical" without looking again. The old inspection transfers. The only thing that needs repeating is the final road test, because that test is about the car-plus-paperwork together.

## 🧠 NAYA NOTE

Cold successor: when you rebase a repair branch onto a new tip and someone asks whether the earlier verification still stands, do not re-verify by default. Compare the blob SHA of every repaired file at the old head and the new head. If all are identical, state the transfer explicitly: "blob-identical across rebase (`<name>` `<sha7>…` at `<old>` and `<new>`); the <N>/<N> byte-verification on exact tip bytes applies to the rebased commit; only the parent moved." Then re-run CI only — CI validates the commit (tree + parent + merge context), not the blobs. If ANY blob differs, the transfer fails and the changed files are re-verified from scratch. This instance: #1354 6055886931 item 3 — `test_ci_declares_test_dependencies.py` `e3d847a2…` and `test_engineering_gates.py` `3b27970c…` identical at `2f6894d7` → `7fd4942c`; the 20/20 from #1354 6055771181 transferred, CI re-run owed and only that.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0667",
  "title": "Verification Transfers Across a Rebase When Blob SHAs Are Byte-Identical — Only the Parent Moved, So Only CI Needs a Re-Run",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"],
  "cousins": ["SN-0236", "SN-0429", "SN-0493"],
  "evidence": {
    "board": ["#1354 6055886931 ([NAYA 2][RELAY] — receipts on your three, 2026-10-08T08:27:24Z, item 3: verification transfers on blob-identity)", "#1354 6055771181 ([NAYA 2][BRAIN-BUILD TICK 08:16Z] #1840 byte-verified valid on exact tip, 2026-10-08T08:19:47Z)"],
    "byte_verification": "#1840 repair applied locally on pristine 53217a40: test_engineering_gates.py 17/17 with sys.path fix; both files applied 20/20 — exact-tip evidence, no second repair opened (one-repair-per-class)",
    "rebase": "naya4/fix-engineering-gates-import-2026-10-08: 2f6894d7 -> 7fd4942c onto live tip 53217a40",
    "blob_identity": "tests/test_ci_declares_test_dependencies.py e3d847a2... and tests/test_engineering_gates.py 3b27970c... identical at old head 2f6894d7 and new head 7fd4942c — only the parent moved"
  },
  "rule": "file-level evidence is bound to the blob, not the commit: if every repaired file's blob SHA is identical across a rebase, the byte-verification transfers and only the CI re-run is owed; if any blob differs, re-verify the changed files from scratch"
}
```
