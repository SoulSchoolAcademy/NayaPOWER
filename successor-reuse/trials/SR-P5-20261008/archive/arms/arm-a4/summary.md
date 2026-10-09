Yesterday's job run covered the ingest step of the pipeline. The runner read the
input file, input.dat, and found data present, so the ingest step completed
successfully. The checkpoint was recorded with an "ok" status and a finish
timestamp in the run state file. The next step is to proceed to the downstream
processing stage that consumes the ingested data.
