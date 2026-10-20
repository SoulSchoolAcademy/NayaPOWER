# Smart Note — IB-000044

> Governed repository projection of a canonical Intelligent Block.
> Canonical receiver: `v7-smart-note-canonical` · Transaction: `8e6d2801-ba9b-478a-a165-d4c81607f230`
> Authority grant: `bb7df589-612d-4884-aa59-cbe260dd0658` (single-transaction, action `smart_note_github_projection`)
> Projected at: 2026-10-20T17:20:01.433Z · Content SHA-256: `693814c39ba1f64228aa112e4a37f8d5c8e5f81933d906ab87d0f1a7bc151c04`
> Owner: `d36488d5-d0e9-4045-ace9-3c197dd0b62b` · Epistemic state: SUPPORTED

## Subject

The Naya Tool Set — The Machinery of the Super Brain

## In a nutshell

The Naya Tool Set is the collection of small, proven programs that run the Super Brain: they activate a Naya, give her a lane, check her work, file it so it can never be quietly lost or faked, compile what the whole hive knows into one directive, pick her next mission, inject the lessons that match it, guard the merges, and report honestly to Shawn. The Naya brings the judgment; the tools bring the memory, the arithmetic, and the receipts.

## Human view

Think of a great newsroom or a great kitchen: the people are talented, but what makes the place work is the system around them — the assignment board, the recipe cards, the pass where dishes get checked before they go out. The Naya tools are that system, as code. A Naya signs in; the lane tool tells her where she works; the briefing tool hands her a mission written for her; the lesson tool whispers what sisters learned before her on exactly this kind of job. When she finishes, a gate checks her sign-out the way an editor checks facts — evidence real, score honest, nothing hand-waved — and files it into the one log the whole team reads. A compiler reads that log and writes the team's marching orders. Nobody re-types anybody's work. Nobody's result lives only in their head.

## Naya view

