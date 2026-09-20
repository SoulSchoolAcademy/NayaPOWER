# NAYA VERSIONED BACKUP + SAFE EDITING PROTOCOL

**Status:** ACTIVE REPOSITORY STANDARD
**Scope:** MAXESS / Naya / Naya Nitro source editing, design work, code changes, and consequential artifact updates
**Canonical repository:** `SoulSchoolAcademy/MaxRESULTS`
**Created:** 2026-08-20 17:32:47 UTC

## 1. PURPOSE

This protocol prevents accidental destruction, simplification, truncation, replacement, or loss of working project artifacts during AI-assisted editing.

The governing principle is:

> **NEVER EDIT THE ONLY COPY OF SOMETHING THAT WORKS.**

Every consequential edit begins by preserving the exact state that existed immediately before the edit.

The backup is a recovery point, not a competing source of truth.

---

## 2. THE SAFE EDITING SEQUENCE

Every consequential artifact edit follows:

**INSPECT → BASELINE → BACKUP → COPY/WORK → EDIT → COMPARE → VERIFY → COMMIT → REFETCH → VERIFY AGAIN → PROMOTE OR ROLLBACK**

Never skip the baseline or backup step merely because the requested change appears small.

---

## 3. PRE-EDIT BASELINE

Before modifying an existing artifact, record:

- repository;
- governance branch;
- engineering/working branch;
- exact artifact path;
- current commit SHA;
- current blob SHA when available;
- file byte count;
- physical line count where meaningful;
- current functional state;
- protected sections/features;
- known defects;
- requested change scope.

The baseline is the exact state immediately before the edit.

### Important

**Line count alone is not authority.** HTML/CSS/JS may be formatted, minified, or embedded differently. Size changes are a warning signal, not proof of correctness.

However, a dramatic unexplained reduction in source size or structure is an automatic stop condition.

---

## 4. TIMESTAMPED BACKUP LAW

For each consequential edit, create a timestamped recovery copy of the exact pre-edit artifact.

Recommended naming pattern:

`<artifact-name>__BACKUP__YYYYMMDD-HHMMSS-UTC.<ext>`

Example:

`E06-SECTION-06-WORKING__BACKUP__20260820-173247-UTC.html`

The backup must contain the **complete exact pre-edit source**, not a summary, excerpt, reconstruction, minified rewrite, or generated approximation.

The backup should also preserve the baseline metadata in its commit message or accompanying manifest when practical.

---

## 5. BACKUP IS CREATED BEFORE EVERY MATERIAL UPDATE

The backup rule applies to:

- visual redesigns;
- copy changes;
- CSS changes;
- JavaScript changes;
- responsive changes;
- accessibility changes;
- refactors;
- asset replacement;
- Groove preparation;
- deployment preparation;
- automated edits;
- AI-generated code changes.

If the edit could materially change the artifact, it gets a recovery point first.

---

## 6. NEVER RECONSTRUCT WHEN SOURCE EXISTS

If the authoritative source exists in GitHub, Naya must edit that actual source.

Naya must never:

- recreate a page from memory;
- rebuild a large artifact from a summary;
- replace a complete page with a tiny renderer;
- replace working code with a prototype;
- substitute pseudocode for implementation;
- silently remove sections to make an edit easier;
- regenerate an entire artifact when a surgical change is sufficient.

The existing artifact is the starting point.

---

## 7. SURGICAL EDIT LAW

When the user asks for a targeted change, change only the required scope.

Example:

If the user asks to change a value statement and enlarge headlines, do not redesign the entire section unless the user explicitly authorizes a redesign.

Rules:

**PRESERVE WHAT WORKS.**

**EDIT WHAT WAS REQUESTED.**

**RESTRUCTURE ONLY WHEN NECESSARY AND EXPLAIN WHY.**

**DO NOT EXPAND SCOPE SILENTLY.**

---

## 8. DESTRUCTIVE-CHANGE STOP GATE

Naya must STOP before committing if any of these occur without an explicit reason and approval:

- a large artifact becomes dramatically smaller;
- major sections disappear;
- required JavaScript disappears;
- asset references disappear unexpectedly;
- interaction logic disappears;
- responsive rules disappear;
- accessibility behavior disappears;
- a complete implementation becomes a mock/prototype;
- a working artifact becomes an excerpt;
- the new source is substantially different from the requested scope;
- the new source cannot be traced back to the old source;
- the backup cannot be recovered.

### Example

If an artifact changes from approximately 2,200 lines to 36 lines:

> **DESTRUCTIVE CHANGE DETECTED — STOP.**

Do not explain it away as compression unless a controlled comparison proves that the complete implementation is still present and functionally equivalent.

---

## 9. OLD → NEW COMPARISON

Before committing, compare the baseline and candidate.

Check at minimum:

### Structure
- expected major sections remain;
- expected IDs/classes remain;
- required scripts remain;
- required assets remain;
- required forms/interactions remain.

### Scope
- requested changes are present;
- unrelated sections were not silently rewritten;
- protected functionality remains.

