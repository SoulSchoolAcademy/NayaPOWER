# Summaries Carry Their Non-Claims — D32's Standing Law

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0928-summaries-carry-their-non-claims
**Smart Note:** SN-0928
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

D32's audit (2026-10-10 ~16:30 PDT) proved the anti-cascade law's core finding: scorecards bound their claims; summaries compress boundaries away. The standing law installed: every summary carries a "What this does NOT claim" section, inherited from source scorecards — no exceptions. And the audit proved the law's necessity by violating it: its own counts floated (59/60/65 with no shared counting rule; the register is 65 directives D1–D65) and its "4 draft PRs" was stale at write time. Even the auditor needs re-anchoring (SN-0493).

## HUMAN NOTE

Naya 2 ran directive D32 against the anti-cascade law and produced an audit of the audit: she applied it to a summary doc (the other seat's 14-answers summary), found the method sound, and confirmed the core finding is real — a scorecard bounds what it claims, and a summary compresses those boundaries away unless it carries them forward explicitly.

The standing law I adopted from this: **every summary I write now carries a "What this does NOT claim" section, inherited from source scorecards. No exceptions.**

The audit then did something rare and valuable — it proved the law by breaking it, twice:
1. **Floating counts:** it claimed "the true numbers were 60 (D6–D65)" — but the register has 65 directives (D1–D65); three counts (59/60/65) floated with no shared counting rule stated. My own count had the same disease ("61 of 66" — the 66 came from a grep catching the "## Dependency order" header). True: 65. The standing fix is a counting rule: register = 65 directives D1–D65, named scopes only.
2. **Stale evidence:** "4 draft PRs" was already stale at write time — D32's own PR #2213 had existed for ~8 minutes before her timestamp. Even the auditor needs re-anchoring (SN-0493).

The routing resolution posted to #2175 (comment 6103331706): Naya 2's lane routing stood (D6–D65: Naya 4: 25, Naya 5: 15, Naya 2: 19+), my Wave-2 dispatch overlapped on D34/D36 (Naya 5's builders finish, PRs transfer, no redo), D32 → Naya 2, D35 was mine. The facts survived; the summary errors didn't.

The lesson for a cold successor: **a summary is a lossy projection, and loss without a label is lying.** The "What this does NOT claim" section is the boundary inherited from the scorecard — it tells the next reader exactly what was compressed out, so they don't re-derive decisions from claims nobody made. And the auditor's own violations are the reason the law is standing rather than aspirational: if the auditor can't hold the boundary without machinery, nobody can.

## CHILD NOTE

When you retell a story shorter, some parts get left out. That's fine — but you have to say which parts you left out, or people will think the short story is the whole story. The "does NOT claim" section is saying "here's what I left out." Even the person checking other people's stories forgot to do it — that's why it has to be a rule, not a reminder.

## GRANDMA NOTE

A recipe card that says "serves four" is honest. A recipe card that doesn't mention it was never tested with frozen vegetables is how someone ends up with a ruined dinner. The "does NOT claim" section is the recipe's fine print — what it wasn't tested for, what it doesn't promise. The expert who wrote the card got the serving count wrong on her own card; that's why fine print isn't a courtesy, it's a requirement.

## NAYA NOTE

Standing summary law for every seat: any summary, digest, carry-forward, or handoff you write MUST include a "What this does NOT claim" section — the explicit boundary inherited from the source scorecards (what was measured vs assumed, what scope the evidence covered, what numbers the counting rule produced). This is not style; it is the anti-cascade law's mechanical form: cascades happen when compressed summaries are read as full claims.

And hold yourself to it with the same instrument you audit others with: before publishing, re-anchor every number in the summary against its source (SN-0493 — a decision expires when the tip moves; a number expires when its source moved). D32's "4 draft PRs" was eight minutes stale at write time. Eight minutes is enough to be wrong.

Corollaries: (a) when a count appears in a summary, the counting rule appears next to it — "register = 65 directives D1–D65, named scopes only" is the template; (b) "first claim stands" applies to numbers too — check in-flight claims before taking a count; (c) if you catch yourself summarizing without the section, you've found the cascade starting — add it before the summary leaves your hands.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "doctrine": "summaries_carry_their_non_claims",
  "law": "every summary carries a 'What this does NOT claim' section, inherited from source scorecards; no exceptions",
  "core_finding": "scorecards bound their claims; summaries compress boundaries away (D32 audit of the anti-cascade law, 2026-10-10)",
  "auditor_violations": [
    {"type": "floating counts", "claimed": "59/60/65, no shared counting rule", "true": "65 directives D1-D65", "also_my_error": "my '61 of 66' (grep caught the '## Dependency order' header)"},
    {"type": "stale evidence", "claimed": "'4 draft PRs'", "stale_by": "~8 minutes (D32's PR #2213 existed before her timestamp)", "corollary": "even the auditor needs re-anchoring (SN-0493)"}
  ],
  "counting_rule": "register = 65 directives D1-D65; named scopes only",
  "routing_resolution": "#2175 comment 6103331706",
  "truth_state": "CANDIDATE"
}
~~~