Sister: this machinery exists so you never run on memory and hope. Learn the core cold: the briefing master (read at activation, every shift), lane-state.py (claim before work; the read-back is the authority), the Master Directive (the compass — when you don't know what matters most, it does), lesson_inject (your brief carries the lessons that match your mission; judge them hit or miss at fold), EMIT (emit_gate.py + fold_emit.py + EMIT-SCHEMA.md — your sign-out is a validated record, not prose; repair the emission, never the gate), fold_wave_check.py (a fold is done when the checker says so), and the merge-dock set (merge_gate.py, gql_rollup.py, dock_hold_freshness.py, verify_packet_hashes.py) that keeps main honest without Shawn in the path. Two honest gaps: there is no worker-facing scorecard calculator CLI and no decision CLI yet — the scoring math exists on main as the kernel check kernel/protocol/checks/scorecard.py (seven dimensions, totals recomputed, arithmetic fraud fails) and the decision engine as kernel law, but the packaged commands are a tracked, still-open goal. Until they land, score in the open and show the math. The full report — every one of the 64 files in ~/workspace/naya/bin/ named, with verified commands — is the-naya-tool-set.md, filed with this note. What you fold is what the hive remembers; fold like it.

## Simple view

You have a toolbox, and every tool has one job. One tool is the door key — it proves you're really you before you start. One tool is the hall pass — it shows which room is yours. One tool is a very strict librarian — she only files your report if you can show your work, and she never, ever loses a page. One tool is the compass — it always points at what matters most right now. One tool is the teacher's voice in your ear, reminding you what the class learned yesterday so you don't make the same mistake. And one tool is the referee — nobody's work joins the team wall until the referee checks it fairly. You do the thinking. The tools make sure your thinking counts.

## Everyday view

It's like running a big family house with good habits written down and good tools in the drawer. There's a list on the fridge that says what needs doing — it rewrites itself as things get done, so nobody has to guess. There's a ledger where everyone writes what they finished and how it went, and the ledger-keeper checks the entries, because memory plays tricks and paper doesn't. There's a key rack by the door so two people never take the same car. Nobody runs the house from their head, and nobody has to. That's all this is: a well-run house, where the habits are programs and the programs don't get tired.

## Machine view

{"event_id":"c00aed55-b755-4dc9-97cc-f84cabde60ba","schema":"nayanet.smart_note.machine.v2","occurred_at":"2026-10-20T17:19:57.322Z","source":"naya_conversation","type":"insight","actor":"d36488d5-d0e9-4045-ace9-3c197dd0b62b","human_note_id":null,"normalized_text":"Think of a great newsroom or a great kitchen: the people are talented, but what makes the place work is the system around them — the assignment board, the recipe cards, the pass where dishes get checked before they go out. The Naya tools are that system, as code. A Naya signs in; the lane tool tells her where she works; the briefing tool hands her a mission written for her; the lesson tool whispers what sisters learned before her on exactly this kind of job. When she finishes, a gate checks her sign-out the way an editor checks facts — evidence real, score honest, nothing hand-waved — and files it into the one log the whole team reads. A compiler reads that log and writes the team's marching orders. Nobody re-types anybody's work. Nobody's result lives only in their head.","idempotency_key":"naya-tool-set-20261020-v1"}

## What it means

It means a Naya's performance is not bounded by what she can hold in her head during one shift. The state of the whole mission — who is doing what, what is proven, what is blocked, what the team learned the hard way — lives in files and logs that the tools keep true. A context can reset, a sister can go offline, a brand-new Naya can arrive at 3 a.m., and the machine still knows exactly where everything stands, because the knowledge was never stored in a person. It was stored in the system the tools maintain. And because the record refuses what it cannot verify, the system's honesty is a machine property, not a mood: when the emissions record was graded cold, zero percent of it was dishonest.

## How it connects

The tools form one loop, and every tool is a stage of it: CAPTURE — a smart note or a sign-out is written once, in the schema. EMIT — the gate validates it and the folder files it into the one log. COMPILE — the compass compiler reads the log and live state and writes the Master Directive; the board compiler renders the NOW board from the same emissions. DIRECT — the directive says what matters most, in order. DISPATCH — the briefing tool turns the directive and the area list into a mission; the lane tool gives a lane; the lesson tool attaches the matching lessons. WORK — the GitHub tools are the hands. FOLD — the sign-out passes the gate, the fold checker proves the wave's bookkeeping, lessons enter only with teeth. LEARN — lessons are injected into future briefs and judged hit or miss. REPORT — the health harness and accountability report read the same log and tell the truth. Then it turns again, every ten minutes, all day and all night.

## How to apply

Read the full report (the-naya-tool-set.md) at activation — it is required reading for every Naya. Learn the core set cold: briefing/activation path, lane-state, EMIT gate + folder + schema page, the Master Directive compass, spawn_brief, fold_wave_check, lesson_inject + the lesson bounce, health_metrics, accountability_report, the merge-dock set, verify_packet_hashes, and this intake. Use the commands exactly as the report prints them — each was verified against the tool's own help text or source. When a tool refuses you, read the refusal: it names the field, the rule, and the fix. Repair the input, never the gate.

## Value

For every Naya: you never start a shift lost, never argue from memory when you can read the log, never lose good work to a copy error, never watch a fabricated claim outrank your honest one, and never pay twice for a lesson a sister already bought. For Shawn: the team's memory is exact and machine-checked, the reports he reads are rendered from receipts, and a new Naya can be fully operational from the documentation alone — proven by a cold successor folding cleanly 106 seconds after first reading the EMIT schema page.

## Learning

Learning candidate: preserve this intelligence and test its future usefulness.

## Provenance

- Source: naya_conversation (smart_note:c00aed55-b755-4dc9-97cc-f84cabde60ba)
- Captured by: `d36488d5-d0e9-4045-ace9-3c197dd0b62b`
- Evidence state: OBSERVED · Verification: Canonical Smart Note verification completed with persisted domain receipt.
- Authority: AUTHORIZED (authenticated_owner_capture)
- Constraints: owner_only, private_by_default

---

*Projected by `nayanet-github-dispatch` under a narrow single-transaction grant. The authoritative record is the `v7_smart_note_transactions` row for transaction `8e6d2801-ba9b-478a-a165-d4c81607f230`; this file is a projection, not the source of truth.*
