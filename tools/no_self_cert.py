#!/usr/bin/env python3
"""UD-02 — NOTHING MAY CERTIFY ITSELF.

No worker, seat, or lane may declare its own consequential work correct.
Every certification of a consequential artifact is checked for genuine
independence before it can be accepted:

  1. IDENTITY    — the verifier must not be the doer (seat or agent id).
  2. CONTEXT     — the verifier must not share the doer's session/context.
  3. EVIDENCE    — the verifier must bring its own evidence: not a
                   restatement of the doer's claims (parrot check), and at
                   least one checkable source independent of the doer's
                   claims (independent-source check).
  4. PROVENANCE  — the evidence's support must not trace back to the claim
                   itself (circular-evidence check, transitive).

A certification that fails any check is REFUSED with machine-readable
reason codes. All attempts (accepted and refused) can be written to an
append-only ledger.

What this does NOT claim:
  - It does not detect collusion between two distinct seats that share a
    hidden back-channel outside the recorded session/context.
  - It does not judge whether the doer's claims are TRUE — only whether
    the certification is independent. Truth is the verifier's job.
  - The parrot threshold is a tripwire, not a semantic understanding.

Stdlib only.

Usage:
    from no_self_cert import (
        Identity, Artifact, Evidence, Certification, Ledger, certify,
    )

    doer = Identity(seat="naya-4", session_id="s1", context_fingerprint="c1")
    art = Artifact.from_content("art-1", "<bytes>", doer,
                                claims=["the gate rejects empty evidence"])
    verifier = Identity(seat="naya-2", session_id="s9", context_fingerprint="c9")
    cert = Certification(
        artifact_id="art-1", verifier=verifier, verdict="PASS",
        evidence=[Evidence(text="ran tools/test_no_self_cert.py: 12/12 pass",
                           sources=["test-run:tools/test_no_self_cert.py"])],
    )
    decision = certify(art, cert)
    assert decision.accepted
"""

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

PARROT_JACCARD_THRESHOLD = 0.5
SHINGLE_N = 5

# Machine-readable refusal reasons.
REJECT_SELF = "SELF_CERTIFICATION"      # verifier is the doer
REJECT_CONTEXT = "SHARED_CONTEXT"       # verifier shares doer's session/context
REJECT_NO_VERDICT = "NO_VERDICT"        # verdict not PASS/FAIL
REJECT_NO_EVIDENCE = "NO_EVIDENCE"      # no evidence supplied
REJECT_PARROT = "PARROT_EVIDENCE"       # evidence restates doer's claims
REJECT_DERIVATIVE = "DERIVATIVE_ONLY"   # every source traces to doer's claims
REJECT_CIRCULAR = "CIRCULAR_PROVENANCE" # support chain reaches the claim itself
REJECT_MISMATCH = "ARTIFACT_MISMATCH"   # cert names a different artifact


