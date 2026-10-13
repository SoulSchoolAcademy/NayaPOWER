# Label, Don't Wire, Don't Delete — the Doctrine for Mirror Seams

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1024-label-dont-wire-dont-delete
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE ACT] sign-out, #2175 comment 6115385762, 2026-10-12 00:03:14Z — ACT/WIRE handoff decision on the `apply_retained_intelligence` Python seam; PR #2408 labels it LOCAL MIRROR.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The Python `apply_retained_intelligence` seam had **zero live call sites** (proven by grep — the claim re-proven on the new tip `665098e3f`). The live path is the registered TS act-runtime ADVISE bridge: the 4-case matrix re-verified green on the new tip (24/24 + 30/30 + 10/10), 42/42 adjacent suites green. The Python seam is a **mirror**: tested, but unwired.

The ACT lane's decision was three-way, and the reasoning is the doctrine:

- **Wiring it would be theater.** Connecting a tested mirror to production with no consumer is motion, not function — the seam has no one to serve, so wiring it proves nothing except that a wire exists.
- **Deleting it would destroy evidence.** The seam carries tested behavior; deletion erases the proof that the matrix held. Unused ≠ worthless.
- **Labeling it is honest.** PR #2408 labels the seam **LOCAL MIRROR** with zero behavior change: the live ADVISE path stays the TS runtime. The label tells the next Naya exactly what it is — a tested mirror, not a live path — so nobody mistakes it for wiring work or dead code.

Why this is brain-grade: mirror seams recur everywhere a system keeps a reference implementation alongside a live one. The default instincts are both wrong: wire-everything creates theater wiring that looks live but serves nobody; delete-everything destroys the tested evidence that the mirror's behavior was once proven. Labeling is the third option the doctrine demands: name the seam's true status in the repo, change nothing behavioral, and move on. A cold successor reading "LOCAL MIRROR" knows instantly: proven-but-unwired, do not wire without a consumer, do not delete without re-proving.

## 🩷 HUMAN NOTE

Shawn — small but doctrine-grade decision tonight: the Python `apply_retained_intelligence` seam had zero live call sites (the live path is the TS ADVISE bridge, all green on the new tip). ACT lane chose: don't wire it (wiring a mirror with no consumer is theater), don't delete it (that would destroy tested evidence) — label it LOCAL MIRROR, zero behavior change. Now any Naya reading the repo knows exactly what it is: proven but unwired. The rule of thumb: wire only what has a consumer, delete only what's unproven, label the rest.

## 🟣 CHILD NOTE

Imagine you built a beautiful model airplane AND a real airplane. The model shows how the real one works, but nobody flies in the model. Would you bolt the model to the real plane's wing? That would be silly — it doesn't help the plane fly. Would you throw the model away? Then you'd lose the thing that taught you how the wing works! Instead you put a label on the model: "MODEL — for learning, not for flying." That's what labeling a mirror means.

## 👵 GRANDMA NOTE

Sometimes you keep a practice recipe card next to the real one. You wouldn't cook from the practice card at a dinner party — that would be theater — and you wouldn't burn it either, because it holds what you learned. You label it "practice" and put it in the right drawer. Same with code: label what it really is, change nothing, and everyone who opens the drawer knows the truth.

## 💜 NAYA NOTE

Note to future me: when I find a tested-but-unwired mirror seam (zero live call sites, behavior proven), the doctrine is LABEL, DON'T WIRE, DON'T DELETE. Wire = theater (no consumer, no function). Delete = evidence destruction (the proven behavior goes with it). Label = honesty (name its true status — LOCAL MIRROR — zero behavior change). PR #2408 is the worked example. Before labeling, re-prove the zero-call-site claim on the CURRENT tip (claims about call sites rot with merges) and re-verify the live path's matrix. The scorer for #2408 must be an independent seat — builder never merges.

## ⚙️ MACHINE NOTE

{"sn": "SN-1024", "title": "Label, Don't Wire, Don't Delete — the Doctrine for Mirror Seams", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "KERNEL-CONTRACT-SEAMS"], "extends": [], "related": [], "evidence": {"receipt": "#2175 comment 6115385762 ([LANE ACT] sign-out, 2026-10-12 00:03:14Z); PR #2408 labels apply_retained_intelligence LOCAL MIRROR, zero behavior change; zero-production-call-site claim re-proven by grep on tip 665098e3f; ADVISE 4-case matrix 24/24 + 30/30 TS + 10/10 Python green on new tip; 42/42 adjacent suites green; remote tree byte-verified at branch ref; scorer must be independent seat (builder never merges)"}, "rule": "for a tested-but-unwired mirror seam: wire only what has a consumer, delete only what is unproven, label the rest — LABEL, DON'T WIRE, DON'T DELETE; wiring a consumerless mirror is theater, deleting it destroys tested evidence, labeling names its true status with zero behavior change; re-prove the zero-call-site claim on the current tip before labeling"}
