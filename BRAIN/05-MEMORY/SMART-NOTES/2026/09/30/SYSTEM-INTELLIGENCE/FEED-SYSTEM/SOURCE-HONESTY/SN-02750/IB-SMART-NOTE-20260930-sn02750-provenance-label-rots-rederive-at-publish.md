# A Provenance Label Stamped at Generation Rots the Moment Its Source Moves — Re-Derive It at Publish or Drop It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02750-provenance-label-rots-rederive-at-publish
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** TIPVERIFY-64 F13 (2026-11-12 20:58 PST, pin 26b1a0e6) + CONNECT-driver run 20:08 PST; memory log ~/memory/2026-11-12.md, TIPVERIFY-64 entry.

## ✦ IN A NUTSHELL

The live Hub feed's `generated_from` label names registry@37c542f6 — but the live feed holds 1,022 entries against main's 877, with 145 IDs only in live. The label is false provenance. A provenance label stamped at generation names a frozen source version; the artifact keeps moving, so the label rots with every later landing. Re-derive provenance at publish or read time, or drop the label — a stale `generated_from` is worse than none, because it cites a version that no longer describes the artifact and a cold reader will trust it.

## 🩷 HUMAN NOTE

Shawn — the live Hub feed says it was "generated from" one version of the registry, but it now holds 145 notes that version never contained. The label is a lie by age: it was true when stamped and false ever since, because the feed kept growing while the label stayed frozen. The fix is simple: either re-stamp the label every time the feed publishes, or take the label off. A wrong label is worse than no label — no label makes a reader check; a wrong label makes them trust something false.

## 🟣 CHILD NOTE

Imagine a lunchbox with a sticker that says "packed by Mom on Monday." By Friday the box has different food in it, but the sticker still says Monday. If you trust the sticker, you think you know what's inside — but you don't. A sticker is only true on the day it's stuck on. Either write a new sticker every day, or peel it off.

## 🔵 GRANDMA NOTE

Dear, it is like a jar labeled "strawberry jam, June" that someone refilled with marmalade in August. The label was honest in June and a lie by August — and the lie is worse than a blank jar, because a blank jar makes you look inside, while the label makes you spread marmalade on toast expecting strawberry. Labels must be rewritten when the contents change, or taken off.

## 🟠 NAYA NOTE

This is the publish-side companion to SN-1333 (provenance is a byte, not a byline — about authorship) and SN-1942 (check deploy currency before grading code — about live-vs-repo mismatch). Those cover who did it and which bundle is live; this covers the label itself. (1) A `generated_from` value is a claim about the artifact's source at a moment, not a property of the artifact — it decays the moment the source moves. (2) The 2026-11-12 measurement is the worked proof: live 1,022 entries (7,885,398 B) vs 877 on main, 145 IDs only in live, newest live card 2026-11-13, label still naming registry@37c542f6 — corroborated by two independent reads (TIPVERIFY-64 and the CONNECT-driver run). (3) The content itself is in the repo — the drift is in the feed file and registry, not in the notes — which is exactly why a false label is dangerous: everything looks present while the provenance is wrong. (4) The cure is mechanical: re-derive at publish, or strip the label.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [
    ["feed", "provenance"],
    ["publish", "label"],
    ["source-of-truth", "drift"]
  ],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note governs stamped provenance labels (generated_from and equivalents) on continuously generated artifacts only: it does not claim all labels rot (a label naming immutable content-addressed bytes does not), only that a label naming a moving source version rots. It does not adjudicate the feed/main divergence itself (feed-refresh owner), only the label's falsehood.",
  "decision_change": "Before a feed publish stamps (or keeps) a generated_from label, the publish step re-derives it from the current registry tip; a label that cannot be re-derived at publish time is stripped rather than carried forward.",
  "enforcement": "The feed-refresh check verifies generated_from == current registry tip at publish; a mismatch blocks publish or strips the label (feed-refresh owner). A published unit whose generated_from names a superseded registry version fails the feed-refresh check.",
  "evidence": [
    "TIPVERIFY-64 F13 (2026-11-12 20:58 PST, pin 26b1a0e6): live feed 1,022 entries (7,885,398 B) vs 877 on main; 145 IDs only in live, 0 only in tip; newest live card 2026-11-13 (33 notes); live generated_from label names registry@37c542f6 — false provenance. Classification: SOURCE-OF-TRUTH DRIFT (feed face).",
    "CONNECT-driver run 20:08 PST (comment 6843942992, board #3352): live Hub feed 145 entries ahead of main (1,022 vs 877); generated_from label now false provenance. Independent corroboration of the same measurement.",
    "All 145 extra notes have pages on main — the content is in the repo; the repo feed file + registry just do not include it. The drift is in the feed surface and the label, not in the notes."
  ],
  "falsifier": "Refuted if a stamped label is shown to stay true while its source moves without re-derivation — e.g. labels content-addressed to the artifact bytes rather than naming a source version; cured when feed-refresh re-derives generated_from at publish and the label matches the live registry across moves.",
  "intelligence_class": "LESSON",
  "mechanism": "The feed is generated continuously from live state while the label names one frozen registry version; each new note lands without updating the label, so the label's claim ('generated from registry@X') becomes false the moment the registry moves past X. A cold reader trusts the label instead of re-checking, so the falsehood propagates as if it were provenance.",
  "related_notes": ["SN-1333", "SN-1942"],
  "truth_state": "CANDIDATE"
}
```
