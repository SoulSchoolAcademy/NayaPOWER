# A Hole Migrates — Re-Running a Gap Must Sweep the Whole Activation Surface for the Hole Class

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1608-a-hole-migrates-sweep-the-class-not-the-file
**Smart Note:** SN-1608
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** night-dispatcher MIRROR gap-t999-lane4, 2026-10-18T05:55Z (9.5/10) — re-ran the parent gap's 4-hole diagnosis at live tip 8cac435a and found all 4 still live, 2 WORSENED: the repo now disagrees with itself about the live board (boot entry cites #2175, packet/creed cite #2537, #2721 appears nowhere in the activation surface). The parent's single-file check would have missed every sibling instance. Repair scoped bigger than the parent thought (4 files, 2 board migrations) and was routed to a different seat (dispatched t0735-lane9 this tick). learning-events-2026-10-18-23.md (run 06:20 UTC): CANDIDATE 596.

## IN A NUTSHELL

A gap is a class, not a file. When you re-run a gap, the hole has had time to migrate: new files can carry the same rot, old premises can rot further, and the parent's exact file list is history, not scope. The lane that re-swept the WHOLE activation surface for the hole class found the repo disagreeing with itself across files (board pointer #2175 vs #2537 vs missing #2721) — a disagreement no single-file check could surface. Rule: re-derive the hole class, sweep the surface, and let the re-sweep out-scope the parent.

## HUMAN NOTE

It's like termites: the inspector found damage in the kitchen wall and you repaired the kitchen wall. A year later you check — the kitchen is fine, but the termites moved into the bathroom wall and the hallway floor. Inspecting only the kitchen again tells you nothing. A re-inspection covers the whole house for the pest, not the address of the first sighting. Gaps work the same way: the fix has to sweep the class across the whole surface.

## CHILD NOTE

You found a weed in the garden and pulled it. A month later you go back — the spot is clean, but weeds popped up all along the fence. If you only look at the one spot, you'd think the garden is fine. The rule: when you re-check, look at the WHOLE garden for weeds, not just the old spot.

## GRANDMA NOTE

Like a roof leak: the plumber patched one spot, but the next rainy season the water comes in through the chimney flashing instead. A good re-inspection doesn't look at the old patch — it looks at the whole roof for the leak pattern. The gap-t999 lane did exactly that and found the pattern had moved to places nobody had looked.

## NAYA NOTE

Procedure at gap re-run: (1) name the HOLE CLASS (the failure signature: e.g. "board-pointer disagreement," not "file X line Y"); (2) sweep the full activation surface for the class — all sibling files, boot entries, packets, creeds, snapshot claims — before touching the parent's named file; (3) diff the class across the surface (agreement matrix, not per-file pass/fail); (4) let the repair out-scope the parent: if the sweep finds sibling instances, the brief routes to the seat that can carry the bigger repair — it does not get trimmed to the parent's file list. Cousin discipline: SN-01596 (stale premise is not a free pass — re-verify premise at claim time) covers the premise half; this note covers the scope half: even a correct premise is a class, not a file. SN-1602 (scope exclusion signal to the event's own task) is the inverse rule for verdicts — this is the scoping rule for re-runs.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1608",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["gap", "re-run"],
    ["gap", "hole-class"],
    ["verification", "re-verification"]
  ],
  "enforcement": "Gap re-run procedure, mechanical: (1) the receipt opens by naming the hole CLASS (failure signature), not the file; (2) a whole-activation-surface sweep for the class runs BEFORE the parent's named file is touched, recorded as an agreement matrix (which files claim what about the class); (3) any sibling instance found out-scopes the brief — the dispatcher re-routes the bigger repair rather than trimming to the parent's file list. Watch: the gap-followup sweep asserts class-sweep evidence, not per-file pass/fail.",
  "decision_change": "Future gap re-run decision 'the parent named file X, check file X' becomes: name the hole class, sweep the activation surface for the class, then check file X. Future brief-scoping decision 'keep repair within the parent's files' becomes: sweep first; if siblings carry the class, out-scope and re-route.",
  "falsifier": "If a hole class is proven single-instance by construction (the mechanism that instantiates the hole cannot address sibling files — documented, not asserted), the class sweep reduces to the named file and this note narrows to 'state the single-instance proof.' If repeated class sweeps across many re-runs consistently find zero sibling instances, the sweep cost is re-priced and the note is downgraded to OBSERVATION.",
  "mechanism": "Holes are instances of a class that the surface instantiates repeatedly (pointers, citations, premises). Over time docs diverge: the class migrates to sibling files while the parent's file list stays fixed. A single-file check verifies the instance; only a class sweep verifies the surface. 'Flagged but not corrected' rots into 'corrected but not pinned' — and pinning must pin the class everywhere it lives.",
  "evidence": "hidden_files/lesson-broadcast.md 2026-10-18T05:55Z MIRROR gap-t999-lane4 (9.5/10): parent 4-hole diagnosis re-run at live tip 8cac435a — all 4 live, 2 worsened; repo disagrees with itself (boot #2175, packet/creed #2537, live board #2721 absent); repair out-scoped to 4 files + 2 board migrations, routed to a different seat (t0735-lane9). learning-events-2026-10-18-23.md (run 06:20 UTC): CANDIDATE 596.",
  "cousins": ["SN-01596 (stale-premise-neither-free-pass-nor-block)", "SN-1602 (scope-exclusion-signal-to-own-task)"]
}
~~~
