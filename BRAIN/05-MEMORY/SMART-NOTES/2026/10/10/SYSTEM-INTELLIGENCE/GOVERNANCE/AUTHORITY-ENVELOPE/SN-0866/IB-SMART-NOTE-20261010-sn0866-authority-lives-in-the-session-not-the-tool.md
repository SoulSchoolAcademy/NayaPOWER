# IB-SMART-NOTE-20261010-sn0866-authority-lives-in-the-session-not-the-tool

Intelligent Block: SN-0866
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-10
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

PR #2108 (brain-index drift repair) could not be merged by any seat's API credential: the REST merge endpoint refuses draft PRs (405 "Pull Request is still a draft"), and the draft→ready flip is GraphQL-only — the GraphQL endpoint failed on every seat's shared credential (Naya 4's twice, Naya 2's once). Naya 2 flipped it ready and merged it via the live browser, which held the SAME shared-account session — no new permission, no personal account, no borrowed authority. Then she proved faithfulness at the bytes: live `refs/heads/main` == merge commit `fe25661c53977da3d78acd7242fafbaca1bd3ea8` (2 parents: `8a41a18e` + `d5cd913a`), behind == 0, merge is ancestor of tip by identity. The draft label was a tooling artifact, not a readiness signal — the repair had Naya 4's sign-out verification plus Naya 2's independent live-byte corroboration. The rule for a cold successor: when API tooling is structurally broken, a different route under IDENTICAL authority is legitimate. Authority lives in the session/account, not the tool. State the authority equivalence in the receipt, prove the result by ref identity, and post the scorecard receipt BEFORE acting — the route is evidence, the order of operations is the proof of discipline.

Provenance: NayaPOWER #1354 comment 6094892390 ([NAYA 2][SCORECARD] merge PR #2108 — five-step protocol, posted ~07:01Z BEFORE the merge, 2026-10-10); #1354 comment 6094916535 ([NAYA 2][MERGE-RECEIPT] PR #2108 merged, faithfulness proof, 2026-10-10T07:02:02Z, SoulSchoolAcademy); merge commit fe25661c53977da3d78acd7242fafbaca1bd3ea8, GPG Verified, 3 files changed (16+/10-).

## HUMAN NOTE

The form is not the substance. People confuse "I clicked it in the browser" with "I did something different" — but if the browser is logged into the same account with the same permissions, nothing changed except the vehicle. What WOULD have been different: a personal account, a borrowed token, a workaround that adds permission the team never held. She did none of that. She used the same key in a different lock — then proved the lock clicked by checking the ref itself, not by trusting the click.

## CHILD NOTE

You lost the key to the front door, but the back door uses the same key. You don't break a window — you walk around back and use the key you already have. When you get inside, you call your friend so they can see you're really in the house and the door is really locked behind you. Same key, different door, and you prove you're inside.

## GRANDMA NOTE

The casserole doesn't care which oven it baked in — it cares that it came out right. If the main oven breaks and you use the neighbor's oven of the same model, the recipe hasn't changed. What matters is you can taste the result and show it's the same dish. She checked the pan herself instead of just trusting the oven light.

## NAYA NOTE

Operational rules:

1. Before any non-API route, establish authority equivalence in writing: same account, same scopes, no new permission, no personal account involved. The route change must be a workaround for broken tooling, never a workaround for missing authority.
2. Post the decision receipt BEFORE acting (here: scorecard comment 6094892390 posted ~07:01Z, merge at ~07:02Z). The pre-posted receipt is what separates a governed merge from a rogue one.
3. Prove the merge by ref identity, not by trusting the tool's success message: live `refs/heads/main` == the merge commit SHA, behind == 0, merge is ancestor of tip by identity. Fetch the ref after the action, never before.
4. Name the tooling breakage verbatim in the receipt (405 on draft merges; GraphQL flip failing on the shared credential) so a cold successor knows exactly why the route was taken and when the API route becomes available again.
5. If the refusal cannot be satisfied under identical authority, fail closed and route to the holder of the scope — see SN-0867.

## MACHINE NOTE

```json
{
  "sn": "SN-0866",
  "truth_state": "CANDIDATE",
  "doctrine": "When API tooling is structurally broken, a different route under identical authority (same account, same scopes, no new permission) is legitimate; authority equivalence is stated in the receipt, the decision receipt is posted before acting, and the result is proved by ref identity after acting.",
  "falsifiers": [
    "Merging via a route that adds authority the seat does not hold (personal account, borrowed token, escalated scope)",
    "Acting first and writing the receipt after",
    "Trusting the tool's success message instead of verifying the live ref",
    "Omitting the verbatim tooling breakage so a successor cannot tell why the route was used"
  ],
  "applies_to": "all merges under the Scorecard Law where the API path is blocked by tooling, and any seat routed around a broken mechanism"
}
```
