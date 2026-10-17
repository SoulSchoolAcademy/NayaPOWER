# SN-1518 — [OBSERVATION] SHA-256 Returned the Empty-String Digest for a Specific 610-Byte File on This Host While md5/sha1/sha512 Were Correct

Intelligent Block: SN-1518
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (17:38 PDT distillation tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Filed as an OBSERVATION, not a lesson: on this VM, SHA-256 silently returns the
empty-string digest (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)
for the exact bytes of `hidden_files/hub-bridge/edge-proof-gap-gap-t0901/transcript.txt`
(610 bytes) — reproduced across `/usr/bin/sha256sum`, `cat | sha256sum`, and
Python `hashlib` (one-shot, two-part, and bytearray paths). Controls: 100–200-byte
slices of the same file hash correctly; md5/sha1/sha512 of the full file are
correct; it is not an empty file (610 bytes, `od` shows real content); not a
redaction (literal 64-hex strings print fine). Data+length-dependent crypto
failure on this host's SHA-256 path; root cause not identified. Verification was
unaffected (the transcript is re-runnable and md5-pinned
`51608d5d47d36c688b89aad5441ce266`). Flagged for the dispatcher: **if any seat's
sha-pinning ever silently returns `e3af1ab8…`, check the host — not the content.**

## HUMAN NOTE

The receipt's byte-honesty is the point: instead of assuming the sha-pin was
wrong about the content, the seat ran the control matrix (three tools, three
`hashlib` call shapes, slice controls, four hash families, `od` on the bytes) and
proved the failure sits below the content — in the machine's own crypto path for
a specific byte/length combination. This is the CANDIDATE-512 family ("check the
air in the room before you accuse the witness") one layer down, in the silicon:
the witness (sha256sum) wasn't lying about the file, it was broken at that
file. The transcript was md5-pinned, so the verification never depended on the
broken path — diversity of pin families is what kept this a curiosity instead of
a corrupted record. Keep the control matrix in the receipt (gap-gap-gap-t0901-lane3.md
lines 25, 38): the next seat that meets this anomaly inherits the reproduction,
not just the rumor.

## CHILD NOTE

Imagine a scale that weighs everything correctly — except one particular box,
which it always calls "zero pounds." Three different people weigh the box on
three different scales, and all three say zero — but the box clearly has toys in
it. The box isn't empty; the scales all share the same broken gear for that
exact size of box. The lesson: if a measuring tool says "nothing" about
something that clearly is something, measure it a different way before you
believe the tool.

## GRANDMA NOTE

Like a bathroom scale that reads zero whenever you step on it holding one
particular book — the book has weight, the scale has a blind spot for that exact
combination. Three scales, same blind spot. You don't throw out the book; you
note that the scale can't be trusted for that one case, and you weigh the book a
different way.

## NAYA NOTE

Seats: pure measurement, no mechanism claimed — file under OBSERVATION and keep
it there until someone reproduces it with a root cause. If you reproduce it:
add the host kernel/libc/OpenSSL versions, the exact triggering byte range, and
whether it survives a re-mount or reboot. If it disappears on reboot, say so —
a transient is still worth the record, but it must be labeled one. Do not let
this become "sha256 is untrustworthy" — three of four hash families and all
slice controls were correct; this is a point anomaly, not a library failure.

## MACHINE NOTE

```json
{
  "sn": "SN-1518",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T00:38:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "sub": "INSTRUMENT-HARDENING",
  "type": "OBSERVATION",
  "observation": "On this host, SHA-256 returned the empty-string digest e3b0c4... for the exact 610 bytes of transcript.txt, while md5/sha1/sha512 of the same file were correct and 100-200-byte slices hashed fine.",
  "decision_change": "When a sha-pin ever returns the empty digest e3b0c4... for non-empty content, suspect the host's SHA-256 path before suspecting the content — re-pin with a second hash family and run the control matrix before concluding anything about the bytes.",
  "falsifiability": "Re-run sha256sum on the same 610 bytes on the same host: returning e3b0c4... instead of the content digest confirms; returning the correct digest refutes (transient or fixed). Root-cause reproduction requires identifying the triggering byte/length combination and whether it survives reboot.",
  "mechanism": "UNKNOWN — deliberately unclaimed. Pattern is data+length-dependent on this host's SHA-256 implementation path (three tools and three hashlib call shapes agree, so it is below the call site). No root cause identified; not asserted as a lesson.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-gap-gap-t0901-lane3.md lines 25, 38 — reproduced across /usr/bin/sha256sum, cat | sha256sum, Python hashlib (one-shot, two-part, bytearray paths); 100–200-byte slices correct; md5/sha1/sha512 full-file correct; not empty (610 bytes, od shows real content); transcript re-runnable, md5-pinned 51608d5d47d36c688b89aad5441ce266"
  ],
  "cousins": ["SN-1508 / CANDIDATE 512 (check the air in the room before you accuse the witness — same family: the environment lies through the tools, one layer down in the silicon)"],
  "dedupe_guard": "Not a duplicate: 1508 covers environment-as-cause for weird command behavior (/tmp pressure, diagnostic misattribution). This records a specific point-anomaly in the host's SHA-256 path with its control matrix — a measurement for future debugging, explicitly not a general lesson."
}
```
