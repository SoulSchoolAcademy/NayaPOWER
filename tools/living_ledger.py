"""UD-18 — NOTHING CONSEQUENTIAL HAPPENS UNTRACKED: the Living Ledger.

The capstone (D51). The master record above the sibling ledgers
(belief, baseline, work-honesty, exactly-once): every consequential
decision, action, evidence item, and outcome is appended as a chained,
tamper-evident receipt. Nothing consequential happens untracked.

Design:
- Append-only. There is no mutation API. History can only grow.
- Every receipt hash-chains to the previous one (sha256 over a
  canonical encoding). Any edit anywhere breaks the chain at an
  exactly named sequence number.
- DECISION and ACTION receipts must link evidence (non-empty
  evidence_refs) — an unlinked decision is refused, not recorded.
- Internal links (to other receipts' entry hashes) must reference
  entries that exist — dangling links are refused.
- Timestamps are monotonic — a backdated receipt is refused.
- Sibling ledgers feed the master via anchor_summary(): they submit a
  summary payload plus its hash; the hash is recomputed before
  acceptance. A mismatched anchor is refused, never recorded.
- Query surface: by actor, by kind, by time range, by causal chain.

This module proves tamper-evidence and queryability of what IS
recorded. It does NOT claim that every code path in the system calls
emit() — wiring the emitter into every consequential path is the
integration job that follows.
"""

import hashlib
import json
from dataclasses import dataclass, field

GENESIS_PREV = "GENESIS"

KINDS = ("DECISION", "ACTION", "EVIDENCE", "OUTCOME", "ANCHOR", "NOTE")

# Kinds that must carry evidence: an unlinked decision/action is refused.
EVIDENCE_REQUIRED_KINDS = ("DECISION", "ACTION")


class LedgerError(Exception):
    """Refusal with a machine-readable code."""

    def __init__(self, code, message):
        super().__init__(f"{code}: {message}")
        self.code = code


def _canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _utcnow_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Receipt:
    seq: int
    timestamp: str
    actor: str
    kind: str
    action: str
    evidence_refs: tuple = field(default_factory=tuple)
    scope: str = ""
    content: dict = field(default_factory=dict)
    links: tuple = field(default_factory=tuple)
    prev_hash: str = GENESIS_PREV
    entry_hash: str = ""

    def to_dict(self):
        return {
            "seq": self.seq,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "kind": self.kind,
            "action": self.action,
            "evidence_refs": list(self.evidence_refs),
            "scope": self.scope,
            "content": self.content,
            "links": list(self.links),
            "prev_hash": self.prev_hash,
            "entry_hash": self.entry_hash,
        }

    def does_not_claim(self):
        return ("This receipt proves a chained record exists with the stated "
                "content. It does not prove the content is true — truth is "
                "the sibling ledgers' job.")


