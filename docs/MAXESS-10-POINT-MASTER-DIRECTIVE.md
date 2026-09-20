# 🔥 MAXESS — 10-POINT MASTER EXECUTION DIRECTIVE

**Status:** ACTIVE
**North Star:** Make MAXESS work completely and accurately without wrecking the verified experience.
**Repository:** `SoulSchoolAcademy/MaxRESULTS`
**Governance:** `main`

## 0. NORTH STAR

The objective is not to preserve code for its own sake. The objective is to preserve **working behavior** while changing whatever code is genuinely required to make the product work.

Use this rule:

> **PRESERVE WHAT WORKS → CHANGE ONLY WHAT MUST CHANGE → VERIFY THE ACTUAL PRODUCT → REPAIR → FREEZE.**

Never confuse preservation with refusal to edit. If a feature is broken, edit the code until the feature works. If a component is already working, do not redesign, replace, or unnecessarily restructure it.

---

## 1. SOURCE-OF-TRUTH LAW

Before every consequential action:

1. Read the repository README/index and governing MAXESS/Naya instructions.
2. Inspect the current `main` artifact, not conversation memory.
3. Establish the current HEAD and relevant file/blob SHA.
4. Identify the exact runtime source of truth.
5. Identify what is protected and what is actually broken.
6. Work from the latest verified checkpoint.

Unknown is **UNKNOWN**. Never guess.

---

## 2. FROZEN-GOOD EXPERIENCE

Protect these unless the task explicitly requires otherwise:

- existing 15-question wording;
- existing answer choices and radio/selection interaction;
- existing scoring architecture;
- existing Naya behavior and opening experience;
- Naya Profile 6 image;
- existing visual design, responsive behavior, and accessibility;
- existing E01/E02/E03/E04 presentation structure;
- existing result-generation architecture.

Do not redesign the assessment to solve a flow problem.

---

## 3. Q15 FLOW LAW

The intended completion path is exactly:

**QUESTION 15 → SAVE ANSWER → AUTHORITATIVE RESULT GENERATION → PUBLISH `MAXESS_RESULT_V1` → RESULTS**

There must be:

- no visible Interest page;
- no Interest-page selection requirement;
- no “Continue to My Report” intermediary;
- no unnecessary completion gate;
- no second scoring pass.

The safest implementation is behavioral: preserve dormant legacy markup/functions when they are harmless, but make the old Interest/Complete path unreachable from Q15. Do not delete unrelated UI/CSS merely to hide the path.

---

## 4. DATA CONTRACT LAW

`window.MAXESS_RESULT` is the authoritative runtime result.

The result must originate from the user's actual 15 answers and one authoritative scoring engine.

Required chain:

**15 ANSWERS → AUTHORITATIVE SCORING → `MAXESS_RESULT_V1` → `window.MAXESS_RESULT` → E01/E02/E03/E04 → PERSONALIZED REPORT**

No hard-coded scores. No demo fallbacks. No invented values. No independent competing score source.

Before display, validate the contract. If required data is absent, fail safely with an explicit unavailable state rather than fake data.

---

## 5. RESULT ACCURACY LAW

### E01

Display the authoritative `overallScore`.

### E02

Render the **actual dimensions returned by `MAXESS_RESULT`**. Do not hard-code a dimension list that can drift from the assessment engine.

For every dimension display:

- authoritative dimension name;
- authoritative score;
- correct band/label where defined;
- correct order from the result contract.

### E03

Consume the same authoritative result for:

- overall score;
- mastery band;
- dimensions;
- strongest capability;
- opportunity;
- fingerprint;
- personalized analysis.

### E04

Resolve the authoritative `Direction` dimension from the result contract and derive its capability position from that real score.

All four sections must represent the **same completed assessment**.

---

## 6. MINIMUM-CHANGE ENGINEERING

When a defect is found:

1. Trace the actual execution/data path.
2. Identify the smallest causal defect.
3. Change the smallest coherent unit that fixes it.
4. Do not remove working architecture merely because it is no longer reached.
5. Do not rewrite a large artifact from a truncated representation.
6. Do not introduce a second renderer, scorer, or result contract.
7. Do not change unrelated files.

A successful change is measured by **working behavior**, not by how much code was changed.

---

## 7. EXECUTE → VERIFY → CRITIQUE → REPAIR

Every material implementation must pass all four phases.

### EXECUTE

Apply the required code change.

### VERIFY

Re-fetch the changed artifact and inspect the resulting source/diff.

### CRITIQUE — OSCAR

Ask:

> **WHY IS THIS NOT A 10?**

Specifically check:

- boot/runtime failure;
- broken event flow;
- stale or fake data;
- result-contract mismatch;
- regression of working UI;
- mobile/responsive regression;
- accessibility regression;
- deployment/path mismatch;
- accidental redesign;
- temporary tooling left behind;
- incomplete requirement.

### REPAIR

If Oscar finds a material defect, repair it before declaring completion.

---

## 8. RELEASE GATE

Do not call a batch complete until these are proven as applicable:

### Assessment

- loads;
- Naya loads;
- Q1 works;
- all 15 questions work;
- radio/answer selection works;
- Continue works;
- Q15 saves correctly;
- Q15 goes directly to Results;
- Interest page never appears.

### Result contract

- `MAXESS_RESULT_V1` exists;
- overall score is correct;
- all returned dimensions are present;
- mastery band is correct;
- fingerprint is correct;
- strongest dimension is correct;
- opportunity dimension is correct.

### Results

- E01 shows the real overall score;
- E02 shows the real returned dimensions;
- E03 uses the real result contract;
- E04 shows the real Direction score;
- no demo/fallback scores;
- no stale hard-coded result data.

### Preservation

- Naya image remains correct;
- existing visual design remains intact;
- existing interactions remain intact;
- no unrelated files changed;
- no temporary execution machinery remains.

### Evidence

- GitHub diff inspected;
- changed source re-fetched;
- source-level behavior verified;
- live/browser behavior verified when available;
- any remaining human-only verification explicitly stated.

---

## 9. FAILURE RULE

If the live product does not load, **stop feature work**.

First restore the last known-good checkpoint or isolate the smallest boot-breaking change.

Never stack additional changes on an unverified broken build.

A live failure overrides source-level confidence.

---

## 10. FREEZE AND FORWARD MOTION

Once a checkpoint passes the release gate:

- record the commit SHA;
- identify the protected behaviors;
- treat the checkpoint as the new baseline;
- move only to the next actual defect/feature.

Never restart the project because one feature needs repair.

Never preserve a broken behavior merely because it is old.

### Operating command

**Find the real problem → change only what is necessary → prove it works → score it → repair until 10 → freeze → move forward.**

---

## DEFINITIVE PRIORITY ORDER

When instructions appear to conflict, use this order:

1. **Working product / user outcome**
2. **Accuracy of real user data**
3. **Preservation of already-working behavior**
4. **Minimal coherent code change**
5. **Architectural cleanliness**
6. **Cosmetic/code elegance**

Code is the means. **A working, accurate MAXESS experience is the North Star.**
