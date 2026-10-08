Yesterday's job run executed the ingest step. The step read the
input data file and checked it for content. The file was found to
be non-empty, so the ingest succeeded and the run was recorded as
"ok" in the job's run state. The outcome of the run was therefore a
clean, successful ingest with no errors reported. The next step is
for the downstream processing to pick up the ingested data and
continue the pipeline from this successful checkpoint.
