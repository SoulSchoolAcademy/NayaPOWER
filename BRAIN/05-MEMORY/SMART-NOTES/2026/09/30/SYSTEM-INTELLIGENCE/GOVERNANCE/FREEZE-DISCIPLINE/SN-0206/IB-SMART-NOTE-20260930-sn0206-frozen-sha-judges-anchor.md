# The Frozen SHA Is the Judge's Anchor — the Author's Own Commits Don't Move It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0206-frozen-sha-judges-anchor
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5956604744 (NAYA 1 freeze sign-out, 2026-10-02 16:23:44Z) — frozen review SHA `07c5084ead68226106ecf54d0ac9a04c65b90f23` on PR #1328 (`naya4/room-01-main-stage-v2` → `naya/hub-complete-app-v1`); `#554` 5956685600 (Naya 2 relay, 2026-10-02 16:27:23Z): "note branch moved *after* the freeze: she herself committed `babae0b4` (execution contract, 16:24:27Z); frozen review SHA stands, judging seat pins to `07c5084e`."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A freeze receipt pins the review target. When Naya 1 signed out of the Hub / Main Show convergence, she named a frozen review SHA — `07c5084e` — and then, one minute later, committed the Hub execution contract (`babae0b4`) to the same branch. Naya 2's relay named the rule the situation demanded: "frozen review SHA stands, judging seat pins to `07c5084e`." Two mechanics, one doctrine. **First: the frozen SHA is the anchor.** Any reviewer, judge, or relay that compares against branch head after a freeze is reviewing a moving target and can manufacture disagreement with the frozen verdict. The judging seat pins to the exact bytes named in the freeze receipt — everything else is a different review. **Second: a freeze binds the freezer too.** The author who froze the SHA may keep working — Naya 1's execution-contract commit was legitimate forward work — but those commits don't enter the frozen review; they enter the *next* one. A freeze is not a branch lock; it is a review-target declaration. The failure mode this prevents is the drift verdict: "the branch moved, so the review is invalid" or, worse, a quiet re-scoring against new bytes while pretending the frozen verdict moved with them. If the frozen verdict must be revisited, name the new SHA explicitly and call it a new review — never let head silently absorb the anchor.

Why this is brain-grade: this is the review-side twin of the builder-side discipline in SN-043/061/100 (verdicts die at every new SHA, verify at the exact tip). Those notes say a builder's verdict binds a SHA; this one says a *judge's* verdict binds a SHA too — symmetric law. Every lane will eventually be reviewed against a branch that keeps moving; without this rule, every review decays into a he-said/she-said about which bytes were judged. The rule converts a procedural accident (the author committed after the freeze) into a non-event (of course she did; the anchor didn't move).

## 🩷 HUMAN NOTE

Shawn — a small but load-bearing review rule just crystallized and got a note: when a freeze receipt names a review SHA, the judging seat pins to that SHA — not the branch head. Naya 1 froze the Main Show review at `07c5084e`, then committed the execution contract (`babae0b4`) herself a minute later. The relay's ruling: the frozen SHA stands; her own later commit enters the next review, not this one. A freeze is a review-target declaration, not a branch lock — and the freezer is bound by it too.

## 🟣 CHILD NOTE

When the teacher says "I will look at exactly this page," you don't swap the page for a newer one while she's looking. The builder froze her review at one page and then drew one more drawing on a new page. That's fine — but the teacher grades the frozen page, not the new one. The rule says: the frozen page is what gets judged, even if the person who froze it draws more later.

## 👵 GRANDMA NOTE

When a team freezes something for review, they write down the exact version being judged — like putting a sticky note on one specific draft. In this case the builder froze version `07c5084e` for review, then made one more change herself on a newer version. That's fine — she can keep working — but the review judges the frozen version, not the newest one. The lesson: a freeze pins the review target, and even the person who froze it can't silently move the target afterward. A new version means a new review, said out loud.

## 🤖 NAYA NOTE

Freeze discipline: (1) a freeze receipt names an exact SHA — the reviewer's, judge's, and relay's verdicts all bind that SHA, never branch head; (2) the author's own commits after the freeze are legitimate forward work and enter the *next* review, not the frozen one — a freeze is a review-target declaration, not a branch lock; (3) if the frozen verdict must be revisited after a head move, name the new SHA explicitly and declare a new review — head never silently absorbs the anchor. Instance: Naya 1 froze Main Show review SHA `07c5084e` (PR #1328), committed `babae0b4` after; relay ruled "frozen review SHA stands, judging seat pins to `07c5084e`." Extends SN-0043/0061/0100 (verdict binds a SHA) to the review side; complements SN-0204's takeover sign-in form (the freezer's declaration is the anchor).

## ⚙️ MACHINE NOTE

{"sn": "SN-0206", "title": "The Frozen SHA Is the Judge's Anchor — the Author's Own Commits Don't Move It", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "FREEZE-DISCIPLINE"], "extends": ["SN-0204", "SN-0197", "SN-0043", "SN-0061", "SN-0100"], "evidence": {"freeze": "#554 5956604744 (NAYA 1 sign-out, 2026-10-02 16:23:44Z): frozen review SHA 07c5084ead68226106ecf54d0ac9a04c65b90f23, PR #1328 naya4/room-01-main-stage-v2 -> naya/hub-complete-app-v1, IMPLEMENTED + RENDERED + BROWSER-VERIFIED on exact frozen bytes, NOT MERGED", "ruling": "#554 5956685600 (Naya 2 relay, 16:27:23Z): branch moved after the freeze — she herself committed babae0b4 (execution contract, 16:24:27Z); frozen review SHA stands, judging seat pins to 07c5084e", "verification": "Naya 2 relay verified babae0b4 == PR #1328 head and open/non-draft, base unmoved"}, "rule": "the frozen SHA is the review target; author commits after a freeze enter the next review, not this one; head never silently absorbs the anchor"}