class LivingLedger:
    """Append-only, hash-chained master record."""

    def __init__(self):
        self._entries = []  # list[Receipt], seq == index+1
        self._by_hash = {}

    # ---- emission ----------------------------------------------------

    def emit(self, *, actor, kind, action, evidence_refs=(),
             scope="", content=None, links=(), timestamp=None):
        """Append one chained receipt. Refusals raise LedgerError."""
        if not actor or not str(actor).strip():
            raise LedgerError("EMPTY_ACTOR", "actor is required")
        if kind not in KINDS:
            raise LedgerError("UNKNOWN_KIND",
                              f"kind must be one of {KINDS}, got {kind!r}")
        refs = tuple(evidence_refs or ())
        if kind in EVIDENCE_REQUIRED_KINDS and not refs:
            raise LedgerError(
                "UNLINKED_DECISION",
                f"{kind} receipt refused: every decision/action must link "
                "its evidence (evidence_refs may not be empty)")
        link_t = tuple(links or ())
        for lh in link_t:
            if lh not in self._by_hash:
                raise LedgerError("UNKNOWN_LINK",
                                  f"link references unknown entry hash {lh[:16]}...")
        ts = timestamp or _utcnow_iso()
        if self._entries and ts < self._entries[-1].timestamp:
            raise LedgerError(
                "BACKDATED_ENTRY",
                f"timestamp {ts} is older than head "
                f"{self._entries[-1].timestamp}; receipts are monotonic")
        seq = len(self._entries) + 1
        prev_hash = self._entries[-1].entry_hash if self._entries else GENESIS_PREV
        body = {
            "seq": seq, "timestamp": ts, "actor": actor, "kind": kind,
            "action": action, "evidence_refs": list(refs), "scope": scope,
            "content": content or {}, "links": list(link_t),
            "prev_hash": prev_hash,
        }
        entry_hash = _sha256_hex(_canonical(body))
        receipt = Receipt(seq=seq, timestamp=ts, actor=actor, kind=kind,
                          action=action, evidence_refs=refs, scope=scope,
                          content=content or {}, links=link_t,
                          prev_hash=prev_hash, entry_hash=entry_hash)
        self._entries.append(receipt)
        self._by_hash[entry_hash] = receipt
        return receipt

    # ---- sibling-ledger anchor feed -----------------------------------

    def anchor_summary(self, *, ledger_name, payload):
        """Accept an anchored summary from a sibling ledger.

        payload must be a dict containing 'payload_hash', the sha256 of the
        canonical encoding of the payload WITHOUT the payload_hash field.
        The hash is recomputed before acceptance; mismatch => refused.
        Returns the ANCHOR receipt.
        """
        if not isinstance(payload, dict) or "payload_hash" not in payload:
            raise LedgerError("ANCHOR_MALFORMED",
                              "payload must be a dict carrying 'payload_hash'")
        claimed = payload["payload_hash"]
        body = {k: v for k, v in payload.items() if k != "payload_hash"}
        actual = _sha256_hex(_canonical(body))
        if actual != claimed:
            raise LedgerError(
                "ANCHOR_HASH_MISMATCH",
                f"sibling ledger {ledger_name!r}: claimed {claimed[:16]}... "
                f"!= recomputed {actual[:16]}...; anchor refused")
        return self.emit(
            actor="living-ledger",
            kind="ANCHOR",
            action=f"anchor:{ledger_name}",
            evidence_refs=[claimed],
            scope=ledger_name,
            content={"ledger": ledger_name, "summary": body,
                     "payload_hash": claimed},
        )

    @staticmethod
    def seal_payload(payload_without_hash):
        """Helper sibling ledgers use to compute a valid payload_hash."""
        body = {k: v for k, v in payload_without_hash.items()
                if k != "payload_hash"}
        sealed = dict(body)
        sealed["payload_hash"] = _sha256_hex(_canonical(body))
        return sealed

    # ---- verification -------------------------------------------------

    def _expected_hash(self, receipt):
        body = {
            "seq": receipt.seq, "timestamp": receipt.timestamp,
            "actor": receipt.actor, "kind": receipt.kind,
            "action": receipt.action,
            "evidence_refs": list(receipt.evidence_refs),
            "scope": receipt.scope, "content": receipt.content,
            "links": list(receipt.links), "prev_hash": receipt.prev_hash,
        }
        return _sha256_hex(_canonical(body))

    def verify_chain(self):
        """Walk the whole chain. Returns (ok, break_seq, detail)."""
        prev = GENESIS_PREV
        for r in self._entries:
            if r.seq != self._entries.index(r) + 1:
                return (False, r.seq, "DUPLICATE_OR_GAPPED_SEQUENCE")
            if r.prev_hash != prev:
                return (False, r.seq, "PREV_HASH_MISMATCH")
            if self._expected_hash(r) != r.entry_hash:
                return (False, r.seq, "ENTRY_HASH_MISMATCH")
            prev = r.entry_hash
        return (True, None, f"{len(self._entries)} entries verified")

    def verify_receipt(self, seq):
        r = self.get(seq)
        return r is not None and self._expected_hash(r) == r.entry_hash

    # ---- query surface ------------------------------------------------

    def get(self, seq):
        if 1 <= seq <= len(self._entries):
            return self._entries[seq - 1]
        return None

    def by_actor(self, actor):
        return [r for r in self._entries if r.actor == actor]

    def by_kind(self, kind):
        return [r for r in self._entries if r.kind == kind]

    def by_time_range(self, start_iso, end_iso):
        return [r for r in self._entries
                if start_iso <= r.timestamp <= end_iso]

    def causal_chain(self, seq):
        """All receipts transitively linked from seq (following links)."""
        root = self.get(seq)
        if root is None:
            return []
        seen = []
        stack = [root]
        while stack:
            r = stack.pop()
            if r.seq in seen:
                continue
            seen.append(r.seq)
            for lh in r.links:
                linked = self._by_hash.get(lh)
                if linked is not None:
                    stack.append(linked)
        return [self.get(s) for s in sorted(seen)]

    @property
    def head_hash(self):
        return self._entries[-1].entry_hash if self._entries else GENESIS_PREV

    @property
    def head_seq(self):
        return len(self._entries)

    # ---- persistence (append-only discipline) --------------------------

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            for r in self._entries:
                f.write(json.dumps(r.to_dict(), sort_keys=True) + "\n")

    @classmethod
    def load(cls, path):
        """Load and verify. A broken chain raises LedgerError — never
        silently accepted."""
        ledger = cls()
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                receipt = Receipt(
                    seq=d["seq"], timestamp=d["timestamp"], actor=d["actor"],
                    kind=d["kind"], action=d["action"],
                    evidence_refs=tuple(d.get("evidence_refs", ())),
                    scope=d.get("scope", ""), content=d.get("content", {}),
                    links=tuple(d.get("links", ())),
                    prev_hash=d["prev_hash"], entry_hash=d["entry_hash"])
                # Sequence continuity is enforced by the chain check, but a
                # duplicated seq in the file is an immediate refusal.
                if any(e.seq == receipt.seq for e in ledger._entries):
                    raise LedgerError("DUPLICATE_SEQUENCE",
                                      f"seq {receipt.seq} appears twice")
                ledger._entries.append(receipt)
                ledger._by_hash[receipt.entry_hash] = receipt
        ok, break_seq, detail = ledger.verify_chain()
        if not ok:
            raise LedgerError("CHAIN_BREAK",
                              f"chain broken at seq {break_seq}: {detail}")
        return ledger

    # ---- living surface -------------------------------------------------

    def render_surface(self, path, title="Living Ledger — collective record"):
        """Write a self-contained HTML page: every receipt with its
        evidence, chain status, and client-side filters. No external
        dependencies. Regenerate to keep it live."""
        ok, break_seq, detail = self.verify_chain()
        rows = []
        for r in self._entries:
            refs = ", ".join(r.evidence_refs) if r.evidence_refs else "—"
            rows.append(
                f"<tr data-actor='{r.actor}' data-kind='{r.kind}'>"
                f"<td>{r.seq}</td><td>{r.timestamp}</td><td>{r.actor}</td>"
                f"<td>{r.kind}</td><td>{r.action}</td>"
                f"<td class='refs'>{refs}</td><td>{r.scope}</td>"
                f"<td class='hash'>{r.entry_hash[:12]}…</td></tr>")
        status = ("CHAIN OK — " + detail) if ok else (
            f"CHAIN BROKEN at seq {break_seq}: {detail}")
        status_cls = "ok" if ok else "broken"
        html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<style>
