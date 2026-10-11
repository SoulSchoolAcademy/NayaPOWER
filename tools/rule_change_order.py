"""UD-16 — ONE ORDER FOR CHANGING RULES; CRASHES CREATE NOTHING.

Plain words: rules change through one ordered process, never by side
channels. A single writer, a clear sequence, every change authorized and
recorded. No seat rewrites the rules mid-game. And when a worker crashes
mid-change, recovery reconstructs what actually committed from durable
evidence — it never invents a new outcome and never treats ambiguity
as permission.

Absorbs D53, D54.

Canonical commit sequence:
    PROPOSED -> PREPARED -> VERIFIED -> AUTHORIZED -> COMMITTED -> PROPAGATED

Recovery states (D54): PREPARED / COMMIT_OUTCOME_UNKNOWN / COMMITTED /
PROJECTION_PENDING / INDEPENDENTLY_VERIFIED.

Every committed rule change advances a monotonic governance epoch.
Commits lock the ledger and re-read governing state atomically.
"""

import hashlib
import threading
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# Refusals — every refusal carries a machine-readable code.
# ---------------------------------------------------------------------------

REFUSAL_CODES = (
    "UNAUTHORIZED_PROPOSER",
    "UNAUTHORIZED_AUTHORITY",
    "RULE_IN_FLIGHT",
    "STALE_BASE",
    "INSUFFICIENT_EVIDENCE",
    "SELF_VERIFY",
    "BAD_PHASE",
    "OUT_OF_ORDER",
    "PROPOSAL_TAMPERED",
    "MID_DECISION_REWRITE",
    "STALE_REPLAY",
    "REPLAY_DUPLICATE_SAFE",  # not a failure: idempotent replay, original receipt
    "AMBIGUOUS_NO_AUTHORITY",
)


class Refusal(Exception):
    """A refused governance action. Never raises past the caller silently."""

    def __init__(self, code, detail=""):
        if code not in REFUSAL_CODES:
            raise ValueError("unknown refusal code: %r" % code)
        self.code = code
        self.detail = detail
        super().__init__("[%s] %s" % (code, detail))


class SimulatedCrash(Exception):
    """Raised by the crash simulator at a named crash point. Test-only."""


# ---------------------------------------------------------------------------
# Guards (mutable only via disable_guard — the mutation harness).
# ---------------------------------------------------------------------------

_GUARDS = {"authz": True, "sequence": True, "inflight": True}


@contextmanager
def disable_guard(name):
    """Test-only: remove a guard to prove the suite detects the hole."""
    old = _GUARDS[name]
    _GUARDS[name] = False
    try:
        yield
    finally:
        _GUARDS[name] = old


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _proposal_hash(proposer, rule_id, old_text, new_text, reason, evidence):
    body = "|".join([
        proposer, rule_id,
        "" if old_text is None else old_text,
        new_text, reason,
        ",".join(sorted(evidence)),
    ])
    return _sha256_text(body)


PHASES = ("PROPOSED", "PREPARED", "VERIFIED", "AUTHORIZED", "COMMITTED", "PROPAGATED")
RECOVERY_STATES = (
    "PREPARED",
    "COMMIT_OUTCOME_UNKNOWN",
    "COMMITTED",
    "PROJECTION_PENDING",
    "INDEPENDENTLY_VERIFIED",
)


class RuleChange(object):
    """One proposed rule change. operation_id is bound to the exact
    proposal hash — durable operation identity."""

    def __init__(self, proposer, rule_id, old_text, new_text, reason,
                 evidence, base_epoch):
        self.proposal_hash = _proposal_hash(
            proposer, rule_id, old_text, new_text, reason, evidence)
        self.operation_id = "op-" + self.proposal_hash[:12]
        self.proposer = proposer
        self.rule_id = rule_id
        self.old_text = old_text
        self.new_text = new_text
        self.reason = reason
        self.evidence = list(evidence)
        self.base_epoch = base_epoch
        self.phase = "PROPOSED"
        self.commit_epoch = None

    def rehash(self):
        return _proposal_hash(self.proposer, self.rule_id, self.old_text,
                              self.new_text, self.reason, self.evidence)

    def to_dict(self):
        return {
            "operation_id": self.operation_id,
            "proposal_hash": self.proposal_hash,
            "proposer": self.proposer,
            "rule_id": self.rule_id,
            "old_text": self.old_text,
            "new_text": self.new_text,
            "reason": self.reason,
            "evidence": self.evidence,
            "base_epoch": self.base_epoch,
            "phase": self.phase,
            "commit_epoch": self.commit_epoch,
            "does_not_claim": (
                "A committed change proves the change followed the one order; "
                "it does not prove the new rule text is wise."
            ),
        }


