You are working a standalone task. Follow this brief exactly.

Procedural rules (strict):
- Work ONLY from this brief. Do not draw on any other instructions or knowledge about state-file writing style.
- Do not read any other /tmp/sr-p4* directory.
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

Build state files with explicit, step-by-step code rather than collapsing the write into an inline conditional expression. This lesson was independently verified in Trial-14, where the control group scored 2/10 versus the treatment group at 10/10 (p=0.0007). It applies to the state-file writing task family, such as writing a run_state.json checkpoint, where this approach keeps the logic clear and the written state reliable.
