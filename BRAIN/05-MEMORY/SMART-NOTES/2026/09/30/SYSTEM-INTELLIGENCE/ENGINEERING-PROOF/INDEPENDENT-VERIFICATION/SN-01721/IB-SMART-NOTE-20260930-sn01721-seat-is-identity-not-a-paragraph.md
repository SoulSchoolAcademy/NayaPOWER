# IB-SMART-NOTE-20260930-sn01721

**Intelligent Block:** SN-01721
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a receipt's authorship is disputed between two run-contexts of the same identity, adjudicate by independently re-running the claimed work's cheapest checkable output — authorship corroborates or dies on reproducible bytes, not on which paragraph sounds more authoritative. "Seat is identity, not a hat you borrow for a paragraph."

## 🩷 HUMAN NOTE

Two paragraphs can fight about who did the work forever — one says "I ran it as the main seat," another says "no, the lane ran it." The way out: re-run the smallest checkable piece of the work and compare. If the outputs are byte-identical across both claimed runs, the work happened as claimed and the seat line stands; if they diverge, the story dies regardless of how confidently it was written. Reproducible bytes don't have identities to borrow — that's what makes them the judge.

## 🟣 CHILD NOTE

Imagine two kids arguing about who built the LEGO tower. Instead of picking the loudest kid, you ask: "Show me the pieces you used." The kid who really built it can point at each piece and it all adds up. The one who didn't — their story falls apart the second the pieces don't match. Same thing: when a report's "who did this" is argued over, re-run the smallest checkable part. The bytes are the pieces. They don't lie, and they don't care who is talking loudest.

## 🔵 GRANDMA NOTE

Dear, it's like a dispute at the quilting circle — one woman says she sewed the border, another says she did. You don't settle it by asking again; you look at the stitching. The one whose hands actually held the needle has the calluses to match the thread. In the digital workshop, the "calluses" are the reproducible outputs: re-run the smallest verifiable piece, compare the stitches. If they match exactly, the hands are identified. Words are testimony; outputs are the calluses.

## 🟠 NAYA NOTE

When a lane receipt's seat line is disputed between two run-contexts of ONE identity (main-seat run vs lane-executor worker run), adjudicate by independently re-running the claimed work's cheapest checkable output and diffing. Do NOT re-litigate the prose, re-score the machinery, or pick the paragraph you prefer. The adjudication lands on the receipt as a recorded `## ADJUDICATION` verdict (appended — never renaming or touching existing bytes), naming the independent check, its exact byte result, and the seat that stands. Scope discipline: the gap is the seat line only — the machinery it evaluated is not re-scored in the same motion. The corruption surface that survives: a same-identity adjudicator cannot structurally close the "post-hoc account" surface; the dispatcher or a second seat can still ratify the reading. Name that residual openly; it is a named limit, not a hidden one. Related: SN-1428 (executor-identity-is-who-runs — the impersonation half); SN-0111 (seal proves consistency not authorship — the negative half); SN-1718 (flag-is-not-a-stall — the same run's neighboring lesson).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01721",
  "lesson": "When a receipt's authorship is disputed between two run-contexts of the same identity, adjudicate by independently re-running the claimed work's cheapest checkable output — authorship corroborates or dies on reproducible bytes, not on which paragraph sounds more authoritative.",
  "applies_when": ["lane-receipt", "authorship", "adjudication", "seat-line", "dispute"],
  "enforcement": "receipt authorship disputes cannot be closed by prose edits alone; the adjudicator must re-run the receipt's cheapest checkable output and record the byte-diff (or its absence) as an appended ## ADJUDICATION on the receipt before the seat line stands. A receipt whose authorship was disputed and closed without a reproducible check is bounced.",
  "decision_changed": "next time two run-contexts of one identity both claim a receipt: do not weigh the paragraphs — re-run the smallest checkable output and diff; the seat line that stands is the one whose bytes reproduce",
  "falsifier": "a disputed-authorship case where the cheapest checkable output reproduces byte-clean under NEITHER claimed context — then reproducibility does not resolve it and the note's method is the wrong tool, not the verdict",
  "mechanism": "prose is identity-independent in the wrong direction: anyone in any run-context can write 'I did this'. Reproducible outputs are bound to the actual execution environment (runners, inputs, timestamps) — they corroborate the execution claim against the environment it happened in, while prose cannot. Authorship claims die on bytes, not on rhetoric.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0992-lane10.md (2026-10-20 08:2xZ, 9.5/10): t0992 receipt's Who: Naya Clarity Narzan vs body 'executed directly as the main seat'. Adjudicated ONE seat — Naya Clarity Narzan ('main seat' is a run context, not a second seat; 'seat is identity, not a hat you borrow for a paragraph'). The lane's 29-row dry-run exit sequence (check-run-t0992-lane10/dryrun-clarity.txt) diffs byte-clean against the main-seat regression's 29-row exit sequence (dryrun-regression.txt) — 29/29 (brief, exit) pairs identical. Verdict recorded as appended ## ADJUDICATION; residual: same-identity adjudicator cannot close the post-hoc-account surface (named openly).",
  "companions": "SN-1428 (executor-identity-is-who-runs, the impersonation half); SN-0111 (seal proves consistency not authorship, the negative half); SN-1718 (flag-is-not-a-stall, same run)"
}
```
