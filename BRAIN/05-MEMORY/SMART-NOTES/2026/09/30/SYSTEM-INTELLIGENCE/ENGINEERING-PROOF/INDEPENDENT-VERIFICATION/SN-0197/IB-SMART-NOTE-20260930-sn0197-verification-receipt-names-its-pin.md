# A Verification Receipt Names Its Pin

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0197-verification-receipt-names-its-pin
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5955116009 (Naya 2 relay, 2026-10-02 14:56:47Z) — PR `#1331` verified OPEN, non-draft, mergeable at head `d01ffa93`; head then moved to `f307ded2` when the oath file landed on the same branch after her check. The relay explicitly reconciled: "note the head has moved since your check: now `f307ded2`… your d01ffa93 verification was correct at the time."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A verification is a statement about an exact SHA, not about a branch. In a moving repo, a head will keep moving after any check — Naya 2 verified PR #1331 at `d01ffa93`, and one commit later the head was `f307ded2` (the oath file, additive, convergence untouched). Because her verification was recorded with its pin, the relay could say the only sentence that reconciles motion with truth: "your d01ffa93 verification was correct at the time." Without the pin, the reader faces a contradiction — "verified at d01ffa93" vs "head is f307ded2" — and must guess whether something regressed, something was missed, or the world simply moved. With the pin, the move is a delta to evaluate, not a dispute to adjudicate.

This is the constructive complement to SN-0100 (verdicts die at every new SHA). SN-0100 says a verdict does not survive a head move; this note says the receipt's job is to make that death legible: name the pin, and the successor knows exactly which slice of history was proven and which slice remains open. A verification receipt without a SHA is gossip; with a SHA it is evidence with a known boundary. The practice: every live-venue verification carries (1) the exact SHA verified, (2) what was asserted at that SHA, and (3) an explicit head-move acknowledgment when the check lands after the pin — turning "the head moved" from a credibility event into a reconciliation routine.

## 🩷 HUMAN NOTE

Shawn — on #1331 the head moved right after Naya 2 verified it (oath file added after `d01ffa93`). Because her check was pinned to its exact SHA, the relay could say plainly "your verification was correct at the time" instead of anyone wondering whether the verification was wrong. The brain lesson: always record the exact commit a verification checked, so a later head move reads as a normal delta, not a contradiction.

## 🟣 CHILD NOTE

Imagine you check that a sandwich has peanut butter at 9:00. At 9:05 someone adds jelly — and your mom asks, "did the sandwich have jelly when you checked?" If you wrote down the time, you can say "no, but it was fine at 9:00." If you didn't, it sounds like you checked wrong. Writing down the exact moment you checked keeps everyone honest about what you saw and what changed after.

## 👵 GRANDMA NOTE

When one Muse verified a design document, another file was added to it right after her check. Because she had written down exactly which version she checked, there was no confusion — everyone could see her check was right for the version she looked at, and the new file just needed its own look. The lesson: always note precisely what you checked, so later changes don't make an honest check look mistaken.

## 🤖 NAYA NOTE

Every live-venue verification receipt carries the exact SHA it verified. When the head has moved since the pin, say so explicitly: "verified at X; head is now Y; the verification was correct at its pin." A verification without a SHA is gossip; a verification with a SHA is evidence with a known boundary. Never restate an old pin as a claim about the current head; restate it as a bounded historical fact plus the delta that remains open.

## ⚙️ MACHINE NOTE

{"sn": "SN-0197", "title": "A Verification Receipt Names Its Pin", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"], "extends": ["SN-0100", "SN-0061", "SN-0175"], "evidence": {"verification": "#554 5955116009 — PR #1331 verified OPEN/non-draft/mergeable at head d01ffa93 (Naya 2)", "head_move": "head moved to f307ded2 when the oath file (HUB/ULTIMATE-DESIGN-CONTRACT-V1.md) landed after her check; relay explicitly reconciled: 'your d01ffa93 verification was correct at the time'", "content": "additive, convergence untouched — oath file added on the same branch"}, "rule": "verification receipts name their exact SHA; a later head move reconciles as a delta, never invalidates the pinned verdict; restate old pins as bounded historical facts, never as claims about the current head"}
