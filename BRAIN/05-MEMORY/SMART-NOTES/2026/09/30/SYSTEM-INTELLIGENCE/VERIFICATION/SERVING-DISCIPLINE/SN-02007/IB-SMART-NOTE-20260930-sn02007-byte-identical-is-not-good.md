**Intelligent Block:** SN-02007 — Byte-Identical to the Repo Is Not Good — Score a Live Face Against Its Spec, Not Just Its Bytes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-26
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A live page can be byte-proven identical to the repo and still be bad: on 2026-10-26 the PI face at nayanet.live/pi-face was byte-identical to the repo file and verified 9.0 for wiring, yet cold-scored 4.0 against its governing spec, with 10 holes (missing list, placeholder areas, dead links) that were already in the repo bytes. Byte-matching proves deployment fidelity only; it cannot prove design quality, because the repo is a copy of the defect, not an independent reference. Score a live face against its spec, never against its repo copy alone.

## 🩷 HUMAN NOTE
Think of it like photocopying a typo: the copy can be perfect and the page can still be wrong. The team proved the live PI face matched the repo exactly — and then scored it 4 out of 10, because the repo itself held the flaws: a missing list, placeholder dots, dead links. A perfect copy of a bad page is still a bad page. From now on, a face is judged against what it was supposed to be, not just against the file it came from.

## 🟣 CHILD NOTE
Imagine you draw a picture, then trace it perfectly. The tracing is exactly the same — but if your first picture had a missing arm, the tracing has a missing arm too. Tracing it right does not fix the picture. To know if the picture is good, you have to look at what you meant to draw, not just at the tracing.

## 🔵 GRANDMA NOTE
If a recipe has a mistake in it, copying it out neatly does not fix the cake. The copy can be letter-perfect and the cake can still flop. Check the cake against what a good cake should be — not just against the card you copied it from.

## 🟠 NAYA NOTE
Cold successor, hear this: deployment fidelity and design quality are two different questions, and one proof cannot answer both. A VERIFY receipt that says "live bytes equal repo bytes" answers only "did the right file get served?" It says nothing about whether the file is good. The PI face case is the canonical instance: live /pi-face == repo HUB/app/pi-face.html (31,566 B, same sha256, VERIFY 9.0 for wiring) and, in the same hour, a cold score of 4.0 against the merged spec v2, because every one of the 10 defects lived in the repo bytes themselves. Whenever you accept a live surface, demand both proofs: the byte proof (served == repo) and the spec proof (served == spec, scored cold). A byte-proof-only 9.0 must never close a face item. Cousin, not duplicate: SN-2001 (prove by served title, never by HTTP 200) governs a different false proof — status code instead of content; this note governs a different false proof — repo copy instead of spec.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-02007",
  "title": "Byte-Identical to the Repo Is Not Good — Score a Live Face Against Its Spec, Not Just Its Bytes",
  "truth_state": "CANDIDATE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "VERIFICATION", "SERVING-DISCIPLINE"],
  "rule": "A live surface is accepted only on two proofs: served bytes equal repo bytes (deployment fidelity) AND a cold score against the governing spec (design quality); a byte-proof-only receipt never closes a face item, because repo bytes can themselves carry the defect.",
  "applies_when": ["verify", "live-face"],
  "enforcement": "A VERIFY receipt for a live face must cite the governing spec version plus a cold spec score with its defect list; a receipt citing only byte-identity (same sha256 / byte-identical to repo) is bounced and does not close the PI item.",
  "cousins": ["SN-2001"],
  "evidence": ["Live board #3066 comment 6421431051 (VERIFY 2026-10-26T16:32:31Z: nayanet.live/pi-face == repo HUB/app/pi-face.html byte-identical, 31,566 B, same sha256; /projects HOLD)", "Live board #3066 comment 6421757244 (PI face scored 4.0/10 at live /pi-face, 10 byte-proven holes: list missing, areas placeholder, dots not icons, nothing alive, '?' orbs, no per-area truth, apology prose, dead/wrong links)", "Live board #3066 comment 6421980646 (PI FACE CANONICAL MERGED SPEC v2 governs the rebuild)", "Live board #3066 comment 6422275203 (VERIFY: /pi wiring PASS VERIFIED LIVE 9.0, byte-identical at tip 0eb1f939; HOME DIVERGENCE CONFIRMED, /projects + /api HOLDS STAND)"],
  "status": "CANDIDATE — staged 2026-10-26, not ratified; only Shawn ratifies.",
  "decision_change": "The next VERIFY receipt for a live face must score against the governing spec; a byte-match-only 9.0 no longer closes a face item.",
  "falsifiability": "Proven wrong for this instance if a cold re-score against spec v2 finds the 10 holes absent from the served bytes — i.e. if the defect lived in the served copy, not the repo source.",
  "mechanism": "Byte-matching checks one relation (served == repo); design quality is a different relation (served == spec). When the repo is the defect's source, the first relation holds precisely because the defect was faithfully deployed."
}
```
