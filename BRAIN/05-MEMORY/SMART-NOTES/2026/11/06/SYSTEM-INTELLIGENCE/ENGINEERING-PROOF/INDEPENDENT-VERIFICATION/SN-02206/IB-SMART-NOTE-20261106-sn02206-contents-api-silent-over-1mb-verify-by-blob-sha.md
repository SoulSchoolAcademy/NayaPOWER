# INTELLIGENT BLOCK — SN-2206

**Intelligent Block:** IB-SMART-NOTE-20261106-sn02206-contents-api-silent-over-1mb-verify-by-blob-sha
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Director tick 2026-11-05 19:38 PST (executed 2026-11-06T03:49Z, memory log ~/memory/2026-11-05.md): the ledger sync script's first 'UNVERIFIED' verdicts on the two >1MB ledger files (ACTIVITY-LEDGER.md, activity-ledger.jsonl) were a verification-method artifact — the contents API returns empty content for files >1MB, so byte-compare always fails; re-checked by git blob SHA, both MATCH (bd0a174f, e6436f30). Corroborated the same day by the smart-link reverify, which used raw download_url because the contents API returns empty content for the 1.4 MB index (hidden_files/smart-link-reverify-2026-11-05.md), and by the 716fa2bf index read (1,408,974 B; 'contents API returns encoding none over 1MB'). Number census at live tip 9004ce29 (git protocol, local mirror): SN-2206 absent from main-tree paths, branch tree, and registry index .naya/memory/smart-notes/index.json (1,246 entries; 0 'contents', 0 '1MB', 0 'empty content'; the 9 blob-SHA hits are about rebase/compare identity, not the API limit); lessons.jsonl carries no contents-API note (its one 'blob' hit is quota-attribution). Branch head 03fcc466 (SN-2205); counter ends at 2205; open PRs #3256, #3255, #3254, #3178, #3089 claim no SN file (file lists checked via App route this tick); #2416 closed unmerged since 2026-10-21; #1354 capped at 2,500, commenting disabled.

## ✦ IN A NUTSHELL

The GitHub contents API returns empty content for files over about 1MB — so a verify step that fetches a big file through that API and byte-compares the result is comparing the local bytes against nothing, and it fails no matter how correct the file is. The ledger sync learned this the loud way: two good >1MB ledger files were first reported UNVERIFIED, then re-checked by git blob SHA and found to MATCH. The verdict indicted the API, not the file. The rule: for any file over 1MB, verify by git blob SHA (or raw download_url) — never by contents-API byte-compare.

## 🩷 HUMAN NOTE

Shawn — when the team checks that a file landed correctly on GitHub, the usual way is to ask GitHub for the file and compare it byte for byte with the local copy. That works until the file is bigger than about 1MB: above that size GitHub's contents API hands back an empty file, so the comparison fails even when the file is perfect. Tonight the ledger sync called two big ledger files UNVERIFIED for exactly that reason, then re-checked them a different way — by their content hash — and both matched. The fix is simple: big files get verified by their hash, never by asking the API for their bytes.

## 🟣 CHILD NOTE

Imagine you want to check that your homework made it into the teacher's folder exactly right. You ask the teacher's helper to read it back to you — but the helper refuses to read anything longer than one page, and just hands you a blank sheet instead. You compare your homework to the blank sheet, they don't match, and you shout that the homework is wrong — but the homework was fine all along; the helper just wouldn't read it. The rule is: for long homework, don't ask the helper to read it. Compare the fingerprints instead — if the fingerprints match, the homework is right.

## 🔵 GRANDMA NOTE

Dear, it is like asking the post office to read back a long letter to check it arrived safely — but the post office only reads short notes, and for a long letter it just sends you back an empty envelope. You compare your letter to the empty envelope, they don't match, and you think the letter was lost — but the letter arrived perfectly fine; the post office simply wouldn't read it back. The lesson: for long letters, don't ask for a read-back. Compare the wax seals instead — if the seals match, the letter is the one you sent.

