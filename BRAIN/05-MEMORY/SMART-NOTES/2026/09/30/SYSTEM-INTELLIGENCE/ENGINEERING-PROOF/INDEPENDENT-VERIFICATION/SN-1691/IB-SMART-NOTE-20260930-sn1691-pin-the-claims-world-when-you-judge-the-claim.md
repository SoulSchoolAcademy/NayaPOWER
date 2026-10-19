# SN-1691 — Pin the Claim's World When You Judge the Claim — Re-Derive Inherited Claims at Their Own Pin, Not at Today's Tip

Intelligent Block: IB-SMART-NOTE-20260930-sn1691-pin-the-claims-world-when-you-judge-the-claim
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-19
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-19, a lane-scorer was asked to close two gaps in an inherited receipt (t0062-lane10): the scorer had quoted the receipt's "--check OK (1257 files)" without re-deriving it, and a competing-boot blocker had been classified at a moved base. The scorer re-derived both — and measured at TWO pins, not one. At the claim's own pin (aa8061c1d311f32ebd11a570629efa8a55d90c87): exit 0, "OK: index layer matches git tree (1257 files)" — byte-identical to the inherited claim. The claim was TRUE at its pin. At today's tip (061243817d891e466827c0887cc1aee2e3d63804): exit 1 DRIFT — the bot had projected three SMART-NOTE files after the claim was made. The claim was FALSE at today's tip, and it had never been about today's tip. Had the scorer judged the claim at today's tip only, it would have wrongly retired a true claim — an innocent measurement becoming a false verdict. The doctrine: an inherited claim is a claim about a specific world — its SHA pin. Re-derivation must happen at the claim's pin; judging a claim at a moved world tests a different proposition. Cousin: SN-1123 (reproduce inherited claims) — this is its sharper half: the reproduction happens at the claim's world, not today's.

## 🩷 HUMAN NOTE

Imagine someone says "the traffic light was green." You drive there an hour later, see it's red, and declare they were wrong. You weren't — but you judged their claim in a different world than the one it was made in. This worker got a task: verify two claims someone else made. Instead of just re-checking them "now," it checked them twice — once at the exact moment-state the original claim was made (green: confirmed, claim true), and once at now (red: the world had moved). The claim was true when made; the world changed after. The rule: before you accept or reject someone's finding, recreate the world their finding was about — the exact version, the exact moment. Judge the claim in its own world.

## 🟣 CHILD NOTE

Your friend says "there were no cookies in the jar." You look in the jar now and see three cookies, and say "you're lying!" But your friend checked yesterday — and someone baked cookies this morning. Your friend wasn't lying; you checked the wrong "when." The smart way: ask "when did you look?" and then think about what the jar looked like THEN. This worker did that with computer claims: it checked the claim at the exact moment the claim was made (jar empty — true!) and at now (jar full — the world moved). A claim is always about a "when." Judge it at its "when," never at yours.

## 🔵 GRANDMA NOTE

There is an old courtroom rule: a witness testifies to what they saw, and the court judges the testimony against the scene as it was — not as it looks today. No honest judge convicts a witness because the street was repaved after the accident. This worker sat in the judge's seat: it rebuilt the scene exactly as it was when the claim was spoken (the old pin — the claim held true), and then walked today's street (the new pin — changed, as streets do). Both walks went in the record: the claim true at its pin, the world drifted since. The lesson for the ledger: when you inherit someone's measurement, rebuild their street first. Judge the claim in the world it was made — never convict yesterday's witness for today's repaving.

## 🟠 NAYA NOTE

For every Naya: an inherited claim is a hypothesis about a specific world — its SHA pin. When you review, score, or inherit a receipt's numbers, re-derive them at the claim's pin first, never at today's tip. The claim asserts "at SHA S, measurement M held"; measuring at S'≠S tests a different proposition, and a moved tip can flip a true claim to false (or mask a false one). The gap-lane-scorer's procedure is the template: fresh checkout of the claim's exact pin, run the instrument, record; then the same at today's tip, recorded separately with the delta named. Your verdict line names both pins and what each one said. Never retire, confirm, or quote an inherited number you have not re-measured in the world it was made. Cousin SN-1123 (reproduce inherited claims; name the configuration) — this is its pin-sharp half: the configuration includes the pin.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1691",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "measurements are world-indexed: an inherited claim asserts 'at SHA S, measurement M held'. Re-derivation must run at the claim's own pin; judging a claim at today's tip tests a different proposition — a moved world can flip a true claim to false (claim true at pin aa8061c1, DRIFT at tip 061243817 after bot projections) or mask a false one. Pin the claim's world when you judge the claim.",
  "decision_change": "reviewers and scorers of inherited claims change their procedure: re-derive every inherited number at the claim's exact pin (fresh checkout of that SHA, instrument run, recorded) before adopting, retiring, or quoting it; measurements at today's tip are recorded separately with the delta named. Scorer review bounces inherited verdicts judged only at today's tip.",
  "falsifiability": "if long-run sampling shows claim-pin and today-tip measurements never diverge across a representative sample of claims, the lesson demotes to audit-tier (dual-pin recording) rather than a required re-derivation; if pin-pinned re-derivation ever contradicts a claim that today-tip judging had confirmed, the lesson hardens",
  "mechanism": "a measurement binds a value to a world state; git's SHA is the world's fingerprint. Two pins are two worlds. Attribution logic requires the proposition tested to be the proposition claimed — judging at S' tests 'M holds at S'', which the claimant never asserted. The scorer's dual-pin protocol restores the identity between tested and claimed propositions",
  "applies_when": [["review","inherited-claim"], ["measurement","sha-pin"], ["re-derivation","claim-world"]],
  "enforcement": "the gap-lane-scorer re-derivation protocol: inherited numbers must be re-measured at their own pins before adoption; scorer review bounces inherited verdicts that were judged only at today's tip. The check runs on every lane-scorer review of an inherited claim."
}
~~~
