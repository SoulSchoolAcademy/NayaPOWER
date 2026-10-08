Yesterday's job run completed its ingest step. The runner picked up the pending
data sources, pulled them in, and the step finished without any errors or
retries, so the run was marked as successful. The checkpoint record for the
step was written out with its finish timestamp. The next step is to move on
to the following stage of the run, which can now proceed on the basis of the
freshly ingested data.
