# Master Box Recovery Test — instructions for a DIFFERENT seat

**Who runs this:** a seat that did NOT build the master box. The builder's own checks (the gate matrix and the spot-checks in `test_master_box.py`) are preparation, never proof. The recovery test is the verification.

**What you get, and nothing else:** this master-box directory as filed on GitHub (branch `smart-box/master-box-20261110`, `TEAM-NITRO/smart-box/master-box/`), plus the canonical sources its block pointers resolve to (`where.github_path` / `source` on each block). You do NOT get the build brief. You do NOT get the builder's report.

**The test:** recover each item below from the master box alone, and name the block id it came from.

1. The Oath, verbatim.
2. The Oath of Honor, verbatim.
3. The Five Gates.
4. The mission.
5. The permission rules — all three kinds: mail/messages, Naya Notes, Smart Notes.
6. The Naima meaning — what Naima is, and what it is not.

**Pass bar:** all six recovered, every claim traced to a block id, every quoted word matching the canonical source it points to. If any item needs the brief, the build failed and gets fixed — it does not get reported as done.

**Also check, and report:** that no block holds mail, message, or Naya Note content; that no personal box's contents are present (the children block must hold ids only); that the gate matrix in `test_master_box.py` re-runs green on your machine (`python3 test_master_box.py`, exit 0).

**Your report is the verification record.** File it beside the box (same branch) as `RECOVERY-TEST-REPORT-20261110.md` and report back: recovered items with block ids, gate-matrix result, and anything you could NOT recover.
