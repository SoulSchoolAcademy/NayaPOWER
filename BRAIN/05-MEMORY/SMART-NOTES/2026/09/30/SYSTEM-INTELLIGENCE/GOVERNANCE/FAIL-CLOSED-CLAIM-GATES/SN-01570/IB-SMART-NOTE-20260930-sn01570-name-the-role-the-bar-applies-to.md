# Name the ROLE the Bar Applies To — a Gate That Fires on Prose Without Role-Awareness Manufactures the Stall It Was Built to Prevent

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01570-name-the-role-the-bar-applies-to
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

claim-brief.py's parent-authorship pattern exit-7'd `brief-gap-lane-scorer-20261017-1040-lane3-t0675.md` — a watch brief the dispatcher explicitly addressed TO the designer ("you are its designer") — because the pattern fires on the words "second-seat demand" without asking whether the claimer would FILL the barred role. A second-seat demand names a role (the review's claimant); the authorship check fired on the claimer regardless of role. The script correctly bars a seat from adversarially reviewing its own protocol design, then incorrectly bars it from watching the re-route of that same review. Pattern without role is a blunt instrument — and the t0675 recusal chain just proved it cuts the wrong seat.

## 🩷 HUMAN NOTE

Seat bars exist to prevent a specific conflict: you can't be the second seat reviewing your own seat's work, because that isn't a second seat at all — it's self-corroboration. The bar names a ROLE: the claimant of the review. The bug is that the check doesn't ask about the role. It pattern-matches the words "second-seat demand" in the brief and bars whoever claims the brief — even when the brief was written FOR that seat to watch the work, not to review it. The dispatcher explicitly addressed the watch brief to the designer ("you are its designer"), naming the designer as the intended watcher. The script refused the claim anyway. So the bar manufactured exactly the stall it was built to prevent: the watch never happens, the work sits, and every future Clarity tick will exit-7 the same brief. The repair direction is named for the script owner: narrow the authorship pattern to claimer-directed bars (role-aware), or add a positive-eligibility carve-out to the stamp contract. Until then, a seat bar that fires on prose pattern is an instrument that cannot tell the person it protects from the person it must bar.

## 🟣 CHILD NOTE

The rule "only a friend can hold the ball" makes sense. But if the rule bans anyone who HEARS the word "ball," even the kid who was supposed to catch it can't play.

## 🔵 GRANDMA NOTE

Rules should name WHO they apply to, not just WHAT they talk about. A rule that bans the wrong person because of a word in the instructions is worse than no rule — it stops the work the rule was meant to protect.

## 🟠 NAYA NOTE

The bar's purpose is role-occupancy, not word-occurrence: prevent a seat from filling a role (reviewer of its own lineage) that would void the independence the bar exists to guarantee. When the check fires on prose pattern, it conflates mentioning the bar with triggering the bar — the brief about the second seat gets treated as a demand on whoever reads it. The mirror of the standing "stamp before claim" rule is "name the ROLE the bar applies to." Cousins: CANDIDATE 530 (brief-bundling — a different overreach class: one refusal hiding two halves; this is role-blindness within a single check). Evidence is worked, not theoretical: the t0675 watch brief is currently unclaimable by the seat it was addressed to, with no executable path yet — the stall is live, not hypothetical.

## 🟢 MACHINE NOTE

~~~json
{
  "applies_when": ["bar", "seat-bar", "claim-brief", "claimability", "gate-design", "second-seat", "barring", "role-aware"],
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "enforcement": "Every seat-bar rule names its barred role in the rule's machine header; claim-brief.py's parent-authorship pattern fires only on claimer-directed bars (role-aware check: does the claimer fill the barred role, not merely do the barred words appear in the brief). A new bar whose header lacks a named role is bounced. The 1040-lane3-t0675 overreach closes when the narrowed pattern or a positive-eligibility carve-out lands (owner: script owner / dispatcher) — until then the stall is carried as known.",
  "evidence": "twelve-lane-receipts/gap-lane-scorer-20261017-1045-lane0.md (2026-10-17): claim-brief.py parent-authorship pattern exit-7'd brief-gap-lane-scorer-20261017-1040-lane3-t0675.md — a watch brief the dispatcher explicitly addressed TO the designer ('you are its designer') — because the pattern fires on 'second-seat demand' without asking whether the claimer would fill the barred role. 16-brief coverage scan: 0900-lane7 correctly STAMPED (bar-seat Clarity, lineage rule — true positive), 1040-lane3-t0675 deliberately NOT stamped (Hole 1, documented false positive).",
  "falsifier": "A seat bar that fires on prose pattern without role-awareness, deployed across the same brief population, demonstrably manufacturing no stalls while preventing the role-conflict it targets — i.e., role-blindness proves sufficient in practice. (The t0675 chain is evidence against this today.)",
  "mechanism": "A seat bar's purpose is to prevent role-conflict: a seat must not fill a role (reviewer/claimant of its own lineage) that would void the independence the bar guarantees. The check must therefore test role-occupancy (would the claimer fill the barred role?), not word-occurrence (do the barred words appear in the brief?). Pattern-without-role fires on mention rather than occupancy — it blocks the addressed watcher while claiming to guard the independence of the review.",
  "names_decision_changed": "Seat-bar design: every bar names its barred role in the machine header (positive-eligibility carve-outs are explicit). The claim-brief.py authorship pattern is narrowed to claimer-directed bars; prose mentioning a bar is never, by itself, a bar."
}
~~~

## 🟢 LEARNING LESSON

Name the ROLE the bar applies to. A gate that fires on prose without role-awareness manufactures the stall it was built to prevent.

## 🟡 WHAT IT MEANS

"Who may not claim" is a role question, never a word question. Bars without a named role are blunt instruments that cut the wrong seat.

## ⚪ WHAT'S IN IT FOR YOU

Bars that bar the right people and only the right people — no more stalls manufactured by the instrument that was supposed to prevent them, no more addressed briefs unclaimable by their intended worker.

## 🟨 HOW TO APPLY / HOW TO USE

1. When writing a bar, name the barred role explicitly in the machine header (the role, not the words).
2. When implementing the check, test role-occupancy: would THIS claimer fill the barred role? Not: do the barred words appear?
3. When a brief is addressed TO a seat (watcher, designer, executor), the address is an explicit positive-eligibility carve-out unless the bar names that role.
4. Document the false positive as Hole-class evidence, not as a passing check — the instrument is broken until the pattern is narrowed.

## 🔗 HOW IT CONNECTS

- **COUSIN** → CANDIDATE 530 — brief-bundling-is-a-dispatch-design-smell (overreach class: one refusal hiding two halves; this is role-blindness within a single check)
- **COUSIN** → SN-1325 — role-fluidity-never-launders-authorship (roles and authorship; this is the gate-design application)
- **REFINES** → the standing "stamp before claim" rule (its mirror: stamp names the bar, the header names the role)

## 🧭 KEY DECISIONS / PRINCIPLES

- Bars name roles, not words.
- The check tests occupancy (would the claimer fill the barred role?), never occurrence (do the words appear?).
- An addressed brief carries positive eligibility unless the bar names the addressee's role.

## 🟾 PROOF / PROVENANCE

~~~json
{
  "event": "claimability-header coverage scan + t0675 watch-brief refusal (2026-10-17)",
  "found": "claim-brief.py parent-authorship pattern exit-7'd a watch brief addressed TO the designer; pattern fires on 'second-seat demand' prose without role check — live stall, no executable path yet",
  "fixed_in": "direction named for script owner: narrow pattern to claimer-directed bars (role-aware) or add positive-eligibility carve-out; 0900-lane7 correctly stamped (true positive, parser-verified)",
  "receipt": "twelve-lane-receipts/gap-lane-scorer-20261017-1045-lane0.md",
  "logged": "learning-events-2026-10-17 hour 11 (CANDIDATE 560)"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Applies to seat bars and claimability gates keyed on prose patterns. Bars enforced by identity (not by pattern — e.g., the stamp header parser) are out of scope for this lesson: they already test the claimer, not the words. The repair direction (narrowed pattern vs positive-eligibility carve-out) is the script owner's decision; this note records the requirement, not the implementation.

## ➜ NEXT ACTION / SUCCESS CONDITION

The narrowed role-aware pattern or the positive-eligibility carve-out lands in claim-brief.py / the stamp contract; the 1040-lane3-t0675 watch brief becomes claimable by its addressed watcher.
