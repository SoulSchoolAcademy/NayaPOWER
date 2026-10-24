# NayaNET Citizen Discovery + AutoMatch — executable V1 seam (draft)

**Seat:** Naya Tree (T) · **Owner lanes:** Citizen Trinity / Nitro, Onboarding XP #1598, Smart Spaces #1891, Project Intelligence #3012, Security #2823, independent VERIFY.

**Authority:** Human Director's spoken vision (2026-10-23 ~17:01 local); existing Citizen Trinity brief; Smart Note SN-1769 (the town matchmaker); SN-0843 (6 × 3 North Star). This is a **candidate implementation**, not a new system of record, identity provider, permission engine or deployed recommender.

## Why this code belongs here

The existing `HUB/app/js/naya-intake.js` legitimately processes Welcome/invite flows and its backend writes to `invites`. Modifying its submit path to create citizen profiles would conflate unrelated records and could bypass authentication. The existing Welcome page remains deliberately simple under #1598. This module is a **companion post-Welcome discovery step** and source of *draft data*, designed for authorized assembly by the existing Trinity/Smart Factory owners.

## Executable files

- `HUB/citizen-discovery-core.js` — dependency-free browser/Node data engine, ten optional questions, preview-only Personal/Business/Space assembly, opt-in public-discovery features, deterministic public-only topic classification and candidate ranking.
- `HUB/citizen-discovery-preview.html` — screen-by-screen prototype, Speak via browser SpeechRecognition where available, Type/Paste, Copy prompt to any AI you choose (no automatic prompt transmission), Next/Back/Skip/Edit, review and per-answer visibility controls, preview three unpublished pages.
- `tests/citizen_discovery.test.mjs` — adversarial Node built-in tests, no network or credentials.

No new cron, data table, duplicate Hub, account creation, profile write, connection, invitation, Space join, mail send or auto-publish is present. All text is displayed with DOM `textContent`; no raw user HTML interpolation. No localStorage, telemetry of raw answers or background upload. Browser speech APIs may use a browser/vendor speech service; the UI discloses it and works without it.

## Personal → Business → Space one-question discovery

1. About you (personal).
2. Interests (personal; optional discovery).
3. Mission (personal; optional discovery).
4. Vision (personal; optional discovery).
5. Goals (personal; optional discovery).
6. Motto (personal; remains private in matching).
7. Business/project/cause (business; optional discovery).
8. Offers/contributions (business; optional discovery).
9. Community/Space topics (space; optional discovery).
10. Desired connections (space; optional discovery).

Any question may be skipped. An empty Business or Space remains an **absent draft**, not an invented public entity. The last screen lets the person edit every answer and opt in to only the fields they want discoverable. **Changing or skipping an answer revokes its prior public-discovery grant.** Discovery opt-in is separately off by default. The result is a private JSON draft preview; **trusted owner identity is checked only at a future governed authenticated write boundary**. An unsigned alias in the draft is not authority.

## AutoMatch behavior — permission first, relevance second

1. **Candidate admission:** only eligible `visibility=public`, `discoverable=true`, not opted out, not self, not blocked; no private mail or Space-member field. Private scoped discovery requires a separate issuer-authenticated server/RLS gate and is NOT implemented here.
2. **Conservative classification:** `classifyPublicItem()` reads only explicitly public title, description and published tags; maps them to controlled V1 categories (learning, technology, business, community, creativity, environment). It returns classifications linked to canonical IDs; `organizePublicItems()` returns category→ID projections, never copies or edits the originals. This is a basic deterministic taxonomy, not trained semantic understanding.
3. **Ranking:** `rankPublicCandidates()` uses context-specific token overlap with weights **topics 40 / goals 25 / offers 20 / sought connections 15**. Only public/approved personal answers participate. Requires ≥60% reliable feature coverage and two distinct overlapping signals. Emits an **uncalibrated experimental relevance percentage**, signal coverage, reasons and `SUGGEST_ONLY`, not compatibility truth or a rating of human worth.
4. **Next gate:** calibrate rank/weights and fairness/diversity against independent real people and declared goals before showing any result as a trusted production match percentage. The internal `nayanet_applicability_match` RPC is KNOW-context equality with default 0.5, **not this social permission or match engine**. Do not substitute it as an authorization check.
5. **Actions:** CONNECT, publish, private mail, private Space join, inviting, notifications and sharing remain user/recipient/LAW governed actions. No automated relationship creation; a click on CONNECT expresses a viewer's interest, **not consent for unauthorized recipient contact**. “Connect”, not “Follow”.

## Governance/real integration — remaining owner work

| Lane | Smallest integration | Independent acceptance |
| --- | --- | --- |
| Nitro Citizen Trinity | Authenticated alias → idempotent, reviewed private Personal / optional Business / Space drafts in existing flagship records | Claimed identity shows correct own content, second account cannot edit, skip leaves no imaginary business |
| Naya 2 #1598 | Wire post-Hub Talk-to-Naya discovery UI using design-parts library; preserve first Welcome page and current invite flow | Real voice/type/AI-paste, Back/Skip/Edit on desktop/mobile/keyboard, no answer loss or covert upload |
| Smart Spaces #1891 / Projects | One owner-approved typed Project↔Space link, same event/source ID in permitted pages, people can disconnect | A/B correct, unrelated C DENY, no duplicate posts or involuntary join |
| Security #2823 | Replace production `connections` anonymous ALL and broad membership reads; secure identity alias and private mail | Real authenticated A/B exchange, C cannot read/write/send-as or spoof; revoked rights refuse |
| KNOW/Value/VERIFY | Calibrate relevance and denominators/coverage, explanations, diversity and feedback; independent 6×3 human/Naya tests | No private inference; plausible useful introductions and measured completion vs no-matching baseline |
| Integrator | Adopt only once existing ownership and current WIP/merge gates permit; attach evidence to canonical Projects/Hub/Factory | Exact source SHA and deployed SHA, independent reviewer, rollback and genuine user outcomes |

**What can be claimed right now:** a tested post-Welcome discovery and public-only matching **prototype**. Not live AutoMatch, not real account creation, not automatic Trinity publishing, and not production-qualified 9.5+/10 user experience.

**Why this is still valuable:** it establishes a small, executable, inspectable seam for the Director's game-of-match vision while isolating high-risk identity and privacy operations until existing owners have verified them.
