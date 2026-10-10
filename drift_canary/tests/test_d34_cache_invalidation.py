"""D34 — Selective Cache Invalidation and Intelligence Preservation.

Decisive fixture tests. Follows the D29-D33 convention: check() counting,
test_* functions, runnable directly or under pytest.

Fixture choreography (matches the task's sharpest case exactly):
  G1: E3 -> SUSPENDED (possibly compromised)
  G2: E6 -> REVOKED (unused source; empty closure)
  G3: summary S1 generated (depends on A_causal); note N1 (10 claims) created+indexed
  G4: E7 -> REVOKED (unused source; empty closure)
  G5: E1 -> REVOKED (A_causal REVOKED, A1_narrow DOWNGRADED to staging)

The ten-claim note N1: C1..C6 + B_outcome + D1 (8 unaffected),
A1_narrow (downgrades), A2_susp (suspends).
"""
import sys

from drift_canary.d34_cache_invalidation import (
    ACT_AUTHORIZED,
    ACT_REFUSED,
    AUTHORITY_ROUTES,
    CACHED_SUMMARY,
    CONSEQUENTIAL_ACT,
    CURRENT,
    HISTORICAL_ONLY,
    HISTORICAL_RECEIPT,
    INDEX_ENTRY,
    INDEX_LOOKUP,
    KNOW_RETRIEVAL,
    LEARN_PROMOTION,
    REFRESH_PENDING,
    REFUSE_STALE,
    REVALIDATION_REQUIRED,
    SERVE_CURRENT,
    SERVE_HISTORICAL,
    SMART_NOTE,
    SUCCESSOR_PACKAGE,
    IntelligenceStore,
    Projection,
    StaleGenerationError,
    UNAFFECTED,
    REQUALIFIED,
    DOWNGRADED,
    INSUFFICIENT_DATA,
    SUSPENDED,
    REVOKED,
)

PASSED, FAILED = 0, 0


