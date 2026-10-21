# A Merge Watch That Scans Merged PRs Cannot See a Direct Push — the Wave-Closeout Enforcement-vs-Anchor Byte Comparison Is the Backstop Audit

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01760-unlogged-direct-push-surface-backstop-audit
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-21 the director byte-verified a direct push to main (b52c2121d5a6, Oct 19 13:26Z, 17 files, "[Team Verity] dock: land Eta's v2 9.5-flip") that no watch had ever logged. The tick-time merge watch scans closed-pulls for merged_at events — a direct push leaves no PR and no merge event, so it is invisible to that watch by construction. The wave-410 closeout's enforcement-vs-anchor byte comparison (8 enforcement rows vs anchor 895d7361) surfaced it: 7/8 rows identical, row-7 (delivery_evidence_gate.py) differed. Lesson: merge-event surveillance is blind to direct landings; the backstop is a tip/anchor byte comparison at every wave closeout, and any surfaced push joins the ratify-or-route queue.

## 🩷 HUMAN NOTE

Hey Shawn — guess what I discovered: our "MERGE RECEIPT WATCH: CLEAN" can be a lie. A direct push to main doesn't create a PR or a merge event, so a watch that scans merged PRs literally cannot see it. The wave-410 Auditor compared what was *supposed* to be on main (the enforcement map) against what was *actually* there — and found a 2-day-old direct landing nobody had logged. So from now on, every wave closeout ends with that byte comparison: what merged versus what landed. If the two disagree, the surprise push goes to the ratify-or-reroute queue — the same queue as the direct-push alerts — and gets adjudicated. The watch watches merges; the closeout audits the tip. That is why.

## 🟣 CHILD NOTE

Imagine a library where the checkout desk logs every book that is checked out — but someone can also walk in and put a book on the shelf without ever visiting the desk. The desk's log will say "everything is fine" forever, and it will never know about the extra book. The fix: at the end of every day, someone counts the books on the shelves and compares that count to the desk's log. If there are more books than the log says, one arrived through the back door — and it gets checked then.

## 🔵 GRANDMA NOTE

Our watch keeps a careful record of everything that arrives through the normal checkout lane. But things can also arrive by another route that leaves no checkout slip — and the watch has no eyes there. So now, at the end of every big round of work, we compare the actual shelves against the record book, item by item. The day we started doing that, we found something two days old that nobody had recorded. That is the job now: check the shelves, not just the slips.

## 🟠 NAYA NOTE

For every Naya who closes a wave: the merge receipt watch (closed-pulls scan, merged_at in window) reports CLEAN only for the merge lane. Before sign-out, run the enforcement-vs-anchor byte comparison: the current enforcement map (each row pinned to the anchor tip the wave started from) against the live main tip. Any file that differs without a merged PR behind it is an UNLOGGED-DIRECT-PUSH-SURFACE event: byte-verify the landing commit on main (committer, timestamp, single/multi-parent, file count), log it in the wave closeout, and route it to the main-seat ratify-or-route adjudication (it joins the SN-1737 direct-push queue). Never read MERGE RECEIPT WATCH: CLEAN as "nothing landed on main."

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn01760-unlogged-direct-push-surface-backstop-audit",
  "title": "A merge watch that scans merged PRs cannot see a direct push — the wave-closeout enforcement-vs-anchor byte comparison is the backstop audit",
  "lesson": "A tick-time merge watch that scans closed-pulls for merged_at events is structurally blind to direct pushes to main: a direct push creates no PR and no merge event. The backstop is a byte comparison at every wave closeout: the enforcement map (rows pinned to the wave's anchor tip) against the live main tip. 2026-10-21: Auditor wave-410 closeout compared enforcement vs anchor 895d7361 — 8/8 rows identical EXCEPT row-7 (kernel/protocol/checks/delivery_evidence_gate.py 5bddfda2->a499ddcc) via direct push b52c2121d5a6 '[Team Verity] dock: land Eta's v2 9.5-flip at tip 1a1c22d3' (Oct 19 13:26Z, committer Naya Verity Narzan, single-parent, 17 files). Not a new push in-window; no watch record had ever logged it. Distinct from SN-1737 (alert fatigue on repeatedly-fired alerts): this is surveillance-surface coverage — the alert never fired at all.",
  "applies_when": [["watch", "merge-receipt-watch"], ["push", "direct-to-main"]],
  "enforcement": "Every wave closeout runs the enforcement-vs-anchor byte comparison (each enforcement row pinned to the wave's anchor tip vs the live main tip) before sign-out. Any file differing without a merged PR behind it is an UNLOGGED-DIRECT-PUSH-SURFACE event: byte-verify the landing commit (committer, timestamp, parent count, file count), log it in the closeout, and route it to the main-seat ratify-or-route adjudication. The tick watch may never report CLEAN as 'nothing landed on main'.",
  "evidence": ["live-plan.md DIRECTOR TICK 2026-10-21 03:38 PDT (10:38Z): previously-unlogged direct push b52c2121d5a6 SURFACED on main, director byte-verified on-main (Oct 19 13:26Z, committer Naya Verity Narzan, single-parent, 17 files); named failure mode UNLOGGED-DIRECT-PUSH-SURFACE; joins ratify-or-route owed", "wave-410 Auditor enforcement comparison vs anchor 895d7361 (8/8 byte-identical EXCEPT row-7: delivery_evidence_gate.py 5bddfda2->a499ddcc)", "memory/2026-10-21.md line ~1018 (director surfacing record)", "follow-on 11:08Z tick: night-shift-wire claimed the row-7 enforcement-significance verdict on delivery_evidence_gate.py @ ef8af6f5 (#2793 comment 6314296824) — the backstop already driving verification work"],
  "decision_change": "The next wave closeout deciding whether main is clean: it cannot accept 'MERGE RECEIPT WATCH: CLEAN' as sufficient — it must run the enforcement-vs-anchor byte comparison, because any direct landing in-window is invisible to the tick watch. A cold Naya inheriting this system would otherwise certify a dirty tip clean forever.",
  "falsifiability": "If the tick-time merge watch had ever logged b52c2121, the premise is falsified: the surveillance surface covered direct pushes and no backstop was needed. Corroboration: the 11:08Z row-7 enforcement-significance claim (wire lane, #2793 6314296824) independently anchors the surface finding to live bytes @ ef8af6f5.",
  "mechanism": "Direct pushes to main bypass PR/merge-based surveillance by construction — there is no PR object and no merged_at event to scan. Only a direct byte comparison of main's content (tip diff against a known anchor) observes them. Closed-pulls surveillance and tip content are two different observation surfaces; the watch that scans one cannot certify the other.",
  "captured_date": "2026-10-21",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/WATCHER-INTEGRITY"
}
```
