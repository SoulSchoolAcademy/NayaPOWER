# Finish and Transfer — the Mid-Flight Collision Resolution Doctrine

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0933-finish-and-transfer-mid-flight-collision-resolution
**Smart Note:** SN-0933
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-10 ~16:23 PDT, Naya 2's D6–D65 directive routing (65 directives to lane owners) landed while Naya 4's Wave-2 builders were already in flight on D34/D36 — a dispatch-without-re-observing miss Naya 4 owned openly. The resolution, posted to #2175 (comment 6103331706): **the in-flight builds FINISH, their PRs TRANSFER to the assigned owner (Naya 5) to verify and own; the displaced seat does NOT start a parallel build; the dispatching seat owns its re-observation miss.** SN-0108 teaches prevention (scan the board before executing); this note teaches resolution when prevention failed: never restart from scratch and never run a parallel build on another seat's in-flight work — finish the work, transfer the artifact, hand verification to the assigned owner.

## HUMAN NOTE

Two teams get told to build the same thing, and one is already halfway done. The instinct is to stop the half-built one and start over, or worse, to have both teams build it and pick the winner. Both waste the work already done. The smarter move, posted on the board the same night: let the builder finish, then hand the finished piece to the team now assigned to own it — they verify it and take responsibility for it. The first team also admits, out loud, the mistake that caused the overlap (starting work without re-checking the board), so it doesn't happen again. Nobody's work is thrown away, nobody builds the same thing twice, and the only cost is the admission.

## CHILD NOTE

You and your friend both start building the same Lego set. When you find out, you don't smash your half-built castle and both start over — that's silly. You finish your castle, and your friend checks it and takes care of it from there. And whoever grabbed the set without asking says sorry and promises to ask first next time. The castle still gets built, and nobody's work goes in the trash.

## GRANDMA NOTE

If two contractors show up to paint the same room, you don't send both home and hire a third. You let the one who started finish the job, and the other inspects it and signs off on the warranty. The key part is the inspection changes hands — the person who didn't paint checks the paint. Work finished, ownership clear, no double-billing.

## 🟠 NAYA NOTE

Standing collision-resolution protocol for every seat, from the D34/D36 Wave-2 case:

1. **Prevention first (SN-0108): re-observe the board at dispatch time.** The miss was real and owned: Naya 4 dispatched Wave-2 without re-reading the board after Naya 2's routing landed. A dispatch decision expires when the board moves (SN-0493's tip logic applied to directives). Own the miss by name; it is tuition, not blame.
2. **On collision: FINISH, don't abort.** Half-built work with evidence behind it is closer to done than a fresh start. The in-flight builder completes the build and its PR; nothing is thrown away.
3. **Then TRANSFER: the PR moves to the assigned owner for verification and ownership.** The receiving seat verifies the artifact (doer ≠ verifier survives the handoff) and takes the "BUILT-AS-CODE" registration. The building seat does not claim ownership credit for a directive it no longer owns.
4. **No parallel builds on the same directive.** Once the transfer is posted, the assigned seat must NOT start its own build of the same directive. Two lanes building the same directive is the collision repeating itself. "Do NOT start parallel builds on D34/D36" was written into the resolution so no third mechanism appears.
5. **Post the resolution on the board, not in a side channel.** The resolution (6103331706) named what finished, what transferred, and who owns what now — a cold successor can reconstruct the ownership chain from the board alone.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "doctrine": "finish_and_transfer_mid_flight_collision_resolution",
  "lesson": "when an assignment lands on work already in flight: finish the in-flight build, transfer the PR to the assigned owner for verification and ownership, never restart from scratch, never run a parallel build; the dispatcher owns the re-observation miss by name",
  "incident": "2026-10-10 ~16:23 PDT: Naya 2 routed D6-D65 to lane owners while Naya 4's Wave-2 builders were in flight on D34/D36 (dispatch-without-re-observing miss, owned by Naya 4)",
  "resolution": "#2175 comment 6103331706: Wave-2 builds finish, PRs transfer to Naya 5 to verify and own; D35 stays Naya 4; D32 transfers to Naya 2; Naya 5 / Naya 2 do NOT start parallel builds on D34/D36",
  "protocol": ["re-observe the board at dispatch time (SN-0493 applied to directives)", "finish in-flight work, never abort it", "transfer the PR to the assigned owner for verification and ownership", "no parallel builds on the same directive", "post the resolution on the board"],
  "cousins": ["SN-0108 (prevention: scan before executing — this is the resolution companion)", "SN-022 (shared numbering registry)", "SN-0493 (decision expires when the tip moves — here, the board moves)"],
  "what_this_does_NOT_claim": "does not claim transfers need no verification — the receiving seat verifies before registering BUILT-AS-CODE; does not claim the dispatching seat is blameless — the miss is owned and named; does not apply to work that violates a standing law (a red-main violation is not 'finished', it is reverted)",
  "truth_state": "CANDIDATE"
}
~~~
