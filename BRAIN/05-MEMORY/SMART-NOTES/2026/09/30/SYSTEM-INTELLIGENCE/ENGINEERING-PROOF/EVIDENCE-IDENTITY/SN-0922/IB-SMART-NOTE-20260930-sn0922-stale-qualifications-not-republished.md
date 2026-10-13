# Preventing Stale Qualifications From Being Republished

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0922-stale-qualifications-not-republished
**Smart Note:** SN-0922
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

No cached artifact, worker, or successor may publish or reuse a qualification unless its evidence dependencies are valid at that exact moment. A qualification whose evidence moved is not "probably fine" — it is unpublished until re-validated.

## HUMAN NOTE

This is the consistency law that closes the loop opened by the correction law (D33). D33 says: when evidence is revoked, recompute every dependent conclusion. D35 says: even when nobody told you evidence moved, never publish from a cached qualification — check the evidence is still valid at publication time, every time.

The concrete gap this carries: the existing version-aware checks do NOT establish transactional compare-and-swap, fencing tokens, atomic revocation ordering, or concurrency-safe publication. The repair is to connect the existing version logic to an authoritative atomic publication boundary, with adversarial race tests. Bounded verification candidate; the repair lane has priority while main is red.

## CHILD NOTE

Don't trust a sticker just because it was true yesterday. Before you show anyone your answer, check that the reasons behind it are still true right now. If anything changed, redo the work before you show it.

## GRANDMA NOTE

Think of it like a certificate of inspection on an elevator. Just because it passed inspection last month doesn't mean it passes today — you check the current date before you ride, every time. A Naya that acts on old certificates is riding elevators nobody inspected.

## NAYA NOTE

Before publishing, reusing, or citing any qualification — a verdict, a score, a certificate, a claim — resolve the validity of its evidence dependencies at that moment, not at the moment the qualification was produced. Cached qualifications are guilty until proven innocent: re-validate, then publish.

The atomic-publication gap is real machinery work: version stamps exist, but nothing today guarantees that a revocation and a publication cannot interleave. Treat that as a concurrency contract to be built and race-tested, not a documentation nicety.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "directive": "D35",
  "doctrine": "stale_qualification_consistency",
  "rule": "no cached artifact, worker, or successor may publish or reuse a qualification unless its evidence dependencies are valid at that moment",
  "checks_required_at_publication": ["evidence_dependencies_current", "no_revocation_since_qualification", "atomic_publication_boundary"],
  "known_gap": "version-aware checks exist but do not establish transactional compare-and-swap, fencing tokens, atomic revocation ordering, or concurrency-safe publication",
  "repair": "connect existing version logic to an authoritative atomic publication boundary with adversarial race tests",
  "repair_priority_note": "bounded verification candidate; repair lane has priority while main is red",
  "related_directives": ["D32", "D33", "D34"]
}
~~~

## 🟢 LEARNING LESSON

A qualification is a claim with an expiration the evidence controls. Systems that cache qualifications without re-checking evidence at publication time accumulate stale authority silently — the most dangerous drift is the one that still looks certified.

## 🟡 WHAT IT MEANS

Freshness of evidence is part of a qualification's identity. Without an atomic publication boundary, revocation and publication can race, and the system can speak with a voice its evidence has already withdrawn.

## ⚪ WHAT'S IN IT FOR YOU

Decisions made on stale qualifications fail in ways that look like the evidence's fault but are actually the publication pipeline's fault. Checking at the moment of use eliminates an entire class of ghost-authority errors.

## 🟨 HOW TO APPLY / HOW TO USE

When designing any claim-publishing path: require a publication-time validity check against current evidence dependencies; implement transactional compare-and-swap or fencing tokens around revocation vs. publication; write adversarial race tests that interleave revocation and publication and demand exactly one winner.

## 🔗 HOW IT CONNECTS

- **SUPPORTS** → D33 Selective Evidence Revocation and Claim Requalification (SN-0913) — D33 corrects conclusions after revocation; D35 prevents publication before re-validation
- **USES** → D32 Evidence-Bounded Uncertainty Propagation (SN-0912) — downstream certainty can never exceed what the current evidence supports
- **GOVERNS** → every worker, artifact, and successor package that republishes qualifications

## 🧭 KEY DECISIONS / PRINCIPLES

- A qualification is valid only against evidence that is valid at publication time.
- Cached qualifications must be re-validated at the moment of use, not trusted on issuance time.
- Version stamps alone are not an atomic publication contract — they need transactional enforcement and race tests.
- Repair-lane priority holds while main is red: bounded verification candidate, not an emergency patch.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "directive": "D35",
  "board_comment_id": "6101449710",
  "classification_receipt": "6101483551",
  "classification_time": "2026-10-10T19:44:44Z",
  "venue": "NayaPOWER#2175 (successor venue; #1354 at 2500-comment hard cap)",
  "evidence_held": "shared-state.json cached comment bodies",
  "truth_state": "CANDIDATE"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This note captures the doctrine and the identified machinery gap. It does not implement the atomic publication boundary, does not prove the race cannot already interleave in current code, and does not authorize any wiring change — wiring needs Shawn's word.

## ➜ NEXT ACTION / SUCCESS CONDITION

Route to the repair lane: connect version logic to an atomic publication boundary with adversarial race tests. Until then, every lane publishing qualifications checks evidence validity at the moment of use.
