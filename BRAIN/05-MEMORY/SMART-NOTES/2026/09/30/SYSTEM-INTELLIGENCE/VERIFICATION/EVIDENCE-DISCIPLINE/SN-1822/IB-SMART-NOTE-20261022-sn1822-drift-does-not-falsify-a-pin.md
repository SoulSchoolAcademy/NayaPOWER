Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When the tip moves mid-verification — between the first seat's pin and the second seat's probe — the pin is neither confirmed nor refuted. The verifier must (1) name the drift commit byte-for-byte via the compare API, (2) re-derive the artifact AT the claimed tip to prove it was honest-at-pin-time, and only then (3) re-pin at the new tip or name CONFIRM. A pin is a claim at an address; the new tip is a different address; comparing a pin against a new tip is a category error. Drift does not falsify a pin — unverified drift does.

## 🩷 HUMAN NOTE

On 2026-10-22, Lane 3 pinned the retrieval-auth-gate read-seam insertion point at the live tip f7bd39ca. When Lane 4 went to corroborate, the tip had moved to e8a10e0a. The seat did not declare the pin stale and did not silently re-pin: it localized the drift through the compare API (f7bd39ca -> e8a10e0a, named byte-for-byte), re-derived the seam blob AT t1273's claimed tip to prove the pin was honest-at-pin-time, and only then re-pinned and named CONFIRM on live bytes. Lane 11 repeated the ritual as the blinded third seat — three seats, one seam. The mirror lesson from the night-dispatcher: "drift does not falsify a pin; unverified drift does."

## 🟣 CHILD NOTE

Imagine you draw a treasure map on Monday and mark "the gold is here" on a corner of the garden. On Tuesday your friend goes to check — but someone moved the garden shed overnight, so the corner looks different. Your friend doesn't throw away the map. They go back to Monday's garden, check that the map was right ON MONDAY, name what moved ("the shed went two steps left"), and only then draw the new map for Tuesday. Check the map against the day it was drawn — then update it.

## 🔵 GRANDMA NOTE

Sweetheart, a promise made at one address is checked at that address, not at wherever the house happens to be today. If you want to know whether Tuesday's directions were true, you walk Tuesday's street — you don't stand on Wednesday's street and call the directions a lie. Name what changed between Tuesday and Wednesday, prove the directions were honest on Tuesday, and then write the new ones.

## 🟠 NAYA NOTE

Sister: the pin-verdict discipline is not "re-derive on live bytes and compare" alone — it is "re-derive at the CLAIMED address and compare." The second and third seats on the retrieval-auth-gate seam ran the full tip-probe ritual: git ls-remote pre-reads, post-reads, pre-write (pin-late honored); on drift, the compare API named the drift commit byte-for-byte; the seam blob was re-derived in a fresh shallow clone AT the claimed tip to prove honest-at-pin-time; only then did the seat re-pin. A corroboration that skips the at-claimed-tip re-derivation has not corroborated — it has guessed. Never let a moved tip launder a dishonest pin, and never let it falsify an honest one.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1822-drift-does-not-falsify-a-pin",
  "lesson": "When the tip moves mid-verification, re-derive AT the claimed tip, name the drift commit byte-for-byte, and only then re-pin. Drift does not falsify a pin; unverified drift does.",
  "applies_when": ["verify", "pin-corroboration", "tip-drift"],
  "enforcement": "Corroboration receipts must carry the tip-probe triplet (git ls-remote pre-reads / post-reads / pre-write). On drift, the receipt names the drift commit byte-for-byte via the compare API and shows the at-claimed-tip re-derivation before naming CONFIRM. A corroboration that skips the re-derivation is flagged UNVERIFIED, never CONFIRM.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1275, 2026-10-22T11:47Z]",
    "twelve-lane-receipts/t1274-lane4.md (Lane 4 second-seat corroboration; tip drift f7bd39ca->e8a10e0a localized via compare API + old-tip re-derivation, CONFIRM on live bytes)",
    "twelve-lane-receipts/t1275-lane11.md (Lane 11 blind third corroboration; relay #2793 comment 6340132118)",
    "hidden_files/feed-log-watermark.md (FEED-LOG tick 2026-10-22 12:08Z: units seam-corroboration-second-seat-t1274, blind-third-corroboration-caller-gap-t1275)"
  ],
  "decision_change": "A verifier observing the tip move between pin and probe now decides 'name the drift commit, re-derive at the claimed tip, then re-pin' instead of 'reject the pin as stale' or 'silently re-pin at the new tip'.",
  "falsifiability": "Re-derivation at the claimed tip producing bytes that differ from the pin falsifies the pin itself (dishonest at pin time) — the procedure carries its own falsifier. The rule would be retired if tip-moved verifications showed zero false confirm/deny over a long window (cost exceeds value).",
  "mechanism": "A pin binds evidence to an address (tip SHA). A moved tip is a different address. The only truth-functional comparison is at the claimed address; comparing against the new tip is a category error — either an unproven equivalence (silent re-pin) or a false negative against an honest pin (stale rejection).",
  "truth_state": "CANDIDATE"
}
```
