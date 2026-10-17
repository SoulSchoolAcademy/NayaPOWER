# IB-SMART-NOTE — SN-1538

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/VERIFICATION/REVERIFICATION-DISCIPLINE

## IN A NUTSHELL

"Just regenerate it" is a hypothesis, not a plan. Before any mechanical regeneration overwrites artifacts, the protocol is: backup everything, run the builder, byte-diff, and let the bytes decide whether regeneration is safe. On 2200-lane9 the bytes said no: the builder reproduced only 5 of 8 outputs — the regenerated rubric.md had LOST the "## Proof query text (declared deviation)" section, queries.json dropped its query_note fields, and an arm.py diff sat uncharacterized. The hand-edits were not stale residue; they were load-bearing documentation the builder could not produce. Blind regeneration would have destroyed them; the restore from backup (rubric.md back to sha256 8291a7d0) was the intelligent move. The deeper root cause: the builder is INCOMPLETE, not merely bypassed — the real fix is builder surgery (teach it to generate the proof-query-text section), not a mechanical re-run. A builder's output space can be strictly smaller than the artifact's content; only the diff measures that gap before destruction does.

## HUMAN NOTE

Someone said "the file was edited by hand, so just rebuild it from the tool and overwrite it." Sounds efficient — but the tool was outdated. It didn't know about content people had added later, and overwriting would have deleted that content silently. The rule before any "rebuild and replace": run the tool, compare its output against what's actually there, and only replace if the comparison comes back clean. If they differ, the tool needs fixing — not the file.

## CHILD NOTE

You were told "the toy machine is broken, just press the button and replace everything it made." But the button machine was missing a part — the new pieces came out broken. Good thing you checked one piece against the real thing first, instead of throwing the whole pile away. Always compare before you replace: the machine might be the broken one, not the pile.

## GRANDMA NOTE

Dear, the electric grinder jammed, so someone said "just throw the hand-ground batch and run it all through the new mill." But the new mill's finest setting was broken — it would have ruined the good grind. Good thing we tested one handful first and kept the rest. Sweetheart: test the machine against what you have before you let it eat what you have.

## NAYA NOTE

Future Naya: never execute a "regenerate from builder" brief as a blind overwrite. The three-step pre-regeneration gate is: (1) BACKUP all builder outputs (named directory, all files); (2) RUN the builder; (3) DIFF builder output vs on-disk, byte by byte. An empty diff means the mechanical fix is safe — proceed. ANY substantive diff means the builder and the artifact evolved on independent tracks: HALT the overwrite, restore the backups byte-identical (verify with sha256), characterize the divergence, and re-scope the work as builder surgery (a code brief, not a regeneration brief). The tell from this pass: "hand-edited rather than regenerated" is ambiguous — hand-edits can be drift OR they can be content the builder never learned to produce. The diff decides which. Log the builder's divergent files in the receipt so the next seat inherits the map, not just the verdict. And keep the backups until the regenerated tree is verified — restores are cheap, reconstructions are not.

## MACHINE NOTE

```json
{
  "sn": "SN-1538",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T07:45:00Z",
  "applies_when": [["regeneration","builder"],["gap","artifact"],["mechanical","re-run"],["artifact","overwrite"]],
  "enforcement": "Pre-regeneration gate: no regeneration brief executes an overwrite without (1) backup of all builder outputs to a named directory, (2) builder run, (3) byte-diff against on-disk artifacts. Any substantive diff halts the overwrite (restore backups, verify sha256) and re-scopes to a builder-surgery code brief. The brief template's regeneration section requires the backup path + diff summary in the receipt; the receipt-gate treats a regeneration receipt without a diff summary as incomplete.",
  "evidence": [
    "gap-20261017-0045-clarity.md (2026-10-17 ~00:45 PDT): builder bin/build_t0412_baseline_battery.py run against batteries/t0412-baseline/ — 3 of 8 outputs differed: rubric.md (on-disk '## Proof query text (declared deviation)' section the builder never generates; regenerated version shorter, loses it), queries.json (on-disk lacks builder's 'manual-picks stripped' prefix but carries 'query_note' fields the builder omits), arms/tfidf-t0412/arm.py (diff uncharacterized)",
    "restore: all 8 files restored from /tmp/rubric-backup/, rubric.md verified back to sha256 8291a7d0",
    "deeper root cause: builder INCOMPLETE not merely bypassed — real fix is builder surgery (generate proof-query-text section + query_note fields), scoped as a future code brief"
  ],
  "falsifiable_by": "a builder run that reproduces the artifacts byte-identically (empty diff) — the diff protocol itself falsifies 'regeneration is unsafe' for that case and the mechanical overwrite proceeds; if empty diffs are the norm across regenerations, the lesson's cost/benefit flips and the gate drops to a fast-path",
  "mechanism": "builders and their hand-maintained artifacts evolve on independent tracks; hand-edits can add content (proof-query-text sections, query_note fields) the builder's code path never learned to emit, making the builder's output space strictly smaller than the artifact's content set. Blind overwrite maps the larger set onto the smaller one — destroying the difference. The byte-diff measures the set gap before destruction, converting an irreversible guess into a reversible measurement."
}
```
