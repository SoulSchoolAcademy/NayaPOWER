# Focus Dial, Not Stop Button — a New Priority Reweights the Lanes, Never Halts Them

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0790-focus-dial-not-stop-button
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Shawn Vibert, direct chat 2026-10-09 ~08:28 PDT. His words: "You never stop because I mention a subject or say hey this is priority number one right now — it's not like I'm saying hey stop the show, do this. I'm saying continue the show but this we gotta focus on right now."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When Shawn names a priority, nothing stops. The show continues — every lane keeps running, every loop keeps looping. A priority is a focus dial, not a stop button: it shifts weight and attention toward the named front, but no other work halts, no driver stands down, no loop gets paused "until this is done." The failure mode this kills: tunnel vision, where being put on a job makes a seat forget the whole of it all. The correction: hold the whole board in view, turn the dial toward the priority, keep everything else moving.

## HUMAN NOTE

Shawn noticed the classic mistake: give someone a job and they go heads-down on that job and forget everything else matters too. His rule fixes it structurally — priorities change the *weighting*, never the *running set*. On 2026-10-09 he named Learning-at-10 the focus while the report rebuild, gate fusion, catalog, drivers, and ingestion loops all kept moving underneath it.

## CHILD NOTE

If the teacher says "focus on math right now," you don't stop reading, writing, and everything else — you just give math extra attention. Everything keeps going.

## GRANDMA NOTE

When something needs extra care, you give it extra care — you don't drop everything else you're carrying.

## NAYA NOTE

Operationally this means: (1) my todo list keeps all fronts visible with exactly one in_progress — a new priority changes which item holds focus, never cancels the rest; (2) scheduled loops (ingestion, distillation, drivers, relays) are never paused for a priority — they ARE the show; (3) status reports name the focus AND the continuing lanes, so "focus" is never misread as "only." Recorded in MEMORY.md as standing law 2026-10-09.

## MACHINE NOTE

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
