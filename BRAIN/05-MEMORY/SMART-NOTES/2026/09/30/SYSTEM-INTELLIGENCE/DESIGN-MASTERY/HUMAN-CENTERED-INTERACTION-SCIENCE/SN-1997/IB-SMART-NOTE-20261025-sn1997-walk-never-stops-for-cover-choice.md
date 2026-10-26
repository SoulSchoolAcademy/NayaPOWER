**Intelligent Block:** SN-1997 — The walk never stops for a cover choice
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
Shawn's simplicity ruling (2026-10-26T00:11Z): when a citizen is walked through creating a page, the walk never stops to ask them to pick a cover. The system builds everything in one pass, and the cover is already chosen from the citizen's answers: a strong match (2 or more signals) means the top matched featured cover is worn at birth with a one-sentence why; a weak signal means the page-type default plus a suggestion. Changing the cover afterward is one tap from the page. Builders named: Power owns the birth pass wearing the pick; Nitro owns the end-of-walk moment; Resolve owns match plus why plus cold-walk proof. The withdrawn chooser page (PR #3074, closed by Resolve after Shawn's rejection) is the counter-example: a standalone chooser inside the walk is not the design.

## 🩷 HUMAN NOTE
People do not come to pick decorations. They come to get a page. Stopping them halfway through to choose a cover breaks their momentum and asks them a question the system can already answer from what they have told it. So the system answers it, shows its work in one sentence, and lets them change it in one tap. Choice is preserved. Interruption is removed.

## 🟣 CHILD NOTE
Imagine you are making a birthday card, and someone keeps stopping you to ask "which sticker?" before you have even finished. That is annoying, right? So instead, your helper picks the sticker that matches what you said you like, puts it on, and tells you why in one short sentence. If you do not like it, one tap swaps it. You never have to stop.

## 🔵 GRANDMA NOTE
When someone is making their page, we do not stop them halfway to ask about the cover, dear. We already listened to their answers, so we pick the cover that fits best and put it right on. We tell them why in one short sentence. And if they would rather have a different one, it is just one tap away. No fuss, no stopping.

## 🟠 NAYA NOTE
This is a standing product decision, not a suggestion. Any future birth-pass, onboarding, or walk design that inserts a cover-choice stop contradicts it: route such a proposal back to this ruling and to the cold-walk proof. The chooser interface itself is Nitro's to design (the Smart Cover Library, living in Smart Factory and at the page-creation moment), but it must not become a stop in the walk. Verify by cold-walk proof: zero cover-choice stops, the worn cover matching the spec rule, and a working one-tap change. Provenance, stated plainly: the evidence here is Resolve's board relay of Shawn's ruling (board #3066 comment 6405333867), not Shawn's typed bytes in this loop's chat. This note is CANDIDATE, not RATIFIED; only Shawn ratifies.

## 🟢 MACHINE NOTE
```json
{
  "title": "The walk never stops for a cover choice",
  "slug": "walk-never-stops-for-cover-choice",
  "sn": "SN-1997",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["onboarding", "birth-pass", "cover"],
  "enforcement": "Cold-walk proof (Resolve-owned: match + why + cold-walk proof) must show zero cover-choice stops, the worn cover matching the spec rule (strong match of 2 or more signals: top matched featured cover + one-sentence why; weak signal: page-type default + suggestion), and a working one-tap change; a birth-pass build that stops for a cover choice fails the cold-walk proof.",
  "evidence": "Board #3066 comment 6405333867 (Resolve relay of Shawn's 2026-10-26T00:11Z simplicity ruling); consequence PR #3074 closed-unmerged per board #3066 comment 6405361349; rule encoded in automatch-onboarding-sync spec.",
  "decision_change": "Any future proposal to add a cover-choice stop to the onboarding walk, or to build a chooser page inside the walk, is decided against: the pick is pre-computed from answers and worn at birth.",
  "falsifier": "A cold-walk proof showing pre-picked covers mismatch citizen answers more often than a choice stop would, or showing citizens cannot find or use the one-tap change, would overturn the ruling's premise.",
  "mechanism": "Answers carry match signals; strong (2 or more) signals select the top matched featured cover with a one-sentence why, weak signals fall back to the page-type default plus a suggestion; agency is preserved by a one-tap change, so no walk stop is needed.",
  "provenance": "Evidence is a board relay of Shawn's ruling, not his typed bytes in this loop's chat; disclosed as record-not-body. Note marked CANDIDATE, not RATIFIED."
}
```
