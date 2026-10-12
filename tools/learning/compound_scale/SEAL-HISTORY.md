# Seal history (pre-registration integrity)

- **v1** `5024565f` sealed 23:36:29Z — debug run exposed a defective A3
  citation (contradicting quote not verbatim in the source). Seal refused
  the next run correctly.
- **v2** `aa8115ea` sealed 23:37:52Z — A3 citation corrected to the verbatim
  source text. Full run: 11/11 proven, 3/3 adversarial rejected, 14/14
  prereg matches (run in /tmp/scale-run2, superseded).
- **v3** sealed now — L11 capture source updated to the REAL error-signal
  loop event id (`le-20261011-2c1a5b65b5`, live scan 23:40Z, event file in
  `capture_proof/`). Citation fix only; no expectation changed.

No seal was ever re-issued after arm outcomes were used to move a bar.
Each re-seal fixed the registration's evidence pointers, never the
pass/fail thresholds.
- **v4** `30f7a6e9c` sealed 2026-10-12 12:38:03Z — hermeticity fix (t0292):
  all 14 `receipt_file` paths moved from the author's mutable home files
  (`~/MEMORY.md`, `~/AGENTS.md`, `~/TOOLS.md`,
  `~/workspace/agent-briefing-master.md`, `~/workspace/naya/bin/gh-api`)
  to pinned in-repo fixtures (`fixtures/receipts/*.md`) via the new `pkg:`
  scheme; quotes captured verbatim. Citation fix only; no expectation
  changed. (`gates._read_receipt` learned `pkg:`; legacy `~/` unchanged.)
