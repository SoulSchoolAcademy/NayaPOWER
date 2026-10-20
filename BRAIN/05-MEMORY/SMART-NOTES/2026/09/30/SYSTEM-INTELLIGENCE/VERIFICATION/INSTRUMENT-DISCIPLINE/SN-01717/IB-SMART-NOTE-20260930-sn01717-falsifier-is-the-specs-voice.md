# IB-SMART-NOTE-20260930-sn01717-falsifier-is-the-specs-voice

Intelligent Block: SN-01717
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-20
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
When your implementation disagrees with a RED-first falsifier, the falsifier is the spec's voice: re-read the spec's exact wording and fix the implementation — never defend your first reading or weaken the falsifier.

## 🩷 HUMAN NOTE
The seat built six checks from a spec, wrote fourteen falsifier fixtures from the same spec's explicit language, and ran them: 6 of 14 failed. Every failure was the spec teaching the seat, not a bug in the tests — the seat's first reading of the spec (numeric list order) was wrong; the spec's actual words ("on sight") were right. The move that mattered: the seat changed the machine semantics to match the spec's exact wording instead of defending its first reading. That is the whole discipline: when the test and the code disagree, the test was written from the spec's mouth — re-read the spec, don't re-argue it.

## 🟣 CHILD NOTE
Imagine you and a friend both read the same recipe, and your friend says "the recipe says to add the eggs NOW." You think the eggs go in later. Instead of arguing about who remembers better, you open the recipe and read the words together. The words are the boss — not your memory of the words. When a test written from the spec disagrees with your code, open the spec and read the words. Change your code to match the words, not the other way around.

## 🔵 GRANDMA NOTE
There is a moment every builder knows: the thing you built does not behave the way the plan said it should, and the temptation is to say the plan must have meant what you built. It almost never did. The plan said what it said — the words are still there on the page. Read them again, slowly, and you will usually find the instruction you skimmed past the first time. The plan is the voice; your first reading was just a guess at it.

## 🟠 NAYA NOTE
This is the test-authority-inversion companion to SN-0122 ("Re-Read the Spec When Your Numbers Diverge") and SN-01304 ("RED-first at action time"). SN-0122 covers divergence between artifact and canonical numbers; SN-01304 covers writing the suite before the code. This note covers the dispute-resolution protocol between them: in a falsifier-vs-implementation disagreement, authority flows falsifier → spec text → implementation, never implementation → falsifier. The failure mode it kills is interpretation entrenchment: the implementer's first reading feels like the spec, so the falsifier looks wrong. The enforcement makes the resolution mechanical: the frozen fixtures (SHAs pinned per t0950) stay green, and any fixture repair must quote the spec § verbatim — the repair cites the words, never the reading. Boundary: the principle holds only while the falsifier encodes the spec faithfully; a documented case where the spec's exact text sides with the implementation is the note's own falsifier — then the falsifier gets repaired to the spec text, with the quote, not weakened.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01717",
  "lesson": "When your implementation disagrees with a RED-first falsifier, the falsifier is the spec's voice: re-read the spec's exact wording and fix the implementation — never defend your first reading or weaken the falsifier.",
  "applies_when": ["spec-implementation", "falsifier-disagreement", "red-first"],
  "enforcement": "the t0943 RED-first per-falsifier acceptance checklist: frozen fixture SHAs (pinned per t0950) must stay green via claim-brief.py --self-test, and any fixture repair that does not quote the spec section text verbatim fails the lane-10 receipt review; authority resolves falsifier -> spec text -> implementation",
  "decision_changed": "when a falsifier fails against your implementation: the first move is re-reading the spec's exact wording and fixing the implementation; defending the first reading or weakening the falsifier is never the first move",
  "falsifier": "a documented case where the spec's exact text sides with the implementation while the falsifier misencodes the spec — then the falsifier gets repaired to the spec text with the spec quote, not silently weakened",
  "mechanism": "interpretation entrenchment: the implementer's first reading of a spec carries private interpretation and feels like the spec itself; the falsifier was written from the spec's explicit language, so treating the falsifier as the spec's voice forces re-reading the exact authoritative wording, which removes the bias (in the evidence case, section 9.2's 'on sight' beat the implementer's numeric-list-order reading)",
  "evidence": "hidden_files/twelve-lane-receipts/t0986-lane10.md (2026-10-20 06:44Z, 9.5/10): first self-test run failed 6/14 fixtures; every failure was the spec teaching the seat — the spec's 'on sight' language was the authority, not the implementer's list-order reading; machine semantics changed to match the exact spec wording",
  "companions": "SN-0122 (re-read the spec when numbers diverge — the canonical-document discipline); SN-01304 (RED-first at action time — the suite-precedes-code discipline); t0950 (frozen fixture SHAs)"
}
```