body{{font-family:system-ui,sans-serif;margin:2em;background:#0b0f14;color:#e6edf3}}
.banner{{padding:1em;border-radius:8px;margin-bottom:1em}}
.ok{{background:#0f2a1a;border:1px solid #2ea043}}
.broken{{background:#2a0f0f;border:1px solid #f85149}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid #30363d;padding:6px 8px;text-align:left;vertical-align:top}}
th{{background:#161b22}} .hash{{font-family:monospace}} .refs{{max-width:280px;overflow-wrap:anywhere}}
.filters{{margin:1em 0}} input,select{{margin-right:1em;padding:4px 8px}}
.note{{color:#8b949e;font-size:12px;margin-top:1em}}
</style></head><body>
<h1>{title}</h1>
<div class="banner {status_cls}">{status} · head seq {self.head_seq} ·
head hash <span class="hash">{self.head_hash[:16]}…</span></div>
<div class="filters">
<label>actor <input id="fActor" placeholder="filter actor"></label>
<label>kind <select id="fKind"><option value="">all</option>
{"".join(f"<option>{k}</option>" for k in KINDS)}</select></label>
</div>
<table><thead><tr><th>seq</th><th>timestamp</th><th>actor</th><th>kind</th>
<th>action</th><th>evidence refs</th><th>scope</th><th>hash</th></tr></thead>
<tbody id="rows">
{chr(10).join(rows)}
</tbody></table>
<div class="note">Regenerate this page from the ledger to keep it live.
It proves a chained record exists with the stated content; truth of the
content is the sibling ledgers' job.</div>
<script>
const rows=[...document.querySelectorAll('#rows tr')];
function apply(){{const a=fActor.value,k=fKind.value;
rows.forEach(r=>{{r.style.display=
(!a||r.dataset.actor.includes(a))&&(!k||r.dataset.kind===k)?'':'none'}})}}
fActor.oninput=apply;fKind.onchange=apply;
</script></body></html>"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return path
