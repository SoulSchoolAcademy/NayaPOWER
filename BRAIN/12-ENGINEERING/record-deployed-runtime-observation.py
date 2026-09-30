#!/usr/bin/env python3
"""Record a deployed-runtime observation from a REAL runtime response.

The observation is EVIDENCE, not a claim. This script exists so that both CI and a
human operator produce an observation the same way, from an actual response file,
and never by hand.

NEVER hand-write evidence/deployed-runtime-observation.json. An observation that
was not observed is worse than no observation at all, because it gets trusted.

Usage:
  python BRAIN/12-ENGINEERING/record-deployed-runtime-observation.py \
      <runtime-response.json> [output.json]

The response file must be the unmodified output of an actual runtime call. The
script records the sha256 of that file, the commit the checkout is at, and the
runtime's own `deployed_source_revision` verbatim - including the sentinel
UNSTAMPED, which is reported rather than quietly normalised away.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO / "evidence" / "deployed-runtime-observation.json"
UNSTAMPED = "UNSTAMPED"


def head_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(REPO), capture_output=True, text=True
    ).stdout.strip()


def main(argv: list) -> int:
    if len(argv) not in (2, 3):
        print(__doc__)
        return 2
    response_path = Path(argv[1]).resolve()
    out = Path(argv[2]).resolve() if len(argv) == 3 else DEFAULT_OUT

    if not response_path.exists():
        print(f"error: no such runtime response file: {response_path}")
        print("Refusing to invent one. Capture a real response first.")
        return 2

    raw = response_path.read_bytes()
    document = json.loads(raw.decode("utf-8"))

    if "receipt" not in document:
        print(f"error: {response_path.name} has no 'receipt' object; it is not a CONNECT runtime response")
        return 2

    revision = document.get("deployed_source_revision")
    stamped = revision is not None and revision != UNSTAMPED

    observation = {
        "function": "nayanet-cold-runtime-proof",
        "mode": "connect",
        "canonical_commit_observed": head_commit(),
        "observed_at": document.get("verified_at") or "recorded-at-record-time",
        "provenance": (
            "Recorded by BRAIN/12-ENGINEERING/record-deployed-runtime-observation.py from an "
            f"unmodified runtime response file ({response_path.name}). This entry is regenerated, "
            "never hand-edited."
        ),
        "observation_quality": (
            "COMPLETE - the full runtime response document, recorded programmatically from the file "
            "the runtime actually produced. Not a transcription."
        ),
        "artifact_digest_sha256": hashlib.sha256(raw).hexdigest(),
        "deployed_source_revision_reported_by_runtime": revision,
        "deployed_revision_is_stamped": stamped,
        "observed_document": document,
        "how_to_refresh": (
            "Capture a real runtime response, then re-run this script. Never hand-write this file."
        ),
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(observation, indent=2) + "\n", encoding="utf-8")

    print(f"recorded observation -> {out.relative_to(REPO).as_posix() if out.is_relative_to(REPO) else out}")
    print(f"  canonical commit  : {observation['canonical_commit_observed'][:8]}")
    print(f"  runtime reports   : {revision}")
    print(f"  stamped           : {stamped}")
    if not stamped:
        print("  NOTE: the deployed artifact does not report a real revision. Parity is UNDECIDABLE")
        print("        until an authorized operator stamps DEPLOYED_SOURCE_REVISION and redeploys.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
