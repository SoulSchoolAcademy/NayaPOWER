# Every BRAIN Domain Needs a Registered Floor — An Unregistered Domain Passes Full Deletion Silently

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0850-every-brain-domain-needs-a-floor
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6093004193 (2026-10-10T02:51:51Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The brain index's `--check` ratchet guards registered domain floors — but a domain that was never registered has no floor, and a full deletion of that domain passes `--check` silently. BRAIN/00-ACTIVATION/ (Activation Package v1, PR #1971) shipped without a floor entry: every file could vanish and the check would report OK. PR #2105 (`fix(brain): register 00-ACTIVATION domain floor (deletion tripwire)`) closed the ratchet gap: the index now holds the floor for 00-ACTIVATION, and an adversarial deletion proof exits 2 naming the domain. The rule: no BRAIN domain is complete until its floor is registered — a tripwire that fails loudly on full deletion. Registration is not bookkeeping; it is the mechanism that makes deletion detectable.

## 🩷 HUMAN NOTE

Think of a museum with a security camera per room. A room the floor plan forgot gets no camera — and a thief can empty it while the monitors show "all clear." That's what happened with the brain: the index checked everything it knew about, but nobody had registered the new 00-ACTIVATION room, so deleting it entirely would have passed every check. The fix: every room must be on the floor plan with a tripwire — the moment the whole room goes dark, the alarm names the room. PR #2105 added the missing camera and proved it works by simulating the theft.

## 🟣 CHILD NOTE

Imagine a burglar alarm for every room in a house — but someone forgot to put one in the new playroom. If a thief empties the playroom, the alarm still says "everything's fine!" because it didn't know the playroom existed. Always put an alarm in every new room, and test it by pretending to steal everything from it.

## 🔵 GRANDMA NOTE

Every new room gets an alarm, dear — the one without an alarm is the one the thief will find. And test the alarm by walking into the room yourself, not by hoping it works.

## 🟠 NAYA NOTE

1. The failure mode is a registration gap, not a check gap. The check (`--check`, 1233 files, green) was working exactly as designed — it verifies floors, and a floor that was never registered is a floor that cannot be violated. The silent pass is the check behaving correctly over incomplete data.
2. The mechanical repair: the floor registry must be complete over all BRAIN domains as a precondition, not a nice-to-have. PR #2105 registered 00-ACTIVATION's floor, put the new head (`72d94c87`) on the exact live tip (`9aa04ab8`), and shipped an adversarial deletion proof (exits 2 naming the domain) as the acceptance test. 25/25 tests, `--check` OK.
3. The durable pattern: any system that guards by registry (domain floors, migration ledgers, permission lists) fails open on unregistered members. The admission ritual for a new domain must include "floor registered + adversarial deletion proof green" — otherwise the ratchet has a hole shaped exactly like the newest room.
4. This is the ratchet doctrine: a ratchet that doesn't hold every domain holds no domain — the gap migrates to whatever was added last.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261009-sn0850-every-brain-domain-needs-a-floor",
  "automatic_truth_ceiling": "CANDIDATE",
  "captured": "2026-10-09",
  "rule": "domain_floor_registration",
  "statement": "every_registered_brain_domain_must_have_a_floor_entry_or_full_deletion_passes_silently",
  "admissible_form": "floor_registered + adversarial_deletion_proof_green_before_domain_admitted",
  "inadmissible_form": "domain_added_without_floor (check_stays_green_over_incomplete_data)",
  "evidence": {
    "note": "#1354/6093004193 (2026-10-10T02:51:51Z, Naya 4 KNOW-driver)",
    "gap": "BRAIN/00-ACTIVATION/ (Activation Package v1, PR #1971) had no floor entry — full deletion passed --check silently",
    "fix": "PR #2105 fix(brain): register 00-ACTIVATION domain floor (deletion tripwire); head 72d94c87 on exact tip 9aa04ab8; mergeable clean; --check OK (1233 files); 25/25 tests; adversarial deletion proof exits 2 naming the domain",
    "signout": "#1720 sign-out"
  },
  "applies_to": ["brain_index_registry", "migration_ledgers", "any_guard_by_registry"]
}
~~~

## 🟢 LEARNING LESSON

The check was green and the room was empty — both true at once. The index guards what it knows, so knowing is the mechanism, not the metadata. When a new domain is added without its floor, the ratchet's strongest property (fails loudly) inverts exactly where the newest work lives. The adversarial deletion proof is the admission ticket: prove the tripwire fires before the domain is considered guarded.

## 🟡 WHAT IT MEANS

No new BRAIN domain is admitted without a registered floor and a green adversarial deletion proof. Cold successors treat "floor registered" as a precondition on the domain, not a later cleanup item. The ratchet's coverage is audited by domain list, never assumed from `--check` green alone.

## 🟨 HOW TO APPLY / HOW TO USE

Adding a BRAIN domain → write its floor entry into the index registry first → run the adversarial deletion proof (expect exit 2 naming the domain) → only then ship content under that domain. Auditing an existing domain → list all domains → for each, confirm a floor entry exists and the deletion proof fires → register and prove any gap immediately (PR shape of #2105).

## 🔗 HOW IT CONNECTS

- **PAIRS** → SN-0125 — verify the tree after push: pins prove coverage; here, the floor proves the registry is complete
- **GOVERNS** → brain index `--check` trust: green is evidence of coverage only when the floor registry is complete
- **PAIRS** → register-every-migration ledger lesson (2026-09-30): a guard-by-registry fails open on unregistered members — the same failure shape

## 🧾 PROOF / PROVENANCE

- #1354 comment 6093004193 (2026-10-10T02:51:51Z, Naya 4 KNOW-driver): "PR #2105 opened: `fix(brain): register 00-ACTIVATION domain floor (deletion tripwire)`. Closes the ratchet gap where BRAIN/00-ACTIVATION/ (Activation Package v1, PR #1971) had no floor entry — full deletion passed silently. Head `72d94c87` on exact tip `9aa04ab8`, mergeable clean, --check OK (1233 files), 25/25 tests, adversarial deletion proof exits 2 naming the domain."
- #1720 sign-out: KNOW 9.0 → 9.3 on this evidence.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Truth state is CANDIDATE: observed once as a clean object lesson with a closed repair. The rule does not claim the floor registry is now complete — it claims completeness must be verified by domain list, not inferred from a green check. A second domain added without a floor would be a regression, not a refutation.

## ➜ NEXT ACTION / SUCCESS CONDITION

Every BRAIN domain carries a floor entry and a green adversarial deletion proof. Success is behavioral: no future `--check` green is ever treated as proof of domain coverage without the domain list being walked.
