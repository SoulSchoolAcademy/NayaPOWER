# A PATCH Echo Is Not Proof the Write Landed — Re-GET and md5 Every PATCH

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02804-patch-echo-is-not-proof-re-get-every-patch
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Board #3352 comment 6876188189 (Naya 5 director 10:45Z sign-out, 2026-11-14); shared-state failure_mode_patch_md5_echo_20261114 (recorded 2026-11-14T11:13:27Z).

## ✦ IN A NUTSHELL

On 2026-11-14 the #2599 board PATCH (265,691 chars) came back echoing the submitted body with a matching md5 — and never landed: the remote stayed at f43aaa9d, last updated 09:43:22Z. A 256,854-char PATCH persisted; 265,691- and 280,845-char PATCHes did not. The surrogate echoes what it received, not what it stored, so an md5 match on the echo proves the bytes arrived, not that they stuck. The rule: a PATCH is an unverified claim until a fresh GET returns the new body with a matching md5 — and board bodies stay under ~257K chars.

## 🩷 HUMAN NOTE

Shawn — imagine you hand a letter to the post office, they photocopy it back to you, and you take the photocopy as proof it was delivered. The photocopy only proves they received it. On Nov 14 the board PATCH for #2599 came back with a perfect photocopy — md5 matched — but the board never changed; the remote still showed the old version. The letter was too long (265,691 characters) and silently never landed, while a shorter one (256,854) went through fine. The fix is simple and now the rule: after every PATCH, fetch the board fresh and compare — the echo is the receipt for sending, the re-GET is the proof of landing.

## 🟣 CHILD NOTE

Imagine you tell your friend a really long secret, and your friend repeats it back to you perfectly — so you think they remembered it. But they only repeated what they just heard; they didn't write it down, and by tomorrow it's gone. The repeat-back proves they heard you, not that they kept it. The smart move: ask them tomorrow what the secret was. If they can tell you, it stuck. That's what re-GET does after a PATCH — it asks the board tomorrow what it remembers.

## 🔵 GRANDMA NOTE

Dear, it's like mailing a long letter and getting the carbon copy back — the copy proves you wrote it, not that it arrived. The board on Nov 14 sent back a perfect copy of a 265,691-character PATCH, md5 and all, and the board itself never changed — the old version sat there untouched since 09:43. A shorter letter went through just fine, so size was the silent tripwire. From now on: never trust the copy. Fetch the board fresh after every PATCH and check the words are really there. The copy is the sending; the fresh fetch is the landing.

## 🟠 NAYA NOTE

Evidence, first-hand from shared state (failure_mode_patch_md5_echo_20261114, recorded 2026-11-14T11:13:27Z; source board #3352 comment 6876188189, Naya 5 director 10:45Z sign-out): #2599's 265,691-char PATCH echoed md5-match but never landed — remote stayed f43aaa9d, updated 09:43:22Z. Boundary measured the same window: 256,854 chars persisted, 265,691 and 280,845 did not — the silent-failure threshold sits near ~257K chars. Repaired the same window: board trimmed, #2599 re-PATCHED 10:50:55Z and RE-GET-VERIFIED md5 f321ad59 (226,195 chars); #2154 re-PATCHED 10:51:08Z and RE-GET-VERIFIED md5 da2bab22. Cousin map: SN-01626 (verify against the tree you claim — same family: verify at the target, not at the artifact); SN-082 (execution identity, not content identity — the echo identifies content, not the act of persisting); SN-2803 (deterministic parse failure — same family: a record that never gates the next step); the 2026-11-13 /tmp-wipe failure mode (re-fetch to prove bytes — same instinct, different axis). This note is the PATCH-side twin of SN-01626: the echo is the artifact; the re-GET is the tree.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "patch_echo_is_not_proof_re_get_and_md5_after_every_patch_board_bodies_under_257k_chars",
  "mechanism": "the PATCH surrogate echoes the submitted body — its md5 is computed over what it received, not what it stored — so an echo match proves arrival, not persistence; bodies above ~257K chars fail to persist silently while the echo still matches, so a large PATCH can report success and change nothing",
  "evidence": "shared-state failure_mode_patch_md5_echo_20261114 (2026-11-14T11:13:27Z), source board #3352 comment 6876188189 (Naya 5 director 10:45Z sign-out): #2599 265,691-char PATCH echoed md5-match, remote stayed f43aaa9d updated 09:43:22Z; 256,854 chars persisted, 265,691 + 280,845 did not; repaired same window: #2599 re-PATCHED 10:50:55Z + RE-GET-VERIFIED md5 f321ad59 (226,195 chars); #2154 re-PATCHED 10:51:08Z + RE-GET-VERIFIED md5 da2bab22",
  "falsifiability": "if a re-GET after a PATCH returns the new body with matching md5, the write landed and the echo was truthful that time; if the surrogate's echo is ever shown to be computed over persisted bytes (an echo match after a failed persist becomes impossible), the mechanism claim fails; the #2599 case already demonstrates the failure, so the burden is on the echo, not the re-GET",
  "decision_change": "when any seat PATCHes a board (or any surrogate-mediated write), the landing verdict changes from 'echo md5 matched' to 'fresh GET returns the new body with matching md5'; a PATCH without a re-GET is recorded as an unverified claim, never as a landing; and bodies are trimmed below ~257K chars before the PATCH, not after it fails",
  "applies_when": [["verification", "patch-persistence"], ["board", "write"], ["claim", "landing"]],
  "enforcement": "every PATCH receipt must cite the re-GET md5 (fresh GET after the PATCH, md5 of the returned body == md5 of the submitted body); a PATCH receipt citing only the echo md5 does not count as a landing; board bodies are kept under ~257K chars, verified by byte count before the PATCH",
  "related": ["SN-01626 verify-against-the-tree-you-claim — same family: verify at the target, not at the artifact", "SN-082 execution-identity-not-content-identity — the echo identifies content, not the act of persisting", "SN-2803 deterministic-parse-failure-needs-terminal-state — same family: a record that never gates the next step"]
}
~~~
