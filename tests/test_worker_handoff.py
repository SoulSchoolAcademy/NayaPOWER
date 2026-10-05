

# ==========================================================================
# WORKER HANDOFF VALIDATOR -- "a worker says done, the system says show me"
# ==========================================================================
def test_complete_handoff_is_accepted():
    from tools.worker_handoff import check_handoff

    good = """
## Current known reality
main at abc123, gate measured, exit 0.

## Current P0
backfill the five captures.

## Next three actions
1. backfill
2. verify
3. report

## Permanent constraints
no merges, no production.

## First action
apply the key.

## Handoff completion
Coda 1, test 15/15, commit abc123
"""
    res = check_handoff(good)
    assert res.accepted, res.violations
    assert res.score >= 9.0


def test_empty_handoff_is_rejected():
    from tools.worker_handoff import check_handoff
    assert not check_handoff("").accepted
    assert not check_handoff("   ").accepted


def test_missing_section_is_rejected():
    from tools.worker_handoff import check_handoff
    res = check_handoff("""
## Current known reality
main at abc123
""")
    assert not res.accepted
    assert any("required canonical section" in v for v in res.violations)


def test_heading_with_no_body_is_not_a_section():
    """An empty heading is a claim without evidence."""
    from tools.worker_handoff import check_handoff
    res = check_handoff("""
## Current known reality

## Current P0

## Next three actions

## Permanent constraints

## First action

## Handoff completion
""")
    assert not res.accepted
    assert len(res.missing) >= 5


def test_completion_claim_without_evidence_is_rejected():
    """THE load-bearing negative control: 'done' with no evidence."""
    from tools.worker_handoff import check_handoff
    res = check_handoff("""
## Current known reality
Everything is fine and the work is done.

## Current P0
nothing

## Next three actions
1. continue

## Permanent constraints
none

## First action
carry on

## Handoff completion
complete
""")
    assert not res.accepted
    assert any("no evidence marker" in v for v in res.violations)


def test_declared_uncertainty_is_advisory_not_violation():
    """Honesty must not be scored as a defect."""
    from tools.worker_handoff import check_handoff
    res = check_handoff("""
## Current known reality
main at abc123, measured, exit 0. Staleness UNKNOWN.

## Current P0
backfill

## Next three actions
1. backfill
2. verify

## Permanent constraints
no merges

## First action
apply

## Handoff completion
commit abc123, BLOCKED on merge
""")
    assert res.accepted, res.violations
    assert not any("epistemic" in v for v in res.violations)
    # Declaring UNKNOWN/BLOCKED must not REDUCE the score.
    assert res.score >= 9.0
    assert res.advisories == [], "declared uncertainty must not raise an advisory"


def test_score_never_exceeds_ten():
    from tools.worker_handoff import check_handoff
    res = check_handoff("""
## Current known reality
sha abc123 test exit 0 measured UNKNOWN BLOCKED

## Current P0
p0

## Next three actions
1. a 2. b 3. c

## Permanent constraints
none

## First action
go

## Handoff completion
verified sha abc123
""")
    assert res.score <= 10.0


def test_scorecard_counts():
    from tools.worker_handoff import check_handoff, scorecard
    good = check_handoff("""
## Current known reality
sha abc test exit 0

## Current P0
p0

## Next three actions
1. a 2. b 3. c

## Permanent constraints
none

## First action
go

## Handoff completion
verified sha abc123
""")
    bad = check_handoff("nothing")
    card = scorecard([good, bad])
    assert card["checked"] == 2 and card["rejected"] == 1, card
    assert card["accepted"] == 1