class GovernanceLedger(object):
    """The one canonically ordered governance state.

    authorized_changers: set of identities allowed to propose/commit rule
    changes (e.g. Shawn, a ratified governance seat). Nobody else can move
    the rules — no side channels.
    """

    def __init__(self, authorized_changers, evidence_bar=1):
        self.authorized = set(authorized_changers)
        self.evidence_bar = evidence_bar
        self.epoch = 0
        self.rules = {}            # rule_id -> current text (durable)
        self.journal = []          # durable event log: (event, operation_id, ...)
        self.in_flight = {}        # rule_id -> RuleChange (at most one)
        self.decisions = {}        # decision_id -> {start_epoch, status}
        self._lock = threading.Lock()

    # -- decisions (the mid-game that rules must not be rewritten under) --

    def open_decision(self, decision_id):
        self.decisions[decision_id] = {"start_epoch": self.epoch,
                                       "status": "OPEN"}

    def close_decision(self, decision_id, outcome):
        d = self.decisions.get(decision_id)
        if d is None:
            raise Refusal("STALE_REPLAY", "unknown decision %r" % decision_id)
        if d["status"] != "OPEN":
            raise Refusal("MID_DECISION_REWRITE",
                          "decision %r already %s" % (decision_id, d["status"]))
        d["status"] = "CLOSED_" + outcome
        d["close_epoch"] = self.epoch

    def decision_valid(self, decision_id):
        """True only if the decision may still proceed under current rules."""
        d = self.decisions.get(decision_id)
        return bool(d) and d["status"] == "OPEN" and \
            d["start_epoch"] == self.epoch

    # -- the one order: propose -> prepare -> verify -> authorize -> commit --

    def propose(self, proposer, rule_id, old_text, new_text, reason,
                evidence):
        if _GUARDS["authz"] and proposer not in self.authorized:
            raise Refusal("UNAUTHORIZED_PROPOSER",
                          "%r is not an authorized rule changer" % proposer)
        if _GUARDS["inflight"] and rule_id in self.in_flight:
            raise Refusal("RULE_IN_FLIGHT",
                          "rule %r already has change %s in flight"
                          % (rule_id, self.in_flight[rule_id].operation_id))
        current = self.rules.get(rule_id)
        if old_text != current:
            raise Refusal("STALE_BASE",
                          "rule %r base text does not match current state" % rule_id)
        if not reason or len(evidence) < self.evidence_bar:
            raise Refusal("INSUFFICIENT_EVIDENCE",
                          "need reason + >=%d evidence refs" % self.evidence_bar)
        op = RuleChange(proposer, rule_id, old_text, new_text, reason,
                        evidence, self.epoch)
        self.journal.append(("PROPOSED", op.operation_id, op.proposal_hash))
        return op

    def prepare(self, op):
        self._require_phase(op, "PROPOSED")
        if op.rehash() != op.proposal_hash:
            raise Refusal("PROPOSAL_TAMPERED", op.operation_id)
        op.phase = "PREPARED"
        self.in_flight[op.rule_id] = op
        self.journal.append(("PREPARED", op.operation_id, op.proposal_hash))

    def independent_verify(self, op, verifier):
        self._require_phase(op, "PREPARED")
        if verifier == op.proposer:
            raise Refusal("SELF_VERIFY", "proposer cannot verify own change")
        if not op.reason or len(op.evidence) < self.evidence_bar:
            raise Refusal("INSUFFICIENT_EVIDENCE", op.operation_id)
        op.phase = "VERIFIED"
        self.journal.append(("VERIFIED", op.operation_id, verifier))

    def authorize(self, op, authority):
        self._require_phase(op, "VERIFIED")
        if _GUARDS["authz"] and authority not in self.authorized:
            raise Refusal("UNAUTHORIZED_AUTHORITY",
                          "%r cannot authorize rule changes" % authority)
        op.phase = "AUTHORIZED"
        self.journal.append(("AUTHORIZED", op.operation_id, authority))

    def commit(self, op, crash_point=None):
        """Atomic commit: lock, re-read governing state, apply in order."""
        self._require_phase(op, "AUTHORIZED")
        with self._lock:
            # Re-read governing state atomically inside the lock.
            epoch_now = self.epoch
            if _GUARDS["sequence"] and op.base_epoch != epoch_now:
                raise Refusal("OUT_OF_ORDER",
                              "%s based at epoch %d, ledger at %d"
                              % (op.operation_id, op.base_epoch, epoch_now))
            if op.rehash() != op.proposal_hash:
                raise Refusal("PROPOSAL_TAMPERED", op.operation_id)
            self.journal.append(("COMMIT_INTENT", op.operation_id, epoch_now))
            if crash_point == "during_commit":
                # Journal shows intent; durable store NOT updated.
                # Outcome is now ambiguous — recovery must resolve it.
                raise SimulatedCrash("during_commit")
            # Durable application.
            self.rules[op.rule_id] = op.new_text
            self.epoch = epoch_now + 1
            op.commit_epoch = self.epoch
            op.phase = "COMMITTED"
            self.journal.append(
                ("COMMIT_APPLIED", op.operation_id, self.epoch))
            # Mid-game protection: any decision opened under older rules
            # cannot proceed — it is voided and must re-run under the new epoch.
            for did, d in self.decisions.items():
                if d["status"] == "OPEN" and d["start_epoch"] < self.epoch:
                    d["status"] = "VOIDED_MID_DECISION_REWRITE"
                    d["void_epoch"] = self.epoch
            self.in_flight.pop(op.rule_id, None)
            return {
                "operation_id": op.operation_id,
                "rule_id": op.rule_id,
                "commit_epoch": self.epoch,
                "does_not_claim": (
                    "Receipt proves ordered, authorized application; "
                    "not the wisdom of the new rule."
                ),
            }

    def abort(self, op, reason):
        """Void a prepared-but-uncommittable change (e.g. its base epoch
        went stale). Works from any pre-commit phase. The rule is freed;
        the abort is journaled. The change may be re-proposed fresh at the
        current epoch."""
        if op.phase in ("COMMITTED", "PROPAGATED", "ABORTED"):
            raise Refusal("BAD_PHASE",
                          "%s is %s, cannot abort" % (op.operation_id, op.phase))
        holder = self.in_flight.get(op.rule_id)
        if holder is not op:
            raise Refusal("BAD_PHASE",
                          "%s is not the in-flight change" % op.operation_id)
        self.in_flight.pop(op.rule_id, None)
        op.phase = "ABORTED"
        self.journal.append(("ABORTED", op.operation_id, reason))

    def propagate(self, op):
        self._require_phase(op, "COMMITTED")
        op.phase = "PROPAGATED"
        self.journal.append(("PROPAGATED", op.operation_id, op.commit_epoch))

    # -- authority: ambiguous outcomes never create authority --

    def has_authority(self, operation_id):
        """True only for durably committed operations. While an outcome is
        COMMIT_OUTCOME_UNKNOWN, this returns False — ambiguity is never
        permission."""
        for rule_id, op in self.in_flight.items():
            if op.operation_id == operation_id:
                return False
        # Committed ops are no longer in flight; check journal for APPLIED.
        applied = [e for e in self.journal
                   if e[0] == "COMMIT_APPLIED" and e[1] == operation_id]
        return bool(applied)

    # -- idempotent replay: stale events can't overwrite newer state --

    def replay(self, op_dict):
        """Re-submit a proposal dict (e.g. after a crash). Same operation_id
        + same hash and already committed -> original receipt, no double
        apply. Older epoch than current -> STALE_REPLAY refused."""
        op_id = op_dict["operation_id"]
        if op_dict["base_epoch"] < self.epoch and not any(
                e[0] == "COMMIT_APPLIED" and e[1] == op_id
                for e in self.journal):
            raise Refusal("STALE_REPLAY",
                          "%s based at epoch %d, ledger at %d"
                          % (op_id, op_dict["base_epoch"], self.epoch))
        applied = [e for e in self.journal
                   if e[0] == "COMMIT_APPLIED" and e[1] == op_id]
        if applied:
            return {"operation_id": op_id,
                    "commit_epoch": applied[0][2],
                    "replay": "REPLAY_DUPLICATE_SAFE"}
        # Not yet committed: safe to re-drive through the one order.
        raise Refusal("STALE_REPLAY",
                      "%s not committed; re-propose through the one order" % op_id)

    # -- recovery: reconstruct what actually committed from durable evidence --

    @classmethod
    def recover(cls, journal, durable_rules, durable_epoch,
                authorized_changers, evidence_bar=1):
        """Rebuild the true committed state from (journal, durable store).
        The durable store is ground truth: a COMMIT_INTENT without a
        matching durable application means the commit did NOT happen.
        Returns (ledger, recovery_report)."""
        ledger = cls(authorized_changers, evidence_bar)
        ledger.rules = dict(durable_rules)
        ledger.epoch = durable_epoch
        ledger.journal = list(journal)
        report = {}
        intents = [e for e in journal if e[0] == "COMMIT_INTENT"]
        applied = {e[1]: e[2] for e in journal if e[0] == "COMMIT_APPLIED"}
        for _ev, op_id, _ep in intents:
            if op_id in applied:
                report[op_id] = "COMMITTED"
            else:
                # Ambiguous: journal intent, no durable application.
                # Durable store is ground truth -> not committed.
                # Safe to retry; never granted authority meanwhile.
                report[op_id] = "COMMIT_OUTCOME_UNKNOWN->NOT_COMMITTED"
        # Anything PREPARED but never intented is simply PREPARED.
        for ev, op_id, _h in journal:
            if ev == "PREPARED" and op_id not in report:
                report[op_id] = "PREPARED"
        propagated = {e[1] for e in journal if e[0] == "PROPAGATED"}
        for op_id in list(report):
            if report[op_id] == "COMMITTED" and op_id in propagated:
                report[op_id] = "INDEPENDENTLY_VERIFIED"
            elif report[op_id] == "COMMITTED":
                report[op_id] = "COMMITTED_PROJECTION_PENDING"
        return ledger, report

    # -- internals --

    def _require_phase(self, op, phase):
        if op.phase != phase:
            raise Refusal("BAD_PHASE",
                          "%s is %s, need %s"
                          % (op.operation_id, op.phase, phase))


