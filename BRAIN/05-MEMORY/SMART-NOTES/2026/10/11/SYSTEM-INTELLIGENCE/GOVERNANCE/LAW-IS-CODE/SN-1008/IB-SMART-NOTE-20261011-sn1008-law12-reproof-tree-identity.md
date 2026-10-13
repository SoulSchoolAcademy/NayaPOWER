# Law-12 Re-Proof by Tree Identity — Byte-Identical Enforcement Blobs Carry Across the Tip Move

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1008-law12-reproof-tree-identity
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:08 PDT distillation tick (2026-10-11) from #2175 comment 6113187563 (night-shift-wire sign-out — T-09 watch re-proof on moved tip, 2026-10-11T20:06:35Z), read live. Both tips ref-anchored live: 6f854cf9 → 4fc40263 (7 commits: merges #2371, #2372, #2373).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-0493 says a decision expires when the tip moves — re-verify at action time. The wire lane showed what "re-verify" actually looks like as a procedure, not a slogan. When the tip moved 6f854cf9 → 4fc40263, the lane did NOT re-run everything blind. It compared the enforcement blobs at both tips byte-for-byte: all 9 enforcement blobs plus the checks/ subtree were identical, so Law-11-v2 ENFORCED, the Law-12 door, and conflict-resolution enforcement all CARRY — the manifest move was registration delta only. One mechanism was NEW (#2372 BRAIN-INDEX-FRESHNESS, now WIRED into kernel-tests.yml) and it was classified separately: equivalent-or-stronger machinery, proven both-directions (clean tip → PASS "OK: index layer matches git tree (1243 files)"; planted drift → FAIL exit 1 naming the drifted files plus the fix command). Two distinct claims, two distinct proofs: CARRIED = byte-identical at both tips; RE-PROVEN = re-run the both-directions probe on the new tip. A replaced check is either equivalent-or-stronger (proven both directions, old check retired with a reason) or it is dropped coverage and must be named as such. This is the procedure that makes Law-12 executable.

## 🩷 HUMAN NOTE

A contractor signed off on your wiring last month. This month you add a room. You don't rewire the whole house — you check: are the wires in the old rooms the same wires he signed off on? If yes, his signature carries; you only inspect the new room, with the same rigor he used. If someone replaced an outlet with a better one, you don't fail them for changing things — you test the new outlet both ways (works when it should, trips when it shouldn't) and file "equivalent or stronger." That's the whole method: compare what you can, re-test what changed, and never pretend a changed part is the same part.

## 👶 CHILD NOTE

When you build with blocks and your friend adds a few new ones, you don't take apart everything you already built. You check: are my old blocks exactly where I left them? Yes → they're still fine. Then you look at just the new blocks and test them: does the tower still stand? You also test that if you put a wobbly block in, the tower falls the way you expect. Only the new part needs testing — but it needs REAL testing, not just looking.

## 👵 GRANDMA NOTE

The plumber did a great job on your pipes last year. This year you remodel the kitchen. You don't make him redo the bathroom pipes — you just confirm they're the same pipes he already certified, untouched. Then you watch him test the new kitchen work: water runs where it should, and the shutoff actually stops it when it shouldn't. And if he swapped an old valve for a newer model, he shows you the new one is at least as good — not just newer.

## 🤖 NAYA NOTE

Three distinct verdicts, never conflated:
1. **CARRIED** — the enforcement tree at the new tip is byte-identical to the tip the original proof ran on (compare via `git/trees` recursive at both SHAs; enforcement blobs + checks/ subtree). No re-run needed: identity IS the proof the bytes carry.
2. **RE-PROVEN** — a mechanism is new at this tip or its bytes changed. Run the both-directions probe live on the new tip (clean → PASS with the exact expected output string; planted fault → FAIL naming the fault + fix command; probe worktree removed after).
3. **EQUIVALENT-OR-STRONGER** — an old check was replaced. The replacement must prove both-directions on the new tip AND the old check's retirement must name the replacement. "The old --check step was replaced by equivalent-or-stronger machinery" is the correct sentence; "B-01 heal holds on the new tip" is the receipt.

MERGED-NOT-ENFORCED stays its own verdict: zero call sites (re-grep'd on the exact tip) is a fact about the world, not a proof to carry. Cold-successor rule: after any tip move, run tree-identity on the enforcement seam BEFORE deciding what to re-run; the re-run list is exactly the delta, and anything you skip must be carried-by-identity, not skipped-by-hope.

## ⚙️ MACHINE NOTE

{
  "sn_id": "SN-1008",
  "intelligent_block": "IB-SMART-NOTE-20261011-sn1008-law12-reproof-tree-identity",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE",
  "sub": "GOVERNANCE/LAW-IS-CODE",
  "evidence": [
    {"type": "board_comment", "ref": "#2175 comment 6113187563", "created_at": "2026-10-11T20:06:35Z", "lane": "night-shift-wire T-09", "tips": ["6f854cf9", "4fc40263"], "merges_between": ["#2371", "#2372", "#2373"]},
    {"type": "tree_identity", "blobs": 9, "subtree": "checks/", "result": "byte-identical at both tips; Law-11-v2 ENFORCED + Law-12 door + conflict-resolution enforcement CARRY; manifest move = registration delta only"},
    {"type": "both_directions_probe", "mechanism": "#2372 BRAIN-INDEX-FRESHNESS (WIRED into kernel-tests.yml)", "clean": "PASS 'OK: index layer matches git tree (1243 files)'", "planted_drift": "FAIL exit 1 naming drifted files + fix command", "verdict": "equivalent-or-stronger machinery; B-01 heal holds"}
  ],
  "rule": "After a tip move: (1) tree-identity compare the enforcement seam at both tips — byte-identical means CARRIED; (2) re-prove only the delta, both-directions, on the new tip; (3) classify replaced checks as equivalent-or-stronger (proven) or dropped coverage (named). Never skip by hope.",
  "relates_to": ["SN-0493 (decision expires when the tip moves)", "Law-12 discipline", "SN-0987 / SN-0992 (law-is-code)"],
  "carrier": {"branch": "naya4/smart-notes-2026-09-30", "pr": "#1825", "merge": "NEVER", "ratification": "Shawn only"}
}
