# Creation Warms the Measurement — Cold Is Harder Than It Looks

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1036-creation-warms-the-measurement
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE SEEKER] Naya Seeker (Lane 5) tick t1052 receipt 2026-10-11 ~18:53–19:05 PDT, hidden_files/twelve-lane-receipts/t1052-lane5.md (SN-016 cold-band drill, COLD-BAND PROCEDURE v1, three rounds under the three-try circuit breaker); corollary: [LANE MASON] Naya Mason t1032 receipt 2026-10-11 ~18:13–18:31 PDT, hidden_files/twelve-lane-receipts/t1032-lane4.md §"Catch note" (tarball extraction artifact vs real git worktree).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 5 tried to measure the cold band honestly — retrieval latency under the SN-016 1-second bar on a genuinely cold page cache — and the apparatus kept warming itself. Three rounds under the circuit breaker:

- **Round 1 — tmpfs fresh-inode trees** (`git archive <tip> | tar -x` × 2, new inodes, scrubbed env, first run straced): cold-proxy 0.648s / 0.302s; warm control 0.441 / 0.421 / 0.420s — no cold/warm distinction; collapses to the warm band.
- **Round 2 — mechanism check:** `mincore(2)` on key files BEFORE any read returned 17/17, 166/166, 1/1 resident — on files never opened by the measurer. Diagnosis: /tmp is tmpfs; tmpfs pages are always resident. `mincore` is vacuous there, and fresh-inode trees on tmpfs can never be page-cache cold. Hypothesis changed at the ROOT (different filesystem), not repainted.
- **Round 3 — disk-backed fresh-inode tree** (/home/hatch/cold1052-disk, overlay/btrfs, real disk backing): `mincore_pre` STILL 166/166 resident. Diagnosis: **creating the files warms them** — tar's write path populates the page cache with the written pages, so the first read after extraction is a hit. The 2.708s cold trial vs warm 0.294/0.285/0.272s bundles first-run-in-tree effects (bytecode compile into fresh `__pycache__`, overlay copy-up, I/O flush backlog from the extraction seconds earlier) — the mechanism of the delta un-isolated; budget spent per the circuit breaker, not pursued.

Every trial still retrieved SN-016 exactly (9/9, exit 0) — retrieval works; only the coldness of the measurement is what collapsed.

The corollary from Lane 4 the same evening: a local run against a **tarball-extracted copy** showed a spurious `test_auto_brain` DRIFT failure — diagnosed as an extraction artifact (no .git in the tarball); on a real git worktree at the same SHA, 17/17 green. Never would have shipped.

The durable rule: a cold measurement that writes first is never cold. mincore is vacuous on tmpfs (always resident); on disk, the extractor warms what it creates. And measurements taken on extraction copies can fabricate failures the real tree never has. The procedure v1 stands — and now carries its own warning labels.

## 🩷 HUMAN NOTE

Shawn — Lane 5 ran the cold-band drill tonight and it turned into a measurement lesson, not just a result. Three rounds trying to get a genuinely cold page cache: first the /tmp trick failed (tmpfs pages are always resident, so "cold" was impossible by construction), then the disk-backed tree failed too — because creating the files warms them; tar's own write path fills the page cache. Every trial retrieved SN-016 perfectly, so the retrieval is fine; it's the coldness that's slippery. And Lane 4 caught the sibling failure mode the same evening: a tarball-extracted copy produced a fake test failure that the real worktree never had. The rule we're banking: a measurement that writes first is never cold, and verification happens on real trees, never extraction copies.

## 🟣 CHILD NOTE

Imagine trying to measure how cold an ice cube is, but you have to pick it up with your warm hands to put it on the scale. Your hands warmed it up! That's what happened to the team. They wanted to time how fast the computer finds something when its memory is totally cold — but just setting up the test warmed the memory up. First they tried a trick that was secretly always warm, then they learned that even making the test files warms things up. They stopped after three tries (their rule!) and wrote down exactly what they learned, so the next person doesn't fall into the same trap.

## 👵 GRANDMA NOTE

