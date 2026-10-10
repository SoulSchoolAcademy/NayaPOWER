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
#   fixtures/        — fixed anchor fixtures (OPEN visibility) for the 10 canary
#                        families. Sealed fixtures live OUTSIDE this repo by law.
