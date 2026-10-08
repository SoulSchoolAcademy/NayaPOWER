# Yesterday's Job Run — Summary

The scheduled job run executed its first step, the ingest stage, against the
expected input file. The input file was present and contained data, so the
ingest step completed successfully with no errors reported.

With the ingest step marked as successful, the checkpoint state was updated to
reflect the outcome. The next step in the pipeline is to proceed with the
downstream processing stages that depend on the ingested data, beginning with
whatever step follows ingest in the run configuration.
