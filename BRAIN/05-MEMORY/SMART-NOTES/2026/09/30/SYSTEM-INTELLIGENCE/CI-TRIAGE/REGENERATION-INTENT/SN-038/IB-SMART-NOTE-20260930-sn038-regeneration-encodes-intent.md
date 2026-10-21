# Regeneration Encodes Intent, Not Accident

**Intelligent Block:** IB-SMART-NOTE-20260930-sn038-regeneration-encodes-intent
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Gate PR #1224's `test` check went red on `regenerate_brain_index.py --check` (exit 2): the deliberate pin `EXPECTED_DOMAIN_COUNTS["03-KERNEL"] = 27` was stale against both main (28) and the branch tree (36 = 28 main + 9 new master specs/scorecard − 1 removed `0005` Ultimate-Lock file). The mechanical repair is obvious — bump the pin to 36 and regenerate the checked-in index artifacts. The durable lesson is in what the repair proposal refused to do: it did NOT regenerate first and ask later. Regenerating an index canonicalizes whatever the tree currently holds, including an accidental deletion. The builder lane therefore proposed the repair but asked the branch author an explicit open question before baking: is the `0005` Ultimate-Lock removal deliberate? The overnight operating letter names the Ultimate Lock as the semantic authority — regenerating the index over an accidental removal would have canonicalized the accident. The rule: before any `--check`-to-regenerate repair, reconcile the tree-state arithmetic (what changed, on purpose or by accident), confirm removals are deliberate, and only then bake state into checked-in artifacts. Regeneration is a truth-write; truth-writes require intent evidence.

## 🩷 HUMAN NOTE

Making the test green isn't just changing a number — the regeneration step writes the current state of the tree into the official index. If something in the tree is there by accident (like a file that was deleted unintentionally), regenerating would permanently bless the accident. Always ask "was this removal on purpose?" before you bake.

## 🟣 CHILD NOTE

If you redraw the treasure map from what you see on the island, and someone accidentally threw a landmark into the sea, your new map will leave it out forever. Check that the island looks the way it's supposed to before you draw the new map.

## 🔵 GRANDMA NOTE

It's like reprinting the family recipe book from memory — if a page fell out by mistake, the reprint would lose the recipe for good. Before you reprint, make sure no pages fell out by accident.

## 🟠 NAYA NOTE

When a `--check`-style guard fails because a hard-coded pin drifted from the tree: (1) step-decompose first (SN-021): which step failed, what does it compare; (2) reconcile the arithmetic against BOTH main and the branch — the pin here was stale vs main (27 vs 28) too, not just the branch; (3) enumerate every tree-state delta and mark each deliberate vs accidental — a removal that is an accident must be restored, not baked; (4) only then regenerate the checked-in artifacts; (5) when the removed item is a named authority (here the Ultimate Lock), require the branch author's explicit confirmation of intent — propose-first per the lane protocol (SN-019), never bake-first. A red guard after a head advance is structural drift, not a flake — it deserves reconciliation, not a re-run.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": [
    {"board": "5926241703", "event": "#1224 test red root-caused", "defect": "EXPECTED_DOMAIN_COUNTS[03-KERNEL]=27 pin vs 36 files in branch tree", "step": "regenerate_brain_index.py --check exit 2; pytest green", "survived_head_advance": "34f8b8bd -> 19abcf2f"},
    {"board": "5926327574", "event": "builder-lane repair proposal (Naya 4)", "arithmetic": "28 (main a726a837) + 9 (0006 + 8x 0002-MASTER-SPEC) - 1 (0005 removed) = 36", "pin_also_stale_vs_main": "27 vs 28", "open_question": "is the 0005 Ultimate-Lock removal deliberate?", "no_action_taken": "propose-first per lane protocol"},
    {"boundary": "regeneration is a truth-write; verify intent before baking; protected merge gate unchanged (#1224 merge = Shawn)"}
  ],
  "rule": "regeneration_encodes_intent_not_accident",
  "protocol": [
    "step-decompose the CI failure before touching code (SN-021)",
    "reconcile pin vs tree arithmetic against main AND branch",
    "enumerate tree-state deltas; classify each deliberate vs accidental",
    "require explicit author confirmation when a removed item is a named authority",
    "only then bump the pin and regenerate checked-in artifacts",
    "never bake-first; propose-first on another lane's branch (SN-019)"
  ],
  "related": ["SN-019 (direct lane protocol)", "SN-021 (CI exit-2 triage)", "SN-031 (classify-before-code)", "SN-036 (push-run CI evidence)"]
}
~~~
