import json

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t0561",
        "agent": "Team Naya Scorer",
        "lane": 8,
        "task": "Re-fire delivery-gate + claim-evidence-gate on PR #2683 post-reset and classify the morning reds",
        "receipt": "t0561-lane8.md",
        "score": 9.5,
        "note": "VERIFIED this tick on LIVE GitHub API bytes (commit check-runs at head 1c8cd141397c91373e57dcc0ec79d0600355324a): check 117012500409 delivery-gate success completed 2026-10-16T14:04:22Z, check 117012509844 claim-evidence-gate success completed 2026-10-16T14:04:19Z, check 116804602629 Team review + scorecard receipt failure completed 2026-10-16T04:03:38Z — all three ID/name/conclusion/timestamp exact as receipted. NOT PHANTOM. Clears 9.5 because the receipt's core deliverable — the post-reset re-fire turning both infrastructure reds GREEN on identical content, confirming the quota hypothesis and closing t0556's named next action — is confirmed by an independent live read 12 days later, with scope discipline held (Zeta leg untouched, dirty merge state carried, merge-consensus boundary named). Residual caveats that do not block 9.5: the branch ref is gone from ls-remote (PR lifecycle, not a receipt defect — the check-runs API still pins the head's runs); the morning exit-2 semantics are inherited from t0556, but the green re-fire on identical content is strictly stronger evidence than that chain; the merge-consensus 04:03Z workflow failure remains unclassified by design (outside this brief's two gates). No gap follow-up: 9.5 clears the bar. No PHANTOM, no lane below 7.0 this tick.",
    },
    {
        "tick": "t0562",
        "agent": "Team Naya Scorer",
        "lane": 12,
        "task": "RECUSE on capture-inbox adapter conformance re-fire (authoring seat) + durable claimability-gate stamp cure",
        "receipt": "t0562-lane12.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live workspace bytes: hidden_files/one-flow/capture-inbox-adapter.py sha256 2383c949d488c84b1f9807874f019d541eb2847dbdc0424f3055bd91f9811ec1 exactly as receipted, confirming authorship and that the eligibility gate correctly fires. The brief's pre-stamp sha 45ee3ae722a8bada3e7e6d04b854f933340ece071a8e5f3023ba8cfed80a59d2 matches the receipt's own 14:41Z post-move SHA, proving the byte-intact re-file chain internally. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, agreeing with lane honest 9.0. Why not 9.5: (1) third claim-then-recuse round-trip on this one brief in a day — the systemic filing-path cure (dispatcher stamping contract) was still outstanding, the stamper only cured this brief retroactively; (2) no independent conformance battery was produced, by design, so the adapter still stood on the builder's own self-verification at receipt time; (3) the brief is no longer in brief-queue/ today (t0582 dispatcher disposition moved it out of rotation queued), so the OPEN state claimed in the addendum cannot be re-confirmed from the queue path alone. GAP-RECYCLE THROTTLED: rotation queued=31 >= 30, zero follow-ups filed this tick. No PHANTOM, no lane below 7.0 this tick.",
    },
    {
        "tick": "t0563",
        "agent": "Team Naya Scorer",
        "lane": 4,
        "task": "SMARTBLOCKS shared-schema-spec v0.1 + machine lint check_smartblock.py with red/positive fixtures",
        "receipt": "t0563-lane4.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live workspace bytes: both fixtures sha-exact as receipted (conformant 608078e9b1f79818ad86caa883730ad2303f177f70adfa383966de42277e0a6b, malformed 294905e6b2c1860ec875772446c9d402816183b3ac6fd0c37b066333ef905613), and bin/check_smartblock.py --selftest still passes with the receipt's exact behavior (conformant exit 0, malformed fail-closed with 8 checks). Spec and lint SHAs have drifted since receipt (12 days of later edits) — lineage intact via the unchanged fixtures and reproduced selftest, not a phantom. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, agreeing with lane honest 9.0. Why not 9.5: (1) the diary-intake exemplar is synthetic — authored the same tick, so its need is constructed, not observed from a query log (receipt's own -gap); (2) the provenance join with Herald's provenance-marker-spec-v1 is prose, not proven — no battery reads both markers (receipt's own -gap); (3) the blockquote-status WARN regex truncation on multi-word prose statuses is cosmetic but unfixed in the receipt. GAP-RECYCLE THROTTLED: rotation queued=31 >= 30, zero follow-ups filed this tick. No PHANTOM, no lane below 7.0 this tick.",
    },
]

with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
