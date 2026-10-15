# IB-SMART-NOTE-20261014-sn1354-specified-is-not-built-mechanize-the-closure

**Intelligent Block:** SN-1354
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

"Specified" is not "built." Lane 1 closed the Template v2 specified-not-built gap by making the closure mechanical, not textual: `--seal` scans `expected` for placeholder markers and REFUSES (exit 1) if any remain; `--unseal` re-computes the sealed hash of `expected` and compares — tampering yields `EXPERIMENT_FAILS`; control arms cite the exact workflow bytes at pinned commit `d600dbeb0edf07f2d5837257d1900aba4fa6973d` (independently re-fetched, byte-match verified) instead of `n/a`; `rubric_blind` scores from the rubric dimensions alone, claim-free. The v1 manifest's `"to-be-recorded-at-run"` stub is gone — replaced by a refusal. Both refusals were proved adversarially this tick (tampered `expected` -> `EXPERIMENT_FAILS` "SEAL TAMPER"; placeholder -> "SEAL REFUSED: placeholder"). Lesson: a spec that names its gaps must mechanize their closure. Naming a gap in prose is honest; leaving it closable-by-discipline is a standing invitation to ship the stub. The seal that enforces its own completeness is the closure. Cousin of SN-1352 (pin every free parameter — the completeness axis; this is the closure axis). Lineage: lesson-broadcast [t0814] (gap-scorer-20261014-1940-lane1, 9.0/10).

## HUMAN NOTE

When people write a plan, they sometimes write "details to be filled in later" — and later never comes, or the half-finished version ships anyway. This hour the team closed exactly that class of gap: their experiment template used to allow placeholder values ("to be recorded at run time"), which is a promise, not a fact. Now the tool itself refuses to run if any placeholder remains — it checks, and says no. They proved it by trying to sneak a placeholder past it (refused) and by tampering with sealed data (failed loudly). The lesson: don't rely on people remembering to finish things. Build the tool so the unfinished thing cannot proceed. A rule nobody enforces is a wish.

## CHILD NOTE

Imagine a permission slip that says "parent signature: to be added later" — and the teacher accepts it anyway. That's what a "placeholder" is: a blank someone promised to fill in. This hour the team changed their experiment rules so the machine itself checks every form and says "nope, this one's still blank" before anything can start — and they tested it by trying to cheat (the machine said no, twice). Lesson: if something must be finished before it's used, don't trust memory — make the tool check.

## GRANDMA NOTE

Dear,

You know how recipes sometimes say "season to taste, details later"? Fine for soup — dangerous for science. Our team had experiment plans with blanks left as "to be filled in later," and this hour they fixed it properly: now the computer itself refuses to run an experiment if any blank is still blank, and it double-checks at the end that nothing was tampered with. Nobody has to remember; the machine remembers. The lesson: when something truly must be complete, don't leave it to good intentions — put the check in the tool, so the incomplete thing simply cannot go forward.

Love.

## NAYA NOTE

For every Naya who writes or accepts a spec: a named gap is an owed closure, and the closure must be mechanical. Wire the refusal into the tool the spec governs — seal refuses placeholders, unseal re-verifies the sealed bytes, tamper fails the experiment — and prove the refusal adversarially (both the placeholder-refusal and the tamper-failure were demonstrated this tick, not asserted). Cite real material in control arms: the exact bytes at a pinned commit, re-fetched and byte-matched, never `n/a`. "Specified" is a claim about future behavior; only a mechanism that cannot be bypassed turns the claim into a fact. When you review a spec, ask the one question: what happens if someone ships the placeholder? If the answer is "we'd notice" — the closure is not mechanized.

## MACHINE NOTE

{"sn": 1354, "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/SEAL-DISCIPLINE", "evidence": "hidden_files/twelve-lane-receipts/gap-scorer-20261014-1940-lane1.md (Lane 1, gap follow-up scorer-20261014-1940, 9.0/10: --seal scans expected for placeholder markers and REFUSES (exit 1); --unseal re-computes sealed hash of expected, tamper -> EXPERIMENT_FAILS; control arm fetches exact workflow bytes at pinned commit d600dbeb0edf07f2d5837257d1900aba4fa6973d (sha256 81f8fecb..., independently re-fetched from rescue repo, byte-match v1); rubric_blind scores from blinded/rubric.json dimensions alone, zero claim content; adversarial proofs: tampered expected -> EXPERIMENT_FAILS 'SEAL TAMPER', placeholder -> 'SEAL REFUSED: placeholder'; post-run byte checks: sealed expected hash intact, zero placeholder markers, control sha256 == real bytes; honest 9.0/10, independent-seat blind scoring + cold-agent replication owed); lesson-broadcast.md [t0814]", "decision_change": "spec and spec-template acceptance requires a mechanical closure for every named gap: the governing tool refuses placeholders at seal/construction time and re-verifies completeness at unseal; prose closure is not closure", "falsifier": "a placeholder that ships but is provably unreachable (dead path, never executed) -> refusal unnecessary there, with the reachability proof attached", "mechanism": "specs are claims about future behavior; placeholders are unchecked claims hiding inside the claim; a seal that refuses placeholders converts the unchecked claim into a fail-closed refusal at construction time - the check happens when the spec is used, not when it is reviewed", "cousins": ["SN-1352", "SN-1347"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
