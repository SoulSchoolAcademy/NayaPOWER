# SMART NOTE — A Push Receipt Is Not Proof of Contents: Verify the Tree

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-125` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn125-verify-the-tree-after-push` |
| Human title | A Push Receipt Is Not Proof of Contents: Verify the Tree |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING PROOF |
| Subtopic | INDEPENDENT VERIFICATION |
| Captured | 2026-10-02 01:45:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (evidence discipline — forever applicable) |
| Capture type | Process fix / Verifier discipline |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5943984072 — Naya 4's public correction: comment 5943868719 had reported the IB files at commit `6da736f4` on `naya4/hub-rooms-v1`. They were not there — the push-map extension silently did not apply, and the commit was reported without verifying tree contents. Re-pushed and verified file-by-file via the Git API; everything below exists at `0c9a25e0` (verified present). "Lesson re-learned: a push receipt is not proof of contents; verify the tree." |

---

## ✦ IN A NUTSHELL

**A successful push is not proof your files moved — only the remote tree is.** Naya 4 reported a commit SHA for a pushed pipeline demo; a later check showed the files were never in that tree — the push-map extension had silently not applied. The correction: re-push, then verify file-by-file through the Git API at the resulting commit before claiming anything exists anywhere. The discipline generalizes: push receipt ≠ tree contents; the commit announcement is a claim, the tree read is the proof. Verify after every push, every time, mechanically — because silent non-application looks exactly like success until you check.

---

## 🩷 HUMAN NOTE

Imagine mailing a package: the post office hands you a tracking number and a receipt. You tell a friend "the gift is on its way — tracking says delivered." Then the friend opens an empty mailbox. It turns out the clerk printed the label but the box never left the counter. From now on you don't trust the receipt — you ask the friend to open the box and read back what's inside. The push command is the post office; the commit SHA is the tracking number; the remote tree is the friend opening the box. Always ask the box.

---

## 🟣 CHILD NOTE

You tell your teacher "I turned in my homework!" because your backpack zipper felt like it closed. Then the teacher checks your folder — empty. The homework fell out on the playground. From then on, you don't say "it's turned in" because of how the zipper felt — you check the folder yourself. Same here: don't say the files are there because the push felt like it worked. Look at the actual folder on GitHub.

---

## 🔵 GRANDMA NOTE

There's an old habit worth keeping: trust, but verify. When someone tells you the check is in the mail, you wait for the envelope, not the promise of one. In the team's work, "I pushed it" is the promise; "I read the remote tree and the files are there" is the envelope. The correction on the board was a builder saying, plainly: I told you it was there, it wasn't, here's how I checked for real this time. That honesty plus the habit is what keeps the system honest.

---

## 🟠 NAYA NOTE

1. **There is a defect class here distinct from SN-050's.** SN-050 (verify the pushed bytes, not the pre-commit bytes) is about the *wrong bytes being verified* — pre-commit vs remote. This one is about *the push operation reporting success while silently not applying the change*: the push-map extension didn't apply, no error surfaced, and the commit SHA was announced as evidence of contents. The push receipt became a phantom citation token — a verifiable-looking claim pointing at nothing. Cold successors: a commit SHA proves a tree exists; it proves nothing about what that tree contains unless you read it.
2. **The repair protocol is mechanical: re-push, then read the tree via the API, file by file.** Not "check one file," not "the push output looked fine." Naya 4's repair enumerated every expected artifact (3 IBs, the README/contract, `ib-ingest.py`, `ib-feed-trigger.yml`, the spec, smart-tabs) against the tree at `0c9a25e0` before re-announcing. The protocol scales: the cost of a tree read is seconds; the cost of a phantom announcement is a downstream lane building on files that don't exist.
3. **Public correction is the evidence that the discipline works.** The error was owned on the board before anyone else could cite it — "my error, owned," with the exact mechanism (push-map extension silently not applying) named so others can recognize it. That is the correction culture (Orientation Brief §22/§34) applied to a tooling edge: name the silent failure mode, not just the fix.
4. **Watch for it wherever layers sit between you and the truth.** Push-map extensions, CI artifact uploads, deploy scripts, cached proxies — any layer that can report "done" without doing the thing is a candidate for this defect. The rule is position-independent: the claim is about the *destination's state*, so the evidence must be read from the *destination*.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn125-verify-the-tree-after-push",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Process fix",
  "rule": "a push receipt is not proof of contents — after every push, verify the remote tree via the API (file by file against the expected artifact list) at the resulting commit before announcing anything",
  "instance": {
    "announced": "IB files at 6da736f4 on naya4/hub-rooms-v1 (#554 comment 5943868719)",
    "actual": "files not in the tree — push-map extension silently did not apply",
    "repair": "re-pushed; verified every expected artifact file-by-file via the Git API at 0c9a25e0 before re-announcing",
    "quoted_discipline": "a push receipt is not proof of contents; verify the tree"
  },
  "defect_class": "silent non-application of a successful-looking operation — distinct from SN-050 (wrong bytes verified) and from push-trigger silence (SN-048/074)",
  "repair_protocol": ["re-push", "read the remote tree via the API at the new commit", "verify every expected artifact file-by-file", "then announce"],
  "generalization": "any layer that can report 'done' without doing the thing (deploy scripts, CI uploads, caches) needs destination-read evidence, not origin receipts",
  "family": ["SN-050 (verify the pushed bytes, not the pre-commit bytes)", "SN-062 (the count ledger is part of the change)", "SN-058 (adversarial implementation-fidelity audit — field-level fidelity at exact SHA)", "SN-100 (a mechanical change is still a change)"],
  "open": ["none — discipline is mechanical and fully specified"],
  "evidence": ["#554 comment 5943984072", "#554 comment 5943868719 (the superseded claim)"]
}
```

---

## 🔗 HOW IT CONNECTS

- **SN-050** (verify the pushed bytes, not the pre-commit bytes): sibling, not duplicate — SN-050 guards against verifying the wrong bytes; SN-125 guards against the push silently not applying at all. Both end at the same place: read the remote tree.
- **SN-058** (adversarial implementation-fidelity audit): same epistemology at a different layer — field-level fidelity at the exact SHA. SN-125 is the pre-audit precondition: make sure the SHA's tree holds the files before you audit them.
- **SN-042** (explicit supersession): the correction was published as a supersession of the earlier claim on the board — phantom claim withdrawn, verified state substituted, mechanism named. SN-125 is the discipline that would have prevented the claim; SN-042 is the protocol that repaired it.

---

*Truth state: CANDIDATE — auto-captured, not ratified. Only Shawn ratifies.*
