#!/usr/bin/env python3
"""
Triage a scorer disagreement: reader variance vs rubric ambiguity.

LEARN lesson, distilled to code (Battery D verdict 2026-10-12 + rubric-sharpening
probe folded 2026-10-12 ~09:19Z):

    The TR-8DB748/M1 disagreement (primary=1, scorer-2=0) first looked like a
    rubric defect. A preregistered probe re-tested the same item with 3 fresh
    cold readers under the FROZEN Battery D rubric (R-D, verbatim). They
    converged unanimously, and a sharpened rubric (R-SHARP) showed NO-DELTA
    (18/18 vs 18/18 -- ceiling effect, not equivalence). The original split was
    single-scorer reader variance, not systematic rubric ambiguity.

Reframed lesson: triage scorer disagreements as READER VARIANCE FIRST -- re-test
with fresh cold readers under the existing frozen rubric -- before assuming
rubric ambiguity and rewriting the instrument.

This module makes that triage mechanical:

    record = DisagreementRecord(item_id="TR-8DB748", cell="M1", ...)
    verdict = triage_disagreement(record, reader_fn, n_readers=3)

Step 1: spawn fresh cold readers under the FROZEN existing rubric.
  - If the disagreement dissolves (fresh readers unanimous) -> READER_VARIANCE:
    no instrument change, evidence recorded. The item is NOT re-graded.
  - If the disagreement persists (fresh readers still split) ->
    RUBRIC_REVIEW: escalate with the full evidence pack.

Machine-enforced boundaries (what the software CAN guarantee):
  * The rubric is never edited during triage: the record must carry a rubric
    sha256 that matches a frozen-rubric registration; a mismatch is a hard
    error, not a warning.
  * Information isolation: the reader seam receives ONLY the item text and the
    frozen rubric -- never the original votes, never a variant rubric.
  * A record that is not a genuine disagreement (<2 distinct valid votes) is
    refused: there is nothing to triage.

What this module CANNOT guarantee (caller's operational duty, D32):
  * The coldness of the readers themselves (new sessions, blind ids, sealed
    assignment, no cross-contact) -- that lives in the battery harness, not here.
  * READER_VARIANCE does not prove the rubric is perfect. It means THIS
    incident gives no evidence of a rubric defect. Readers can share blind
    spots; the verdict is recorded as probabilistic evidence, not proof.
  * This module does not grade items, does not rewrite rubrics, and does not
    spawn real model readers. The `reader_fn` seam is the injection point for
    the real harness; `--replay` mode replays recorded votes deterministically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

SCHEMA_VERSION = "triage_disagreement/v1"

READER_VARIANCE = "READER_VARIANCE"
RUBRIC_REVIEW = "RUBRIC_REVIEW"

VALID_VOTES = (0, 1)
NA_VOTE = "na"


class TriageError(Exception):
    """Raised when a disagreement record cannot be triaged."""


# --------------------------------------------------------------------------
# Frozen rubric registry: rubrics are instruments; instruments don't change
# mid-measurement. Registration is explicit and append-only for a run.
# --------------------------------------------------------------------------

_frozen: dict[str, str] = {}


def register_frozen_rubric(rubric_id: str, rubric_text: str) -> str:
    """Register a rubric version as frozen. Returns its sha256.

    Idempotent for identical text. Re-registering the same id with DIFFERENT
    text raises TriageError: an instrument must not change mid-measurement,
    and a silent swap is worse than a loud refusal."""
    sha = hashlib.sha256(rubric_text.encode("utf-8")).hexdigest()
    existing = _frozen.get(rubric_id)
    if existing is not None and existing != sha:
        raise TriageError(
            f"rubric {rubric_id!r} already frozen with a different sha "
            f"({existing[:16]}... vs {sha[:16]}...): refusing silent "
            "instrument swap; freeze a NEW rubric version instead"
        )
    _frozen[rubric_id] = sha
    return sha


def frozen_sha(rubric_id: str) -> str | None:
    return _frozen.get(rubric_id)


def clear_frozen_rubrics() -> None:
    _frozen.clear()


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------

@dataclass
class Vote:
    reader_id: str
    vote: int | str  # 0 | 1 | "na"
    note: str = ""

    def valid(self) -> bool:
        return self.vote in VALID_VOTES


@dataclass
class ReadRequest:
    """What a fresh cold reader receives. Deliberately minimal:

    item text + frozen rubric + blind id. No original votes. No variant
    rubric. No trial purpose. Anything else is contamination."""

    item_id: str
    cell: str
    item_text: str
    rubric_id: str
    rubric_text: str
    blind_reader_id: str


@dataclass
class DisagreementRecord:
    item_id: str
    cell: str
    rubric_id: str
    rubric_sha256: str
    votes: list[Vote] = field(default_factory=list)

    def distinct_valid_votes(self) -> set[int]:
        return {v.vote for v in self.votes if v.valid()}

    def validate(self) -> None:
        if not self.votes:
            raise TriageError("record has no votes: nothing to triage")
        if len(self.distinct_valid_votes()) < 2:
            raise TriageError(
                f"record {self.item_id}/{self.cell} is not a genuine disagreement "
                f"(distinct valid votes: {sorted(self.distinct_valid_votes())}); "
                "refusing to triage unanimity"
            )
        expected = frozen_sha(self.rubric_id)
        if expected is None:
            raise TriageError(
                f"rubric {self.rubric_id!r} is not registered as frozen: "
                "triage requires a frozen instrument"
            )
        if expected != self.rubric_sha256:
            raise TriageError(
                f"rubric sha mismatch for {self.rubric_id!r}: record carries "
                f"{self.rubric_sha256[:16]}..., frozen registry has "
                f"{expected[:16]}... -- refusing to triage against an "
                "unfrozen/drifted rubric"
            )


@dataclass
class TriageVerdict:
    verdict: str  # READER_VARIANCE | RUBRIC_REVIEW
    item_id: str
    cell: str
    rubric_id: str
    rubric_sha256: str
    n_readers: int
    original_votes: list[dict]
    fresh_votes: list[dict]
    fresh_unanimous: bool
    evidence: dict
    schema_version: str = SCHEMA_VERSION
    decided_utc: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


def append_ledger(ledger_path: str, verdict: TriageVerdict) -> None:
    """Append a verdict to an append-only JSONL ledger. If it's not in the
    ledger, the triage didn't happen -- LEARN compounds only what is recorded."""
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(verdict.to_json().replace("\n", " ") + "\n")


