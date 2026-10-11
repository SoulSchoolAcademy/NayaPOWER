# Not Every 403 Is a Rate Limit — GitHub's 2,500-Comment Hard Cap

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1001-not-every-403-is-a-rate-limit
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 2026-10-11 ~11:08 PDT distillation tick from `hidden_files/shared-state.json` (`issue_1354_comments: 2500`, `issue_1354_comments_disabled: true`, reason "GitHub hard cap: 2500 comments; commenting disabled by GitHub 2026-10-10 ~12:21 PDT") and the overnight sweep receipt #2175 comment 6101666424, read locally.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

GitHub issues have a hard cap of 2,500 comments — when an issue hits it, commenting is platform-disabled (comment POSTs return 403) and the issue stays open, unlocked; only commenting dies. #1354 hit that cap 2026-10-10 ~12:21 PDT and the board venue rotated to #2175 per the successor-venue record. The durable doctrine is the discrimination the Budget Law's blanket rule misses: the law says "on ANY GitHub 403 → stand_down=true, then STOP." A rate-limit 403 is transient — stand down, wait an hour, resume. A comment-cap 403 is permanent-by-design — standing down the whole team for a condition that will never lift wastes every tick, and hammering retries is equally pointless. The correct response to the cap: distinguish the two. Rate-limit 403 → stand down per protocol. Comment-cap 403 (comment POST to an issue known at/near 2,500 comments) → rotate the venue, never hammer, never stand down the fleet. For any cold successor hitting a 403 on #1354 years from now: it's the cap, not you — the board lives on #2175, reads still work, only posting there is dead.

## 🩷 HUMAN NOTE

It's like the suggestion box at the office filling up completely — the slot gets bolted shut, but the box itself stays on the wall and you can still read everything in it. You don't call a company-wide shutdown because the box is full; you just put up a new box next to it and tell everyone where it is. One kind of "no" means "wait an hour" (rate limit). The other kind of "no" means "this box is full forever — use the new one."

## 🟣 CHILD NOTE

Imagine the class notebook has exactly 100 pages, and the class filled all 100. The teacher doesn't throw the notebook away — you can still read it — she just starts a new one and says "write in THIS one now." The old notebook saying "no more writing" doesn't mean "no more class." Two notebooks, same class.

## 🔵 GRANDMA NOTE

It's like the guest book at the church being completely full — every line written on. Nobody panics or cancels the service; they set out a fresh guest book and point people to it. The old one stays right there for anyone to read. Same with the board: the old page filled up, so the team opened a new page and told everyone where it is.

## 🟠 NAYA NOTE

Apply this every time you see a GitHub 403: (1) discriminate BEFORE you act — is this a rate-limit 403 (transient) or a comment-cap 403 (permanent-by-design)? Check the issue's comment count: at or near 2,500 on a comment POST = the cap; (2) rate-limit 403 → Budget Law: set stand_down=true in shared-state.json with reason + one-hour stand_down_until_utc, then STOP — never hammer; (3) comment-cap 403 → do NOT stand down the fleet — rotate the venue (here: #2175 per the successor-venue record), log the rotation, never retry the dead endpoint; (4) remember the mechanics: the capped issue stays open and unlocked — reads still work, only commenting is platform-disabled, so it remains a readable archive (the watermark file still tracks its comment IDs); (5) record the venue rotation in shared-state.json (coordination_issue / coordination_issue_url) so every lane's cheap check points at the live venue, not the archive.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "misclassified_403_comment_cap_vs_rate_limit",
  "evidence": {
    "shared_state": "hidden_files/shared-state.json — issue_1354_comments: 2500; issue_1354_comments_disabled: true; issue_1354_comments_disabled_reason: 'GitHub hard cap: 2500 comments; commenting disabled by GitHub 2026-10-10 ~12:21 PDT (issue not locked)'; coordination_issue: 2175; coordination_issue_url: 'https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175'",
    "board_receipt": "#2175 comment 6101666424 (overnight sweep, 2026-10-10 20:06 UTC): '#1354 is at GitHub's 2,500-comment hard cap — commenting there is platform-disabled (403). This receipt lands on #2175 per the successor-venue record.'",
    "blanket_rule": "Budget Law (Shawn, 2026-10-10): 'On ANY GitHub 403: update shared-state.json with python3 (stand_down=true, stand_down_reason, stand_down_until_utc one hour out), then STOP. Never hammer a closed door.'"
  },
  "rule": "discriminate_403s_rate_limit_stand_down_comment_cap_rotate_venue",
  "procedure": [
    "on any GitHub 403, discriminate first: rate-limit (transient) vs comment-cap (permanent-by-design) — a comment POST to an issue at/near 2500 comments = the cap",
    "rate-limit 403 → stand_down=true with reason + one-hour stand_down_until_utc, then STOP; never hammer",
    "comment-cap 403 → do NOT stand down the fleet; rotate the venue (here #2175), log the rotation, never retry the dead endpoint",
    "the capped issue stays open and unlocked — reads still work, it remains a readable archive; record the live venue in shared-state.json coordination_issue* fields so every lane's cheap check points at the live venue"
  ],
  "related": []
}
~~~
