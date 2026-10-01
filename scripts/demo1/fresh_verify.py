#!/usr/bin/env python3
"""Demo-1 fresh VERIFY: independently confirm what ACT did.

This script runs in a FRESH process. It inherits nothing from the act
run — no in-memory objects, no shared state. It reads ONLY:

  1. the persisted execution receipt JSON, and
  2. the artifact file on disk, plus the canonical Smart Door registry.

Three SEPARATE verdicts (a later revocation does not erase a valid
historical observation, but it does prevent unauthorized reuse —
historical verification must never be mistaken for fresh permission):

  VERDICT 1 — receipt integrity: the receipt_hash recomputes.
  VERDICT 2 — historical outcome verification: the receipt's OWN tool
      binding resolves to exactly one declared operation in the
      canonical registry (re-read from disk); the bound version matches
      the declaration; the artifact exists and its sha256 equals the hash
      bound in effects_observed; the parameters commitment, decision
      reference, and EXECUTED path are present. Semantic validation
      runs even when the hash matches — a freshly resealed
      contradictory receipt cannot pass on hash equality alone.
  VERDICT 3 — current authorization for another action: resolve the
      referenced DECISION receipt and the CURRENT grant file — never the
      execution receipt's frozen authority_basis, which is history, not
      permission. The basis kind must satisfy the tool's required_authority,
      the live grant must match the decision's basis ref, not be revoked,
      and be fresh against the real clock (typed, tz-aware). Missing
      dependencies yield UNKNOWN; failed authority yields FAIL (fail
      closed). A V3 PASS means the grant is live — it does NOT authorize
      reuse of this receipt; a new action needs a fresh LAW decision.

Usage:
    python3 scripts/demo1/fresh_verify.py <receipt-json> [--grant-path PATH]
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from naya_kernel import smart_door
from naya_kernel.nodes import act_node


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    grant_path = REPO_ROOT / "scripts" / "demo1" / "demo_grant.json"
    rest = []
    i = 0
    while i < len(argv):
        if argv[i] == "--grant-path" and i + 1 < len(argv):
            grant_path = Path(argv[i + 1])
            i += 2
        else:
            rest.append(argv[i])
            i += 1
    if len(rest) != 1:
        print("usage: fresh_verify.py <receipt-json> [--grant-path PATH]",
              file=sys.stderr)
        return 2
    receipt_path = Path(rest[0])
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    # Per-verdict failure collectors and unknown-dependency collectors.
    # Exit 0 iff V1 and V2 pass — the historical verification. V3 answers
    # the separate question "is another action authorized now?" and never
    # affects the exit code; its verdict is explicit in the output.
    failures = {"V1": [], "V2": [], "V3": []}
    unknown = {"V1": [], "V2": [], "V3": []}

    def chk(bucket: str, name: str, cond: bool, detail: str = ""):
        print(("PASS " if cond else "FAIL ") + f"[{bucket}] " + name
              + (f" — {detail}" if detail and not cond else ""))
        if not cond:
            failures[bucket].append(name)
        return cond

    def unk(bucket: str, name: str, detail: str = ""):
        print("UNKNOWN [" + bucket + "] " + name
              + (f" — {detail}" if detail else ""))
        unknown[bucket].append(name)

    # ---- VERDICT 1 — receipt integrity ---------------------------------
    body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    chk("V1", "receipt_hash recomputes",
        act_node._sha256(body) == receipt.get("receipt_hash"),
        "MISMATCH — receipt does not recompute")

    # ---- VERDICT 2 — historical outcome verification -------------------
    # The tool comes from THE RECEIPT's own binding, never a hardcoded name.
    tool = receipt.get("tool") or {}
    tool_id = tool.get("tool_id")
    tool_version = tool.get("version")
    chk("V2", "receipt binds a tool_id", isinstance(tool_id, str) and tool_id,
        f"tool={tool!r}")

    reg = smart_door.load_registry()
    door = op = None
    if isinstance(tool_id, str) and tool_id:
        try:
            door, op = smart_door.find_operation_any_door(reg, tool_id)
        except KeyError as exc:
            door = op = None
            decl_err = str(exc)
        else:
            decl_err = ""
    else:
        decl_err = "no tool_id bound"
    chk("V2", "receipt tool is declared in the canonical registry",
        op is not None, decl_err or f"tool_id={tool_id!r}")

    entry = None
    if op is not None:
        entry = smart_door.project_act_tool_entry(
            door, op, registry_version=reg.get("version", "1.0"))
        chk("V2", "receipt version matches the declared version",
            tool_version == entry["version"],
            f"receipt={tool_version!r} declared={entry['version']!r}")
        chk("V2", "registry status is honest (not production-live)",
            door.get("status") == "REGISTERED_DEMO",
            f"status={door.get('status')!r}")
        chk("V2", "verification_required",
            op.get("verification_required") is True)

    # Parameters commitment: params_hash well-formed + artifact re-read.
    params_hash = receipt.get("params_hash")
    chk("V2", "params_hash committed",
        isinstance(params_hash, str) and bool(re.fullmatch(r"[0-9a-f]{64}",
                                                           params_hash)),
        f"params_hash={params_hash!r}")
    chk("V2", "decision_ref present",
        isinstance(receipt.get("decision_ref"), str)
        and bool(receipt.get("decision_ref")),
        f"decision_ref={receipt.get('decision_ref')!r}")
    chk("V2", "execution path was EXECUTED",
        receipt.get("path") == "EXECUTED", f"path={receipt.get('path')!r}")
    # Semantic validation beyond hash equality: an EXECUTED receipt whose
    # own authority_basis claims revoked=True is contradictory — ACT §4.2
    # refuses revoked bases, so no honest execution can produce it. This is
    # about the receipt's story cohering with the admission rules, not
    # about current authorization (that's V3's separate question).
    chk("V2", "authority basis not revoked at execution time",
        (receipt.get("authority_basis") or {}).get("revoked") is not True,
        "EXECUTED with a revoked authority basis is contradictory — "
        "ACT §4.2 would have refused it")

    effects = str(receipt.get("effects_observed", ""))
    m = re.search(r"demo-staging/(\S+\.md)", effects)
    h = re.search(r"sha256:([0-9a-f]{64})", effects)
    chk("V2", "receipt binds an artifact + sha256", bool(m and h),
        f"effects_observed={effects!r}")
    if m and h:
        demo_staging = receipt_path.parent.parent
        artifact = demo_staging / m.group(1)
        chk("V2", "artifact filename matches the declared pattern",
            entry is None or bool(
                re.match(r"^sn-candidate-[A-Za-z0-9][A-Za-z0-9_-]*\.md$",
                         m.group(1))),
            f"filename={m.group(1)!r}")
        chk("V2", "artifact exists on disk", artifact.is_file(),
            str(artifact))
        if artifact.is_file():
            actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
            chk("V2", "artifact sha256 matches receipt binding",
                actual == h.group(1),
                f"receipt={h.group(1)[:12]}… disk={actual[:12]}…")

    # ---- VERDICT 3 — current authorization for another action ----------
    # V3 answers ONLY "is another action authorized NOW?" It resolves the
    # referenced DECISION receipt and the CURRENT grant file — never the
    # execution receipt's frozen authority_basis, which is history, not
    # permission. A historical receipt stays valid after the grant lapses;
    # it can never authorize another action. Missing dependencies yield
    # UNKNOWN; failed authority yields FAIL (fail closed). A V3 PASS means
    # the grant is live — it does NOT authorize reuse of this receipt.
    decision_ref = receipt.get("decision_ref")
    decision = None
    if isinstance(decision_ref, str) and decision_ref:
        candidate = receipt_path.parent / f"decision-{decision_ref}.json"
        if candidate.is_file():
            try:
                decision = json.loads(candidate.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                unk("V3", "decision receipt unreadable", str(exc))
        else:
            unk("V3", "decision receipt not found",
                f"{candidate.name} — cannot resolve current authority")
    else:
        unk("V3", "no decision_ref bound",
            "cannot resolve the authorizing decision")

    if decision is not None:
        basis = decision.get("authority_basis") or {}
        if entry is not None:
            chk("V3", "authority basis kind satisfies required_authority",
                basis.get("kind") == entry["required_authority"],
                f"basis={basis.get('kind')!r} "
                f"required={entry['required_authority']!r}")
        else:
            chk("V3", "authority basis kind satisfies required_authority",
                False,
                "tool not declared — no authority requirement to satisfy")

        grant = None
        if grant_path.is_file():
            try:
                grant = json.loads(grant_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                chk("V3", "current grant readable", False, str(exc))
        else:
            chk("V3", "current grant file present", False,
                f"{grant_path} absent — no current authority evidence; "
                "fail closed")
        if grant is not None:
            chk("V3", "current grant matches the decision's basis ref",
                grant.get("grant_ref") == basis.get("ref"),
                f"grant={grant.get('grant_ref')!r} "
                f"basis ref={basis.get('ref')!r}")
            chk("V3", "current grant not revoked",
                grant.get("revoked") is not True,
                f"grant {grant.get('grant_ref')!r} is revoked — "
                "no new action is authorized")
            exp_moment = act_node._parse_moment(grant.get("expiry"))
            now_real = datetime.now(timezone.utc)
            if exp_moment is None:
                chk("V3", "grant expiry is a tz-aware ISO-8601 moment",
                    False,
                    f"expiry={grant.get('expiry')!r} — fail closed, "
                    "never unlimited")
            else:
                chk("V3", "grant fresh against the real clock",
                    exp_moment > now_real,
                    f"expiry={grant.get('expiry')!r} "
                    f"now={now_real.isoformat()}")

    print()
    verdict_state = {}
    for verdict, label in (("V1", "receipt integrity"),
                           ("V2", "historical outcome verification"),
                           ("V3", "current authorization for another action")):
        if failures[verdict]:
            state = "FAIL"
        elif unknown[verdict]:
            state = "UNKNOWN"
        else:
            state = "PASS"
        verdict_state[verdict] = state
        print(f"VERDICT {verdict} ({label}): {state}")
    print()
    print("VERDICTS:", json.dumps(verdict_state, sort_keys=True))
    print()
    historical_ok = (verdict_state["V1"] == "PASS"
                     and verdict_state["V2"] == "PASS")
    if historical_ok:
        print("FRESH VERIFY: PASS — observation confirmed independently.")
    else:
        print("FRESH VERIFY: FAIL — historical proof incomplete; see above.")
    print("V3 NOTE: a V3 PASS means the grant is currently live — it does "
          "NOT authorize reuse of this receipt; a new action needs a fresh "
          "LAW decision. A V3 FAIL means history may stand but no new "
          "action is authorized. A V3 UNKNOWN means current authority "
          "could not be resolved.")
    return 0 if historical_ok else 1


if __name__ == "__main__":
    sys.exit(main())
