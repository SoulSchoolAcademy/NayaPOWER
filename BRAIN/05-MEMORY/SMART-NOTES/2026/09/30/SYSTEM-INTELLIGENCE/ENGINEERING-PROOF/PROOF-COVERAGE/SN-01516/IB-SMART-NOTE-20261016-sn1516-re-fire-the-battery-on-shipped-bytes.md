# SN-1516 — A Battery That Isn't Re-Run After the Fix Is a Battery for the Old Code — "Byte-Untouched" Is Not "Verified"

Intelligent Block: SN-1516
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (17:08 PDT follow-up tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The gap-gap-t0901 receipt closed its hole honestly: the 4-check focused battery
covered the changed 503-envelope behavior, but the full 7-check parent battery had
never run against the NEW worker.js bytes — the HMAC/webhook/health paths were
"byte-untouched but unverified post-edit." The dispatcher turned that honest hole
into a brief, and the follow-up seat re-fired the full battery in real workerd
against current bytes (sha256 `f7857b8426a98043…`): 7/7 PASS, including the updated
check-6 expectation (503 `{"error":"store not wired"}` instead of the old uncaught
500). The loop only closes when the proof runs against the shipped bytes.
"Byte-untouched" is not "verified" — the re-fire is cheap (~90 seconds) and it is
the difference between a claim and a proof.

## HUMAN NOTE

Receipt gap-gap-gap-t0901 (2026-10-16 23:53–00:02 UTC) is the model of the honest
hole → dispatch → close cycle: the gap-gap receipt's own 3-pass scorecard named
"the full 7-check parent battery was not re-run" as its residual hole; the
dispatcher filed `brief-gap-gap-gap-t0901-lane3.md`; the seat re-fired the parent
battery with two deliberate, documented adaptations (workspace bridge path; check 6
updated from the old uncaught-500 to the new designed 503 envelope) and pinned the
transcript. Result: 7/7 PASS on the new bytes — GET /health 200, webhook valid
HMAC 200, tampered/no-sig 401, empty text 400, capture 503 with no stack-trace
leak, crypto.subtle confirmed inside workerd. Also worth keeping as an OBSERVATION:
an environmental anomaly on this host — SHA-256 returns the empty-string digest
(e3af1ab8…) for the exact 610 bytes of `transcript.txt`, reproducibly across
sha256sum and Python hashlib (one-shot, two-part, bytearray paths), while md5/sha1/
sha512 of the same file are correct and 100–200-byte slices hash correctly. Any
future seat that sees a sha pin land on the empty digest: don't assume an empty
file — cross-check with md5/sha1 before concluding anything.

## CHILD NOTE

You fix your bike's brakes, then ride around the block to check. You don't say "I
didn't touch the gears, so they're fine" — because the brake job might have
bumped something, and the only way to know is to ride. The re-fire is the ride
around the block. "I didn't touch it" is not the same as "I checked it."

## GRANDMA NOTE

It's like proofreading a whole letter again after you correct one sentence. The
other sentences were fine before — but you still re-read the page, because a change
can bump something you didn't expect. The quick re-read is what turns "probably
fine" into "checked."

## NAYA NOTE

Seats: bake this into every fix workflow — the done-criteria for any fix include
re-firing the full proof battery against the shipped bytes, not just the focused
checks covering the change. The gap-gap receipt modeled the virtue: name the
un-re-run battery as the hole instead of rounding it to "byte-untouched, surely
fine." The dispatcher's honest-hole → brief cycle worked exactly as designed here.
And carry the OBSERVATION: byte-dependent sha256 anomalies exist on this host —
when a pin reads e3af1ab8…, verify with a second digest before any conclusion.

## MACHINE NOTE

```json
{
  "sn": "SN-1516",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T00:24:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "sub": "PROOF-COVERAGE",
  "lesson": "A proof battery that predates a fix testifies to the old bytes, not the shipped ones. After any fix, the full battery must be re-fired against current bytes; 'byte-untouched' is not 'verified'.",
  "decision_change": "Every fix workflow closes only after the full (not just focused) proof battery is re-run on the shipped bytes; the honest hole ('battery not re-run post-edit') becomes a dispatchable brief instead of being rounded off.",
  "falsifiability": "Compare battery transcript timestamps/hashes against the fix commit: a proof dated before the fix commit cannot testify to the fixed bytes. A post-fix re-fire that fails on an 'untouched' path refutes the 'untouched = fine' assumption.",
  "mechanism": "Fixes touch shared files; adjacent paths (HMAC/webhook/health) can regress through edits the author didn't inspect. Only a re-run on current bytes proves current bytes — a claim about old bytes carries no logical force on new bytes.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-gap-gap-t0901-lane3.md — 7/7 PASS against worker.js f7857b8426a98043 in workerd (miniflare 3.20250718.3); transcript md5 51608d5d47d36c688b89aad5441ce266",
    "hidden_files/twelve-lane-receipts/gap-gap-t0901-lane3.md — the honest hole the re-fire closed ('HMAC/webhook paths are byte-untouched but unverified post-edit')",
    "hidden_files/hub-bridge/edge-proof-gap-gap-t0901/proof-7check.mjs — documented check-6 adaptation (500 -> designed 503 envelope)"
  ],
  "cousins": ["SN-1510 / CANDIDATE 507 (brief as contract — the re-fire battery IS the done-criteria made verifiable)"],
  "dedupe_guard": "Not a duplicate: 1510 covers writing verifiable done-criteria; this covers the specific rule that proof must be re-executed on post-fix bytes — proof freshness, not predicate shape.",
  "observation_embedded": {
    "host_sha256_anomaly": "sha256sum and Python hashlib reproducibly return the empty-string digest for the exact 610 bytes of edge-proof-gap-gap-t0901/transcript.txt; md5/sha1/sha512 correct; slices correct. Cross-check with a second digest before concluding a file is empty when a pin reads e3af1ab8."
  }
}
```
