Yesterday's job run executed the ingest step of the job runner. The input file
was present and non-empty, so the ingest step succeeded. The checkpoint script
recorded the step name, an "ok" status, and the finish timestamp into
run_state.json, which now documents the completed run. The next step is to
proceed with whatever processing follows ingest, using the validated input as
its starting point.
