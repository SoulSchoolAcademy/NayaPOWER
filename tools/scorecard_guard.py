"""L577 write-path guard — no score renders or writes without a measured_at.

Shawn's charge, 2026-10-21 (comment 6306413833): "don't create it" — a
claimed point is a void point. The alignment audit's Senses-100 bar
(6306383248): every headline score is computed by the judge from
evidence AND carries measured_at; zero pinned constants anywhere in
state files.

This module is the enforcement: every path that writes or renders a
scorecard report goes through `guard()` first. A report without a
valid measured_at is refused — in plain words, never silently, never
defaulted. Unmeasured is not zero, it is not low: it is REFUSED.

measured_at shape: ISO-8601 UTC, e.g. "2026-10-21T02:50:00Z".
"""

import datetime
import json
import os

GUARD_VERSION = "L577/1.0"

_MEASURED_AT_RE = __import__("re").compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


class UnmeasuredRefusal(Exception):
    """Raised when a score is offered to the write path without a valid
    measured_at. Plain words, per the judge's own convention: refusal is
    a sentence, never a traceback-foraging exercise."""


def stamp(report):
    """Stamp a score_work report with its computation time. Idempotent:
    an existing valid measured_at is never overwritten — re-stamping
    would be a new computation, and a new computation says so."""
    if not isinstance(report, dict):
        raise TypeError("L577: stamp expects the score_work report dict")
    if is_valid(report.get("measured_at")):
        return report
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    report["measured_at"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return report


def is_valid(measured_at):
    """True only for a well-formed ISO-8601 UTC timestamp string."""
    if not isinstance(measured_at, str):
        return False
    if not _MEASURED_AT_RE.match(measured_at):
        return False
    try:
        datetime.datetime.strptime(measured_at, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False


def check(report):
    """Fail-closed legibility check: returns (ok: bool, message: str)."""
    if not isinstance(report, dict):
        return False, ("L577 REFUSED: not a scorecard report — the write "
                       "path accepts only the judge's report dict")
    mat = report.get("measured_at")
    if not mat:
        return False, ("L577 REFUSED: this score has no measured_at — it "
                       "was not measured, it was asserted. A claimed "
                       "point is a void point; refusing to write it.")
    if not is_valid(mat):
        return False, ("L577 REFUSED: measured_at %r is not a valid "
                       "ISO-8601 UTC timestamp — refusing to write a "
                       "score whose measurement time cannot be read."
                       % (mat,))
    return True, "L577 OK: measured_at %s" % mat


def guard(report):
    """The write-path gate. Returns the report unchanged when its
    measured_at is valid; raises UnmeasuredRefusal (plain words) when
    it is not. Call this before EVERY write or render of a score."""
    ok, message = check(report)
    if not ok:
        raise UnmeasuredRefusal(message)
    return report


def render(report, renderer):
    """Render through the guard: the renderer callable is invoked only
    when the report's measured_at is valid. An unmeasured score is
    refused — nothing renders."""
    guard(report)
    return renderer(report)


def write(path, report):
    """Write the report JSON to path through the guard. The write is
    atomic-ish (temp file + rename) so a refused score never leaves a
    half-written file behind. Byte-verifiable by the caller."""
    guard(report)
    tmp = path + ".l577tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
        fh.write("\n")
    os.replace(tmp, path)
    return path
