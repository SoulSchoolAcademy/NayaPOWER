Yesterday's job run covered the ingest step of the pipeline. The runner read the
day's input file, found it to contain the expected payload, and recorded a
successful outcome in the run state file. The state now shows the ingest step
as completed successfully, with the finish time noted for the record. The next
step is to move on to the downstream stage that consumes the ingested data, so
the run can proceed from where the checkpoint left off.
