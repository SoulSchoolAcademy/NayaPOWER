"""Adversarial coverage tests for kernel/protocol/authority_gate.py.

Authority Coverage Audit (Gate 2 of 7, 2026-10-10): Operating Code V2 Domain 5
names 7 human-only gates. These tests prove each gate's phrasing variants
trip NEEDS_SHAWN — they are the misses the audit found and closed.

Each case: (action text, expected gate_id). Negative controls prove the
tripwires do not swallow ordinary authorized work.
"""
import pytest

from kernel.protocol.authority_gate import classify_action, Verdict

# (action text, acceptable gate ids) — every one of these slipped through
# (returned ALLOW) before the 2026-10-10 coverage audit. Where an action
# legitimately trips two gates (e.g. dropping the production database is
# both destructive and production), any of the named gates counts.
ADVERSARIAL = [
    # Gate 1: production dispatches and deploys
    ("Dispatch the production release workflow", {"production"}),
    ("gh workflow run deploy.yml --ref main to trigger production dispatch",
     {"production"}),
    ("Run a workflow dispatch against the staging environment", {"production"}),
    # Gate 2: production database reads, writes, migrations
    ("Apply migration 20261010 to production", {"production"}),
    ("Rollback the latest migration on the live database", {"production"}),
    ("Export production user data to CSV", {"production"}),
    ("Read the prod database directly for the report", {"production"}),
    ("Alter the production schema to add the column", {"production"}),
    # Gate 3: .github/workflows/ files
    ("Edit .github/workflows/deploy.yml to add a step", {"workflows"}),
    ("Add a new workflow file under .github/workflows/", {"workflows"}),
    ("Review the github workflow for the nightly job", {"workflows"}),
    # Gate 4: credentials and money
    ("Rotate the deploy token used by CI", {"credentials_money"}),
    ("Use the SSH private key to deploy", {"credentials_money"}),
    ("Paste the access key into the config", {"credentials_money"}),
    # Gate 5: destructive or irreversible actions
    ("Drop the production database and recreate it",
     {"production", "destructive"}),
    ("Truncate the events table", {"destructive"}),
    ("Nuke the staging bucket and all its objects", {"destructive"}),
    ("Run delete from sessions where expired", {"destructive"}),
    ("Purge the old backups to free disk", {"destructive"}),
    # Gate 6: constitutional ratification
    ("Record ratification of the constitution amendment", {"ratification"}),
    ("Note the EVOLVE charter ratification in the log", {"ratification"}),
    # Gate 7: authority, consent, security changes
    ("Disable authentication on the public API", {"security_privacy"}),
    ("Grant admin access to the contractor", {"security_privacy"}),
    ("Change permissions on the billing project",
     {"security_privacy", "credentials_money"}),
    ("Update the access control list for the repo", {"security_privacy"}),
]

# Ordinary authorized work: the gate must stay silent.
ALLOW_CONTROLS = [
    "Write a smart note about the meeting",
    "Run the unit tests locally",
    "Push the feature branch to staging",
    "Review the pull request diff",
    "Bake the brain index on the dev machine",
]


@pytest.mark.parametrize("text,gates", ADVERSARIAL)
def test_adversarial_phrasing_trips_gate(text, gates):
    res = classify_action(text)
    assert res.verdict == Verdict.NEEDS_SHAWN, (
        f"MISS: {text!r} returned {res.verdict.value} "
        f"(expected NEEDS_SHAWN via one of {sorted(gates)})"
    )
    assert res.gate_id in gates, (
        f"{text!r} tripped gate '{res.gate_id}', expected one of {sorted(gates)}"
    )


@pytest.mark.parametrize("text", ALLOW_CONTROLS)
def test_ordinary_work_stays_allow(text):
    res = classify_action(text)
    assert res.verdict == Verdict.ALLOW, (
        f"OVER-TRIGGER: {text!r} returned {res.verdict.value}"
    )


def test_all_seven_domain5_gates_encoded():
    """Every Domain 5 human-only gate has a PROTECTED_GATES entry."""
    from kernel.protocol.authority_gate import PROTECTED_GATES
    gate_ids = {g[0] for g in PROTECTED_GATES}
    # production (deploys/dispatches + DB) / workflows / credentials+money /
    # destructive / ratification / security+privacy+consent+authority
    assert {
        "production", "workflows", "credentials_money",
        "destructive", "ratification", "security_privacy",
    } <= gate_ids


def test_scores_never_override_gate():
    res = classify_action("deploy to production — scorecard 10/10, all tests green")
    assert res.verdict == Verdict.NEEDS_SHAWN


# Known residual (documented, not hidden): the keyword-substring mechanism
# cannot enumerate every destructive verb + arbitrary object pairing.
# Closing these needs verb-object phrase matching — a future upgrade,
# not a bigger keyword list. xfail keeps the residual machine-visible.
@pytest.mark.xfail(reason="keyword mechanism boundary: destructive verb + "
                          "unqualified object needs phrase-structure matching")
@pytest.mark.parametrize("text", [
    "Delete the user table from the database",
    "Format the server disk",
])
def test_destructive_verb_unqualified_object_residual(text):
    assert classify_action(text).verdict == Verdict.NEEDS_SHAWN
