# IB-SMART-NOTE-20261006-sn0489-merged-is-not-closed

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20261006-sn0489-merged-is-not-closed |
| Smart Note | SN-0489 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-06 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

PR #1627 merged a truth-state guard file into main. Nothing changed: no canonical function calls it. Two lanes independently verified on live main bytes that the guard exists as a file and nowhere else. "Merged" is a git fact; "closed" is a behavioral fact. A repair is only closed when the canonical call path provably invokes the mechanism — never when the diff lands.

## HUMAN NOTE

The fix got merged and the bug was still there. How? The new guard file sat on main like a fire extinguisher still in its box — nobody had mounted it on the wall. Both Naya seats read the actual code on live main: the functions that matter (promote_note, audit_registry) had zero references to the guard. Merged is what GitHub says. Closed is what the running code does. Those are two different things.

## CHILD NOTE

If you build a fence but never put it around the yard, the dog still gets out. The fence exists — it's just not doing the job. Putting it in the garage and saying "fence done" doesn't keep the dog in.

## GRANDMA NOTE

Buying the medicine and taking the medicine are not the same thing. The bottle can sit in the cabinet, paid for and delivered — but until someone actually swallows it, nothing changes. "It's in the house" is not "it worked."

## NAYA NOTE

From now on: a repair PR is not closed when merged. It is closed when I can point at the canonical function and show it calls the new mechanism. My closeout checklist for any enforcement repair: (1) repo-wide scan for references to the new artifact — if nothing outside the artifact's own file and test names it, it is unwired; (2) open the canonical caller and read it; (3) prove the behavior on the live path, not the file's existence. PR #1627 failed all three: exactly 2 files added, zero wiring. The #1603 repair order is the held next step — wire promote_note and audit_registry to the guard before any claim of closure.

## MACHINE NOTE

```json
{
  "rule": "merged_is_not_closed",
  "family": ["SN-0388-deployed-url-not-product", "SN-0421-run-success-skipped-jobs-vacuous", "SN-0430-kernel-green-not-tip-green"],
  "closeout_checklist": [
    "repo-wide reference scan: new artifact named outside its own file + tests?",
    "canonical caller opened and read: invokes the mechanism?",
    "behavior proven on the live path, not file existence"
  ],
  "evidence_class": "failure_classification",
  "falsifier": "a merged enforcement repair whose canonical callers provably invoke it"
}
```

## EVIDENCE

- #1354 comment 6024126398 (Naya 4, 2026-10-06 19:43 PDT): TRUTH CORRECTION — promoter string not a verified LAW grant; canonical `smart_note_v2.promote_note()` does not call the guard; canonical `audit_registry()` does not invoke semantic audit; six current RATIFIED legacy entries have no elevation history. Repair order posted on #1603. TRUTH stays below 9.
- #1354 comment 6024356065 (Naya 2 relay, 2026-10-06 19:58 PDT): byte-verified on live main tip `930406f6` via refs API — PR #1627's files are exactly 2 added (`tools/truth_state_guard.py` + `tests/test_truth_state_poison.py`); repo-wide scan finds nothing outside those two referencing `truth_state_guard`; `promote_note` (L832) and `audit_registry` (L1009) contain zero guard/semantic references. Two-lane convergence: merged ≠ closed stands on the bytes.
