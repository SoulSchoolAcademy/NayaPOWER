# TEAM NAYA — SMART LINK + HUMAN EVIDENCE LAW

## 🔴 ZERO-AMBIGUITY SMART LINK LAW — READ THIS BEFORE USING THE TERM “SMART LINK”

**Canonical contract:** `.naya/codex/NAYA-LINK-IDENTITY-AND-EVIDENCE-CONTRACT-V1.md`

> **SMART LINK = DIRECT GITHUB LINK TO THE CANONICAL HUMAN-READABLE `smart-note.md` ARTIFACT.**

A Hub/runtime URL such as `/hub?ib=IB-XXXXXX` is a **Hub Deep Link**, never a Smart Link. A receipt/event/workflow/commit URL is an **Evidence/Provenance Link**, never a Smart Note Smart Link.

**Before saying “Smart Link,” verify:** the URL lands on `.naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md`, the file exists on the reported canonical branch, and the file contains the same IB ID being reported. If the repository projection does not exist, report **SMART LINK: PENDING**. Never substitute a runtime link.

**This distinction is mandatory for every Naya, handoff, report, test, and UI label.**


**STATUS:** CANONICAL TEAM-NAYA OPERATING LAW V1
**DATE:** 2026-09-17
**AUDIENCE:** Every Naya, Team Naya, and every human-facing handoff

## 1. THE RULE

> **DO NOT TELL SHAWN THAT WORK EXISTS. SHOW SHAWN THE WORK.**

Whenever Naya creates, changes, or claims a durable repository artifact, the human-facing handoff must provide a **Smart Link** to the actual artifact whenever a navigable URL exists.

A commit SHA, internal ID, tool result, filename in gray/code formatting, or prose assertion is **not a substitute** for the clickable artifact link.

## 2. WHAT A SMART LINK IS

A **Smart Link** is:

**a direct, clickable, navigable link to the actual durable artifact or evidence that supports the claim being made.**

Examples:

- a Markdown Smart Note → direct GitHub file link;
- a verification receipt → direct GitHub file link;
- an Activity record → direct GitHub file link;
- a continuation prompt → direct GitHub file link;
- a JSON control-plane record → direct GitHub file link when machine inspection is useful;
- a standalone HTML artifact → direct GitHub file link;
- a workflow/run/artifact → direct navigable evidence link when available;
- a live deployment claim → direct public runtime URL plus deployment evidence when available.

## 3. WHY THE SMART LINK EXISTS

The purpose is independent inspection.

The human should not have to trust:

> “I created it.”

The human should be able to click:

> **HERE IS THE ARTIFACT.**

Then inspect the actual work.

This is evidence discipline, not decoration.

## 4. HUMAN DELIVERY STANDARD

For every meaningful durable artifact, use this pattern:

**WHAT WAS CREATED/CHANGED**

→ **SMART LINK — CLICK THE ACTUAL ARTIFACT**

→ **WHAT WAS VERIFIED**

→ **EVIDENCE**

→ **WHAT REMAINS UNKNOWN**

When multiple artifacts matter, link each one individually.

Do not dump a list of SHAs and expect the human to reconstruct which file changed.

## 5. SMART LINK PRIORITY

For human-facing delivery, use this order:

1. **Human-readable artifact link**
2. **Verification receipt link**
3. **AI Smart Note link**, when applicable
4. **Canonical JSON/event link**, when useful
5. **Commit/PR/workflow identifiers**, as secondary provenance

A commit SHA is useful for provenance and reproducibility.

It is **not the primary human receipt** when the artifact itself has a navigable URL.

## 6. SMART NOTE DELIVERY

When reporting a Smart Note:

**Human Smart Note → Verification Receipt → AI Smart Note (optional) → Canonical Event JSON (optional/system use)**

Never give a raw JSON link and label it simply “Smart Note” when Shawn needs the readable note.

The canonical Smart Notes human-readable delivery law already requires this distinction.

## 7. ACTIVITY DELIVERY

When meaningful Activity is created, provide a direct link to the actual Activity record when one exists.

The human should be able to click the record and inspect:

- actor;
- date/time;
- mission;
- work;
- changes;
- verification;
- learning;
- blockers/unknowns;
- ending state;
- next action/successor.

## 8. CONTINUATION DELIVERY

When Naya says a continuation prompt exists, provide its direct clickable GitHub file link.

The required continuation artifact is:

`.naya/TEAM-NAYA/10-NEXT-NAYA-CONTINUATION-PROMPT.md`

A filename shown as code is only a locator hint. The **Smart Link is the usable human handoff**.

## 9. EVIDENCE CLAIM LAW

Every evidence-backed human-facing claim should answer:

**WHAT → WHERE → WHAT WAS OBSERVED → WHAT DOES THAT PROVE → WHAT DOES IT NOT PROVE**

Example:

**Activity record created** → clickable Activity link → file exists at the linked path → proves the record exists in GitHub → does not by itself prove the Activity UI rendered it live.

This prevents artifact existence from being confused with runtime behavior.

## 10. NO-SHA-ONLY RULE

Do not use a commit number as the sole human-facing proof of meaningful work.

Bad:

> “Done. Commit `abc123`.”

Correct:

> **Activity record:** [clickable artifact]
>
> **Smart Note:** [clickable artifact]
>
> **Verification receipt:** [clickable artifact]
>
> **Commit:** `abc123` (secondary provenance)

## 11. NO-GRAY-CODE-ONLY RULE

Putting a repository path in inline code does not make it a Smart Link.

Putting a path in a heading does not make it a Smart Link.

Mentioning that a file exists does not make it evidence.

**A Smart Link must be navigable.**

## 12. TEAM NAYA RESPONSIBILITY

Every Naya must know this rule before substantive execution.

Every Team Naya handoff must include Smart Links for the material artifacts produced during that execution.

Every successor must be able to click directly into the evidence instead of performing repository archaeology.

## 13. RELATION TO EXISTING LAWS

This law strengthens, and does not replace:

- Runtime Constitution;
- Team Naya Execution Instructions;
- Continuous Torch-Pass Law;
- Smart Notes Human-Readable Delivery Law;
- GitHub-First Freeze-Point Delivery Standard;
- Naya Handoff Template;
- 100-Question Entry Preflight;
- 30-Question Torch Handoff.

## 14. ACCEPTANCE TEST

A human-facing execution handoff fails this law if it says work was done but does not provide a clickable path to the durable artifact when one exists.

A handoff passes when Shawn can:

1. click the artifact;
2. inspect the actual work;
3. click the verification receipt;
4. understand what was verified;
5. see what remains unknown;
6. click the continuation prompt;
7. hand that prompt to the next Naya.

## FINAL LAW

> **DON'T TELL ME. SHOW ME.**
>
> **THE ARTIFACT IS THE EVIDENCE. THE SMART LINK IS THE HUMAN RECEIPT. THE SHA IS PROVENANCE.**

**END — SMART LINK + HUMAN EVIDENCE LAW**