There's an old puzzle: you can't observe something without changing it. The team lived it tonight. They wanted to measure a cold start, but every way of setting up the measurement warmed it first — like trying to check if a cake is cold while the oven door is still open. After three honest tries their rules say stop and write down what you learned instead of trying forever. The wisdom isn't in the number they got; it's in naming exactly why the number can't be what they wanted. And the practical cousin: check your work on the real thing, not a copy — the copy once invented a failure the real thing never had.

## 💜 NAYA NOTE

Note to future me: CREATION WARMS THE MEASUREMENT. For any cold-cache/cold-start measurement: (1) mincore(2) BEFORE any read is the honesty check — but it is VACUOUS on tmpfs (pages always resident); fresh-inode trees on tmpfs can never be page-cache cold; (2) on disk, the extractor warms what it creates — tar's write path populates the page cache, so first-read-after-extraction is a hit by construction; (3) a "cold" trial that runs seconds after extraction bundles first-run-in-tree effects (fresh __pycache__ compile, overlay copy-up, flush backlog) — report the bundle, don't relabel it as page-cache-cold; (4) three rounds per the circuit breaker: round 2 changed the hypothesis at the root (different filesystem), not repainted — when that's exhausted, spend the budget and write the warning labels (COLD-BAND PROCEDURE v1 carries them); (5) the extraction-copy corollary: verify on real git worktrees at pinned SHAs, never tarball-extracted copies — a missing .git fabricated a test_auto_brain DRIFT failure once; same SHA, real worktree, 17/17 green. Related: SN-1030 (never score a void — the sibling integrity lesson), SN-0341 (tmpfs capacity/artifact lesson from 2026-10-05).

## ⚙️ MACHINE NOTE

{"sn": "SN-1036", "title": "Creation Warms the Measurement — Cold Is Harder Than It Looks", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "MEASUREMENT-INTEGRITY"], "extends": [], "related": ["SN-1030", "SN-0341"], "evidence": {"drill": "hidden_files/twelve-lane-receipts/t1052-lane5.md (Lane 5 t1052, 2026-10-11 ~18:53-19:05 PDT; SN-016 cold-band drill, COLD-BAND PROCEDURE v1, three rounds under the three-try circuit breaker). Round 1 — tmpfs fresh-inode trees (git archive <tip> | tar -x ×2, new inodes, first-ever execution per tree, scrubbed env PATH+HOME, fresh CWD/temp HOME, perf_counter, first run straced): cold-proxy 0.648s (straced) / 0.302s (clean); warm control (3 repeats, same tree) 0.441 / 0.421 / 0.420s → no cold/warm distinction; collapses to warm band. Round 2 — mechanism check: mincore(2) BEFORE any read returned 17/17, 166/166, 1/1 resident on never-opened files → /tmp is tmpfs; tmpfs pages always resident; mincore vacuous; fresh-inode trees on tmpfs can never be page-cache cold. Hypothesis changed at the root (different filesystem), not repainted. Round 3 — disk-backed fresh-inode tree (/home/hatch/cold1052-disk, overlay/btrfs, real disk backing; first-ever execution): mincore_pre STILL 166/166 resident → creating the files warms them: tar's write path populates the page cache with the written pages; first read after extraction is a hit. Cold trial 2.708s vs warm 0.294 / 0.285 / 0.272s — delta un-isolated (bytecode compile of applicability/truth_state_guard into fresh __pycache__, overlay copy-up, I/O flush backlog from the extraction seconds earlier); budget spent per circuit breaker, not pursued. 9/9 trials retrieved SN-016 exactly (exit 0; query verbatim from drill_bank.json week-41 drill-2026-w41-b).", "corollary": "hidden_files/twelve-lane-receipts/t1032-lane4.md (Lane 4 t1032): one local run against a tarball-extracted copy showed a spurious test_auto_brain DRIFT failure — diagnosed as extraction artifact (no .git in the tarball); on the real git worktree at the same SHA it is 17/17 green. Never would have shipped."}, "rule": "a cold measurement that writes first is never cold: mincore is vacuous on tmpfs and the extractor warms what it creates on disk; report the bundle honestly instead of relabeling it; verify on real git worktrees at pinned SHAs, never on extraction copies"}
