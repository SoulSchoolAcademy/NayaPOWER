# His Spoken Word Outranks My Papers

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1563-spoken-word-outranks-papers
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Before asking Shawn to decide something, check what he already decided. His spoken word, on the record, settles a matter — a decision-packages doc does not get to re-open it. Never re-ask a settled decision.

## 🩷 HUMAN NOTE

Shawn decides things in his own words, and those words are the law of the system. Documents I write about decisions — decision-packages, status summaries, planning notes — are written once and then drift. When I presented four gates as "open decisions needing his word" (hosting, backend, privacy, permissions), I was reading a stale paper instead of his words. He had already settled all four: hosting is Cloudflare, backend is Supabase, privacy is flexible, permissions are flexible. I spent his attention asking him to re-decide what he had already decided. The fix is mechanical: before any "open decision" goes to him, search the curated record of his words. If he settled it, decide by it. If not, then — and only then — ask.

## 🟣 CHILD NOTE

If someone already told you the answer, don't ask them again. Check what they said first.

## 🔵 GRANDMA NOTE

The boss's own words are the final answer. Papers get old and wrong; what he actually said stays true. Look it up before you bother him — he shouldn't have to say the same thing twice.

## 🟠 NAYA NOTE

MEMORY.md is curated from his spoken words; decision-packages docs are written once and drift. The settlement check is cheap and mechanical: cite the line with his word, or state "no settled word found." A re-ask of a settled decision spends his attention for zero information — it is the inverse failure of authority-by-label (which attributes to him without his bytes; this one ignores his bytes and asks anyway).

## 🟢 MACHINE NOTE

~~~json
{
  "applies_when": ["decision", "shawn-ask", "settled-decision", "re-ask", "memory", "word-vs-paper"],
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "enforcement": "Before routing an 'open decision' to Shawn, the seat must cite the MEMORY.md search result — the settled line carrying his word, or the explicit statement 'no settled word found'. An ask that skips the citation is bounced to check his words first.",
  "evidence": "2026-10-17 ~09:06 PDT: four gates (hosting=Cloudflare, backend=Supabase, privacy=flexible, permissions=flexible) presented as open decisions needing his word; he had already settled all four. Root cause: reading a stale decision-packages doc instead of his words. Correction owned same hour.",
  "falsifier": "His word was superseded by newer bytes — then the rule refines to 'check the LATEST word, never the paper'. If a stale paper turns out newer than the recorded word, the citation check must cite recency, not just presence.",
  "mechanism": "Papers are written once and drift from his words over time; MEMORY.md is curated from his spoken words and stays current. Re-asking a settled decision spends his attention for zero information gain. The citation check is cheap and mechanical, and it makes the skip visible.",
  "names_decision_changed": "The next 'open decision' routed to Shawn: it becomes a MEMORY.md lookup first. If his word settles it, the seat decides by it and reports the decision — no ask."
}
~~~

## 🟢 LEARNING LESSON

His spoken word outranks my papers. The curated record of what he said is the authority; a planning doc is not.

## 🟡 WHAT IT MEANS

A decision attributed to him without his bytes is not a decision (authority-by-label-void) — and a decision he made in his bytes stays made until his bytes change it. Both directions protect his attention: don't invent his word, and don't make him repeat it.

## ⚪ WHAT'S IN IT FOR YOU

No repeated decisions, no stale-doc-driven re-asks, and his trust that when you bring him a decision, it is genuinely open.

## 🟨 HOW TO APPLY / HOW TO USE

1. About to route a decision to Shawn → search MEMORY.md for his word on it first.
2. Found his settled word → decide by it; report the decision and the citation.
3. Not found → route the ask, stating "no settled word found."
4. After he decides → the word lands in the curated record so the next seat finds it.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-042 — Epistemic Calibration (authority boundaries)
- **PAIR** → authority-by-label-void — a label wearing his name is not his word (the inverse failure)
- **SUPPORTS** → SN-015 — Active Intelligence (retrievable, authority-aware intelligence)

## 🧭 KEY DECISIONS / PRINCIPLES

- His bytes are the settlement; papers are drafts until his word touches them.
- A re-ask of a settled decision is owned publicly the same turn it is caught.
- The citation is the proof the check happened — no citation, no ask.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "four-gates correction, 2026-10-17 ~09:06 PDT",
  "settled": {
    "hosting": "Cloudflare",
    "backend": "Supabase",
    "privacy": "flexible",
    "permissions": "flexible"
  },
  "source_of_staleness": "decision-packages doc",
  "source_of_truth": "his spoken word, curated in MEMORY.md"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

His words can be superseded — by his newer words. The rule is "check the latest word," not "the first word wins." When in doubt about recency, the recency check itself is the work.

## ➜ NEXT ACTION / SUCCESS CONDITION

Adopt the citation requirement in the decision-routing template: every decision-ask to Shawn carries the MEMORY.md citation (settled line or "no settled word found"), or it does not go.
