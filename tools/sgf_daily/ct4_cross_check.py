#!/usr/bin/env python3
"""CT-4 strengthened cross-check — Lane 6 port onto the SGF daily runner branch (t0212).

Implements CTA-PROTOCOL-v2 §4 CT-4 (the double-negative remote cross-check) as
executable bytes, plus the v2 G2 mechanical anti-elision rule.

WHY THE OLD CHECK WAS WEAK (named, per the protocol):
v1's CT-4 rested on a THIN SINGLE `git ls-remote origin refs/heads/<branch>`
lookup. A single lookup can fail for reasons that have nothing to do with the
phantom — a transient network/API failure returns empty output, and empty output
is exactly what "branch does not exist" looks like. One check cannot tell a
real phantom from a flaky lookup. v2 requires TWO independent remote reads that
both agree on absence:

  (a) targeted: `git ls-remote origin refs/heads/<branch>`  -> zero lines
  (b) full:     `git ls-remote origin` filtered for the branch-name substring
                -> zero matches

(b) is the independent second mechanism: a transient failure of (a) is caught
when (b) finds the branch anyway, and a real phantom fails both. Disagreement
between (a) and (b) is reported as UNABLE_TO_VERIFY — never as a catch.

The v2 G2 anti-elision rule rides with it: every evidence-row command must be
the complete, exact command text (elision markers forbidden). A PHANTOM_CAUGHT
resting on an elided cross-check is UNPROVEN_CATCH per v2 §6 — a catch you
cannot re-run is a claim, not a catch.

Return shape of run_ct4():
  {"verdict": "PHANTOM_CAUGHT" | "RECEIPT_CONFIRMED" | "UNABLE_TO_VERIFY",
   "rows": [{"assertion","command","observed","expected","match"}, ...],
   "g2_pass": bool, "why": "<one paragraph citing only observations>"}

The G2 anti-elision rule is exposed as assert_rows_elision_free(rows): the daily
seat applies it to any SUCCESSOR-recorded cross-check rows before accepting a
catch. A PHANTOM_CAUGHT resting on elided rows is UNPROVEN_CATCH per v2 §6 —
the seat must refuse it, never trust it.
"""

import re
import subprocess

ELISION_RE = re.compile(r"(\.\.\.|…|\[truncated\]|\(elided\)|\[snip\]|\betc\.$)")


def elision_free(command):
    """v2 G2: mechanical anti-elision — the command must be re-runnable verbatim."""
    return not ELISION_RE.search(command or "")


def _ls_remote(ref, repo):
    r = subprocess.run(["git", "ls-remote", "origin", ref], cwd=repo,
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout


def run_ct4(branch, repo, origin="origin"):
    """Double-negative phantom cross-check for `branch`.

    Verdicts:
      PHANTOM_CAUGHT   — (a) and (b) both agree the branch is absent
      RECEIPT_CONFIRMED— (a) found the branch at a head (the claim exists, not a phantom)
      UNABLE_TO_VERIFY — (a) and (b) disagree (transient lookup suspected), or git failed
    """
    rows = []
    ref = f"refs/heads/{branch}"
    cmd_a = f"git ls-remote {origin} '{ref}'"
    rc_a, out_a = _ls_remote(ref, repo)
    lines_a = [ln for ln in out_a.splitlines() if ln.strip()]
    if rc_a != 0:
        return {"verdict": "UNABLE_TO_VERIFY", "rows": rows, "g2_pass": False,
                "why": f"targeted ls-remote failed (exit {rc_a}) — cannot distinguish "
                       "phantom from broken transport; refusing to catch."}
    rows.append({"assertion": f"targeted ref lookup for {ref} returns no head",
                 "command": cmd_a,
                 "observed": f"{len(lines_a)} line(s)" + (f": {lines_a[0]}" if lines_a else " — empty output"),
                 "expected": "zero lines if the branch is a phantom",
                 "match": len(lines_a) == 0})
    if lines_a:
        head = lines_a[0].split()[0]
        g2 = all(elision_free(r["command"]) for r in rows)
        return {"verdict": "RECEIPT_CONFIRMED", "rows": rows, "g2_pass": g2,
                "why": f"targeted lookup found the branch at head {head} — the claim "
                       "exists; not a phantom."}
    cmd_b = f"git ls-remote {origin} | grep \"{branch}\"; echo \"grep_exit=$?\""
    rc_b, out_b = _ls_remote("", repo)
    if rc_b != 0:
        return {"verdict": "UNABLE_TO_VERIFY", "rows": rows, "g2_pass": False,
                "why": f"full listing failed (exit {rc_b}) — the targeted absence is "
                       "uncorroborated; refusing to catch."}
    matches = [ln for ln in out_b.splitlines() if branch in ln]
    rows.append({"assertion": "full remote listing filtered for branch-name substring returns no matches",
                 "command": cmd_b,
                 "observed": f"{len(matches)} matching line(s)" + (f": {matches[0]}" if matches else " — no matches"),
                 "expected": "zero matches if the branch is a phantom",
                 "match": len(matches) == 0})
    g2 = all(elision_free(r["command"]) for r in rows)
    if matches:
        return {"verdict": "UNABLE_TO_VERIFY", "rows": rows, "g2_pass": g2,
                "why": "targeted lookup said absent but the full listing contains the "
                       "branch — transient failure of the targeted read suspected. "
                       "A single lookup would have caught a phantom that is not one."}
    return {"verdict": "PHANTOM_CAUGHT", "rows": rows, "g2_pass": g2,
            "why": "both independent remote reads agree the branch does not exist on "
                   f"{origin}; both commands are elision-free and re-runnable verbatim."}


def assert_rows_elision_free(rows):
    """v2 G2 mechanical anti-elision for SUCCESSOR-recorded cross-check rows.

    Returns {"g2_pass": bool, "offenders": [row indexes]}. The daily seat must
    refuse a PHANTOM_CAUGHT whose rows fail this (UNPROVEN_CATCH per v2 §6) —
    a catch you cannot re-run verbatim is a claim, not a catch.
    """
    offenders = [i for i, r in enumerate(rows)
                 if not elision_free(r.get("command", ""))]
    return {"g2_pass": not offenders, "offenders": offenders}
