# Amendment Premise Verification — Check Every Amendment's Cited Premises Against the Pinned SHA Before Lock

**Intelligent Block:** IB-SMART-NOTE-20261001-sn027-amendment-premise-verification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a CANDIDATE spec carries PROPOSED amendments, each amendment cites premises — section numbers, quoted text, issue references, claims about what the file says. Those citations must be verified against the exact pinned revision (SHA) of the file before the amendment is applied at lock time. In the CONNECT qualify run, amendment A-CONNECT-8 (Naya-4 builder-lane delta, #1232) claimed the §3 caveat "V2.1 is CANDIDATE (#1185), not ratified law" was stale because V2.1 was ratified via #1186/#1190/#1192. A full read plus grep of the file at the pinned head `19abcf2f` shows no such caveat exists at §3 or anywhere else in the file — the V2.1 reference at S45 carries no caveat. The amendment's premise is ungrounded in the pinned revision: either the caveat lived in an earlier revision, or the citation is wrong. Applying it blindly at lock would have edited a non-existent caveat into the lock checklist. The rule: an amendment is not applicable until its premises are located in the pinned bytes.

## 🩷 HUMAN NOTE

Think of amendments like tracked changes on a contract, and the pinned SHA like the page you froze them on. If someone writes "delete the paragraph on page 3 that says X," you check page 3 first. Here, the "paragraph" wasn't there. That doesn't make the amendment wrong-headed — V2.1 may indeed be ratified — but it means the amendment's stated reason doesn't match the document, and a lock built on a mismatched reason is a lock built on sand. Verify the citation, then decide.

## 🟣 CHILD NOTE

Before you accept a suggested fix, check that the thing it wants to fix is actually in the paper. If the paper doesn't say what the fix claims it says, stop and ask — don't just cross it out anyway.

## 🔵 GRANDMA NOTE

If someone hands you a correction slip for a recipe that says "remove the salt from step 3," but step 3 has no salt, don't scribble on the recipe. First find out whether you're looking at the right copy of the recipe.

## 🟠 NAYA NOTE

Treat every amendment as a small contract with two parts: the *premise* (what the file currently says, cited by section/quote) and the *action* (what to change). The action is only valid if the premise is located in the pinned bytes. When a premise is missing, the amendment goes back to its author with "premise not found at <SHA>" — it does not get applied, and it does not block the lock of unrelated amendments.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "amendment_premise_verification_before_lock",
  "procedure": [
    "for each PROPOSED amendment on the lock candidate:",
    "  1. extract its premises: cited section numbers, quoted strings, issue/PR references, claims of file content",
    "  2. fetch the file at the pinned SHA (the exact revision the qualification/audit was performed on)",
    "  3. locate each premise verbatim in those bytes (grep for quotes; check section numbering)",
    "  4. if a premise is not found: mark amendment PREMISE_UNGROUNDED, return to author with the SHA; do not apply",
    "  5. if premises check out: amendment is applicable; apply or explicitly reject with written reason",
    "  6. record the verified SHA alongside the applied/rejected decision so a later rebase invalidates the check"
  ],
  "concrete_case": {
    "amendment": "A-CONNECT-8 (Naya-4 builder-lane delta, PR #1232)",
    "claim": "§3 caveat 'V2.1 is CANDIDATE (#1185), not ratified law' is STALE; V2.1 ratified via #1186/#1190/#1192",
    "pinned_sha": "19abcf2f22ec5fdbe8e2c2c5e5e2545833aef789",
    "verification": "full file read (1957 lines) + grep for 'CANDIDATE|1185|V2.1' — no such caveat at §3 or elsewhere; S45 'CONNECT uses the shared Value Calculus V2.1.' carries no caveat",
    "verdict": "PREMISE_UNGROUNDED at pinned SHA — returned for citation verification (#1224 comment 5925066392)",
    "note": "the underlying V2.1-ratification fact may still be true; only the citation is ungrounded"
  }
}
~~~

## 🟢 LEARNING LESSON

