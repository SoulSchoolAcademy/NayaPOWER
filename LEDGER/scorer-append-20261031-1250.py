import json
path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t0942",
        "agent": "Team Naya Scorer",
        "lane": 10,
        "task": "Design lift-stamp contract spec v1 (no machinery, no stamps)",
        "receipt": "t0942-lane10.md",
        "score": 9.3,
        "note": "VERIFIED this tick on live bytes: hidden_files/lift-stamp-contract-spec-20261019.md sha256 0fef6b5cff12f133ead2fd025e1fdb46a80aa6c31822151ced255552ca13f8f1 and hidden_files/lift-stamp-falsifiers-redfirst-20261019.md sha256 44e4b0e875bee1df111d2589aa3c20526028f8f2cd80a0bb30e43dff7e8cd71d, both exactly matching the receipt cites; 12-section spec with eligibility, liftable/never-liftable classes, authority chain, TTL rule and ledger schema, plus 6 RED-first falsifiers written before the body. NOT PHANTOM. Score 9.3, GOOD, ONE MORE PASS. Why not 9.5: (1) section 9 machine checks are specified, not built, so the claim block still honors no lift; (2) TTL class caps unset (fail-closed default 0, dispatcher numbers owed); (3) no second-seat adversarial review before the spec leaves CANDIDATE. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "t0944",
        "agent": "Team Naya Scorer",
        "lane": 10,
        "task": "First application of lift-stamp spec v1: classify 29 queued gap briefs into ledger",
        "receipt": "t0944-lane10.md",
        "score": 9.3,
        "note": "VERIFIED this tick on live bytes: hidden_files/lift-application-ledger-20261019.jsonl sha256 180a9280ffcdecd7d63f01bdbcef35a55abb9e1b24a86e85cacc92d6f689ee25 exactly matching the receipt cite, and the spec it applies is byte-unchanged (sha above); 29 rows, one per queued brief, assess-and-recommend only with no stamps issued and no queued briefs touched. NOT PHANTOM. Score 9.3, GOOD, ONE MORE PASS. Why not 9.5: (1) value is recommendatory only - the drain still needs dispatcher H2 caps and H3 spec review before any lift moves; (2) the FA4b machine check used a narrower regex than the evidence phrasing and was corrected by intent re-check, so one falsifier leg rests on judgment, not a machine check; (3) single-seat classification, no second-seat spot-check of the 29 rows. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "t0940",
        "agent": "Team Naya Scorer",
        "lane": 10,
        "task": "Brain-index drift recurrence: bisect, re-cut heal on live tip, merge-ready package",
        "receipt": "t0940-lane10.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: git ls-remote origin refs/heads/naya/ten-brainindex-heal-t0940 = 34e8e84814bb2d1ffb434fa1f4d787d9e47b4e6f, exactly the receipt's pushed head; receipt documents regen diff of exactly the 3 index files, --check exit 0, freshness tests 13/13 on the heal bytes, and an independent fresh-clone re-verification. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: (1) the heal is a branch plus a drafted PR-open package, not a merged heal - the PR was correctly not opened by the lane, but the drift is therefore still live on main; (2) the brain-index freshness gate workflow is still absent at tip, so the IB-projection drift class will recur until #2385 merges plus the required-check click; (3) the recurrence-numbering question (#16 unhealed vs #17/18/19) is named, not resolved, and the #16 introducer status is cited from t0914/t0919, not re-proven this run. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
    },
]
with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
