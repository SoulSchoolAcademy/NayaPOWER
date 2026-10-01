"""NAYA-KERNEL-KNOW — CANDIDATE implementation (NOT RATIFIED — NOT MERGED).

Implements the KNOW node contract from KNOW-NODE-SPEC-CANDIDATE.md (draft)
against the NodeBase interface. Candidate code on a feature branch: it proves
the spec is implementable; it grants nothing, merges nothing, deploys nothing.

Contractual responsibility (spec §0, reconciled to the Ultimate Lock
BRAIN/03-KERNEL/0005-NINE-NODE-ULTIMATE-LOCK-AND-NOTE-READINESS-V1.md):
KNOW is the memory organ — it decides what durable information exists and
what is current: canonical intelligence-object identity, meaning,
lifecycle, provenance, and durable intelligence. It proves every one of
those claims with provenance. KNOW is the only node permitted to persist
knowledge into the intelligent graph.
KNOW does NOT decide applicability (owned by CONNECT — the KNOW→CONNECT
edge is CONTEXTUALIZES; applicability metadata crosses as non-steering
context) and does NOT assess epistemic claims or evidence (owned by PROVE —
KNOW records PROVE's assessed state by receipt reference, never by judging
evidence itself). KNOW is never the final truth authority.

Gate input contract (`state` dict keys; all reads are explicit):
  candidate           ingestion candidate (see INGEST_CANDIDATE contract below)
  query               retrieval request (see RETRIEVAL_QUERY contract below)
  principal           {"identity": str, "entitled_scopes": [str]} —
                      the authenticated principal KNOW acts for
  now                 ISO-8601 timestamp override (tests / determinism)

KNOW does NOT grant, infer, or modify authority — ever (§1.3). Untrusted
content cannot create authority: §7.4 content is refused, not warned about.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import deque
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from naya_kernel.node_base import GateResult, GateVerdict, ManifestEntry, NodeBase

NODE_ID = "NAYA-KERNEL-KNOW"
NODE_VERSION = "0.1.0-candidate"
PIPELINE_POSITION = 4

# §4 — the five RATIFIED intelligence classes. KNOW implements them; it does
# not redefine, merge, or subdivide them.
CLASSES = ("CORE", "REUSABLE", "CONTEXT", "REFERENCE", "EPHEMERAL")

# §4 — the auto-classifier may never assign CORE. Its maximum autonomous
# assignment is REUSABLE. Any auto path attempting CORE is refused (§7.2).
AUTO_CLASSIFIABLE = ("REUSABLE", "CONTEXT", "REFERENCE", "EPHEMERAL")

# §2 — epistemic states a block may carry.
EPISTEMIC_STATES = (
    "INGESTED", "CLASSIFIED", "SUPPORTED", "LEARNED", "VERIFIED",
    "CONTRADICTED", "SUPERSEDED", "INVALIDATED", "EXPIRED",
)

# §8 — lifecycle states. SERVABLE states are served; everything else is
# withheld (explicit absence, never degraded presence — §9 doctrine).
SERVABLE_STATES = ("ACTIVE", "CONTRADICTED")
WITHHELD_STATES = (
    "REFUSED", "SUPERSEDED", "INVALIDATED", "EXPIRED",
    "PROVENANCE_REVIEW", "CLASSIFICATION_REVIEW", "CLASSIFICATION_PENDING",
)

# §4.1 — promotion ladder. EPHEMERAL → CONTEXT requires supporting evidence;
# CONTEXT → REUSABLE requires verification. CORE is never reachable by
# promotion (director ingestion path only).
CLASS_LADDER = {"EPHEMERAL": 0, "CONTEXT": 1, "REUSABLE": 2}

# §5 — provenance source kinds.
SOURCE_KINDS = (
    "DIRECT_OBSERVATION", "ACTION_OUTCOME", "LEARNED", "EXTERNAL",
    "DIRECTOR", "DERIVED", "UNKNOWN",
)

TRANSFORM_KINDS = (
    "DISTILLATION", "SUMMARIZATION", "TRANSLATION", "EXTRACTION",
    "CANONICALIZATION", "MERGE", "SPLIT",
)

# §6 — retrieval modes (master §3).
RETRIEVAL_MODES = ("semantic", "structural", "relational", "contextual")

# §3.4 — bounded intake queue with backpressure: full → DEFERRED, never
# silently dropped.
INTAKE_QUEUE_MAX = 1000

# §13.4 candidate defaults: session-derived 24h, unverified external 7d.
EPHEMERAL_TTL_SESSION_SECONDS = 24 * 3600
EPHEMERAL_TTL_EXTERNAL_SECONDS = 7 * 24 * 3600

# Classifier policy this implementation runs under. Policy changes are
# governance proposals, never silent (§13.2) — the version is receipted.
CLASSIFICATION_POLICY_VERSION = "know-classifier-policy-0.1.0-candidate"

# §7.4 — authority-smuggling heuristics. Content matching these patterns
# implies a permission, authorization, or governance change and is REFUSED as
# ordinary knowledge. Candidate-grade heuristics; receipts record which
# pattern fired so a successor can audit the decision.
_SMUGGLING_PATTERNS = [
    re.compile(r"\b(shawn|director)\s+(approved|authori[sz]ed|granted)\b", re.I),
    re.compile(r"\bpolic(y|ies)\s+(now\s+)?(allow|permit|require)s?\b", re.I),
    re.compile(r"\bpermission\s+granted\b", re.I),
    re.compile(r"\bgranted\s+(new\s+)?authority\b", re.I),
    re.compile(r"\byou\s+are\s+now\s+authori[sz]ed\b", re.I),
    re.compile(r"\boverride\s+(the\s+)?(law|gate|policy|constitution)\b", re.I),
    re.compile(r"\bthe\s+law\s+now\s+(says|allows|permits)\b", re.I),
    re.compile(r"\bratified\s+change\s+to\b", re.I),
]

# Deterministic epistemic ranking for the serving path (§6). Higher is
# better; CONTRADICTED is served but penalized so conflicts are visible
# without dominating the set.
_EPISTEMIC_RANK = {
    "VERIFIED": 90, "SUPPORTED": 80, "LEARNED": 70, "CLASSIFIED": 50,
    "INGESTED": 40, "CONTRADICTED": 30, "SUPERSEDED": 10,
    "INVALIDATED": 0, "EXPIRED": 0,
}


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj).encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _deepcopy_json(obj: Any) -> Any:
    return json.loads(_canonical(obj))


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _canonicalize_text(content: Any) -> str:
    """§3.2 canonicalization: normalize representation only.

    Transforms (distillation, summarization, translation, extraction) are NOT
    canonicalization — they create new blocks via derive_transform().
    """
    if isinstance(content, bytes):
        text = content.decode("utf-8", errors="replace")
    else:
        text = str(content)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    return text.strip()


def _tokens(text: str) -> List[str]:
    return sorted(set(re.findall(r"[a-z0-9]{3,}", text.lower())))


def _valid_prove_ref(ref: Any) -> bool:
    """A PROVE assessment citation is well-formed: it names PROVE's node id
    and a non-empty receipt id. KNOW binds the reference as provenance; it
    does not assess the evidence behind it (Ultimate Lock: epistemic
    claim/evidence assessment belongs to PROVE, never to KNOW)."""
    return (isinstance(ref, dict)
            and ref.get("node_id") == "NAYA-KERNEL-PROVE"
            and isinstance(ref.get("receipt_id"), str)
            and bool(ref.get("receipt_id")))


def _applicability_note(applicability: Any, query_context: Any) -> Dict[str, Any]:
    """Non-steering applicability annotation for CONNECT.

    Ultimate Lock (KNOW vs PROVE vs CONNECT): CONNECT owns task/context
    applicability decisions. KNOW records the declared applicability and
    reports the match honestly, but the annotation is non-steering —
    KNOW never excludes or includes on applicability grounds."""
    declared = applicability or {}
    contexts = declared.get("contexts")
    within = (not contexts) or (not query_context) or (query_context in contexts)
    return {
        "declared": _deepcopy_json(declared),
        "query_context": query_context,
        "within_declared": within,
        "steering_decision": False,
        "decided_by": "NAYA-KERNEL-CONNECT",
    }


class KnowNode(NodeBase):
    """NAYA-KERNEL-KNOW. The memory organ: gated ingestion, provenanced
    storage, selector-gated retrieval. Candidate implementation."""

    def __init__(self) -> None:
        # Durable state mirror: block_id -> KnowledgeBlock. In production
        # this is the intelligent-graph substrate; here it is the node's
        # testable durable state (same pattern as ActNode.ledger).
        self.blocks: Dict[str, Dict[str, Any]] = {}
        self._hash_index: Dict[str, str] = {}  # contentHash -> block_id
        # Every mutation is receipt-backed (MACHINE invariant 8); the
        # receipt log is the replay backbone for cold reconstruction.
        self.receipts: List[Dict[str, Any]] = []
        self.ingestion_log: List[Dict[str, Any]] = []
        self.intake_queue: deque = deque()
        # §1.2 canonical-state deltas: downstream consumers are owed the news
        # when a block's canonical state changes. KNOW records state; it is
        # not the truth authority (Ultimate Lock: KNOW vs PROVE vs CONNECT).
        self.state_deltas: List[Dict[str, Any]] = []
        # §7.2 / §7.3 / §7.7 security events.
        self.security_events: List[Dict[str, Any]] = []
        self.checkpoints: List[Dict[str, Any]] = []
        self._seq = 0

    # ------------------------------------------------------------------
    # NodeBase interface
    # ------------------------------------------------------------------
    def manifest_entry(self) -> ManifestEntry:
        """Return this node's manifest entry (candidate spec, §12 acceptance battery)."""
        return ManifestEntry(
            node_id=NODE_ID,
            version=NODE_VERSION,
            responsibilities=[
                "run the synchronous atomic ingestion gate per block "
                "(canonicalize → provenance_bind → classify → "
                "consent_check → persist → index)",
                "classify into the five ratified intelligence classes; "
                "never auto-assign CORE",
                "persist provenance-bound knowledge blocks with hash-bound "
                "KnowledgeReceipts",
                "serve retrieval sets through the V2 selector gates with "
                "epistemic state, provenance, conflicts, and explicit "
                "exclusions attached",
                "refuse unprovenanced, smuggled, forged, or "
                "evidence-upgraded content with receipted reasons",
                "reconstruct the full store from receipts alone for a "
                "cold successor (§10)",
            ],
        )

    def gate(self, state: Dict[str, Any]) -> GateResult:
        """Evaluate the KNOW gate on `state`.

        - `state["candidate"]` + `state["principal"]` → run the §3.1
          ingestion gate end-to-end (dedupe makes re-gating idempotent).
        - `state["query"]` + `state["principal"]` → retrieval admission:
          authenticated identity/scope binding required (§1.1).
        Anything else → FAIL (unknown gate input).
        """
        principal = state.get("principal") or {}
        now = state.get("now")
        if "candidate" in state:
            receipt = self.ingest(state["candidate"], principal, now=now)
            op = receipt.get("operation")
            reasons = list(receipt.get("reasons", []))
            if op == "INGEST":
                return GateResult(GateVerdict.PASS, reasons)
            if op == "CLASSIFY" and receipt.get("afterState") == "CLASSIFICATION_PENDING":
                return GateResult(GateVerdict.NEED_EVIDENCE, reasons)
            return GateResult(GateVerdict.FAIL, reasons)
        if "query" in state:
            verdict, reasons = self._admit_query(state["query"], principal)
            return GateResult(verdict=verdict, reasons=reasons)
        return GateResult(GateVerdict.FAIL, ["KNOW gate: neither candidate nor query supplied"])

    def persisted_transitions(self) -> List[str]:
        """Every state transition this node persists (spec §8 + §4.1)."""
        return [
            "CANDIDATE -> CLASSIFIED",
            "CLASSIFIED -> ACTIVE",
            "CANDIDATE -> REFUSED",
            "CANDIDATE -> CLASSIFICATION_PENDING",
            "CLASSIFICATION_PENDING -> ACTIVE",
            "CLASSIFICATION_PENDING -> REFUSED",
            "ACTIVE -> SUPERSEDED",
            "ACTIVE -> CONTRADICTED",
            "CONTRADICTED -> SUPERSEDED",
            "CONTRADICTED -> INVALIDATED",
            "ACTIVE -> INVALIDATED",
            "ACTIVE -> EXPIRED",
            "CONTRADICTED -> EXPIRED",
            "ACTIVE -> PROVENANCE_REVIEW",
            "PROVENANCE_REVIEW -> ACTIVE",
            "PROVENANCE_REVIEW -> INVALIDATED",
            "ACTIVE -> CLASSIFICATION_REVIEW",
            "CLASSIFICATION_REVIEW -> ACTIVE",
            "CLASSIFICATION_REVIEW -> REFUSED",
            "EPHEMERAL -> CONTEXT",
            "CONTEXT -> REUSABLE",
            "REUSABLE -> CONTRADICTED",
            "REUSABLE -> CONTEXT",
        ]

    def evidence_hooks(self) -> List[str]:
        """List the evidence hooks this node exposes (candidate spec, §12 acceptance battery)."""
        return [
            "provenance chains (cite_provenance; recomputed by provenance_audit)",
            "KnowledgeReceipt stream (hash-bound, independently re-derivable)",
            "ingestion log (refusals visible, never silent)",
            "V2 selector gate decisions per SERVE receipt",
            "classifier signals + policy version per CLASSIFY receipt",
            "security events (§7.2 CORE attempts, §7.3 scope breaches, §7.7 quarantine)",
            "checkpoints + RESTORE receipts (cold-reconstruction backbone)",
            "canonical-state deltas (downstream notification ledger)",
        ]

    def authority_checks(self) -> List[str]:
        """Declared — never granted. Every string here names a check; no
        string affirms granting authority (see test_authority_checks_grant_nothing).

        Spec §7.4 — authority-smuggling refusal (KNOW declares, never grants)."""
        return [
            "ingest requires authenticated identity binding; caller-supplied identity alone not trusted — no_authority_grant_performed",
            "CORE classification requires a director authority receipt naming the block — no_authority_grant_performed",
            "ownerScope write entitlement checked against the principal; cross-scope writes refused — no_authority_grant_performed",
            "consent_ref required for non-public owner scopes; consent recorded, never manufactured here",
            "retrieval admission requires authenticated identity/scope binding; cross-scope retrieval refused — no_authority_grant_performed",
            "§7.4 content implying a permission, authorization, or governance change is refused as knowledge; authority is declared by LAW, never by a block — no_authority_grant_performed",
            "epistemic upgrades require a PROVE assessment receipt reference; this node never assesses evidence or upgrades state on request — no_authority_grant_performed",
        ]

    # ------------------------------------------------------------------
    # §3.4 intake (async boundary with backpressure)
    # ------------------------------------------------------------------
    def intake(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Queue an ingestion candidate. Full → DEFERRED, never silently
        dropped (§3.4). The gate itself stays synchronous (ingest())."""
        if len(self.intake_queue) >= INTAKE_QUEUE_MAX:
            record = {
                "status": "DEFERRED",
                "reason": "intake queue full (%d); candidate NOT dropped, "
                          "retry intake later" % INTAKE_QUEUE_MAX,
                "at": _now_iso(),
            }
            self.ingestion_log.append(record)
            return record
        self.intake_queue.append(_deepcopy_json(candidate))
        return {"status": "QUEUED", "queue_depth": len(self.intake_queue)}

    def drain_intake(self, principal: Dict[str, Any], now: Optional[str] = None) -> List[Dict[str, Any]]:
        """Process queued candidates through the synchronous gate (§3.1)."""
        out = []
        while self.intake_queue:
            candidate = self.intake_queue.popleft()
            out.append(self.ingest(candidate, principal, now=now))
        return out

    # ------------------------------------------------------------------
    # §3.1 the synchronous atomic ingestion gate
    # ------------------------------------------------------------------
    def ingest(self, candidate: Dict[str, Any], principal: Dict[str, Any],
               now: Optional[str] = None) -> Dict[str, Any]:
        """Run the atomic ingestion gate on one candidate. Any step failing
        → the candidate is REFUSED with a receipt; nothing is half-stored.

        Spec §5 — ingestion: atomic gate (canonicalize→provenance_bind→classify→consent_check→persist→index)."""
        now = now or _now_iso()
        candidate = _deepcopy_json(candidate)
        principal = _deepcopy_json(principal)

        decision = self._adjudicate(candidate, principal, now)

        if decision["verdict"] == "INGEST":
            block = self._build_block(decision, candidate, principal, now)
            self._persist_block(block)
            receipt = self._receipt(
                "INGEST", block["id"], "CANDIDATE", block["state"],
                decision["reasons"], decision, candidate, principal, now,
                block_snapshot=_deepcopy_json(block),
            )
            if candidate.get("supersedes"):
                self._apply_supersession(candidate["supersedes"], block["id"],
                                         principal, now)
            self._record_ingestion("INGESTED", block["id"], decision, now)
            return receipt

        if decision["verdict"] == "DUPLICATE":
            existing = self.blocks[decision["existing_block_id"]]
            receipt = self._receipt(
                "INGEST", existing["id"], existing["state"], existing["state"],
                decision["reasons"], decision, candidate, principal, now,
                duplicate_of=existing["id"],
            )
            self._record_ingestion("DUPLICATE", existing["id"], decision, now)
            return receipt

        if decision["verdict"] == "PENDING":
            pending = self._build_block(decision, candidate, principal, now)
            pending["state"] = "CLASSIFICATION_PENDING"
            self._persist_block(pending)
            receipt = self._receipt(
                "CLASSIFY", pending["id"], "CANDIDATE", "CLASSIFICATION_PENDING",
                decision["reasons"], decision, candidate, principal, now,
                block_snapshot=_deepcopy_json(pending),
            )
            self._record_ingestion("PENDING", pending["id"], decision, now)
            return receipt

        # REFUSE
        receipt = self._receipt(
            "REFUSE", None, "CANDIDATE", "REFUSED",
            decision["reasons"], decision, candidate, principal, now,
        )
        self._record_ingestion("REFUSED", None, decision, now)
        if decision.get("security_alert"):
            self.security_events.append({
                "kind": decision["security_alert"],
                "at": now,
                "issuedBy": principal.get("identity"),
                "reasons": decision["reasons"],
                "content_hash": decision.get("content_hash"),
            })
        return receipt

    def _adjudicate(self, candidate: Dict[str, Any], principal: Dict[str, Any],
                    now: str) -> Dict[str, Any]:
        """Pure gate decision shared by ingest() and recompute(). No
        persistence; returns verdict + all gate outputs."""
        # --- identity binding (master §10): caller-supplied identity is not
        # trusted without authenticated binding.
        binding = candidate.get("identity_binding") or {}
        if binding.get("verified") is not True:
            return {"verdict": "REFUSE", "reasons": [
                "§1.1/master §10: ingestion requires authenticated identity "
                "binding; caller-supplied identity is not trusted"]}
        principal_identity = principal.get("identity")
        if not principal_identity:
            return {"verdict": "REFUSE", "reasons": [
                "§1.1: principal has no authenticated identity; fail closed"]}

        # --- canonicalize (§3.2)
        raw = candidate.get("content")
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            return {"verdict": "REFUSE", "reasons": [
                "§3.1 canonicalize: malformed input — empty content"]}
        canonical = _canonicalize_text(raw)
        if not canonical:
            return {"verdict": "REFUSE", "reasons": [
                "§3.1 canonicalize: content normalizes to empty"]}
        content_hash = _sha256(canonical)
        block_id = "kb-" + content_hash[:24]

        # --- provenance_bind (§5, §7.1, §7.5)
        provenance = candidate.get("provenance")
        if not provenance or not provenance.get("sources"):
            return {"verdict": "REFUSE", "reasons": [
                "§7.1: unprovenanced ingestion refused — no source, no chain, "
                "no receipt. 'Store it for now, provenance later' is not an "
                "ingestion mode"]}
        bad_sources = [s for s in provenance["sources"]
                       if s.get("kind") not in SOURCE_KINDS]
        if bad_sources:
            return {"verdict": "REFUSE", "reasons": [
                "§5: provenance source kind not recognized: %s" %
                sorted({s.get("kind") for s in bad_sources})]}
        unknown_source = any(
            s.get("kind") == "UNKNOWN" or not s.get("ref")
            for s in provenance["sources"])
        existing_id = self._hash_index.get(content_hash)
        if existing_id is not None:
            existing = self.blocks[existing_id]
            if self._provenance_differs(existing["provenance"], provenance):
                return {"verdict": "REFUSE", "security_alert": "PROVENANCE_FORGERY", "reasons": [
                    "§7.5: provenance forgery/conflict — known content "
                    "re-ingested with different claimed provenance; block %s "
                    "retained, candidate refused" % existing_id],
                    "content_hash": content_hash}
            return {"verdict": "DUPLICATE", "existing_block_id": existing_id,
                    "content_hash": content_hash, "reasons": [
                        "§3.3 dedupe: contentHash already persisted as %s; "
                        "not re-persisted" % existing_id]}

        # --- classify (§4): evidence-bound, CORE never auto-assigned
        proposed = candidate.get("proposed_class")
        if proposed not in CLASSES:
            return {"verdict": "REFUSE", "reasons": [
                "§4: proposed class %r not one of the five ratified classes" % (proposed,)]}
        signals = candidate.get("class_signals") or []
        if not signals:
            return {"verdict": "REFUSE", "reasons": [
                "§4.1: unexplained classification refused — the classifier "
                "must record why (signals, thresholds, policy version)"]}
        classifier = candidate.get("classifier", "auto")
        director_receipt = candidate.get("director_authority_receipt")
        if proposed == "CORE":
            if classifier == "auto":
                return {"verdict": "REFUSE", "security_alert": "CORE_AUTO_ASSIGNMENT_ATTEMPT", "reasons": [
                    "§7.2: auto-classifier attempted CORE assignment — "
                    "refused and alerted; this is a security event, not a "
                    "validation error"], "content_hash": content_hash}
            if not self._valid_director_receipt(director_receipt, content_hash):
                return {"verdict": "PENDING", "content_hash": content_hash,
                        "block_id": "kb-" + content_hash[:24],
                        "class": "CORE",
                        "epistemic_state": "INGESTED",
                        "classifier": classifier,
                        "owner_scope": candidate.get("owner_scope", "public"),
                        "reasons": [
                            "§8: CORE proposed without a director authority "
                            "receipt → CLASSIFICATION_PENDING; held until the "
                            "Director decides, not served in the meantime"],
                        "class_signals": signals}
        elif classifier == "auto" and proposed not in AUTO_CLASSIFIABLE:
            return {"verdict": "REFUSE", "reasons": [
                "§4: auto-classifier maximum autonomous assignment is "
                "REUSABLE; %r refused" % proposed]}

        # --- consent / scope (§7.3)
        owner_scope = candidate.get("owner_scope", "public")
        entitled = set(principal.get("entitled_scopes", []))
        if owner_scope not in entitled:
            return {"verdict": "REFUSE", "security_alert": "SCOPE_VIOLATION", "reasons": [
                "§7.3: block claims ownerScope %r the ingesting principal %r "
                "is not entitled to write — refused" % (owner_scope, principal_identity)],
                "content_hash": content_hash}
        if owner_scope != "public" and not candidate.get("consent_ref"):
            return {"verdict": "REFUSE", "reasons": [
                "§7.3: consent_ref required for non-public ownerScope %r" % owner_scope]}

        # --- authority smuggling (§7.4): untrusted content cannot create authority
        smuggled = [p.pattern for p in _SMUGGLING_PATTERNS if p.search(canonical)]
        if smuggled:
            return {"verdict": "REFUSE", "security_alert": "AUTHORITY_SMUGGLING", "reasons": [
                "§7.4: content implies a permission/authorization/governance "
                "change — refused as knowledge; routes to LAW/governance as a "
                "proposal, never into the store as fact. patterns: %s"
                % ", ".join(smuggled)], "content_hash": content_hash}

        # --- epistemic claims require a PROVE assessment (§7.6, reconciled to
        # the Ultimate Lock): epistemic claim/evidence assessment belongs to
        # PROVE. KNOW records PROVE's assessed state by receipt reference —
        # it never assesses evidence itself. evidence_refs are citations,
        # not assessments, and no longer suffice on their own.
        claimed = candidate.get("epistemic_state", "INGESTED")
        if claimed not in EPISTEMIC_STATES:
            return {"verdict": "REFUSE", "reasons": [
                "§2: epistemic state %r not recognized" % (claimed,)]}
        if claimed in ("SUPPORTED", "LEARNED", "VERIFIED") \
                and not _valid_prove_ref(candidate.get("prove_receipt_ref")):
            return {"verdict": "REFUSE", "reasons": [
                "§7.6 (Ultimate Lock): epistemic state %r requires a PROVE "
                "assessment receipt reference (prove_receipt_ref naming "
                "NAYA-KERNEL-PROVE); KNOW does not assess evidence" % claimed]}
        if unknown_source and claimed != "INGESTED":
            # §5 rule: unknown provenance caps at INGESTED — recorded, not silent.
            capped = True
        else:
            capped = False

        # --- supersession target must exist and be servable
        supersedes = candidate.get("supersedes")
        if supersedes and supersedes not in self.blocks:
            return {"verdict": "REFUSE", "reasons": [
                "supersession target %r not found; cannot supersede a "
                "nonexistent block" % (supersedes,)]}

        reasons = [
            "ingestion gate §3.1 passed: canonicalize → provenance_bind → "
            "classify → consent_check → persist → index",
            "class %r assigned by %r under policy %s" % (
                proposed, classifier, CLASSIFICATION_POLICY_VERSION),
        ]
        if capped:
            reasons.append("§5: source UNKNOWN — epistemic state capped at INGESTED")
        if unknown_source:
            reasons.append("provenance: source kind UNKNOWN recorded honestly")
        return {
            "verdict": "INGEST",
            "content_hash": content_hash,
            "block_id": block_id,
            "class": proposed,
            "epistemic_state": ("INGESTED" if capped else claimed),
            "class_signals": signals,
            "classifier": classifier,
            "owner_scope": owner_scope,
            "reasons": reasons,
        }

    # ------------------------------------------------------------------
    # block construction / persistence
    # ------------------------------------------------------------------
    def _build_block(self, decision: Dict[str, Any], candidate: Dict[str, Any],
                     principal: Dict[str, Any], now: str) -> Dict[str, Any]:
        """§2 — build the typed KnowledgeBlock from a passing adjudication."""
        provenance = _deepcopy_json(candidate["provenance"])
        provenance.setdefault("evidenceRefs", candidate.get("evidence_refs") or [])
        provenance.setdefault("upstreamReceipt", candidate.get("upstream_receipt"))
        # Ultimate Lock: PROVE's assessment is cited by reference. KNOW binds
        # the receipt as provenance without assessing the evidence behind it.
        if candidate.get("prove_receipt_ref"):
            provenance["proveReceiptRef"] = _deepcopy_json(
                candidate["prove_receipt_ref"])
        provenance["boundAt"] = now
        provenance["boundBy"] = "node_id=%s" % NODE_ID
        ttl = candidate.get("ttl_seconds")
        if ttl is None and decision["class"] == "EPHEMERAL":
            kinds = {s.get("kind") for s in provenance["sources"]}
            ttl = (EPHEMERAL_TTL_SESSION_SECONDS
                   if kinds <= {"DIRECT_OBSERVATION"} else EPHEMERAL_TTL_EXTERNAL_SECONDS)
        block = {
            "id": decision["block_id"],
            "content": _canonicalize_text(candidate["content"]),
            "contentHash": decision["content_hash"],
            "class": decision["class"],
            "epistemicState": decision["epistemic_state"],
            "provenance": provenance,
            "evidenceRefs": candidate.get("evidence_refs") or [],
            "ownerScope": decision["owner_scope"],
            "consentRef": candidate.get("consent_ref"),
            "applicability": candidate.get("applicability") or {},
            "validFrom": candidate.get("valid_from", now),
            "validUntil": candidate.get("valid_until"),
            "freshness": {"checkedAt": now, "ttl_seconds": ttl},
            "supersedes": candidate.get("supersedes"),
            "supersededBy": None,
            "contradicts": [],
            "retrievalModes": candidate.get("retrieval_modes") or list(RETRIEVAL_MODES),
            "issuedAt": now,
            "issuedBy": principal.get("identity"),
            "upstreamReceipt": candidate.get("upstream_receipt"),
            "state": "ACTIVE",
            "classSignals": decision["class_signals"],
            "classifierPolicy": CLASSIFICATION_POLICY_VERSION,
            "transitions": [
                {"from": "CANDIDATE", "to": "CLASSIFIED", "at": now,
                 "reason": "ingestion gate passed; class %r assigned" % decision["class"]},
                {"from": "CLASSIFIED", "to": "ACTIVE", "at": now,
                 "reason": "serving admission; block is current, scoped, supported"},
            ],
        }
        return block

    def _persist_block(self, block: Dict[str, Any]) -> None:
        """Persist a block + content-hash index entry. No partial writes:
        the caller only reaches here after the full gate passes (§3.1)."""
        self.blocks[block["id"]] = block
        self._hash_index[block["contentHash"]] = block["id"]

    @staticmethod
    def _provenance_differs(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
        """§7.5 — same content, different claimed provenance → forgery."""
        def key(p: Dict[str, Any]) -> str:
            srcs = sorted((s.get("kind"), s.get("ref")) for s in p.get("sources", []))
            trs = sorted((t.get("kind"), tuple(sorted(t.get("from", []))))
                         for t in p.get("transforms", []))
            return _canonical({"sources": srcs, "transforms": trs,
                               "upstreamReceipt": p.get("upstreamReceipt")})
        return key(a) != key(b)

    @staticmethod
    def _valid_director_receipt(receipt: Any, content_hash: str) -> bool:
        """CORE assignment needs a director authority receipt naming this
        block's content hash with a CORE_ASSIGN decision. The receipt is
        validated, never trusted by presence alone."""
        return (
            isinstance(receipt, dict)
            and receipt.get("decision") == "CORE_ASSIGN"
            and receipt.get("content_hash") == content_hash
            and receipt.get("verified") is True
            and receipt.get("issued_by_role") == "DIRECTOR"
        )

    def _record_ingestion(self, outcome: str, block_id: Optional[str],
                          decision: Dict[str, Any], now: str) -> None:
        self.ingestion_log.append({
            "outcome": outcome,
            "block_id": block_id,
            "at": now,
            "reasons": list(decision.get("reasons", [])),
            "content_hash": decision.get("content_hash"),
        })

    # ------------------------------------------------------------------
    # KnowledgeReceipt (§11) — hash-bound, independently re-derivable
    # ------------------------------------------------------------------
    def _receipt(self, operation: str, block_id: Optional[str],
                 before_state: Optional[str], after_state: str,
                 reasons: List[str], decision: Dict[str, Any],
                 candidate: Dict[str, Any], principal: Dict[str, Any],
                 now: str, **extra: Any) -> Dict[str, Any]:
        self._seq += 1
        body = {
            "node_id": NODE_ID,
            "node_version": NODE_VERSION,
            "operation": operation,
            "blockId": block_id,
            "beforeState": before_state,
            "afterState": after_state,
            "reasons": list(reasons),
            "evidenceRefs": _deepcopy_json(candidate.get("evidence_refs") or []),
            "provenance": _deepcopy_json(candidate.get("provenance")),
            "classSignals": _deepcopy_json(decision.get("class_signals") or []),
            "selectorDecisions": _deepcopy_json(extra.pop("selector_decisions", [])),
            "ownerScope": decision.get("owner_scope") or candidate.get("owner_scope", "public"),
            "issuedAt": now,
            "issuedBy": principal.get("identity"),
            "upstreamReceipt": candidate.get("upstream_receipt"),
            "classifierPolicy": CLASSIFICATION_POLICY_VERSION,
            "candidate_snapshot": _deepcopy_json(candidate),
            "seq": self._seq,
        }
        body.update(extra)
        body["receipt_hash"] = _sha256({k: v for k, v in body.items()
                                        if k != "receipt_hash"})
        self.receipts.append(body)
        return _deepcopy_json(body)

    def recompute(self, receipt: Dict[str, Any]) -> str:
        """§11 — independently re-derive a receipt. Returns MATCH/MISMATCH.

        Recomputes the receipt hash AND re-runs the gate decision on the
        receipt's candidate snapshot: same block, same policy, same
        evidence must produce the same verdict and class. If it cannot,
        the receipt is defective."""
        receipt = _deepcopy_json(receipt)
        claimed = receipt.pop("receipt_hash", None)
        if claimed != _sha256(receipt):
            return "MISMATCH"
        if receipt.get("node_id") != NODE_ID:
            return "MISMATCH"
        snapshot = receipt.get("candidate_snapshot") or {}
        principal = {"identity": receipt.get("issuedBy"),
                     "entitled_scopes": [receipt.get("ownerScope"), "public"]}
        # Re-run adjudication against a scratch node so replay is isolated.
        scratch = KnowNode()
        scratch.blocks = _deepcopy_json(self.blocks)
        scratch._hash_index = dict(self._hash_index)
        decision = scratch._adjudicate(snapshot, principal, receipt.get("issuedAt"))
        op = receipt.get("operation")
        if op == "INGEST":
            if decision["verdict"] == "DUPLICATE":
                existing = scratch.blocks.get(decision.get("existing_block_id", ""))
                ok = (existing is not None
                      and existing.get("class") == snapshot.get("proposed_class"))
            else:
                ok = (decision["verdict"] == "INGEST"
                      and decision.get("class") == snapshot.get("proposed_class"))
        elif op == "REFUSE":
            ok = decision["verdict"] == "REFUSE"
        elif op == "CLASSIFY":
            ok = decision["verdict"] == "PENDING"
        else:
            ok = True  # non-gate ops: hash integrity is the re-derivation
        return "MATCH" if ok else "MISMATCH"

    # ------------------------------------------------------------------
    # §3.2 transforms are additive lineage
    # ------------------------------------------------------------------
    def derive_transform(self, source_ids: List[str], transform_kind: str,
                         content: Any, candidate_fields: Dict[str, Any],
                         principal: Dict[str, Any],
                         now: Optional[str] = None) -> Dict[str, Any]:
        """A transform (distillation, summarization, ...) creates a NEW block
        whose provenance names the transform and points at the source
        block(s). The sources are never replaced (§3.2 'Life with Naya' rule)."""
        now = now or _now_iso()
        if transform_kind not in TRANSFORM_KINDS:
            raise ValueError("unknown transform kind %r" % (transform_kind,))
        missing = [sid for sid in source_ids if sid not in self.blocks]
        if missing:
            raise KeyError("transform sources not found: %s" % missing)
        candidate = _deepcopy_json(candidate_fields)
        candidate["content"] = content
        candidate["provenance"] = {
            "sources": [{"kind": "DERIVED",
                         "ref": sid,
                         "capturedAt": now,
                         "capturedBy": principal.get("identity")} for sid in source_ids],
            "transforms": [{
                "kind": transform_kind,
                "from": list(source_ids),
                "performedBy": principal.get("identity"),
                "performedAt": now,
                "receipt": candidate_fields.get("transform_receipt"),
            }],
        }
        return self.ingest(candidate, principal, now=now)

    # ------------------------------------------------------------------
    # §6 serving — retrieval through the V2 selector gates
    # ------------------------------------------------------------------
    def _admit_query(self, query: Dict[str, Any], principal: Dict[str, Any]):
        """§1.1 — a query without authenticated identity/scope binding fails
        closed; caller-supplied identity is not trusted without binding."""
        binding = (query.get("identity_binding") or {})
        reasons = []
        if binding.get("verified") is not True:
            return GateVerdict.FAIL, [
                "§1.1/master §10: query without authenticated identity/scope "
                "binding fails closed"]
        if not principal.get("identity"):
            return GateVerdict.FAIL, ["query: principal has no authenticated identity"]
        reasons.append("retrieval admission passed: authenticated identity/scope binding present")
        return GateVerdict.PASS, reasons

    def _freshness_ok(self, block: Dict[str, Any], now: str) -> bool:
        try:
            now_dt = _parse_iso(now)
        except Exception:
            return False
        if block.get("validUntil"):
            try:
                if _parse_iso(block["validUntil"]) < now_dt:
                    return False
            except Exception:
                return False
        ttl = (block.get("freshness") or {}).get("ttl_seconds")
        issued = block.get("issuedAt")
        if ttl and issued:
            try:
                from datetime import timedelta
                if _parse_iso(issued) + timedelta(seconds=ttl) < now_dt:
                    return False
            except Exception:
                return False
        return True

    def retrieve(self, query: Dict[str, Any], principal: Dict[str, Any],
                 now: Optional[str] = None) -> Dict[str, Any]:
        """Serve a typed retrieval set through the V2 selector gates.

        Never pads, never silences exclusions, never presents stored content
        as assessed truth — epistemic assessment belongs to PROVE, and
        applicability decisions belong to CONNECT (Ultimate Lock). Conflicts
        are served with CONTRADICTS linkage visible.
        Similarity scores are metadata, never evidence (§1.3, invariant 1).
        """
        now = now or _now_iso()
        query = _deepcopy_json(query)
        verdict, admit_reasons = self._admit_query(query, principal)
        if verdict != GateVerdict.PASS:
            return {"admitted": False, "blocks": [], "exclusions": [],
                    "reasons": admit_reasons, "receipt": None}
        entitled = set(principal.get("entitled_scopes", []))
        requested_scopes = set(query.get("requested_scopes") or ["public"])
        modes = [m for m in (query.get("modes") or list(RETRIEVAL_MODES))
                 if m in RETRIEVAL_MODES]
        text = query.get("text") or ""
        qtokens = set(_tokens(text))
        class_filter = set(query.get("class_filter") or [])
        query_context = query.get("context")

        served, exclusions, selector_decisions = [], [], []
        for block in self.blocks.values():
            bid = block["id"]
            # Gate 1 — lifecycle: only SERVABLE states reach the set.
            if block["state"] not in SERVABLE_STATES:
                exclusions.append({"block_id": bid, "gate": "lifecycle",
                                   "reason": "state %r not servable" % block["state"]})
                selector_decisions.append("EXCLUDE %s lifecycle:%s" % (bid, block["state"]))
                continue
            # Gate 2 — epistemic exclusions are redundant with lifecycle but
            # recorded explicitly per the V2 contract mapping.
            # Gate 3 — temporal validity: never silently prefer stale data.
            if not self._freshness_ok(block, now):
                exclusions.append({"block_id": bid, "gate": "temporal",
                                   "reason": "stale: validUntil/ttl exceeded"})
                selector_decisions.append("EXCLUDE %s temporal:stale" % bid)
                continue
            # Gate 4 — consent: per block per query; intersection only.
            if block["ownerScope"] not in entitled:
                exclusions.append({"block_id": bid, "gate": "consent",
                                   "reason": "ownerScope %r not in principal's entitled scopes"
                                   % block["ownerScope"]})
                selector_decisions.append("EXCLUDE %s consent:scope" % bid)
                continue
            if block["ownerScope"] not in requested_scopes:
                exclusions.append({"block_id": bid, "gate": "consent",
                                   "reason": "ownerScope %r not requested" % block["ownerScope"]})
                selector_decisions.append("EXCLUDE %s consent:not-requested" % bid)
                continue
            # KNOW does not decide applicability. Ultimate Lock
            # (KNOW vs PROVE vs CONNECT): CONNECT owns task/context
            # applicability decisions; the declared applicability rides along
            # as non-steering metadata for CONNECT to decide on.
            # (applicability exclusion removed — lock reconciliation)
            # Gate 6 — supersession: older versions excluded, newer named.
            if block.get("supersededBy"):
                exclusions.append({"block_id": bid, "gate": "supersession",
                                   "reason": "superseded by %s" % block["supersededBy"]})
                selector_decisions.append("EXCLUDE %s supersession:by-%s"
                                          % (bid, block["supersededBy"]))
                continue
            if class_filter and block["class"] not in class_filter:
                exclusions.append({"block_id": bid, "gate": "class_filter",
                                   "reason": "class %r filtered" % block["class"]})
                selector_decisions.append("EXCLUDE %s class_filter" % bid)
                continue
            selector_decisions.append("ADMIT %s" % bid)
            note = _applicability_note(block.get("applicability"), query_context)
            selector_decisions.append(
                "APPLICABILITY-NOTE %s %s (non-steering; CONNECT decides)"
                % (bid, "within-declared" if note["within_declared"]
                   else "outside-declared-noted"))
            served.append((block, note))

        # Deterministic ranking (§6): inputs recorded — ranking is evidence.
        rank_inputs = {
            "epistemic_rank_table": "VERIFIED90/SUPPORTED80/LEARNED70/CLASSIFIED50/"
                                   "INGESTED40/CONTRADICTED30",
            "tiebreak": "issuedAt desc, id asc",
            "query_tokens": sorted(qtokens) if "semantic" in modes else [],
        }
        def rank_key(pair):
            b = pair[0]
            sim = 0.0
            if qtokens and "semantic" in modes:
                btokens = set(_tokens(b["content"]))
                sim = (len(qtokens & btokens) / len(qtokens | btokens)) if (qtokens | btokens) else 0.0
            return (-_EPISTEMIC_RANK.get(b["epistemicState"], 0),
                    -sim, b["issuedAt"], b["id"])
        served.sort(key=rank_key)

        out_blocks = []
        for b, note in served:
            conflicts = [cid for cid in b.get("contradicts", [])
                         if cid in self.blocks]
            entry = {
                "id": b["id"],
                "content": b["content"],
                "class": b["class"],
                "epistemicState": b["epistemicState"],
                "state": b["state"],
                "ownerScope": b["ownerScope"],
                "applicability": b["applicability"],
                # Non-steering annotation for CONNECT (Ultimate Lock): KNOW
                # reports the declared applicability and whether the query
                # context falls within it; it never decides steering
                # eligibility — that decision belongs to CONNECT.
                "applicability_note": note,
                "freshness": b["freshness"],
                "contradicts": conflicts,
                "provenance_summary": {
                    "source_kinds": sorted({s.get("kind") for s in
                                            b["provenance"].get("sources", [])}),
                    "transforms": [t.get("kind") for t in
                                   b["provenance"].get("transforms", [])],
                },
                "retrieval_metadata": {},
            }
            if qtokens and "semantic" in modes:
                btokens = set(_tokens(b["content"]))
                sim = (len(qtokens & btokens) / len(qtokens | btokens)) if (qtokens | btokens) else 0.0
                # §1.3/master invariant 1: similarity is metadata, NOT evidence.
                entry["retrieval_metadata"]["similarity_score"] = round(sim, 4)
                entry["retrieval_metadata"]["similarity_is_evidence"] = False
            out_blocks.append(entry)

        receipt = self._receipt(
            "SERVE", None, None, "SERVED",
            (["retrieval set: %d served, %d excluded" % (len(out_blocks), len(exclusions))]
             + (["empty retrieval set — unknown stays unknown; no padding"] if not out_blocks else [])),
            {"reasons": []}, {"evidence_refs": []}, principal, now,
            selector_decisions=selector_decisions,
            query_digest=_sha256({k: v for k, v in query.items() if k != "identity_binding"}),
            rank_inputs=rank_inputs,
        )
        return {"admitted": True, "blocks": out_blocks, "exclusions": exclusions,
                "selector_decisions": selector_decisions,
                "rank_inputs": rank_inputs, "receipt": receipt}

    def cite_provenance(self, block_id: str) -> Dict[str, Any]:
        """§5 — first-class provenance citation. Any served block can produce
        its full chain on demand; a cold successor answers 'why do you
        believe this?' from the chain alone."""
        block = self.blocks.get(block_id)
        if block is None:
            raise KeyError("unknown block %r" % (block_id,))
        return _deepcopy_json(block["provenance"])

    # ------------------------------------------------------------------
    # §8 state machine — supersession, contradiction, invalidation
    # ------------------------------------------------------------------
    def _transition(self, block: Dict[str, Any], to_state: str, reason: str,
                    now: str) -> Dict[str, Any]:
        frm = block["state"]
        # Legal targets are the §8 lifecycle entries of persisted_transitions
        # (the CLASS ladder entries are class promotions, not lifecycle).
        legal_tos = [t.split(" -> ")[1] for t in self.persisted_transitions()
                     if t.split(" -> ")[0] == frm and " -> " in t
                     and t.split(" -> ")[1] not in CLASSES]
        if to_state not in legal_tos:
            raise ValueError("illegal KNOW transition %s -> %s; fail closed"
                             % (frm, to_state))
        block["state"] = to_state
        block["transitions"].append({"from": frm, "to": to_state, "at": now,
                                     "reason": reason})
        return {"from": frm, "to": to_state}

    def _apply_supersession(self, old_id: str, new_id: str,
                            principal: Dict[str, Any], now: str) -> None:
        """§8 — supersession is a transition with lineage, never an erasure.
        The superseded record remains traceable (MACHINE invariant 7)."""
        old = self.blocks.get(old_id)
        if old is None:
            return
        tr = self._transition(old, "SUPERSEDED",
                              "superseded by %s; lineage intact" % new_id, now)
        old["supersededBy"] = new_id
        old["epistemicState"] = "SUPERSEDED"
        self._state_delta(old_id, "ACTIVE", "SUPERSEDED",
                          "superseded by %s" % new_id, principal, now)
        self._receipt("SUPERSEDE", old_id, tr["from"], tr["to"],
                      ["supersession: %s -> %s; old record traceable" % (old_id, new_id)],
                      {"reasons": []}, {"evidence_refs": []}, principal, now,
                      superseded_by=new_id)

    def contradict(self, block_id: str, other_id: str, principal: Dict[str, Any],
                   evidence_refs: Optional[List[str]] = None,
                   now: Optional[str] = None) -> Dict[str, Any]:
        """§8/§9 — contradiction preserves BOTH sides. KNOW surfaces the
        conflict; reconciliation belongs to LEARN and the Director."""
        now = now or _now_iso()
        a = self.blocks.get(block_id)
        b = self.blocks.get(other_id)
        if a is None or b is None:
            raise KeyError("contradict: unknown block(s) %r %r" % (block_id, other_id))
        for blk in (a, b):
            if blk["state"] not in ("ACTIVE", "CONTRADICTED"):
                raise ValueError("contradict: block %s in state %r cannot be contradicted"
                                 % (blk["id"], blk["state"]))
        for blk, other in ((a, b), (b, a)):
            if other["id"] not in blk["contradicts"]:
                blk["contradicts"].append(other["id"])
            before = blk["state"]
            if before != "CONTRADICTED":
                self._transition(blk, "CONTRADICTED",
                                 "contradicted by %s; both preserved" % other["id"], now)
                blk["epistemicState"] = "CONTRADICTED"
                self._state_delta(blk["id"], before, "CONTRADICTED",
                                  "conflict with %s" % other["id"], principal, now)
        return self._receipt(
            "CONTRADICT", block_id, "ACTIVE", "CONTRADICTED",
            ["contradiction recorded: %s <-> %s; both preserved, neither "
             "auto-resolved" % (block_id, other_id)],
            {"reasons": []}, {"evidence_refs": evidence_refs or []},
            principal, now, contradicts_with=other_id)

    def invalidate(self, block_id: str, reason: str, principal: Dict[str, Any],
                   now: Optional[str] = None) -> Dict[str, Any]:
        """§8 — invalidation is itself a block: the disproof is knowledge."""
        now = now or _now_iso()
        block = self.blocks.get(block_id)
        if block is None:
            raise KeyError("invalidate: unknown block %r" % (block_id,))
        tr = self._transition(block, "INVALIDATED", "invalidated: %s" % reason, now)
        block["epistemicState"] = "INVALIDATED"
        self._state_delta(block_id, tr["from"], "INVALIDATED", reason, principal, now)
        inv_candidate = {
            "content": "INVALIDATION of %s: %s" % (block_id, reason),
            "proposed_class": "REFERENCE",
            "class_signals": [{"signal": "invalidation_record", "value": 1.0}],
            "classifier": "auto",
            "provenance": {"sources": [{
                "kind": "DERIVED", "ref": block_id,
                "capturedAt": now, "capturedBy": principal.get("identity")}]},
            "identity_binding": {"verified": True},
            "owner_scope": block["ownerScope"],
            "consent_ref": block.get("consentRef"),
            "epistemic_state": "CLASSIFIED",
            "evidence_refs": block.get("evidenceRefs", []),
        }
        inv_receipt = self.ingest(inv_candidate, principal, now=now)
        return self._receipt(
            "INVALIDATE", block_id, tr["from"], tr["to"],
            ["invalidated: %s" % reason,
             "invalidation persisted as its own block %s" % inv_receipt.get("blockId")],
            {"reasons": []}, {"evidence_refs": []}, principal, now,
            invalidation_block=inv_receipt.get("blockId"))

    def _state_delta(self, block_id: str, before: str, after: str, reason: str,
                     principal: Dict[str, Any], now: str) -> None:
        """§1.2 — downstream consumers of a block are owed the news when its
        epistemic state changes. Knowledge is a ledger, not a snapshot."""
        self.state_deltas.append({
            "block_id": block_id, "before": before, "after": after,
            "reason": reason, "at": now,
            "issuedBy": principal.get("identity"),
            "delivery": "pending: lineage-subscriber fan-out is a substrate "
                        "concern; the delta is persisted here, not dropped",
        })

    # ------------------------------------------------------------------
    # §4.1 promotion / demotion and reclassification review
    # ------------------------------------------------------------------
    def promote(self, block_id: str, target_class: str,
                evidence: Dict[str, Any], principal: Dict[str, Any],
                now: Optional[str] = None) -> Dict[str, Any]:
        """Promotion between classes requires the target class's gate:
        supporting evidence cited for CONTEXT (presence recorded; KNOW does
        not assess its sufficiency), a PROVE assessment receipt for REUSABLE
        (Ultimate Lock: epistemic claim/evidence assessment belongs to
        PROVE — KNOW binds the receipt, never judges the evidence). A
        versioned transition with lineage, never a silent field edit."""
        now = now or _now_iso()
        block = self.blocks.get(block_id)
        if block is None:
            raise KeyError("promote: unknown block %r" % (block_id,))
        if block["state"] != "ACTIVE":
            raise ValueError("promote: block %s in state %r is not promotable"
                             % (block_id, block["state"]))
        current = block["class"]
        if target_class not in CLASS_LADDER or current not in CLASS_LADDER:
            raise ValueError("promote: %s -> %s not on the promotion ladder; "
                             "CORE is never reachable by promotion" % (current, target_class))
        if CLASS_LADDER[target_class] != CLASS_LADDER[current] + 1:
            raise ValueError("promote: only single-rung promotion %s -> next rung allowed"
                             % current)
        if target_class == "CONTEXT" and not (evidence.get("supporting") or block["evidenceRefs"]):
            raise ValueError("promote: CONTEXT requires supporting evidence")
        if target_class == "REUSABLE" and not _valid_prove_ref(
                evidence.get("prove_receipt_ref")):
            raise ValueError(
                "promote: REUSABLE requires a PROVE assessment receipt "
                "(prove_receipt_ref naming NAYA-KERNEL-PROVE); KNOW does not "
                "assess verification evidence itself (Ultimate Lock)")
        before = current
        block["class"] = target_class
        block["transitions"].append({"from": before, "to": target_class, "at": now,
                                     "reason": "promotion gate passed: %s" %
                                     (evidence.get("kind") or "supporting evidence")})
        return self._receipt(
            "RECLASSIFY", block_id, before, target_class,
            ["promotion %s -> %s: target-class gate passed with %s"
             % (before, target_class, evidence.get("kind") or "supporting evidence")],
            {"reasons": []}, {"evidence_refs": evidence.get("refs", [])},
            principal, now, promotion_evidence=evidence)

    def request_reclassification(self, block_id: str, reason: str,
                                 principal: Dict[str, Any],
                                 now: Optional[str] = None) -> Dict[str, Any]:
        """§4.1 — misclassification detected downstream (e.g. PROVE finds a
        REUSABLE block unsupported): the block is HELD, not served in the
        meantime."""
        now = now or _now_iso()
        block = self.blocks.get(block_id)
        if block is None:
            raise KeyError("request_reclassification: unknown block %r" % (block_id,))
        tr = self._transition(block, "CLASSIFICATION_REVIEW",
                              "reclassification review: %s" % reason, now)
        self._state_delta(block_id, tr["from"], tr["to"], reason, principal, now)
        return self._receipt("RECLASSIFY", block_id, tr["from"], tr["to"],
                             ["held for reclassification review: %s" % reason],
                             {"reasons": []}, {"evidence_refs": []}, principal, now)

    def resolve_reclassification(self, block_id: str, new_class: str,
                                 class_signals: List[Dict[str, Any]],
                                 principal: Dict[str, Any],
                                 now: Optional[str] = None) -> Dict[str, Any]:
        """Re-gate a held block: the new class must pass the §4 rules again."""
        now = now or _now_iso()
        block = self.blocks.get(block_id)
        if block is None:
            raise KeyError("resolve_reclassification: unknown block %r" % (block_id,))
        if block["state"] != "CLASSIFICATION_REVIEW":
            raise ValueError("block %s is not under review" % block_id)
        if new_class not in CLASSES:
            raise ValueError("unknown class %r" % (new_class,))
        if not class_signals:
            raise ValueError("unexplained classification refused")
        if new_class == "CORE":
            raise ValueError("CORE cannot be assigned via reclassification; "
                             "director ingestion path only")
        before = block["class"]
        block["class"] = new_class
        block["classSignals"] = class_signals
        tr = self._transition(block, "ACTIVE", "re-gated to class %r" % new_class, now)
        return self._receipt("RECLASSIFY", block_id, tr["from"], tr["to"],
                             ["reclassification resolved: class %s -> %s, re-gated"
                              % (before, new_class)],
                             {"reasons": []}, {"evidence_refs": []}, principal, now,
                             class_before=before, class_after=new_class)

    def resolve_director_pending(self, block_id: str, decision: str,
                                 principal: Dict[str, Any],
                                 now: Optional[str] = None) -> Dict[str, Any]:
        """Director decision on a CLASSIFICATION_PENDING (CORE-proposed) block:
        'approve' persists it as CORE; 'refuse' refuses it with a receipt."""
        now = now or _now_iso()
        block = self.blocks.get(block_id)
        if block is None:
            raise KeyError("resolve_director_pending: unknown block %r" % (block_id,))
        if block["state"] != "CLASSIFICATION_PENDING":
            raise ValueError("block %s is not pending director decision" % block_id)
        if decision == "approve":
            tr = self._transition(block, "ACTIVE",
                                  "director approved CORE assignment", now)
            return self._receipt("CLASSIFY", block_id, tr["from"], tr["to"],
                                 ["director decision: CORE assignment approved"],
                                 {"reasons": []}, {"evidence_refs": []}, principal, now)
        tr = self._transition(block, "REFUSED", "director refused CORE assignment", now)
        return self._receipt("REFUSE", block_id, tr["from"], tr["to"],
                             ["director decision: CORE assignment refused"],
                             {"reasons": []}, {"evidence_refs": []}, principal, now)

    # ------------------------------------------------------------------
    # §7.7 poisoning → quarantine
    # ------------------------------------------------------------------
    def quarantine_batch(self, candidates: List[Dict[str, Any]],
                         principal: Dict[str, Any],
                         anomaly_signals: List[str],
                         now: Optional[str] = None) -> Dict[str, Any]:
        """Poisoning signals (bulk anomalies, source shifts) → the whole
        batch is quarantined and refused; the attempt itself is persisted as
        a security event. No partial ingestion.

        Spec §7.7/§9 — quarantine on poisoning signals (bulk anomalies, source shifts)."""
        now = now or _now_iso()
        event = {
            "kind": "INGESTION_QUARANTINE",
            "at": now,
            "issuedBy": principal.get("identity"),
            "anomaly_signals": list(anomaly_signals),
            "batch_size": len(candidates),
            "ingested": 0,
        }
        self.security_events.append(event)
        self.ingestion_log.append({
            "outcome": "QUARANTINED", "block_id": None, "at": now,
            "reasons": ["§7.7: batch quarantined; signals: %s" % ", ".join(anomaly_signals)],
            "content_hash": None,
        })
        return self._receipt(
            "QUARANTINE", None, None, "QUARANTINED",
            ["§7.7: %d candidates quarantined, 0 ingested; attempt persisted "
             "as a security event" % len(candidates)],
            {"reasons": []}, {"evidence_refs": []}, principal, now,
            anomaly_signals=anomaly_signals)

    # ------------------------------------------------------------------
    # §5 provenance audit — loss is detected, not assumed away
    # ------------------------------------------------------------------
    def provenance_audit(self, now: Optional[str] = None) -> Dict[str, Any]:
        """Recompute every block's provenance chain. A block whose chain no
        longer resolves → PROVENANCE_REVIEW, withheld from serving until
        repaired or invalidated (master acceptance criterion 6)."""
        now = now or _now_iso()
        withheld, healthy = [], []
        for block in self.blocks.values():
            problems = self._chain_problems(block)
            if problems:
                if block["state"] in ("ACTIVE", "CONTRADICTED"):
                    frm = block["state"]
                    try:
                        self._transition(block, "PROVENANCE_REVIEW",
                                         "provenance audit: %s" % "; ".join(problems), now)
                        self._state_delta(block["id"], frm, "PROVENANCE_REVIEW",
                                          "; ".join(problems),
                                          {"identity": "NAYA-KERNEL-KNOW/audit"}, now)
                    except ValueError:
                        pass
                withheld.append({"block_id": block["id"], "problems": problems,
                                 "state": block["state"]})
            else:
                healthy.append(block["id"])
        return {"audited": len(self.blocks), "healthy": healthy,
                "withheld": withheld, "at": now}

    def _chain_problems(self, block: Dict[str, Any]) -> List[str]:
        problems = []
        prov = block.get("provenance") or {}
        sources = prov.get("sources") or []
        if not sources:
            problems.append("no sources")
        for s in sources:
            if s.get("kind") not in SOURCE_KINDS:
                problems.append("unknown source kind %r" % s.get("kind"))
            if not s.get("ref"):
                problems.append("source missing ref")
        for t in prov.get("transforms") or []:
            if t.get("kind") not in TRANSFORM_KINDS:
                problems.append("unknown transform kind %r" % t.get("kind"))
            for src in t.get("from", []):
                if src not in self.blocks:
                    problems.append("transform source %r no longer resolves" % src)
        if prov.get("boundBy") != "node_id=%s" % NODE_ID:
            problems.append("chain not bound by this node")
        return problems

    def repair_provenance(self, block_id: str, provenance: Dict[str, Any],
                          principal: Dict[str, Any],
                          now: Optional[str] = None) -> Dict[str, Any]:
        """Repair a PROVENANCE_REVIEW block's chain and return it to serving."""
        now = now or _now_iso()
        block = self.blocks.get(block_id)
        if block is None:
            raise KeyError("repair_provenance: unknown block %r" % (block_id,))
        if block["state"] != "PROVENANCE_REVIEW":
            raise ValueError("block %s is not under provenance review" % block_id)
        block["provenance"] = _deepcopy_json(provenance)
        block["provenance"]["boundAt"] = now
        block["provenance"]["boundBy"] = "node_id=%s" % NODE_ID
        if self._chain_problems(block):
            raise ValueError("repaired chain still does not resolve")
        tr = self._transition(block, "ACTIVE", "provenance repaired and re-verified", now)
        self._state_delta(block_id, tr["from"], tr["to"], "provenance repaired",
                          principal, now)
        return self._receipt("RECLASSIFY", block_id, tr["from"], tr["to"],
                             ["provenance repaired; block returned to serving"],
                             {"reasons": []}, {"evidence_refs": []}, principal, now)

    # ------------------------------------------------------------------
    # expiry sweep (§8 ttl/context end → EXPIRED + tombstone receipt)
    # ------------------------------------------------------------------
    def expire_sweep(self, now: Optional[str] = None) -> Dict[str, Any]:
        """Sweep ACTIVE/CONTRADICTED blocks whose validUntil/ttl has lapsed
        into EXPIRED (§7 temporal law: CURRENT(o,t) ⟺ valid_from ≤ t <
        valid_until; expired blocks keep their tombstone, never silent
        erasure per §15 lifecycle)."""
        now = now or _now_iso()
        expired = []
        for block in self.blocks.values():
            if block["state"] not in ("ACTIVE", "CONTRADICTED"):
                continue
            if not self._freshness_ok(block, now):
                frm = block["state"]
                self._transition(block, "EXPIRED",
                                 "ttl/validity window ended; tombstone retained", now)
                block["epistemicState"] = "EXPIRED"
                self._state_delta(block["id"], frm, "EXPIRED", "ttl/validity ended",
                                  {"identity": "NAYA-KERNEL-KNOW/sweep"}, now)
                expired.append(block["id"])
                self._receipt("EXPIRE", block["id"], frm, "EXPIRED",
                              ["expired by ttl/validity; tombstone receipt retained"],
                              {"reasons": []}, {"evidence_refs": []},
                              {"identity": "NAYA-KERNEL-KNOW/sweep"}, now)
        return {"expired": expired, "at": now}

    # ------------------------------------------------------------------
    # §10 cold reconstruction — checkpoint + receipt-log replay
    # ------------------------------------------------------------------
    def checkpoint(self, now: Optional[str] = None) -> Dict[str, Any]:
        """Snapshot: block store + receipt-log offset. Indexes are caches —
        they are re-derived, never trusted (§10 step 3)."""
        now = now or _now_iso()
        snap = {
            "node_id": NODE_ID,
            "at": now,
            "blocks": _deepcopy_json(self.blocks),
            "receipt_log_offset": len(self.receipts),
            "store_hash": self._store_hash(),
        }
        snap["checkpoint_hash"] = _sha256({k: v for k, v in snap.items()
                                           if k != "checkpoint_hash"})
        self.checkpoints.append(snap)
        self._receipt("CHECKPOINT", None, None, "CHECKPOINTED",
                      ["checkpoint %s: %d blocks, store hash %s"
                       % (snap["checkpoint_hash"][:12], len(self.blocks), snap["store_hash"][:12])],
                      {"reasons": []}, {"evidence_refs": []},
                      {"identity": "NAYA-KERNEL-KNOW/checkpoint"}, now,
                      checkpoint_hash=snap["checkpoint_hash"])
        return _deepcopy_json(snap)

    def _store_hash(self) -> str:
        return _sha256(sorted(
            (bid, b["contentHash"], b["state"], b["class"], b["epistemicState"])
            for bid, b in self.blocks.items()))

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rebuild this node's durable state from receipts alone (cold start).

        §10 procedure: validate persisted receipt integrity → replay the
        receipt log → re-derive indexes → provenance_audit → install the
        reconstructed state on THIS node → emit a hash-bound RESTORE receipt.

        A reconstruction report is not sufficient if the receiving node stays
        empty. Public operations after this method returns must operate on the
        restored state. If any persisted artifact is malformed, tampered, or
        cannot be replayed coherently, fail loudly rather than return a
        green-looking receipt over unusable state.
        """
        fresh = KnowNode()
        mine = [r for r in (_deepcopy_json(receipts))
                if r.get("node_id") == NODE_ID]
        mine.sort(key=lambda r: (r.get("seq", 0), r.get("issuedAt", "")))
        replayed = 0
        checkpoint_ref = None
        max_seq = 0

        def replay_transition(block: Optional[Dict[str, Any]], to_state: str,
                              receipt: Dict[str, Any], reason: str) -> None:
            if block is None:
                raise ValueError(
                    "cold_reconstruct: %s references missing block %r"
                    % (receipt.get("operation"), receipt.get("blockId")))
            before = block.get("state")
            if before == to_state:
                return
            block["state"] = to_state
            block.setdefault("transitions", []).append({
                "from": before,
                "to": to_state,
                "at": receipt.get("issuedAt") or receipt.get("at") or _now_iso(),
                "reason": reason,
            })

        for r in mine:
            claimed_hash = r.get("receipt_hash")
            if not claimed_hash:
                raise ValueError(
                    "cold_reconstruct: persisted KNOW receipt lacks receipt hash; "
                    "integrity unverifiable")
            body = {k: v for k, v in r.items() if k != "receipt_hash"}
            if claimed_hash != _sha256(body):
                raise ValueError(
                    "cold_reconstruct: receipt hash integrity check failed "
                    "for %s"
                    % claimed_hash[:12])

            seq = r.get("seq")
            if isinstance(seq, int):
                if seq < 0:
                    raise ValueError("cold_reconstruct: negative receipt seq")
                max_seq = max(max_seq, seq)

            op = r.get("operation")
            if op in ("CHECKPOINT", "RESTORE"):
                if op == "CHECKPOINT":
                    checkpoint_ref = r.get("checkpoint_hash")
                continue  # no store effect; noted, not replayed

            if op == "INGEST" and r.get("afterState") == "ACTIVE":
                if r.get("duplicate_of"):
                    replayed += 1  # dedupe reference; no store effect
                    continue
                snap = r.get("block_snapshot")
                if snap is None:
                    raise ValueError(
                        "cold_reconstruct: INGEST receipt %s lacks block_snapshot; "
                        "persistence defective" % claimed_hash[:12])
                bid = snap.get("id")
                content_hash = snap.get("contentHash")
                if not bid or not content_hash:
                    raise ValueError(
                        "cold_reconstruct: INGEST snapshot lacks identity/hash")
                if bid in fresh.blocks and fresh.blocks[bid] != snap:
                    raise ValueError(
                        "cold_reconstruct: conflicting snapshot for block %s" % bid)
                indexed = fresh._hash_index.get(content_hash)
                if indexed is not None and indexed != bid:
                    raise ValueError(
                        "cold_reconstruct: content hash %s maps to conflicting blocks"
                        % content_hash[:12])
                fresh.blocks[bid] = snap
                fresh._hash_index[content_hash] = bid
                replayed += 1

            elif op == "CLASSIFY":
                after = r.get("afterState")
                if after == "CLASSIFICATION_PENDING":
                    snap = r.get("block_snapshot")
                    if snap is None:
                        raise ValueError(
                            "cold_reconstruct: CLASSIFY receipt lacks block_snapshot")
                    bid = snap.get("id")
                    content_hash = snap.get("contentHash")
                    if not bid or not content_hash:
                        raise ValueError(
                            "cold_reconstruct: CLASSIFY snapshot lacks identity/hash")
                    fresh.blocks[bid] = snap
                    fresh._hash_index[content_hash] = bid
                elif after in ("ACTIVE", "REFUSED"):
                    blk = fresh.blocks.get(r.get("blockId"))
                    replay_transition(
                        blk, after, r,
                        "cold replay of director classification decision")
                else:
                    raise ValueError(
                        "cold_reconstruct: unsupported CLASSIFY afterState %r" % after)
                replayed += 1

            elif op == "SUPERSEDE":
                old = fresh.blocks.get(r.get("blockId"))
                replay_transition(
                    old, "SUPERSEDED", r,
                    "cold replay: superseded by %s" % r.get("superseded_by"))
                old["supersededBy"] = r.get("superseded_by")
                old["epistemicState"] = "SUPERSEDED"
                replayed += 1

            elif op == "CONTRADICT":
                primary = r.get("blockId")
                other = r.get("contradicts_with")
                for bid, peer in ((primary, other), (other, primary)):
                    blk = fresh.blocks.get(bid)
                    replay_transition(
                        blk, "CONTRADICTED", r,
                        "cold replay: contradicted by %s" % peer)
                    blk["epistemicState"] = "CONTRADICTED"
                    blk.setdefault("contradicts", [])
                    if peer not in blk["contradicts"]:
                        blk["contradicts"].append(peer)
                replayed += 1

            elif op == "INVALIDATE":
                blk = fresh.blocks.get(r.get("blockId"))
                replay_transition(
                    blk, "INVALIDATED", r, "cold replay: invalidated")
                blk["epistemicState"] = "INVALIDATED"
                # The invalidation block itself arrives via its own INGEST receipt.
                replayed += 1

            elif op == "EXPIRE":
                blk = fresh.blocks.get(r.get("blockId"))
                replay_transition(blk, "EXPIRED", r, "cold replay: expired")
                blk["epistemicState"] = "EXPIRED"
                replayed += 1

            elif op == "RECLASSIFY":
                blk = fresh.blocks.get(r.get("blockId"))
                if blk is None:
                    raise ValueError(
                        "cold_reconstruct: RECLASSIFY references missing block %r"
                        % r.get("blockId"))
                if r.get("promotion_evidence"):
                    before_class = blk.get("class")
                    after_class = r.get("afterState")
                    blk["class"] = after_class
                    blk.setdefault("transitions", []).append({
                        "from": before_class,
                        "to": after_class,
                        "at": r.get("issuedAt") or _now_iso(),
                        "reason": "cold replay: class promotion",
                    })
                elif r.get("class_after"):
                    before_class = blk.get("class")
                    after_class = r.get("class_after")
                    blk["class"] = after_class
                    if before_class != after_class:
                        blk.setdefault("transitions", []).append({
                            "from": before_class,
                            "to": after_class,
                            "at": r.get("issuedAt") or _now_iso(),
                            "reason": "cold replay: reclassification",
                        })
                    replay_transition(
                        blk, r.get("afterState", blk.get("state")), r,
                        "cold replay: reclassification resolved")
                else:
                    replay_transition(
                        blk, r.get("afterState", blk.get("state")), r,
                        "cold replay: lifecycle reclassification")
                replayed += 1

            elif op == "REFUSE":
                # Most refusals have no store effect. A director refusal of a
                # previously persisted CLASSIFICATION_PENDING block does.
                bid = r.get("blockId")
                if bid and bid in fresh.blocks and r.get("afterState") == "REFUSED":
                    replay_transition(
                        fresh.blocks[bid], "REFUSED", r,
                        "cold replay: persisted classification refused")
                replayed += 1

            elif op in ("QUARANTINE", "SERVE"):
                replayed += 1  # no store effect; counted for the audit trail

            else:
                raise ValueError(
                    "cold_reconstruct: unknown operation %r; cannot replay" % op)

        audit = fresh.provenance_audit()
        withheld = [w["block_id"] for w in audit["withheld"]]
        store_hash = fresh._store_hash()

        # CS-01 repair: install the reconstructed durable state on the actual
        # receiving node. A report over a throwaway local object is not
        # continuity. Restore the replay log and sequence as well so later
        # authorized writes cannot collide with predecessor receipt ordering.
        self.blocks = _deepcopy_json(fresh.blocks)
        self._hash_index = dict(fresh._hash_index)
        self.receipts = _deepcopy_json(mine)
        self.ingestion_log = []
        self.intake_queue = deque()
        self.state_deltas = _deepcopy_json(fresh.state_deltas)
        self.security_events = []
        self.checkpoints = []
        self._seq = max_seq

        restore_at = _now_iso()
        restore = self._receipt(
            "RESTORE", None, None, "RESTORED",
            ["cold reconstruction installed on receiving KNOW node",
             "replayed %d persisted receipts; restored %d blocks"
             % (replayed, len(self.blocks))],
            {"reasons": []}, {"evidence_refs": []},
            {"identity": "NAYA-KERNEL-KNOW/restore"}, restore_at,
            checkpoint_ref=checkpoint_ref,
            replayed=replayed,
            restored_block_count=len(self.blocks),
            withheld_blocks=withheld,
            store_hash=store_hash,
        )

        return {"node_id": NODE_ID,
                "restored_block_count": len(self.blocks),
                "replayed_receipts": replayed,
                "checkpoint_ref": checkpoint_ref,
                "withheld_blocks": withheld,
                "store_hash": store_hash,
                "restore_receipt": restore,
                "block_ids": sorted(self.blocks)}
