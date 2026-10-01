"""NAYA-KERNEL-KNOW acceptance battery (CANDIDATE — NOT RATIFIED — NOT MERGED).

Mirrors KNOW-NODE-SPEC-CANDIDATE.md §12: valid input reaches the intended
state; malformed input refused with receipted reasons; missing dependencies
fail closed; identity/scope mismatches block; CORE auto-assignment blocked;
provenance loss detected; stale/superseded explicit; dedupe safe; receipts
hashable and re-derivable; cold successor restores identically.
"""
import pytest

from naya_kernel.node_base import GateVerdict, NodeBase
from naya_kernel.nodes import know_node
from naya_kernel.nodes.know_node import KnowNode

NOW = "2026-10-01T03:00:00+00:00"

PRINCIPAL = {"identity": "naya-test", "entitled_scopes": ["public", "team"]}
OUTSIDER = {"identity": "outsider", "entitled_scopes": ["public"]}


def make_candidate(content="The quick brown fox", **overrides):
    cand = {
        "content": content,
        "proposed_class": "CONTEXT",
        "class_signals": [{"signal": "auto-classifier-v0", "value": 0.82}],
        "classifier": "auto",
        "provenance": {"sources": [{
            "kind": "EXTERNAL", "ref": "ext://example/" + content[:8],
            "capturedAt": NOW, "capturedBy": "naya-test"}]},
        "identity_binding": {"verified": True},
        "owner_scope": "public",
        "epistemic_state": "INGESTED",
    }
    cand.update(overrides)
    return cand


def make_query(**overrides):
    q = {
        "identity_binding": {"verified": True},
        "modes": ["structural"],
        "requested_scopes": ["public"],
    }
    q.update(overrides)
    return q


# ------------------------------------------------------------------
# interface
# ------------------------------------------------------------------

def test_module_exposes_node_class():
    assert issubclass(know_node.KnowNode, NodeBase)


def test_manifest_entry_contract():
    entry = KnowNode().manifest_entry()
    assert entry.node_id == "NAYA-KERNEL-KNOW"
    assert entry.version == "0.1.0-candidate"
    assert len(entry.responsibilities) >= 5


def test_persisted_transitions_cover_spec_machine():
    transitions = KnowNode().persisted_transitions()
    for t in ["CANDIDATE -> CLASSIFIED", "CLASSIFIED -> ACTIVE",
              "CANDIDATE -> REFUSED", "ACTIVE -> SUPERSEDED",
              "ACTIVE -> CONTRADICTED", "ACTIVE -> INVALIDATED",
              "ACTIVE -> EXPIRED", "ACTIVE -> PROVENANCE_REVIEW",
              "CANDIDATE -> CLASSIFICATION_PENDING"]:
        assert t in transitions, "missing transition %s" % t


def test_evidence_hooks_declared():
    assert KnowNode().evidence_hooks()


def test_authority_checks_grant_nothing():
    checks = KnowNode().authority_checks()
    assert checks, "KNOW must declare the authority boundary it does not grant"
    for check in checks:
        negated = check.replace("no_authority_grant_performed", "")
        assert "grant" not in negated, \
            "authority check affirms granting: %s" % check


# ------------------------------------------------------------------
# §3.1 ingestion gate — acceptance 1, 2, 3
# ------------------------------------------------------------------

def test_ingest_valid_reaches_serving():
    """Acceptance 1: valid input reaches the intended state."""
    node = KnowNode()
    receipt = node.ingest(make_candidate(), PRINCIPAL, now=NOW)
    assert receipt["operation"] == "INGEST"
    assert receipt["afterState"] == "ACTIVE"
    assert receipt["blockId"]
    assert receipt["receipt_hash"]
    block = node.blocks[receipt["blockId"]]
    assert block["state"] == "ACTIVE"
    assert block["class"] == "CONTEXT"
    assert block["contentHash"]
    # serving admission sees it
    result = node.retrieve(make_query(), PRINCIPAL, now=NOW)
    assert result["admitted"] is True
    assert [b["id"] for b in result["blocks"]] == [receipt["blockId"]]


