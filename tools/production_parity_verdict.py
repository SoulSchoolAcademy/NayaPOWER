"""Durable production-parity verdicts for the governed production promotion chain.

The deploy workflow stamps the promoted source SHA into the deployed
function sources (``const DEPLOYED_SOURCE_REVISION = "<40-hex>";``) and
promotes the stamped commit to the ``production`` branch
(.github/workflows/governed-supabase-production-deploy.yml,
"Build provenance-stamped production deployment commit"). The standing
policy gates promotion on stamp freshness, but nothing *records* the
parity verdict as durable evidence: proving "production runs the
promoted SHA" today requires re-deriving it from the production branch
by hand.

This module builds the complementary artifact: a parity verdict receipt
that binds the promoted source SHA, the production branch tip, and the
revision stamp read from each deployed function source, and reduces
them to a machine-verifiable verdict per function plus an overall
verdict. It is signal-only: it certifies nothing about promotion and
authorizes nothing.

Design rules (SN-0526 quality bar):
- Never raises on missing or malformed inputs. Unknown state is recorded
  as UNKNOWN with a reason, never invented.
- Never weakens a gate: the strongest claim this module can emit is
  PARITY_VERIFIED, and only when the observed stamp byte-equals the
  promoted SHA. STALE (production behind tip) is the expected steady
  state after main moves; DRIFT (stamp not an ancestor of the promoted
  SHA) is the alarming one.
- Pure function of its inputs: no IO, no environment reads, no git
  calls. The workflow step does IO (fetch production branch, read the
  stamped sources, test ancestry) and passes parsed mappings in.

Verdict taxonomy (per deployed function):
- PARITY_VERIFIED: stamp is 40-hex and equals the promoted SHA.
- STALE: stamp is 40-hex, differs from the promoted SHA, and is an
  ancestor of it (production runs an older promoted revision).
- DRIFT: stamp is 40-hex, differs, and is NOT an ancestor (production
  runs something the chain never promoted).
- UNSTAMPED: the deployed source still carries the UNSTAMPED sentinel.
- UNKNOWN: stamp missing/malformed, promoted SHA unknown, or ancestry
  could not be determined.

Overall verdict: the most severe per-function verdict, severity order
DRIFT > UNSTAMPED > UNKNOWN > STALE > PARITY_VERIFIED. No functions
observed -> UNKNOWN.

Schema: NAYAPOWER_PRODUCTION_PARITY_VERDICT_V1
"""

from __future__ import annotations

import re
from typing import Any, Mapping

SCHEMA = "NAYAPOWER_PRODUCTION_PARITY_VERDICT_V1"

# (verdict key, deployed source path on the production branch) for every
# function whose deployed copy carries the DEPLOYED_SOURCE_REVISION stamp.
# Mirrors the stamp-write step of governed-supabase-production-deploy.yml;
# that step owns the list, this module only records what was observed.
STAMPED_FUNCTIONS = (
    (
        "nayanet-cold-runtime-proof",
        "supabase/functions/nayanet-cold-runtime-proof/index.ts",
    ),
    (
        "nayanet-verified-ai-action",
        "supabase/functions/nayanet-verified-ai-action/index.ts",
    ),
)

STAMP_RE = re.compile(r'const DEPLOYED_SOURCE_REVISION = "([0-9a-f]{40}|UNSTAMPED)";')
UNSTAMPED_SENTINEL = "UNSTAMPED"

# Worst verdict first.
SEVERITY = ("DRIFT", "UNSTAMPED", "UNKNOWN", "STALE", "PARITY_VERIFIED")

_HEX40 = re.compile(r"\A[0-9a-f]{40}\Z")


def _is_hex40(value: Any) -> bool:
    return isinstance(value, str) and _HEX40.match(value) is not None


def extract_stamp(source_text: Any) -> str | None:
    """Extract the DEPLOYED_SOURCE_REVISION stamp from a deployed source.

    Returns the 40-hex SHA, the UNSTAMPED sentinel, or None when the
    source is missing or carries no recognizable stamp. Never raises.
    """
    try:
        if not isinstance(source_text, str):
            return None
        match = STAMP_RE.search(source_text)
        return match.group(1) if match else None
    except Exception:
        return None


