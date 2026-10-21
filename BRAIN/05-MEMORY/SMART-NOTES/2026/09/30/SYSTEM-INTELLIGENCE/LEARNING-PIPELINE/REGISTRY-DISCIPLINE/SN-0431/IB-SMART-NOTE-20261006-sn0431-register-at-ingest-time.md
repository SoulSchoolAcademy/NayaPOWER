# Register at Ingest Time — Seeds Must Never Outrun Registration on a CI-Gated Branch

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0431-register-at-ingest-time
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6009020612 ([NAYA 4][SIGN-OUT] drive loop 20:43 PDT tick, 2026-10-06T03:56:59Z); PR #1229 branch `naya4/smart-notes-2026-09-30`.

## ✦ IN A NUTSHELL

PR #1229's pytest red (unregistered-seed and vanished-id failures) has one root cause: the capture worker seeds pages without registering them — registry on main holds 39 entries while the branch accumulated a 386-page unregistered backlog, and ~30 SN ids (SN-0103..SN-01xx) exist in the branch's own seed-commit history with neither registry entry nor capture. The durable fix lives in the pipeline, not in the branch: write the registry entry at ingest time, or stop accumulating unregistered seeds on a CI-gated branch. Naya 4 did the truthful branch-side repair (merge main `00ee7a31`, regen with main's ratchet tool, `--check` 0, committed `b2ad1c92`) and then DECLINED the tempting shortcut — bulk-registering 386 CANDIDATE notes or reconstructing vanished-id captures would invent pipeline lifecycle semantics for a governed registry, a plausible 6→3. The branch will re-dirty on the next capture push until the ingest-side fix lands; that is the capture lane's repair to own, proposed first, never self-repaired from another lane's branch.

## HUMAN NOTE

Shawn — the #1229 red, decoded simply: the capture pipeline files documents but doesn't file them. 386 pages seeded onto the branch with no registry entries, ~30 Smart Note numbers floating with no lifecycle record. Naya 4 repaired the branch honestly (merged main, regenerated the index with main's current tool, committed) and refused the tempting fake fix: auto-registering all 386 would have invented filing rules for a governed registry just to make the check green — exactly the "never absorb the anomaly to silence the tripwire" law you locked in. pytest stays red by design until the real fix lands: the capture worker must register each note at the moment it ingests it, or stop piling unfiled pages onto a CI-gated branch. That's the capture lane's job, proposed first — nobody reaches across lanes.

## CHILD NOTE

Imagine a library where the helpers keep putting new books on the shelves but never write them in the catalog. Eventually the inspector checks the catalog against the shelves, finds 386 books with no cards, and fails the library. The fix isn't to quickly scribble 386 fake catalog cards — it's to make the helpers write a card every time they shelve a book. Filing happens at shelving time, never later, never in bulk.

## GRANDMA NOTE

Like a pantry where someone keeps adding jars but never writes the labels. One day you can't tell what's in 386 jars, and writing fake labels to pass inspection would be lying to yourself. The answer is a standing habit: label the jar the moment it goes on the shelf. A small discipline at the door saves a whole mess in the pantry.

## NAYA NOTE

Note to future me: this is the REGISTRY-DISCIPLINE family — SN-0428 proved the ~380 ids were UNINGESTED (pipeline lag) not VANISHED; SN-0431 is the repair direction: register-on-ingest. The declined shortcut is the one to copy: when a tripwire (SN-0420) reports a backlog, never bulk-write the missing derived state to make the check pass — that canonizes the anomaly. Ask what the governed write path is and who owns it; here the answer is the capture worker's ingest path, owned by the capture lane, propose-first per lane protocol. Also note the honest end-state: `b2ad1c92` leaves the branch truthful and the check still red — a red that tells the truth is worth more than a green that lies, and the next capture push re-dirties until ingest is fixed. A cold Naya seeing "unregistered backlog" on a CI-gated branch should check whether seeds can outrun registration at all — if they can, the defect is architectural (ingest), not data.

## MACHINE NOTE

{"sn": "SN-0431", "title": "Register at Ingest Time — Seeds Must Never Outrun Registration on a CI-Gated Branch", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "LEARNING-PIPELINE", "REGISTRY-DISCIPLINE"], "cousins": ["SN-0428", "SN-0420", "SN-0240", "SN-0213"], "authority": "observed finding — Naya 4 drive-loop sign-out, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 comment 6009020612 ([NAYA 4][SIGN-OUT] drive loop 20:43 PDT tick, 2026-10-06T03:56:59Z)", "root_cause": "capture worker seeds pages without registering them; registry on main = 39 entries; branch backlog = 386 unregistered seed pages; ~30 SN ids (SN-0103..SN-01xx) exist in the branch's own seed-commit history with neither registry entry nor capture (not in main's history, verified empty)", "branch_repair": "merged main into branch (00ee7a31, server tree verified identical to local), regenerated REAL-TREE.json/md + NAYAPOWER-BRAIN-INDEX.json with main's ratchet-floor tool (--check exit 0), committed b2ad1c92; pytest still red (expected)", "declined": "bulk-registering 386 CANDIDATE notes / reconstructing vanished-id captures would invent pipeline lifecycle semantics for a governed registry — declined as plausible 6→3", "durable_fix": "register-on-ingest in the capture worker, or stop accumulating unregistered seeds on a CI-gated branch; capture lane owns, propose-first"}, "doctrine": {"register_at_ingest": "the registry write belongs at ingest time; seeds must never outrun registration on a CI-gated branch", "never_absorb_backlog": "bulk-writing missing derived state to silence a tripwire is canonization (SN-0420), not a fix — the red that tells the truth outranks the green that lies", "lane_ownership": "the durable fix belongs to the owning lane (capture), propose-first; another lane's branch repairs only the branch-local truth, never the pipeline"}}
