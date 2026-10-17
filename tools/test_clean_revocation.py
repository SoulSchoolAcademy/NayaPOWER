"""Adversarial tests for UD-11 clean revocation.

Every test names what it proves. The suite must also prove the negative:
a mark-everything-REVOKED engine and an ignore-the-revocation engine both
fail these tests — selectivity is the property under test.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clean_revocation import (
    UNAFFECTED, REQUALIFIED, DOWNGRADED, INSUFFICIENT_DATA, SUSPENDED,
    REVOKED, ELIGIBLE, REVOKED_E, CONFIRMED, POSSIBLE,
    Evidence, SupportPath, Claim, RevocationEngine,
    FencingToken, ProjectionLayer, Publisher, RecoveryLog, ReplayEvent,
    PUB_COMMITTED, PUB_STALE_DEPENDENCY, PUB_WRITE_CONFLICT,
    READ_ALLOW, READ_STALE,
    MUTANTS, verify_law,
)

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail and not cond else ""))


def ev(eid, fragments=("full",), regions=("staging", "production")):
    return Evidence(eid, content_hash="h-" + eid, fragments=frozenset(fragments),
                    regions=frozenset(regions))


def req(*pairs):
    return frozenset(pairs)


def sharpest_engine(derived=False):
    """C=(E1^E3) v (E2^E4) v (E3^E4)[staging]; D=(E5)."""
    eng = RevocationEngine()
    for eid in ("E1", "E2", "E3", "E4", "E5"):
        eng.add_evidence(ev(eid))
    if derived:
        eng.derive_evidence("E2", "E1")  # E2 secretly derived from E1
    eng.add_claim(Claim("C", paths=[
        SupportPath(req(("E1", "full"), ("E3", "full"))),
        SupportPath(req(("E2", "full"), ("E4", "full"))),
        SupportPath(req(("E3", "full"), ("E4", "full")),
                    region=frozenset({"staging"})),
    ]))
    eng.add_claim(Claim("D", paths=[SupportPath(req(("E5", "full")))]))
    return eng


# 1. Sharpest case: revoke E1 -> C REQUALIFIED via E2^E4, D UNAFFECTED.
eng = sharpest_engine()
rep = eng.revoke("E1", reason="E1 exposed; blind-certification withdrawn")
by_id = {r.claim_id: r for r in rep.recomputes}
check("sharpest: C requalified via independent path",
      by_id["C"].new_verdict == REQUALIFIED, by_id["C"].new_verdict)
check("sharpest: D unaffected (selectivity — not even recomputed)",
      "D" not in by_id and eng.claims["D"].verdict == UNAFFECTED,
      str([r.claim_id for r in rep.recomputes]))
check("sharpest: exactly the affected closure recomputed",
      {r.claim_id for r in rep.recomputes} == {"C"},
      str([r.claim_id for r in rep.recomputes]))
check("sharpest: evidence history preserved (not deleted)",
      "E1" in eng.evidence and eng.ledger.current("E1") == REVOKED_E)

# 2. False corroboration: E2 derived from E1 -> no independent path.
eng2 = sharpest_engine(derived=True)
rep2 = eng2.revoke("E1", reason="E1 exposed")
by2 = {r.claim_id: r for r in rep2.recomputes}
check("false-corroboration: tainted E2 path does not requalify",
      by2["C"].new_verdict == DOWNGRADED and by2["C"].new_region == frozenset({"staging"}),
      f"{by2['C'].new_verdict} {set(by2['C'].new_region)}")
check("false-corroboration: D still unaffected",
      "D" not in by2 and eng2.claims["D"].verdict == UNAFFECTED)

# 3. A claim needing only E1 loses qualification.
eng3 = RevocationEngine()
for eid in ("E1", "E2"):
    eng3.add_evidence(ev(eid))
eng3.add_claim(Claim("A", paths=[SupportPath(req(("E1", "full"),))]))
eng3.add_claim(Claim("B", paths=[SupportPath(req(("E2", "full"),))]))
rep3 = eng3.revoke("E1", reason="confirmed compromise")
by3 = {r.claim_id: r for r in rep3.recomputes}
check("dependent claim revoked", by3["A"].new_verdict == REVOKED, by3["A"].new_verdict)
check("independent claim untouched", "B" not in by3)

# 4. Stale publication: delayed writer's old PASS rejected.
eng4 = sharpest_engine()
proj4 = ProjectionLayer(eng4)
pub4 = Publisher(eng4, proj4)
m4 = proj4.build_manifest("summary")  # built at G0
tok4 = FencingToken(reader_id="w1", read_generation=0)
eng4.revoke("E1", reason="E1 exposed")  # G1 commits
out4 = pub4.publish(m4, tok4, expected_generation=0)
check("stale publication rejected (write conflict)",
      out4 == PUB_WRITE_CONFLICT, out4)
check("fencing token does not save a stale write", out4 != PUB_COMMITTED)

# 5. Fresh writer publishes legitimately after rebasing.
m4b = proj4.build_manifest("summary")  # rebuilt at G1
tok4b = FencingToken(reader_id="w1", read_generation=1)
out4b = pub4.publish(m4b, tok4b, expected_generation=1)
check("rebased writer publishes", out4b == PUB_COMMITTED, out4b)

# 6. Manifest built pre-revoke but published at current gen with changed
#    verdicts -> STALE_DEPENDENCY.
eng6 = sharpest_engine()
proj6 = ProjectionLayer(eng6)
pub6 = Publisher(eng6, proj6)
m6 = proj6.build_manifest("note")  # G0, C UNAFFECTED
eng6.revoke("E1", reason="x")      # G1, C REQUALIFIED
out6 = pub6.publish(m6, FencingToken("w", 0), expected_generation=1)
check("changed verdicts -> stale dependency", out6 == PUB_STALE_DEPENDENCY, out6)

# 7. Read-time gate: stale manifest refused on authority routes only.
eng7 = sharpest_engine()
proj7 = ProjectionLayer(eng7)
proj7.build_manifest("summary")
eng7.revoke("E1", reason="x")
check("stale manifest refused on ACT route",
      proj7.read_gate("summary", "ACT") == READ_STALE)
check("stale manifest refused on KNOW_RETRIEVAL",
      proj7.read_gate("summary", "KNOW_RETRIEVAL") == READ_STALE)
check("stale manifest allowed on non-authority route (labeled history)",
      proj7.read_gate("summary", "HISTORY_VIEW") == READ_ALLOW)

# 8. Replay cannot resurrect: old ELIGIBLE event ignored after revocation.
eng8 = sharpest_engine()
rec8 = RecoveryLog(eng8)
rep8 = eng8.revoke("E1", reason="confirmed")
rev_at_revoke = eng8.ledger.revision_of("E1")
old_eligible = ReplayEvent("E1", revision=rev_at_revoke - 1,
                           new_state=ELIGIBLE)
counts = rec8.reconcile([old_eligible])
check("replayed old ELIGIBLE ignored",
      counts["ignored_stale"] == 1 and eng8.ledger.current("E1") == REVOKED_E,
      str(counts))
# Replaying the same event twice is idempotent.
counts2 = rec8.reconcile([old_eligible])
check("replay idempotent", counts2["ignored_stale"] == 1, str(counts2))

# 9. Independent requalification IS permitted: new independent evidence
#    arrives; the withdrawn evidence is untouched (no ABA games on E1).
rev_before = eng8.ledger.revision_of("E1")
r = eng8.requalify_with(ev("E1b"))
check("withdrawn evidence untouched by requalification",
      eng8.ledger.revision_of("E1") == rev_before
      and eng8.ledger.current("E1") == REVOKED_E)
check("new independent evidence eligible",
      eng8.ledger.current("E1b") == ELIGIBLE and r.revision == 1)

# 10. Smallest unit: fragment-scoped revocation.
eng10 = RevocationEngine()
eng10.add_evidence(ev("E1", fragments=("f1", "f2")))
eng10.add_evidence(ev("E2"))
eng10.add_claim(Claim("NEEDS_F1", paths=[SupportPath(req(("E1", "f1"),))]))
eng10.add_claim(Claim("NEEDS_F2", paths=[SupportPath(req(("E1", "f2"),))]))
eng10.add_claim(Claim("NEEDS_E2", paths=[SupportPath(req(("E2", "full"),))]))
rep10 = eng10.revoke("E1", reason="f1 contaminated", fragments={"f1"})
by10 = {x.claim_id: x for x in rep10.recomputes}
check("fragment revoke hits exactly the f1-dependent claim",
      set(by10) == {"NEEDS_F1"}, str(set(by10)))
check("f1 claim revoked", by10["NEEDS_F1"].new_verdict == REVOKED)
check("f2 fragment still eligible",
      eng10.ledger.current("E1", {"f2"}) == ELIGIBLE)

# 11. Possible compromise -> SUSPENDED (hold, don't destroy).
eng11 = RevocationEngine()
eng11.add_evidence(ev("E1"))
eng11.add_claim(Claim("C", paths=[SupportPath(req(("E1", "full"),))]))
rep11 = eng11.revoke("E1", reason="possible compromise", assessment=POSSIBLE)
by11 = {x.claim_id: x for x in rep11.recomputes}
check("possible compromise suspends", by11["C"].new_verdict == SUSPENDED,
      by11["C"].new_verdict)

# 12. Expired evidence -> reassess path exists (not auto-revoke).
eng12 = RevocationEngine()
eng12.add_evidence(ev("E1"))
eng12.ledger.change("E1", "EXPIRED", "freshness lapsed")
check("expired is distinct from revoked",
      eng12.ledger.current("E1") == "EXPIRED")

# 13. Min-paths bar: single surviving path insufficient when bar=2.
eng13 = RevocationEngine()
for eid in ("E1", "E2", "E3"):
    eng13.add_evidence(ev(eid))
eng13.add_claim(Claim("C", paths=[SupportPath(req(("E1", "full"),)),
                                  SupportPath(req(("E2", "full"),)),
                                  SupportPath(req(("E3", "full"),))],
                      min_live_paths=2))
rep13 = eng13.revoke("E1", reason="x")
rep13 = eng13.revoke("E2", reason="x")
by13 = {x.claim_id: x for x in rep13.recomputes}
check("below bar -> insufficient data", by13["C"].new_verdict == INSUFFICIENT_DATA,
      by13["C"].new_verdict)

# 14. The Law, model-checked: clean machine has zero violations across
#     all interleavings; every mutant yields a counterexample.
law = verify_law()
check("S1-S6 hold on clean machine, all interleavings",
      law["clean_violations"] == [],
      str(law["clean_violations"][:2]))
for mutant in MUTANTS:
    hits = law["mutants"][mutant]
    check(f"mutant {mutant} yields counterexample", len(hits) > 0,
          f"{len(hits)} traces")
    if hits:
        name, inter, viols = hits[0]
        invs = sorted({v[0] for v in viols})
        print(f"    e.g. {mutant}: scenario={name} violates {invs}")

# 15. Generation advances exactly once per committed revocation.
eng15 = sharpest_engine()
g0 = eng15.generation
eng15.revoke("E1", reason="x")
check("one revocation = one generation", eng15.generation == g0 + 1)

# 16. Crash recovery: a fresh engine rebuilt from the receipt log
#     reconstructs the exact committed eligibility state.
eng16 = sharpest_engine()
eng16.revoke("E1", reason="confirmed")
eng16.revoke("E3", reason="confirmed")
fresh = RevocationEngine()
rec16 = RecoveryLog(fresh)
evts16 = [ReplayEvent(r.evidence_id, r.revision, r.new_state, r.fragments)
          for r in eng16.ledger.receipts()]
counts16 = rec16.reconcile(evts16)
same = all(fresh.ledger.current(eid) == eng16.ledger.current(eid)
           and fresh.ledger.revision_of(eid) == eng16.ledger.revision_of(eid)
           for eid in ("E1", "E2", "E3", "E4", "E5"))
check("crash recovery reconstructs committed state",
      counts16["applied"] == len(evts16) and same, str(counts16))
check("recovered ledger still refuses resurrection",
      rec16.reconcile([ReplayEvent("E1", 1, ELIGIBLE)])["ignored_stale"] == 1)

# 17. Consecutive revocations: each recomputes its own closure; the
#     earlier revocation is never forgotten by the later recompute.
eng17 = sharpest_engine()
eng17.revoke("E1", reason="x")
rep17 = eng17.revoke("E3", reason="y")
by17 = {x.claim_id: x for x in rep17.recomputes}
# After E1 revoked: C requalified via E2^E4. Revoking E3 now kills
# path1 (already dead) and the staging path -> C must NOT come back.
check("second revocation recomputes affected closure",
      by17["C"].new_verdict == REQUALIFIED, by17["C"].new_verdict)
check("earlier revocation not forgotten",
      eng17.ledger.current("E1") == REVOKED_E)

print()
print(f"{len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
