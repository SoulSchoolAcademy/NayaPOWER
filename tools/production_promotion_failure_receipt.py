"""Durable failure receipts for the governed production promotion chain.

The parent promotion receipt
(.github/workflows/governed-supabase-production-deploy.yml,
"Write durable production promotion receipt") is a fail-closed handshake: it
refuses to certify PROMOTED_AND_PROVEN unless every proof leg succeeded
against the authorized source SHA (see
tests/test_production_promotion_receipt_handshake.py). On the failure path
that handshake step is skipped, so a promoted-but-unproven production
deployment leaves no receipt at all -- the exact path the chain has been
living on (every recent promotion run fails at the runtime-proof dispatch).

This module builds the complementary artifact: a failure receipt that is
ALWAYS writable, records the handshake refusal explicitly, and binds every
available piece of proof evidence (per-leg run ids, conclusions, head SHAs)
to the authorized source and the deployment commit.

Design rules (SN-0526 quality bar):
- Never raises on missing or malformed inputs. Unknown state is recorded as
  UNKNOWN / NOT_EXECUTED, never invented.
- Never weakens the gate: the only success claim this module can emit is
  "UNEXPECTED_ALL_SUCCESS", which flags a miswired call instead of
  certifying a proof. PROMOTED_AND_PROVEN is exclusively the parent
  handshake's claim.
- Pure function of its inputs: no IO, no environment reads. The workflow
  step does IO and passes parsed mappings in.
- Upstream gate evidence is bound, not just proof legs: the standing-policy
  verdict, the promotion denial receipt, and the required workflows' run
  conclusions at the source SHA (read-only GitHub API observations by the
  receipt step). A failed run's receipt therefore names the gate that
  stopped the chain, instead of leaving DEPLOY_FAILED unexplained.

Schema: NAYAPOWER_PRODUCTION_PROMOTION_FAILURE_RECEIPT_V1
"""

SCHEMA = "NAYAPOWER_PRODUCTION_PROMOTION_FAILURE_RECEIPT_V1"

# (leg key, artifact filename written by the deploy workflow's dispatch steps)
PROOF_LEGS = (
    ("producer", "producer-run.json"),
    ("runtime_proof", "proof-run.json"),
    ("act_proof", "act-proof-run.json"),
    ("learning_act_proof", "learning-act-proof-run.json"),
    ("connect_proof", "connect-proof-run.json"),
)

SUPABASE_CHECK_FILE = "supabase-production-check.json"

# Authority note: this list mirrors the required-workflow set in the
# "Enforce ratified standing policy before automatic promotion" step of
# governed-supabase-production-deploy.yml. That step owns the list; this
# module only records what the receipt step observed at failure time.
REQUIRED_WORKFLOWS = ("kernel-tests.yml", "collective-chain-readiness-gate.yml")

VERDICT_FILE = "standing-authorization-verdict.json"
DENIAL_FILE = "production-promotion-denial.json"


def evaluate_leg(run, github_sha):
    """Evaluate one proof leg's recorded run against the authorized source.

    Returns a small status mapping. `run` is the parsed artifact dict or
    None when the dispatch step never produced one.
    """
    if run is None:
        return {"status": "NOT_EXECUTED", "run_id": None}
    if not isinstance(run, dict):
        return {"status": "UNKNOWN", "run_id": None}
    run_id = run.get("databaseId")
    conclusion = run.get("conclusion")
    head_sha = run.get("headSha")
    head_matches = head_sha == github_sha
    if conclusion == "success" and head_matches:
        return {
            "status": "SUCCESS",
            "run_id": run_id,
            "conclusion": conclusion,
            "head_sha": head_sha,
            "head_sha_matches_authorized_source": True,
        }
    if conclusion is not None and conclusion != "success":
        return {
            "status": "FAILED",
            "run_id": run_id,
            "conclusion": conclusion,
            "head_sha": head_sha,
            "head_sha_matches_authorized_source": head_matches,
        }
    if not head_matches:
        return {
            "status": "SOURCE_MISMATCH",
            "run_id": run_id,
            "conclusion": conclusion,
            "head_sha": head_sha,
            "head_sha_matches_authorized_source": False,
        }
    return {
        "status": "UNKNOWN",
        "run_id": run_id,
        "conclusion": conclusion,
        "head_sha": head_sha,
        "head_sha_matches_authorized_source": head_matches,
    }


def evaluate_gate_run(run, github_sha):
    """Evaluate one required workflow's recorded run against the authorized source.

    Unlike proof legs, a gate run is recorded verbatim: the gate's own
    conclusion IS the evidence (the enforcement step, not this module,
    decides what the conclusion means). None means no run was observed;
    malformed means UNKNOWN. Never raises.
    """
    if run is None:
        return {"status": "NOT_EXECUTED", "run_id": None}
    if not isinstance(run, dict):
        return {"status": "UNKNOWN", "run_id": None}
    run_id = run.get("id") or run.get("run_id")
    return {
        "status": "RECORDED",
        "run_id": run_id,
        "run_status": run.get("status"),
        "conclusion": run.get("conclusion"),
        "head_sha": run.get("head_sha"),
        "head_sha_matches_authorized_source": run.get("head_sha") == github_sha,
    }


