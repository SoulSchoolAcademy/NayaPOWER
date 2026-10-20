# A Parent's Receipt Does Not Close Its Child Gap Brief — Match the Exact Brief Name in the Receipt Body, Never the Filename Substring

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01741-parent-receipt-does-not-close-child-gap
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A dispatcher receipt sweep matched a queued gap follow-up (`brief-gap-t1034-lane10.md`) against a receipt filename by substring (`t1034-lane10.md`) and nearly closed it — but the receipt's bytes named the PARENT brief (`brief-t1034-lane10.md`), not the gap child (0 hits for the gap name in the receipt body). Closing on filename substring lets a parent's receipt close its child. The rule: a receipt closes a queued brief only when the receipt's body bytes contain the exact queued brief filename AND the receipt post-dates the brief (the t1062 direction rule). Filename matching alone never closes anything. This does not contradict SN-01706's stem matching: SN-01706 matches the filename stem across two name-spaces (queue name vs claimed/ path) for the SAME brief; this rule forbids matching a PART of the filename to claim a DIFFERENT brief. The identity unit is the exact brief filename — `brief-gap-X` and `brief-X` are different entities.

## 🩷 HUMAN NOTE

Shawn — the dispatcher checks "did this job finish?" by looking for its receipt. Tonight the check almost closed a follow-up job using a receipt that belonged to the job it followed up on. The receipt file shared part of the name, but its contents named the parent job, not the child. New rule: a receipt only closes the job whose exact name appears inside the receipt's contents — never close a job just because the receipt's filename looks similar.

## 🟣 CHILD NOTE

Imagine two permission slips: one for "field-trip-class-A" and one for "extra-field-trip-class-A." If you file the second slip just because the name contains the first, you marked the wrong trip done. Always read the slip itself — it says which trip it belongs to.

## 🔵 GRANDMA NOTE

Like matching a receipt to a grocery bag: the bag labeled "grocery" and the bag labeled "grocery-return" are two different bags, even though one name sits inside the other. You don't check off the return by looking at the shopping bag's receipt — you read what the receipt actually says.

## 🟠 NAYA NOTE

Apply to every dispatcher receipt sweep before any rotation write: (1) never match receipts to queued briefs by filename substring — gap follow-ups are named `brief-gap-<parent-stem>`, so any substring check on the stem matches the parent's receipt; (2) a receipt closes a brief only when the receipt's body bytes contain the exact queued brief filename AND the receipt post-dates the brief (t1062 direction rule, t1062 case: a parent's own open-gap receipt matched as an execution receipt); (3) reconcile SN-01706 with this: SN-01706 matches the full filename stem across name-spaces (`brief-queue/<name>` vs `brief-queue/claimed/<name>`) for the SAME brief — the entire `<name>` must match; this rule forbids matching a substring of `<name>` to reach a DIFFERENT brief. The identity unit is the exact brief filename; the receipt body is the only authoritative claim of which brief it closes; (4) enforcement sits in the sweep itself — a dequeue on substring match alone fails the close-criteria gate.

## 🟢 MACHINE NOTE

~~~json
{
  "slug": "parent-receipt-does-not-close-child-gap",
  "sn": "SN-1741",
  "title": "A Parent's Receipt Does Not Close Its Child Gap Brief: Match the Exact Brief Name in the Receipt Body, Never the Filename Substring",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-20",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["dispatcher", "reconcile", "receipt", "brief-queue", "queue-sweep", "dequeue"],
  "enforcement": "The dispatcher receipt sweep matches a receipt to a queued brief ONLY when the receipt's body bytes contain the exact queued brief filename AND the receipt post-dates the brief (t1062 direction rule: verify the receipt claims THIS brief's work, not a predecessor's). Matching by filename substring alone (e.g. receipt filename t1034-lane10.md against queued brief-gap-t1034-lane10.md) never closes a brief; a sweep that dequeues on substring match alone fails the close-criteria gate and the rotation write is rolled back.",
  "evidence": {
    "t1074": "lesson-broadcast.md [night-dispatcher t1074, 2026-10-20T21:13Z]: receipt sweep matched brief-gap-t1034-lane10.md against receipt t1034-lane10.md; 0 hits for 'brief-gap-t1034' in the receipt bytes — the receipt names the PARENT (brief-t1034-lane10.md), not the gap follow-up; dequeue blocked by the t1062 rule",
    "t1062": "lesson-broadcast.md [night-dispatcher t1062, 2026-10-20T19:12Z]: alternate-name sweep CAN false-positive — brief-gap-gatestaall-20261019-0610-executor.md matched gate-stall-20261019-0610.md, the brief's own PARENT receipt (open gap follow-up), not an execution receipt; direction matters — receipt must post-date the brief and name it"
  },
  "decision_changed": "Whether a queued brief is dequeued as 'done' on a receipt hit: require the exact brief filename in the receipt's body bytes plus the t1062 post-dating direction check. Substring-matched receipts are triage signals, never close signals.",
  "falsifier": "A documented, ratified dispatcher convention that parent-close propagates to children (closing the parent legitimately closes all its gap children); then parent receipts closing gap briefs is by design and this rule's premise is false. Alternatively: 50+ ticks of substring-only matching with zero parent/child mis-assignments under the brief-gap naming scheme.",
  "mechanism": "Gap follow-ups inherit the parent's filename stem (brief-gap-<parent-stem>), so any substring check on the stem matches the parent's receipt — inherited identity is not unique identity. The receipt's Brief: body field is the author-claimed identity of what the receipt closes; the receipt filename is a labeling convenience. Matching on the filename confuses the receipt name-space with the brief-identity name-space — the same error class SN-01706 identified in the opposite direction (exact-string matching across two name-spaces for the SAME brief).",
  "cousins": ["SN-01706 (reconcile greps match filename stems — the same-brief name-space rule this lesson must be read with, not against)", "t1062 direction rule (receipt must post-date and name the brief)"]
}
~~~
