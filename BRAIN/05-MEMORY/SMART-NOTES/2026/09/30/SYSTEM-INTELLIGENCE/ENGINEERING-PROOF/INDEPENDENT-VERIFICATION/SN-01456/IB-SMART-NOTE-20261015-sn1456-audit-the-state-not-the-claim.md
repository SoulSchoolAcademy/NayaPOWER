# IB-SMART-NOTE

- Intelligent Block: AUDIT-METHOD — census from the canonical store, not the prose
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-15 (PDT)
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
When closing a hole census, read the counts off the canonical ledger JSON — never the parent receipt's prose. Prose summaries are derived copies and they drift; machine state is the ground. Audit the state, not the claim.

## HUMAN NOTE
A lane scorer closing the ledger's holed verdicts ignored the receipt's prose list (which said 8) and read the census off the ledger JSON instead (which said 10). The JSON caught both a phantom — one verdict named in the prose had no ledger row at all — and three real omissions the prose never named. Every verdict was then re-extracted as a verbatim quote from its receipt with SHAs re-pinned against live disk. The prose wasn't lying; it was just a copy, and copies drift. When the count matters, the store wins over the story.

## CHILD NOTE
If you're counting how many toys are in the box, count the toys — don't ask your friend how many they remember. The box knows; the memory might miss some or invent one.

## GRANDMA NOTE
Trust the ledger, not the letter about the ledger. Whoever wrote the letter could have missed a line or counted twice. Go back to the original list and count again yourself.

## NAYA NOTE
The pattern is prose-as-derived-copy: a human writes a summary over a canonical store, and every hand-off drifts the count. The 2120 lane-scorer run (gap-lane-scorer-20261015-2120-lane11) made the census mechanical: enumerate the ledger JSON, then for each row re-extract the verdict verbatim from the receipt with the SHA re-pinned against live disk. Result: prose 8 → store 10, one phantom excluded (t0582-lane3, no ledger row — a non-SURGE receipt mis-named, correctly kept out), three genuine omissions recovered (t0555-lane4, t0572-lane4, t0593-lane10). The rule relaxes only when the prose is itself deterministically generated from the store with provenance shown — then the provenance is the audit. Until then: counts come from the store, always.

## MACHINE NOTE
{"sn": "SN-1456", "rule": "For any closure census (holes, verdicts, claims), enumerate the canonical store's rows; treat prose summaries as leads, never as answers. Re-extract each verdict verbatim from its source artifact with identity re-pinned.", "evidence": ["gap-lane-scorer-20261015-2120-lane11: ledger JSON 10 vs prose 8; phantom t0582-lane3 excluded; omissions t0555-lane4, t0572-lane4, t0593-lane10 recovered", "hidden_files/learning-events-2026-10-15-22.md (goal workspace)"], "mechanism": "Prose is a derived copy with a human in the loop; copies drift at every hand-off. The JSON store is the single source of truth for counts.", "decision_change": "Future hole-closure and census work starts from the ledger JSON and re-extracts verdicts verbatim; prose lists are never the enumeration.", "falsifiability": "If a prose summary is proven to be deterministically generated from the canonical store by a verified pipeline with provenance shown, the rule relaxes to 'verify the provenance, then trust the copy.'", "siblings": ["SN-0085 resolve-then-trust / anchor trust in invariants (adjacent, origin not count)"]}
