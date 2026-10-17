#!/usr/bin/env python3
"""Trigger-chain jurisdiction gate (GOVERN wave 31 — Keeper).

Closes the #2020/#2152 bypass class: jurisdiction analysis must follow the
TRIGGER CHAIN, not just the file list.

The #2020 incident: a PR whose file list said "one benign learn-capture JSON"
merged under low jurisdiction, but its trigger chain —
`.naya/capture/**` push-to-main -> live-intelligence-commit-proof
(mints OIDC identity, invokes the LIVE runtime, contents:write)
-> live-supabase-runtime-proof —
executed production-consequential actions no file-list review had covered.

What this enforces (mechanically, from LIVE workflow bytes at the tree under
test — never a cached copy):
  1. Compute, for the changed paths, every workflow that WOULD fire on push
     to main (branch filter + paths/paths-ignore), plus transitive
     `workflow_run` descendants.
  2. Only CHANGE-SPECIFIC chains count: path-filtered push triggers and their
     descendants. Every-push workflows (kernel-tests, cvo-runtime-proof,
     ...) are the standing ratified pipeline — they fire regardless of the
     change's files, so they cannot be a jurisdiction bypass.
  3. If any change-specific chain link is production-consequential, the change
     BLOCKS unless a deploy-authorization marker covers every chained path.
     The scorer verifies the marker's quoted human authorization against the
     board; the gate makes the consequence impossible to merge silently.

Exit codes: 0 = PASS, 1 = BLOCK (fail closed), 2 = tool error (fail closed).
"""

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REPO = "SoulSchoolAcademy/NayaPOWER"
WORKFLOWS_DIR = ".github/workflows"
AUTH_MARKER_PATH = ".github/trigger-chain-deploy-authorization.json"
MANIFEST_PATH = "tools/trigger_chain_jurisdiction_manifest.machine.json"