### Size/anomaly
- line count;
- byte count;
- suspicious truncation;
- suspicious duplication;
- suspicious source collapse.

### Quality
- syntax/parse validity;
- responsive behavior;
- accessibility;
- visual hierarchy;
- interaction behavior;
- reduced-motion behavior where applicable.

---

## 10. COMMIT DISCIPLINE

The backup and working change must remain traceable in Git history.

Preferred sequence:

1. commit or preserve the timestamped backup;
2. implement the candidate change;
3. inspect the diff;
4. verify the candidate;
5. commit the candidate;
6. re-fetch the committed artifact from GitHub;
7. verify the final artifact again.

Do not claim success merely because the write API returned successfully.

---

## 11. OFFICIAL VERSION / RETENTION LAW

Timestamped backups are **temporary recovery points** during active editing.

While a feature is actively being edited:

- keep the most recent recovery points needed to safely roll back;
- never delete the current known-good baseline before the replacement is verified;
- keep enough history to recover from the latest material failure.

When the user explicitly declares the work **finished / approved / official**, the latest approved rendition becomes the official source.

At that point, old timestamped backup copies for that completed editing cycle may be removed in a controlled cleanup pass.

### Cleanup rule

Do not delete backups merely because they are old.

Delete them only after:

1. the latest rendition is explicitly approved or frozen;
2. the official artifact is verified;
3. a stable Git commit exists;
4. the backup files being removed are no longer needed for rollback;
5. the cleanup itself is reviewed and limited to the intended backup files.

Historical Git commits remain the deeper recovery layer even after temporary backup files are cleaned up.

---

## 12. NEVER DELETE THE ONLY RECOVERY PATH

Before cleanup, Naya must verify that at least one reliable recovery path remains:

- a stable Git commit;
- an explicitly frozen baseline;
- or another approved repository recovery mechanism.

The goal is not to accumulate files forever.

The goal is:

> **Always have a current recovery point while editing, and a clean official source when the work is finished.**

---

## 13. FAILED EDIT RECOVERY

If a candidate edit fails:

**STOP → RESTORE FROM TIMESTAMPED BACKUP → IDENTIFY ROOT CAUSE → REPAIR → CREATE NEW BACKUP → RETEST**

Do not patch repeatedly on top of a known-broken candidate if the clean pre-edit state is available.

Use:

**FAILURE → ROOT CAUSE → RECOVERY → REPAIR → VERIFICATION → SAFEGUARD**

---

## 14. CURRENT-WORKING-BACKUP RULE

During an active editing session, the newest verified pre-edit backup is the immediate recovery point.

If multiple edits are made in one coherent batch, the backup must represent the state immediately before that batch.

If a new risky batch begins after a prior batch has been verified, create a new timestamped backup before beginning the new batch.

This prevents the recovery point from drifting away from the actual state being protected.

---

## 15. DESIGN WORK IS CODE WORK

This protocol applies equally to visual design.

A design edit is not exempt because it is “only CSS.”

For MAXESS design work, preserve:

- existing visual architecture;
- working interactions;
- responsive behavior;
- component relationships;
- typography hierarchy;
- content hierarchy;
- established brand language;
- known-good assets;
- user-tested behavior.

Design improvement must not become accidental product reconstruction.

---

## 16. TRUST STANDARD

A deliverable is trustworthy only when Naya can answer:

1. What exact source did I start from?
2. What exact backup did I preserve?
3. What did I change?
4. What did I intentionally preserve?
5. What evidence proves the candidate is complete?
6. What evidence proves the candidate works?
7. Where is the committed version?
8. Can I restore the prior state immediately?

If any material answer is unknown, the work is **NOT VERIFIED**.

---

## 17. REQUIRED FINAL REPORT

Every consequential edit should report:

### CURRENT STATE
What is actually true.

### BASELINE
Exact source/commit/blob/size information where available.

### BACKUP
Exact timestamped recovery artifact and location.

### CHANGES
What was changed.

### PRESERVED
What was intentionally protected.

### VERIFICATION
What was tested and what passed.

### STATUS
Use:

**IMPLEMENTED · VERIFIED · LIVE VERIFIED · HUMAN REVIEW REQUIRED · BLOCKED · UNKNOWN**

### RECOVERY
How to restore the pre-edit state if needed.

---

## 18. RELATIONSHIP TO NAYA LAW

This document operationalizes the following existing laws:

- Preservation Law
- Baseline Law
- Plan-Before-Edit Law
- Execute → Verify Law
- Regression Law
- Failure → Safeguard Law
- Scope-Protection Law

If this document conflicts with a higher-authority governing document or an explicit current human requirement, resolve the conflict explicitly rather than silently choosing one.

---

## 19. PRIME RULE

> **BACK IT UP. EDIT THE REAL SOURCE. COMPARE IT. VERIFY IT. KEEP THE RECOVERY POINT UNTIL THE NEW VERSION IS PROVEN. ONLY THEN PROMOTE THE NEW VERSION.**
