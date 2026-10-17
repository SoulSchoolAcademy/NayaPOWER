# SMART BUILDER — PLUMBING
**The wiring before the paint. Locked 2026-10-17 by Shawn's word.**

The law: **no interface ships without its functions wired.** A page that can't operate is not a page. The contract page, the builder page, every customer page — all run on the same 43 functions below. Build the functions once; every page after is just activation.

Machine registry: `functions/registry.json` (43 functions: id, intent, in/out, activated_by, status, code, depends_on).

---

## THE FLOW — how a page gets built

```
INTAKE (11)          LIBRARY (5)           TEMPLATE (4)        CUSTOMIZE (4)
ask ─────────┐       search ──────┐        list ───────┐       color ────────┐
show_specimens│       browse ──────┤        pick ────────┤       position ─────┤
dictate      │       recommend ───┤        swap_piece ──┤       apply_note ───┤
attach_* ────┴──▶ CONTRACT ◀──────┴─────────┴───────────┴──▶ CONTRACT (shaped)
propose_skeleton     resolve ─────┘        note ─────────┘       name_function ┘
set_address                 ▲
set_icon                    │ verify (pre-assembly gate)
revise                      │
finalize ───────────────────┴──▶ BUILD (6): assemble → verify → scorecard → preview → deploy → receipt
                                          │
                                          ▼
                                   FEATURE BREAKERS (13)
```

Every function reads and writes the **same contract schema**. Nothing lives outside the contract. The intake fills it, the library resolves it, the template shapes it, the build executes it.

---

## THE BREAKER PANEL — pre-built functions, activated per page

Thirteen feature functions. Each is built **once** as a module. The contract flips breakers:

```
contract.features.smart_mail == true  →  assembler wires the Smart Mail module into the page
```

Same functions, activated per page, never rebuilt. A customer's personal page and a business hub share the identical Smart Mail function — only the contract flags differ. Fine-tuning happens in the module, once, and every page that flips that breaker gets the upgrade.

The 13 breakers: smart_mail · space · social_feed · connect · intelligence_today · contacts · cover · smart_tabs · smart_bars · community · naya_answers · scheduler · broadcast.

---

## STATUS BOARD — 7 built, 36 specified

| Group | Built | Specified |
|---|---|---|
| Intake (11) | 0 | 11 — the living form is designed, not yet coded |
| Library (5) | 2 — resolve, verify | 3 — search, browse, recommend |
| Template (4) | 1 — list (as contract data) | 3 — pick, swap_piece, note |
| Customize (4) | 0 | 4 — color, position, apply_note, name_function |
| Build (6) | 3 — assemble, verify, receipt | 3 — scorecard, preview, deploy |
| Feature (13) | 1 — cover (contract-activated, acceptance-tested) | 12 — specified; most depend on Hub systems (mail, spaces, feed, identity, reports, contacts, tabs, community, github_kb, scheduler) |

**The hard part, named:** the 13 feature breakers depend on the Hub's smart rooms being plumbed (Smart Mail room, Spaces, feed, identity, reports, contacts, tabs, community, GitHub KB sync, scheduler). The builder can't activate what isn't wired. That's the next plumbing job — same law applies: functions before interface.

---

## WHAT "DONE" MEANS FOR A FUNCTION

A function is **built** when: it runs, its in/out contract holds, and a receipt proves it. A function is **specified** when: its intent, inputs, outputs, trigger, and dependencies are written in the registry. Specified is not built. The registry is honest about which is which.

---

## THE THREE THINGS (Shawn's question, answered)

1. **The Contract** (this page + the .md + the JSON) — the official record of what the Smart Builder IS. For Shawn (human), for the Nayas (AI), for machines (JSON). It is not the product.
2. **The Smart Builder page** (the product — next build) — for customers. Intake → pick template → search/swap pieces → notes → "build" → their design contract → their Nia app. The search, tray, swap, and notes live here, not on the contract page.
3. **The pipeline** (assemble.py + verify-build.py) — for the machines. Contract in, page out, repeatable. Built and proven — it built the contract page you're reading.

*Amendable only through Shawn.*