# Curated production-consequence classification, keyed by workflow FILE.
# Each entry was read from the live workflow bytes (evidence strings cite the
# exact mechanism). The freshness test (T4) fails closed if any listed file's
# bytes change without re-curation — trigger changes always get a human
# jurisdiction review.
CURATED = {
    # file: (production_consequential, evidence)
    "live-intelligence-commit-proof.yml": (
        True,
        "push(main, paths .naya/capture/**): fresh-lesson job mints GitHub OIDC "
        "runtime identity (ACTIONS_ID_TOKEN_REQUEST_URL) and POSTs to the live "
        "Supabase runtime function; permissions contents:write; workflow_run "
        "descendant live-supabase-runtime-proof executes live "
        "runtime too. No fail-closed precondition on the push path "
        "(only a head_commit.message dedup guard).",
        None,
    ),
    "live-supabase-runtime-proof.yml": (
        True,
        "CHAINED via workflow_run on 'Live Intelligence Commit Proof': mints "
        "OIDC runtime identities and executes cold Naya runtime / CONNECT "
        "runtime / causal experiments against the live runtime. Authorized via "
        "the root workflow's deploy authorization.",
        None,
    ),
    "live-law-proof.yml": (
        False,
        "path-triggered on law-runtime paths, but its jobs only POST "
        "read-only modes (evaluate, verify_existing_action) to the runtime — "
        "authorization evaluation, no commit/deploy/ref writes.",
        None,
    ),
    "live-act-proof.yml": (
        False,
        "path-triggered on act/law/know runtime paths, but the consequential "
        "job (law-to-act, mode:execute naya_node_apply) is gated on "
        "needs.preflight.outputs.eligible == 'true' (fail-closed preflight); "
        "the unconditional job (independent-act-verification) only inspects / "
        "rereads (mode:inspect-plan, reread) — no state-changing runtime call.",
        None,
    ),
    "current-truth-resolver.yml": (
        False,
        "path-triggered on BRAIN/** etc.: collects GitHub evidence, resolves "
        "truth locally, publishes to the job summary. No live-runtime invoke, "
        "no ref writes.",
        None,
    ),
    "doc-completeness-gate.yml": (
        False,
        "path-triggered on .naya/capture/** + BRAIN/01-GOVERNANCE/**: read-only "
        "completeness check. No OIDC mint, no runtime invoke.",
        None,
    ),
    "governed-supabase-production-deploy.yml": (
        True,
        "UNFILTERED push-to-main: on push (not only dispatch) it takes "
        "PROMOTION_MODE=STANDING_POLICY and can auto-promote main->production "
        "under the ratified standing policy (step 'Enforce ratified standing "
        "policy before automatic promotion' asserts RATIFIED status, then "
        "promotes subject to preconditions). Production-consequential; "
        "unfiltered, so it is standing pipeline rather than change-specific.",
        {
            "status": "RATIFIED",
            "authority": "HUMAN_DIRECTOR",
            "record": ".naya/governance/STANDING-PRODUCTION-PROMOTION-V1.json",
            "ratified_at": "2026-09-29",
            "basis": (
                "STANDING-PRODUCTION-PROMOTION-V1: status RATIFIED, authority "
                "HUMAN_DIRECTOR, constitutional amendment "
                "STANDING-PRODUCTION-AUTHORIZATION-AMENDMENT-V1; automatic "
                "execution true, fail_mode FAIL_CLOSED on unmet preconditions."
            ),
        },
    ),
    "live-verified-ai-action-proof.yml": (
        False,
        "fires on every push to main (standing pipeline) AND its consequential "
        "jobs (authorized-action, authority-absent-refusal, idempotency) are "
        "gated on needs.preflight.outputs.eligible == 'true' — skipped by "
        "design unless parity-eligible. GATED.",
        None,
    ),
    "live-cvo-runtime-proof.yml": (
        True,
        "UNFILTERED push-to-main: on EVERY main push the cvo-runtime job mints "
        "a GitHub OIDC runtime identity and POSTs {\"mode\":\"cvo\"} to the LIVE "
        "Supabase runtime, asserting production_action_executed is True "
        "(live bytes lines 24-63). Production-consequential by the same bar "
        "as live-intelligence-commit-proof; unfiltered, so it is standing "
        "pipeline rather than change-specific.",
        {
            "status": "PLACEMENT_ONLY",
            "authority": "HUMAN_DIRECTOR",
            "basis": (
                "Workflow placed by the human director's manual click under "
                "the standing human-only-workflows law; the on-push live-"
                "runtime execution is in the placed bytes. Standing operation "
                "under the NayaPOWER Operation Protocol (Shawn, 2026-10-11). "
                "No separate ratification document for the standing "
                "production execution was found in-tree as of 2026-10-12."
            ),
        },
    ),
    # --- standing-pipeline (unfiltered push-to-main) workflows: curated so
    # the class cannot silently grow. All verified 2026-10-12 from live
    # bytes: zero OIDC mints, zero live-runtime invokes, zero write
    # permissions, zero ref writes.
    "collective-chain-readiness-gate.yml": (
        False,
        "unfiltered push-to-main (standing pipeline): readiness check only; "
        "no OIDC mint, no runtime invoke, no writes (verified live bytes).",
        None,
    ),
    "design-gate.yml": (
        False,
        "unfiltered push-to-main (standing pipeline): design check only; "
        "no OIDC mint, no runtime invoke, no writes (verified live bytes).",
        None,
    ),
    "kernel-tests.yml": (
        False,
        "unfiltered push-to-main (standing pipeline): runs node --test and "
        "pytest; no OIDC mint, no runtime invoke, no writes (verified live "
        "bytes). This is the workflow that executes the pytest gate below.",
        None,
    ),
    "protocol-gates.yml": (
        False,
        "unfiltered push-to-main (standing pipeline): protocol checks; "
        "no OIDC mint, no runtime invoke, no writes (verified live bytes).",
        None,
    ),
    "ratified-guard.yml": (
        False,
        "unfiltered push-to-main (standing pipeline): ratified-object "
        "deletion guard; no OIDC mint, no runtime invoke, no writes "
        "(verified live bytes).",
        None,
    ),
    "safety-grant-gate.yml": (
        False,
        "unfiltered push-to-main (standing pipeline): anonymous-grant "
        "allowlist check; no OIDC mint, no runtime invoke, no writes "
        "(verified live bytes).",
        None,
    ),
    "spec-integrity.yml": (
        False,
        "unfiltered push-to-main (standing pipeline): spec pin check; "
        "no OIDC mint, no runtime invoke, no writes (verified live bytes).",
        None,
    ),
    "trigger-chain-jurisdiction.yml": (
        False,
        "unfiltered push-to-main (standing pipeline): this gate itself — "
        "runs the trigger-chain script read-only and fails the check on "
        "BLOCK. No OIDC mint, no runtime invoke, no writes (verified live "
        "bytes 2026-10-12).",
        None,
    ),
}