# --------------------------------------------------------------------------
# The triage
# --------------------------------------------------------------------------

def triage_disagreement(
    record: DisagreementRecord,
    reader_fn,
    *,
    n_readers: int = 3,
    item_text: str = "",
    rubric_text: str = "",
    evidence_extra: dict | None = None,
) -> TriageVerdict:
    """Run the variance-first triage on one disagreement record.

    reader_fn: callable(ReadRequest) -> Vote. Must perform a genuinely cold
    read of the item under the frozen rubric. The function receives NO
    information about the original votes.
    """
    if n_readers < 2:
        raise TriageError("need at least 2 fresh readers for a re-read")
    record.validate()

    fresh: list[Vote] = []
    for i in range(n_readers):
        req = ReadRequest(
            item_id=record.item_id,
            cell=record.cell,
            item_text=item_text,
            rubric_id=record.rubric_id,
            rubric_text=rubric_text,
            blind_reader_id=f"FRESH-{i + 1:03d}",
        )
        vote = reader_fn(req)
        if not isinstance(vote, Vote):
            raise TriageError(f"reader_fn must return a Vote, got {type(vote)!r}")
        if vote.vote not in VALID_VOTES and vote.vote != NA_VOTE:
            raise TriageError(
                f"fresh reader {vote.reader_id!r} returned invalid vote "
                f"{vote.vote!r}: garbage in is not ambiguity; refusing to "
                "fold it into the triage"
            )
        fresh.append(vote)

    fresh_valid = [v.vote for v in fresh if v.valid()]
    # "na" from a fresh reader means the metric did not apply to their read:
    # convergence is impossible on a binary cell, so this is a split.
    unanimous = len(fresh_valid) == n_readers and len(set(fresh_valid)) == 1

    original_votes = [asdict(v) for v in record.votes]
    fresh_votes = [asdict(v) for v in fresh]

    if unanimous:
        verdict = READER_VARIANCE
        evidence = {
            "classification": READER_VARIANCE,
            "instrument_change": None,
            "reason": (
                f"{n_readers}/{n_readers} fresh cold readers converged under the "
                f"frozen rubric {record.rubric_id}; the original split "
                f"({', '.join(f'{v.reader_id}={v.vote}' for v in record.votes if v.valid())}) "
                "is attributed to single-scorer reader variance, not rubric ambiguity."
            ),
            "confidence_note": (
                "Unanimity among N independent fresh readers is strong evidence, "
                "not proof: the strength of the evidence scales with N, and "
                "readers can share blind spots. Per the Uncertainty Principle "
                "this verdict is a calibrated probability judgment, recorded "
                "with its evidence -- not a certainty."
            ),
            "no_regrade_performed": True,
            "regrade_note": (
                "The unanimous fresh read resolves the TRIAGE question only; "
                "the item's score of record is unchanged (Battery D convention: "
                "disagreements are recorded, not re-graded)."
            ),
        }
    else:
        verdict = RUBRIC_REVIEW
        split_pattern: dict[str, list[str]] = {}
        for v in list(record.votes) + fresh:
            split_pattern.setdefault(str(v.vote), []).append(v.reader_id)
        evidence = {
            "classification": RUBRIC_REVIEW,
            "reason": (
                "Disagreement PERSISTED across independent fresh cold readers: "
                "fresh votes were not unanimous. Reader variance alone cannot "
                "explain the split; the rubric text for this cell is a candidate "
                "cause and needs human review."
            ),
            "confidence_note": (
                "The escalation is the conservative call: with fresh readers "
                "still split, the evidence cannot distinguish rubric ambiguity "
                "from correlated reader error. Human review decides."
            ),
            "split_pattern": split_pattern,
            "no_regrade_performed": True,
            "reviewer_instructions": (
                "1. Read the item text against the frozen rubric cell verbatim. "
                "2. Decide whether the rubric cell text admits both readings; if "
                "so, sharpen the cell text WITHOUT changing its letter, freeze a "
                "new rubric version, and re-run the affected cells as a fresh "
                "preregistered battery (never re-grade sealed items in place). "
                "3. If the rubric text is unambiguous and the split is reader "
                "error, record that finding and re-train readers, not the rubric."
            ),
        }

    if evidence_extra:
        evidence.update(evidence_extra)

    return TriageVerdict(
        verdict=verdict,
        item_id=record.item_id,
        cell=record.cell,
        rubric_id=record.rubric_id,
        rubric_sha256=record.rubric_sha256,
        n_readers=n_readers,
        original_votes=original_votes,
        fresh_votes=fresh_votes,
        fresh_unanimous=unanimous,
        evidence=evidence,
        decided_utc=datetime.now(timezone.utc).isoformat(),
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _load_record(path: str) -> tuple[DisagreementRecord, str, str]:
    raw = json.load(open(path))
    rec = raw["record"]
    votes = [Vote(**v) for v in rec["votes"]]
    return (
        DisagreementRecord(
            item_id=rec["item_id"],
            cell=rec["cell"],
            rubric_id=rec["rubric_id"],
            rubric_sha256=rec["rubric_sha256"],
            votes=votes,
        ),
        raw.get("item_text", ""),
        raw.get("rubric_text", ""),
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Triage a scorer disagreement: reader variance first, "
        "rubric review only if the disagreement survives a cold re-read."
    )
    ap.add_argument("--record", required=True,
                    help="JSON file: {record: {item_id, cell, rubric_id, "
                    "rubric_sha256, votes: [{reader_id, vote, note}]}, "
                    "item_text?, rubric_text?}")
    ap.add_argument("--replay", required=True,
                    help="JSON file with a list of fresh votes to replay "
                    "deterministically: [{reader_id, vote, note}]. Use the "
                    "dry-run script for the real Battery D case.")
    ap.add_argument("--out", default="",
                    help="Write the verdict JSON here (default: stdout).")
    ap.add_argument("--ledger", default="",
                    help="Append the verdict to this JSONL ledger file "
                    "(append-only; if it's not in the ledger, the triage "
                    "didn't happen).")
    ap.add_argument("--register-rubric", action="store_true",
                    help="Register the record file's rubric_text as frozen "
                    "before triaging (convenience for dry runs; production "
                    "harnesses register instruments separately).")
    args = ap.parse_args(argv)

    record, item_text, rubric_text = _load_record(args.record)
    if args.register_rubric:
        sha = register_frozen_rubric(record.rubric_id, rubric_text)
        # Fixture records carry a placeholder sha; the registered frozen
        # text is the instrument of record for dry runs.
        if record.rubric_sha256.startswith("<"):
            record.rubric_sha256 = sha
        elif sha != record.rubric_sha256:
            print(f"error: record's rubric sha does not match the registered "
                  f"text ({sha[:16]}...); refusing", file=sys.stderr)
            return 2

    fresh_votes = [Vote(**v) for v in json.load(open(args.replay))]
    it = iter(fresh_votes)

    def replay_reader(req: ReadRequest) -> Vote:
        try:
            return next(it)
        except StopIteration:
            raise TriageError("replay file exhausted: need one vote per reader")

    try:
        verdict = triage_disagreement(
            record, replay_reader,
            n_readers=len(fresh_votes),
            item_text=item_text, rubric_text=rubric_text,
        )
    except TriageError as e:
        print(f"TRIAGE REFUSED: {e}", file=sys.stderr)
        return 1

    out = verdict.to_json()
    if args.out:
        open(args.out, "w").write(out + "\n")
    else:
        print(out)
    if args.ledger:
        append_ledger(args.ledger, verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
