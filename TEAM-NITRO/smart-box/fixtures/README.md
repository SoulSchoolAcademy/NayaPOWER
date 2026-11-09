# Fixtures — verbatim copies of the real sources the proof runs on

These files are the real data, not samples and not invented. The test
suite reads them from its own directory so a different seat re-running
it from a clean checkout gets the same result.

## Smart notes (3)

- `SN-2535-what-naya-does.md` — "What Naya Does — Daily Reports, Smart
  Notes, Naya Notes, and Pages", SN-2535. Decoded from GitHub
  `BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/PRODUCT/SN-2535/IB-SMART-NOTE-20261109-sn2535-what-naya-does.md`,
  blob `9328c68cadab4f87e14aecaf8503eea6f2b2522e`, 14,199 bytes,
  sha256 `7c2ffb95faaddba5f69a6af575593c47b1c4dfd4717a57622a82f5f6c05b1c9f`.
  The local working copy at `~/workspace/sn2532-fix/what-naya-does-sn2535.md`
  was 0 bytes, so it was NOT used — the GitHub blob is the source.
- `SN-2543-smart-box-cure-saving-sickness.md` — "The Smart Box Is the
  Cure for the Saving Sickness", SN-2543. Byte-identical copy of
  `~/workspace/team-nitro/smart-notes/SN-2543-smart-box-cure-saving-sickness.md`,
  sha256 `50224d96505d7a7d2363b85c5817d823045e3d9ced370590a365b8870d8554ed`.
- `SN-2545-super-brain-is-yours.md` — "The Super Brain Is Yours", SN-2545.
  Byte-identical copy of
  `~/workspace/team-nitro/smart-notes/SN-2545-super-brain-is-yours.md`,
  sha256 `1729b35ec9606e6c6adc974e240fa1df10e3258a7119bb7a995c053a6639239d`.

## Smart Box entries (3)

- `smart-box-entries.json` — SB-0001, SB-0002, SB-2086, extracted
  verbatim from the canonical store
  `~/workspace/nitro-smart-box/store/entries.jsonl` (2,086 entries,
  2,816,102 bytes, 2026-11-06 snapshot — the source the live
  `nayanet.app/smartbox` snapshot came from; the live page served
  2,088 entries on 2026-11-09 19:12Z, HTTP 200).
  - SB-0001, dictation, 2026-11-04 — "THE WISE ONE", the first entry.
  - SB-0002, law, date UNSOURCED — "PRIVACY LAW", the edge case: its
    date stays "UNSOURCED" in the block, never guessed into a real date.
  - SB-2086, system-map, 2026-11-06 — "[SYSTEM-MAP] LINKED", the latest
    entry in the store.

No Supabase table backs the live Box — the scout
(`~/workspace/team-nitro/smart-box-real/SCOUT-FINDINGS.md`) proved the
live data is a Cloudflare KV snapshot of this same `entries.jsonl`, and
no Box table exists in Supabase. So the store file, not a table query,
is the honest source of the real entries. If the store is re-harvested,
re-extract these three ids and re-run the suite.