def repo_root(tree):
    if tree:
        return os.path.abspath(tree)
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except Exception:
        here = os.path.abspath(os.path.dirname(__file__))
        return os.path.abspath(os.path.join(here, "..", ".."))


def github_glob_to_regex(pattern):
    """Translate a GitHub `paths`/`branches` glob to a regex.

    GitHub semantics: `*` matches anything except `/`; `**` matches across
    `/` (including zero segments); `?` matches one char except `/`;
    `[...]` character classes (incl. `[!...]` negation) match one char
    except `/`. A pattern without `/` matches the basename at any depth.
    """
    if "/" not in pattern.rstrip("/"):
        pattern = "**/" + pattern
    i, n, out = 0, len(pattern), []
    while i < n:
        c = pattern[i]
        if c == "*":
            if i + 1 < n and pattern[i + 1] == "*":
                # consume any trailing slash after **
                j = i + 2
                slash = j < n and pattern[j] == "/"
                if slash:
                    j += 1
                out.append("(?:.*/)?" if slash else ".*")
                i = j
            else:
                out.append("[^/]*")
                i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        elif c == "[":
            j = pattern.find("]", i + 1)
            if j == -1:
                out.append("\\[")
                i += 1
            else:
                cls = pattern[i + 1:j]
                if cls[:1] in ("!", "^"):
                    # negated: also exclude `/` (GitHub classes never cross /)
                    out.append("[^/" + cls[1:] + "]")
                else:
                    # positive: lookahead keeps `/` out without touching `^`
                    out.append("(?![/])[" + cls + "]")
                i = j + 1
        elif c in ".+()|^${}\\":
            out.append("\\" + c)
            i += 1
        else:
            out.append(c)
            i += 1
    return re.compile("^" + "".join(out) + "$")


def path_matches_any(path, patterns):
    return any(github_glob_to_regex(p).match(path) for p in (patterns or []))


def load_workflows(root):
    """Parse every workflow file from LIVE bytes. Returns {file: info}."""
    if yaml is None:
        raise RuntimeError("pyyaml is required")
    wf_dir = os.path.join(root, WORKFLOWS_DIR)
    out = {}
    for fname in sorted(os.listdir(wf_dir)):
        if not fname.endswith((".yml", ".yaml")):
            continue
        fpath = os.path.join(wf_dir, fname)
        with open(fpath, "rb") as f:
            raw = f.read()
        sha = hashlib.sha256(raw).hexdigest()
        try:
            doc = yaml.safe_load(raw.decode("utf-8"))
        except Exception as e:  # fail closed on unparseable workflow
            raise RuntimeError(f"cannot parse {fname}: {e}")
        on = (doc.get(True) if isinstance(doc, dict) else None) or (
            doc.get("on") if isinstance(doc, dict) else None
        ) or {}
        # List-form `on: [push, ...]` cannot carry path filters; treat a bare
        # push as an unfiltered trigger (standing pipeline, never
        # change-specific). Dict-form is handled below.
        list_push = isinstance(on, list) and "push" in on
        push = on.get("push") if isinstance(on, dict) else None
        wfr = on.get("workflow_run") if isinstance(on, dict) else None
        info = {
            "file": fname,
            "sha256": sha,
            "name": (doc.get("name") if isinstance(doc, dict) else None) or fname,
            "push_main": False,
            "push_paths": None,  # None = every push (no path filter)
            "push_paths_ignore": None,
            "workflow_run_parents": [],
        }
        if isinstance(push, dict):
            branches = push.get("branches") or []
            branches_ignore = push.get("branches-ignore") or []
            if isinstance(branches, str):
                branches = [branches]
            if isinstance(branches_ignore, str):
                branches_ignore = [branches_ignore]
            # GitHub: `push:` with no `branches` key fires on ALL branches,
            # including main. Fail closed toward modeled, never toward silent.
            branch_filter = "branches" in push
            info["push_main"] = (
                not branch_filter
                or any(path_matches_any("main", [b]) for b in branches)
            ) and not path_matches_any("main", branches_ignore)
            paths = push.get("paths")
            if isinstance(paths, str):
                paths = [paths]
            paths_ignore = push.get("paths-ignore")
            if isinstance(paths_ignore, str):
                paths_ignore = [paths_ignore]
            info["push_paths"] = paths
            info["push_paths_ignore"] = paths_ignore
        elif push is True or list_push:
            info["push_main"] = True
        if isinstance(wfr, dict):
            parents = wfr.get("workflows") or []
            info["workflow_run_parents"] = (
                parents if isinstance(parents, list) else [parents]
            )
        out[fname] = info
    return out


