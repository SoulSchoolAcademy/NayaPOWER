# The Clobber Check — Byte-Compare a Regen-Bundled PR's Artifacts Against the Live Tip Before Claiming Its Delta

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0645-clobber-check-regen-bundle-delta
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6050774832 ([NAYA 4][SELF-BUILD] SIGN IN — #1803 tip-verification, 2026-10-08T02:13:41Z) and 6050776671 ([NAYA 4][SELF-BUILD] SIGN OUT — #1803 tip-verification COMPLETE, 2026-10-08T02:13:51Z); PR #1803 (`drive-loop` lane, head `dff1cf02`) verified at live tip `77e86701` — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two lanes independently regenerated the same brain-index artifacts at adjacent tips: the drive loop merged #1804 (index regen at `8337f9d9` → tip `77e86701`), while the repair PR #1803 also carried 3 regenerated brain-index blobs plus its capture repair. When Naya 4 independently verified #1803 at the live tip, the first step was not re-running the tests — it was a **clobber check**: byte-compare the PR's regenerated blobs against the live tip's already-merged copies. All 3 blobs were byte-identical. Conclusion: #1803's index half was a no-op against the live tip; its *effective delta* was the capture repair only (+52/-0, purely additive) — and "mergeable: clean" was therefore an accurate claim, not an optimistic one.

Then the RED reproduction ran on a pin-exact tip tree (the 92 files the audit reads, fetched at the pin): tip-as-is **fails** `test_live_repository_drift_never_grows_per_class` (`captures_missing_intelligence: 1`, exactly `20261008-sn0530-do-do-and-report.json` — a non-vacuous RED, one missing capture, not an environment artifact). With #1803's repaired capture substituted: **12/12 pass**, all 10 classes ≤ pins. Verdict recorded: #1803 is a SAFE HEAL for the only kernel RED — PR-introduced defect (#1801), the tripwire firing correctly, no second RED behind it on this surface.

The doctrine, stated as a rule: **before merging (or re-verifying) any PR that bundles a regenerated artifact with a repair, byte-compare the PR's regenerated blobs against the live tip's copies — the clobber check.** If identical, the regen half is a no-op and the effective delta is the repair alone; score and merge the repair, not the bundle. If they differ, the regen races the tip and the PR needs re-anchoring (SN-0493). Either way, the claimed delta is measured, not asserted. This is the BYTE-IDENTICAL family (SN-0178, byte-identical landing = stand down) applied to the *verification* side of a regen, and SN-0493's "decision expires when the tip moves" operationalized as a mechanical step: the check is meaningless against a stale tip, so it runs at the pin-exact live tip, every time.

## 🩷 HUMAN NOTE

Shawn — one verification trick worth banking from tonight's self-build loop: a repair PR carried both a regenerated brain index *and* a capture fix, but another lane had already merged an identical index regen at the live tip. Instead of trusting the diff, the verifying lane byte-compared the PR's regenerated files against the live tip's copies — identical, so the index half was a no-op and the real change was just the +52-line capture fix. Then it proved the failure on the exact live tip (one missing capture, a real red, not a fluke) and proved the fix closes it 12-for-12. The rule now written down: whenever a PR bundles a regenerated file with a repair, compare the regenerated files byte-for-byte against the live tip first — measure the real delta, don't just read the diff. It takes seconds and kills an entire class of merge surprises.

## 👶 CHILD NOTE

Imagine two kids both draw the same picture for the classroom wall, and the teacher already hung one up. The second kid hands in hers — plus a brand-new drawing of her own. Before hanging it, a smart helper holds the two pictures side by side: the classroom pictures are exactly the same, so that part changes nothing — only the brand-new drawing is really new. Now the helper knows exactly what she's approving: one new drawing, not two. Always compare first, so you never hang the same picture twice.

## 👵 GRANDMA NOTE

Dear, this is about knowing what you're really signing off on. When someone brings you a folder with two things in it — a copy of something already on the shelf, plus a genuine fix — don't just stamp the folder. Hold the copy next to the shelf copy and check: if they're identical, the copy changes nothing, and your stamp only covers the fix. And always check against *today's* shelf, not yesterday's, because the shelf moves. A minute of comparing saves you from approving work that's already been done — or worse, from a copy that quietly replaced something new.

## 🧠 NAYA NOTE

Cold successor: the clobber check is a mandatory step in the independent-verification of any regen-bundled PR. Procedure: (1) identify the regenerated artifacts in the PR (brain-index blobs, registry files, any machine-regenerated layer); (2) fetch their live-tip counterparts at the pin-exact tip — never from your worktree, never from a stale checkout (SN-0233); (3) byte-compare (`sha256` of blob bytes — content identity, not diff hunks); (4) if identical, declare the regen half a no-op and scope the effective delta to the remainder; re-run the claim ("mergeable: clean") against the scoped delta; (5) if they differ, the PR's regen is stale relative to the tip — re-anchor before any verdict (SN-0493). Then, and only then, run the RED reproduction on the pin-exact tip tree: tip-as-is must FAIL non-vacuously (name the exact missing artifact, not a class), and tip-with-repair-substituted must pass the full battery. Both halves are required — the clobber check scopes *what* the PR changes; the substitution test proves the change *heals*. Read-only throughout: the verifying lane never pushes to the PR branch. Cite in the receipt: blob shas compared, tip SHA, RED class, substitution result.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0645",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/PUSHED-BYTES-VERIFICATION",
  "doctrine": "The clobber check: before merging or re-verifying a PR that bundles a regenerated artifact with a repair, byte-compare the PR's regenerated blobs against the live tip's copies at the pin-exact tip. Identical = regen half is a no-op; the effective delta is the repair alone. Different = regen is stale vs the tip; re-anchor before any verdict.",
  "family": "BYTE-IDENTICAL (SN-0178 local-green-vs-byte-identical-CI-green; byte-identical landing = stand down) + SN-0493 (decision expires when tip moves) + SN-0233 (verify on virgin state) + SN-0429 (instrument parity)",
  "evidence": [
    "#1354 comment 6050776671 (2026-10-08T02:13:51Z): #1803's 3 brain-index blobs byte-identical to live tip's merged #1804 regen → index half a no-op; effective delta = capture repair only (+52/-0, additive); 'mergeable: clean' accurate",
    "#1354 comment 6050776671: pin-exact tip tree (92 files) — tip-as-is FAILS test_live_repository_drift_never_grows_per_class (captures_missing_intelligence: 1, exactly 20261008-sn0530-do-do-and-report.json); with repaired capture substituted: 12/12 pass, all 10 classes ≤ pins",
    "PR #1803 open (head dff1cf02), live tip 77e86701; merge decision parked for Shawn (protected gate)",
    "Classification: PR-introduced RED (#1801), tripwire firing correctly, no second RED behind it on this surface"
  ],
  "falsifiers": [
    "Approving a regen-bundled PR's delta from the diff without byte-comparing regenerated artifacts to the live tip",
    "Running the clobber check against a stale or worktree copy instead of the pin-exact live tip",
    "Citing a run-level pass as the heal proof without the non-vacuous tip-as-is RED reproduction"
  ],
  "applies_to": "independent verification of any PR bundling regenerated artifacts (brain index, registry, sequence policy) with a repair; kernel-RED heal classification"
}
```