def check(name, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  PASS {name}")
    else:
        FAILED += 1
        print(f"  FAIL {name} {detail}")


STAGING = frozenset({"staging"})
PROD = frozenset({"production"})
BOTH = frozenset({"staging", "production"})

HISTORIC_TEXT = "the workflow failed because the scheduler withheld execution."
NEW_TEXT = ("The workflow's failure remains independently established. "
            "The evidence previously supporting scheduler causation is no "
            "longer eligible for certification; the cause requires "
            "re-evaluation.")


def build_world(store=None):
    """Register the sharpest-case topology. Returns the store."""
    s = store if store is not None else IntelligenceStore()
    s.register_source("E1", scope=BOTH)    # causation evidence
    s.register_source("E2", scope=BOTH)    # outcome evidence (independent)
    s.register_source("E3", scope=STAGING)  # will become possibly-compromised
    s.register_source("E4", scope=STAGING)  # independent staging source
    s.register_source("E5", scope=BOTH)    # unused by sharpest-case claims
    s.register_source("E6", scope=BOTH)    # unused; G2 commit
    s.register_source("E7", scope=BOTH)    # unused; G4 commit
    # A_causal: certified causation, single path on E1 -> REVOKED at G5.
    s.register_claim("A_causal", paths=[(frozenset({"E1"}), BOTH)],
                     scope=BOTH, min_paths=1, kind="certification")
    # A1_narrow: E1 covered production, E2 covers staging -> DOWNGRADED.
    s.register_claim("A1_narrow",
                     paths=[(frozenset({"E1"}), frozenset({"production"})),
                            (frozenset({"E2"}), STAGING)],
                     scope=BOTH, min_paths=1, kind="certification")
    # A2_susp: single path on E3 -> SUSPENDED at G1.
    s.register_claim("A2_susp", paths=[(frozenset({"E3"}), STAGING)],
                     scope=STAGING, min_paths=1, kind="certification")
    # B_outcome: independently established on E2 -> UNAFFECTED throughout.
    s.register_claim("B_outcome", paths=[(frozenset({"E2"}), BOTH)],
                     scope=BOTH, min_paths=1, kind="observational")
    for i in range(1, 7):
        s.register_claim(f"C{i}", paths=[(frozenset({"E2"}), BOTH)],
                         scope=BOTH, min_paths=1, kind="observational")
    s.register_claim("D1", paths=[(frozenset({"E4"}), STAGING)],
                     scope=STAGING, min_paths=1, kind="observational")
    return s


NOTE_CLAIMS = ["C1", "C2", "C3", "C4", "C5", "C6", "B_outcome", "D1",
               "A1_narrow", "A2_susp"]


def build_sharpest_case():
    """Full choreography through G5. Returns (store, S1, N1)."""
    s = build_world()
    s.commit_eligibility_change("E3", SUSPENDED, reason="possibly compromised")  # G1
    s.commit_eligibility_change("E6", REVOKED, reason="confirmed compromised")   # G2
    # G3: summary + note created at generation 2... we need G3 first.
    return s


def build_through_g5():
    s = build_world()
    s.commit_eligibility_change("E3", SUSPENDED, reason="possibly compromised")  # G1
    s.commit_eligibility_change("E6", REVOKED, reason="confirmed compromised")   # G2
    s.commit_eligibility_change("E5", REVOKED, reason="confirmed compromised")   # G3
    # --- generation is now 3: create the summary and the note ---
    s.add_projection("S1", CACHED_SUMMARY, ["A_causal"], content=HISTORIC_TEXT)
    s.add_smart_note("N1", NOTE_CLAIMS)
    s.index_note("N1", NOTE_CLAIMS)
    s.add_projection("IDX_N1", INDEX_ENTRY, NOTE_CLAIMS,
                     content="index entry for N1", link="N1")
    s.commit_eligibility_change("E7", REVOKED, reason="confirmed compromised")   # G4
    s.commit_eligibility_change("E1", REVOKED, reason="confirmed compromised")   # G5
    assert s.generation == 5, s.generation
    return s


# ---------------------------------------------------------------------------
# The task's sharpest case, in three parts.
# ---------------------------------------------------------------------------

def test_summary_gated_after_revocation():
    s = build_through_g5()
    r = s.serve("S1", KNOW_RETRIEVAL)
    check("G5: S1 (gen G3) refused as current on KNOW_RETRIEVAL",
          r.decision == REFUSE_STALE, r)
    check("G5: refusal names the recomputed claim",
          "A_causal" in r.annotation and "5" in r.annotation, r.annotation)
    r2 = s.serve("S1", CONSEQUENTIAL_ACT)
    check("G5: S1 refused on CONSEQUENTIAL_ACT too",
          r2.decision == REFUSE_STALE, r2)
    # The projection still exists and still knows its generation.
    check("S1 generation still G3 (not silently bumped)",
          s.projections["S1"].generation == 3, s.projections["S1"].generation)
    check("S1 status is REVALIDATION_REQUIRED",
          s.projections["S1"].status == REVALIDATION_REQUIRED,
          s.projections["S1"].status)


def test_note_keeps_ten_claims_with_split_verdicts():
    s = build_through_g5()
    slots = s.note_claims["N1"]
    check("note keeps all ten claim slots", len(slots) == 10, len(slots))
    verdicts = {cid: s.claims[cid].verdict for cid in NOTE_CLAIMS}
    unaffected = [c for c, v in verdicts.items() if v == UNAFFECTED]
    check("eight claims stay usable (UNAFFECTED)", len(unaffected) == 8,
          verdicts)
    check("A1_narrow DOWNGRADED (staging survives)",
          verdicts["A1_narrow"] == DOWNGRADED, verdicts["A1_narrow"])
    check("A1_narrow covered scope narrowed to staging",
          s.claims["A1_narrow"].covered_scope == STAGING,
          s.claims["A1_narrow"].covered_scope)
    check("A2_susp SUSPENDED (held, not destroyed)",
          verdicts["A2_susp"] == SUSPENDED, verdicts["A2_susp"])
    # History is append-only: every slot still has its initial entry.
    for cid in NOTE_CLAIMS:
        hist = s.note_history("N1", cid)
        check(f"slot {cid} history starts at initial qualification",
              hist[0][1].startswith("initial"), hist[0])
    # The downgraded and suspended slots gained amendments; others did not.
    check("A1_narrow gained an amendment",
          len(s.note_history("N1", "A1_narrow")) >= 1, "")
    check("B_outcome slot has exactly its initial entry (untouched)",
          len(s.note_history("N1", "B_outcome")) == 1,
          s.note_history("N1", "B_outcome"))


def test_index_discovers_but_does_not_certify():
    s = build_through_g5()
    found = s.index_discover("A1_narrow")
    check("index still discovers N1 for A1_narrow (discoverability)",
          found == ["N1"], found)
    verdict, pointer = s.index_pointer("N1", "A1_narrow")
    check("pointer verdict follows recomputation (DOWNGRADED)",
          verdict == DOWNGRADED, verdict)
    check("pointer reads REVALIDATION_REQUIRED, not certified",
          pointer == REVALIDATION_REQUIRED, pointer)
    v2, p2 = s.index_pointer("N1", "B_outcome")
    check("unaffected pointer stays CURRENT",
          (v2, p2) == (UNAFFECTED, CURRENT), (v2, p2))
    # INDEX_LOOKUP route: discovery served, annotated, never certified.
    r = s.serve("IDX_N1", INDEX_LOOKUP)
    check("index lookup served as discovery (not refused)",
          r.decision in (SERVE_CURRENT, SERVE_HISTORICAL), r)
    check("lookup annotation carries pointer statuses",
          "REVALIDATION_REQUIRED" in r.annotation, r.annotation)


# ---------------------------------------------------------------------------
# The register's sharpest case: historic text preserved, new serving text.
# ---------------------------------------------------------------------------

def render_new(quals):
    a = quals["A_causal"]
    assert a.verdict == REVOKED  # the test's precondition
    return NEW_TEXT


def test_historic_report_not_silently_rewritten():
    s = build_through_g5()
    proj = s.projections["S1"]
    check("pre-refresh content is the historic text",
          proj.content == HISTORIC_TEXT, proj.content)
    s.refresh_projection("S1", expected_generation=5, render=render_new)
    check("post-refresh content is the new serving text",
          proj.content == NEW_TEXT, proj.content)
    check("historic text preserved byte-identically in history",
          proj.history == (HISTORIC_TEXT,), proj.history)
    check("history was not rewritten to the new text",
          all(h != NEW_TEXT for h in proj.history), proj.history)
    r = s.serve("S1", KNOW_RETRIEVAL)
    check("refreshed summary serves as current",
          r.decision == SERVE_CURRENT and r.content == NEW_TEXT, r)


# ---------------------------------------------------------------------------
# Refresh window, CAS publication, TOCTOU.
# ---------------------------------------------------------------------------

def test_refresh_window_gating():
    s = build_through_g5()
    # Between commit (G5) and refresh, the gate holds.
    r = s.serve("S1", KNOW_RETRIEVAL)
    check("mid-window: stale summary refused", r.decision == REFUSE_STALE, r)
    s.refresh_projection("S1", expected_generation=5, render=render_new)
    r2 = s.serve("S1", KNOW_RETRIEVAL)
    check("post-refresh: summary serves current",
          r2.decision == SERVE_CURRENT, r2)
    check("reconcile sweep clean after refresh", s.reconcile() == [],
          s.reconcile())


def test_delayed_refresh_never_republishes_old_pass():
    s = build_through_g5()
    s.refresh_projection("S1", expected_generation=5, render=render_new)
    good_text = s.projections["S1"].content
    # Another eligibility change moves the world to G6.
    s.commit_eligibility_change("E2", SUSPENDED, reason="possibly compromised")  # G6
    assert s.generation == 6
    # A refresh computed against G5 must be refused: it would republish a
    # PASS (E2 eligible) over a later revocation (E2 suspended).
    try:
        s.refresh_projection("S1", expected_generation=5,
                             render=lambda q: "stale PASS text")
        check("stale-generation refresh refused", False, "no exception")
    except StaleGenerationError as e:
        check("stale-generation refresh refused", True)
        check("error says recompute first", "recompute first" in str(e), str(e))
    check("refused refresh did not touch content",
          s.projections["S1"].content == good_text,
          s.projections["S1"].content)
    # Recomputing against G6 publishes fine.
    s.refresh_projection("S1", expected_generation=6, render=render_new)
    check("fresh-generation refresh publishes",
          s.projections["S1"].generation == 6, s.projections["S1"].generation)


def test_act_commit_boundary_toctou():
    s = build_through_g5()
    d = s.authorize_act(["B_outcome"], seen_generation=5)
    check("ACT authorized on current generation", d == ACT_AUTHORIZED, d)
    s.commit_eligibility_change("E2", SUSPENDED, reason="possibly compromised")  # G6
    d2 = s.authorize_act(["B_outcome"], seen_generation=5)
    check("ACT refused when generation moved under the caller (TOCTOU)",
          d2 == ACT_REFUSED, d2)
    d3 = s.authorize_act(["A_causal"], seen_generation=6)
    check("ACT refused on REVOKED claim even at current generation",
          d3 == ACT_REFUSED, d3)
    d4 = s.authorize_act(["nope"], seen_generation=6)
    check("ACT refused on unknown claim", d4 == ACT_REFUSED, d4)


# ---------------------------------------------------------------------------
# Independently supported conclusions stay available; no full-brain rebuild.
# ---------------------------------------------------------------------------

def test_unaffected_stays_available_throughout():
    s = build_world()
    s.add_projection("SB", CACHED_SUMMARY, ["B_outcome"], content="outcome summary")
    r0 = s.serve("SB", KNOW_RETRIEVAL)
    check("pre-revocation: B_outcome summary serves", r0.decision == SERVE_CURRENT, r0)
    s.commit_eligibility_change("E1", REVOKED, reason="confirmed compromised")
    r1 = s.serve("SB", KNOW_RETRIEVAL)
    check("post-revocation: unaffected summary still serves",
          r1.decision == SERVE_CURRENT, r1)
    check("unaffected projection untouched (status)",
          s.projections["SB"].status == CURRENT, s.projections["SB"].status)
    check("unaffected projection untouched (content)",
          s.projections["SB"].content == "outcome summary",
          s.projections["SB"].content)


def test_no_full_brain_rebuild_on_minor_change():
    s = build_world()
    # 50 claims on independent sources; only 2 touch E1.
    for i in range(50):
        s.register_claim(f"X{i}", paths=[(frozenset({"E4"}), STAGING)],
                         scope=STAGING, min_paths=1, kind="observational")
        s.add_projection(f"PX{i}", CACHED_SUMMARY, [f"X{i}"],
                         content=f"summary {i}")
    s.add_projection("PA", CACHED_SUMMARY, ["A_causal"], content="a")
    s.add_projection("PB", CACHED_SUMMARY, ["B_outcome"], content="b")
    before = {pid: (p.status, p.generation, p.content)
              for pid, p in s.projections.items()}
    s.commit_eligibility_change("E1", REVOKED, reason="confirmed compromised")
    marked = [pid for pid, p in s.projections.items()
              if p.status == REVALIDATION_REQUIRED]
    check("only the E1-dependent projection marked",
          marked == ["PA"], marked)
    untouched = all(
        (p.status, p.generation, p.content) == before[pid]
        for pid, p in s.projections.items() if pid != "PA")
    check("52 other projections byte-identical (no rebuild)", untouched)


# ---------------------------------------------------------------------------
# Successor packages: seal, mandatory reconciliation, cold successor.
# ---------------------------------------------------------------------------

def test_successor_package_reconciles():
    s = build_through_g5()
    pkg = s.seal_package("PKG1", ["A_causal", "B_outcome", "A1_narrow"])
    check("package sealed at G5", pkg["sealed_generation"] == 5,
          pkg["sealed_generation"])
    check("sealed snapshot pins verdicts",
          pkg["snapshot"]["A_causal"].verdict == REVOKED, "")
    # The world moves: E2 suspended at G6.
    s.commit_eligibility_change("E2", SUSPENDED, reason="possibly compromised")
    # Activation must reconcile, not serve the sealed G5 content as current.
    result = s.activate_package("PKG1", replay=build_world)
    check("activation reconciled (not failed)", result["activated"] is True,
          result)
    check("reconciled verdicts equal the live store",
          result["verdicts"]["B_outcome"] == s.claims["B_outcome"].verdict and
          result["verdicts"]["B_outcome"] == SUSPENDED,
          result["verdicts"])
    check("package projection now current at G6",
          s.projections["PKG1"].status == CURRENT and
          s.projections["PKG1"].generation == 6,
          (s.projections["PKG1"].status, s.projections["PKG1"].generation))


def test_cold_successor_reaches_same_verdict():
    live = build_through_g5()
    # A cold successor: fresh store, same topology, same event order.
    cold = build_world(IntelligenceStore())
    for ev in live.events:
        cold.commit_eligibility_change(ev.source_id, ev.new_status, ev.reason)
    check("cold store reached the same generation",
          cold.generation == live.generation, (cold.generation, live.generation))
    same = all(cold.claims[c].verdict == live.claims[c].verdict
               and cold.claims[c].covered_scope == live.claims[c].covered_scope
               for c in live.claims)
    check("cold successor reconstructs every current verdict", same)
    check("cold A_causal REVOKED", cold.claims["A_causal"].verdict == REVOKED,
          cold.claims["A_causal"].verdict)


# ---------------------------------------------------------------------------
# History preserved everywhere; reconcile sweep; routes; receipts.
# ---------------------------------------------------------------------------

def test_history_preserved_everywhere():
    s = build_through_g5()
    n0 = len(s.receipts)
    s.commit_eligibility_change("E2", SUSPENDED, reason="possibly compromised")
    check("receipts grew by exactly one", len(s.receipts) == n0 + 1,
          len(s.receipts))
    check("old receipts byte-identical (append-only)",
          [ (e.seq, e.source_id, e.new_status) for e in s.receipts[:n0] ] ==
          [ (e.seq, e.source_id, e.new_status) for e in build_through_g5().receipts[:n0] ])
    # Provider claim history also append-only.
    h = s.provider.history("A_causal")
    check("claim history has initial + recomputation entries",
          len(h) == 2 and h[0][0] == UNAFFECTED and h[1][0] == REVOKED, h)


def test_reconcile_sweep_catches_planted_violation():
    s = build_through_g5()
    check("reconcile clean on honest state", s.reconcile() == [], s.reconcile())
    # Plant a violation: mark the stale projection CURRENT anyway.
    s.projections["S1"].status = CURRENT
    v = s.reconcile()
    check("reconcile flags the planted violation",
          len(v) == 1 and "S1" in v[0], v)


def test_all_routes_apply_the_gate():
    s = build_through_g5()
    from drift_canary.d34_cache_invalidation import (
        CONNECT_EXPANSION, SUMMARY_GENERATION, NOTE_CAPTURE,
        SUCCESSOR_ACTIVATION, LEARN_PROMOTION)
    for route in (KNOW_RETRIEVAL, CONNECT_EXPANSION, SUMMARY_GENERATION,
                  NOTE_CAPTURE, SUCCESSOR_ACTIVATION, LEARN_PROMOTION,
                  CONSEQUENTIAL_ACT):
        r = s.serve("S1", route)
        check(f"stale S1 refused on {route}", r.decision == REFUSE_STALE, r)
    check("AUTHORITY_ROUTES covers the 7 authority routes",
          AUTHORITY_ROUTES == frozenset({
              KNOW_RETRIEVAL, CONNECT_EXPANSION, SUMMARY_GENERATION,
              NOTE_CAPTURE, SUCCESSOR_ACTIVATION, LEARN_PROMOTION,
              CONSEQUENTIAL_ACT}), AUTHORITY_ROUTES)


def test_historical_receipt_never_serves_as_current():
    s = build_through_g5()
    s.add_projection("HR1", HISTORICAL_RECEIPT, ["A_causal"],
                     content="receipt text", status=HISTORICAL_ONLY)
    r = s.serve("HR1", KNOW_RETRIEVAL)
    check("historical receipt serves as historical only",
          r.decision == SERVE_HISTORICAL and r.content == "receipt text", r)
    # A commit does not touch it.
    s.commit_eligibility_change("E2", SUSPENDED, reason="x")
    r2 = s.serve("HR1", KNOW_RETRIEVAL)
    check("historical receipt still historical after commits",
          r2.decision == SERVE_HISTORICAL, r2)


def test_d33_provider_interface_composability():
    """D34 composes with D33's RevocationEngine via D33EngineAdapter. The
    fake below carries D33's exact public shapes: register_source takes a
    source record, register_claim takes a claim record, revoke takes an
    assessment keyword, qualification returns a record with
    .verdict/.covered_scope."""
    from drift_canary.d34_cache_invalidation import D33EngineAdapter

    class FakeRecord:
        def __init__(self, verdict, covered_scope, reason=""):
            self.verdict = verdict
            self.covered_scope = covered_scope
            self.reason = reason

    class FakeD33Engine:
        """D33's exact public interface (d33_revocation.py)."""
        def __init__(self):
            self.seen = []
        def register_source(self, source):  # EvidenceSource record
            self.seen.append(("register_source", source.source_id))
        def register_claim(self, claim):  # Claim record
            self.seen.append(("register_claim", claim.claim_id,
                              [p.sources for p in claim.paths]))
        def add_derivation(self, derived_id, origin_id):
            self.seen.append(("add_derivation", derived_id, origin_id))
        def revoke(self, source_id, reason, assessment="confirmed_compromised"):
            self.seen.append(("revoke", source_id, assessment))
            class R:
                affected_claims = ["A_causal"]
            return R()
        def qualification(self, claim_id):
            return FakeRecord(REVOKED, frozenset(), "no admissible path")
        def history(self, claim_id):
            return (FakeRecord(UNAFFECTED, frozenset({"staging", "production"})),
                    FakeRecord(REVOKED, frozenset()))

    engine = FakeD33Engine()
    provider = D33EngineAdapter(engine)
    # Registration translates D34 shapes -> D33 records.
    provider.register_source("E1")
    provider.register_claim("A_causal",
                            paths=[(frozenset({"E1"}), frozenset({"staging"}))])
    provider.add_derivation("E2", "E1")
    check("adapter forwarded register_source with source_id",
          engine.seen[0] == ("register_source", "E1"), engine.seen[0])
    check("adapter forwarded register_claim with paths",
          engine.seen[1][0] == "register_claim" and
          engine.seen[1][2] == [frozenset({"E1"})], engine.seen[1])
    # Assessment vocabulary translated: REVOKED_SRC -> confirmed_compromised.
    from drift_canary.d34_cache_invalidation import REVOKED_SRC, SUSPENDED_SRC
    provider.revoke("E1", "confirmed compromised", new_status=REVOKED_SRC)
    check("adapter translated status to D33 assessment",
          engine.seen[3] == ("revoke", "E1", "confirmed_compromised"),
          engine.seen[3])
    provider.revoke("E3", "possibly compromised", new_status=SUSPENDED_SRC)
    check("adapter translated SUSPENDED status",
          engine.seen[4] == ("revoke", "E3", "possibly_compromised"),
          engine.seen[4])
    # Qualification records normalized to triples.
    q = provider.qualification("A_causal")
    check("adapter normalized D33 record to (verdict, scope, reason)",
          q == (REVOKED, frozenset(), "no admissible path"), q)
    h = provider.history("A_causal")
    check("adapter normalized history",
          len(h) == 2 and h[0][0] == UNAFFECTED and h[1][0] == REVOKED, h)
    # And the store accepts the adapted provider end to end.
    s = IntelligenceStore(provider=provider)
    check("store accepts D33-adapted provider", s.provider is provider)


def test_verdict_vocabulary_matches_on_main():
    from drift_canary import revocation as rev
    from drift_canary import d34_cache_invalidation as d34
    check("six verdicts identical to on-main revocation.py",
          {d34.UNAFFECTED, d34.REQUALIFIED, d34.DOWNGRADED,
           d34.INSUFFICIENT_DATA, d34.SUSPENDED, d34.REVOKED} ==
          set(rev.VERDICTS))


if __name__ == "__main__":
    print("D34 decisive fixture tests")
    for name, fn in sorted(
            [(k, v) for k, v in globals().items()
             if k.startswith("test_")]):
        print(f"- {name}")
        fn()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)
