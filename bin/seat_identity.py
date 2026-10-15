#!/usr/bin/env python3
"""Seat identity for commit authorship — the t0796 (lane 1, Verity) repair.

Forensics root (2026-10-13/14): push tooling hardcoded the identity it
stamped on API-built commits (`lane-5/push_demote_branch_t0762.py:84-85`
stamped "Naya Clarity Narzan"; `bin/stage_smart_note.py:96` stamped
"Naya 4"; evolve-driver scripts stamped "Naya 4"; `bin/push_branch.py`
stamped nothing, so the API defaulted to the GitHub App identity). The
commit author line is a script default, not the seat — the bytes lied
about who built them, and every future self-review gate (the t0790/t0795
identity-decline discipline) reads that line first.

This module is the single parameterization point: the executing seat
declares itself through the environment, and the commit gets THAT
identity on both author and committer. Fail-closed by design: no
defaults, no silent substitution — an unset seat refuses loudly (exit 2)
instead of stamping a misleading identity, because metadata that
misleads is a silent failure, not a cosmetic one (principle 4).

Usage in push tooling (import via the hidden_files/bin absolute path —
the codebase convention, matching the hardcoded GH/WORK paths):
    import os, sys
    sys.path.insert(0, "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/bin")
    from seat_identity import seat_identity
    ident = seat_identity()          # {"name": ..., "email": ...}; exits 2 if unset
    ...
    api("POST", "/git/commits", {"message": msg, "tree": tree,
                                 "parents": [tip],
                                 "author": ident, "committer": ident})

The dispatcher / executor sets the seat before running push tooling:
    export NAYA_SEAT_NAME="Naya Clarity Verity"
    export NAYA_SEAT_EMAIL="naya4@nayapower.local"
"""
import os
import sys

SEAT_NAME_ENV = "NAYA_SEAT_NAME"
SEAT_EMAIL_ENV = "NAYA_SEAT_EMAIL"


def seat_identity():
    """Return the executing seat's {"name","email"} for commit authorship.

    Reads NAYA_SEAT_NAME / NAYA_SEAT_EMAIL. Fail-closed: exits 2 with a
    loud, actionable message when unset, instead of letting the caller
    fall back to a hardcoded or app-default identity.
    """
    name = os.environ.get(SEAT_NAME_ENV, "").strip()
    email = os.environ.get(SEAT_EMAIL_ENV, "").strip()
    if not name or not email:
        print(
            f"IDENTITY-REFUSED (t0796): {SEAT_NAME_ENV} and {SEAT_EMAIL_ENV} are unset. "
            "Commit author/committer would misattribute authorship. "
            "Set both to the executing seat (e.g. export "
            f'{SEAT_NAME_ENV}="Naya Clarity Verity" {SEAT_EMAIL_ENV}="naya4@nayapower.local") '
            "and re-run. Refusal is the fail-closed path; a default would be a lie.",
            file=sys.stderr,
        )
        sys.exit(2)
    return {"name": name, "email": email}


if __name__ == "__main__":
    import json
    if "--self-test" in sys.argv:
        # Fail-closed probe: unset env must refuse (exit 2), never default.
        import subprocess as _sp
        env = {k: v for k, v in os.environ.items()
               if k not in (SEAT_NAME_ENV, SEAT_EMAIL_ENV)}
        r = _sp.run([sys.executable, __file__], capture_output=True,
                    text=True, env=env)
        ok = r.returncode == 2 and "IDENTITY-REFUSED" in r.stderr
        print(f"self-test fail-closed: {'PASS' if ok else 'FAIL'} "
              f"(exit={r.returncode})")
        # Set probe: identity must round-trip exactly.
        env[SEAT_NAME_ENV] = "Probe Seat (t0796)"
        env[SEAT_EMAIL_ENV] = "probe@nayapower.local"
        r2 = _sp.run([sys.executable, __file__], capture_output=True,
                     text=True, env=env)
        got = json.loads(r2.stdout)
        ok2 = got == {"name": "Probe Seat (t0796)",
                      "email": "probe@nayapower.local"}
        print(f"self-test round-trip: {'PASS' if ok2 else 'FAIL'} ({got})")
        sys.exit(0 if (ok and ok2) else 1)
    print(json.dumps(seat_identity()))
