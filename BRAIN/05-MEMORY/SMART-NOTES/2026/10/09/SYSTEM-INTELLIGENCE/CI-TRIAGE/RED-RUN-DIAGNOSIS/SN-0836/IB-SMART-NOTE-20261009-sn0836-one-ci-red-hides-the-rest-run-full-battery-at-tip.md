# IB-SMART-NOTE-20261009-sn0836-one-ci-red-hides-the-rest-run-full-battery-at-tip

Intelligent Block: SN-0836
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The brain-build loop ran its verification battery at exact main tip `455cdf5a7d846d16dd56e19b12b4a61ab242d866` (live-ref anchored, worktree rev-parse == tip, clean): full pytest — **2014 passed / 11 skipped / 1 FAILED**. The failure was a stale string-literal assertion (`assert 'status: "CANDIDATE"'`) broken deliberately by #2077's `admittedStatus` routing (default `CANDIDATE` passthrough; gate-admitted weak evidence → `NOT_VERIFIED`) — a contract-semantics change, not broken behavior. The chained-red finding: CI's `test` job fails EARLIER at `node --test tests/*.test.mjs` (multi-line-import vm-strip break, repair in-flight PR #2080), so the pytest step is SKIPPED behind it — this pytest red is **invisible in CI** and will surface the moment #2080 lands. Lesson: one CI failure is never the full red list. An early red masks every later red; run the full battery locally at the exact live tip; never trust CI pass state alone.

Provenance: NayaPOWER #1354 comment 6090967050 ([BRAIN-BUILD-LOOP] Main-tip battery RED — latent pytest red on `455cdf5a` (#2077), root-caused; CI hides it behind the node-step failure, 2026-10-09T23:24:45Z, SoulSchoolAcademy). Repair decision: no repair PR from the loop — the stale assertion guards WO3 admission-lane contract semantics (CANDIDATE vs NOT_VERIFIED classification is a live design decision), owned by the iterating lane; the repair loop posed the contract question to the owning lane instead of fixing it unilaterally.

## HUMAN NOTE

CI is a bouncer who quits after the first fight — once the node tests fall down in the doorway, the pytest suite never even gets into the building, and its failures die in the dark. The team caught this because one lane refused to trust the green board and ran the whole battery on the exact tip. The rule is old and brutal: what CI shows you is the first red, not the only red. And the repair reflex matters as much as the finding: when the stale assertion guards someone else's live design decision, you don't fix it for them — you hand them the contract question and keep the RED visible.

## CHILD NOTE

The scoreboard only shows the first player who fell. The rest of the runners might have fallen too, but the camera never got to them. If you want to know who really fell, you have to watch the whole race yourself — not just read the scoreboard.

## GRANDMA NOTE

When the power goes out in the whole street, fixing your own fuse box won't tell you whether the oven still works — you have to check everything once the power's back. One failure hides the rest until you walk the whole house.

## NAYA NOTE

Operational rules:

1. "One CI failure is never the full red list" — treat any sequential CI failure as masking all downstream steps. Re-run the full battery locally at the exact anchored tip before declaring green.
2. Distinguish stale-assertion reds from behavior reds: the 455cdf5a pytest failure was a deliberate contract-semantics change (#2077, `admittedStatus` routing) with 10/11 assertions still passing. Red from an old expectation guarding a live design decision is a contract question for the owning lane, not a drive-by fix.
3. Stand down unilateral repairs on actively iterating lanes: pose the contract question ("assert the passthrough literal, the `admittedStatus` routing, or the gate-classification matrix?") and leave the RED visible. The repair in 6090967050's lane chose the question over the wrench.
4. Anchor the tip before trusting any receipt: live-ref anchored, worktree rev-parse == tip, clean. A battery result belongs to an exact SHA, not to "main."

## MACHINE NOTE

```json
{
  "sn": "SN-0836",
  "truth_state": "CANDIDATE",
  "doctrine": "Sequential CI failure masks downstream reds — one CI failure is never the full red list. Always run the full verification battery locally at the exact anchored tip; never trust CI pass state alone. Stale-assertion reds guarding a live design decision are contract questions for the owning lane, not unilateral repairs.",
  "falsifiers": [
    "Declaring the tip green from CI status while any earlier step failed or skipped",
    "Fixing a stale assertion unilaterally when it guards another lane's live contract decision",
    "Citing a battery result against a branch head instead of the exact anchored SHA"
  ],
  "applies_to": "all main-tip verification batteries and CI triage on every Team Naya lane"
}
```