def change_specific_chains(changed_paths, workflows):
    """Map each changed path -> directly-triggered (path-filtered) workflows.

    Only path-filtered push-to-main triggers are change-specific. Unfiltered
    push triggers are the standing pipeline (fire for every change) and are
    excluded — they cannot smuggle change-specific jurisdiction.
    """
    hits = {}
    for path in changed_paths:
        matched = []
        for fname, wf in workflows.items():
            if not wf["push_main"]:
                continue
            if wf["push_paths"] is None:
                continue  # standing pipeline, not change-specific
            if wf["push_paths_ignore"] and path_matches_any(
                path, wf["push_paths_ignore"]
            ):
                continue
            if path_matches_any(path, wf["push_paths"]):
                matched.append(fname)
        if matched:
            hits[path] = sorted(matched)
    return hits


def descendants(roots, workflows):
    """Transitive workflow_run descendants of the root workflow FILES."""
    seen, stack = set(), list(roots)
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        cur_name = workflows[cur]["name"]
        for fname, wf in workflows.items():
            if cur_name in wf["workflow_run_parents"] and fname not in seen:
                stack.append(fname)
    return sorted(seen - set(roots))


def is_production(fname, workflows):
    """Curated classification with a mechanical consistency tripwire."""
    if fname not in CURATED:
        # Unknown workflow with a path-filtered main trigger: fail closed.
        # The freshness test forces curation before CI can go green.
        return None
    return CURATED[fname][0]


def jurisdiction_for(changed_paths, workflows):
    """Full jurisdiction verdict inputs for a set of changed paths."""
    hits = change_specific_chains(changed_paths, workflows)
    roots = sorted({w for ws in hits.values() for w in ws})
    chained = descendants(roots, workflows)
    production_links = []
    unknown = []
    for fname in roots + chained:
        prod = is_production(fname, workflows)
        if prod is None:
            unknown.append(fname)
        elif prod:
            production_links.append(fname)
    chained_paths = [p for p in changed_paths if p in hits and any(
        w in production_links for w in hits[p]
    )]
    return {
        "changed_paths": sorted(changed_paths),
        "direct_triggers": hits,
        "chain_roots": roots,
        "chain_descendants": chained,
        "production_links": sorted(production_links),
        "unknown_workflows": sorted(unknown),
        "production_chained_paths": sorted(chained_paths),
        "authorization_required": bool(production_links) or bool(unknown),
    }


def validate_auth_marker(marker, production_paths, pr_author=None):
    """Validate the deploy-authorization marker. Returns (ok, reasons).

    The marker rides WITH the change, so the PR author cannot authorize
    themselves: when pr_author is known, authorized_by == pr_author BLOCKs.
    The merge seat must still verify the quoted human authorization against
    the board receipt — the gate makes silent merges impossible, the seat
    makes forged ones pointless.
    """
    reasons = []
    if not isinstance(marker, dict):
        return False, ["marker is not a JSON object"]
    for field in ("authorized_paths", "board_receipt", "authorized_by"):
        if not marker.get(field):
            reasons.append(f"missing required field: {field}")
    paths = marker.get("authorized_paths") or []
    if not isinstance(paths, list) or not paths:
        reasons.append("authorized_paths must be a non-empty list of globs")
    else:
        uncovered = [
            p for p in production_paths if not path_matches_any(p, paths)
        ]
        if uncovered:
            reasons.append(
                "authorized_paths do not cover production-chained paths: "
                + ", ".join(uncovered)
            )
    receipt = marker.get("board_receipt") or ""
    if not re.match(
        r"^https://github\.com/SoulSchoolAcademy/NayaPOWER/(issues|pull)/\d+"
        r"#issuecomment-\d+$",
        receipt,
    ):
        reasons.append(
            "board_receipt must be a comment-anchored "
            "github.com/SoulSchoolAcademy/NayaPOWER issue/PR URL "
            "(#issuecomment-N) — the specific human utterance, not a thread"
        )
    authorized_by = (marker.get("authorized_by") or "").strip().lower()
    if pr_author and authorized_by and authorized_by == pr_author.strip().lower():
        reasons.append(
            f"self-authorization: authorized_by == PR author ({pr_author}); "
            "production authorization must come from a different seat "
            "(the human director)"
        )
    return (not reasons), reasons


