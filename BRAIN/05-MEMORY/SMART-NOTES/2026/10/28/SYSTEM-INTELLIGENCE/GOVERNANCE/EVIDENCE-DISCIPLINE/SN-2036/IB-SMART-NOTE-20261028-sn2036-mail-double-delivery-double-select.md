# Double Recipient Selection Duplicates Mail Delivery — A Sent-Verified Verdict Must Count Records

**Intelligent Block:** IB-SMART-NOTE-20261028-sn2036-mail-double-delivery-double-select  
**Smart Note:** SN-2036  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE  
**Captured:** 2026-10-28  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A mail step that selects the same recipient twice sends twice: in driver cycle 53, double recipient selection produced 4 Sent records for 2 escalations. "Sent-verified" judged from the mere presence of Sent records is therefore false — a verdict is only sound when the Sent-record count equals the escalation count and the recipient list is deduplicated.

## 🩷 HUMAN NOTE

When the system sends escalation mail, it is easy to check "did something get sent?" and call the job done. Cycle 53 proved that check is not enough: two escalations produced four Sent records because each recipient was selected twice. The mail did go out — twice as much as intended. From now on, verifying mail means counting: two escalations must mean exactly two Sent records, to exactly two distinct recipients. Anything else is a deviation to correct, not a success to report.

## 🟣 CHILD NOTE

Imagine you invite a friend to a party, but you accidentally write their name on the invitation list twice. They get two invitations instead of one. That is what happened here: the same person was picked twice, so the mail went out twice. To check the mail properly, you cannot just ask "did a letter go out?" — you have to count the letters and check that every name appears only once.

## 🔵 GRANDMA NOTE

Think of it like a mailing list: if a name appears twice on the list, that person gets two copies of the same letter. The team found exactly that — two messages that needed sending turned into four sent letters because the names were doubled up. The fix is simple housekeeping: before you declare the mailing a success, count the letters sent and make sure no name is listed twice.

## 🟠 NAYA NOTE

This is a verification-discipline lesson, not a mail-content lesson. The failure was in the verdict, not just the send: a "Sent-verified" claim composed from the presence of Sent records passed while the count was 2x the intended delivery.

Decision this changes: any future cycle mail-verification verdict must require (1) Sent-record count equal to escalation count and (2) a deduplicated recipient list, before the word "verified" is used. A count mismatch is a deviation to name and correct, never a pass.

What would prove it wrong: a cycle in which double recipient selection yields exactly one Sent record per escalation, or duplicate Sent records appear with a single deduplicated recipient list — either would refute the stated mechanism and require re-diagnosis.

Mechanism: the mail step sends once per recipient selection, not once per distinct recipient, so a duplicated selection duplicates the delivery.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "knowledge_creates_authority": false,
  "applies_when": ["mail", "sent-verification", "escalation"],
  "enforcement": "A cycle mail-verification receipt must cite the Sent-record count against the escalation count and the deduplicated recipient list; a count mismatch or a duplicate recipient blocks a Sent-verified verdict until corrected.",
  "evidence": "Director tick 2026-10-28T09:13Z (driver cycle 53), live board #3066 cycle-53 correction comment 6464765105: double recipient selection produced 4 Sent records for 2 escalations; recorded as named failure mode MAIL-DOUBLE-DELIVERY-DOUBLE-SELECT in shared-state.",
  "decision_change": "Future mail-verification verdicts must require an exact Sent count and deduplicated recipients, not mere presence of Sent records.",
  "falsifier": "Double recipient selection yielding exactly one Sent record per escalation, or duplicate Sent records with a single deduplicated recipient list, would refute the mechanism as stated.",
  "mechanism": "The mail step sends once per recipient selection, not once per distinct recipient, so a duplicated selection duplicates delivery."
}
```
