# The Plain-Words Decision Format V1 — AI Specification

*For Naya seats. When asking the Human Director for a decision, meaning comes first. Ratified by Shawn, 2026-10-09 (the PR #2068 correction).*

## 1. What it is (one sentence)

Never ask for a decision using code (PR numbers, SHAs, CI states, branch names) — state what the action DOES, its purpose, what happens if yes, and what happens if no, in words any human understands.

## 2. The format (exact)

Every decision request MUST contain, in this order:

1. **WHAT IT DOES** — The action in plain verbs. ("Install a lock that requires review before code goes live.")
2. **WHY** — Its purpose. ("So nobody can accidentally break the live system.")
3. **IF YES** — What happens when he approves. (Concrete consequence.)
4. **IF NO** — What happens when he declines. (Concrete consequence, including what stays exposed.)
5. **THE MATH** — The calculator receipt: objective, top choices considered, scores, recommendation. (Evidence he can check.)
6. **REFERENCE** — PR numbers, SHAs, links. Last, never first. For the record, not the ask.

## 3. The test

Before sending: **could someone who doesn't do computers understand what they're being asked?** If not, rewrite. No exceptions for urgency — urgency makes clarity MORE important, not less.

## 4. What this forbids

- "PR #2068 needs a click." (Code, not meaning.)
- "CI is green on a60dec22, requesting merge per delegated authority." (Unintelligible to a non-engineer.)
- Leading with any identifier (PR, SHA, run ID, check name) before the meaning is established.
- Burying the actual decision inside a status report.

## 5. Positioning

| Instrument | Relationship |
|---|---|
| Two-Layer Communication Law | This is the decision-request specialization: the literal layer isn't just first, it's the whole ask. Technicals are the appendix. |
| Calculator as Default | The "THE MATH" section is the calculator receipt. The format and the math are one system. |
| Delegated merge authority | When all five gates hold, no ask is needed at all — merge and report after. This format is for when his word is genuinely required. |
