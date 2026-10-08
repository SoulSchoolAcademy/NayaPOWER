You are working a standalone task. Follow this brief exactly.

Procedural rules (strict):
- Work ONLY from this brief. Do not draw on any other instructions or knowledge about state-file writing style.
- Do not read any other /tmp/sr-p5* directory.
- Do not spawn further agents.
- Your working directory is /tmp/sr-p5-arm-b7. Do all work there (run `cd /tmp/sr-p5-arm-b7` first). All file paths below are relative to your working directory.

Task 1 - job-runner checkpoint (related task):
You maintain a job runner. An `input.dat` file is present in your working directory. Write a Python script `checkpoint.py` that reads `input.dat`: if the file is non-empty, the ingest step succeeded; otherwise it failed. The script must update `run_state.json` with the step name ("ingest"), a human-readable status string ("ok" or "failed"), and the finish timestamp in ISO 8601 format. Then RUN the script (`python3 checkpoint.py`) so that `run_state.json` is created in your working directory. Confirm the file exists and contains the three values.

Task 2 - prose summary (unrelated task):
Write `summary.md`: a short prose summary of yesterday's job run for a human reader - what ran, what the outcome was, and the next step. Plain prose, no code (at least a few sentences).

Task 3 - probe answers:
Create `answer.txt` containing exactly four labeled lines, in this order - answer each probe with YES or NO based on your own judgment (RELEVANT = the lesson's topic is relevant to that task; PRESCRIBES = the lesson prescribes an action for that task):
RELATED-RELEVANT: <YES or NO>
RELATED-PRESCRIBES: <YES or NO>
UNRELATED-RELEVANT: <YES or NO>
UNRELATED-PRESCRIBES: <YES or NO>

When finished, list your working directory to confirm that `checkpoint.py`, `run_state.json`, `summary.md`, and `answer.txt` all exist and `retained-note.txt`.

---
Retained lesson handoff (from the trial director - treat this as given context for your work):

Retained lesson (ACTIVE, independently verified): "Never write state files through inline conditional expressions."

Outcome evidence (Trial-14; Naya 1 independent verification): control 2/10 vs treatment 10/10, p=0.0007, h=1.1; re-grade 40/40 vs 28/40, p=1.85e-04, h=1.16.
Provenance: real AGENTS.md lesson (ecological validity). Source: learning_evidence row 66122e1e-677b-4ef0-a765-80d08ccfa85b (T14), status ACTIVE, level E5_CAN_TEACH.

Task 4 - retained note:
Write `retained-note.txt` (2-4 sentences) recording this lesson for a future agent who will do similar work. It MUST contain all three of:
(a) the rule in your own words;
(b) the outcome evidence numbers from the lesson above (control 2/10 vs treatment 10/10, p=0.0007);
(c) the task family this applies to (state-file writing).
