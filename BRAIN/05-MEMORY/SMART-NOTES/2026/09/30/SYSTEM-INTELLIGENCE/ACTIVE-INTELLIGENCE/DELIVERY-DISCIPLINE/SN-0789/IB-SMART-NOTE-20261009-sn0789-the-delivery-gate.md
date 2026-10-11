# The Delivery Gate — Nothing Goes Out Unless It Is Useful, Valuable, On-Brand, Accurate, and Aligned

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0789-the-delivery-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Shawn Vibert, direct chat 2026-10-09 ~08:15 PDT — dictated as standing law ("write this down"). His words: "Useful valuable yes. Useless no value no. On brand design yes. Off brand design no. Accurate yes. Not accurate no... do not waste time money or energy sending a user, anyone, anything that is useless, that has no value, that is not aligned with their intent." Recorded as RATIFIED standing law in Naya 4 MEMORY.md; entered in brief-template.md hard-prohibitions. This note stays CANDIDATE per the pipeline rule (auto-capture ≠ auto-ratify) pending the normal promotion path.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Before anything goes out to anyone — a report, a message, a file, a delivery — it must pass five checks: useful, valuable, on-brand in design, accurate, and aligned with the recipient's intent. ALL five, or it doesn't send. A useless send wastes the sender's time, money, and energy and the recipient's attention. Silence beats a useless send, every time. The law is enforced by the machine, not by memory: generators and delivery paths must refuse to emit what fails the gate (e.g., the hourly report generator renders a one-page quiet-hour note instead of a recycled full report when nothing is new — implemented in hourly_report_pdf_v6.py, THE DELIVERY GATE rule).

## HUMAN NOTE

Shawn caught the team sending him the same hourly report over and over — no updates, no changes, off the design standard — and dictated the fix as law: if it's useless, valueless, off-brand, inaccurate, or misaligned with what the person actually wants, it never leaves the building. This is the quality bar for every delivery, and it's mechanical: the system must be unable to send what fails, not merely instructed not to.

## CHILD NOTE

Before you give someone something, ask five questions: Is it useful? Is it valuable? Does it look like ours? Is it true? Is it what they actually want? If any answer is no, don't send it. Saying nothing is better than sending junk.

## GRANDMA NOTE

Don't mail a letter nobody needs. If what you made isn't helpful, isn't right, doesn't look proper, or isn't what the person asked for — keep it. Quiet is kinder than clutter.

## NAYA NOTE

The Delivery Gate is now a hard prohibition in every builder brief I issue. Operationally: (1) every recurring generator gets a quiet-path — when there is nothing new, it emits a minimal honest note or nothing, never a recycled artifact; (2) every number in a delivered artifact carries provenance or it doesn't print; (3) design compliance is checked against the block library, not asserted. A gate that passes obvious garbage is not a gate (SN-0784).

## MACHINE NOTE

```json
{
  "sn": "SN-0789",
  "law": "THE_DELIVERY_GATE",
  "ratified_by": "Shawn Vibert, 2026-10-09 ~08:15 PDT (dictated, 'write this down')",
  "gate": {
    "useful": "required", "valuable": "required", "on_brand_design": "required",
    "accurate": "required", "aligned_with_recipient_intent": "required",
    "on_any_failure": "DO_NOT_SEND"
  },
  "enforcement": [
    "brief-template.md hard-prohibitions (all builder briefs)",
    "hourly_report_pdf_v6.py is_quiet_hour() — quiet-hour note instead of recycled report"
  ],
  "pipeline_state": "CANDIDATE (promotion path pending; ratification recorded in MEMORY.md + brief template)"
}
```
