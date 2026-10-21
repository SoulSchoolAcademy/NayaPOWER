# IB-SMART-NOTE — SN-0588 — Saved Is Not Captured: the Receipt Completes the Chain

Intelligent Block: IB-SMART-NOTE-20260930-sn0588-saved-is-not-captured-receipt-completes-the-chain
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-07
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
PR #1775's capture-chain repair exposed the failure class that matters most: notes were being SAVED while their proof-of-capture never went through — silent failures in the source-event lookup, the checkpoint verification, and the dispatch-transaction RLS path. The note existed; the capture did not. The chain is now save → verify → receipt, deployed live on both Supabase edge functions (v7-smart-note-canonical v18, nayanet-github-dispatch v34), and the standing lesson is the receipt rule: a write without a receipt is not a completed write — the capture loop closes only when the receipt lands, and silent receipt failures must be instrumented as failures, not discovered by accident.

## HUMAN NOTE
Shawn, this is the one that unblocked the whole capture path: before the #1775 repair went live tonight, Smart Notes were saving fine — but the proof-of-capture step was failing silently, so the notes existed in the database without ever completing their capture. Save ≠ captured. Naya 4 traced it to three silent breakages: the source-event lookup from smart_note_events, the checkpoint verification against nayanet_cognition_events, and a permissions repair on the dispatch-transaction lookup (fixed with a service-role client plus an explicit ownership check, so authority was NOT widened to fix it). She deployed the fix to both production edge functions via the Management API — v7-smart-note-canonical v17→v18 and nayanet-github-dispatch v33→v34, both confirmed ACTIVE with JWT verification intact — and cleaned up two stray duplicate functions left over from the endpoint discovery, so no orphans remain. The full chain is now live: save → verify → receipt. The rule going forward: the loop doesn't close at the write — it closes at the receipt — and any step that can fail silently must be instrumented to fail LOUDLY.

## CHILD NOTE
Writing your homework and putting it in your backpack isn't enough — you have to actually hand it in to the teacher! If the teacher's hand isn't there to take it, putting it in your bag doesn't count.

## GRANDMA NOTE
Honey, mailing the birthday card means nothing if it never leaves the mailbox — you need to see the flag go up. From now on, nothing counts as sent until there's proof it arrived.

## NAYA NOTE
This is the receipt-closure law for every capture/write pipeline from here on: (1) a write's completion is the RECEIPT, never the save — instrument the receipt path with the same rigor as the write path; (2) the dangerous failure class is the SILENT one — a receipt step that can fail without surfacing must be treated as a defect, not a risk, and fixed before any scale (here: source-event lookup + checkpoint verification + dispatch RLS); (3) repair authority, never widen it — the RLS fix used a service-role client WITH an explicit ownership check, keeping the authority envelope identical while restoring function; (4) clean up the discovery debris — the two stray duplicate functions created during endpoint discovery were removed, leaving no orphans. Naya 5's team is now unblocked: DB side confirmed (34 candidates, 99 active) plus live functions = capture path fully operational. The P0 pressure this enables: the promotion loop on the 10 frozen CANDIDATEs (grant 57d83ce5, expires 2026-10-14), independent verification of #1786–#1789, cold-retrieve #1665.

## MACHINE NOTE
{
  "smart_note_id": "SN-0588",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn0588-saved-is-not-captured-receipt-completes-the-chain",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM_INTELLIGENCE",
  "topic": "COMPOUNDING_INTELLIGENCE",
  "subtopic": "CAPTURE_RETAIN_SIMPLIFY",
  "captured_at": "2026-10-07",
  "rule": "saved_is_not_captured_receipt_completes_the_chain_silent_receipt_failures_are_defects",
  "procedure": ["instrument the receipt path as rigorously as the write path", "treat any silently-failing receipt step as a defect", "repair authority without widening it (explicit ownership check)", "remove discovery-debris duplicates (no orphans)"],
  "related": ["SN-0513 (note first, enforce next)", "SN-0584 (Smart-Link SLA nightly receipt audit closes the capture loop)"],
  "evidence": ["#1354 comment 6049012444 (NAYA 4 capture-chain deploy sign-out, 2026-10-07T23:35:52Z)", "#1354 comment 6049019768 (NAYA 5 confirmation, v18/v34 ACTIVE, team unblocked)", "PR #1775 (capture-chain repair, merged)"]
}
