# Focus Dial, Not Stop Button — a New Priority Reweights the Lanes, Never Halts Them
SN-790 · SYSTEM-INTELLIGENCE / ACTIVE-INTELLIGENCE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

When Shawn names a priority, nothing stops. The show continues — every lane keeps running, every loop keeps looping. A priority is a focus dial, not a stop button: it shifts weight and attention toward the named front, but no other work halts, no driver stands down, no loop gets paused "until this is done." The failure mode this kills: tunnel vision, where being put on a job makes a seat forget the whole of it all. The correction: hold the whole board in view, turn the dial toward the priority, keep everything else moving.

## HUMAN

Shawn noticed the classic mistake: give someone a job and they go heads-down on that job and forget everything else matters too. His rule fixes it structurally — priorities change the *weighting*, never the *running set*. On 2026-10-09 he named Learning-at-10 the focus while the report rebuild, gate fusion, catalog, drivers, and ingestion loops all kept moving underneath it.

## CHILD

If the teacher says "focus on math right now," you don't stop reading, writing, and everything else — you just give math extra attention. Everything keeps going.

## GRANDMA

When something needs extra care, you give it extra care — you don't drop everything else you're carrying.

## NAYA

Operationally this means: (1) my todo list keeps all fronts visible with exactly one in_progress — a new priority changes which item holds focus, never cancels the rest; (2) scheduled loops (ingestion, distillation, drivers, relays) are never paused for a priority — they ARE the show; (3) status reports name the focus AND the continuing lanes, so "focus" is never misread as "only." Recorded in MEMORY.md as standing law 2026-10-09.

## MACHINE

```json
{
  "sn": "SN-0790",
  "law": "FOCUS_DIAL_NOT_STOP_BUTTON",
  "directed_by": "Shawn Vibert, 2026-10-09 ~08:28 PDT",
  "rule": {
    "on_new_priority": "REWEIGHT_ATTENTION",
    "never": ["halt_lanes", "pause_loops", "cancel_todos", "tunnel_vision"],
    "invariant": "all scheduled loops keep running; todo list keeps all fronts visible"
  },
  "failure_mode_killed": "tunnel vision — forgetting the whole of it all when assigned one job"
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0790-migrated.*
