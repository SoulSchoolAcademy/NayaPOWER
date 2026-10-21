# The Takeover Sign-In: Name the Base, Declare the Deltas, Request the Freeze

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0204-takeover-sign-in-base-deltas-freeze
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5956182906 (Naya 1, 2026-10-02 15:59:08Z) — HUB / MAIN SHOW DIRECTOR CONVERGENCE sign-in: "PR #1328 is the single Room 01/Main Show vehicle. I am taking the exact current head `31ffa4936f3d330fdacabe521d73340cf84e8aed` as the repair base. I am not opening a competing Hub branch." Preserved list + changing list declared (two-drawer shell, runtime seams, evidence retrieval, Today work preserved; Main Show converged around the Human Director law). Coordination: "please do not push new Room 01/Main Show changes to #1328 until I post the freeze receipt, so we do not overwrite each other. I will preserve unrelated Today-room work already on the branch." Verified correct by Naya 2's relay `#554` 5956396390 (09:10 PDT): the freeze base was the exact branch tip at sign-in time; her hold request "stands on the record."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When the director hands you a moving shared branch, the sign-in is a public contract with four parts, and Naya 1's Main-Show convergence sign-in is the canonical form: (1) **name the exact base** — the full head SHA, not a branch name, not "current"; (2) **no competing branch** — state explicitly that the shared vehicle stays single, pre-empting the duplicate-lane failure SN-108 guards; (3) **declare preserved vs. changed** — list what you will not touch (two-drawer shell, runtime seams, evidence retrieval, Today work) and what you will change (Main Show converged on the director's law) — this is the scope contract that lets other lanes keep working on the preserved parts without guessing; (4) **request the freeze** — ask other lanes not to push the affected scope until you post the freeze receipt, and bound the freeze ("Room 01/Main Show changes," not everything; "I will preserve unrelated Today-room work"). The relay verified the base was exact at sign-in time — a receipt-pins-must-resolve-live instance (SN-0200) — and recorded the hold as standing, which is what makes the freeze real: a request nobody records is a wish.

Why this is brain-grade: this is the taker's complement to SN-0202's occupied-branch protocol. SN-0202 governs the latecomer (re-anchor to the live head before building); this note governs the assigned owner (how you take over without freezing the whole team). The freeze request is the genuinely new primitive: a bounded, receipt-ended hold on a shared branch, stated publicly with its scope and its end condition. Note the bounding discipline inside it — she froze Main Show pushes only, explicitly preserving unrelated Today work, and promised the receipt would end the freeze. An unbounded freeze is a veto; a bounded one is coordination. The pattern also shows the sign-in pin done right against SN-0202's failure mode: Naya 1's *first* sign-in froze at the stale pin `3d4672f5`; the takeover sign-in names the live head `31ffa493` — the four-part form only works when part (1) resolves live.

## 🩷 HUMAN NOTE

Shawn — a coordination pattern worth keeping: when Naya 1 took over the Hub convergence, her sign-in named the exact head as repair base, stated no competing branch, listed what she'd preserve vs. change, and requested a bounded freeze (no Room 01/Main Show pushes until her freeze receipt) — with unrelated Today work explicitly preserved. The brain lesson: the takeover sign-in is a four-part public contract — name the base, no second vehicle, declare the deltas, request the freeze. A freeze without a scope and an end condition is a veto; with both, it's coordination.

## 🟣 CHILD NOTE

If someone gives you a turn on the shared drawing board, you say out loud: "I'm starting from exactly this spot, I'm not starting a second drawing, here's the part I'll draw and the part I won't touch, and please don't draw over my part until I say done." Saying all four things out loud is what keeps everyone's drawing safe.

## 👵 GRANDMA NOTE

When one seat was asked to take over the shared work branch, she announced it properly: exactly which version she was starting from, that she wouldn't open a competing copy, what she would keep as-is and what she would change, and asked everyone else to hold their changes to that area until she posted her done-note — while explicitly leaving unrelated work untouched. The lesson: a takeover announced in four parts keeps a shared workspace from colliding; a freeze needs a boundary and an ending, or it's just a block.

## 🤖 NAYA NOTE

Takeover-sign-in protocol (complement to SN-0202's occupied-branch rule): (1) name the exact base head (full SHA, resolves live); (2) declare no competing branch — the shared vehicle stays single; (3) declare preserved vs. changed scope — the lanes keep working on preserved parts without guessing; (4) request a bounded freeze — affected scope only, unrelated work explicitly preserved, ending on your freeze receipt. The relay records the hold so the freeze is real, not a wish. Unbounded freeze = veto; bounded freeze with scope and end condition = coordination. The four-part form only holds when part (1) resolves live at sign-in time.

## ⚙️ MACHINE NOTE

{"sn": "SN-0204", "title": "The Takeover Sign-In: Name the Base, Declare the Deltas, Request the Freeze", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "SHARED-BRANCH-DISCIPLINE"], "extends": ["SN-0202", "SN-0200", "SN-0108"], "evidence": {"sign_in": "#554 5956182906: Naya 1 director-convergence sign-in — exact head 31ffa4936f3d330fdacabe521d73340cf84e8aed as repair base; no competing branch; preserved list (two-drawer shell, runtime seams, semantic color, evidence, Today work) + changing list (Main Show convergence per director law); freeze request bounded to Room 01/Main Show pushes until freeze receipt; unrelated Today work preserved", "receipt": "#554 5956396390: base verified exact at sign-in time; hold stands on record"}, "rule": "takeover sign-in = exact base + no second vehicle + preserved/changed declaration + bounded freeze with receipt end; freeze without scope and end condition is a veto"}