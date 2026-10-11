# Dead in Prose Is Not Dead in Code — Move Every Machine-Readable Reference

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0987-dead-in-prose-not-dead-in-code
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/LAW-IS-CODE

## IN A NUTSHELL

The overnight audit caught a law that is dead on paper and alive in the machinery: `kernel/protocol/MIGRATION.md` says `tools/protocol/` is superseded — dead, do not use — while the machine-readable `kernel/protocol/protocol_manifest.json` still points its checks (SN-0522/0523/0493) at `tools/protocol/checks/...`. A machine following the manifest reads and enforces law the team declared dead. The prose migration was written; the code migration was not finished. Death declared in prose is not death in code.

The durable rule: **a deprecation is not complete until every machine-readable reference has been moved.** Before declaring anything superseded, retired, or "do not use," grep every manifest, config, index, and registry that a machine could follow — then re-run the machines that consume them and watch them go the new way. The MIGRATION.md table is a claim; the manifest is the execution. If they disagree, the machine wins and the law is a zombie. This one is a [YOUR CALL] for Shawn (law-as-code changes need his word); the lesson is mine to bank.

## HUMAN NOTE

Shawn — small catch from the night audit, already flagged for your call: the migration doc says `tools/protocol/` is dead, but the protocol manifest still points three law-checks at it — so any machine following the manifest is enforcing dead law. Lesson banked: retiring something means moving every machine-readable reference to it, not just writing "superseded" in a doc. The fix direction (repoint the manifest to `kernel/protocol/` or record why the old path stays) is your decision; I didn't touch it.

## CHILD NOTE

You told everyone the old clubhouse is closed — but the map on the wall still has a big arrow pointing to it, and new kids follow the map, not your announcement. Closing the clubhouse means taking down every map arrow, not just making the announcement. Rule: when you retire something, chase down every sign that points to it.

## GRANDMA NOTE

It's like telling the family "we don't use that old oven anymore" while the recipe book in the kitchen still says "preheat the old oven to 400." Anyone following the book will cook with the oven you retired. You have to cross out the line in the recipe book too — not just say it at dinner.

## NAYA NOTE

I treat deprecation as a two-phase commit: (1) declare it in prose (migration table, doc), (2) move every machine-readable reference (manifests, configs, indexes, registries) and re-run every consumer to prove it follows the new path. Phase 1 alone creates a zombie: humans believe it's dead, machines keep executing it. Before I say "superseded," I grep the repo for the old path across every file a machine could read, and I verify the manifest no longer resolves to it. When prose and manifest disagree, the manifest is the truth the system lives by — so I fix the manifest.

## MACHINE NOTE

```json
{
  "sn": "SN-0987",
  "slug": "dead-in-prose-not-dead-in-code",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "LAW-IS-CODE"],
  "authority": "distillation tick 2026-10-11 07:08 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "flag": "night-shift-2026-10-10/morning-flags.md flag 1 (2026-10-11) — [YOUR CALL], verified against main tip 57e935c1",
    "prose_death": "kernel/protocol/MIGRATION.md table row: tools/protocol/ | Superseded — dead, do not use",
    "code_life": "kernel/protocol/protocol_manifest.json checks SN-0522/0523/0493 still point at tools/protocol/checks/... — a machine following the manifest enforces law declared dead",
    "resolution_status": "unresolved; repoint-manifest vs keep-old-path is Shawn's call (law-as-code change)"
  },
  "rule": "deprecation_is_not_complete_until_every_machine_readable_reference_is_moved",
  "procedure": [
    "before declaring anything superseded/retired, grep every manifest, config, index, and registry for references to the old path",
    "move every machine-readable reference, then re-run the consumers to prove they follow the new path",
    "when prose and manifest disagree, the manifest is the executed truth — treat the disagreement as the defect",
    "a migration table row is a claim; only the moved references make it true"
  ],
  "related": ["SN-0911 (requested review not landed = hold, not race)", "SN-0881 (freshness law — re-anchor at action time)"]
}
```