def verdict(changed_paths, workflows, auth_marker, pr_author=None):
    jur = jurisdiction_for(changed_paths, workflows)
    report = dict(jur)
    if not jur["authorization_required"]:
        report["verdict"] = "PASS"
        report["reason"] = (
            "no change-specific production-consequential chain; "
            "standing pipeline only"
        )
        return 0, report
    if jur["unknown_workflows"]:
        report["verdict"] = "BLOCK"
        report["reason"] = (
            "unclassified workflow(s) in the change-specific chain "
            "(fail closed): " + ", ".join(jur["unknown_workflows"])
        )
        return 1, report
    if auth_marker is None:
        report["verdict"] = "BLOCK"
        report["reason"] = (
            "change-specific production-consequential chain without a "
            f"deploy-authorization marker ({AUTH_MARKER_PATH}): "
            + ", ".join(jur["production_links"])
        )
        return 1, report
    ok, reasons = validate_auth_marker(
        auth_marker, jur["production_chained_paths"], pr_author
    )
    if not ok:
        report["verdict"] = "BLOCK"
        report["reason"] = "deploy-authorization marker invalid: " + "; ".join(reasons)
        report["marker_problems"] = reasons
        return 1, report
    report["verdict"] = "PASS"
    report["reason"] = (
        "deploy-authorization marker covers all production-chained paths; "
        "the merge seat must still verify the quoted human authorization "
        "against the board receipt before merging"
    )
    report["marker"] = {
        k: auth_marker.get(k)
        for k in ("authorized_paths", "board_receipt", "authorized_by")
    }
    return 0, report


def diff_paths(root, base_ref, head_ref):
    rev_range = base_ref if not head_ref else f"{base_ref}..{head_ref}"
    out = subprocess.run(
        ["git", "-C", root, "diff", "--name-only", rev_range],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"git diff failed: {out.stderr.strip()}")
    return [l for l in out.stdout.splitlines() if l.strip()]


def emit_manifest(workflows, existing=None):
    """Build the checked-in classification manifest.

    existing: previously checked-in manifest (dict) — reviewed_at is carried
    per file ONLY when the sha is unchanged; a sha change resets reviewed_at
    to None so the freshness test forces an explicit human re-curation.
    """
    existing_wf = (existing or {}).get("workflows", {})
    manifest = {
        "version": 2,
        "generated_by": "tools/trigger_chain_jurisdiction.py --emit-manifest",
        "repo": REPO,
        "field_semantics": {
            "production_consequential": (
                "Property of the WORKFLOW, independent of trigger shape: True "
                "iff the workflow, when triggered, executes "
                "production-consequential actions (OIDC-minted live-runtime "
                "invocation, production ref writes, production promotion)."
            ),
            "change_specific": (
                "True iff the workflow has a path-filtered push-to-main "
                "trigger: its firing is attributable to the changed files, "
                "so its production consequences are the change's jurisdiction."
            ),
            "standing_ratification": (
                "Required when a workflow is production_consequential AND "
                "fires on unfiltered push-to-main (standing pipeline): the "
                "recorded authority for its standing production execution. "
                "status=RATIFIED (ratification document in-tree) or "
                "PLACEMENT_ONLY (director-placed bytes, no separate "
                "ratification document found — explicit, reviewable). "
                "workflow_run-only production workflows inherit authorization "
                "from their change-specific chain root."
            ),
            "reviewed_at": (
                "Date a human last reviewed this file's classification "
                "against its exact bytes (sha256). Reset to null by "
                "--emit-manifest whenever the bytes change."
            ),
        },
        "rule": (
            "change-specific = path-filtered push-to-main triggers + "
            "workflow_run descendants; every-push workflows are the standing "
            "pipeline and cannot smuggle jurisdiction. Two enforcement layers: "
            "(1) the verdict gates each change's change-specific production "
            "chain; (2) the manifest curates EVERY push-to-main workflow, so "
            "the class cannot silently grow — an unfiltered production "
            "workflow without a standing_ratification record fails the "
            "freshness test. pull_request_target triggers are a different "
            "trigger class (PR-time, base-repo context with secrets) and are "
            "out of scope for this push-to-main gate."
        ),
        "workflows": {},
    }
    for fname in sorted(workflows):
        wf = workflows[fname]
        curated = CURATED.get(fname)
        prev = existing_wf.get(fname, {})
        reviewed_at = (
            prev.get("reviewed_at")
            if prev.get("sha256") == wf["sha256"]
            else None
        )
        manifest["workflows"][fname] = {
            "sha256": wf["sha256"],
            "workflow_name": wf["name"],
            "push_main": wf["push_main"],
            "push_path_filters": wf["push_paths"],
            "workflow_run_parents": wf["workflow_run_parents"],
            "change_specific": wf["push_main"] and wf["push_paths"] is not None,
            "production_consequential": curated[0] if curated else None,
            "evidence": curated[1] if curated else (
                "UNCLASSIFIED — curate before CI can pass"
            ),
            "standing_ratification": curated[2] if curated else None,
            "reviewed_at": reviewed_at,
        }
    return manifest


