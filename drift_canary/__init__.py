# Drift & Canary System — spec package (Shawn's directive, 2026-10-10)
#
# Governing principle: "Naya may learn from evaluation results, but it must not
# train, tune, promote, or certify itself using hidden evaluation answers."
#
# This package is SPEC + deterministic machinery. It is NOT wired into kernel/,
# KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word.
#
# Contents:
#   fingerprint.py   — calibration identity: binds every decision to the exact
#                        policy/model/verifier/environment/evidence/calibration
#                        under which it was qualified.
#   loops.py         — three monitoring loops (fast/medium/slow) as specs.
#   canary.py        — three-layer canary structure, open/sealed visibility,
#                        evaluation firewall rules.
#   contamination.py — five contamination-form checks (deterministic).
#   schedule.py      — tiered evaluation schedule + severity response ladder.
#   receipt.py       — canary run receipt schema (machine-readable).
#   revocation.py    — partial compromise & selective revocation: four units,
#                        six verdicts, six-step recomputation, ten rules.
#   uncertainty.py   — uncertain scope: two-boundary model, three-valued
#                        typed propagation, clearance packets, governance.
#   authority.py     — enforcement: five capabilities, purpose-bound
#                        authorization, anti-laundering, two checkpoints.
#   propagation.py   — provenance-preserving propagation, four layers:
#                        1. support-set evaluator, evidence-support envelopes,
#                           meaning envelopes + region verdicts + strongest
#                           defensible conclusion, four-surface rules mapped
#                           to existing CONNECT contracts (no parallel registry)
#                        2. composition: proof-obligation maps, compatibility
#                           gate, composition validity, breadth/depth/
#                           integration, four-part qualification report
#                        3. composite qualification audit: five questions,
#                           (E∧A)⇒C implication check, interaction contracts,
#                           environment difference map, four-verdict
#                           certificates, adversarial tests
#                        4. versioning/retiring obligations: immutable
#                           revisions, bitemporal receipts, change
#                           classification, migration receipts, affected
#                           closure, decision-boundary enforcement
#   migration.py     — split/merge proof migration: proof mapping
#                        (ENTAILS/PARTIALLY_SUPPORTS/DOES_NOT_SUPPORT/
#                        UNDETERMINED), two-direction audit (forward
#                        sufficiency + backward fidelity), migration
#                        certificates, interaction-proof layer (discovery,
#                        contracts, receipts, proof ladder), cold-successor
#                        reconstruction. Migrate evidence, not PASS labels.
#   liveness.py      — multi-node liveness & guaranteed progress: three
#                        liveness types (disposition / workflow progress /
#                        task completion), workflow state taxonomy with hard
#                        gates (WAITING_AUTHORITY can never become COMPLETED;
#                        liveness never creates permission), deadlock /
#                        livelock / starvation detection, progress witnesses
#                        (no invented progress), recovery validity (never
#                        weakens LAW), the conditional guarantee
#                        [](Eligible & Fair => <>Completed), append-only
#                        liveness receipts, cold-successor reconstruction.
#                        Safety and liveness are separate verdicts on the
#                        same interaction.
#   fixtures/        — fixed anchor fixtures (OPEN visibility) for the 10 canary
#                        families. Sealed fixtures live OUTSIDE this repo by law.
