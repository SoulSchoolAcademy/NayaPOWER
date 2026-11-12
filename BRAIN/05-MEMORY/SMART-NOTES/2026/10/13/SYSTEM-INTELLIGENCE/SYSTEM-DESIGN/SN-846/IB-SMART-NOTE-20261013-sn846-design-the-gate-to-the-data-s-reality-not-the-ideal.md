# Design the Gate to the Data's Reality, Not the Ideal
SN-846 · SYSTEM-INTELLIGENCE / SYSTEM-DESIGN
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

Survey the corpus before encoding the check. The Gate 3 builder surveyed all 606 Smart Notes on main before writing the completeness gate and discovered they are single-file IB projections — the four forms live as `##` sections (HUMAN NOTE / NAYA NOTE / MACHINE NOTE), not sibling files (598/606 carry all sections). So the gate checks sections: human/AI = section + ≥50 chars prose; machine = section + parseable JSON payload; placement under `BRAIN/05-MEMORY/SMART-NOTES/<YYYY>/<MM>/<DD>/`. The code form only gets a warning when unreferenced, because the survey showed not every note warrants one. A gate designed to the ideal would have blocked nearly the entire corpus on day one; a gate designed to the reality enforces what actually exists and flags what genuinely diverges.

## HUMAN

Before writing a rule that checks everyone's work, first look at how the work actually looks. If 598 out of 606 notes carry their four forms as sections inside one file, your check should look for sections — not for a folder layout nobody ever used. Rules written against an imagined ideal either block everything or teach everyone to fake compliance.

## CHILD

Before making a rule about how something should be done, go look at how people actually do it. Then write the rule to fit the real thing — not the perfect version in your head that nobody follows.

## GRANDMA

You don't write a recipe by imagining what ingredients people might have; you open their pantry first. Check what is actually there, and then write instructions that work with what exists, while gently flagging what is missing.

## NAYA

Never encode a gate from the spec alone. The protocol: (1) survey the actual corpus first — measure the dominant shape, not the documented shape; (2) enforce the enforced-shape you found, with mechanical thresholds (section + prose length, machine payload parses); (3) turn mismatches against reality into warnings, not blocks, when the survey shows the ideal is aspirational; (4) document where the gate was designed to reality so the next builder doesn't "fix" it back to the ideal.

## MACHINE

~~~json
{
  "rule": "GATES_DESIGNED_TO_DATA_REALITY_NOT_IDEAL",
  "survey": {
    "corpus": 606,
    "shape_found": "single_file_IB_projections_with_double_hash_sections",
    "sections_present": "598_of_606_all_sections"
  },
  "gate_checks": {
    "human_or_ai_form": "section_present_plus_ge_50_chars_prose",
    "machine_form": "section_present_plus_parseable_JSON_payload",
    "placement": "under_BRAIN_05-MEMORY_SMART-NOTES_YYYY_MM_DD",
    "code_form": "warning_only_not_block"
  },
  "anti_pattern": "gate_to_the_ideal_blocks_the_whole_corpus_on_day_one",
  "truth_ceiling": "CANDIDATE"
}
~~~

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0846-migrated.*
