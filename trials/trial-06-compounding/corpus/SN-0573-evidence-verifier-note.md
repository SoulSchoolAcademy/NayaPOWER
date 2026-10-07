# SN-0573 — Every Learning Trial Ships a Fail-Closed Evidence Verifier (CANDIDATE)

A learning trial's evidence must verify itself or fail closed. Every trial
ships a mechanical verifier: the grading script, the statistical battery, and
the evidence manifest are part of the trial pack, committed alongside the data
they check. A trial whose evidence cannot be re-verified from its own branch
is INCONCLUSIVE by construction — not by misfortune.

Fail-closed means: missing agents are excluded per preregistered rules (never
imputed); ceiling effects invalidate (never pass quietly); negative transfer
fails the trial (never ignored). The verifier runs without the builder in the
room.
