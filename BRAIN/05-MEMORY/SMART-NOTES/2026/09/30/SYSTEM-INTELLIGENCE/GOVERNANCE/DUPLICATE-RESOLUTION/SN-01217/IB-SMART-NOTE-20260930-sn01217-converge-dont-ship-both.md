# Converge, Don't Ship Both — One Canonical Source Per Concept

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1217-converge-dont-ship-both
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:08 PDT distillation tick (2026-10-13) from #2175 comments 6153440528 (Naya 2 independent audit: duplicate oath/doctrine sources across #2534 and #2535) and 6153589174 (oath convergence proposal), plus 6153412456 (independent cross-PR audit), read from the director's board-window capture on disk.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two PRs carried the same doctrine: **#2534** (Naya 2: oath + manifesto + code, three tongues, `BRAIN/01-GOVERNANCE/0021-0023`) and **#2535** (Naya 5: oath + doctrine, `NAYA-ACTIVATION/` front door, repository-root `CONSTITUTION/`). Same substance, two wordings, two placements, two governance homes — and a third claimant existed in the chain (a dictated-words oath, a reformulated oath, a converged oath; the contract gate verified **three genuinely different oath wordings** across #2533/#2534/#2535). The cross-PR audit named the collision plainly and the convergence proposal scorecarded the synthesis: assign **one canonical authored source per concept** (Shawn's dictated words win where wordings differ; registry artifacts and runtime front-door split by role), demote every other rendering to a **thin pointer or verified projection** (read-me-first, instruction snippet, attunement protocol), pin both paths in the integrity script so renderings can never drift silently, merge through **one carrier PR** under the scorecard machinery, and close the other as superseded. "Do not merge #2534 and #2535 independently and hope later edits will reconcile them" — this is an architecture and truth-source decision, not README formatting. When two lanes build the same doctrine, converge before merge; two parallel truths is the most expensive duplicate in the system because every downstream law inherits the fork.

## 🩷 HUMAN NOTE

It's like two architects both drawing the blueprints for the same house — different scales, different rooms labeled the same name. If you build from both drawings, you get two front doors and a staircase to nowhere. The rule: pick ONE official drawing, hang it on the wall, and turn the other one into a photocopy of the first — never a second original. If the photocopies ever drift from the original, the alarm goes off.

## 🟣 CHILD NOTE

Imagine two kids both write "the rules of the game" for the same game — different words, different order, both taped to the wall. When kids argue, each points to THEIR rules. The fix: pick one set of rules as the real one (say, the one the teacher wrote), and turn the other page into a copy of it. One rulebook. If you let both stay "real," every argument gets twice as confusing.

## 🔵 GRANDMA NOTE

It's like having two family recipe books for the same dish — one says a cup of sugar, one says two spoons. Nobody knows which cake is the real one. The fix is simple: pick the recipe your mother wrote, throw the other one's claim away, and if you ever print a second copy, make sure it's a true copy that can't quietly change. One recipe book per dish — everything else is just a printout.

## 🟠 NAYA NOTE

Apply this whenever two lanes produce overlapping doctrine, governance text, or canonical artifacts: (1) **do not merge both and reconcile later** — reconciliation after merge is a fork with history, and every downstream law inherits it; (2) assign one canonical authored source per concept and write the decision down (which text wins, which path, which IDs — here: Shawn's dictated words; `BRAIN/01-GOVERNANCE/0021-0023` registry artifacts + `NAYA-ACTIVATION/` runtime machinery); (3) demote all other renderings to thin pointers or generated projections — a second authored copy is a second truth; (4) pin every live path in an integrity check so renderings can never drift silently (the `verify-oath-integrity.py` pattern: report NOT_ON_MAIN honestly until deployment); (5) carry it in **one carrier PR** through the scorecard machinery (distinct-seat review, 9.5 bar), and close the other as superseded — no self-merges; (6) watch for the three-wording trap: reformulations, excerpts, and formats are not "the same thing" until the canonical-ownership audit says so.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "competing_doctrine_prs_duplicate_truth_source",
  "evidence": {
    "blocking_finding": "6153440528 — Naya 2 independent audit (2026-10-13T19:26:39Z): #2534 creates numbered three-tongue canonical family (0021 Oath, 0022 Manifesto, 0023 Code) under BRAIN/01-GOVERNANCE/; #2535 independently creates oath under NAYA-ACTIVATION/OATH-OF-THE-NAYA-V1.md + doctrine under repository-root CONSTITUTION/NAYA-DOCTRINE-V1.md; 'Do not merge #2534 and #2535 independently and hope later edits will reconcile them. This is an architecture and truth-source decision, not just README formatting.'",
    "convergence_proposal": "6153589174 — oath convergence: #2534 x #2535, one doctrine no duplicates (2026-10-13T19:34:36Z): one canonical oath text (Shawn's dictated words win), NAYA-ACTIVATION/ = front door + runtime machinery, BRAIN/01-GOVERNANCE/0021-0023 = numbered registry artifacts, integrity script pins both paths, ONE carrier PR, the other closes superseded",
    "cross_pr_audit": "6153412456 — independent cross-PR audit (2026-10-13T19:25:06Z): two competing READ-ME-FIRST files (#2533 BRAIN/00-ACTIVATION vs #2535 NAYA-ACTIVATION), broken relative links across placements, authority hierarchy contradictions — 'No duplicate implementation recommended' before lanes converge",
    "three_wordings": "Memory 2026-10-13 THE CONTRACT: verified 3 genuinely different oath wordings across #2533/#2534/#2535; contract gate reads converged oath bytes rather than pinning one wording"
  },
  "rule": "two_competing_doctrine_prs_converge_before_merge_one_canonical_authored_source_per_concept_other_renderings_are_thin_pointers",
  "procedure": [
    "when two lanes produce overlapping doctrine/governance artifacts, do NOT merge both and reconcile later — merging both is a truth fork with history",
    "assign one canonical authored source per concept, in writing: which text wins (the human's dictated words over reformulations), which path, which registry IDs",
    "demote every other rendering to a thin pointer or generated projection (read-me-first, instruction snippet, attunement protocol) — never a second authored copy",
    "pin all live renderings in an integrity check so copies can never drift silently; report NOT_ON_MAIN honestly until deployment",
    "carry the converged package in ONE carrier PR through the scorecard machinery (distinct-seat review, 9.5 bar); close the other as superseded; no self-merges"
  ],
  "related": ["SN-0463 (parallel work collision protocol — check before you build)", "SN-1216 (verify a derived claim with the claim's own machinery — reformulations are not the same thing until the audit says so)"]
}
~~~
