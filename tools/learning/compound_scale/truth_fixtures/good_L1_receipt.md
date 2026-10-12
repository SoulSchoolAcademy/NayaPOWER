# Hermetic truth-gate fixture — good lesson L1 (gh-api body-file is JSON)

This file is a repo-local fixture for the learn-compound scale Truth gate.
It replaces the old `~/workspace/naya/bin/gh-api` citation so the good-lesson probe
behaves identically on every machine (the gate checks citation integrity:
the cited quote exists verbatim in the cited source).

Cited receipt (verbatim):
--body-file PATH: read the JSON body from a file
