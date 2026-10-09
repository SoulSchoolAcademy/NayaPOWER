Yesterday's job run: the pipeline's ingest step read the incoming
payload from `input.dat` and completed normally. The input file was
non-empty, so the ingest was recorded as successful ("ok") along with
its completion timestamp in `run_state.json`. No errors or retries were
needed. The next step is to continue the pipeline past ingest — hand the
verified payload to the processing stage and record its outcome in the
same state file.
