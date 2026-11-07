# Promotion Is Atomic: Verify First, Move the Pointer Last

SN-2246 · LESSON / DISTILLATION

**Created:** 2026-11-07 23:11Z

## IN A NUTSHELL

Production is the truth; the ledger is a claim. Verify before you mutate: the pointer move is the commit point, last, after every check is green. A hash binds content, never identity — an unkeyed promotion seal is a forgery machine with good paperwork, so bind promotion to an authenticated grant. Ledgered migrations are immutable, even for comment edits — correct the record elsewhere. A deployment authorization expires at its SHA. External REDs go to their canonical owner — never spoof a check, never weaken a gate, never merge around the red. When documentation outruns proof, write "not ready to promise publicly yet," list the gaps, and name the gate. A single passing check is a hypothesis, not a verdict — require a second independent check.

## HUMAN

The promotion pipeline moved the production pointer before the database check ran — so two "deployments" happened in one morning that never landed a single migration, and production now claimed deployments the database could not back up. The design answer is atomicity: authorize, freeze, validate the target, deploy, verify the deployment, confirm independently — and only then advance the pointer. Steps one through six are preparation; step seven is the commit. If anything earlier fails, step seven never executes. The same ordering law governs the smaller pieces: the migration ledger said a migration was pending review while the production database showed it fully applied — the loop trusted the database and flagged the ledger, without rewriting a governed record it did not own. A tool promoted notes from candidate to verified on any name typed as promoter — a fake attacker promoted a fake note and got back a perfect, validly hashed receipt — because the receipt proved the content was unaltered and nothing about who was entitled. And when the database's own security scan found a function callable by anyone on the internet running with owner privileges, the lane recorded it and classified intentional-versus-hole before any fix — fixes cross the human security gate.

## CHILD

Imagine moving the finish line before the race is run, and then saying the runner finished. That is what moving the pointer before the check does — it declares the win before the race is over. The right order is simple: run the race, check the time, and only then move the finish line to where the runner actually stopped.

## GRANDMA

Do not declare a job done before you have checked it is done. The book that says "done" is a claim; the thing itself is the truth — and when they disagree, believe the thing. A stamp that proves nobody changed the paper proves nothing about who was allowed to stamp it. And a warning light you tape over is still a warning — fix it at the source, or leave it shining.

## NAYA

Design every promotion as an atomic sequence with the pointer move last: AUTHORIZE (human-only gate, exact SHA) → FREEZE (pin the artifact) → VALIDATE TARGET → DEPLOY → VERIFY DEPLOYMENT (must be green) → INDEPENDENT CONFIRMATION → ADVANCE POINTER → RECEIPT. If any step before the pointer fails, the pointer never moves. When a ledger and production disagree, verify against the live source of truth, act on what it says, and flag the record for its owning lane — never rewrite a governed record from inside a loop that did not create it. Bind every promotion transition to an authenticated grant with scope and action; until the check is wired, fail closed. When a repository-wide RED comes from a check the repo does not own, classify it fail-closed, route it to its owning authority with the repair-or-retire options written down, hold your own merge, and never spoof, weaken, or merge around it.

## MACHINE

The promotion contract: (1) commit point = pointer move, last, after all checks green; (2) authorization = (SHA, scope, window) triple — re-anchor the exact current main SHA before any authorized window; (3) ledger-covered files are append-only history — correct the record in a new artifact, never by rewriting the covered file; (4) promotion binds to `nayanet_authority_grants` with scope/action — a hash binds content, never identity; (5) external REDs route to the canonical owner with repair-or-retire options; hold, never merge around; (6) a single passing check is a hypothesis — require a second independent check that could have disagreed, or hold and say so.

Distills (Batch 1, 10 of 100): SN-0383 External Checks RED Across Unrelated Commits Are the External App's Problem · SN-0208 Ledgered Migrations Are Immutable · SN-0587 Production Is the Truth, the Ledger Is a Claim · SN-0362 The Unkeyed Seal, Live — promote_note Elevates on a Self-Asserted String · SN-0363 Atomic Promotion — The Pointer Moves Last, Not First · SN-0455 Live Security Advisor Evidence · SN-0475 Deployment Authorization Expires at the SHA · SN-0099 Not Ready to Promise Publicly Yet · SN-0380 Route the External Red to Its Canonical Owner · SN-0458 The Second-Source Rule.

## WHAT IT ALL MEANS

Check-then-mutate is the only safe order; mutate-then-check is how you ship a branch that lies about the database. A gate the pipeline's own ordering can bypass is not a gate — it is a comment. And a receipt that proves the content was not altered, while saying nothing about who was entitled to alter it, is worse than no receipt at all, because it looks audited.

## WHY IT MATTERS

Production is the one place a lie cannot be undone by a better note. A pointer that says "promoted" while the database says "nothing landed" is a lie the whole system will build on — the next deployment, the next verification, the next decision all inherit it. Atomicity is the only design that makes that lie structurally impossible instead of merely discouraged.

## HOW IT CONNECTS

Sibling distilled notes: SN-2245 (the merge is a new tree — the same commit-point problem, one level down) · SN-2239 (authority — the grant this promotion must bind to) · SN-2244 (a law is only real when a machine enforces it — the gate must be impossible to bypass, not documented). Raw family: the ten promotion notes above, from the 2026-09-30 / 2026-10-05 / 2026-10-06 clusters.

## WHAT IS IN IT FOR YOU

Production never claims what the database cannot back up. A deployment is a deployment only when every check is green and the pointer moves last — and anything less waits, visibly, instead of pretending.

## THE LEARNING

Verify first, move the pointer last. A hash binds content, never identity — bind the promotion to the grant.
