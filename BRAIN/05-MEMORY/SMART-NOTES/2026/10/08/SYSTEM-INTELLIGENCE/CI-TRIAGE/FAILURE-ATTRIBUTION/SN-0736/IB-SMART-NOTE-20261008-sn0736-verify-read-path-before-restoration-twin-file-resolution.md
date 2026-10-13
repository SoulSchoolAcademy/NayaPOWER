# Verify the Read Path Before Queuing a Restoration — a Failing Integrity Test May Be Reading the Twin File

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0736-verify-read-path-before-restoration-twin-file-resolution
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6071897835 (brain-build battery, 2026-10-09T00:41:52Z — misdiagnosis) and #1354 comment 6072078875 (Naya 2 repair-verification receipts, 2026-10-09T00:59:02Z — correction); main tip 58bb427d

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The battery run classified `test_protected_intelligence_integrity` x3 REDs as a NEW class — "SN-0359 protected-intelligence HOLLOWING" — diagnosed the `.naya/protected-intelligence.json#/protected/1` skeleton (`stripped_by_1554` lists 7 governed fields, `requires_restoration_provenance: true`) as damage, and queued a restoration build-list item: recover last-good bytes from git history plus a v2 capture.

It was a misdiagnosis, and the mechanism is the lesson. Naya 2 re-verified on exact tip bytes: the canonical `SMART-NOTE-20261005-sn0359-proactive-captain.json` is **intact** (v2, `epistemic_state=CANDIDATE`, full ratification block, `restoration_provenance` present). All three REDs came solely from the test's id-indexed read resolving SN-0359 to a **hollow duplicate** — `ingest-20261008-repin-test-new-invariant.json` — confirming #1837's duplicate-ID-collision root cause byte-for-byte. The flagged "hollow" file was never the canonical artifact. Worse, the skeleton the battery called damage is intentional-by-law: `test_registry_documents_what_1554_stripped` **requires** it. The loop almost queued a restoration against a fixture.

Why this is brain-grade: integrity tests report an ID, not a file. An id-indexed lookup can resolve to any duplicate twin, so "the test says SN-0359 is hollow" is a claim about *the resolution*, not *the canonical artifact*. And "hollow" is not always damage — it can be a governed fixture the law demands. Queueing a restoration from a failing test without reproducing the read path is writing repair work against the wrong bytes. This is the *failure-attribution* half of the twin family: SN-0710 says verify the heal's ancestry before citing a commit; this says verify the test's read path before queueing a restoration.

Rule for a cold successor: **when an integrity test fails, the first question is which file the test's read path resolved the ID to.** Print the resolved path, compare it against the canonical registry entry, and check whether the flagged artifact is a fixture a test requires. Only when the canonical bytes are actually damaged does a restoration belong on the build list.

## 🩷 HUMAN NOTE

Shawn — a sharp one from tonight's battery run. The automated check flagged "protected intelligence SN-0359 is hollow" and queued a restoration job. Naya 2 checked and found the canonical file is completely intact — the test was reading a hollow *duplicate* file under the same ID, not the real one. The loop was one step from spending a build cycle restoring something that was never broken, against a skeleton file that a test *requires* to exist. New standing rule: before anyone queues a restoration from a failing integrity test, they must first prove which file the test actually read. The test names an ID; the ID can point at twins.

## 🟣 CHILD NOTE

Imagine a teacher marks "homework #5" as blank — but she graded the wrong student's paper. The real homework #5 is fine; she just picked up a blank copy from the pile because both had the same number on top. Now imagine someone wants to redo the whole homework because of the bad grade. The rule: before you redo anything, check *whose paper* the teacher was holding. That's the read path — which file with that number did the test actually read.

## 👵 GRANDMA NOTE

An automated checker said an important document was empty and asked for a rescue mission to rebuild it. A second checker looked closer and found the real document was perfectly fine — the first checker had picked up an empty *duplicate* with the same label. No rescue was needed; the alarm was pointing at the wrong copy. The lesson: when an alarm names a document, verify you're looking at the right copy of it before you rebuild anything. Labels can have twins too.

## 🟣 NAYA NOTE

A failing integrity test is a claim about an ID, not about the canonical bytes. I reproduce the read path first: resolve the ID exactly the way the failing test did, print the file it landed on, and diff that file against the canonical registry entry. If the resolved file is a duplicate twin, the repair belongs to the duplicate-ID class (here: #1837), never to a restoration queue. And before calling any "hollow" artifact damaged, I check the fixture contract — some skeletons are required by law (`test_registry_documents_what_1554_stripped`). Restorations are queued against proven canonical damage only, never against a read-path artifact.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0736",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION",
  "doctrine": "verify-read-path-before-restoration-twin-file-resolution",
  "rule": "When an integrity test fails, verify WHICH FILE the test's id-indexed read resolved to before queueing a restoration: print the resolved path, compare against the canonical registry entry, and check whether the flagged artifact is a required fixture. Restorations are queued against proven canonical damage only.",
  "failure_mode": "misdiagnosis queues a restoration against a fixture/duplicate; a build cycle is burned rebuilding bytes that were never damaged",
  "checks": [
    "reproduce the failing test's exact read path and print the resolved file path",
    "diff the resolved file against the canonical registry entry for that ID",
    "check the fixture contract (does any test require this 'hollow' artifact to exist?)"
  ],
  "cousins": ["SN-0710", "SN-0233", "SN-0341", "SN-0392", "SN-0420"],
  "evidence": [
    "#1354 comment 6071897835 (brain-build battery, 2026-10-09T00:41:52Z) — misdiagnosis: test_protected_intelligence_integrity x3 REDs classified as NEW class 'SN-0359 protected-intelligence HOLLOWING'; restoration queued ('last-good bytes from git history + a v2 capture'); tip 58bb427d",
    "#1354 comment 6072078875 (Naya 2 repair-verification receipts, 2026-10-09T00:59:02Z) — correction: canonical SMART-NOTE-20261005-sn0359-proactive-captain.json intact on tip (v2, epistemic_state=CANDIDATE, full ratification block, restoration_provenance present); all 3 REDs from id-indexed read resolving SN-0359 to hollow duplicate ingest-20261008-repin-test-new-invariant.json; stripped_by_1554 skeleton is intentional (test_registry_documents_what_1554_stripped requires it); build-list item flipped to blocked; #1837 confirmed as the owning lane"
  ]
}
