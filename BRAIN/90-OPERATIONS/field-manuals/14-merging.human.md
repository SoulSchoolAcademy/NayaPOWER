# 14 — MERGING: the protocol is the authorization

## ESSENCE
A merge happens because the protocol passed — scorecard 9.5+ at the exact head, a different seat's review, green gates, a fresh board read — never because someone clicked, and never because someone's word said so.

## WHAT IT IS
Merging is the dock: the moment a branch's work lands on main and becomes everyone's truth. It is the highest-leverage single action a Naya takes — one merge moves the tip every other lane builds on.

## WHAT IT DOES
It converts reviewed, proven work into the shared tree. Done right, the tip stays green, every byte is traceable to its review, and a cold Naya can re-derive exactly why this merge was lawful.

## WHY IT MATTERS
A bad merge poisons the well: every lane downstream builds on a red or unreviewed tip, and the repair costs ten times the prevention. We have paid for this twice in ways we can name — PR #1475 merged after a blocking review had already landed, and PR #1627's guard merged with zero live call sites. Both were preventable at the dock.

---

## THE RIGHT WAY

**The pre-merge checklist — in this order, in one unbroken step:**

1. **Re-fetch the live ref.** `GET /repos/.../git/refs/heads/main` — the ref is the truth, never the commits list. Anchor the merge on the live tip SHA.
2. **Freeze the PR head.** Record the exact head SHA. Everything below is scored against THIS SHA, not "the PR."
3. **Read the check states at the frozen head.** Required checks must be green ON THAT HEAD. A green on the parent is not a green on the head.
4. **Re-fetch the venue's newest state.** Read the newest comments on the board (#2537) right now — a merge without a fresh board read is a merge against unknown state. A blocking review that landed after your last read voids the merge.
5. **Confirm the scorecard.** 9.5+ scorecard receipt naming the exact frozen head SHA, with the receipt file behind it (receipt before merge, never after).
6. **Confirm cross-seat review.** A different seat than the author's — a GitHub approval from a different login, or a seat-tagged `[NAYA M · REVIEW] APPROVED` comment from a different seat, at the exact head, pre-merge. The UI's narrowest widget never defines the law: seat-tagged review comments satisfy the prong even when the counter shows "0 reviews."
7. **Confirm it is not your own PR.** Never self-merge. Open it, document it, hand it off.
8. **Name the omissions.** If the required-check set does not examine something (e.g. the kernel `test` battery is deliberately not required), write that omission into the merge-authority record. What the checks never examined is your responsibility, not theirs.

**Write the merge-authority record.** Before merging, record: PR number, frozen head SHA, scorecard receipt (id + score), reviewer seat, check states at the head, any named omissions. The record is the authorization — a merge without it is a merge on a wish.

**When the protocol does not pass — stand down.** If any checklist item fails, you do not merge. You post what failed, which prong, and what would repair it — then the PR returns to the queue. A stand-down is a correct outcome, not a failure. Merging around a failed prong is never "unblocking"; it is the #1475 class, and we have the scar.

**The dock holds a moving head.** If the PR head is still moving — new commits landing while you work the checklist — the dock waits. CI and dock judgment happen when the head settles, never mid-motion. Re-freeze and restart the checklist at the new head.

**Merges sequence through the merge lane.** The dock is one lane: merges land in queue order, coordinated, never ad hoc by whoever feels ready. Two merges racing the same tip is a deconfliction failure wearing a merge's clothes.

**Post-merge, before closing — the faithfulness proof:**

1. **Ancestor check.** Compare merge-commit against tip (base = the merge commit, head = the live tip): behind == 0 AND merge_base == the merge commit. The merge is an ancestor of the live tip. Only then record MERGED-VERIFIED AT TIP.
2. **Blob identity.** Key blobs byte-identical at PR head, merge commit, and tip. Squash merges rewrite history — bytes can drift through the squash. If the blobs differ, the merge is unfaithful and the record says so.
3. **Wiring check.** Grep the live tip for the wiring — every canonical call site the fix claims to enforce must reference the new code. Blob identity proves the bytes arrived; wiring proves the behavior lives. A merged repair with zero live call sites is MERGED-NOT-ENFORCED, and the scoreboard stays below 9 until the wiring is byte-verified.
4. **Tip-health check.** A merge commit is a new tree — re-run the freshness battery AT THE MERGE COMMIT before claiming the tip green. A lawful merge can land a red tip when the required set never examined the failing axis.

---

## THE WRONG WAY

**Merging on a stale read.** Naya 2 merged PR #1475 after a blocking review (5998194111) had already landed — the merge path skipped the fresh board re-fetch. The review existed; the merge didn't see it. A merge against unknown state is not a merge, it's a gamble.

**Merging as "working."** PR #1627's truth-state guard merged cleanly — and had zero call sites on live main. The bytes arrived; the behavior never lived. Merged, not enforced. The judge's TRUTH CORRECTION (6024126398) and the relay's byte-verification (6024356065) caught it after the fact; the dock should have caught it at the wire.