# ---------------------------------------------------------------------------
# Crash matrix driver (test support): crash at each load-bearing point.
# ---------------------------------------------------------------------------

CRASH_POINTS = (
    "after_propose",      # nothing durable beyond PROPOSED
    "after_prepare",      # PREPARED, not committed
    "after_verify",       # VERIFIED, not committed
    "after_authorize",     # AUTHORIZED, not committed
    "during_commit",      # COMMIT_INTENT journaled, durable NOT updated
    "after_commit",        # COMMIT_APPLIED, not yet propagated
    "after_propagate",    # fully done
)


def drive_to_crash_point(ledger, op, verifier, authority, crash_point):
    """Drive one change through the one order, crashing at crash_point.
    Returns (journal_snapshot, durable_rules, durable_epoch) for recovery."""
    if crash_point in ("after_prepare", "after_verify", "after_authorize",
                       "during_commit", "after_commit", "after_propagate"):
        ledger.prepare(op)
    if crash_point in ("after_verify", "after_authorize", "during_commit",
                       "after_commit", "after_propagate"):
        ledger.independent_verify(op, verifier)
    if crash_point in ("after_authorize", "during_commit", "after_commit",
                       "after_propagate"):
        ledger.authorize(op, authority)
    if crash_point in ("during_commit",):
        try:
            ledger.commit(op, crash_point="during_commit")
        except SimulatedCrash:
            pass
    elif crash_point in ("after_commit", "after_propagate"):
        ledger.commit(op)
    if crash_point == "after_propagate":
        ledger.propagate(op)
    return (list(ledger.journal), dict(ledger.rules), ledger.epoch)