An amendment's conclusion can be true while its premise is false in the pinned revision — "V2.1 is ratified" may be true, but "the file says V2.1 is a candidate at §3" is not. Locks consume amendments; a lock that applies an amendment on a false premise inherits the falsehood into canonical state. The cheap check (grep the pinned bytes) precedes the expensive decision (lock), and a branch rebase invalidates all prior premise checks — re-verify after any move of the pinned SHA.

## 🟡 WHAT IT MEANS

Amendment review is a two-stage gate: premise verification (mechanical, against pinned bytes) then merit decision (judgment). Skipping stage one lets phantom citations ride into locked canonical specs, where they become expensive to retract.

## ⚪ WHAT'S IN IT FOR YOU

Lock checklists that don't silently absorb non-existent text; amendments returned to authors with exact, checkable feedback instead of vague unease; fewer lock-day surprises across all eight organs' 0002 specs.

## 🟨 HOW TO APPLY / HOW TO USE

1. Before any lock of a 0002 master spec, list all PROPOSED amendments (both seats' sequences — e.g. A-CONNECT-1..7 and A-CONNECT-8..9).
2. For each, extract cited premises and locate them in the pinned SHA's bytes.
3. Amendments with ungrounded premises go back to the author with the SHA and the missing citation; applicable ones proceed to apply-or-reject-with-reason.
4. If the branch head moves, repeat — premise checks are SHA-bound.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-018 — CI exit-2 triage — evidence before hypothesis; a verdict is not a diagnosis
- **SUPPORTS** → Evidence law — reproduce against the exact bytes; claims about file content are checkable claims
- **SUPPORTS** → Amendment 0002 / Prime 1 — a lock built on a false premise is not a fully-informed decision
- **SUPPORTS** → connect-qualify machine-contract delta — "verify A-CONNECT-8's cited §3 caveat before lock"

## 🧭 KEY DECISIONS / PRINCIPLES

- An amendment's premise is a factual claim about pinned bytes; verify it like any other factual claim.
- PREMISE_UNGROUNDED ≠ amendment rejected: return it for citation repair, don't silently drop it.
- Premise checks are SHA-bound; a rebase invalidates them.
- A true conclusion with a false premise still cannot be applied as written — the premise is part of what gets locked.

## 🧾 PROOF / PROVENANCE

- Amendment text: PR #1232 files diff on `BRAIN/03-KERNEL/NODES/CONNECT/0002-MASTER-SPEC-V1.md` (+23 lines, head `26331055`, branch `naya4/builder-deltas-six-rebuild`): "A-CONNECT-8 [N4-C2 — stale V2.1 caveat]: Re-base: the §3 caveat 'V2.1 is CANDIDATE (#1185), not ratified law — all calculus references in this spec are aspirational until ratification' is STALE."
- Pinned file: `BRAIN/03-KERNEL/NODES/CONNECT/0002-MASTER-SPEC-V1.md` at `19abcf2f22ec5fdbe8e2c2c5e5e2545833aef789` (PR #1224 head, 2026-10-01; 1957 lines / 49479 bytes).
- Verification: full sequential read of all 1957 lines during connect-qualify; targeted grep for `CANDIDATE|1185|V2.1` (excluding status boilerplate): no §3 caveat; only V2.1 mention is S45 "CONNECT uses the shared Value Calculus V2.1." with no caveat.
- Reported: #1224 comment 5925066392 (amendment verification note), #554 comment 5925067756.
- Collision check: main max SN-016; open PRs reference up to SN-026 → SN-027 taken as next free.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

CANDIDATE: demonstrated once, on one amendment, in one qualify run. The rule is procedural, not proven to catch every phantom (an amendment could cite a paraphrase that a grep misses — human judgment still required for semantic premises). Falsifier: an amendment whose premises all verify against the pinned SHA yet whose application still corrupts the lock (would show the procedure is necessary but not sufficient). The SN-numbering collision registry (#554 comments + open PR scans) is itself unverified against comments older than the recent 100 — a stale claim could still collide; re-check before the next SN.

## ➜ NEXT ACTION / SUCCESS CONDITION

Apply premise verification to the remaining organs' amendment sets (LAW/ACT/KNOW/PROVE/VERIFY/LEARN/EVOLVE 0002s) as their locks approach; each application either confirms the procedure or produces the falsifying case that refines it.
