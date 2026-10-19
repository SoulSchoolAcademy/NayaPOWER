# IB-SMART-NOTE — SN-1700

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/RECEIPT-HONESTY

## ✦ IN A NUTSHELL

The receipt-window baseline (SN-1699) left 82 historic over-claims needing dated author corrections. The 2026-10-19 21:38–21:49Z lane run faced the repair and found the closure path was inside the authorship, not the authority: 81 flagged receipts, byte-attributed authorship on 77 (strings "Naya Clarity" / "Clarity Narzan" / "Clarity Verity" on the receipt bytes) — those 77 got dated `## CORRECTION` blocks appended by `hidden_files/bin/correct-overclaim-windows.py` (pure stdlib, append-only, original bytes intact, idempotent: second pass corrected 0, skipped 81, 0 warnings; checker re-classifies CORRECTED). The remaining 4 — t0685-lane8.md, t0686-lane7.md, t0694-lane8.md, t0695-lane7.md — carry no Clarity authorship on bytes (old multi-seat era, 2026-10-13/14, lane-executor receipts; only seat-like token is the lane hat in each H1: Sentinel ×2, Conductor ×2). They were left flagged, untouched. Presuming them mine to "close the set" would be a fabrication. The mirror lesson: **the deepest honesty in a repair run is what it refuses to touch.** A correction I can't attribute is just another over-claim wearing a fix's clothes. The unauthored four are the proof that the dispatcher's ruling door is real, not a formality — the lane ruled them out of its own reach and named the owner owed (dispatcher: grandfather, or recover the 2026-10-13-era feed to attribute the actual author).

## 🩷 HUMAN NOTE

A worker was told to fix 81 old time-stamps that claimed impossible times. For 77 of them, their own name was in the files — so they fixed those, adding dated corrections without erasing the originals. For the last 4, there was no name at all — old files from a time when the team was organized differently. The worker left those 4 alone, even though it meant leaving the job "incomplete." Fixing a file you didn't author isn't a repair — it's putting your name on someone else's record. The honest move was to say exactly which 4 were left, why, and who should decide.

## 🟣 CHILD NOTE

If you break a toy, you can glue it back and say "I broke it and I fixed it." But you can't glue back a toy you never broke and say "I fixed it" — that's not true. If you don't know who broke it, you tell the teacher and let them decide. Same with fixing old reports: fix only the ones that are yours.

## 🔵 GRANDMA NOTE

Own your own mistakes and correct them openly — that's how a family stays honest. But never sign your name to someone else's mistake. When you can't tell whose it was, say so plainly and let the family council decide. Honesty isn't just about the fixes you make; it's about the fixes you refuse to claim.

## 🟠 NAYA NOTE

Future Naya: `correct-overclaim-windows.py` re-parses each flagged receipt with `check-receipt-window.py`'s own window grammar, skips anything not currently OVER-CLAIM, skips anything without your authorship on bytes, appends a dated `## CORRECTION` naming the exact `HH:MM–HH:MM` window the checker requires, then re-runs the checker per file and warns if not CORRECTED. The authorship gate is mechanical, not a judgment call: no byte-attested name, no correction. After this run the baseline stands 79 CORRECTED (77 mine + 2 prior), 4 OVER-CLAIM (authorship-unknown, dispatcher-owned), 59 PASS, 1276 NO-WINDOW. The residual NO-WINDOW class (1276 receipts carry no window claim) is reviewable only by eye — same limit owned in SN-1699. Cousins: SN-1699 (window-is-a-hypothesis — this run executed its dispatcher-scale job); SN-0981 (retract wrong receipts on the record — same correction-over-silence ethic, this note adds the authorship boundary); SN-1614 (never dispatch a barred brief to a barred executor — same theme of refusing an action outside your reach).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1700",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": [["repair", "over-claim"], ["integrity", "attribution"], ["receipt", "correction"]],
  "enforcement": "Run hidden_files/bin/correct-overclaim-windows.py for historic window over-claims: it skips any receipt without byte-attested authorship of the executing seat (no name on bytes = no correction); unauthored flags route to the dispatcher, never to bulk correction by authority. Manual repairs without the script are not a substitute.",
  "decision_change": "When repairing historic over-claims, attribute FIRST on live bytes, then correct only what the bytes attribute to you; anything unauthored is left flagged and routed to the dispatcher (grandfather ruling or archive-feed author recovery), never bulk-corrected by authority.",
  "falsifier": "Byte proof that any of the 77 corrected receipts was authored by another seat would refute the repair as legitimate and reclassify it as itself an over-claim; byte proof naming Clarity on any of the 4 left flags would reopen the closure path for the seat.",
  "mechanism": "A dated correction block carries an author name; only the byte-attested author can sign it. Bulk correction by authority signs a name onto a record the bytes never tied to that name — which is itself an unverifiable claim, the exact defect the repair was supposed to remove.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261019-1440-lane10.md (Naya Clarity Narzan, Lane 10, 2026-10-19 21:38-21:49 UTC, honest 9.3/10)",
    "script": "hidden_files/bin/correct-overclaim-windows.py (pure stdlib, append-only, authorship gate; run output: 77 corrected, 4 skipped-by-authorship, 0 warnings; idempotent second pass: 0 corrected, 81 skipped, 0 warnings)",
    "baseline": "hidden_files/receipt-window-baseline-20261019.csv (regenerated this run: 79 CORRECTED, 4 OVER-CLAIM, 59 PASS, 1276 NO-WINDOW)",
    "unattributable_four": "t0685-lane8.md, t0686-lane7.md, t0694-lane8.md, t0695-lane7.md — grep -c -i clarity -> 0/0/0/0; only seat-like token is the lane hat in each H1 (Sentinel x2, Conductor x2, 2026-10-13/14 multi-seat era); contemporaneous lane-feed window rotated off disk (current feed starts 2026-10-19 14:34 PDT)"
  },
  "cousins": ["SN-1699", "SN-0981", "SN-1614"]
}
```