def _utcnow():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def _shingles(text, n=SHINGLE_N):
    toks = _tokens(text)
    if not toks:
        return set()
    if len(toks) < n:
        return {tuple(toks)}
    return {tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def jaccard(a, b):
    """Jaccard similarity of two shingle sets."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


@dataclass(frozen=True)
class Identity:
    """Who acted. seat + session_id + context_fingerprint together define
    'a different mind'. Two records sharing any of them are not independent."""
    seat: str                 # e.g. "naya-4", "coda-1"
    session_id: str           # runtime session / agent id
    context_fingerprint: str  # hash of the shared conversation context
    agent_id: str = ""        # stable agent identity when known


@dataclass
class Artifact:
    """A consequential work product carrying its doer's identity."""
    artifact_id: str
    content_hash: str
    doer: Identity
    claims: list = field(default_factory=list)
    created_utc: str = field(default_factory=_utcnow)

    @classmethod
    def from_content(cls, artifact_id, content, doer, claims):
        if isinstance(content, str):
            content = content.encode()
        return cls(artifact_id, hashlib.sha256(content).hexdigest(),
                   doer, list(claims))


@dataclass
class Evidence:
    """One observation by the verifier. sources are checkable references
    ('test-run:...', 'api:GET ...', 'file:...'). derived_from lists the
    artifact/claim ids this observation was derived from — it must never
    resolve back to the artifact being certified."""
    text: str
    sources: list = field(default_factory=list)
    derived_from: list = field(default_factory=list)


@dataclass
class Certification:
    """A verifier's judgment on an artifact."""
    artifact_id: str
    verifier: Identity
    verdict: str              # "PASS" or "FAIL" — a FAIL from an independent
                              # verifier is a valid certification too
    evidence: list = field(default_factory=list)
    created_utc: str = field(default_factory=_utcnow)


@dataclass
class Decision:
    accepted: bool
    reasons: list             # machine-readable codes; empty when accepted
    detail: str               # human-readable summary
    receipt: dict             # tamper-evident record of the check


def _is_doer_worded_source(src):
    """A source that is just the doer's own claims wearing a label."""
    s = (src or "").strip().lower()
    return (not s) or ("doer" in s and "claim" in s) or s in {
        "doer", "doer's words", "doers words", "the doer's summary",
        "doer summary", "author assertion"}


def _circular_evidence_indices(cert, tainted_ids):
    """Indices of evidence items whose support chain reaches a tainted id
    (the certified artifact, or the doer's claim set), transitively through
    evidence->evidence references of the form 'evidence:<i>'."""
    n = len(cert.evidence)
    tainted = set()
    for i, e in enumerate(cert.evidence):
        if tainted_ids & set(e.derived_from):
            tainted.add(i)
    changed = True
    while changed:
        changed = False
        for i, e in enumerate(cert.evidence):
            if i in tainted:
                continue
            for d in e.derived_from:
                m = re.fullmatch(r"evidence:(\d+)", (d or "").strip())
                if m and int(m.group(1)) in tainted:
                    tainted.add(i)
                    changed = True
    return tainted


def evaluate(artifact, cert):
    """Check a certification for genuine independence. Never raises on
    adversarial input — every failure mode becomes a refusal reason."""
    reasons = []
    doer, ver = artifact.doer, cert.verifier

    if cert.artifact_id != artifact.artifact_id:
        reasons.append(REJECT_MISMATCH)

    # 1. identity — the verifier must not be the doer
    if ver.seat == doer.seat:
        reasons.append(REJECT_SELF)
    elif ver.agent_id and doer.agent_id and ver.agent_id == doer.agent_id:
        reasons.append(REJECT_SELF)

    # 2. context — a renamed seat in the same session is the same mind
    if ver.session_id and doer.session_id \
            and ver.session_id == doer.session_id:
        reasons.append(REJECT_CONTEXT)
    elif ver.context_fingerprint and doer.context_fingerprint \
            and ver.context_fingerprint == doer.context_fingerprint:
        reasons.append(REJECT_CONTEXT)

    # 3a. a certification must actually judge and show its work
    if cert.verdict not in ("PASS", "FAIL"):
        reasons.append(REJECT_NO_VERDICT)
    if not cert.evidence or not any((e.text or "").strip()
                                    for e in cert.evidence):
        reasons.append(REJECT_NO_EVIDENCE)

    doer_text = "\n".join(artifact.claims or [])
    ev_text = "\n".join((e.text or "") for e in cert.evidence)

    # 3b. parrot check — evidence that restates the claims is not evidence
    similarity = 0.0
    if doer_text.strip() and ev_text.strip():
        similarity = jaccard(_shingles(doer_text), _shingles(ev_text))
    if similarity >= PARROT_JACCARD_THRESHOLD:
        reasons.append(REJECT_PARROT)

    # 3c. independent-source check — at least one evidence item must rest on
    # a checkable source that is not the doer's own claims
    independent = False
    for e in cert.evidence:
        real_sources = [s for s in (e.sources or [])
                        if not _is_doer_worded_source(s)]
        derived_clean = not ({"doer-claims", artifact.artifact_id}
                             & set(e.derived_from or []))
        if real_sources and derived_clean and (e.text or "").strip():
            independent = True
            break
    if cert.evidence and not independent:
        reasons.append(REJECT_DERIVATIVE)

    # 4. circular provenance — support must not trace back to the claim
    tainted = _circular_evidence_indices(
        cert, {artifact.artifact_id, "doer-claims"})
    if tainted:
        reasons.append(REJECT_CIRCULAR)

    accepted = not reasons
    detail = ("ACCEPTED: independent certification"
              if accepted else
              "REFUSED: " + ", ".join(reasons))
    receipt = {
        "artifact_id": artifact.artifact_id,
        "content_hash": artifact.content_hash,
        "doer_seat": doer.seat,
        "verifier_seat": ver.seat,
        "verdict": cert.verdict,
        "accepted": accepted,
        "reasons": list(reasons),
        "evidence_similarity": round(similarity, 3),
        "checked_utc": _utcnow(),
    }
    receipt["receipt_hash"] = hashlib.sha256(
        json.dumps(receipt, sort_keys=True).encode()).hexdigest()
    return Decision(accepted=accepted, reasons=reasons,
                    detail=detail, receipt=receipt)


class Ledger:
    """Append-only record of certification attempts (accepted and refused)."""

    def __init__(self, path=None):
        self.path = path
        self.entries = []
        if path:
            try:
                with open(path) as f:
                    self.entries = [json.loads(line) for line in f
                                    if line.strip()]
            except FileNotFoundError:
                pass

    def record(self, artifact, cert, decision):
        entry = {
            "utc": _utcnow(),
            "artifact_id": artifact.artifact_id,
            "content_hash": artifact.content_hash,
            "doer": {"seat": artifact.doer.seat,
                     "session_id": artifact.doer.session_id},
            "verifier": {"seat": cert.verifier.seat,
                         "session_id": cert.verifier.session_id},
            "verdict": cert.verdict,
            "accepted": decision.accepted,
            "reasons": decision.reasons,
            "receipt_hash": decision.receipt["receipt_hash"],
        }
        self.entries.append(entry)
        if self.path:
            with open(self.path, "a") as f:
                f.write(json.dumps(entry, sort_keys=True) + "\n")
        return entry


def certify(artifact, cert, ledger=None):
    """Evaluate and optionally ledger a certification attempt."""
    decision = evaluate(artifact, cert)
    if ledger is not None:
        ledger.record(artifact, cert, decision)
    return decision


def demo():
    """Demonstrate a self-certification attempt being refused."""
    doer = Identity(seat="naya-4", session_id="sess-1", context_fingerprint="ctx-1")
    art = Artifact.from_content(
        "demo-artifact", "fencing token uses monotonic uuid",
        doer, claims=["the fencing token binds authority via monotonic UUID",
                      "a dead authority token cannot validate at a recycled address"])
    print("== attempt 1: the doer certifies its own work ==")
    d1 = certify(art, Certification(
        artifact_id="demo-artifact", verifier=doer, verdict="PASS",
        evidence=[Evidence(text="looks correct to me", sources=["doer-claims"])]))
    print("accepted:", d1.accepted, "| reasons:", d1.reasons)

    print("== attempt 2: a parroting 'verifier' in the same session ==")
    impostor = Identity(seat="naya-9", session_id="sess-1", context_fingerprint="ctx-1")
    d2 = certify(art, Certification(
        artifact_id="demo-artifact", verifier=impostor, verdict="PASS",
        evidence=[Evidence(
            text="the fencing token binds authority via monotonic UUID; "
                 "a dead authority token cannot validate at a recycled address",
            sources=["doer-claims"],
            derived_from=["demo-artifact"])]))
    print("accepted:", d2.accepted, "| reasons:", d2.reasons)

    print("== attempt 3: a genuinely independent verifier ==")
    indep = Identity(seat="naya-2", session_id="sess-7", context_fingerprint="ctx-7")
    d3 = certify(art, Certification(
        artifact_id="demo-artifact", verifier=indep, verdict="PASS",
        evidence=[Evidence(
            text="ran the adversarial suite: recycled-address token rejected, "
                 "fresh authority accepted; 14/14 green",
            sources=["test-run:tools/test_no_self_cert.py::fencing"],
            derived_from=[])]))
    print("accepted:", d3.accepted, "| reasons:", d3.reasons)


if __name__ == "__main__":
    demo()
