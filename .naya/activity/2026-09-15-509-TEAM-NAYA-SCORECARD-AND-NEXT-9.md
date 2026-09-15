# TEAM NAYA — 509 SCORECARD + NEXT 9

## Score right now

**Repository readiness: 9.6/10**

**Public-shipping proof: 0/10**

**Overall mission status: NOT SHIPPED**

This score is intentionally split. The repository lane is materially stronger after the one-board renderer and structural-lock corrections, but there is no verified candidate/public PASS receipt yet. No success claim is authorized.

## Verified defects repaired in this cycle

1. Candidate `NUTSHELL` geometry acceptance was a false negative caused by comparing content to the outer board rectangle. Repaired in `bb5d79dae9e1649de754e035c21bb50c33ad9915`.
2. Existing V26 renderer was still internally configured for nine boards and emitted `NINE_BOARD_CANONICAL`, contradicting the active one-board contract. Repaired by aligning the existing V26 renderer to one reference board in `bfab45a029e39f8c730ba6ad90059d559aadea02`.
3. Existing structural lock still carried nine-board authority and conflicting sidebar labels. Repaired by aligning the existing structural lock to the one-board contract in `c5f9a658a49f2ea771cd91c266e4ee8f38fbd783`.

## Protected truths

- GitHub `main` is canonical.
- Smart Feed source content is not rewritten by the renderer.
- One reference board only during this phase.
- Exact ten approved sidebar destinations.
- Exact ten approved board sections: one nutshell plus nine semantic layers.
- Candidate acceptance remains mandatory before deployment.
- Public desktop/tablet/mobile acceptance remains mandatory after deployment.
- No nine-board replication before freeze + receipt.

# NEXT 9 — EXECUTE IN ORDER

### 1. Run the canonical release lane

Execute `.github/workflows/509-smart-board-world-class.yml` from the current `main` state. Do not create another workflow.

### 2. Inspect the first gate

If it fails, capture the exact first failing step and determine implementation vs acceptance defect. Do not patch ahead of evidence.

### 3. Repair only the first divergence

Use the smallest correct change. Preserve the existing V26 renderer and structural lock architecture.

### 4. Re-run the full candidate chain

Require static acceptance plus desktop/tablet/mobile browser acceptance. Do not weaken the contract to obtain green.

### 5. Release only after candidate PASS

Deploy `sparkling-shape-7ae5` only when candidate browser acceptance is proven.

### 6. Independently verify public runtime

Run the same browser acceptance against the public runtime at desktop/tablet/mobile. A responding URL is not proof.

### 7. Repair any public divergence

If public differs from candidate, identify the first divergence, repair source, rerun candidate, redeploy, and rerun public acceptance.

### 8. Create the verified receipt and freeze

Record source SHA, workflow run, candidate PASS, public PASS for all three viewports, runtime source SHA, board/section/sidebar state, defects/repaired defects, and next authorization. Freeze the reference.

### 9. Begin replication audit — not replication

Inspect existing architecture and choose the safest proven replication mechanism. Only after that audit may the nine additional boards be built.

## Handoff rule

The next Naya receives an explicit machine-actionable next step. Never hand off with “check what happens,” “see if it works,” or “ask Shawn.”
