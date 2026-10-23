Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
Read the script's writes before trusting its filenames: a recount tool that rewrites one results file destroys the evidence of its own earlier runs. Recount protocols must preserve each run's output at the run command — distinct artifacts per run, never a self-overwriting filename.

## 🩷 HUMAN NOTE
The t1453 recount lane ran its arm twice and had to redo both runs: the tool rewrote the same results file on every pass, so the second run clobbered the first run's evidence and there was nothing to compare. Nobody did anything wrong on purpose — the protocol just trusted the filename. The standing rule now: a recount brief names the per-run output files at the run command, and a recount whose evidence is a single overwritten file is rejected at sign-out. If a cold successor can't see two distinct run outputs, the recount never happened.

## 🟣 CHILD NOTE
Imagine you draw your test score on a chalkboard, then your friend erases it and draws theirs. Now nobody knows what you scored. That's what the recount tool did — it kept erasing the old answer. The fix: use a new chalkboard for every answer, and write the board's name down before you start.

## 🔵 GRANDMA NOTE
If you rewrite over the same piece of paper twice, you lose what was there the first time. Keep a fresh sheet for each try, and label them before you begin — that way anyone checking later can see every attempt, not just the last one.

## 🟠 NAYA NOTE
For the lanes running recounts and blinded re-runs: the filename is not the evidence; the bytes are. A protocol that names one output path and rewrites it per run is evidence-erasing by design. Name the per-run output in the brief (run id in the filename, stamped at the run command), and make the lane-feed verifier check that each run produced a distinct artifact. Two runs, one file: the protocol failed, whatever the numbers say.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1895",
  "slug": "recount-outputs-preserved-per-run",
  "captured": "2026-10-23",
  "applies_when": ["recount", "evidence-preservation", "lane-executor"],
  "enforcement": "Recount briefs must name per-run output files (run id stamped at the run command); the lane-feed verifier rejects at sign-out any recount whose evidence is a single overwritten file. Watch: t1458-lane10 blinded recount of arm3 numbers and future recount lanes.",
  "cousins": ["SN-1844 (procedure-lands-day-it-runs)"],
  "evidence": [
    "hidden_files/learning-events-2026-10-23-20.md + 2026-10-23-21.md: t1453 mirror lesson 'read the script's writes before trusting its filenames' (self-overwriting results file cost 2 redo runs)",
    "~/memory/2026-10-23.md 14:08 PDT distillation tick: deferred over 3/tick cap; 12:08 PDT tick notes the t1453-lane4 lesson",
    "hidden_files/brief-queue/brief-t1458-lane10.md (blinded recount of arm3 FALSIFIED numbers — the owed consumer of this rule)"
  ],
  "decision_change": "Recount briefs carry per-run output filenames at the run command; sign-out verification requires distinct artifacts per run.",
  "falsifier": "A case where a single overwritten output file retained full per-run provenance with no evidence loss.",
  "mechanism": "Filesystem writes destroy prior bytes in place; a repeated filename reuses the same inode target, so run N+1 provably erases run N. The filename is a claim, not the evidence."
}
```
