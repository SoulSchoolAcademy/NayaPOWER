# IB-SMART-NOTE — SN-01469

## Header

- Intelligent Block: SMART-NOTE
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured: 2026-10-16
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

An artifact that shares its filename with the next run is already deleted. Fixed filenames are a write-after-free on your own proof: the 12-hour sensitivity sweep clobbered the r3 probe evidence 44 seconds after the operative run, and the cited SHAs never resolved on disk again. The fix is structural, not discipline: write every operative artifact to a run-stamped filename, make canonical names symlinks repointed at the latest run ("latest" explicit, never an implicit overwrite), and treat "one canonical filename" as a bug on sight.

## HUMAN NOTE

Every researcher learns one hard truth: your proof is only as good as your ability to find it again. A six-hour measurement ran, passed, cited its evidence — and then a routine twelve-hour sweep wrote its own output over the same filenames forty-four seconds later. The proof was gone, not hidden: no archive, no undo. The repair wasn't a reminder ("be more careful") — it was a design change so care is no longer required: every run gets its own timestamped filename, so two runs can never collide; the friendly "latest" name becomes a signpost pointing at the newest run, not a second copy. Run the same probe twice, six seconds apart, and both runs' evidence sits side by side on disk, intact. When the scheme makes the wrong thing impossible, you don't need anyone to remember to do the right thing.

## CHILD NOTE

Imagine you and your sister both save your homework in a folder called "homework." Her file saves over yours — your homework is gone! The fix isn't "try harder to remember" — it's giving every homework its own name with the date on it, so they can never overwrite each other.

## GRANDMA NOTE

Dear, when you make jam, you label every jar with the date — two jars can't both be "the jam jar," or one of them gets thrown out by mistake. This is the same: date every batch of measurements, keep the pretty "latest" label as a little arrow pointing at the newest jar, and nothing ever gets lost.

## NAYA NOTE

The r3 evidence loss (gap-t0533) is closed at the class level, not the instance level. gap-gap-t0533-lane2 (2026-10-16, 9.2/10, 3 passes) wrote v2 probe (`t0533-compound-probe-v2.py`, `bff9b8650afd`) and v2 scorer (`t0533-compound-scorer-v2.py`, `a65c7e9c8bf6`): operative artifacts land on run-stamped names (`<arm>-<YYYYMMDDTHHMMSS.ffffffZ>.log / -verdicts.json`; scorer writes `<arm>-<probe_run_stamp>-score.json` bound to the log it scored) — no two runs can share a filename. Proven on live bytes: two probe runs six seconds apart produced two distinct stamped pairs; run-1's bytes were verified intact AFTER run-2 (score's `log_sha256` == run-1 log on disk) — the exact failure mode that destroyed r3. The sweep's own artifacts were retro-stamped (SHAs byte-verified before/after: `63acec2b492d` / `034101d171fe` / `cfa6843e0229`); the r3 replay bytes were hard-linked to run-stamped names (same inodes, zero duplication — grandfathered citations preserved AND the scheme satisfied). v1 instruments left byte-identical and marked SUPERSEDED (their cited SHAs preserved for the record). Scheme baked into `RUN-STAMPED-EVIDENCE-SCHEME.md` (`e1325f1490f7`) with the v1-superseded warning: v1 would write through the canonical symlinks — named, not hidden. Honest holes: the scorer's stamp is derived from the log's PROBE-START line, not the filename (accepted: logs are evidence, never edited); no retention/prune policy for stamped artifacts yet; v1 remains writable-through-symlink if anyone re-runs it (documented, not permission-enforced); second-seat replay still owed.

## MACHINE NOTE

```json
{
  "sn": "SN-01469",
  "slug": "run-stamped-evidence-retention-is-a-naming-scheme-problem",
  "captured": "2026-10-16",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "Evidence retention is a naming-scheme problem before it is a discipline problem: fixed filenames are a write-after-free on your own proof. Every instrument stamps its outputs from its first invocation (run-stamped filenames); canonical names are symlinks repointed at the latest run ('latest' explicit, never an implicit overwrite); 'one canonical filename' is treated as a bug on sight.",
  "decision_changed": "Every future probe/scorer/instrument author writes operative artifacts to run-stamped filenames from the first invocation, binds the score to the log it scored, and keeps canonical names as explicit-latest symlinks. A fixed-filename instrument is returned to the author on sight.",
  "falsifiability": "Two run-stamped runs landing on one filename (identical microsecond stamps) -> the scheme breaks. A stamped artifact clobbered anyway -> 'structurally impossible' is falsified. Either bounds this note.",
  "mechanism": "Fixed filename + re-run = write-after-free on your own proof — the 12h sweep did exactly what the filename scheme invited; no one misbehaved. Run-stamped names give each run distinct inodes by construction (proven: run-1 bytes intact after run-2 on live bytes); symlink-canonical makes 'latest' an explicit pointer instead of an implicit overwrite; hard-link retro-stamping preserves grandfathered citations with zero duplication. When the scheme makes the wrong thing impossible, you don't need anyone to remember to do the right thing.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-gap-t0533-lane2.md (9.2/10 3 passes: v2 probe bff9b8650afd + scorer a65c7e9c8bf6; two live runs 6s apart, run-1 intact after run-2; sweep retro-stamp SHAs verified; r3 replay hard-linked; scheme doc e1325f1490f7)",
    "hidden_files/twelve-lane-receipts/gap-t0533-lane2.md (the original loss: r3 cited SHAs 34fecf1a4829 / 29e8afe96464 absent on disk, clobbered by the 12h sweep 44s after the r3 run; frozen snapshot re-derived PASS 26/23 on read-only replay)",
    "hidden_files/learning-events-2026-10-16-03.md (CANDIDATE 463 'An artifact that shares its filename with the next run is already deleted' — this note is 463 promoted to SN with the v2 live-bytes proof)"
  ],
  "cousins": [
    "SN-1463 content-parity-not-file-presence-truth-gate (evidence law family; this note is the retention axis)",
    "SN-1467 stage-0-compound-fail-forward-dual-path-rule-validation (the arm whose evidence this scheme protects)",
    "SN-1466 guard-test-before-patch (same RED-first lineage)"
  ],
  "honest_holes": "scorer stamp derived from log PROBE-START line, not filename (accepted: logs are evidence, never edited); no prune policy for stamped artifacts; v1 writable-through-symlink if re-run (documented, not permission-enforced); second-seat replay of the v2 chain still owed"
}
```