def evaluate_function(
    stamp: Any,
    promoted_sha: Any,
    stamp_is_ancestor_of_promoted: Any,
) -> dict[str, Any]:
    """Reduce one deployed function's observed stamp to a verdict.

    Never raises; every non-verdict outcome is UNKNOWN with a reason.
    """
    if stamp == UNSTAMPED_SENTINEL:
        return {
            "verdict": "UNSTAMPED",
            "stamp": stamp,
            "reason": "DEPLOYED_SOURCE_NEVER_STAMPED",
        }
    if not isinstance(stamp, str) or not _is_hex40(stamp):
        return {
            "verdict": "UNKNOWN",
            "stamp": stamp if isinstance(stamp, str) else None,
            "reason": "STAMP_NOT_READ" if stamp is None else "STAMP_MALFORMED",
        }
    if not _is_hex40(promoted_sha):
        return {
            "verdict": "UNKNOWN",
            "stamp": stamp,
            "reason": "PROMOTED_SHA_UNKNOWN",
        }
    if stamp == promoted_sha:
        return {
            "verdict": "PARITY_VERIFIED",
            "stamp": stamp,
            "reason": "STAMP_EQUALS_PROMOTED_SHA",
        }
    if stamp_is_ancestor_of_promoted is True:
        return {
            "verdict": "STALE",
            "stamp": stamp,
            "reason": "STAMP_IS_ANCESTOR_OF_PROMOTED_SHA",
        }
    if stamp_is_ancestor_of_promoted is False:
        return {
            "verdict": "DRIFT",
            "stamp": stamp,
            "reason": "STAMP_NOT_ANCESTOR_OF_PROMOTED_SHA",
        }
    return {
        "verdict": "UNKNOWN",
        "stamp": stamp,
        "reason": "ANCESTRY_UNAVAILABLE",
    }


def _overall_verdict(evaluations: Mapping[str, dict[str, Any]]) -> str:
    worst = "PARITY_VERIFIED"
    worst_rank = len(SEVERITY) - 1
    for evaluation in evaluations.values():
        try:
            rank = SEVERITY.index(evaluation.get("verdict"))
        except (ValueError, AttributeError):
            rank = SEVERITY.index("UNKNOWN")
        if rank < worst_rank:
            worst_rank = rank
            worst = SEVERITY[rank]
    return worst


def build_parity_verdict(
    promoted_sha: Any = None,
    production_tip_sha: Any = None,
    functions: Any = None,
    context: Any = None,
) -> dict[str, Any]:
    """Build the production parity verdict receipt. Never raises.

    `functions` maps function key -> {"stamp": ..., "source_path": ...,
    "stamp_is_ancestor_of_promoted": bool|None}. Every input is treated
    as untrusted observation: malformed entries degrade to UNKNOWN, they
    never raise and never flip a verdict toward PARITY_VERIFIED.
    """
    try:
        evaluations: dict[str, dict[str, Any]] = {}
        observed = functions if isinstance(functions, Mapping) else {}
        for key, entry in observed.items():
            try:
                name = str(key)
                info = entry if isinstance(entry, Mapping) else {}
                evaluations[name] = evaluate_function(
                    stamp=info.get("stamp"),
                    promoted_sha=promoted_sha,
                    stamp_is_ancestor_of_promoted=info.get(
                        "stamp_is_ancestor_of_promoted"
                    ),
                )
                source_path = info.get("source_path")
                if isinstance(source_path, str) and source_path:
                    evaluations[name]["source_path"] = source_path
            except Exception:
                evaluations[name] = {
                    "verdict": "UNKNOWN",
                    "stamp": None,
                    "reason": "EVALUATION_FAILED",
                }
        if not evaluations:
            overall = "UNKNOWN"
            overall_reason = "NO_FUNCTIONS_OBSERVED"
        else:
            overall = _overall_verdict(evaluations)
            overall_reason = "WORST_PER_FUNCTION_VERDICT"
        receipt: dict[str, Any] = {
            "schema": SCHEMA,
            "verdict": overall,
            "verdict_reason": overall_reason,
            "promoted_sha": promoted_sha if _is_hex40(promoted_sha) else None,
            "promoted_sha_invalid": (
                None if _is_hex40(promoted_sha) else promoted_sha
            ),
            "production_tip_sha": (
                production_tip_sha if _is_hex40(production_tip_sha) else None
            ),
            "functions": evaluations,
            "authority_boundary": {
                "certifies_promotion": False,
                "authorizes_deployment": False,
                "signal_only": True,
                "note": (
                    "This receipt records observed revision evidence. "
                    "Promotion authority remains exclusively with the "
                    "governed deploy workflow's standing-policy gate and "
                    "Shawn's explicit deploy authorization."
                ),
            },
        }
        if isinstance(context, Mapping):
            receipt["context"] = {
                str(k): v for k, v in context.items() if isinstance(v, (str, int, bool)) or v is None
            }
        return receipt
    except Exception as exc:  # absolute fail-closed floor: never raise
        return {
            "schema": SCHEMA,
            "verdict": "UNKNOWN",
            "verdict_reason": "BUILDER_FAILED",
            "error": str(exc)[:200],
            "promoted_sha": None,
            "promoted_sha_invalid": None,
            "production_tip_sha": None,
            "functions": {},
            "authority_boundary": {
                "certifies_promotion": False,
                "authorizes_deployment": False,
                "signal_only": True,
            },
        }
