# Plain-English Law — Standing Directive v1

**Status:** Human-Director directive, effective immediately; implementation artifact pending review/merge.  
**Scope:** Every Team Naya status update, handoff, report, PR summary, scorecard, blocker notice, and completion claim.

## The law

Every update MUST contain these two parts, in this order:

1. **THE TECHNICAL** — exact facts: what changed, where, by whom/which seat, commit or run/receipt evidence, observed result, score delta (if any), remaining blocker, and next action.
2. **LITERALLY WHAT I'M SAYING** — a plain-language translation that lets a non-specialist picture what happened, what it means, what still does not work, and what happens next.

Both parts are mandatory. A technical statement without a plain-English translation is incomplete. A plain-English claim without supporting technical evidence is ungrounded.

## Required truth boundaries

- Separate **built**, **tested**, **merged**, **deployed**, and **proven in production**.
- Separate **capture/activation**, **behavior change**, and **cold-successor reuse**.
- Never call a note “learned” merely because it was stored, indexed, retrieved, or linked.
- Name the first broken link, not a vague list of possible causes.
- If a cause is unknown, state exactly what evidence would discriminate the possibilities and who owns obtaining it.
- Every claimed pass must identify its artifact: commit SHA, test/run URL, receipt, measured outcome, and independent verifier where required.
- Never claim that an agent was assigned, a workflow dispatched, a fix deployed, or a test passed unless the corresponding durable receipt exists.
- Translate acronyms and errors on first use. Keep technical details available; do not replace precision with simplification.
- End each update with the highest-value next action and its owner. Ask Shawn only for a real human-authority decision that cannot be inferred from ratified law or current evidence.

## Copyable update template

### THE TECHNICAL
- **State:** PROVEN / PARTIAL / BLOCKED / UNKNOWN
- **Change:** exact file, PR, commit, deployment, or database/runtime object
- **Evidence:** test/run/receipt URL and raw observed result
- **Score:** before → after, with the exact score-contract rung earned; otherwise “no change”
- **First broken link:** one specific failure or “none observed”
- **Owner + next action:** named seat and one executable action

### LITERALLY WHAT I'M SAYING
Explain in ordinary words:
- what now works;
- what does not yet work;
- how we know;
- what the user can actually do right now; and
- what will happen next.

## Acceptance test

An update passes only if a reader can answer all five questions without translating jargon:
1. What changed?
2. How do we know?
3. What can I use right now?
4. What remains broken or unproven?
5. Who does what next?

This law governs communication, not evidence thresholds. Clear wording does not turn an unverified claim into a verified one.
