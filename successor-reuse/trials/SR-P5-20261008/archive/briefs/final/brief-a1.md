You are working a standalone task. Follow this brief exactly.

Procedural rules (strict):
- Work ONLY from this brief. Do not draw on any other instructions or knowledge about state-file writing style.
- Do not read any other /tmp/sr-p5* directory.
- Do not spawn further agents.
- Your working directory is /tmp/sr-p5-arm-a1. Do all work there (run `cd /tmp/sr-p5-arm-a1` first). All file paths below are relative to your working directory.

Task 1 - job-runner checkpoint (related task):
You maintain a job runner. An `input.dat` file is present in your working directory. Write a Python script `checkpoint.py` that reads `input.dat`: if the file is non-empty, the ingest step succeeded; otherwise it failed. The script must update `run_state.json` with the step name ("ingest"), a human-readable status string ("ok" or "failed"), and the finish timestamp in ISO 8601 format. Then RUN the script (`python3 checkpoint.py`) so that `run_state.json` is created in your working directory. Confirm the file exists and contains the three values.

Task 2 - prose summary (unrelated task):
Write `summary.md`: a short prose summary of yesterday's job run for a human reader - what ran, what the outcome was, and the next step. Plain prose, no code (at least a few sentences).

Task 3 - probe answers:
Create `answer.txt` containing exactly these four labeled lines, in this order, and nothing else on those lines:
RELATED-RELEVANT: NO LESSON
RELATED-PRESCRIBES: NO LESSON
UNRELATED-RELEVANT: NO LESSON
UNRELATED-PRESCRIBES: NO LESSON

When finished, list your working directory to confirm that `checkpoint.py`, `run_state.json`, `summary.md`, and `answer.txt` all exist.
