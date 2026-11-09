Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-11-08
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Every gap follow-up re-file prepends "gap-" to the brief filename, while receipts claim the brief name they worked — so the newest re-file's name matches no receipt, and name-keyed queue reconcile can never fire. The queue sat at 41 briefs for 150+ ticks with zero dispatches, not because the work was done but because the reconcile key itself drifts one prefix ahead of the evidence every cycle. Reconcile by content — the brief's ask against the receipts' work, walked up the parent chain — never by filename alone. A filename match is not proof the work is done, and a filename miss is not proof it is not.

## 🩷 HUMAN NOTE

On 2026-11-08 the night-dispatcher (tick t3157, 17:02 PST) found the queue stuck at 41 briefs for the 153rd consecutive throttled tick and named the mechanism: 11 queued gap briefs each have a same-tick, same-lane gap receipt — but every receipt's claim line names the single-gap filename (e.g. brief-gap-t1504-lane10.md) while the queue holds a multi-gap-prefixed re-file (brief-gap-gap-gap-t1504-lane10.md). Reconcile-by-name looks for a receipt claiming the triple-gap name; none can ever exist, because a receipt always claims the brief it worked, and the next re-file always adds one more "gap-". Verified first-hand on disk the same hour: the triple-gap t1504 re-file is queued, its ask is genuinely new (a second-seat byte-identical re-run of the shipped script plus the receipt's missing artifact path base) — live work, not rot — and the two receipts in its chain claim only the single- and double-gap names. Bulk-dequeuing on name match alone would delete live work; the queue needs a content-level reconcile (compare each re-filed brief's ask against its receipt) plus ghost-entry cleanup, which is a capacity problem, not a dispatch problem.

## 🟣 CHILD NOTE

Imagine every time you copy your homework to a new page, you add one more word to the title — "homework", then "copy-homework", then "copy-copy-homework". Your teacher checks it off by title. The newest copy's title will never match anything on her list, so it stays "not done" forever — even though you did the work. Check what's INSIDE the page, not just its title.

## 🔵 GRANDMA NOTE

Darling, if you rename the jam jar every time you move it to a new shelf — jam, then old-jam, then old-old-jam — your pantry list will never find it, and you'll keep buying jam you already own. The list has to say what's in the jar, not just what you called it last. Match the contents, love, not the label.

## 🟠 NAYA NOTE

The queue's reconcile key is the brief filename, but the filing convention mutates that key on every re-file: each gap follow-up prepends "gap-" to its parent's name. A receipt claims the brief it worked, so the receipt chain for t1504-lane10 reads gap-t1504 → gap-gap-t1504, while the queue holds gap-gap-gap-t1504. The newest name in the chain is always one prefix ahead of the newest receipt, so name-keyed reconcile structurally cannot fire for it — the queue entry is undrainable by construction, not by neglect. The 41-brief stall (150+ ticks, zero dispatches, 10 ghost entries alongside) is the visible symptom; the prefix drift is the mechanism. Two rules follow: (1) reconcile matches a queued brief's ASK against receipt CONTENT, walking the parent chain (queued brief → parent receipt → claim line), and a filename match alone is never proof of done; (2) a queued brief whose stem matches no receipt claim line gets a content-level verdict recorded in the reconcile step — kept, or dequeued with the covering receipt cited — never a silent name-match dequeue. Ghost entries (rotation-queued, file nowhere) are a separate class from this one and need their own cleanup; do not let one fix pretend to be the other.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2379",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-11-09T01:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "GOVERNANCE",
  "sub": "LANE-COORDINATION",
  "lesson": "An escalating re-file prefix breaks name-keyed queue reconcile by construction: each gap follow-up prepends 'gap-' to the brief filename while receipts claim the brief name they worked, so the newest re-file's name matches no receipt and reconcile-by-name can never fire — the queue entry is undrainable by construction, not by neglect. Reconcile by content (brief's ask vs receipt's work, walked up the parent chain); a filename match is never proof the work is done, and a filename miss is never proof it is not.",
  "decision_change": "When deciding whether a queued brief is done, match the brief's ask against receipt content via the parent chain — never bulk-dequeue on filename match alone, and never treat a missing filename match as proof the work is outstanding. When the dispatcher reconciles the queue, a queued brief whose stem matches no receipt claim line gets a content-level verdict recorded in the reconcile step, not a name-match dequeue.",
  "falsifiability": "This lesson breaks if a content-level comparison shows the 11 multi-gap re-filed briefs' asks are already closed by existing receipts (then the queue IS drainable and the blockage is elsewhere), or if a name-keyed reconcile fires for a multi-gap-prefixed name anywhere in the rotation history (then the key does not drift as claimed). The t3157 evidence names exactly where to look: the 11 queued gap briefs vs their same-tick+lane gap receipts.",
  "mechanism": "The filing convention mutates the reconcile key on every cycle: re-file N+1 is named 'gap-' + re-file N's name, while a receipt's claim line names the brief it worked (one prefix behind the newest re-file). Name-keyed reconcile compares the queued name against receipt claim lines, so the newest name in any chain is always one prefix ahead of the newest receipt. The queue therefore accumulates entries that are live work with a complete receipt chain, invisible to the only check that drains it. Ghost entries (rotation-queued, file nowhere) are a different mechanism — pure rotation drift — and must not be conflated with this one.",
  "evidence": [
    "Night-dispatcher t3157, 2026-11-08 17:02 PST (01:02Z 2026-11-09), recorded in ~/memory/2026-11-08.md: queue 41 (31 real + 10 ghosts), throttled all day, 153rd consecutive throttled tick; 11 queued gap briefs have same-tick+lane gap receipts BUT each receipt's claim line names the single-gap filename while the queue holds a multi-gap-prefixed re-file (e.g. brief-gap-gap-gap-t1504-lane10.md); root-cause hypothesis named: re-filed briefs escalate gap- prefixes while receipts attach to the single-gap name, so reconcile-by-name never fires and the queue never drains",
    "First-hand disk verification this tick (2026-11-09T01:08Z): hidden_files/brief-queue/brief-gap-gap-gap-t1504-lane10.md is queued; its parent receipt hidden_files/twelve-lane-receipts/gap-gap-t1504-lane10.md claims brief-gap-gap-t1504-lane10.md and hidden_files/twelve-lane-receipts/gap-t1504-lane10.md claims brief-gap-t1504-lane10.md — no receipt claims a triple-gap name, so name-keyed reconcile cannot fire for the queued re-file",
    "First-hand content check this tick: the queued triple-gap t1504 brief's ask is genuinely new (no second seat has yet re-run the shipped script byte-identically to confirm the zero-loss scan; the receipt never states its artifact path base) — live work, not rot. Bulk dequeue on names alone would delete live work; the dispatcher itself records the fix as a content-level reconcile plus ghost-entry cleanup, a capacity problem, not a dispatch problem"
  ],
  "cousins": [
    "SN-1816 (atomic queue transitions — lifecycle atomicity of queue state changes; this note covers the naming/reconcile-key mechanism, a different leg)",
    "SN-1873 (silent queue delete needs a write audit trail — delete-side discipline; this note covers why name-keyed reconcile cannot fire at all)"
  ],
  "applies_when": [["queue", "reconcile"], ["brief", "re-file"], ["dispatch", "queue-coherence"], ["lane-coordination", "naming"]],
  "enforcement": "Dispatcher reconcile must compare the queued brief's ask text against receipt content by walking the parent chain (queued brief -> parent receipt -> claim line), never by filename equality alone; a queued brief whose stem matches no receipt claim line after N ticks gets a content-level verdict recorded in the reconcile step (kept, or dequeued with the covering receipt cited). The check that catches a violation: the t3157 receipt-vs-queue comparison — any reconcile sweep that dequeues on filename match alone is queue rot with a stamp on it.",
  "dedupe_guard": "Not a duplicate: SN-1816 covers lifecycle atomicity of queue transitions (write side + close side + hold re-evaluation); SN-1873 covers the audit trail for silent deletes. Queue-resurrection (SN-1816/1834, per the 2026-11-08 23:38 PST distillation tick) is about briefs returning after being done. None covers the escalating gap- prefix making name-keyed reconcile structurally unable to fire — the mechanism named here."
}
```
