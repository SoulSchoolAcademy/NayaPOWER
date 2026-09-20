# 🧠 MAXESS V2 — Source + Architecture Inventory

**Date:** August 26, 2026  
**Project:** MAXESS  
**Authority:** MAXESS Master Engineering Design Directive V2

## Decision

MAXESS will not select an old E00 variant as the permanent winner. The new authoritative E00 will be rebuilt from the strongest combined lineage while preserving old artifacts as source material and forensic evidence.

## What we learned

The existing assessment lineage has good UX and correct AI Score mathematics, but multiple authorities exist: page-local state, bridges, controllers, storage fallbacks, polling, legacy globals, and Results-side hydration.

The Results sections E01–E09 contain substantial design value, but some current consumers still acquire results through fallback/polling paths. Those paths must be replaced with one immutable `MAXESS_RESULT_V1` contract.

## What is now authoritative

```text
ASSESSMENT DEFINITION
→ E00 ENGINE
→ RESPONSE STORE
→ SCORING
→ RESULT VALIDATION
→ FROZEN MAXESS_RESULT_V1
→ ONE RELEASE
→ E01–E09
```

## First implementation

A pure, DOM-free E00 engine core has been added at:

`PROJECTS/MAXESS/ENGINEERING/MAXESS-E00-AUTHORITATIVE-ENGINE-V1.js`

It has no storage, timers, polling, DOM scraping, or bridges. It validates the 0–4 answer model, stores responses, calculates scores, builds/validates the result, and freezes the result.

## Dynamic MAXESS

The engine is now designed so AI Score is a configuration-defined assessment, not a special scoring implementation. Future topics must resolve through trusted knowledge/rubric coverage before generating an assessment. Unsupported topics must be handled honestly rather than fabricated.

## Current truth

🟢 Source inventory completed.  
🟢 `MAXESS_RESULT_V1` documented.  
🟢 Authoritative engine core created.  
🟢 Rebuild map created.  
🟢 Dynamic compiler foundation documented.  
🟡 Engine still needs integration into the final E00 visual shell.  
🔴 E01–E09 are not yet fully rewired to the contract.  
🔴 Live end-to-end MAXESS is not yet verified.  
🔴 10/10 is not yet claimed.

## Principle locked

**Preserve the goodness. Remove the architectural weakness. Build the machine that should have existed all along.**
