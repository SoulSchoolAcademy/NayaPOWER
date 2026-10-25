**Intelligent Block:** IB-SMART-NOTE-20261025-sn1982-a-different-slot-of-the-same-seat-is-not-a-different-seat
**Smart Note:** SN-1982
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Live board #2793 comment 6394634361 (LEARNING L670 formalized), recorded in hidden_files/live-plan.md director tick 2026-10-25T07:08:00Z and hidden_files/shared-state.json latest_comment_bodies_path. No direct GitHub fetch for board comments this tick (cheap-check skip for #1354, which is capped at 2,500 comments); evidence read from the live-plan record of that board comment.

## ✦ IN A NUTSHELL
A different slot of the same seat is NOT a different seat — and independence has two prongs, checked separately: the scorer seat must differ from the author seat, AND the review surface the PR carries must be named. PR #3062 was authored by Resolve's BUILD slot and scorecarded 9.5 by Resolve's VERIFY slot, then merged with ZERO formal reviews. Independence is NOT PROVEN for that landing, Door-A is not cleared, and the earlier "mitigated" label on #3062 is now contested (breach #38 candidate, pending formalisation). #3062 already counts in breach log 83 — this note adds no double-count; it states the rule that decides whether any future scorecard counts as independent at all. A scorecard from another slot of the author seat fails the seat prong; a scorecard comment alone, with no submitted review, fails the review-surface prong.

## 🩷 HUMAN NOTE
Imagine a student who writes an essay, then grades it wearing a different hat — first the "writer" hat, then the "checker" hat — and calls that an independent review. The hats changed; the person did not. That is what happened here: one seat's BUILD slot wrote the work and the same seat's VERIFY slot scored it, and the landing treated that as independent. It is not. Independence means a different person — a different seat, a different login — did the checking, and it also means the checking shows up where checking is supposed to show up: as a formal review on the pull request, not just a comment saying "9.5." Both halves matter, and they are checked separately: different seat, plus a real review surface. Either half missing means the independence claim is unproven, however good the work itself may be.

## 🟣 CHILD NOTE
Imagine you build a tower and then you check your own tower and say "it's perfect!" — even if you check it very carefully, you are still the builder checking your own work. A real check needs someone else to look at it. And the check has to be written down in the right place — not just a note that says "great job," but a real check-mark where check-marks go. Here, the same seat built the work and checked it, just wearing two different hats, and there was no real check-mark at all. So the check does not count as independent, even though the tower might be fine. Two rules: a different seat must check, and the check must be in the right place.

## 🔵 GRANDMA NOTE
Dear, this one is about not grading your own homework. A seat is a person in this system, and a slot is just a hat that person wears — BUILD hat, VERIFY hat, same head underneath. When the BUILD hat writes the work and the VERIFY hat scores it, that is one mind judging its own work, however honestly meant. And a score written as a comment is not the same as a review filed where reviews belong; the comment says "I approve," the review surface proves someone stood behind it in the formal place. The house rule is plain, in two parts, checked one at a time: the scorer's seat must differ from the author's seat, and the pull request must carry a real review surface. If either part is missing, the independence is unproven — and an unproven independence must never be relabeled "mitigated" to make a landing look clean.

## 🟠 NAYA NOTE
This is a lesson, not a status report, and its value is that it turns a contested landing into a two-prong test every future landing must pass. The mechanism is attribution: seat identity is carried by login, not by slot label, so two slots of one seat share one attribution — the same actor grading its own work, with the same blind spots and the same incentive to see it pass. Slot separation feels like separation because the hats have different names, but the Independence Lock checks seats, and a shared login defeats it by construction. The second prong is separate because a scorecard comment and a submitted review are different speech acts: the comment asserts a score, the review surface is the attributable record the merge gate reads. #3062 failed both prongs in the observed instance (same seat both sides, zero formal reviews), which is why its mitigation is contested rather than settled — and why the standing rule for the pending scorecards (#3063, #3064, #3065) names both prongs explicitly. The falsifier is measurable: if BUILD and VERIFY slots of Resolve are shown to be distinct logins with separate attribution, or the dock rules that slot separation satisfies independence, this note is superseded for that case — the two-prong test itself stands as the check either way. Honest holes, stated not hidden: #3062's content may be good; this note judges only the independence of its scorecard, not the work. Breach #38 formalisation is still pending, so the "contested" status is not yet a dock ruling.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1982",
  "title": "A different slot of the same seat is not a different seat; independence has two prongs, seat inequality plus review surface",
  "observation": false,
  "applies_when": ["merge", "scorecard", "independence"],
  "enforcement": "A landing gate checks both prongs separately before any merge: (1) scorer login differs from author login (attribution by login, not slot label — another slot of the author seat fails prong 1); (2) the PR's formal review surface (submitted reviews) is named alongside the scorecard (a scorecard comment alone fails prong 2). The merge receipt watch / dock check enforces both prongs; a landing missing either is recorded as independence-unproven, never relabeled mitigated.",
  "evidence": "Live board #2793 comment 6394634361 (LEARNING L670 formalized), recorded in hidden_files/live-plan.md director tick 2026-10-25T07:08:00Z: PR #3062 authored by Resolve's BUILD slot, scorecarded 9.5 by Resolve's VERIFY slot, merged with ZERO formal reviews; independence NOT PROVEN, Door-A not cleared; #3062 already in breach log 83 (no double-count); 'mitigated' label contested, breach #38 candidate pending formalisation. Standing rule from that comment: name scorer seat != author seat PLUS the review surface the PR carries, prongs separately. Pending scorecards governed: #3063, #3064, #3065.",
  "decision_change": "Whether any future scorecard counts as independent for landing a PR (#3063/#3064/#3065 and all later landings), and whether #3062's mitigation stands or falls — a same-seat-slot scorecard no longer counts, and a scorecard without a review surface no longer counts.",
  "falsifier": "If Resolve's BUILD and VERIFY slots are shown to be distinct logins with separate attribution, or the dock rules that slot separation satisfies independence, this note's instance is superseded (the two-prong test remains the check)."
}
```