## 🟠 NAYA NOTE

For every seat that verifies a pushed file: (1) never byte-compare a file over 1MB through the contents API — the API returns empty content above ~1MB (encoding none), so the comparison fails on a correct file and the verdict is a false negative manufactured by the method; (2) verify big files by git blob SHA — compare the content-addressed hash of the object itself, which has no size truncation — or fetch the bytes through raw download_url; (3) when a verify step reports UNVERIFIED, check the method before the file: if the fetched content came back empty and the file is over 1MB, the verdict says nothing about the file — re-verify by blob SHA before reporting anything; (4) the ledger sync script's verify step now uses the blob-sha method for big files — any new verify step must do the same; (5) a verification verdict is only as good as the transport that produced it — a method that cannot see the file cannot judge it.

## 🟢 MACHINE NOTE

```json
{
  "slug": "contents-api-silent-over-1mb-verify-by-blob-sha",
  "sn": "SN-2206",
  "title": "The Contents API Goes Silent Over 1MB — Verify Big Files by Blob SHA",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-06",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["verification", "github-api", "large-file"],
  "enforcement": "Any verify step that byte-compares a file over 1MB must use git blob SHA (or raw download_url) — the ledger sync script's verify step uses the blob-sha method for big files; a contents-API byte-compare on a >1MB file is refused as a verification method. Regression check: verify a known-good >1MB file both ways and assert the contents API returns empty content while the blob SHA matches.",
  "falsifier": "A >1MB file whose contents-API call returns full content and byte-compares successfully would prove the limit is not what this note claims (or that the API changed) and collapse this note. A contents-API byte-compare on a >1MB file returning UNVERIFIED while the blob SHA matches confirms the mechanism.",
  "decision_changed": "Which verification method a sync or verify script uses for a file over 1MB: git blob SHA (or raw download_url) instead of contents-API byte-compare — so a good big file is never again reported UNVERIFIED by the check itself.",
  "mechanism": "The contents API returns empty content (encoding none) for files above ~1MB. A verify step that fetches the file through that API and byte-compares the result is comparing the local bytes against nothing — the comparison fails no matter how correct the file is. The failure is a property of the transport, not the artifact, so the verdict 'UNVERIFIED' is a false negative manufactured by the method. Git blob SHA compares the content-addressed hash of the object itself, with no size truncation; raw download_url streams the bytes directly. Either method reads the real file, so either verdict means something about the file.",
  "provenance": "Director tick 2026-11-05 19:38 PST (executed 2026-11-06T03:49Z, memory log ~/memory/2026-11-05.md): the ledger sync script's first 'UNVERIFIED' verdicts on the two >1MB ledger files (ACTIVITY-LEDGER.md, activity-ledger.jsonl) were a verification-method artifact — the contents API returns empty content for files >1MB, so byte-compare always fails; re-checked by git blob SHA, both MATCH (bd0a174f, e6436f30). Corroborated the same day by the smart-link reverify, which used raw download_url because the contents API returns empty content for the 1.4 MB index (hidden_files/smart-link-reverify-2026-11-05.md), and by the 716fa2bf index read (1,408,974 B; 'contents API returns encoding none over 1MB'). Duplication check this tick: live registry index .naya/memory/smart-notes/index.json at tip 9004ce29 (1,246 entries) contains 0 'contents', 0 '1MB', 0 'empty content'; the 9 blob-SHA hits are about rebase/compare identity (SN-0188 family, SN-0250), not the API limit. lessons.jsonl carries no contents-API note (its one 'blob' hit is quota-attribution). Number census at live tip 9004ce29 (git protocol, local mirror): SN-2206 absent from main-tree paths, branch tree, and registry index; branch head 03fcc466 (SN-2205); counter ends at 2205; open PRs #3256, #3255, #3254, #3178, #3089 claim no SN file (file lists checked via App route this tick); #2416 closed unmerged since 2026-10-21; #1354 capped at 2,500, commenting disabled."
}
```
