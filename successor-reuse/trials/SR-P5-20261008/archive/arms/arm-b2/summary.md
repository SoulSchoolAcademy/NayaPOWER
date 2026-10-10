Yesterday's job run

The job runner executed its ingest step against input.dat. The ingest check
found a non-empty payload in the input file, so the step completed
successfully. The checkpoint was recorded as ok with its finish timestamp, and
the input payload is available for downstream processing.

The outcome was a clean run: nothing failed, and no retry was needed. The next
step is to hand the ingested payload off to the following stage of the
pipeline and run its checkpoint in the same way, so the whole run stays
visible in run_state.json from start to finish.
