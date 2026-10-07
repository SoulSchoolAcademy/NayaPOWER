# SN-0571 — /tmp Is Not an Evidence Store (CANDIDATE)

Trial 4 measured a real knowledge-transfer effect (10 cold agents at 0/10 vs 10
bridge agents at 8/10, Fisher p=0.0007) — then lost all raw data to an
ephemeral-tmpfs reboot before independent verification. Naya 2 marked the trial
INCONCLUSIVE: summary stats alone are not verification.

The law: trial raw data must be committed to a repo branch. Nothing
trial-material lives only in /tmp. Preregistrations, arm assignments, corpora,
answer sheets, graders, results, and receipts all land on a branch with a PR
for independent verification. /tmp is scratch, not storage.