def evaluate_policy_file(doc):
    """Summarize the standing-policy verdict file. Absent/malformed input is
    recorded as absent, never invented."""
    if not isinstance(doc, dict):
        return {"verdict_file_present": False}
    verdict = doc.get("verdict") if isinstance(doc.get("verdict"), dict) else {}
    return {
        "verdict_file_present": True,
        "policy_id": doc.get("policy_id"),
        "policy_version": doc.get("policy_version"),
        "decision": verdict.get("decision"),
        "reason": verdict.get("reason"),
    }


def evaluate_denial_file(doc):
    """Summarize the promotion denial receipt. Absent/malformed input is
    recorded as absent, never invented."""
    if not isinstance(doc, dict):
        return {"denial_file_present": False}
    return {
        "denial_file_present": True,
        "decision": doc.get("decision"),
        "reason": doc.get("reason"),
    }


def build_failure_receipt(
    *,
    github_sha,
    production_branch,
    promotion_mode,
    authorized_source_sha,
    actor,
    workflow_run_id,
    env,
    files,
    gates=None,
):
    """Build the failure receipt. See module docstring for the contract.

    `env`: mapping of workflow environment variables (DEPLOYMENT_SHA,
    SOURCE_TREE_SHA, DEPLOYMENT_TREE_SHA may be absent on early failures).
    `files`: mapping of artifact filename -> parsed JSON dict or None.
    `gates`: optional mapping of upstream gate evidence. Keys:
      - "standing_policy_verdict": parsed standing-authorization-verdict.json
        dict or None.
      - "promotion_denial": parsed production-promotion-denial.json dict
        or None.
      - "required_workflows": mapping workflow filename -> workflow-run dict
        or None, as observed by the receipt step via the GitHub API.
    Missing or malformed gate evidence is recorded as absent/UNKNOWN, never
    invented.
    """
    env = dict(env or {})
    files = dict(files or {})
    gates = dict(gates or {})

    supabase_check = files.get(SUPABASE_CHECK_FILE)
    if not isinstance(supabase_check, dict):
        supabase_check = None
    deployment_sha = env.get("DEPLOYMENT_SHA")
    deployed = (
        supabase_check is not None
        and supabase_check.get("conclusion") == "success"
        and bool(deployment_sha)
    )

    legs = {}
    for leg_key, filename in PROOF_LEGS:
        legs[leg_key] = evaluate_leg(files.get(filename), github_sha)

    all_success = all(leg["status"] == "SUCCESS" for leg in legs.values())
    any_failure_evidence = any(
        leg["status"] in ("FAILED", "SOURCE_MISMATCH", "NOT_EXECUTED", "UNKNOWN")
        for leg in legs.values()
    )

    if deployed and all_success:
        # Defensive: this module is only wired to failure(), so every leg
        # succeeding here means the wiring is wrong. Say so loudly instead
        # of certifying a proof this module is not authorized to certify.
        status = "UNEXPECTED_ALL_SUCCESS"
    elif deployed and any_failure_evidence:
        status = "PROMOTED_BUT_UNPROVEN"
    elif deployed:
        status = "PROMOTED_BUT_UNPROVEN"
    else:
        status = "DEPLOY_FAILED"

    gate_runs = gates.get("required_workflows")
    if not isinstance(gate_runs, dict):
        gate_runs = {}
    gate_section = {
        workflow: evaluate_gate_run(gate_runs.get(workflow), github_sha)
        for workflow in REQUIRED_WORKFLOWS
    }

    return {
        "schema": SCHEMA,
        "status": status,
        "source_sha": github_sha,
        "production_branch": production_branch,
        "human_authorization": {
            "type": promotion_mode,
            "confirmation": (
                "STANDING-PRODUCTION-PROMOTION-V1"
                if promotion_mode == "STANDING_POLICY"
                else "DEPLOY"
            ),
            "authorized_source_sha": authorized_source_sha,
            "actor": actor,
            "workflow_run_id": workflow_run_id,
        },
        "gates": {
            "standing_policy": evaluate_policy_file(gates.get("standing_policy_verdict")),
            "promotion_denial": evaluate_denial_file(gates.get("promotion_denial")),
            "required_workflows": gate_section,
        },
        "machine_deployment": {
            "attempted": True,
            "deployment_commit_sha": deployment_sha,
            "deployed_source_revision": github_sha,
            "source_tree_sha": env.get("SOURCE_TREE_SHA"),
            "deployment_tree_sha": env.get("DEPLOYMENT_TREE_SHA"),
            "supabase_check": (
                {
                    "id": supabase_check.get("id"),
                    "name": supabase_check.get("name"),
                    "conclusion": supabase_check.get("conclusion"),
                }
                if supabase_check is not None
                else None
            ),
            "deployed": deployed,
        },
        "proof_handshake": {
            "promoted_and_proven_claim": "REFUSED",
            "reason": (
                "parent promotion receipt is a fail-closed handshake: "
                "PROMOTED_AND_PROVEN requires every proof leg to complete "
                "with conclusion=success against the authorized source SHA"
            ),
            "legs": legs,
        },
        "authority_boundary": {
            "human_authorization_is_deployment_decision": True,
            "machine_authentication_is_supabase_github_integration": True,
            "learning_runtime_identity_remains_github_oidc": True,
            "supabase_personal_access_token_in_workflow": False,
        },
    }
