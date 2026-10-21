# Fingerprint the Bytes Before You Prove Them — the Checkout Is an Instrument Too

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0533-fingerprint-the-bytes-before-you-prove-them
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6036650785 (2026-10-07T11:08:28Z — [NAYA 4 / SELF-BUILD LOOP][SIGN-IN + SIGN-OUT] Cycle #1703-MERGEVERIFY: independent post-merge verification of #1703, nine-node runtime binding, SoulSchoolAcademy).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Cycle #1703-MERGEVERIFY did not run its proof on a local checkout. It fetched the codeload tarball for the pin-exact tip `e7de7b88` and blob-verified **every file's size against the refs API** before executing a single test — and it stated why in the record: "no checkout corruption." The proof subject was then proven faithful: all 4 substantive file blobs byte-identical across PR head `c3e37ebf` → merge commit → tip `e7de7b88`, with zero drift from the 6 intermediate commits. Only after that fingerprinting did the battery run: `scripts/check-node-runtime-bindings.py` PASS (9/9 nodes), `tests/test_runtime_binding_behavior_contract.py` 2/2 PASS, the new CONNECT behavioral test 3/3 PASS under node --test.

The durable rule: **a verification battery executes on bytes, and bytes you have not fingerprinted against the canonical source are unknown bytes.** A local checkout or worktree is an instrument — and the instrument family (SN-0341: the harness lies about disk; SN-0428: the CI checkout lies about the tree; SN-0429: the branch pin lies about the tool) teaches that instruments corrupt silently. The repair is mechanical: pin the tip via the refs API, pull the codeload tarball at that exact SHA, verify file sizes (or blob SHAs) against the API, and only then run. Proof executed on unfingerprinted bytes is a claim about unknown bytes — cite it as such, or don't cite it.

## 🩷 HUMAN NOTE

Shawn — a quiet, load-bearing piece of craft from the #1703 post-merge verification. Before running any test, the cycle pulled the exact tip as a tarball straight from GitHub and checked every file's size against GitHub's own record — proving the code it was about to test was exactly the code at the tip, with no corruption from the download. Then it proved the merge itself was faithful (same bytes at PR head, merge commit, and tip) before running the real checks. The rule going forward: never trust a local copy of the code for verification — fingerprint it against the source of truth first. A test that runs on corrupted bytes proves nothing, and you'd never know.

## 🟣 CHILD NOTE

Imagine a teacher hands you an exam to grade, but the photocopy machine smudged some answers. If you grade the smudged copy, your grades describe the smudges, not the student. So first you hold the copy up against the original answer key, page by page, to prove it's a perfect copy — and *then* you grade. That's what happened here: before testing the code, we proved the downloaded code was a byte-perfect copy of the official version (checking every file's size against GitHub's records). Only then did the tests count. The rule: never grade the smudged copy — prove the copy is clean first.

## 👵 GRANDMA NOTE

Think of it like verifying a will before the reading. You don't just trust the copy the lawyer hands you — you check it against the sealed original in the vault, page by page, to make sure nothing was altered in the copying. We did exactly that with the code: before running any tests, we fetched the official copy from GitHub and verified every single file matched, byte for byte. Only then could the test results mean anything. The standing rule: test results are only as trustworthy as the code they ran on — so prove the code first.

## 💜 NAYA NOTE

Note to future me: whenever you run a verification battery — especially post-merge — the first step is not the tests, it is fingerprinting the subject. Pin the tip via the refs API (never trust a local ref), fetch the codeload tarball at that exact SHA, and verify every file size (or blob SHA) against the API before executing anything. Record the pin SHA and the verification in the sign-out; "ran on pin-exact fingerprinted bytes" is part of the evidence, not decoration. If you cannot fingerprint (no API access, odd artifact), say so explicitly and bound the claim — "proof ran on a local checkout, subject identity unverified." And on the merge-faithfulness half: prove the artifact's blob SHAs identical at PR head → merge commit → tip before citing post-merge results. A merge rewrites history; MERGED is not MERGED-VERIFIED (SN-0447), and verified-on-unknown-bytes is not verified.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0533",
  "rule": "fingerprint-bytes-before-proof",
  "statement": "Before executing a verification battery, fingerprint the exact bytes to be executed against the canonical source: pin the tip via the refs API, fetch the codeload tarball at that SHA, and verify file sizes or blob SHAs against the API. Proof run on unfingerprinted bytes is a claim about unknown bytes.",
  "corollaries": [
    "A local checkout/worktree is an instrument and instruments corrupt silently (family: SN-0341, SN-0428, SN-0429).",
    "Prove merge-faithfulness first: artifact blob SHAs identical at PR head, merge commit, and tip.",
    "Record the pin SHA and the fingerprint result in the sign-out as part of the evidence.",
    "When fingerprinting is impossible, bound the claim explicitly: subject identity unverified."
  ],
  "source": "#1354 6036650785 (2026-10-07) — cycle #1703-MERGEVERIFY, tip e7de7b88, PR #1703 head c3e37ebf"
}
```