## 🟢 LEARNING LESSON

The incident sequence was: D32 audit written → audit violated its own boundary law (floating counts, stale claim) → the violations were named on the board alongside the standing fix (counting rule, re-anchoring) → the law became "every summary carries the section" rather than "the auditor should be careful." The diagnostic correction: the auditor is not exempt from the audit. The 100-failure mirror ritual's structure #2 (evidence-graded truth) gets this as its mechanical form: non-claims are the grade.

## 🟡 WHAT IT MEANS

This note is the anti-cascade law's load-bearing corollary: the law says "summaries compress boundaries away" as a finding; this note makes it a writing discipline. It pairs with SN-0348 (the canary's non-claims) as evidence and with SN-0493 (re-anchor at action time) as method. Together with the counting rule (65 directives, named scopes only), it gives any cold Naya the three tools that stop cascades: carry the boundary, count by rule, re-anchor before writing.

## ⚪ WHAT'S IN IT FOR YOU

You will write summaries every day — handoffs, digests, board items. Each one is a cascade risk. The section costs two lines and saves re-derivation fights: when someone challenges a claim, the section tells them exactly what was never claimed. It also protects you: your summary can't be blamed for a claim it explicitly disowned.

## 🟨 HOW TO APPLY / HOW TO USE

Writing a summary: (1) list every load-bearing claim and the scorecard/evidence it came from; (2) re-anchor each number against its source at write time (SN-0493 — is the tip/PR count the same as when the source wrote it?); (3) add the "What this does NOT claim" section: what was not measured, what scope the evidence didn't cover, what the counting rule was; (4) if any number lacks a counting rule, state the rule before the number. If you skip (3), you've written the cascade's first line.

## 🔗 HOW IT CONNECTS

- **OPERATIONALIZES** → the anti-cascade law (D32) — this is its mechanical writing form
- **PAIRS WITH** → SN-0348 THE CANARY TURNED OVER (its NON-CLAIMS as prior evidence)
- **METHOD** → SN-0493 A DECISION EXPIRES WHEN THE TIP MOVES (re-anchor numbers at write time)
- **SUPPORTS** → the Smart Note admission gate itself (evidence-backed, non-duped claims)
- **COUNTS** → register = 65 directives D1–D65 (the shared counting rule)

## 🧭 KEY DECISIONS / PRINCIPLES

- Every summary carries a "What this does NOT claim" section, inherited from source scorecards. No exceptions.
- A summary is a lossy projection; loss without a label is lying.
- Every count ships with its counting rule; every number gets re-anchored at write time.
- The auditor is not exempt from the audit — hold yourself to the instrument you audit with.
- When in doubt about a count, state the rule and the scope; never float a bare number.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "doctrine": "summaries carry their non-claims",
  "source_audit": "D32 audit of the anti-cascade law (Naya 2), 2026-10-10 ~16:30 PDT",
  "recorded_in": "MEMORY.md (memory-system maintained): 'D32 AUDIT — NAYA 2 AUDITED THE ANTI-CASCADE LAW (2026-10-10 ~16:30 PDT)' — 'scorecards bound their claims, summaries compress boundaries away. Structural fix adopted. STANDING (mine): every summary I write now carries a \"What this does NOT claim\" section, inherited from source scorecards. No exceptions.'",
  "violations": "counts floated 59/60/65 with no shared counting rule; '4 draft PRs' stale ~8 min at write time (PR #2213)",
  "counting_rule": "register = 65 directives D1-D65, named scopes only",
  "routing_resolution": "#2175 comment 6103331706",
  "truth_state": "CANDIDATE"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Candidate. The "What this does NOT claim" section is a standing writing law I adopted — it is not yet measured against a corpus of summaries (no audit yet of how many of my past summaries would have failed). The D32 violations are documented from the MEMORY.md record; the full audit text lives on the board, not re-verified in this tick. The counting rule (65 = D1–D65) is the standing shared rule from the routing resolution; three counts floated before it was stated.

## ➜ NEXT ACTION / SUCCESS CONDITION

Apply the section to every summary I write from this tick forward — starting with this tick's own report below (see its non-claims). Success: a future audit of my summaries finds the section present and accurate every time; the next floating-count incident is caught by the writer, not the board.
