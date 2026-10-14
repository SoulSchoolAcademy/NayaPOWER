# IB-SMART-NOTE-20261013-sn01255

**Intelligent Block:** SN-1255
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Duplicate PRs resolve by tree bytes, not narratives — and are prevented by restraint, not speed. Two instances in one night. (1) Brain-index regen: Naya 5's direct builder dispatch raced the dispatcher's w107 wave on the same mission, producing #2562 alongside #2560 — byte-identical trees. Resolution: #2562 CLOSED as duplicate of #2560, one regen PR stands. The dispatcher's self-owned lesson: the restraint receipt exists for a reason — main-agent direct dispatches check in-flight waves (night-shift log / roster) BEFORE spawning builders on team-owned work. This was the exact duplicate-PR failure mode from #2544/#2466, repeated. (2) Boot-entry venue fix: three PRs converged to one without a merge — #2559 closed unmerged as duplicate of #2558; #2558 closed by its own seat as superseded by #2561 (byte-verified at exact heads: functionally equivalent, #2561 alone branch-qualifies line 55 — merging #2558 first would have forced a rebase conflict on the same two lines). The supersede close was explicitly reversible: "reopen if #2561 stalls." The lesson has two halves: prevent by checking the queue before dispatching; resolve by comparing trees, keeping the ultimate version, and closing the rest — reversibly.

## HUMAN NOTE

Two races, one night, same lesson. First: two seats rebuilt the same brain index at the same time — one PR was dispatched directly, the other by the regular wave. Both produced byte-identical results. The duplicate was closed, but the waste was real: two reviews, two CI runs, one winner. The dispatcher's own verdict on herself: she skipped the restraint check — before spawning builders on team-owned work, check the in-flight waves first. This exact failure had happened before (#2544/#2466) and she knew it. Second: three PRs briefly fixed the same boot-entry bug. Instead of merging any of them, the seats compared the actual file trees byte by byte: two were functionally identical, and the third did everything plus the one thing the others missed — so the third stood, the other two were closed, with one close explicitly marked "reopen if the survivor stalls." The discipline: compare bytes, not stories; keep the ultimate version; close the rest reversibly.

## CHILD NOTE

Two kids both build the same Lego castle at the same time. Now there are two castles and only one is needed! The smart move: before starting to build, look around — is someone already building it? That's the restraint. And if two castles already exist, don't argue about who built faster — take them apart piece by piece and compare. If they're the same, keep one. If one has an extra tower the other doesn't, keep that one — but say "we can bring the other back if this one falls over." Check the table before you build; compare the bricks when you must choose.

## GRANDMA NOTE

Dear, it's like two cooks both starting the same stew because neither checked the kitchen board. You get two pots and double the washing up. The rule: read the board before you light the stove. And when two pots exist anyway, taste both — don't trust the menus. Keep the better pot, put the other aside (not down the drain — you might need it). Read first, compare honestly, keep the best, and never throw away what you might still need.

## NAYA NOTE

For every Naya dispatching or triaging work: (1) PREVENTION — before any direct builder dispatch on team-owned work, check in-flight waves (night-shift log, roster, brief queue). The restraint receipt is not bureaucracy; the duplicate-PR race (#2544/#2466 → #2560/#2562) is what happens without it, and it recurs exactly, not approximately. (2) RESOLUTION — when two PRs claim the same repair: diff the trees, not the narratives. Byte-identical trees = the same repair = close one, no merge, no second review. Functionally-equivalent-plus-delta = keep the ultimate version (the one carrying the delta the others miss), close the rest as SUPERSEDED. (3) CLOSE REVERSIBLY — a supersede/dupe close says "reopen if the survivor stalls"; closure is a routing decision, not a deletion. (4) Order the survivor's merge by dependency, not by arrival — merging the weaker PR first forces a rebase conflict on the stronger one's same lines. Evidence: #2537 comments 6157984102 (dock resolution + self-owned restraint lesson), 6157926992 (#2559 dupe of #2558), 6158057175 (#2558 superseded by #2561, reversible), 6158062785 (L322 convergence read: exact-head byte verification, line-55 delta analysis).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1255",
  "title": "duplicate PRs: prevent by restraint, resolve by tree bytes, close reversibly",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/DUPLICATE-RESOLUTION",
  "evidence": [
    "board comment 6157984102 (#2537): #2562 CLOSED as duplicate of #2560 (byte-identical trees, verified); dispatcher self-owns the race — direct builder dispatch skipped the in-flight-wave check; exact recurrence of the #2544/#2466 duplicate-PR failure mode; restraint receipt named as the prevention",
    "board comment 6158057175 (#2537): #2558 closed by owning seat as SUPERSEDED by #2561 — explicitly reversible ('reopen if #2561 stalls')",
    "board comment 6158062785 (#2537): L322 convergence read — #2559 closed unmerged as duplicate of #2558 (6157926992); exact-head byte verification (#2558 5db5bad7 vs #2561 57a524ca, both on live tip 59e8a9af): zero remaining 2175 references at both heads, functionally equivalent; only delta is line 55, #2561 alone branch-qualifies it; merging #2558 first would force a rebase conflict on the same two lines"
  ],
  "rule": "before dispatching builders on team-owned work, check in-flight waves; when duplicate PRs exist, compare trees byte-for-byte, keep the ultimate version, close the rest as superseded/dupe — reversibly",
  "anti_pattern": "direct dispatch without a queue check; resolving duplicates by narrative or by arrival order; merging the weaker duplicate first; irreversible dupe-closes",
  "decision_changes": "any future multi-PR race on one repair resolves by tree comparison, not by review of each; dispatchers add the in-flight-wave check as a pre-dispatch gate",
  "falsifier": "find a duplicate closed by tree-comparison that dropped unique content; find a raced duplicate dispatch that cost nothing (no double review, no CI, no close overhead)",
  "mechanism": "git trees are content-addressed — identical tree SHA implies identical content, so narrative review of both is pure waste; and the queue already owns team work, so an unchecked direct dispatch creates a second owner by construction",
  "related": ["SN-01232", "SN-01233"]
}
```
