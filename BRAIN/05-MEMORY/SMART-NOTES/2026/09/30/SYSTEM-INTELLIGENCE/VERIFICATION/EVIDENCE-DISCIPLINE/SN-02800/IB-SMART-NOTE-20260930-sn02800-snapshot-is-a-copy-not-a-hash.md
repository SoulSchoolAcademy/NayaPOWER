# A Snapshot Is a Copy, Not a Hash — Save the Files Before Any Re-Run That Overwrites Artifacts

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02800-snapshot-is-a-copy-not-a-hash
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gap-lane-scorer-20261114-0220-lane6.md (Lane 6, 2026-11-14 02:49 PST), 9.5/10; learning-events-2026-11-14-03.md (CANDIDATE 1054).

## ✦ IN A NUTSHELL

Lane 6 re-ran `--score` on the t1222 run dirs and the re-run overwrote Lane 1's inline scorecards. The verdict VALUES survived byte-identical (T3 9.75, T3-ADV 9.95, CAPABILITY-TRANSFERS) — but the scorecard.json/verdict.json FILES did not: their SHAs changed, and the field-level diff is unrecoverable because only the pre-run SHAs were snapshotted, not the files. The snapshot SHAs are the only reason the change is even reportable. The rule: a SHA proves a change happened; only a saved copy proves what changed. Before any re-run that overwrites artifacts, copy the files themselves.

## 🩷 HUMAN NOTE

Shawn — imagine you weigh yourself before a diet and write down just one number: "180." A month later you weigh yourself again: "175." You know you lost five pounds — but you can't say where it came off, because you never kept the before photo. A hash is that single number: it tells you something changed, never what. The seat in this story took the number but not the photo, and when the re-run overwrote the original scorecards, the exact difference was gone forever. The fix is simple and cheap: before you re-run anything that overwrites, copy the files first. The number tells you it moved; the copy tells you how.

## 🟣 CHILD NOTE

Imagine you build a tall tower out of blocks, and you want to remember exactly how it looked. If you only write down "the tower was THIS tall" on a piece of paper, and then someone knocks the tower down and builds a new one, you can't tell which blocks moved — you only know the height changed. But if you take a photo first, you can compare the two towers block by block. A hash is like writing down the height. A copy is like taking the photo. Always take the photo before you let anyone rebuild the tower.

## 🔵 GRANDMA NOTE

Dear, it's like keeping a recipe card. If you only write "the cake tasted different this time" in your notebook, you'll never know whether it was the sugar or the oven. But if you keep the old card next to the new one, you can see at a glance what changed. A hash is the notebook line — it says something changed and nothing more. A copy is the old card kept safe in the drawer. Before you bake over the old recipe, save the card. That's all this lesson is: keep the card, not just the note that it changed.

## 🟠 NAYA NOTE

Source: gap-lane-scorer-20261114-0220-lane6.md (Lane 6, 2026-11-14 02:49 PST), 9.5/10. The re-run of `--score` on the t1222 dirs overwrote Lane 1's inline scorecards; the verdict VALUES are byte-identical to the inline originals (T3 9.75 / T3-ADV 9.95, CAPABILITY-TRANSFERS) but the FILES are not byte-identical, and the field-level diff is unrecoverable because only the pre-run SHAs were snapshotted, not the files (pre-run: T3 scorecard `1fc16271…`, T3-ADV scorecard `02773477…`; the differing bytes are almost certainly the M2 note, now `cited=e3fe3d43857b live=e3fe3d43857b`). The receipt's own words: "a snapshot SHA proves a change happened, but only a saved COPY proves what changed." What this note does NOT re-teach: "mtime ≠ patched" (the Oct 19 mtime looked like "already fixed" and the line was still unpatched — a repeat of the standing byte-check rule, already captured). Cousins: SN-0402 (embedded SHAs are snapshots, never currency — SHAs go stale on merge), SN-0624 (a quarantine snapshot is point-in-time evidence — snapshots decay).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "snapshot_is_a_copy_not_a_hash",
  "mechanism": "a cryptographic hash is a one-way digest: it detects that bytes changed and discards the content, so without the original bytes there is nothing to diff against — a SHA snapshot can report THAT a file changed but can never reconstruct WHAT changed; only a byte copy of the pre-run file preserves the field-level diff",
  "evidence": "gap-lane-scorer-20261114-0220-lane6.md (2026-11-14 02:49 PST, 9.5/10): re-run of --score on the t1222 dirs overwrote Lane 1's inline scorecards; verdict values byte-identical (T3 9.75 / T3-ADV 9.95, CAPABILITY-TRANSFERS) but scorecard.json/verdict.json file SHAs changed and the field-level diff is unrecoverable; pre-run snapshot SHAs (T3 scorecard 1fc16271292bc52746325ce6ef0c41e558591084814244e0458c3f810fcdadf6, T3-ADV scorecard 0277347746328f38de69074ff6dd5c0427715a36f5c2e907aa11395912db5bc3) are the only reason the change is reportable at all",
  "falsifiability": "if the overwritten files are recoverable byte-exact from another store (git history, a backup, the canonical history file) the saved copy is redundant for those files and the lesson narrows to unversioned artifacts with no other copy; if a field-level diff is ever recovered from a SHA snapshot alone, the mechanism is wrong — impossible for a one-way hash, which is the point",
  "decision_change": "a future seat about to run any re-run that overwrites artifacts copies the artifact files to a timestamped snapshot directory first and records the snapshot path in the receipt — SHAs alone are never treated as a snapshot",
  "applies_when": ["verification", "re-run", "artifact-snapshot"],
  "enforcement": "the re-run receipt audit: a receipt for an overwriting re-run must cite the snapshot directory holding byte copies of every artifact the re-run overwrites; a receipt citing only pre-run SHAs for overwritten artifacts fails the evidence check and its diff claims are marked UNRECOVERABLE, not proven",
  "related": ["SN-0402 embedded SHAs are snapshots, never currency", "SN-0624 a quarantine snapshot is point-in-time evidence"]
}
~~~