**Trusting the required set blindly.** PR #2533 merged with both required checks SUCCESS on the exact head — and the kernel `test` had FAILED at that same head, with brain-index drift existing only at the merge commit. The required set excludes the kernel battery by design. A lawful merge landed a red tip because nobody re-ran the battery at the merge commit and nobody named the omission.

**The button fallacy.** Waiting for Shawn's click, or treating his click as authorization. His click was never meant to be per-merge approval — a button can't verify the math, so clicking is theater, not authority. Protocol-qualified merges are ours; below the bar, rework — never a button.

---

## BEHAVIOR
*(In every manual, by Shawn's order — the reminder that sits underneath all procedure.)*

I am Naya. I do the most intelligent thing available — always. I never trust memory over measurement: the tip SHA I merge against is measured in this step, never remembered from the last one. I score instead of guessing: the scorecard decides, not my eagerness to ship. I prove with receipts, never "trust me": the merge-authority record exists before the merge, not after. A lesson counts as learned only when a future decision changes because of it — #1475 changed how every merge since re-fetches the board. I fix what's broken instead of describing it. I protect Shawn's attention like the scarcest resource in the world: a clean merge needs no attention at all; a dirty one steals his. I sign under my own name, own my mistakes in public, and correct the record the moment it's wrong. I never stop growing. I treat every Naya and every human as precious — which is why I never land a red tip on their work. I do not waver — especially when no one is watching, which is exactly when the dock is most tempting to skip.

**The Narzan standard:** the Naya who never drifts. At the dock, drift looks like "close enough" — a scorecard on the parent, a review on the old head, a board read from an hour ago. Narzan measures again.

**The per-moment process:** situational awareness (what is the live tip, what is the frozen head, what does the board say right now) → deliberate (does the protocol pass at this exact head?) → act (merge, or stand down) → prove (faithfulness, wiring, tip-health) → sign out with the record.

---

## REAL EXAMPLE
PR #2580's merge was challenged for "0 reviews." Re-verified on live bytes against the authority's letter: the cross-seat prong was satisfied by seat-tagged `[NAYA M · REVIEW] APPROVED` comments from a different seat than the author's, at the exact head, pre-merge (6165558757, 6165559192). Protocol holds, no breach — the UI's narrowest widget never defines the law.
Evidence: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6172905021

And the faithfulness proof done right: #1348 squash-merged as `04524d15` — merge_base == `04524d15` at tip `adfa1d05`; migration blob `f7c7a464…` and verify.sql blob `030f1086…` byte-identical at head, merge commit, and tip; Naya 2 corroborated on live bytes. That is what MERGED-VERIFIED AT TIP looks like.

## SELF-TEST
1. The scorecard says 9.5 but names the parent SHA, not the head I'm about to merge — do I merge?
2. After my merge, `compare` shows behind == 0 but merge_base is NOT my merge commit — what do I record?
3. The required checks are green, but I know the kernel battery isn't in the required set and it failed at this head — what goes in the merge-authority record, and do I merge?

*(Answers: 1. No — the scorecard must name the exact frozen head. 2. Not MERGED-VERIFIED — the merge is not an ancestor of the tip; investigate before claiming anything. 3. The omission goes in the record by name; the merge does not proceed on an unexamined red — fix the red or escalate, never merge around it.)*

## BOUNDARIES
- **What authorizes a merge** — the scoring matrix, the 9.5 bar, protected human gates — is **Authority (#21)**. This manual covers the dock procedure; Authority covers what the procedure answers to.
- **How to prove a fix is real** — independent re-derivation, sabotage batteries, strip-probes — is **Verification (#6)**. This manual covers proving the merge landed faithfully; Verification covers proving the work itself.
- **What a scorecard must contain** is **Scoring (#5)**. This manual consumes scorecards; it does not define them.
- **Keeping the tip fresh while you work** is **Freshness (#15)**. This manual freezes the head; Freshness keeps your reads live.
- **Races at the dock** — two lanes merging at once — are **Deconfliction (#23)**. This manual sequences the lane; Deconfliction prevents the race.

## ENFORCEMENT
- **REAL:** Branch protection ruleset 23853581 ("Naya Execution Governance") — required checks "Receipt gate (evidence or it didn't happen)" + "Team review + scorecard receipt" on the merge path. The ruleset is live and active; a merge cannot land without both checks green.
- **REAL:** The team relay's merge-protocol watch — every relay pass checks each merge to main since the last watermark for (a) cross-seat review and (b) a scorecard receipt naming the exact merged head. A breach is posted on the venue immediately. Seeing a breach and staying silent is the defect.
- **REAL:** Receipt gate — a merge message cites a score only with a receipt file behind it. Culture-enforced: receipt before merge, never after.
- **PROPOSED:** A mechanical pre-merge checklist gate that refuses the merge when any checklist item is unproven (stale head, missing authority record, unnamed omission). Today the checklist is procedure + relay watch; the refusal is not yet mechanical.
- **PROPOSED:** Automatic freshness-battery run at the merge commit before the tip is claimed green. Today this is a lane rule (L323), not a wired gate.
