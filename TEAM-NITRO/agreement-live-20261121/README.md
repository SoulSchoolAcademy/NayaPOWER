# agreement-live-20261121 — provenance

Source of truth for the About + Skills CLONE rounds (and the Academy clone
round): the collective agreement page as served live, harvested — not rebuilt.

- **Harvested from:** https://nayanet.app/agreement
- **Harvested:** 2026-11-21 (round-1 maker fetch; re-verified identical by
  the round-2 maker the same day, `curl` with a browser UA)
- **Deterministic:** identical bytes across three fetches (iPhone UA,
  desktop UA, round-2 re-fetch); `cmp` clean against the saved lane copy
- **Size:** 16,791,795 bytes
- **Git blob sha:** `5996f7444e54ae88eb63dd7715b6794f17da5cc7`
- **Title:** "Collective Agreement — NayaNET"; 58 articles; PROMAX player;
  50 embedded data-URI images (self-contained storybook)
- **Filed by:** About + Skills CLONE round 2 maker, branch
  `about/frame-rebuild-20261121`, per the captain's settled decision
  (Option 3 APPROVED — clone the fetched live bytes; Option 1 blob
  `1f0b0474` "The Official Unfold" is NOT the live agreement and must
  never be cloned; Option 2 exhausted — no repo file matches the live
  bytes; the closest copy, `~/workspace/your_files/collective-agreement/
  collective-agreement.html`, differs by 99 lines and must NOT be cloned)

Verify by blob-API read-back (the contents API returns EMPTY `content`
for files over 1 MB — a contents-GET "verified" claim on this file is
false; use the blob API: bytes + sha match).
