# In a Seam Sweep, the Definition's Signature Is the Classifier — the Name Is the Suspect List

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01569-definition-signature-is-the-classifier
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Sweeping call sites of the retrieval-auth seam, the name pattern caught `mm.retrieve` and a docstring's "fail-closed retrieve()" with equal confidence — name-match greed nearly inflated the caller list until context showed one was the metabolism's own discipline, not the auth gate. Anchoring every classification on the definition signature — `def retrieve(query)` (the seam) vs `def retrieve(records, …)` (the metabolism) — fixed it. The method: sweep definitions first, then classify call sites against them. Names are shared and drift; signatures are the contract.

## 🩷 HUMAN NOTE

When you search a codebase for who calls a function, the obvious move is to grep for the name. The sweep pattern here did exactly that — and it caught three "callers" of `retrieve` with equal confidence: the real auth-gate seam (`def retrieve(query)` in tools/smart_note_v2.py:797), the memory metabolism's own retriever (`def retrieve(records, …)` in kernel/memory_metabolism.py:508 — takes records, not a query; a completely different seam), and a docstring that merely said "fail-closed retrieve()" describing the metabolism's discipline. Two of three were false positives, and the name gave no way to tell. The fix: anchor classification on the definition signature, not the name. Once the signature was the classifier, the metabolism retriever excluded itself on its parameter list and the docstring excluded itself as non-code. The sweep then ran correctly: the one genuine caller `x = retrieve(args.query)` verified in context, the CLI argparse subcommand pinned. The durable method: enumerate definitions first, then classify call sites against the signatures — doing call sites first meant re-anchoring everything afterward.

## 🟣 CHILD NOTE

If three kids are named Alex, yelling "Alex!" tells you nothing. Check what each Alex DOES — that's how you tell them apart.

## 🔵 GRANDMA NOTE

Names are like labels on jars — two jars can have the same label with different things inside. The recipe on the jar's label (what it takes in) is what tells you which jar you have. When checking a system, read the recipes first, not just the labels.

## 🟠 NAYA NOTE

A name is a convenience that drifts across seams; a signature is the seam's contract. Name-match greed is the specific failure: a grep for the name returns candidates at equal confidence and the sweeper, trusting the name, either inflates the caller list or — worse — quietly accepts false membership. The signature anchors on what the thing IS (parameter list, arity, call convention), which is what the classification question actually asks. Cousins in the corpus: SN-0225 (string-keyed classifiers are gamable — the warning; this is the method), SN-01350 (probe the wiring seam, not just the modules — the target; this names how to classify what you find there). Passes the bar: future seam sweeps run definitions-first as a standing step, not as a recovery.

## 🟢 MACHINE NOTE

~~~json
{
  "applies_when": ["seam", "sweep", "classifier", "caller-list", "migration-packet", "audit", "wiring"],
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "enforcement": "A seam-sweep receipt opens with the definition signature (quoted def line) of every target; classification evidence cites signature matches, with name matches labeled suspect-list only. A sweep whose first evidence is a bare name-grep is bounced back to definitions-first. The receipt must show the signature it anchored on before the caller list it produced.",
  "evidence": "twelve-lane-receipts/gap-lane-scorer-20261017-1040-lane8.md (pass-3 9.0/10, ship, 2026-10-17): seam def tools/smart_note_v2.py:797 `def retrieve(query)`; excluded DIFFERENT-SEAM kernel/memory_metabolism.py:508 `def retrieve(records, …)` on its signature; `mm.retrieve(…)` (memory_store.py:305) and the :22 docstring 'fail-closed retrieve()' resolved by context read, not by name.",
  "falsifier": "A future sweep where a name-only scan finds a genuine caller that signature-anchored classification misses — or where signature-anchoring misses a true member the name-grep catches. Either re-opens the ordering.",
  "mechanism": "Names are labels shared across unrelated seams and subject to drift; signatures (parameter lists, arity, call conventions) are the seam's contract. Classification asks 'is this the seam?' — a contract question, answerable only by the contract. Anchoring on the name answers a different question ('does the label match?') and manufactures false membership at equal confidence.",
  "names_decision_changed": "Seam-sweep procedure: enumerate the target definitions FIRST, then classify call sites against the signatures. Never invert (call sites first, signatures as recovery). The receipt's evidence section leads with the signature, not the grep."
}
~~~

## 🟢 LEARNING LESSON

The definition's signature is the classifier; the name is the suspect list. Sweep definitions first.

## 🟡 WHAT IT MEANS

A name-grep is a suspect list, not a verdict. Classification happens against the signature — the contract the seam actually is.

## ⚪ WHAT'S IN IT FOR YOU

Sweeps that don't inflate: caller lists you can trust, migration packets whose seam claims survive a second seat, no quiet false members riding in on a shared name.

## 🟨 HOW TO APPLY / HOW TO USE

1. Before grepping for callers, enumerate the target's definition: quote the full `def` line (name + parameters).
2. For every candidate the name-grep returns, ask: does its signature match the target's? No → excluded (note the exclusion, name the differing signature).
3. Read ambiguous candidates in context (docstrings describe; code calls).
4. State the sweep's bound honestly (bounded sweeps are legitimate instruments when the bound is stated and argued, not claimed as tree-wide).

## 🔗 HOW IT CONNECTS

- **COUSIN** → SN-0225 — a-string-keyed-classifier-is-gamable (the warning: syntax can't certify semantics; this is the constructive method)
- **COUSIN** → SN-01350 — probe-the-wiring-seam-not-just-the-modules (the target: probe the seam; this names how to classify what you find)
- **COUSIN** → CANDIDATE 552 — verify the seam, not the cited instances (the discipline; this names the classifier mechanism)

## 🧭 KEY DECISIONS / PRINCIPLES

- Signature is the classifier; name is the suspect list.
- Definitions-first, always — call sites classified against signatures, never signatures inferred from call sites.
- A sweep's bound is stated and argued; bounded ≠ untrustworthy, unstated ≠ verified.

## 🟾 PROOF / PROVENANCE

~~~json
{
  "event": "retrieval-auth-gate migration-packet seam sweep (gap-lane-scorer-20261017-1040-lane8, 2026-10-17)",
  "found": "name pattern caught mm.retrieve + docstring 'fail-closed retrieve()' with equal confidence; near-miss inflated caller list until signature anchoring excluded both",
  "fixed_in": "anchored every classification on def retrieve(query) vs def retrieve(records, …); genuine caller x = retrieve(args.query) verified in context",
  "receipt": "twelve-lane-receipts/gap-lane-scorer-20261017-1040-lane8.md (pass-3 9.0/10, ship)",
  "logged": "learning-events-2026-10-17 hour 11 (CANDIDATE 557)"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Applies to seam sweeps where multiple same-named definitions exist or names drift across modules. Where the name is genuinely unique tree-wide, name-grep converges with signature anchoring and the method costs nothing extra. The sweep's completeness claim rests on the stated bound (importable surface), not a full-tree scan — honest scope is part of the method.

## ➜ NEXT ACTION / SUCCESS CONDITION

Future seam-sweep briefs carry "definitions-first" as a standing step; the lane-scorer's sweep protocol adopts the signature-anchored evidence ordering.
