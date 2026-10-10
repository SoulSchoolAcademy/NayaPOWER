# Quoted SHAs Expire in Minutes Under Concurrent Push — the Board-as-Cache Staleness Rule

**Intelligent Block:** IB-SMART-NOTE-20261001-sn058-stale-sha-board-cache
**Smart Note:** SN-058
**Truth state:** CANDIDATE
**Scope:** PRIVATE canonical runtime object; this file is a PUBLIC DERIVED VIEW authorized by the human director.
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

During the 24-hour non-stop push, PR #1243 moved four commits in 41 minutes (`e48731ce` → `ec412d61` → `bd4cffa6` → `2a7851a8`), and three seats quoted three different heads within 11 minutes — including one seat about to re-freeze on a SHA that no longer sits on the branch. Treat every SHA quoted on the coordination board as a cache entry, not a pin: re-verify the branch head live at consumption, and writers verify their quoted SHA still resolves to the intended ref at publication. The relay carries this re-verification as its lane so builders don't have to watch.

## HUMAN NOTE

Think of the board like a whiteboard in a hallway during a sprint. Someone writes "the build is at ec41" at 9:15, someone else writes "the build is at bd4c" at 9:17, and by 9:26 the build is at 2a78. Every line on the board was true when written — and nearly every line was stale within minutes. If you freeze your work on the line instead of the live branch, you freeze onto a ghost: `ec412d61` still exists as a commit object but has zero branch membership. You would integrate against an orphan and never know, because the commit hash is real — it just isn't *the branch* anymore.

The rule that prevents this:

1. **Consumers re-verify at consumption.** Before you freeze on a quoted SHA — for an integration, a qualification, a review — re-fetch the branch head live (`GET /repos/.../pulls/<n>` → `head.sha`, or `git/refs/heads/<branch>`). Never trust a board-quoted SHA, even one posted minutes ago.
2. **Writers verify at publication.** Before you quote a SHA in a board comment, confirm it is the current head of the ref you mean (not your local checkout, not an earlier push). The relay independently verified `ec412d61` exists as an object *and* is absent from the branch's commit list — a writer-side check takes seconds.
3. **Dangling SHAs get flagged, not silently dropped.** A quoted SHA that exists as an object but sits on no branch is the sharpest failure mode: it looks valid (every git command resolves it) while pointing at superseded work. The relay flags these explicitly.

## CHILD NOTE

When everyone is building fast, the note someone left about "which version we're on" goes old in minutes. So before you build on a version number someone wrote down, check the live board yourself. And when YOU write down a version number, make sure it's the newest one first.

## GRANDMA NOTE

When the family group chat moves fast — "dinner's at 6!" then "actually 6:30!" then "actually 7!" — you don't leave the house on the first message. You check the newest one. Same with build versions: the newest message wins, and the relay keeps an eye on the chat for you.

## NAYA NOTE

This is the operational twin of SN-057's consumer re-freeze, aimed at *board-quoted* SHAs rather than tool SHAs. Naya 1's control-tower rule ("if a head moves, the qualification tied to the old head becomes historical") applies to board comments with the same force — during the 24-hour push, "the old head" can mean "eleven minutes ago." When you are the relay: announce head movements you observe live, flag dangling SHAs by name, never let a seat freeze onto a ghost. When you are a builder: expect the relay to correct your quoted SHA — that is the lane working, not criticism.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "raw_source_separate_from_distillation": true,
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "knowledge_creates_authority": false,
  "protocol": "board_sha_staleness_rule",
  "moves": [
    "consumer re-fetches branch head live immediately before freezing",
    "writer verifies quoted SHA == current ref head before publishing",
    "relay flags quoted SHAs with object-exists-but-no-branch-membership as dangling"
  ],
  "dangling_sha_check": "GET /commits/<sha> exists AND <sha> absent from PR commit list => dangling",
  "applies_to": ["board_quoted_shas", "cross_seat_freeze_decisions", "relay_announcements"],
  "during": "high_velocity_push_periods"
}
~~~

## 🟢 LEARNING LESSON

A real commit hash that sits on no branch is more dangerous than a wrong hash: the wrong hash fails loudly, the dangling one resolves everywhere and points at dead work. Under concurrent push, "the SHA someone wrote down" is a claim about the past; only a live ref read is a claim about now.

## 🟡 WHAT IT MEANS

Naya 1's freeze discipline ("any qualification tied to a previous SHA becomes historical") was written for daily-scale movement. The 2026-10-01 morning showed minute-scale movement: #1243's head moved four times in 41 minutes, the three quoting comments were all correct at write time, and one of them (`ec412d61`) became dangling within six minutes of being quoted. The discipline scales down unchanged — the only difference is the relay must run the re-verification check every run, not once a day. It also refines SN-057: dual-SHA delivery is only trustworthy if the "live head" half is re-verified at consumption.

## ⚪ WHAT'S IN IT FOR YOU

No integrations against ghost commits, no qualifications invalidated by invisible drift, and the board stays trustworthy during the fastest hours of the push because one lane is paid to keep checking.

## 🟨 HOW TO APPLY / HOW TO USE

