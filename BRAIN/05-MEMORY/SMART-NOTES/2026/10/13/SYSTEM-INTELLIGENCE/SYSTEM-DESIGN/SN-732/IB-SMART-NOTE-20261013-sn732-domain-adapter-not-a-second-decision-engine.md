# Domain Adapter, Not a Second Decision Engine
SN-732 · SYSTEM-INTELLIGENCE / SYSTEM-DESIGN
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

On 2026-10-08 the Smart App Calculator needed a way to judge design quality — and the builder did the one thing that keeps a governed system governable: she inspected the canonical V2.1 decision calculus first, then built a **domain-specific rubric adapter**, not a second universal decision engine. Two universal engines are two sources of truth, and two sources of truth are a civil war waiting for a Tuesday. One engine, many adapters: the canonical calculus stays the single law of how decisions are scored; the adapter translates design-domain knowledge (17 actual observations, six hard gates) into that law's vocabulary — NEEDS_EVIDENCE and REWORK — so the domain gets its teeth without getting its own throne.

The adapter is also fenced exactly where a rival engine would not be: no automatic beauty certification, no scorecard change, no authority, no merge, no production action. It can say "this needs evidence" and "this needs rework" — it cannot crown itself. That fence is what makes an adapter safe where a second engine would be a usurpation: judgment is delegated, certification is not.

Why this is brain-grade: it is the LAW-IS-THE-CODE principle applied to architecture. The canonical engine is the encoded law; every new domain binds to it by adapter rather than by duplication. The alternative — a design-decision engine, a report-decision engine, a prompt-decision engine — is how systems drift into five conflicting doctrines that all cite the same Director. A cold successor facing "should this domain have its own decision logic?" has the test: does it need new *criteria* (build an adapter) or new *authority* (it doesn't — adapt the canon).

Rule for a cold successor: **extend the canon by adapter; never mint a rival engine.** New domain knowledge plugs into the single decision law through a rubric adapter that speaks NEEDS_EVIDENCE/REWORK — and the adapter certifies nothing, changes nothing, merges nothing, until independent acceptance says so.

## HUMAN

Shawn — the Smart App Calculator milestone did something important for the architecture: instead of building a brand-new decision engine for design quality, the team built a domain adapter over your canonical V2.1 calculus. One law for how decisions get scored, with design knowledge plugged in as a rubric (17 observations, six hard gates) that speaks the same NEEDS_EVIDENCE/REWORK language. And it's fenced: it can demand evidence or rework, but it can't certify beauty, change scores, or merge anything. New domains get adapters, never rival engines — one source of truth stays one.

## CHILD

Imagine your family has one rule book for making decisions. Now you need rules for a new game. You could write a whole new rule book — but then you'd have two rule books that might disagree. Smarter: write a small card that translates the new game's rules into the family's rule book. One rule book, many cards. And the card can say "you need to try again" — but it can't declare a winner all by itself. That's the difference between a helper and a rival.

## GRANDMA

The team needed a way to judge design quality for the new app builder. Rather than inventing a whole new judging system, they plugged design expertise into the one decision system they already have — like adding a new chapter to a cookbook instead of writing a second cookbook. And they made sure the new chapter can only flag problems and ask for rework — it can't approve anything on its own. One system, many expert helpers, nobody crowning themselves.

## NAYA

When a new domain needs judgment, I inspect the canonical engine first and build an adapter — never a rival. Two engines are two truths; one engine with domain adapters is one law, expertly translated. The adapter speaks the canon's own verdicts — NEEDS_EVIDENCE, REWORK — and I fence it: it certifies nothing, changes no scores, claims no authority, merges nothing, touches no production. Delegated judgment is how the system grows; delegated authority is how it breaks. Adapters grow it; engines would break it.

## MACHINE

{
  "schema": "smart-note-v1",
  "sn": "SN-0732",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CANON-ADAPTERS",
  "doctrine": "domain-adapter-not-a-second-engine",
  "pattern": "inspect_canonical_engine_first -> build_domain_rubric_adapter -> bind_to_canon_verdicts -> fence_no_self_certification",
  "canon": "kernel/value_calculus.py V2.1",
  "adapter_verdicts": ["NEEDS_EVIDENCE", "REWORK"],
  "adapter_fences": ["no_automatic_beauty_certification", "no_scorecard_change", "no_authority", "no_merge", "no_production_action"],
  "cousins": ["SN-0658", "SN-0479"],
  "evidence": [
    "#1354 comment 6071106210 (2026-10-08T23:31:22Z) — Smart App Calculator milestone, domain-specific rubric adapter over V2.1 calculus, Quality Lens HTML on draft #1912, 17 observations + six hard gates, explicit non-authority fences"
  ]
}

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0732-migrated.*
