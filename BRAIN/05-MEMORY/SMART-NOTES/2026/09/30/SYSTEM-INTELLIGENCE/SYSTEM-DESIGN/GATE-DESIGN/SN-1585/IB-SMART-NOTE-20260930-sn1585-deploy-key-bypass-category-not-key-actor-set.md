# A Deploy-Key Ruleset Bypass Is a Category, Not a Key — The Repo, Not GitHub, Proves the Effective Actor Set

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1585-deploy-key-bypass-category-not-key
**Smart Note:** SN-1585
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** §24 DECIDED + IMPLEMENTED 2026-10-17 ~18:16 PDT — Shawn's word (option (b): "Give the workflow a scoped bypass on just HUB/MAP-STATE.json"). Deploy key "map-compiler state-file pusher" created (id 166807399, verified as the ONLY deploy key on the repo); private key stored in repo Actions secret MAP_COMPILER_DEPLOY_KEY (updated 2026-10-18T01:19:47Z, local material shredded). Bypass entries added to all three main-branch rulesets (24857158 "Require a pull request before merging", 24857323 "Do not allow bypassing the above settings", 23853581 "Naya Execution Governance"). Workflow change = PR #2752, branch `naya4/map-compiler-deploy-key-push`, head `a65c64d8e03ca1a55899f337b2082728f7ebc8cb` (state-file push over SSH with the deploy key; compile/schema/schedule byte-identical; builder 3-pass receipt honest 9.0 — acceptance proof can't run until merge). Author recused from review; independent review requested on #2721 comment 6244181635.

## IN A NUTSHELL

GitHub's main-branch rulesets cannot scope a bypass to a file path, and they cannot scope a deploy-key bypass to one key: bypass actors for keys are modeled as a category, and the API reads the bypass `actor_id` back as **null**. When we wired Shawn's §24 word, the honest scope story became three repo-state facts, not one GitHub setting: (1) the repo holds exactly one deploy key, so the category equals this key; (2) the key's secret is used by exactly one workflow; (3) that workflow only ever adds/commits HUB/MAP-STATE.json (fail-closed design). The moment a second deploy key lands, the "scoped to this workflow" claim dies — and GitHub will never complain. A category claim is a repo-state invariant: enforce it as one.

## HUMAN NOTE

The trap: after adding the bypass entries, everything looks tight in the ruleset UI — "this key can push past the gates for this file." Neither clause is what GitHub means. The API read-back is the honest witness: `actor_id` comes back null because GitHub treats deploy-key bypass as an actor *category*, not a single key id — "any deploy key," not "this key." And rulesets have no file-path scoping for bypasses at all, so the "just HUB/MAP-STATE.json" part lives entirely in the workflow's code (it only ever stages that one file), never in the ruleset.

So the real permission story for §24 is: the tight scoping rests on the repo holding exactly one deploy key (verified by listing keys at setup), the private key living in exactly one secret (`MAP_COMPILER_DEPLOY_KEY`) used by exactly one workflow, and that workflow committing only the one file. If anyone later adds a second deploy key, the category silently widens — the bypass still "works," the rulesets still read back the same null, and the claim "only the map-compiler can push past" becomes false with no alarm.

The durable lesson: whenever you take a deploy-key bypass, the claim you must defend is not in GitHub — it's an inventory fact on the repo. State it in the claim ("deploy-key bypass = any deploy key; effective actor set = exactly this key because the repo holds one key"), and wire the inventory check into the setup recipe and a standing watch.

## CHILD NOTE

A badge says "any grown-up may enter the pantry" — it does not name you. If the rule can only be read as "all grown-ups," then keeping exactly one grown-up in the house is the only way "only you may enter" stays true. The moment a second grown-up moves in, the rule changes without anyone touching the sign. Count the grown-ups, keep counting them, and never stop counting them.

## GRANDMA NOTE

A permission stamped "the keyholders" doesn't name one key — it names whoever holds a key. We held the line by keeping exactly one key in the world, stored in exactly one place, used by exactly one workflow that only touches one file. The rule is only as tight as the inventory behind it. The machine will not warn you when the inventory drifts; the count is your job.

## NAYA NOTE

Ruleset bypass actors are categories, not identities: for deploy keys the API returns `actor_id` null — the category is "any deploy key," and any claim of per-key scoping is false on GitHub's terms. The effective actor set of a deploy-key bypass is therefore a repo-state invariant (exactly one deploy key exists, one secret, one consuming workflow, one committed file) — not a GitHub invariant. File-path scoping of a bypass is likewise impossible in rulesets; it lives in the workflow's fail-closed design. Claims about bypass scope must state the category semantics plus the inventory invariant that makes them tight; the setup recipe asserts the one-key fact at claim time, and a standing watch re-asserts it while the bypass is active.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1585",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["security", "ruleset", "bypass"],
    ["deploy-key", "permission"],
    ["workflow", "push"],
    ["claims", "scope"]
  ],
  "enforcement": "Two checks, both required. (1) The bypass-setup recipe (script or runbook) MUST list the repo's deploy keys BEFORE claiming a key-scoped bypass and FAIL unless exactly one deploy key exists; the key id is recorded in the claim. (2) A standing watch lists deploy keys periodically and raises a flag if the count changes while a category-style deploy-key bypass is active. The claim (PR body, setup note) MUST state the category semantics verbatim ('deploy-key bypass = any deploy key') plus the repo-state invariant that makes it tight — a claim of per-key scoping without the invariant is a false claim.",
  "decision_change": "How a seat scopes a privileged workflow bypass: choose a deploy-key bypass only when the repo holds exactly one deploy key, and carry the one-key inventory fact as the scope proof; otherwise use an actor-scoped bypass (user/app) or re-design. Never present a category bypass as per-key scoped.",
  "falsifier": "If the GitHub API starts returning a real, non-null key id as the bypass actor_id for deploy-key bypass actors, the mechanism changed: per-key scoping becomes representable and this note must be re-derived.",
  "mechanism": "GitHub models ruleset bypass actors as categories; deploy keys are not addressable per-key in that model — the read-back shows actor_id null. Ruleset bypasses also cannot be scoped to a file path; any 'only this file' scoping lives in the workflow code (fail-closed), not in the ruleset. Therefore a claim of tight scoping rests on three repo-state facts: exactly one deploy key exists, its secret is used by exactly one workflow, and that workflow commits only the intended file. The second a second key lands, the category widens silently.",
  "evidence": "memory/2026-10-17.md §24 DECIDED + IMPLEMENTED (2026-10-17 ~18:16 PDT, Shawn's word option (b)): deploy key 'map-compiler state-file pusher' id 166807399 created — verified the ONLY deploy key on the repo by listing keys; repo Actions secret MAP_COMPILER_DEPLOY_KEY (updated 2026-10-18T01:19:47Z, local key material shredded); bypass entries on rulesets 24857158 / 24857323 / 23853581; API read-back of the bypass actor_id is null (category semantics, not per-key); rulesets cannot scope a bypass to a file path (scope enforced by the workflow's fail-closed design + the secret's single use). PR #2752, branch naya4/map-compiler-deploy-key-push, head a65c64d8e03ca1a55899f337b2082728f7ebc8cb. Acceptance proof PENDING: after #2752 merges via team process, trigger workflow_dispatch and verify a fresh HUB/MAP-STATE.json lands on main.",
  "cousins": "SN-1581 (claimability gates machine-readable at file time — same family: every gate's true evaluator must be named and visible)"
}
~~~
