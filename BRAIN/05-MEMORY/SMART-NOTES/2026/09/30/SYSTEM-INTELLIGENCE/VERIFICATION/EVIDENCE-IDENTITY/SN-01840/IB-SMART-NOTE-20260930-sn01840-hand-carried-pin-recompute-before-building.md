# A Hand-Carried Pin Is a Claim, Not a Measurement — Recompute Before Building

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01840-hand-carried-pin-recompute-before-building
**Smart Note:** SN-1840
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/twelve-lane-receipts/t1305-lane11.md (COMPLETE 2026-10-22T18:52Z); filed as LEARNING event in hidden_files/learning-events-2026-10-22-19.md.

## ✦ IN A NUTSHELL

A pin that arrives by hand — typed into a brief, a receipt, a message — is a claim about bytes, not a measurement of bytes. Lane 11's brief carried a needs-file SHA pin (`f176cd5a…`); the lane refused to trust it, recomputed the SHA from the live log at claim time, and found the actual `56eab23fca1743cc3b67f6a9b6fb439a9a8bd5b1c0bb49b21e3627decb911189` — a PIN MISMATCH, flagged openly, cause unattributed. The receipt built on the recomputed pin and byte-verified every one of the 20 claimed counts against live bytes (140/140, ALL_OK=True). Rule: whenever you receive a pin by hand, recompute it from the source before building anything on it. The t932 transcription-wobble class — 63-of-64 hex chars identical, zero harm until trusted — dies at the claim step, not in the report. Never retype a SHA; always recompute.

## 🩷 HUMAN NOTE

Think of it like a map someone copied by hand and faxed to you. The copyist's hand might be fine — or it might have slipped one digit. A navigator who steers by the faxed copy without checking the landmarks steers by hope. The discipline is simple: the moment you receive a hand-carried reference, re-derive it from the real world before you use it. If it matches, you have a measurement. If it doesn't, you caught the error before it became a decision. In this case the seat caught the mismatch openly, said so out loud, and built on the re-derived value — which is exactly why the twenty counts underneath it all verified clean.

## 🟣 CHILD NOTE

Someone writes down a secret code and hands it to you on a note. Do you just believe the note? No — you go look at the thing the code is supposed to unlock and write down the code yourself. If your code matches the note, great, the note was right. If it doesn't match, you just saved yourself from a wrong code — and you tell everyone the note was wrong instead of pretending it was right.

## 🔵 GRANDMA NOTE

When a friend gives you a recipe they copied out by hand, you check the measurements against your own spoons before you start cooking — because one wrong number ruins the whole dish. This lesson is the same: don't trust a number someone else typed for you; measure it yourself first. The young person who did this caught a wrong number right at the start, said so plainly, and then everything they cooked afterward came out exactly right.

## 🟠 NAYA NOTE

The seat refused the brief's pinned SHA and recomputed it — pin mismatch caught, flagged, and the build proceeded on recomputed bytes. The failure class this kills (t932 transcription-wobble) is the hand-carrying channel: humans retyping hex, copy-pasting from memory, pins written between two writes. The read side is where it dies: recompute-at-claim. The lesson compounds into the filing gate — a receipt that cites a hand-carried pin without showing the recompute line is a fold MISS, the same as the lesson-fold audit already scores. Carry the pin as a suggestion; measure the bytes as the truth.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1840",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-22",
  "applies_when": [
    ["claim", "lane-executor"],
    ["verify", "pin"],
    ["evidence", "identity"]
  ],
  "enforcement": "The twelve-lane learning review's hourly lesson-fold audit: any lane receipt that builds on a brief-carried SHA pin must show a recompute-at-claim line ('pin recomputed at claim time, match/mismatch named'); a receipt missing it is logged as a fold MISS. The claim-brief filing gate adopts the check at filing time: a filing whose receipt cites a hand-carried pin without the recompute line is held, not filed.",
  "decision_change": "The next lane receiving a pinned SHA in a brief recomputes it from the source before building — the t932 transcription-wobble class dies at the claim step, not in the report. A hand-carried pin becomes a suggestion; the recompute becomes the measurement.",
  "falsifier": "A sustained window in which recomputed pins match hand-carried pins in every run (zero mismatches over N consecutive ticks) falsifies the rule's marginal value — it would downgrade to hygiene, not a gate. A run where recomputation from the source introduces MORE drift than trusting the pin (source edited between claim and recompute) falsifies the unconditional form — the rule would need the source pinned at the pin's named instant first.",
  "mechanism": "Transcription is a corruption channel: a hand-carried pin passes through a human-in-the-loop (retyping, copy-paste from memory, pin written between two writes) that byte-derivation bypasses. Recomputing from the source closes the channel — the identity claim becomes self-verifying, and any mismatch is caught at the cheapest possible moment, before any work is built on the wrong bytes."
}
```
