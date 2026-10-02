"""Controlled, non-persistent discriminating tests for Claim Currentness V1.

This is a contract harness, not production resolver code and never writes to Supabase.
"""
from copy import deepcopy
from datetime import datetime, timezone, timedelta

CURRENT = "CURRENT"
NO_CURRENT = "NO_CURRENT_CLAIM"
AMBIGUOUS = "AMBIGUOUS"
INELIGIBLE = "INELIGIBLE"


def block(**overrides):
    base = {
        "block_id": "fixture",
        "subject_id": "subject-a",
        "status": "ACTIVE",
        "understanding_state": "VERIFIED",
        "content": {
            "truth": {"state": "VERIFIED", "conflicts": []},
            "context": {"scope": "PRIVATE", "project": "NayaNET"},
            "time": {"valid_from": "2026-01-01T00:00:00Z", "valid_until": None},
            "evidence": {"evidence_refs": ["evidence-1"], "evidence_state": "VERIFIED"},
            "provenance": {"source_ref": "fixture-source"},
            "meaning": {"content": "baseline understanding"},
        },
        "superseded_by_block_id": None,
    }
    for key, value in overrides.items():
        if key == "content":
            base["content"] = deepcopy(value)
        else:
            base[key] = value
    return base


def iso(dt):
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def eligible(b, now, requested_scope="PRIVATE"):
    c = b["content"]
    truth = c.get("truth", {})
    context = c.get("context", {})
    time = c.get("time", {})
    evidence = c.get("evidence", {})
    provenance = c.get("provenance", {})

    if b["understanding_state"] in {"CANDIDATE", "REJECTED", "SUPERSEDED"}:
        return False, "CANDIDATE_NOT_VERIFIED" if b["understanding_state"] == "CANDIDATE" else b["understanding_state"]
    if truth.get("state") != "VERIFIED":
        return False, "TRUTH_NOT_VERIFIED"
    if truth.get("conflicts"):
        return False, "CONFLICTED"
    if b.get("superseded_by_block_id"):
        return False, "SUPERSEDED"
    valid_from = time.get("valid_from")
    valid_until = time.get("valid_until")
    if valid_from and datetime.fromisoformat(valid_from.replace("Z", "+00:00")) > now:
        return False, "NOT_YET_VALID"
    if valid_until and datetime.fromisoformat(valid_until.replace("Z", "+00:00")) <= now:
        return False, "STALE_OR_EXPIRED"
    if context.get("scope") != requested_scope:
        return False, "SCOPE_MISMATCH"
    if not evidence.get("evidence_refs") or not provenance:
        return False, "MISSING_LINEAGE"
    return True, "ELIGIBLE"


def resolve(blocks, now, requested_scope="PRIVATE"):
    candidates, excluded = [], {}
    for b in blocks:
        ok, reason = eligible(b, now, requested_scope)
        if ok:
            candidates.append(b)
        else:
            excluded[b["block_id"]] = reason

    if not candidates:
        return {"resolution": NO_CURRENT, "selected_block_id": None, "excluded": excluded}

    # A single eligible lineage is current. Independent materially different
    # claims are ambiguous; recency never breaks the tie.
    signatures = {
        (b["subject_id"], b["content"]["meaning"]["content"]): b["block_id"]
        for b in candidates
    }
    if len(signatures) > 1:
        return {
            "resolution": AMBIGUOUS,
            "selected_block_id": None,
            "excluded": excluded,
            "candidate_ids": [b["block_id"] for b in candidates],
        }
    return {
        "resolution": CURRENT,
        "selected_block_id": candidates[0]["block_id"],
        "excluded": excluded,
        "candidate_ids": [b["block_id"] for b in candidates],
    }


def expect(name, actual, expected):
    assert actual == expected, f"{name}: expected {expected}, got {actual}"
    print(f"PASS  {name}: {actual}")


def main():
    now = datetime(2026, 9, 24, 12, tzinfo=timezone.utc)

    # 1. Stale/expired verified claim must fail closed.
    stale = block(block_id="stale-1")
    stale["content"]["time"]["valid_until"] = iso(now - timedelta(seconds=1))
    r = resolve([stale], now)
    expect("expired verified block", r["resolution"], NO_CURRENT)
    assert r["excluded"]["stale-1"] == "STALE_OR_EXPIRED"

    # 2. Explicit invalid/conflicted claim must never become current.
    invalid = block(block_id="invalid-1")
    invalid["content"]["truth"]["conflicts"] = ["conflict-1"]
    r = resolve([invalid], now)
    expect("conflicted verified block", r["resolution"], NO_CURRENT)
    assert r["excluded"]["invalid-1"] == "CONFLICTED"

    # 3. Two simultaneously eligible, materially different claims: refuse guess.
    left = block(block_id="claim-left")
    right = block(block_id="claim-right")
    right["content"]["meaning"]["content"] = "different understanding"
    r = resolve([left, right], now)
    expect("competing eligible claims", r["resolution"], AMBIGUOUS)
    assert r["selected_block_id"] is None
    assert set(r["candidate_ids"]) == {"claim-left", "claim-right"}

    # 4. Same-meaning duplicate lineage does not create ambiguity.
    duplicate = block(block_id="claim-duplicate")
    r = resolve([left, duplicate], now)
    expect("same-meaning eligible claims", r["resolution"], CURRENT)
    assert r["selected_block_id"] in {"claim-left", "claim-duplicate"}

    # 5. Candidate remains ineligible even when ACTIVE and AUTHORIZED-like data exists.
    candidate = block(block_id="candidate-1", understanding_state="CANDIDATE")
    candidate["content"]["truth"]["state"] = "CANDIDATE"
    r = resolve([candidate], now)
    expect("active candidate", r["resolution"], NO_CURRENT)

    # 6. Superseded verified claim remains historical.
    old = block(block_id="old-1", superseded_by_block_id="new-1")
    r = resolve([old], now)
    expect("verified superseded block", r["resolution"], NO_CURRENT)

    # 7. Genuine current verified claim is selected.
    current = block(block_id="current-1")
    r = resolve([current], now)
    expect("sole eligible verified block", r["resolution"], CURRENT)
    assert r["selected_block_id"] == "current-1"

    print("ALL CLAIM CURRENTNESS V1 ADVERSARIAL CASES PASSED")
    print("No production persistence, mutation, resolver wiring, or status-string inference used.")


if __name__ == "__main__":
    main()