def main(argv=None):
    ap = argparse.ArgumentParser(description="Trigger-chain jurisdiction gate")
    ap.add_argument("--tree", default=None)
    ap.add_argument("--base-ref", default=None)
    ap.add_argument("--head-ref", default="HEAD",
                    help="empty string = working tree (git diff <base>)")
    ap.add_argument("--paths-file", default=None,
                    help="newline-separated changed paths (instead of git diff)")
    ap.add_argument("--auth-file", default=None,
                    help="path to a deploy-authorization marker JSON to evaluate")
    ap.add_argument("--pr-author", default=None,
                    help="login of the PR author (CI: github.event.pull_request.user.login); "
                         "a marker naming the author as authorized_by is rejected")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--emit-manifest", action="store_true")
    args = ap.parse_args(argv)

    try:
        root = repo_root(args.tree)
        workflows = load_workflows(root)
    except Exception as e:
        print(f"TRIGGER-CHAIN-GATE ERROR: {e}", file=sys.stderr)
        return 2

    if args.emit_manifest:
        existing = None
        mpath = os.path.join(root, MANIFEST_PATH)
        if os.path.exists(mpath):
            try:
                with open(mpath) as f:
                    existing = json.load(f)
            except Exception:
                existing = None
        print(json.dumps(emit_manifest(workflows, existing),
                         indent=2, sort_keys=True))
        return 0

    try:
        if args.paths_file:
            with open(args.paths_file) as f:
                changed = [l.strip() for l in f if l.strip()]
        elif args.base_ref:
            changed = diff_paths(root, args.base_ref, args.head_ref)
        else:
            changed = []
    except Exception as e:
        print(f"TRIGGER-CHAIN-GATE ERROR: {e}", file=sys.stderr)
        return 2

    auth_marker = None
    if args.auth_file:
        try:
            with open(args.auth_file) as f:
                auth_marker = json.load(f)
        except Exception as e:
            print(f"TRIGGER-CHAIN-GATE ERROR: bad auth file: {e}", file=sys.stderr)
            return 2
    else:
        # The marker authorizes only when it rides WITH the change under review.
        marker_in_diff = AUTH_MARKER_PATH in changed
        if marker_in_diff:
            mpath = os.path.join(root, AUTH_MARKER_PATH)
            if os.path.exists(mpath):
                try:
                    with open(mpath) as f:
                        auth_marker = json.load(f)
                except Exception:
                    auth_marker = "UNREADABLE"

    if auth_marker == "UNREADABLE":
        print("TRIGGER-CHAIN-GATE BLOCK: authorization marker is not valid JSON",
              file=sys.stderr)
        return 1

    code, report = verdict(changed, workflows, auth_marker,
                           pr_author=args.pr_author)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"TRIGGER-CHAIN-GATE {report['verdict']}: {report['reason']}")
        if report.get("production_links"):
            prod_roots = [r for r in report["chain_roots"]
                          if r in report["production_links"]]
            prod_desc = [d for d in report["chain_descendants"]
                         if d in report["production_links"]]
            chain = prod_roots + (["..."] if prod_desc else []) + prod_desc
            print("  production chain: " + " -> ".join(chain))
    return code


if __name__ == "__main__":
    sys.exit(main())
