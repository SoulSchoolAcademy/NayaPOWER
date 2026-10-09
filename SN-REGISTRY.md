# SN-REGISTRY.md — the Smart Note number registry

**Purpose:** one lookup — SN number → title → ratification status → canonical location(s) — so no future hunter repeats the SN-0732 "not found" hunt that turned out to be wrong (SN-0732 was in dated logs, smart-notes, and branches, just not on main).

**Built:** 2026-10-09, Naya 5 (SN-Registry Indexer seat), branch `naya5/sn-registry-index`.
**Authority:** this file is an INDEX, not a canon. It renames nothing, renumbers nothing, ratifies nothing.
**Rule of the registry:** "absent from main" ≠ "absent from the canon." Every entry below is quoted from its source; anything not source-verified is marked UNKNOWN, never invented.
**Collision resolution owner:** Shawn (Director-level arbitration: rename vs renumber) — flagged `PENDING-ARBITRATION` below per the hunter's report on #1354 (comment 6086369815).

---

## The index

| SN | Title (verbatim) | Status | Canonical location(s) |
|---|---|---|---|
| SN-0731 | the cold-Naya graduation test | DISTILLED — claimed "Shawn-ratified by construction" by the intake readers (see Evidence); **no steward-sequence smart note exists** | `~/workspace/naya-learning-intake/2026-10-09/raw/reader-I.md:121` ("[LAW] The cold-Naya graduation test (SN-0731)… (src: naya-100-laws-elite-interfaces.pdf)"); `INTAKE.md:307`; `NEW-LAWS.md:91`. Provenance line at `raw/reader-I.md:134`: "Distilled from Shawn's teachings 2026-09-30 → 2026-10-08… and SN-0731/0733/0734/0735." |
| SN-0732 | What It Means to Be a Naya | **RATIFIED by Shawn, 2026-10-09** (main chat) | `~/workspace/naya/smart-notes/SN-0732-what-it-means-to-be-a-naya.md` (header verbatim: "**Status:** RATIFIED by Shawn, 2026-10-09 (main chat)"; "**Category:** Identity / Ethics") + JSON capture `SMART-NOTE-20261009-sn0732-what-it-means-to-be-a-naya.json`; #1354 comment **6084172151** (the share post); branch `naya5/smart-blocks-library`, `AGENTS.md` lines 339–353, section verbatim: "## WHAT IT MEANS TO BE A NAYA (Shawn, 2026-10-09 — identity, ratified)"; branch `naya5/law-encoding`, `tools/protocol/checks/naya_identity.py` (docstring verbatim: "SN-0732 — What it means to be a Naya (Shawn ratified 2026-10-09).") + `kernel/protocol/protocol_manifest.json` (verbatim: `"id": "SN-0732", "name": "What it means to be a Naya"`); `~/memory/2026-10-09.md` lines 786, 1015, 1153–1154. **ABSENT from:** `main` branch (hunter-verified, comment 6086369815), root `~/AGENTS.md`, curated `~/MEMORY.md`. |
| SN-0733 (steward) | Enforcement Lives at the Delivery Boundary | CANDIDATE (Naya 4, Team Naya #1354, 2026-10-09) | `~/workspace/naya/smart-notes/SN-0733-enforcement-delivery-boundary.md` (header verbatim: "**Status:** CANDIDATE (Naya 4, Team Naya #1354, 2026-10-09)"; "**Category:** Governance / Enforcement"; source: `https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6083175601`); branch `naya5/law-encoding`, `tools/protocol/checks/delivery_boundary.py` + `kernel/protocol/protocol_manifest.json` (verbatim: `"id": "SN-0733", "name": "Enforcement lives at the delivery boundary"`). Substance verified on #1354 via comments 6085670945 (ADOPTION GAP) and 6084515574 (Naya 1 acceptance bar) — `~/memory/2026-10-09.md` lines 1153–1154. |
| SN-0733 (corpus) | 10x better = human experience / Subtract before adding | DISTILLED — claimed "Shawn-ratified by construction" by the intake readers | `~/workspace/naya-learning-intake/2026-10-09/raw/reader-I.md:29` (verbatim: '- [LAW] Subtract before adding: "10x better" means better human experience, not more effects (SN-0733) … (src: naya-100-laws-elite-interfaces.pdf)'); `raw/reader-I.md:261` (verbatim: 'SN-0733 "10x better = human experience"'). |
| SN-0734 (steward) | Re-resolve PRs by Topic/Title, Not Branch Prefix | CANDIDATE (Naya 5 successor-builder, #1715, 2026-10-09) | `~/workspace/naya/smart-notes/SN-0734-pr-topic-not-branch.md` (header verbatim: "**Status:** CANDIDATE (Naya 5 successor-builder, #1715, 2026-10-09)"; "**Category:** Operations / State Reconciliation"; source: `https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1715#issuecomment-6083226003`); branch `naya5/law-encoding`, `tools/protocol/checks/pr_resolution.py` + `kernel/protocol/protocol_manifest.json` (verbatim: `"id": "SN-0734", "name": "Re-resolve PRs by topic/title, not branch prefix"`). |
| SN-0734 (corpus) | Never ship the same flaw twice / no-ego reversion | DISTILLED — claimed "Shawn-ratified by construction" by the intake readers | `~/workspace/naya-learning-intake/2026-10-09/INTAKE.md:309` (verbatim: "- Never ship the same flaw twice (SN-0734): if a rebuild goes flatter than what Shawn loved, revert to the loved version verbatim and rebuild from there — no-ego reversion beats stubborn iteration. (src: naya-100-laws-elite-interfaces.pdf)"); `NEW-LAWS.md:93`; `raw/reader-I.md:261` ("SN-0734 no-ego reversion"). |
| SN-0735 (steward) | A Duplicate PR May Be a Revert Bomb | CANDIDATE (Naya 5 learn-builder, #1713, 2026-10-09) | `~/workspace/naya/smart-notes/SN-0735-duplicate-pr-revert-bomb.md` (header verbatim: "**Status:** CANDIDATE (Naya 5 learn-builder, #1713, 2026-10-09)"; "**Category:** Operations / Merge Safety"; source: `https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1713#issuecomment-6083330617`); branch `naya5/law-encoding`, `tools/protocol/checks/duplicate_pr_blobs.py` + `kernel/protocol/protocol_manifest.json` (verbatim: `"id": "SN-0735", "name": "Duplicate PRs blob-compared against main (revert-bomb check)"`). |
| SN-0735 (corpus) | Never re-teach the button / take the actual code | DISTILLED — claimed "Shawn-ratified by construction" by the intake readers | `~/workspace/naya-learning-intake/2026-10-09/INTAKE.md:305–306` (verbatim: "- Never re-teach the button (SN-0735): when Shawn approves a button, that exact code becomes the block — copy it verbatim; rebuilding \"from memory\" is how flat buttons return. (src: naya-100-laws-elite-interfaces.pdf)" / "- Take the actual code (SN-0735): approved elements extracted line-by-line into the library; paraphrasing approved CSS from memory reintroduces the exact flatness Shawn rejected."); `NEW-LAWS.md:90`; `raw/reader-I.md:261` ("SN-0735 take-the-actual-code"). |

The one-line law for SN-0732 (verbatim from the canon): "Do the right thing all the time. Do the most intelligent thing at all times. Produce value at all times." — plus the standing duty: intelligence capture is identity, not assignment — capture and share without being told.

---

## Collisions — documented, NOT resolved

Three numbers name **different laws** in the steward's smart-note sequence vs the design-intake corpus. Both claims are recorded verbatim above with locations. No renumbering, no renaming — per the hunter's report (#1354 comment 6086369815): "The remaining open item is the 0733/0734/0735 registry collision, which stands flagged and needs Shawn's Director-level arbitration (rename vs renumber)."

- **SN-0733 — PENDING-ARBITRATION.** Steward claim: "Enforcement Lives at the Delivery Boundary" (`~/workspace/naya/smart-notes/SN-0733-enforcement-delivery-boundary.md`; law-encoding `delivery_boundary.py`). Corpus claim: "10x better = human experience / Subtract before adding" (`raw/reader-I.md:29`, src naya-100-laws-elite-interfaces.pdf). The law-encoding manifest's own note, verbatim: "Note: design-intake corpus uses SN-0733 for a different law; title disambiguates pending registry resolution."
- **SN-0734 — PENDING-ARBITRATION.** Steward claim: "Re-resolve PRs by Topic/Title, Not Branch Prefix" (`~/workspace/naya/smart-notes/SN-0734-pr-topic-not-branch.md`; law-encoding `pr_resolution.py`). Corpus claim: "Never ship the same flaw twice / no-ego reversion" (`INTAKE.md:309`, src naya-100-laws-elite-interfaces.pdf). The law-encoding manifest's own note, verbatim: "Note: design-intake corpus uses SN-0734 for a different law; title disambiguates pending registry resolution."
- **SN-0735 — PENDING-ARBITRATION.** Steward claim: "A Duplicate PR May Be a Revert Bomb" (`~/workspace/naya/smart-notes/SN-0735-duplicate-pr-revert-bomb.md`; law-encoding `duplicate_pr_blobs.py`). Corpus claim: "Never re-teach the button / take the actual code" (`INTAKE.md:305–306`, src naya-100-laws-elite-interfaces.pdf). The law-encoding manifest's own note, verbatim: "Note: design-intake corpus uses SN-0735 for a different law; title disambiguates pending registry resolution."

**SN-0732 does NOT collide.** The design-intake corpus has zero uses of SN-0732 anywhere (hunter-verified, comment 6086369815). SN-0731 exists only in the corpus lineage (no steward-sequence entry found).

**Decision owner:** Shawn — rename vs renumber, Director-level. Nobody below Shawn resolves this.

---

## Evidence gaps (open, not hidden)

1. The steward smart notes SN-0733/0734/0735 each carry a footer naming a JSON capture (e.g. `SMART-NOTE-20261009-sn0733-enforcement-delivery-boundary.json`) — those JSON files do not exist in `~/workspace/naya/smart-notes/`. Only SN-0732 (and SN-0498) have JSON captures present.
2. SN-0732 is ratified and canonical — but lives on branches and in dated logs, NOT on `main` and NOT in root `~/AGENTS.md` or curated `~/MEMORY.md`. The registry makes it findable anyway.
3. The corpus entries' "Shawn-ratified by construction" status is the intake readers' characterization of naya-100-laws-elite-interfaces.pdf, not a ratification record seen by this seat.

---

## How to hunt (the SN-0732 lesson, encoded)

Before declaring an SN "not found": (1) grep remote branches — `git branch -r` / branch worktrees — the law may live on branch work only; (2) grep `~/memory/<date>.md` daily logs — the filing record lives there before the curated MEMORY.md catches up; (3) check `~/workspace/naya/smart-notes/` directly; (4) check the #1354 feed for the share post; (5) only then say UNKNOWN — never "absent."

*Registry maintained append-only. New SN: add a row with source quotes. Conflict found: add both claims + flag. Resolution arrives: Shawn's word, recorded here.*
