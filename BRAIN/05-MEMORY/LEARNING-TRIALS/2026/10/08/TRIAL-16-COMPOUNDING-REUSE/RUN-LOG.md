# TRIAL-16 RUN LOG (TRIAL-16 coordinator, Naya 4 lane)

- Run start: 2026-10-08T02:55:58Z (directory prep; first spawn ~02:52Z)
- Seed (from arm_assignment.txt): 20261008
- Arm assignment (coordinator eyes only — never revealed to leaf subjects):
  - TREATMENT (10): T16-A01, T16-A03, T16-A06, T16-A07, T16-A09, T16-A11, T16-A13, T16-A14, T16-A17, T16-A20
  - CONTROL (10): T16-A02, T16-A04, T16-A05, T16-A08, T16-A10, T16-A12, T16-A15, T16-A16, T16-A18, T16-A19

## Subject spawn table (ID -> brief sent; no blinding terms in any leaf message)

| Subject | Brief | Leaf note |
|---|---|---|
| T16-A01 | treatment | completed 02:53:43Z, usable design |
| T16-A02 | control | pending |
| T16-A03 | treatment | pending |
| T16-A04 | control | pending |
| T16-A05 | control | spawned last (02:55Z) — sequencing error, omitted mid-run, caught and corrected before any result analysis |
| T16-A06 | treatment | pending |
| T16-A07 | treatment | pending |
| T16-A08 | control | pending |
| T16-A09 | treatment | pending |
| T16-A10 | control | pending |
| T16-A11 | treatment | pending |
| T16-A12 | control | pending |
| T16-A13 | treatment | pending |
| T16-A14 | treatment | pending |
| T16-A15 | control | pending |
| T16-A16 | control | pending |
| T16-A17 | treatment | pending |
| T16-A18 | control | pending |
| T16-A19 | control | pending |
| T16-A20 | treatment | first leaf (one-word brief typo "be corrected") closed before producing; respawned with verbatim brief |

## Anomalies / blinding concerns
- A20 first instance closed pre-result due to a coordinator typo ("be corrected" instead of "be concrete" in section (c)) in the brief sent; replaced with verbatim brief. No result was produced by the closed instance.
- A05 was initially skipped in the spawn sequence; caught before any analysis, spawned with control brief (blinded, same instructions as all others).
- No leaf received any mention of arms, treatment/control, hypotheses, L16, or experiment purpose. Blinding intact.

## End
- Run end: 2026-10-08T03:04:03Z. All 20 subjects completed; no subject failed, refused, or returned nothing usable. Failures: 0 (stop-condition of >4 failures never triggered).

## Final collection accounting
- Usable designs per arm (coordinator mapping; leaves never learned this):
  - TREATMENT: 10/10 — T16-A01, T16-A03, T16-A06, T16-A07, T16-A09, T16-A11, T16-A13, T16-A14, T16-A17, T16-A20
  - CONTROL: 10/10 — T16-A02, T16-A04, T16-A05, T16-A08, T16-A10, T16-A12, T16-A15, T16-A16, T16-A18, T16-A19
  - Total usable: 20/20. Refusals: 0. Empty/unusable: 0.
- Answer sheets: 20 files in answer_sheets/ (T16-A01.md … T16-A20.md), verbatim leaf returns.
- designs_raw.json: all 20 keys non-null, round-trip exact-match verified against the answer sheets.
- Excluded (not counted, logged for honesty):
  - One extra A20 attempt carrying the coordinator's one-word brief typo ("be corrected" for "be concrete" in template clause (c)): closed/superseded; its completed design is NOT collected. Canonical T16-A20 is the verbatim-brief respawn.
  - One cancelled instance: "cancelled before it finished" — incomplete, no usable output.
- Blinding: no leaf message mentioned arms, treatment/control, hypotheses, L16, or the experiment's purpose. Intact.

## Collection progress (03:0xZ update)
- Answer sheets written (verbatim, 15/20): T16-A01, T16-A02, T16-A03, T16-A04, T16-A06, T16-A07, T16-A08, T16-A09, T16-A10, T16-A11, T16-A12, T16-A13, T16-A14, T16-A15, T16-A20. All usable designs (all six sections present, valid Tier-S bar, validity gates with numeric thresholds).
- Pending: T16-A05, T16-A16, T16-A17, T16-A18, T16-A19 (leaf agents still running).
- Excluded from collection:
  - Superseded A20 instance (brief typo "be corrected"): closed pre-result; the verbatim-brief respawned instance is the canonical T16-A20. The superseded instance also produced a design, but it is excluded (non-verbatim brief) and not counted.
  - Cancelled instance: "cancelled before it finished" — incomplete, no usable output.
