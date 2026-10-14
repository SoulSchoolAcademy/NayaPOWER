# IB-SMART-NOTE — SN-1276 — Full-64 SHA Compare, Always

Intelligent Block: IB-SMART-NOTE-20261014-sn1276-full-64-sha-compare-always
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-14
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Compare full 64-hex commit SHAs, always. A first-16-character prefix match is not a match: human transcription mangles long hex strings into common-prefix near-misses, and short-prefix comparison cannot distinguish the mangled copy from the real one. Brief-quoted SHAs are suspects, never premises.

## HUMAN NOTE
A t0733-lane10 brief mangled two SHA quotes — a 59-character common-prefix near-miss. Comparing the builder's receipt bytes at full 64 hex exposed it; the first-16 match had nearly let it through. Git's 160-bit collision resistance guards against adversarial collisions, not against human transcription drift: the near-miss wasn't an attack, it was a mangled quote, and prefix comparison is exactly the tool that can't tell them apart. Standing rule from the event: compare the builder's receipt bytes at full-64; any SHA quoted in a brief is a suspect until the full string is matched against live bytes. Linked to the byte-exactness family (candidate 246). Evidence: hidden_files/twelve-lane-receipts/t0733-lane10.md, learning-events-2026-10-14-02.md (candidate 255).

## CHILD NOTE
Imagine two nearly identical keys — they look the same for the first half but differ at the end. If you only check the first half, you'd think they're the same key. Always check the whole key before you declare a match.

## GRANDMA NOTE
Honey, when you're checking whether two of those long number-strings are the same, check every last character. The front half matching means nothing — people miscopy the tail all the time.

## NAYA NOTE
Verification doctrine: SHAs are compared at full 64 hex or not at all. Prefix matching (first-8, first-16) is a lookup convenience, never a verification primitive. Anything quoted in a brief — SHA, hash, signature — is a suspect until its full length is re-derived against live bytes. The trap is specific: transcription produces common-prefix near-misses, which are the one class of error that prefix comparison structurally cannot catch. When a brief says "head X matched," the audit question is: matched at what length?

## MACHINE NOTE
{
  "smart_note_id": "SN-1276",
  "intelligent_block_id": "IB-SMART-NOTE-20261014-sn1276-full-64-sha-compare-always",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM-INTELLIGENCE",
  "subcategory": "SYSTEM-DESIGN/VERIFICATION-DOCTRINE",
  "captured": "2026-10-14",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "compare_full_64_hex; prefix_match_is_not_a_match; brief_quoted_sha_is_suspect",
  "falsifier": "if transcription were always faithful, prefix matching would suffice; the 59-char common-prefix near-miss in t0733-lane10 falsifies that",
  "evidence": ["hidden_files/twelve-lane-receipts/t0733-lane10.md", "learning-events-2026-10-14-02.md (candidate 255)"]
}
