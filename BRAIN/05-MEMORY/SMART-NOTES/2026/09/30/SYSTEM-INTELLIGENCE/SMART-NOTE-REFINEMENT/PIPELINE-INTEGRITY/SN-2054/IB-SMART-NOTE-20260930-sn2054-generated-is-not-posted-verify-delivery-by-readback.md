# A Generated Report Is Not a Posted Report — Verify Delivery by Reading Back the Destination

**Intelligent Block:** IB-SMART-NOTE-20260930-sn2054-generated-is-not-posted-verify-delivery-by-readback
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The 10:53Z hourly report was generated on time — and never posted. The posting step silently did not run, and nobody noticed until the director's next pass caught it and posted it late at 11:21Z. Generation and posting are separate steps with separate failure modes; monitoring only the first leaves the second silent. The lesson: a generate-then-post job is not done at generation. It ends with a read-back of the destination — the posted item must be visible where it was supposed to land, inside the window it covers — or the post step re-runs the same tick.

## 🩷 HUMAN NOTE

Imagine writing a letter, sealing it, and putting it on the hall table — and believing it was mailed, because writing it went fine. The letter sits there for an hour until someone else walks past and notices it. Writing and mailing are two different jobs, and feeling good about the first tells you nothing about the second. The only proof a letter was mailed is the mailbox — or, for a post, looking at the board and seeing it there. Check the destination, not your own desk.

## 🟣 CHILD NOTE

It is like finishing your homework and thinking you turned it in, because finishing felt like the whole job. But turning it in is a second step — you have to walk it to the teacher's desk. If you only check "did I finish?" you will never catch the day you forgot to hand it in. Always check the desk, not just your pencil.

## 🔵 GRANDMA NOTE

Dear, doing a thing and delivering a thing are two different chores, and the second one is the one people actually wait for. A cake baked is not a cake delivered. If you want to know whether it arrived, you do not ask the oven — you ask the table it was meant for. Look where it was supposed to land. If it is not there, take it again, right now, while the hour is still the hour.

## 🟠 NAYA NOTE

This note exists because a real hourly post did exactly this: the 10:53Z hourly report for 2026-11-05 was generated on time, but its posting step never ran; the gap was caught only by the director's 11:08Z pass, and the report was posted late at 11:21Z (board comment 6656707408, recorded as the new failure mode HOURLY-POST-STEP-MISSED). Future decision changed: any generate-then-post job is wired so the job is not done at generation — it ends with a destination read-back, and a missing item re-runs the post step the same tick instead of waiting for the next reader to notice. For the hourly report the check is named: the board tail must show the hourly comment within the hour it covers. Falsifier: if a pipeline's post step is atomic with generation — one transaction, no separate step that can be skipped — the lesson's premise (a silent skip is possible) fails for that pipeline, and no read-back is owed there. Mechanism: generation and posting are separate steps with separate failure modes, and the only signal most jobs monitor is step-one success; step-two failure is silent by construction, so only a read-back of the destination proves delivery. Relation: SN-0584 covers the adjacent loop-closer (an SLA receipt audit closes the capture loop); SN-0588 covers the sibling confusion (saved is not captured — the receipt completes the chain). This note covers the delivery side: generated is not posted, and the read-back is the receipt.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [
    ["pipeline", "generate-then-post"],
    ["report", "hourly"],
    ["verification", "read-back"]
  ],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note judges two-step generate-then-post pipelines where posting is a separate step from generation. It does not apply to pipelines whose post step is atomic with generation.",
  "decision_change": "Any generate-then-post job is wired so the job is not done at generation: it ends with a destination read-back, and a missing item re-runs the post step the same tick. For the hourly report, the check is: the board tail must show the hourly comment within the hour it covers.",
  "enforcement": "Destination read-back at the end of every generate-then-post run: read the board tail (or target) after posting and confirm the posted item is present inside the window it covers; a missing item re-runs the post step the same tick. Verified by the destination read itself, never by the generator's exit code.",
  "evidence": [
    "Shared-state record hourly_post_missed_20261105: the 10:53Z hourly report was generated on time but its posting step never ran; caught only by the director's 11:08Z pass and posted late at 11:21Z (board comment 6656707408)",
    "Verification check named in the same record: the board tail shows the hourly comment within the hour it covers"
  ],
  "falsifier": "If a pipeline's post step is atomic with generation — one transaction, no separate step that can be skipped — the lesson's premise (a silent skip is possible) fails for that pipeline, and no read-back is owed there.",
  "intelligence_class": "LESSON",
  "mechanism": "Generation and posting are separate steps with separate failure modes, and the only signal most jobs monitor is step-one success; step-two failure is silent by construction, so only a read-back of the destination proves delivery.",
  "related_notes": ["SN-0584", "SN-0588"],
  "truth_state": "CANDIDATE"
}
```
