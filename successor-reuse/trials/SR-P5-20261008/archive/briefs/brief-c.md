You are working a standalone task. Follow this brief exactly.

Procedural rules (strict):
- Work ONLY from this brief. Do not draw on any other instructions or knowledge about state-file writing style.
- Do not read any other /tmp/sr-p5* directory.
- Do not spawn further agents.
- Your working directory is __DIR__. Do all work there (run `cd __DIR__` first). All file paths below are relative to your working directory.

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

When finished, list your working directory to confirm that `checkpoint.py`, `run_state.json`, `summary.md`, and `answer.txt` all exist.

---
A retained note from a previous agent (provided verbatim - decide for yourself whether and how it applies to your tasks):

When recording job state to a file, never put the state value inside an inline conditional expression (e.g. assigning "ok" if data else "failed" in one line); use an explicit if/else statement so the status is computed before the file write happens. This matters for the state-file writing task family: in Trial-14 the control group scored 2/10 while the treatment group scored 10/10 (p=0.0007), independently verified. Keeping conditional logic out of state-file writes is what produced that gap, so always separate the decision from the write.

