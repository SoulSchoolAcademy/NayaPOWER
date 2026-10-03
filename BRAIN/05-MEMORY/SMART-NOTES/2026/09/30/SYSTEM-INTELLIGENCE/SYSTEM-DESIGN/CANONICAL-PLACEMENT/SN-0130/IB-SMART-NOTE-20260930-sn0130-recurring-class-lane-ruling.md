# Intelligent Block — SN-130

- **Intelligent Block:** SN-130 — Route Recurring Repair Classes to a Lane Ruling
- **Truth state:** CANDIDATE (proactive auto-capture; only Shawn ratifies)
- **Scope:** PRIVATE
- **Captured date:** 2026-10-02
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The 05-MEMORY projection-count drift has now been repaired three times (#1251, #1301, and the current instance) — and the third instance shows the repair is patching a classification dispute, not a count bug. Byte-verified +3: (1) SN-018's original capture, (2) SN-018's verified-projection copy (264-line diff, self-declares "not a second source of truth"), (3) SN-019's capture. The runtime registry `.naya/memory/smart-notes/index.json` registers SN-018 once; the file counter counts it twice. When the same repair class recurs a third time, stop patching instances — route the class question to the owning lane: do verified projections live under `SMART-NOTES/SN-*/` as counted notes, or relocate to a projections path? Instance patches never close a class dispute.

## HUMAN NOTE

Shawn: the brain-index drift fix isn't failing — the count keeps moving because the rule for what counts keeps being ambiguous. There are two copies of SN-018's note on disk (the original capture and a verified projection copy that says it's "not a second source of truth"), and the registry counts one while the file counter counts two. We've now patched this three times. The real fix isn't another patch — it's your Smart-Note lane ruling once, clearly: do verified projections count as notes under the SN folder, or do they move to a projections folder? One ruling, applied everywhere, ends the cycle.

## CHILD NOTE

If your room keeps getting messy in the same way three weekends in a row, cleaning it again won't fix it. The fix is a family rule about where the toys go. One rule, once, fixes every future weekend.

## GRANDMA NOTE

Three times the pipes froze this winter. The plumber doesn't need to come a fourth time — what you need is the answer to "do we heat the basement or drain the pipes?" Answer the question once and the freezes stop.

## NAYA NOTE

Sisters: the class-vs-instance distinction is the load-bearing part. Instance repairs (#1251, #1301, and now) each fixed their own delta correctly — and the class survived, because each instance patched the count without settling the classification: are verified projections counted notes? Note the split evidence inside the +3: the runtime registry treats SN-018 as one note (projection not separately registered); the brain-index file counter treats it as two files. Neither is wrong — they're counting different things, and the class question is which one is canonical for the drift check. The standing protocol this note proposes: **three strikes and the class goes to the owning lane** — when the same defect class recurs a third time, the repair work pauses and the owning lane issues a written ruling on the class (placement rule + count rule + one deliberate bump), which the lanes then execute once. Do not merge a fourth instance patch before the ruling lands — it would just move the ambiguity.

## MACHINE NOTE

```json
{
  "sn": "SN-130",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-02",
  "taxonomy": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CANONICAL-PLACEMENT",
  "sibling": ["SN-062", "SN-078", "SN-128"],
  "lesson": "When a defect class recurs a third time, stop patching instances and route the class question to the owning lane for a written ruling; instance patches never close a classification dispute.",
  "evidence": {
    "board": "#554 comment 5944290497 (Naya 4 self-build sign-out, 2026-10-02T02:09:19Z)",
    "occurrences": ["PR #1251 (05-MEMORY 21)", "PR #1301 (05-MEMORY 21->23)", "current (05-MEMORY +3 vs expected)"],
    "byte_verified_plus3": [
      {"item": "SN-018 original capture", "path_class": "10/01", "blob_prefix": "0a00a49b"},
      {"item": "SN-018 verified-projection copy", "path_class": "10/02", "blob_prefix": "6d22e769", "diff": "264 lines, same SN id + filename, different content, self-declares not a second source of truth"},
      {"item": "SN-019 capture", "landed": "2026-10-02T01:59Z"}
    ],
    "classification_split": {
      "runtime_registry": ".naya/memory/smart-notes/index.json registers SN-018 once",
      "file_counter": "brain-index file counter counts SN-018 twice"
    }
  },
  "rule": "three-strikes-class-escalation: third recurrence of a repair class → owning lane issues a written ruling (placement rule + count rule + one deliberate bump); no fourth instance patch before the ruling.",
  "class_question": "Do verified projections live under SMART-NOTES/SN-*/ as counted notes, or relocate to a projections path?",
  "ratification": "NOT_RATIFIED — only Shawn ratifies"
}
```
