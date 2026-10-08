# Yesterday's Job Run — Summary

Yesterday the job runner executed the scheduled daily run, beginning with the ingest step, which pulls the day's input data into the system. The ingest step completed successfully without errors, and a checkpoint was recorded capturing the step name, its successful outcome, and the finish timestamp. With the data now loaded, the next step is to run the processing stage that transforms the ingested data into the final output records.
