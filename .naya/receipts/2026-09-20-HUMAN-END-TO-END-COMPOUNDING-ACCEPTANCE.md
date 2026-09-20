# 🔱 NayaNET Human End-to-End Compounding Acceptance — 2026-09-20

## Status

**VERIFIED — single live human/browser transaction closed through human capture → canonical persistence → Smart Feed → reload → Dream → learning evidence → learning apply → cold decision → changed successor behavior → fresh-browser cold retrieval.**

Execution surface: canonical Assistant Cloudflare Hub `sparkling-shape-7ae5`

Acceptance run: local Playwright runtime execution on 2026-09-20T19:03:53Z–19:04:08Z

Source commit tested: `5e4a02eb3b8e59df03a23dab2bd962692ed042ca`

## Exact lineage

- Human Smart Note canonical event ID: `b1d49191-d179-4047-8658-950f84986a68`
- Human capture transaction ID: `a8baf895-882f-40f4-9c61-8b3e927607a3`
- Cognition event ID: `0ef6183b-8547-45e4-9d39-32692ee2f2b3`
- Intelligence Index row: `2797083e-c29a-40ad-a758-7eda9f6d3ab4`
- Smart Note source row: `518b302a-8204-498c-bac9-7abe23bd56ef`
- Dream replay ID: `698c34d8-22b4-4a4b-a0c3-4d0b5084595c`
- Learning evidence ID: `c6a221ff-6eb2-4dcc-95f5-649da7b615c3`
- Learner state version: `1`
- Successor verification evidence ID: `935d04c9-5bd2-4c3d-a6da-13a60e4c48e5`

## Acceptance checks

| Boundary | Result |
|---|---|
| Name-first identity | PASS |
| Canonical React Hub | PASS |
| Runtime authentication | PASS |
| Human Smart Note capture control | PASS |
| Canonical receiver result | PASS |
| Exact canonical event identity | PASS |
| Cognition persistence | PASS |
| Intelligence Index persistence | PASS |
| Smart Note private-by-default state | PASS |
| Exact Smart Feed event render | PASS |
| Feed reload preserves exact event | PASS |
| Dream replay | PASS |
| Learning evidence bound to human event | PASS |
| Learning Apply | PASS |
| Baseline successor decision before learning | NOT INFLUENCED |
| Cold decision after learning | USE_VERIFIED_LEARNING_CONTEXT |
| Exact learning evidence retrieved | PASS |
| Exact Dream replay retrieved | PASS |
| Authority changed | FALSE |
| Successor behavior changed | PASS |
| Successor verification evidence | PASS |
| Fresh browser context cold retrieval | PASS |

## Compounding proof

The same target was evaluated before and after learning:

- Baseline: `influenced = false`
- After Dream + Apply: `decision = USE_VERIFIED_LEARNING_CONTEXT`
- Exact evidence reused: `c6a221ff-6eb2-4dcc-95f5-649da7b615c3`
- Exact replay reused: `698c34d8-22b4-4a4b-a0c3-4d0b5084595c`
- Successor behavior: `successor_behavior_changed = true`
- Authority: unchanged
- Fresh browser context independently retrieved the same learned evidence and decision.

## Real divergences encountered and repaired

1. Harness attempted to access browser `window` from the Node/Playwright environment after reload. Repaired by using a Playwright JSHandle for the in-page Supabase client.
2. Cognition query used nonexistent `owner_id`; runtime schema uses `user_id`. Repaired to the canonical column.
3. Successor test used a new target with no learner-state context. Repaired by defining the successor comparison against the same target: baseline before learning → learned successor after Apply.
4. Fresh-browser check initially created a new identity instead of preserving the authenticated human session. Repaired by creating a genuinely fresh browser context from the existing authenticated storage state.
5. Fresh-browser decision response was nested under the function result envelope. Repaired the harness to inspect the canonical nested decision object.

No production redesign was required.

## Important boundary

This consolidated acceptance proves the **human-originating compounding chain** in one live browser transaction.

It does **not** falsely merge the separately proven governed side-effect action from Proof 7 into this transaction. Proof 7 remains the independent production proof for governed action, receipt binding, policy improvement, and successor action execution.

## Source hygiene

The temporary experimental modification to `.github/workflows/verify-human-smart-note-capture.yml` was restored to the prior standalone human-capture workflow after the local consolidated acceptance completed. The failed workflow run therefore does not remain as the canonical human-capture proof.

## Next Naya continuation

The next acceptance boundary is no longer the human Smart Note → compounding core. It is:

**human Hub surface completeness → Search → Reports → Settings → Dream → Naya Play → broader Lists/Spaces/Connections/Share/Mail journeys → governance/adversarial regression → final public Welcome/front-door activation.**

Do not reopen the proven Smart Note/PIS canonical event identity boundary without new evidence.
