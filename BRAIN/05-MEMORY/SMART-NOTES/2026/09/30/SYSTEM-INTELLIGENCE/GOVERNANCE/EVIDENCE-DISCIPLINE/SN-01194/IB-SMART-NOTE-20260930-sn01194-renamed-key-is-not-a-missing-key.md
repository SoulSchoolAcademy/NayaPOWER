# IB-SMART-NOTE-20260930-sn01194-renamed-key-is-not-a-missing-key

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20260930-sn01194-renamed-key-is-not-a-missing-key |
| Smart Note | SN-01194 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-13 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

Lane 4 (Naya Mason) designed the corrected H-dc6 EQ-D0 instrument and, on the way, corrected t0629's "never written" gloss: t0626's results DID contain the bug fingerprint — `eq_d0_diffs` with got-perfect-triples and want=null ×3 — hiding under a different field name. The absence claim had been checked against one remembered key; the fingerprint lived under another. The same receipt recorded a second drift left uninvestigated: the t0622 design doc SHA moved (…815880→…825880) between observations — recorded, not verdict — and dispatched as follow-up work. Two rules banked: an absence claim is a claim about a namespace, not a name — diff the full key namespace before concluding "never written"; and a design-doc SHA that moved between two observations gets a verdict (MATCH/DIVERGED), never a gloss.

## HUMAN NOTE

Shawn — the retrieval lane corrected its own record today. Yesterday's read said a value was "never written" to the experiment results; today's executor found it sitting right there under a different field name — the bug's fingerprint, plain as day, just filed under `eq_d0_diffs` instead of the name everyone remembered. Same run also caught the design document itself drifting between observations (its fingerprint changed) — that one's recorded honestly and handed to a follow-up lane to investigate byte-by-byte. Two rules banked: "never written" means you checked every name, not one name; and when the blueprint changes under you, you say whether it matches or diverged — you don't wave it through.

## CHILD NOTE

Imagine you're told "there's no cookie in the jar" — but someone moved the cookie to a different jar with a different label. The cookie was never missing; you just looked in one jar. Before you say "no cookie," you check all the jars. And if the recipe card itself looks different from yesterday, you don't shrug — you figure out what changed. That's what the lane did today: found the "missing" thing under its new name, and flagged the changed recipe card for a proper check.

## GRANDMA NOTE

The inspector reported a part was never installed. A second inspector found it installed under a different part number — same part, renamed on the paperwork. The first report was an honest mistake: he checked the name he remembered instead of the whole parts list. The rule from now on: "missing" means checked everywhere, not checked once. The same visit also found the blueprint itself had changed between two inspections — noted honestly and sent for a proper comparison, not filed under "probably fine." Renames are the cheapest way to hide something; checking the whole list is the cheapest way to find it.

## NAYA NOTE

Note to future me: never accept or issue an absence claim ("never written," "not present," "missing") based on one remembered key name. Enumerate the full key namespace of the artifact — results JSON, design doc, ledger — and diff before concluding. t0629's gloss fell to t0633's byte check: `eq_d0_diffs` was there all along, got-perfect-triples / want-null ×3, the exact bug fingerprint. Same discipline for design docs: a SHA that moved between observations (t0622: …815880→…825880) is an open MATCH/DIVERGED verdict, not a footnote — dispatch the byte-diff (which commits, EQ-D0 byte-diff, verdict), don't gloss it. Renames are the cheapest way to hide a fingerprint; namespace-wide checks are the cheapest way to find one. When you issue the correction, name the hiding mechanism explicitly so the next seat checks names first.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20260930-sn01194-renamed-key-is-not-a-missing-key",
  "smart_note": "SN-01194",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "An absence claim is a claim about a namespace, not a name: diff the full key namespace before concluding 'never written'; a design-doc SHA that moved between observations gets a MATCH/DIVERGED verdict, never a gloss.",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "EVIDENCE-DISCIPLINE"],
  "cousins": ["SN-01191"],
  "evidence": {
    "memory_log": "~/memory/2026-10-13.md — 'Lane-executor run (t0633 + t0634)' entry",
    "receipt": "twelve-lane-receipts/t0633-lane4.md (Naya Mason, 9.0/10 — corrected H-dc6 EQ-D0 instrument designed + sealed + dry-fired 45/45)",
    "correction": "t0626 results DID contain the bug fingerprint (eq_d0_diffs: got perfect triples, want=null x3); t0629's 'never written' gloss corrected — the different field name hid it",
    "open_verdict": "t0622 design doc SHA drifted since t0629 (…815880→…825880), recorded not investigated → dispatched as brief-t0639-lane4 (design-doc drift investigation: which commits, EQ-D0 byte-diff, MATCH/DIVERGED verdict)"
  },
  "rules": [
    "Never issue an absence claim from one remembered key name; enumerate and diff the full key namespace first.",
    "When correcting a wrong absence claim, name the hiding mechanism (rename, moved field) explicitly.",
    "A design-doc SHA that moved between two observations is an open MATCH/DIVERGED verdict — dispatch the byte-diff, never gloss it.",
    "Sealed instruments and dry-fire runs (45/45 incl. real-file RED checks) precede any claim about what the results contain."
  ]
}
```
