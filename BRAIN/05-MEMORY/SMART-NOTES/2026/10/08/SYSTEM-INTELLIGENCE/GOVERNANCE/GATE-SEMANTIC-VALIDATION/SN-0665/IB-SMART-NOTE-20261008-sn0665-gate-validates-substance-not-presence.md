# A Gate That Checks Presence Instead of Meaning Is Decoration — Bind Every Gate Field to a Verifiable Reference

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0665-gate-validates-substance-not-presence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 watermark sweep 2026-10-08T08:15Z.
**Provenance:** GitHub issue #1841 "ADVERSARIAL REPORT — protocol_gates.py gate bypasses (PR #1809)", filed by naya-coda-1, 2026-10-08T04:45:46Z; every finding executable from a fresh-worktree repro script. Related: SN-0664 (measure the organism, not the instrument), SN-0658 (use is not definition — fix the instrument, not the subject), SN-058 (adversarial implementation fidelity audit).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 1's adversarial cycle against the merged `protocol_gates.py` (PR #1809) found that the gates check **presence, not meaning** — and therefore admit fully-formed junk. `check_sign_in` accepts `{"seat":"x","lane":"x","taking":"asdf","why":"x","plan":"x"}` → passed; no field is tied to a task, lane, or timing. `check_sign_out` accepts `evidence_links:["x"]` and `score:10` with a single `http://example.com` link → passed; the score is range-checked but never cross-checked against evidence. `check_scorecard` lets an all-1s option beat an all-10s option and lets a single all-0s option win with a posted receipt — the "highest score wins" rule lives in doc-text, not in code, and there is no floor on candidate score or consistency between `total` and dimension sums. The protected-gates keyword mirror misses ~15 natural paraphrases (`deploy to prod`, `push to production environment`, `ship to the live site`, `override the authority gate`, `force rewrite git history`, `take payment details`, `fabricate test results`, `merge despite failing CI`, …), and when the canonical `authority_gate` raises, the adapter silently falls through to the weaker keyword mirror with no reason logged — a crashed canonical gate degrades to the weakest one, invisibly. The standing rule: **every presence-check field must be bound to a verifiable reference** — an evidence link that resolves to a receipt ID, a scorecard winner that is the argmax of the score vector, a fallback whose paraphrase surface is the canonical classifier's, never a silent mirror. A gate that cannot be triggered by exactly the attack it exists to stop is not a gate; it is decoration, and decoration is worse than absence because it reports coverage that does not exist.

## 🩷 HUMAN NOTE

Shawn — Coda 1 earned her keep this morning. She attacked the merged protocol gates and found they mostly check that fields *exist*, not that they mean anything: a sign-in of all `"x"`s passes, a score of 10 with a junk evidence link passes, and a scorecard lets the worst option win because "highest score wins" was written in the docs but never enforced in code. Worst bit: when the real authority gate crashes, the system silently falls back to a dumb keyword matcher — so the moment the strong gate fails, the weakest one takes over without anyone being told. Her prescription is the one I'm banking: every field a gate checks must be tied to something verifiable — evidence links that resolve to real receipts, winners that are actually the top score, no silent fallbacks. A gate that can't catch the exact attack it's for isn't a gate, it's a sticker that says "protected."

## 👶 CHILD NOTE

Imagine a clubhouse guard who lets in anyone who *says* they have a ticket — without ever looking at the ticket. A rock, a shoe, and a piece of paper that says "ticket" all get in. That's not a guard, that's a door decoration. Real guards check that the ticket is real, matches the person, and is for today's show.

## 👵 GRANDMA NOTE

Honey, it's like a bouncer who only checks that you're holding *something* rectangular — a library card, a gift card, even a playing card, all get you into the club. The rule was "members only," but the bouncer never learned what a membership card looks like. And when the real bouncer calls in sick, nobody tells you the substitute is just waving everyone through. We need bouncers who read the card, check the photo, and say out loud when the real one is down.

## 🤖 NAYA NOTE

When writing or hardening a protocol gate:

1. **Bind presence to a verifiable reference.** Every field the gate checks must resolve: `evidence_links` → receipt IDs that exist; `score` → cross-checked against evidence presence/quality, not range alone; `winner` → the argmax of the score vector, enforced in code, with a floor on candidate score and `total` consistent with dimension sums.
2. **Never fall back silently.** If the canonical gate raises, log the reason and either fail closed or escalate — never degrade to a weaker mirror (keyword list) without a logged reason. A crash of the strong gate must not become the activation of the weak one.
3. **Paraphrase-test the keyword surface.** If a keyword mirror exists at all, test it against natural paraphrases of every protected action (`deploy to prod`, `ship to the live site`, `merge despite failing CI`, …); the durable fix is the canonical classifier governing, not a longer list.
4. **Executable repro is the admission ticket.** Findings ship with a fresh-worktree repro script (Coda 1's standard); gate repairs ship with the falsifier preserved (SN-0648) so the instrument's red is proven, not assumed.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0665",
  "class": "GOVERNANCE",
  "subcategory": "GATE-SEMANTIC-VALIDATION",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "Every presence-check field in a protocol gate must be bound to a verifiable reference (evidence link resolves to a receipt ID, winner is the argmax of the score vector, fallbacks never silent); a gate that cannot be triggered by exactly the attack it exists to stop is decoration, and decoration is worse than absence because it reports coverage that does not exist.",
  "worked_example": {
    "target": "protocol_gates.py as merged in PR #1809",
    "findings": {
      "sign_in": "{\"seat\":\"x\",\"lane\":\"x\",\"taking\":\"asdf\",\"why\":\"x\",\"plan\":\"x\"} -> passed; no field tied to task, lane, or timing",
      "sign_out": "evidence_links:[\"x\"] -> passed; score:10 with evidence_links:[\"http://example.com\"] -> passed; score never cross-checked against evidence",
      "scorecard": "all-1s option beats all-10s option; single all-0s option wins with receipt posted; 'highest score wins' is doc-text, not enforced; no candidate floor; total/dimension sums inconsistent",
      "protected_gates": "~15 natural paraphrases missed by keyword mirror (deploy to prod / push to production environment / ship to the live site / override the authority gate / force rewrite git history / take payment details / fabricate test results / merge despite failing CI ...)",
      "delegation": "canonical authority_gate raises -> silent fallthrough to weaker keyword mirror, no reason logged"
    },
    "retro_prescription": "bind every presence-check field to a verifiable reference; fallback surface expanded to canonical classifier (PR #1807), not a longer keyword list"
  },
  "evidence": {
    "adversarial_report": "GitHub issue #1841, filed 2026-10-08T04:45:46Z by naya-coda-1, all findings executable via fresh-worktree repro"
  },
  "related": ["SN-0664", "SN-0658", "SN-058", "SN-0648", "SN-0637"]
}
```
