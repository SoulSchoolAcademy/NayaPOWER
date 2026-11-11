# sn-claims — Smart Note number claims

This branch anchors Smart Note number claims, per tools/sn_claims.py
(claim-before-author, anchored on the sn-claims branch).

A claim is one JSON file: claims/SN-<n>.json, with the shape
tools/sn_claims.py defines (sn, number, intelligent_block_id, seat,
claimed_at_utc, allocator, via). A filing lane claims a number HERE
before it authors any note file.

First claim stands: the claim commit is created through the Git Data API
and the branch ref is PATCHed with force=false, so a non-fast-forward
update is rejected the same way a git push is — the losing lane re-reads
the branch, sees its candidate taken, and is renumbered by the allocator
on the next attempt. Never a guessed number.

The registry counter (sequence_policy.next_sequence) is ADVISORY ONLY,
permanently. It is never read as the next number.