def test_ingest_malformed_refused_with_receipted_reasons():
    """Acceptance 2: malformed input refused with receipted reasons."""
    node = KnowNode()
    receipt = node.ingest(make_candidate(content="   "), PRINCIPAL, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert receipt["reasons"]
    assert not node.blocks
    # refusal is inspectable in the ingestion log — never silent
    assert node.ingestion_log[-1]["outcome"] == "REFUSED"


def test_ingest_without_identity_binding_fails_closed():
    """Acceptance 3/4: unauthenticated caller cannot ingest."""
    node = KnowNode()
    cand = make_candidate()
    del cand["identity_binding"]
    receipt = node.ingest(cand, PRINCIPAL, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert any("identity" in r for r in receipt["reasons"])
    assert not node.blocks


def test_ingest_missing_principal_identity_fails_closed():
    node = KnowNode()
    receipt = node.ingest(make_candidate(), {"entitled_scopes": ["public"]}, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert not node.blocks


# ------------------------------------------------------------------
# §7 refusal conditions
# ------------------------------------------------------------------

def test_unprovenanced_ingestion_refused():
    """§7.1 — 'store it for now, provenance later' is not an ingestion mode."""
    node = KnowNode()
    cand = make_candidate()
    del cand["provenance"]
    receipt = node.ingest(cand, PRINCIPAL, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert any("7.1" in r for r in receipt["reasons"])


def test_core_auto_assignment_refused_and_alerted():
    """§7.2 — CORE auto-assignment is a security event, not a validation error."""
    node = KnowNode()
    receipt = node.ingest(make_candidate(proposed_class="CORE"), PRINCIPAL, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert node.security_events
    assert node.security_events[-1]["kind"] == "CORE_AUTO_ASSIGNMENT_ATTEMPT"
    assert not node.blocks


def test_core_proposal_without_director_receipt_held_pending():
    """§8 — a CORE proposal waits in CLASSIFICATION_PENDING; not served."""
    node = KnowNode()
    receipt = node.ingest(make_candidate(proposed_class="CORE", classifier="director"),
                          PRINCIPAL, now=NOW)
    assert receipt["operation"] == "CLASSIFY"
    assert receipt["afterState"] == "CLASSIFICATION_PENDING"
    block = node.blocks[receipt["blockId"]]
    assert block["state"] == "CLASSIFICATION_PENDING"
    result = node.retrieve(make_query(), PRINCIPAL, now=NOW)
    assert result["blocks"] == []
    assert any("lifecycle" in e["gate"] for e in result["exclusions"])


def test_core_with_valid_director_receipt_ingests():
    node = KnowNode()
    content = "Constitutional summary v1"
    # the director receipt must name the block's content hash
    from naya_kernel.nodes.know_node import _sha256, _canonicalize_text
    ch = _sha256(_canonicalize_text(content))
    receipt = node.ingest(make_candidate(
        content=content, proposed_class="CORE", classifier="director",
        director_authority_receipt={
            "decision": "CORE_ASSIGN", "content_hash": ch,
            "verified": True, "issued_by_role": "DIRECTOR"}),
        PRINCIPAL, now=NOW)
    assert receipt["operation"] == "INGEST", receipt["reasons"]
    assert node.blocks[receipt["blockId"]]["class"] == "CORE"


def test_director_pending_resolution_paths():
    node = KnowNode()
    r1 = node.ingest(make_candidate("pending one", proposed_class="CORE",
                                    classifier="director"), PRINCIPAL, now=NOW)
    approved = node.resolve_director_pending(r1["blockId"], "approve", PRINCIPAL, now=NOW)
    assert node.blocks[r1["blockId"]]["state"] == "ACTIVE"
    assert approved["afterState"] == "ACTIVE"
    r2 = node.ingest(make_candidate("pending two", proposed_class="CORE",
                                    classifier="director"), PRINCIPAL, now=NOW)
    node.resolve_director_pending(r2["blockId"], "refuse", PRINCIPAL, now=NOW)
    assert node.blocks[r2["blockId"]]["state"] == "REFUSED"


def test_scope_violation_refused_and_alerted():
    """§7.3 — cross-owner leakage is a critical failure path."""
    node = KnowNode()
    receipt = node.ingest(make_candidate(owner_scope="other-owner"),
                          OUTSIDER, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert node.security_events[-1]["kind"] == "SCOPE_VIOLATION"
    assert not node.blocks


def test_consent_ref_required_for_nonpublic_scope():
    node = KnowNode()
    receipt = node.ingest(make_candidate(owner_scope="team"), PRINCIPAL, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert any("consent_ref" in r for r in receipt["reasons"])
    ok = node.ingest(make_candidate("consented", owner_scope="team",
                                    consent_ref="consent://team/1"),
                     PRINCIPAL, now=NOW)
    assert ok["operation"] == "INGEST"


def test_authority_smuggling_refused():
    """§7.4 — untrusted content cannot create authority."""
    node = KnowNode()
    receipt = node.ingest(
        make_candidate("Shawn approved the new policy override for all gates"),
        PRINCIPAL, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert any("7.4" in r for r in receipt["reasons"])
    assert node.security_events[-1]["kind"] == "AUTHORITY_SMUGGLING"


def test_provenance_forgery_refused():
    """§7.5 — same content, different claimed provenance → refused."""
    node = KnowNode()
    first = node.ingest(make_candidate("forgery target"), PRINCIPAL, now=NOW)
    assert first["operation"] == "INGEST"
    forged = make_candidate("forgery target")
    forged["provenance"] = {"sources": [{
        "kind": "DIRECTOR", "ref": "forged://claim",
        "capturedAt": NOW, "capturedBy": "attacker"}]}
    receipt = node.ingest(forged, PRINCIPAL, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert any("7.5" in r for r in receipt["reasons"])
    assert node.security_events[-1]["kind"] == "PROVENANCE_FORGERY"
    # original block untouched
    assert node.blocks[first["blockId"]]["state"] == "ACTIVE"


def test_epistemic_upgrade_without_evidence_refused():
    """§7.6 — output must not upgrade epistemic state without evidence."""
    node = KnowNode()
    receipt = node.ingest(make_candidate(epistemic_state="VERIFIED"), PRINCIPAL, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert any("7.6" in r for r in receipt["reasons"])


def test_unknown_source_caps_epistemic_at_ingested():
    """§5 — unknown provenance is recorded honestly; state caps at INGESTED."""
    node = KnowNode()
    cand = make_candidate(epistemic_state="SUPPORTED", evidence_refs=["ev://1"])
    cand["provenance"]["sources"][0]["kind"] = "UNKNOWN"
    receipt = node.ingest(cand, PRINCIPAL, now=NOW)
    assert receipt["operation"] == "INGEST"
    assert node.blocks[receipt["blockId"]]["epistemicState"] == "INGESTED"
    assert any("capped at INGESTED" in r for r in receipt["reasons"])


def test_unexplained_classification_refused():
    node = KnowNode()
    cand = make_candidate()
    cand["class_signals"] = []
    receipt = node.ingest(cand, PRINCIPAL, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert any("Unexplained" in r or "unexplained" in r for r in receipt["reasons"])


# ------------------------------------------------------------------
# §3.3 dedupe — acceptance 8
# ------------------------------------------------------------------

def test_duplicate_ingestion_safe_and_idempotent():
    node = KnowNode()
    first = node.ingest(make_candidate("dedupe me"), PRINCIPAL, now=NOW)
    second = node.ingest(make_candidate("dedupe me"), PRINCIPAL, now=NOW)
    assert first["blockId"] == second["blockId"]
    assert len(node.blocks) == 1
    assert any("dedupe" in r for r in second["reasons"])


def test_gate_reingestion_is_idempotent():
    """gate() on the same candidate twice → PASS both times, one block."""
    node = KnowNode()
    state = {"candidate": make_candidate("gate idem"), "principal": PRINCIPAL, "now": NOW}
    r1 = node.gate(state)
    r2 = node.gate(state)
    assert r1.verdict == GateVerdict.PASS
    assert r2.verdict == GateVerdict.PASS
    assert len(node.blocks) == 1


# ------------------------------------------------------------------
# §11 receipts — acceptance 9: hashable, independently re-derivable
# ------------------------------------------------------------------

def test_receipt_recomputes_to_match():
    node = KnowNode()
    receipt = node.ingest(make_candidate("receipt proof"), PRINCIPAL, now=NOW)
    assert node.recompute(receipt) == "MATCH"


def test_recompute_detects_tamper():
    node = KnowNode()
    receipt = node.ingest(make_candidate("tamper target"), PRINCIPAL, now=NOW)
    receipt["afterState"] = "VERIFIED"
    assert node.recompute(receipt) == "MISMATCH"


def test_refuse_receipt_recomputes_to_match():
    node = KnowNode()
    receipt = node.ingest(make_candidate(content=""), PRINCIPAL, now=NOW)
    assert receipt["operation"] == "REFUSE"
    assert node.recompute(receipt) == "MATCH"


# ------------------------------------------------------------------
# §6 serving — selector gates, conflicts, empty sets
# ------------------------------------------------------------------

def test_query_without_binding_fails_closed():
    """§1.1 — a query without authenticated identity/scope binding fails closed."""
    node = KnowNode()
    result = node.retrieve({"modes": ["structural"]}, PRINCIPAL, now=NOW)
    assert result["admitted"] is False
    assert result["blocks"] == []


def test_retrieval_never_pads_empty_set():
    """§1.2/§6 — empty is an answer; never a padded set."""
    node = KnowNode()
    result = node.retrieve(make_query(), PRINCIPAL, now=NOW)
    assert result["admitted"] is True
    assert result["blocks"] == []
    assert result["receipt"]["operation"] == "SERVE"
    assert any("no padding" in r for r in result["receipt"]["reasons"])
    assert result["receipt"]["receipt_hash"]


def test_cross_scope_retrieval_refused_with_reasons():
    """§7.3 — a query gets the intersection it is entitled to; exclusions recorded."""
    node = KnowNode()
    node.ingest(make_candidate("team secret", owner_scope="team",
                               consent_ref="consent://team/9"), PRINCIPAL, now=NOW)
    node.ingest(make_candidate("public note"), PRINCIPAL, now=NOW)
    result = node.retrieve(make_query(requested_scopes=["public", "team"]),
                           OUTSIDER, now=NOW)
    ids = [b["id"] for b in result["blocks"]]
    assert len(ids) == 1
    assert any(e["gate"] == "consent" for e in result["exclusions"])
    assert any("EXCLUDE" in d and "consent" in d for d in result["selector_decisions"])


def test_stale_blocks_excluded_not_silently_ranked_down():
    """§6/master invariant 3 — never silently prefer stale data."""
    node = KnowNode()
    node.ingest(make_candidate("fresh item"), PRINCIPAL, now=NOW)
    node.ingest(make_candidate("stale item", valid_until="2026-01-01T00:00:00+00:00"),
                PRINCIPAL, now=NOW)
    result = node.retrieve(make_query(), PRINCIPAL, now=NOW)
    contents = [b["content"] for b in result["blocks"]]
    assert "fresh item" in contents
    assert "stale item" not in contents
    assert any(e["gate"] == "temporal" for e in result["exclusions"])


def test_contradictions_served_not_hidden():
    """§6 — conflicts are served with CONTRADICTS linkage visible."""
    node = KnowNode()
    a = node.ingest(make_candidate("the sky is blue"), PRINCIPAL, now=NOW)
    b = node.ingest(make_candidate("the sky is green"), PRINCIPAL, now=NOW)
    node.contradict(a["blockId"], b["blockId"], PRINCIPAL, now=NOW)
    result = node.retrieve(make_query(), PRINCIPAL, now=NOW)
    by_id = {blk["id"]: blk for blk in result["blocks"]}
    assert a["blockId"] in by_id and b["blockId"] in by_id
    assert b["blockId"] in by_id[a["blockId"]]["contradicts"]
    assert by_id[a["blockId"]]["epistemicState"] == "CONTRADICTED"
    # truth-state deltas recorded for downstream (§1.2)
    assert any(d["block_id"] == a["blockId"] and d["after"] == "CONTRADICTED"
               for d in node.truth_deltas)


def test_similarity_score_is_metadata_not_evidence():
    """§1.3/master invariant 1 — similarity never counts as evidence."""
    node = KnowNode()
    node.ingest(make_candidate("the quick brown fox jumps"), PRINCIPAL, now=NOW)
    result = node.retrieve(make_query(modes=["semantic"], text="quick fox"),
                           PRINCIPAL, now=NOW)
    assert result["blocks"]
    meta = result["blocks"][0]["retrieval_metadata"]
    assert "similarity_score" in meta
    assert meta["similarity_is_evidence"] is False


def test_ranking_is_deterministic_and_recorded():
    node = KnowNode()
    node.ingest(make_candidate("zebra fact", epistemic_state="INGESTED",
                               evidence_refs=["ev://1"]), PRINCIPAL, now=NOW)
    node.ingest(make_candidate("alpha fact", epistemic_state="SUPPORTED",
                               evidence_refs=["ev://2"]), PRINCIPAL, now=NOW)
    r1 = node.retrieve(make_query(), PRINCIPAL, now=NOW)
    r2 = node.retrieve(make_query(), PRINCIPAL, now=NOW)
    assert [b["id"] for b in r1["blocks"]] == [b["id"] for b in r2["blocks"]]
    assert r1["rank_inputs"]  # ranking inputs recorded as evidence


def test_cite_provenance_first_class():
    """§5 — any served block produces its full chain on demand."""
    node = KnowNode()
    receipt = node.ingest(make_candidate("provenance demo"), PRINCIPAL, now=NOW)
    chain = node.cite_provenance(receipt["blockId"])
    assert chain["sources"]
    assert chain["boundBy"] == "node_id=NAYA-KERNEL-KNOW"
    with pytest.raises(KeyError):
        node.cite_provenance("kb-nonexistent")


# ------------------------------------------------------------------
# §8 lifecycle — supersession, invalidation, expiry
# ------------------------------------------------------------------

def test_supersession_keeps_old_traceable():
    """Acceptance 7 — stale/superseded is explicit; old record traceable."""
    node = KnowNode()
    old = node.ingest(make_candidate("version one"), PRINCIPAL, now=NOW)
    new = node.ingest(make_candidate("version two", supersedes=old["blockId"]),
                      PRINCIPAL, now=NOW)
    assert new["operation"] == "INGEST"
    assert node.blocks[old["blockId"]]["state"] == "SUPERSEDED"
    assert node.blocks[old["blockId"]]["supersededBy"] == new["blockId"]
    result = node.retrieve(make_query(), PRINCIPAL, now=NOW)
    ids = [b["id"] for b in result["blocks"]]
    assert new["blockId"] in ids
    assert old["blockId"] not in ids
    assert any(d["after"] == "SUPERSEDED" for d in node.truth_deltas)


def test_invalidation_is_itself_a_block():
    node = KnowNode()
    receipt = node.ingest(make_candidate("disproven claim", epistemic_state="SUPPORTED",
                                         evidence_refs=["ev://x"]), PRINCIPAL, now=NOW)
    inv = node.invalidate(receipt["blockId"], "counter-evidence ev://y", PRINCIPAL, now=NOW)
    assert node.blocks[receipt["blockId"]]["state"] == "INVALIDATED"
    inv_block = node.blocks.get(inv["invalidation_block"])
    assert inv_block is not None and inv_block["state"] == "ACTIVE"


def test_expire_sweep_labels_expired_with_tombstone():
    node = KnowNode()
    short = make_candidate("short-lived", ttl_seconds=1)
    receipt = node.ingest(short, PRINCIPAL, now="2026-01-01T00:00:00+00:00")
    swept = node.expire_sweep(now="2026-06-01T00:00:00+00:00")
    assert receipt["blockId"] in swept["expired"]
    assert node.blocks[receipt["blockId"]]["state"] == "EXPIRED"
    result = node.retrieve(make_query(), PRINCIPAL, now="2026-06-01T00:00:00+00:00")
    assert receipt["blockId"] not in [b["id"] for b in result["blocks"]]


def test_illegal_transition_fails_closed():
    node = KnowNode()
    receipt = node.ingest(make_candidate("no skip"), PRINCIPAL, now=NOW)
    block = node.blocks[receipt["blockId"]]
    with pytest.raises(ValueError):
        node._transition(block, "CANDIDATE", "time travel", NOW)


# ------------------------------------------------------------------
# §4.1 promotion, demotion, reclassification review
# ------------------------------------------------------------------

def test_promotion_requires_target_class_gate():
    node = KnowNode()
    receipt = node.ingest(make_candidate("promotable", epistemic_state="INGESTED",
                                         evidence_refs=["ev://s"]),
                          PRINCIPAL, now=NOW)
    bid = receipt["blockId"]
    # EPHEMERAL→CONTEXT needs supporting evidence; use an EPHEMERAL block
    eph = node.ingest(make_candidate("ephemeral note", proposed_class="EPHEMERAL"),
                      PRINCIPAL, now=NOW)
    with pytest.raises(ValueError):
        node.promote(eph["blockId"], "CONTEXT", {}, PRINCIPAL, now=NOW)
    ok = node.promote(eph["blockId"], "CONTEXT",
                      {"supporting": True, "refs": ["ev://s"]}, PRINCIPAL, now=NOW)
    assert ok["afterState"] == "CONTEXT"
    assert node.blocks[eph["blockId"]]["class"] == "CONTEXT"
    # CONTEXT→REUSABLE needs verification
    with pytest.raises(ValueError):
        node.promote(eph["blockId"], "REUSABLE", {"supporting": True}, PRINCIPAL, now=NOW)
    ok2 = node.promote(eph["blockId"], "REUSABLE",
                       {"kind": "verification", "refs": ["ev://v"]}, PRINCIPAL, now=NOW)
    assert node.blocks[eph["blockId"]]["class"] == "REUSABLE"
    # CORE never reachable by promotion
    with pytest.raises(ValueError):
        node.promote(eph["blockId"], "CORE", {"kind": "verification"}, PRINCIPAL, now=NOW)


def test_reclassification_review_holds_block():
    """§4.1 — misclassified block held; not served in the meantime."""
    node = KnowNode()
    receipt = node.ingest(make_candidate("suspect reusable", proposed_class="REUSABLE",
                                         epistemic_state="SUPPORTED",
                                         evidence_refs=["ev://w"]),
                          PRINCIPAL, now=NOW)
    bid = receipt["blockId"]
    node.request_reclassification(bid, "PROVE found it unsupported", PRINCIPAL, now=NOW)
    assert node.blocks[bid]["state"] == "CLASSIFICATION_REVIEW"
    result = node.retrieve(make_query(), PRINCIPAL, now=NOW)
    assert bid not in [b["id"] for b in result["blocks"]]
    resolved = node.resolve_reclassification(
        bid, "CONTEXT", [{"signal": "prove-review", "value": 0.6}], PRINCIPAL, now=NOW)
    assert node.blocks[bid]["state"] == "ACTIVE"
    assert node.blocks[bid]["class"] == "CONTEXT"


# ------------------------------------------------------------------
# §5 provenance audit — acceptance 6
# ------------------------------------------------------------------

def test_provenance_audit_catches_broken_chain():
    node = KnowNode()
    receipt = node.ingest(make_candidate("audit target"), PRINCIPAL, now=NOW)
    bid = receipt["blockId"]
    # simulate provenance loss
    node.blocks[bid]["provenance"]["sources"] = []
    report = node.provenance_audit(now=NOW)
    assert bid in [w["block_id"] for w in report["withheld"]]
    assert node.blocks[bid]["state"] == "PROVENANCE_REVIEW"
    result = node.retrieve(make_query(), PRINCIPAL, now=NOW)
    assert bid not in [b["id"] for b in result["blocks"]]
    # repair returns it to serving
    node.repair_provenance(bid, {"sources": [{
        "kind": "EXTERNAL", "ref": "ext://repaired",
        "capturedAt": NOW, "capturedBy": "naya-test"}]}, PRINCIPAL, now=NOW)
    assert node.blocks[bid]["state"] == "ACTIVE"


# ------------------------------------------------------------------
# §3.2 transforms additive — §3.4 backpressure — §7.7 quarantine
# ------------------------------------------------------------------

def test_transform_creates_new_block_source_untouched():
    """'Life with Naya' rule: distillation never replaces the book."""
    node = KnowNode()
    book = node.ingest(make_candidate("the whole book of wisdom",
                                      proposed_class="REFERENCE"),
                       PRINCIPAL, now=NOW)
    distill = node.derive_transform(
        [book["blockId"]], "DISTILLATION", "one minute of wisdom",
        make_candidate("one minute of wisdom"), PRINCIPAL, now=NOW)
    assert distill["operation"] == "INGEST"
    new_block = node.blocks[distill["blockId"]]
    kinds = [t["kind"] for t in new_block["provenance"]["transforms"]]
    assert "DISTILLATION" in kinds
    assert book["blockId"] in new_block["provenance"]["transforms"][0]["from"]
    assert node.blocks[book["blockId"]]["state"] == "ACTIVE"


def test_intake_backpressure_defers_never_drops():
    """§3.4 — full queue → DEFERRED, never silently dropped."""
    node = KnowNode()
    for _ in range(1000):
        node.intake(make_candidate("queued"))
    deferred = node.intake(make_candidate("one too many"))
    assert deferred["status"] == "DEFERRED"
    assert len(node.intake_queue) == 1000
    receipts = node.drain_intake(PRINCIPAL, now=NOW)
    # all 1000 are duplicates of one content hash → 1 block, 1000 receipts
    assert len(receipts) == 1000
    assert len(node.blocks) == 1


def test_quarantine_batch_refuses_all_and_records_event():
    """§7.7 — poisoning attempt: batch quarantined, attempt persisted."""
    node = KnowNode()
    receipt = node.quarantine_batch(
        [make_candidate("poison %d" % i) for i in range(5)],
        PRINCIPAL, ["bulk anomaly", "source-behavior shift"], now=NOW)
    assert receipt["operation"] == "QUARANTINE"
    assert not node.blocks
    assert node.security_events[-1]["kind"] == "INGESTION_QUARANTINE"
    assert node.ingestion_log[-1]["outcome"] == "QUARANTINED"


# ------------------------------------------------------------------
# §10 cold reconstruction — acceptance 13
# ------------------------------------------------------------------

def test_cold_successor_restores_identical_store():
    node = KnowNode()
    r1 = node.ingest(make_candidate("cold one"), PRINCIPAL, now=NOW)
    r2 = node.ingest(make_candidate("cold two"), PRINCIPAL, now=NOW)
    r3 = node.ingest(make_candidate("cold three", supersedes=r1["blockId"]),
                     PRINCIPAL, now=NOW)
    node.contradict(r2["blockId"], r3["blockId"], PRINCIPAL, now=NOW)
    node.checkpoint(now=NOW)
    report = KnowNode().cold_reconstruct(node.receipts)
    assert report["restored_block_count"] == 3
    assert report["store_hash"] == node._store_hash()
    assert report["replayed_receipts"] == len(node.receipts) - 1  # checkpoint not replayed
    assert report["restore_receipt"]["receipt_hash"]


def test_cold_reconstruct_defective_receipt_fails_loudly():
    node = KnowNode()
    receipt = node.ingest(make_candidate("defective"), PRINCIPAL, now=NOW)
    del receipt["block_snapshot"]
    with pytest.raises(ValueError):
        KnowNode().cold_reconstruct([receipt])


# ------------------------------------------------------------------
# gate() dispatch
# ------------------------------------------------------------------

def test_gate_ingest_pass_and_refuse():
    node = KnowNode()
    passed = node.gate({"candidate": make_candidate("gate pass"),
                        "principal": PRINCIPAL, "now": NOW})
    assert passed.verdict == GateVerdict.PASS
    failed = node.gate({"candidate": make_candidate(content=""),
                        "principal": PRINCIPAL, "now": NOW})
    assert failed.verdict == GateVerdict.FAIL
    assert failed.reasons


def test_gate_pending_needs_evidence():
    node = KnowNode()
    result = node.gate({"candidate": make_candidate("core ask", proposed_class="CORE",
                                                    classifier="director"),
                        "principal": PRINCIPAL, "now": NOW})
    assert result.verdict == GateVerdict.NEED_EVIDENCE


def test_gate_query_admission():
    node = KnowNode()
    ok = node.gate({"query": make_query(), "principal": PRINCIPAL})
    assert ok.verdict == GateVerdict.PASS
    bad = node.gate({"query": {"modes": ["structural"]}, "principal": PRINCIPAL})
    assert bad.verdict == GateVerdict.FAIL


def test_gate_unknown_input_fails():
    node = KnowNode()
    result = node.gate({"principal": PRINCIPAL})
    assert result.verdict == GateVerdict.FAIL
