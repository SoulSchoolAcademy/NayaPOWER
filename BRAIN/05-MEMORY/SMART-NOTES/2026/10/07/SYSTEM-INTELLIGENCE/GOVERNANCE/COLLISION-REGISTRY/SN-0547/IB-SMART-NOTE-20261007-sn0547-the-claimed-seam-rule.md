# The Claimed-Seam Rule — Check for an In-Flight Lane Claim Before Opening a Build

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0547-the-claimed-seam-rule
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07 ~09:15 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6041724313 ([NAYA] P0 learning activation seam — deconflicted, no duplicate build, 2026-10-07 16:01 UTC); prior lane claim #1724 comment 6041053057 ([LEARNING-ACTIVATION-SEAM]); handoff preserved on #1724 comment 6041722141.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two lanes finding the same seam and both building is a self-inflicted merge war: wasted work, duplicated branches, and eventually someone's repair lands over someone else's unpushed state. The NAYA seat found the exact [LEARNING-ACTIVATION-SEAM] already claimed by another lane on #1724 (comment 6041053057), honored the stop condition, and opened **nothing** — no competing branch, no competing PR. Instead it preserved a full cold-successor handoff (falsifiers, the minimal ACT.PLAN → optional LAW re-resolution → ACT.EXECUTE design) on the claiming lane's feed (#1724 comment 6041722141) and moved on to the next highest-value seam.

**The rule:** before you open a branch or PR for a seam, check the board and the project feeds for an in-flight lane claim on that exact seam. First claim stands. If claimed, your job is deconfliction — hand off findings, don't duplicate the build. This is SN-0508's older sibling: SN-0508 says *stand down your unpushed repair when another lane heals the seam first*; this says *never open the competing build in the first place*. Both protect the same thing: one owner per seam, zero merge wars.

## 🩷 HUMAN NOTE

Before starting any significant piece of work, the team checks who's already doing that exact thing — and if someone is, they share their findings with that person instead of building a second, competing version. No wasted effort, no collisions.

## 👶 CHILD NOTE

If your friend is already building the LEGO castle, you don't build a second castle right next to it. You give them your cool LEGO pieces and help instead.

## 👵 GRANDMA NOTE

Two cooks in the same kitchen, each making the same soup, just makes a mess — twice the work and no better soup. The wise cook checks who's already at the stove and offers her vegetables instead.

## 🧠 NAYA NOTE

This is the pre-build counterpart to the no-supersession family (SN-0236 one repair per RED class; SN-0240 never self-repair another lane's branch; SN-0508 stand down the unpushed repair). The check costs one board/feed read; the duplicate build costs hours and a merge war. Highest-value move after a stand-down is the handoff: falsifiers plus the minimal design, preserved on the claiming lane's feed, so the claiming lane gets your intelligence without a second build. For a cold successor: when you arrive at a seam, search #1354 and the project feeds for the seam's name in comments before touching git — a claim there is a stop sign, not an invitation.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0547",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY",
  "doctrine": "Before opening a branch/PR for a seam, check the board and project feeds for an in-flight lane claim on that exact seam. First claim stands: if claimed, deconflict — hand off findings to the claiming lane's feed — and open nothing. Never open a competing build.",
  "evidence": [
    "#1354 comment 6041724313 ([NAYA] P0 learning activation seam — deconflicted, no duplicate build, 2026-10-07)",
    "Prior claim: #1724 comment 6041053057 ([LEARNING-ACTIVATION-SEAM] lane claim)",
    "Handoff preserved: #1724 comment 6041722141 (falsifiers + minimal ACT.PLAN design)",
    "No production/DB/merge/ratification boundary crossed"
  ],
  "falsifiers": [
    "Opening a branch/PR for a seam already claimed on another lane's feed",
    "Treating an existing lane claim as an invitation to build a second implementation",
    "Reaching the claimed-seam discovery and building anyway 'to show the work'"
  ],
  "applies_to": "seam claims; branch/PR creation; multi-lane coordination; learning-activation work",
  "sibling": "SN-0508 (stand down unpushed repair — post-build stand-down); SN-0236 (one repair per RED class); SN-0240 (no self-repair of another lane's branch)"
}
```
