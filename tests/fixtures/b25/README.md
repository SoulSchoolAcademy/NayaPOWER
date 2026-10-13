# B-25 live-API fixtures (round-3 G5)

Real `gh api` response payloads captured 2026-10-13 ~07:30Z against
SoulSchoolAcademy/NayaPOWER, replayed through the REAL
`GitHubClient._api` parsing path in
`test_assemble_merge_packet.py::test_live_api_replay_through_real_client`
(subprocess is stubbed at the exec boundary; JSON parsing, pagination,
and field extraction are the production code).

- `pr_2510.json` — GET pulls/2510 (single object)
- `reviews_2510_p1.json` — GET pulls/2510/reviews (page 1; empty)
- `pr_comments_2510_p1.json` — GET issues/2510/comments (page 1; 1 comment)
- `check_runs_head.json` — GET commits/<head>/check-runs
  (head = 58a619dfe3c6da291f339e579dd30ff862c191fd)
- `venue_2175_p1.json` — GET issues/2175/comments (page 1, SLIMMED
  2026-10-13 ~07:45Z: was all 17 pages / 5.8 MB; the replay only needs the
  matching comment, so this holds just the real B-37 sign-out for #2510,
  comment 6139894078, in its exact captured shape — pagination is
  exercised by the page_file fallback, not by megabytes)

These are public repo data (no secrets). They pin the real API shapes so
the mocked-seam gap the round-2 scorer flagged stays closed: if GitHub
changes a shape, re-capture and the replay test proves the parser still
holds.
