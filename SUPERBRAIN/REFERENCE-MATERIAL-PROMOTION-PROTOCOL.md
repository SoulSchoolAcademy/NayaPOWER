# REFERENCE MATERIAL → CANONICAL INTELLIGENCE PROTOCOL

**STATUS:** CANONICAL  
**PURPOSE:** Define how long-form source material—including PDFs—becomes useful, traceable NayaPOWER intelligence without turning a document folder into an uncontrolled second source of truth.

## 1. SOURCE CLASSES

NayaPOWER distinguishes:

- **CONTROL PLANE:** current operational truth and authority.
- **CANONICAL KNOWLEDGE:** maintained Markdown/contracts/protocols that agents should rely on directly.
- **REFERENCE MATERIAL:** PDFs, papers, exported documents, research, historical specifications, and other source artifacts.
- **EVIDENCE:** receipts, workflow artifacts, logs, browser observations, production observations.
- **HISTORY:** preserved records of what was true or attempted at an earlier time.

A PDF is **reference material by default**. It does not become canonical merely because it is stored in the repository or on the authorized computer.

## 2. WHERE MATERIAL BELONGS

Preferred repository structure:

```
REFERENCES/
  PDFs/
  Research/
  External/

SUPERBRAIN/
  MASTER-NOTES/
  ...
  
NAYA/
  KNOWLEDGE/
  ...
```

Use the repository's existing canonical structure when one already exists. Do not create a new parallel knowledge hierarchy merely for convenience.

If a source is important enough to affect execution, its distilled operational meaning should normally be represented in a canonical Markdown artifact under the appropriate existing NayaPOWER knowledge area.

## 3. THE PROMOTION PIPELINE

### Stage 0 — REFERENCE

Store the original source with stable identity/provenance where permitted.

Record enough metadata to identify:

- title;
- source/author when known;
- date/version when known;
- file identity/hash when available;
- acquisition/context;
- relationship to the project.

### Stage 1 — INSPECT

Read only the portions relevant to the current question when possible.

Do not treat an unreviewed document as truth.

### Stage 2 — EXTRACT

Extract claims, definitions, requirements, decisions, constraints, mechanisms, examples, and evidence.

Separate:

- what the source states;
- what the source demonstrates;
- what is interpretation;
- what is obsolete or historical.

### Stage 3 — NORMALIZE

Convert useful material into concise, searchable Markdown.

Preserve the source's provenance and distinguish direct source facts from interpretation.

### Stage 4 — VERIFY

Before promoting a consequential claim, verify it against the strongest available source.

Verification may include:

- a second authoritative source;
- repository implementation;
- current runtime behavior;
- current governance contract;
- direct evidence;
- human/browser observation.

A reference claim that conflicts with current canonical truth must not silently overwrite it.

### Stage 5 — CANONICALIZE

If the information is durable and operationally useful, place it in the appropriate canonical Markdown/intelligence artifact.

The canonical artifact should state:

- the knowledge/decision;
- why it matters;
- source provenance;
- verification status;
- scope;
- date/currentness;
- supersession status where applicable.

### Stage 6 — PROMOTE

Promotion into reusable intelligence occurs only when the content has semantic value beyond being a copy of the source.

Examples of promotable intelligence:

- a reusable rule;
- a verified architectural constraint;
- a validated pattern;
- a durable decision;
- a proven lesson;
- a generalizable procedure;
- a verified relationship between cause and outcome.

Examples that normally remain reference/evidence:

- an unchanged source document;
- raw logs;
- screenshots;
- receipts;
- temporary debugging output;
- historical claims that are no longer current;
- communication/event records whose value is primarily their occurrence.

### Stage 7 — TRACE

Promoted intelligence must remain traceable back to its source and verification evidence.

Do not strip provenance during summarization.

## 4. SEMANTIC GATE

Before promotion, answer:

1. **What is this?**
2. **Is it reusable understanding?**
3. **Who/what does it apply to?**
4. **What evidence supports it?**
5. **Is it current or historical?**
6. **Does it supersede anything?**
7. **Can a future Naya use it to make a better decision or action?**

If those questions cannot be answered, keep it as reference material or evidence and mark the uncertainty.

## 5. PDF FOLDER RULE

A folder containing many PDFs can be useful as a **reference library**.

It should NOT be treated as:

- the control plane;
- authorization;
- current project state;
- an automatic knowledge base;
- proof;
- a substitute for canonical Markdown/intelligence.

The preferred pattern is:

**PDF → relevant extraction → verified canonical intelligence → provenance → future retrieval**

not:

**PDF pile → agent guesses what matters.**

## 6. COLD-AGENT RULE

A fresh Coda should be able to operate from repository truth without needing to have previously seen the source documents.

Therefore, any reference that is essential to recurring execution should have its important operational conclusions represented in canonical, searchable repository knowledge.

The original PDF remains valuable as the deeper source.

## 7. CONFLICT RULE

If reference material conflicts with current canonical project truth:

- do not silently update canonical truth;
- preserve the source;
- identify the conflict;
- determine whether the source is historical, superseded, scoped differently, or evidence of a regression;
- escalate consequential ambiguity to the appropriate authority.

**Reference material informs canonical intelligence; it does not silently override it.**

## 8. PROMOTION RECEIPT

For consequential promoted intelligence, retain a durable record of:

- source identity;
- extracted claim;
- semantic class;
- verification evidence;
- canonical destination;
- promotion decision;
- timestamp/version;
- supersession relationship if applicable.

This keeps intelligence auditable and prevents a polished summary from becoming an unexplained assertion.

## 9. NORTH STAR

**Store documents for depth.  
Store canonical intelligence for continuity.  
Store evidence for proof.  
Store control-plane state for action.**

That separation lets NayaPOWER compound knowledge without turning memory into an uncontrolled document pile.
