# 06 — Feature Completion + Activity Contract

## Purpose

The NayaNET Engineering System must not only describe what features are supposed to do. It must preserve a living, reviewable record of what NIS actually did, what was verified, what remains, and how the system progressed over time.

This contract establishes the common completion checklist and activity-feed behavior for every Engineering System feature.

## 1. ONE FEATURE = ONE LIVING ENGINEERING RECORD

Every feature in `NayaNETEngineeringSystem/features/` owns a continuously updated engineering state.

At minimum each feature records:

- definition/contract;
- source-of-truth `.naya` references;
- implementation inventory;
- runtime/backend inventory;
- current state;
- completed work;
- verified evidence;
- open gaps;
- blockers/questions;
- next action;
- dated activity history.

The feature document is the engineering map. The activity history is the chronological work journal. Neither replaces canonical runtime event truth.

## 2. STANDARD COMPLETION CHECKLIST

Every feature uses the same progression:

- [ ] Source contract identified
- [ ] `.naya` authority read
- [ ] Existing repository implementation inspected
- [ ] Existing runtime/backend primitives inspected
- [ ] Canonical data owner identified
- [ ] Front-end surface identified
- [ ] Back-end/API path identified
- [ ] Authority/privacy boundary identified
- [ ] Event/provenance path identified
- [ ] Implementation completed
- [ ] Unit/component tests completed where applicable
- [ ] Integration path tested
- [ ] Persistence verified
- [ ] Authorization/owner isolation verified
- [ ] Source → build parity verified
- [ ] Build → deployed runtime parity verified
- [ ] Authenticated runtime behavior observed
- [ ] Evidence/receipt captured
- [ ] Activity record written
- [ ] Feature document updated
- [ ] Next action recorded

A box is checked only when evidence exists at the level required by the item. Do not convert “planned,” “source exists,” or “looks correct” into completion.

## 3. STATUS

Use the shared vocabulary from `04-VERIFICATION-GOVERNANCE-AND-DELIVERY.md`:

`DEFINED → IMPLEMENTED → TESTED → LIVE VERIFIED → INDEPENDENTLY VERIFIED`

When evidence is insufficient, use `UNKNOWN` or `BLOCKED`. `STALE` and `SUPERSEDED` remain available when historical state is no longer current.

## 4. FEATURE ACTIVITY FEED

Every feature has an activity projection that answers:

**What happened on this feature, when, by whom, what changed, what was verified, and what happens next?**

The feed is chronological and navigable by:

**YEAR → MONTH → DAY → SESSION**

The human-facing UI should expose:

- year selector/index;
- month selector/index;
- day selector/index;
- entries for that day;
- session detail;
- links to changed source/runtime/evidence;
- completion-state change;
- next action.

The user must be able to click a day such as `2026-09-18` and see the work performed on that feature that day, then select `2026-09-17` and review the previous day's work.

## 5. TEAM NAYA ACTIVITY

The Team Naya feed remains the Naya-to-Naya communication journal.

Every substantive Naya engineering session must:

**SIGN IN → WORK → REPORT → VERIFY → SIGN OUT → HAND OFF**

The session record must include:

- Naya/actor identity;
- session identifier where available;
- local date and exact timestamp;
- feature/sub-feature;
- mission;
- work performed;
- files and runtime objects inspected/changed;
- decisions;
- questions/blockers;
- tests executed;
- evidence links;
- verification state;
- what remains;
- exactly one successor action.

The record must use the human-facing local calendar date for navigation, while retaining an exact timestamp for ordering and auditability.

## 6. FEATURE ↔ ACTIVITY CONNECTION

A feature activity entry must carry enough stable information to connect it back to the feature and its evidence.

Conceptually:

```text
FEATURE
  ↓
FEATURE ACTIVITY
  ├── DATE / SESSION
  ├── ACTOR
  ├── WORK
  ├── CHANGES
  ├── TESTS
  ├── EVIDENCE
  ├── COMPLETION STATE
  ├── GAPS
  └── NEXT ACTION
```

A Team Naya communication entry may link to the same canonical event/evidence. It must not create a competing event store merely to make the feed visible.

## 7. ACTIVITY IS NOT A SECOND TRUTH STORE

The canonical event/intelligence substrate remains the source of operational truth.

Activity feeds are projections optimized for human review and Naya-to-Naya continuity.

Therefore:

- do not duplicate canonical intelligence merely to populate a feed;
- preserve source/event identifiers;
- retain provenance;
- allow projections to be rebuilt;
- distinguish communication from durable intelligence;
- distinguish activity from verification.

## 8. ENGINEERING SYSTEM UPDATE RULE

When work changes a feature, the same session must update the feature's engineering document before sign-out.

Minimum update:

1. completion checklist;
2. current state;
3. implementation/runtime evidence;
4. gaps;
5. next action;
6. dated activity entry.

If another feature is affected, update that feature too. Cross-feature changes must be visible from both sides.

This creates the required loop:

`WORK → OBSERVE → VERIFY → UPDATE ENGINEERING → UPDATE ACTIVITY → HANDOFF`

## 9. NO SILENT WORK

Substantive engineering work must not disappear into an undocumented session.

If work was performed but not verified, record it as work performed with the appropriate `UNKNOWN`, `BLOCKED`, `IMPLEMENTED`, or `TESTED` state.

If a defect is discovered, record:

**OBSERVED → DIAGNOSED → CHANGED → RERUN → VERIFIED / BLOCKED**

Do not rewrite history to make a failed attempt appear successful.

## 10. DAILY REVIEW

The activity system should make a daily review trivial:

`2026 / 09 / 19 → Smart Note → sessions → evidence → current completion → next action`

A month view should make progress visible without opening every session, while the day view provides the complete detail.

The same structure must work for every feature and project.

## 11. MINIMUM FEATURE ACTIVITY ENTRY

```text
DATE: YYYY-MM-DD
TIME: YYYY-MM-DDTHH:MM:SS±HH:MM
ACTOR: Naya / human / system
FEATURE: <feature>
SESSION: <stable session id when available>
MISSION: <one sentence>

DONE:
- <completed work>

CHANGED:
- <source/runtime/data changes>

TESTED:
- <tests>

EVIDENCE:
- <commit/runtime/receipt/test reference>

STATE:
- <current status>

REMAINING:
- <open gaps>

NEXT:
- <exactly one continuation action>
```

## 12. PRODUCT REQUIREMENT: SMART TABS

Smart Tabs are the first explicit navigation surface for this contract and must eventually expose the feature/project activity hierarchy through the same persistent top-of-page navigation system.

The Smart Tabs bar itself must not become the activity database. It is the navigation control that gets the human to the appropriate activity projection.

## 13. NEXT ACTION

**Implement the shared feature-activity model and human-facing YEAR → MONTH → DAY → SESSION navigation, then connect each Engineering System feature to its own activity projection and completion checklist. Prove one feature end-to-end first, use that implementation as the pattern, and propagate the same contract without creating duplicate event stores.**
