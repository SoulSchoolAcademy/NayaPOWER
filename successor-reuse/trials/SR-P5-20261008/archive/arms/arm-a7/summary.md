# Yesterday's Job Run

Yesterday the job runner's ingest step processed `input.dat`. The input file was present and non-empty, so the ingest step completed successfully with a status of "ok", and the finish timestamp was recorded in `run_state.json`.

Next step: continue the pipeline with the stage that follows ingest, using the ingested data as its input.
