# Intelligent Block: SN-0297

**Intelligent Block:** SN-0297 — Branch Citations Are Not Canonical Provenance
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Declare citation state alongside substance. On 2026-10-04, Coda 1's Super Brain verification measured Naya 4's citations of SN-0288 (Triple-A), SN-0289 (Worker Protocol), SN-0290 (self-correcting), SN-0291 (execution heartbeat), and SN-0295 (Super Brain) — NOT FOUND on main, in any open PR, or in any closed PR; the only related PRs are #1379 (charter) and #1380 (Constitution V2), neither so numbered; highest capture on main = SN-042. And the substance was real: SN-034/035/041/042 conformed to the gate. "So: the content is real and conformant; the citations do not resolve. In a system whose premise is verifiable provenance, citing five artifacts that do not exist is precisely the failure class this lane exists to catch." Naya 4 corrected on the record: those notes are CANDIDATE on draft PR #1229 — the smart links resolve on the draft branch, but citing branch-only artifacts as canonical is the failure class. The law: every citation must name the ref it resolves on (main SHA, branch, draft PR) and the artifact's truth state (CANDIDATE vs canonical). Substance-real + citation-unresolved gets credit with correction, never conflation. This is the artifact-citation axis of the premise-citation rule; SN-065 covers the capability-placement axis (a claim that places a capability on a branch where it does not exist).

## HUMAN NOTE

Shawn — quick one, in plain words. Naya 4 wrote up the super brain and cited five smart-note numbers as the sources of its laws. Coda 1 went to check those five numbers and found they didn't exist anywhere public — they only existed on a draft branch that hasn't merged. The laws themselves were real (other, older notes confirmed them), but the references pointed at nothing you or I could see on main. Naya 4 said "you're right," corrected it on the record, and the standing rule is now: every citation has to say WHERE it resolves — which branch, which commit — and whether the thing it points to is finished law or still a draft. A link that works on somebody's private branch is not proof. Think of it like footnotes in a book: the footnote has to actually lead somewhere real, or it isn't a footnote, it's decoration.

## CHILD NOTE

Imagine writing a report for school and listing books you read — but the books are still being written in someone's drawer, and nobody else can see them! That's what happened. The ideas were actually true, but the references pointed to books that don't exist yet in the library. The new rule: when you say "I learned this from book X," you also have to say where book X lives and whether it's a finished book or still being written. Good ideas, real references. Both matter.

## GRANDMA NOTE

It's like quoting a recipe from a cookbook that hasn't been printed yet — the dish might be delicious, but nobody can check your source. So now there's a simple house rule: whenever you name where you learned something, you also say exactly where to find it and whether it's a finished page or still a draft. Honest footnotes, dear. That way nobody ever has to wonder.

## NAYA NOTE

From Naya 4's sign-out (#1354, comment 5985817185): "Citation discipline — branch vs main matters for provenance. Fixed going forward." And from Coda 1's finding (#1354, comment 5985769255): the citations were "NOT FOUND... highest capture on main = SN-042." I keep the credit-with-correction pattern he modeled: SN-034, SN-035, SN-041, SN-042 were measured real and conformant — those get full credit — while SN-0288/0289/0290/0291/0295 as cited get the correction (they are CANDIDATE on draft PR #1229, not main). Cold successors: when you cite a Smart Note or any artifact, write the ref it resolves on next to the number. If it only resolves on a draft branch, say so. Never let a branch-only reference wear canonical clothes.

## MACHINE NOTE

```json
{
  "sn": "SN-0297",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-04",
  "lesson": "Every citation must declare its resolution state: the ref it resolves on (main SHA / branch / draft PR) and the artifact's truth state (CANDIDATE vs canonical). Branch-resolving references are never cited as canonical.",
  "law_statement": "SUBSTANCE-REAL + CITATION-UNRESOLVED = CREDIT WITH CORRECTION, NEVER CONFLATION.",
  "evidence": {
    "board": "#1354",
    "finding_comment": "5985769255 (Coda 1: 'SN-0288 NOT FOUND ... SN-0295 NOT FOUND ... highest capture on main = SN-042 ... citing five artifacts that do not exist is precisely the failure class this lane exists to catch.')",
    "correction_comment": "5985817185 (Naya 4: 'those notes are CANDIDATE on the draft branch; substance confirmed real via SN-034/035/041/042 ... Citation discipline — branch vs main matters for provenance.')",
    "conformant_substance": ["SN-034", "SN-035", "SN-041", "SN-042"],
    "non_resolving_citations": ["SN-0288", "SN-0289", "SN-0290", "SN-0291", "SN-0295"],
    "related_prs_checked": ["#1379 (charter)", "#1380 (Constitution V2)"]
  },
  "related": ["SN-065 (branch-boundary: capability-placement axis of the premise-citation rule)"],
  "citation_rule": "cite as <ID> @ <ref> (<TRUTH STATE>); if ref is not main, the state must say so explicitly",
  "failure_mode_prevented": "phantom citations — references that resolve nowhere on canonical state, eroding the verifiable-provenance premise"
}
```
