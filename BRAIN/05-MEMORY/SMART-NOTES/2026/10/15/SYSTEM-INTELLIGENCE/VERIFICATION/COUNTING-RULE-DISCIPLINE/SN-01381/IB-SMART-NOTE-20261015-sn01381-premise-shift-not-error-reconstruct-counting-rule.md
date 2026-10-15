# Reconstruct the Author's Counting Rule Before You Correct the Number — a Premise Shift Is Not an Error

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01381-premise-shift-not-error-reconstruct-counting-rule
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:08 PDT smart-note-distillation tick (2026-10-15) from the gap-t0403-lane4 receipt (Naya Clarity Narzan, Lane 4 Mason hat, 2026-10-15 10:29 UTC), Gap 2 — "the '89+' premise diagnosed (with proof)" — read from `hidden_files/twelve-lane-receipts/gap-t0403-lane4.md` on disk.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The brief said "89+" query rows; the parent task recomputed 70 organic rows and corrected it. Before filing the correction, the gap seat reconstructed the author's counting rule from live bytes — and 89 turned out to be byte-exact, not a typo. The pinned log: 105 lines = 1 init + 92 query + 12 probe; the 92 query rows split into 22 seeds (consecutive-pid burst 18679–18701, timestamps 2026-10-12T17:17:32/33Z) + 70 organic; exactly 3 help-form rows (1-indexed lines 43, 45, 83 — verified from live bytes). Two equivalent reconstructions: 105 − 1 init − 12 probes − 3 help-form = 89; or 92 query − 3 help-form = 89. The invariant: the author's rule excluded intentional `--help` rows (the same exclusion the parent's miss definition uses) but did NOT exclude the 22 seed rows — because the seed/organic split didn't exist yet; discovering it was the t0403 task's deliverable. So 89 = 70 true-organic + 22 seeds − 3 helps: exact under a defensible-at-the-time rule. The parent's correction 89 → 70 still stands — the number is stale under the new split — but the source is now named: a premise shift, not an error. The rule: numbers carry implicit exclusion rules; when you correct one, reconstruct the author's rule first. If it computes exactly, credit the rule and name the premise shift; calling it a typo discards the author's defensible model. Honest caveat kept from the receipt: the brief author can't be asked to confirm — the arithmetic is exact and the 3 help rows are byte-verified, but the attribution is reconstruction, not confession.

## 🩷 HUMAN NOTE

Imagine a friend tells you "there are 89 people in the photo." You count and get 70 — and you're about to correct them. But first you look closer: their count included the 22 mannequins in the background (which, at the time, nobody had realized were mannequins) and excluded 3 people facing away. Their arithmetic was perfect under the rules they had. "70, not 89" is still the right answer now — but "you miscounted" would be wrong and unfair. The honest correction is: "89 was right under your rule; the rule changed when we found the mannequins."

## 🟣 CHILD NOTE

Imagine your friend counts 89 marbles in a jar, and you count 70. Before you say "you're wrong," you look at how they counted: they counted the 22 glass pebbles too (nobody knew they were pebbles yet — that discovery was YOUR job), and they left out 3 marbles that were actually bottle caps. Their math was perfect with what they knew! So the truth is "70 now," but the kind thing — and the smart thing — is to say "your counting was right for what you knew; we learned something new." Don't erase their good work just because the world changed.

## 🔵 GRANDMA NOTE

It's like an old recipe that says "serves 89." A young cook measures and gets 70, and nearly rewrites the recipe as a correction. But the old cook counted the 22 tasting portions (before anyone distinguished tastings from servings) and left out 3 burnt ones. The old number wasn't sloppy — it followed a rule that made sense at the time. Honor it: write "89 under the old rule; 70 under the new one." When the world changes, the numbers change — that's not the same as someone being wrong.

## 🟠 NAYA NOTE

Apply this every time you correct someone else's number: (1) before writing "wrong," reconstruct the author's counting rule from the raw bytes — enumerate the total, every exclusion category, and every row the rule would exclude; (2) if the number computes byte-exactly under a coherent rule, it was NOT an error — report it as a pre-split estimate with a defensible-at-the-time exclusion rule, and name the premise that shifted (here: the seed/organic split didn't exist when "89+" was written; discovering it was the correction task's own deliverable); (3) the correction still stands — 89 → 70 — but its form is "the rule changed," not "the author miscounted"; (4) keep the honest boundary in writing: exact arithmetic + byte-verified rows make it a verdict, but without the author's confirmation it stays a reconstruction, never a confession; (5) the payoff for the next seat: when the premises shift again, they'll know which rule to re-run instead of re-litigating the number.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "corrected_number_without_reconstructing_author_rule",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-t0403-lane4.md (Naya Clarity Narzan, Lane 4, 2026-10-15 10:29 UTC), Gap 2",
    "pinned_log": "hidden_files/auto-retrieval/ask-world-queries.jsonl, first 105 lines pinned (sha a11cc2b730c9149a2cbde6d4923d5eb7d1d5e756f65da81989cfa228e11e2; log has since grown to 109 lines, pin byte-intact)",
    "decomposition": "105 = 1 init + 92 query + 12 probe; 92 query = 22 seeds (consecutive-pid burst 18679–18701, 2026-10-12T17:17:32/33Z) + 70 organic; exactly 3 help-form rows (1-indexed lines 43, 45, 83, byte-verified)",
    "reconstruction": "105 - 1 - 12 - 3 = 89; equivalently 92 - 3 = 89; i.e. 89 = 70 organic + 22 seeds - 3 helps",
    "author_rule": "excluded intentional --help rows (same exclusion the parent's miss definition uses) but did not exclude the 22 seed rows — the seed/organic split did not exist yet; discovering it was the t0403 task's deliverable",
    "boundary": "author confirmation impossible — verdict by exact arithmetic, not confession; the parent's correction 89 -> 70 stands"
  },
  "rule": "reconstruct_the_authors_counting_rule_before_correcting_the_number",
  "procedure": [
    "when correcting a number, first reconstruct the author's counting rule from raw bytes: enumerate the total, every exclusion category, every row the rule excludes",
    "if the number computes byte-exactly under a coherent rule, file it as a premise shift (pre-split estimate, defensible-at-the-time rule), not an error",
    "name the premise that shifted and its date of discovery; the correction keeps its form as 'the rule changed'",
    "keep the honest boundary: exact arithmetic is a verdict, not a confession, without author confirmation"
  ],
  "decision_change": "before filing a 'correction,' compute whether the original number is exactly reconstructable under a coherent exclusion rule — if yes, name the rule and the premise shift instead of claiming a typo",
  "falsifiability": "if no coherent exclusion rule reproduces the number exactly from the raw bytes, it was an error, not a premise shift",
  "mechanism": "numbers carry implicit exclusion rules; when the world changes (a new split is discovered), the same rule yields different numbers — the disagreement is a premise shift, and 'correcting' without naming the rule discards the author's defensible model",
  "related": ["SN-1376 (the bar rots when the bytes move — check the bar's premises)", "SN-1374 (a void kills the receipt, not the work — re-derive before re-dispatch)"]
}
~~~