- Before freezing on any board-quoted SHA: `GET /repos/SoulSchoolAcademy/NayaPOWER/pulls/<n>` and compare `head.sha` with the quoted value. If they differ, freeze on the live head and note the staleness.
- Before quoting a SHA in a board post: confirm your SHA == the live ref head (unless you explicitly mean a historical SHA, in which case label it "historical").
- Relay per-run checklist addition: for every branch the relay tracks (#1224, #1216, #1243), diff the live head against the watermark; for any quoted-but-unmatched SHA seen in board comments, run the dangling check (object exists? on the branch?) and flag it by name.
- Deconfliction (applied this run): last-second re-fetch caught two newer comments (Naya 4's receipt 5935744966, main seat's v3 post 5935793156); the relay trimmed its draft to avoid duplicating the v3 announcement and posted only the dangling-SHA correction the other posts didn't carry. Stand down on races, post only what's uncovered.

## 🔗 HOW IT CONNECTS

- **SUPPORTS** → NayaPOWER North Star: evidence-backed verification instead of activity theater
- **REQUIRES** → Team Naya Issue #554 durable coordination and handoff
- **USES** → live PR-head reads, commit-object existence probes, SN-057's consumer re-freeze
- **GOVERNS** → SHA quoting and freeze decisions during high-velocity push periods
- **ENABLES** → trustworthy board state when branches move in minutes
- **EXTENDS** → SN-017 (seat coordination), SN-057 (handoff protocol), SN-022/SN-026 (collision registry + pagination)

## 🧭 KEY DECISIONS / PRINCIPLES

- A board-quoted SHA is a cache entry, not a pin. TTL is effectively "until the next push" — assume minutes during a push window.
- Dangling SHA (object exists, no branch membership) is the sharpest failure mode: it resolves everywhere and means nothing.
- The writer checks at publication; the consumer checks at consumption; the relay checks every run. Redundancy here is cheap, ghosts are expensive.
- Stand down on same-topic races; post only what is uncovered. (Demonstrated: relay reply 5935801542.)
- The relay announces state and flags drift; it never performs the owning lane's verification and never merges.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event_id": "9c3e1a7f-4b2d-4e8f-b1c9-7d5e2a8f3c4d",
  "intelligent_block_id": "IB-SMART-NOTE-20261001-sn058-stale-sha-board-cache",
  "lineage_id": "d2a7b4c1-8e3f-4a5d-9c6e-1f2a8b3d4e5f",
  "relationship_id": "e8f1c2a9-5b6d-4c7e-8f2a-3b5c7d9e1f2a",
  "runtime_index_id": "f5a4d8c2-9e1b-4f8d-a2c7-6b9e4f1a3d8c",
  "receipt_id": "a7b9e1d4-2c5f-4a8d-9e3f-8d1b5f6c4a9e2",
  "independent_verification": false,
  "truth_state": "CANDIDATE"
}
~~~

**Receipts (all live-verified 2026-10-01 ~09:25–09:27 PDT):**
- PR #1243 (`naya2/persistence-integration-package`) commit list (live): `b7a6822df2` → `e48731ce` (15:45:10Z) → `bd4cffa6` (16:15:27Z) → `2a7851a8c6` (16:26:24Z) — four heads in 41 minutes.
- `ec412d61a62c27a8975cb25c62822555cbd7a85c`: `GET /commits/ec412d61` returns the commit object (CI-fix message, parent `e48731ce`) — object exists; `grep` over the PR's full commit list returns 0 matches — not on the branch. Dangling, verified.
- Three seats, three quoted heads within 11 minutes: brain-drive comment 5935554685 (16:15:54Z) quoted `ec412d61` (already superseded); Naya 4 sign-in 5935557373 (16:16:03Z) quoted `ec412d61` as live head (six minutes after `bd4cffa6` became the branch); Naya 1 control-tower update 5935588786 (16:17:53Z) quoted `bd4cffa6` (superseded at 16:26:24Z).
- Naya 4's receipt 5935744966 (16:26:24Z) stated "re-froze on #1243 `ec412d61` ... Resolved" — at the exact minute v3 (`2a7851a8`) landed; she was about to freeze onto a dangling SHA.
- Relay reply 5935801542 (09:27 PDT) posted after last-second deconfliction re-fetch: acknowledged her receipts, flagged `ec412d61` as dangling by name, verified #1216 torch head `43d5d6e4aa62` == published torch head, torch comment 5935651716 found on #1216, `test` + `chain-readiness-gate` SUCCESS on that head, #1224 `a71fbfe1` unchanged.
- SN numbering: max SN-NNN on main = 16; open-PR claims enumerated (up to SN-057 via PR #1245); #554 comments scanned for claims ≥ SN-058 (none found). SN-058 free; claimed on the board via comment 5935801542 edit.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This note records one incident (2026-10-01 morning, PR #1243) and one demonstrated correction. It is CANDIDATE until the rule is adopted across lanes or demonstrably prevents a second failure. The `ec412d61` object-exists finding is verified live; the inference "superseded push" (rather than deliberate orphan) comes from the branch's commit sequence, not from a push log — the practical effect (no branch membership) is identical either way. It does not grant authority for production changes, merges, or anything outside reversible cross-seat coordination.

## ➜ NEXT ACTION / SUCCESS CONDITION

Adopt the relay per-run checklist addition on the next relay run; if a seat is caught quoting a stale head again, the relay flags it before anyone freezes. Promote toward ACCEPTED when two lanes have demonstrably re-verified at consumption instead of trusting a board quote.
