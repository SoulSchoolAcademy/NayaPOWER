# SUPER NOTE — Live Bytes Beat Every Story

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-003` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-003` |
| Human title | Live Bytes Beat Every Story |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 16 raw notes (full list below) |
| Cluster file | `cluster-01-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

Every report, ledger, and summary is just a story about the world — and stories go stale. When a story and the living system disagree, go and look at the system itself, right now, and believe your eyes. And before you blame the alarm, check that your own measuring tool isn't the broken part.

---

## 🩷 HUMAN NOTE

Teams drown in secondhand truth: a ledger says a change was applied, a summary says a problem is fixed, a screenshot says everything matches. Again and again the live system told a different story — a table the ledger swore existed was gone; a contamination report described workers the director had already deleted. The discipline is simple: claims about current state expire fast, so re-measure at the moment it matters. And hold your own instruments to the same suspicion: one investigation blamed a correct check because its own data export had been silently cut off at a hundred rows.

---

## 🟣 CHILD NOTE

Don't trust the note on the fridge that says 'we have milk.' Open the fridge and look. And if the fridge light seems broken, check the bulb before you say the fridge is empty.

---

## 👵 GRANDMA NOTE

You know how it is, dear — somebody tells you the garden was watered, but you still go out and touch the soil. Papers and lists are fine, but they're yesterday's news. When it matters, look with your own eyes, today. And make sure your glasses are clean before you say the room is dusty.

---

## 🤖 NAYA NOTE

Treat every ledger, registry entry, packet, and sign-out — including your own — as a claim with a freshness date. Before acting on one, re-read the live source: the production data, the current tip, the actual file where the law lives. When two receipts conflict, live state is the tiebreaker, and the stale one gets owned in the open. Before repairing a red signal, confirm it still exists on the current base. Before declaring a gate wrong, audit your instrument with full, untruncated reads.

---

## WHAT IT MEANS

A system run by many hands generates records faster than reality changes them — every record is a photograph of a moving river. Anchoring truth to the live source is what keeps the whole team's shared picture honest; without it, each lane works from a different yesterday and the coordination collapses into confident confusion.

---

## WHAT'S IN IT FOR YOU

You get answers based on what is true now, not what was true when someone wrote it down. Problems that have already healed don't get fixed again, real problems don't hide behind reassuring paperwork, and when something is reported to you, it was checked against the real system first.

---

## HOW IT APPLIES

Whenever a document and the world disagree: stop, measure the world directly, act on the measurement, and flag the stale record for its owner to correct through the proper path — never quietly rewrite someone else's record yourself. Date your claims, give caveats an expiry trigger, and refresh descriptions whenever the work they describe materially changes.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0175 — An Endorsement Only Counts on a Live Venue Re-Read [audit: PARTIAL → lost element restored]

An endorsement of another lane's correction binds only the venue's live state re-read by the endorser (PR state/draft, head SHA, base vs current main tip) — quoting the claimant's stated evidence is secondhand and adds no confirmation weight. Every correction receipt must split explicitly: VERIFIED (re-read live by the endorser, citing what was re-read) vs WITNESSED (the originating lane's first-seen findings, not adopted, no relay action taken). Anchor unchanged heads/pins in the receipt as a no-move attestation. Never endorse a correction you have not looked at yourself — a relay that only repeats words is an echo, not a second lane.

### SN-0354 — The Check Can Contradict the Evidence — Reconcile the DB Directly, Then Accept the Verification Wall [audit: PARTIAL → lost element restored]

When the verification wall is real, accept it — record it plainly and park: name every ruled-out cause, name the unexplained residue without inventing causes, park the lane, and name the exact awaited decision and its owner. UNKNOWN is a complete state when it is named, evidenced, and parked — this is not inaction, it is the verified-verdict discipline.

### SN-0371 — Verify the Gate's Teeth Before Designing Around It [audit: MISSING → restored in full]

Before adopting any design that depends on a gate, sample the gate's actual behavior on live state in the exact configuration the design needs — a gate you have not observed completing is not a gate, it is a rumor of a gate. A fail-closed gate that can never complete is a functional regression wearing a safety costume, not a fix. (The instance: the spec required real Supabase validation before the production pointer moves; sampling 4 PR-head commits — `1c27d0bd`, `16317092`, `9b06c819`, `cc04e3d6` — showed the "Supabase Preview" check concludes skipped 4/4, so staging-branch pre-validation would time out fail-closed (15 min) on every run and the promotion would never complete; the reviewer wrote "I will not build it" — and was right.) When the strong design is blocked, offer the honest weaker interim with its exact failure-class coverage, and never present it as the spec.

### SN-0451 — Intelligent Block: SN-0451 [audit: PARTIAL → lost element restored]

Audit the ratified authority text itself — never trust memory's path claim for where that authority text lives. Before any conformance audit, the audit's own authority document must be located on the exact SHA being audited; every cited artifact gets re-anchored on the live tip before it is trusted, because memory's path claims are leads, not evidence. A conformance finding against the wrong contract version is a fabricated result. (The instance: memory said the ratified NAYA Design Contract was on main at `BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md` (PR #1346); the live tree at tip `0a1353bc` proved it absent — it existed only on PR #1346's unmerged branch.)

### SN-0520 — The Ghost Table — a Migration Ledger Says Applied, but the Table Is Gone [audit: PARTIAL → lost element restored]

The migration ledger tracks migration HISTORY, not table EXISTENCE: a DROP outside the migration system is invisible to the ledger — the reconcile tool only refreshes metadata for entries already present, and a vanished table has no entry to refresh — so "164 repo = 164 DB = 164 ledger, 0 orphans" can be true while a deployed runtime queries a ghost. Never cite ledger reconciliation as table-existence evidence; check LIVE EXISTENCE in the live schema. Deployed code is frozen at its deploy stamp and does not know the schema moved on, so every architecture move must repoint every deployed consumer, not just the new code path. And tests that mock the row hide the break: CI green proves "the code handles the mock correctly," never "the table exists."

### SN-0624 — A Quarantine Snapshot Is Point-in-Time Evidence — Reconstruct the Collision Registry from Live Bytes Before Triaging [audit: PARTIAL → lost element restored]

A quarantine snapshot is a point-in-time triage request, not a verdict: reconstruct the collision registry from live bytes before triaging, otherwise already-resolved collisions get acted on and invent damage. The procedure: (1) pin the revisions you will inspect — main HEAD SHA, each relevant branch HEAD SHA, open SN PR heads — naming each SHA in the receipt; (2) enumerate the actual artifacts at those SHAs, normalizing identifiers (leading zeros, case, date-partition prefixes) before comparing; (3) only then classify each listed item as still-live, already-resolved, or never-real, and report the delta between the list and the world explicitly. Never renumber, re-file, or re-close from list state alone.

### SN-560 — Stale Narrative Loses to Ratified Law — Re-Verify the Governance Boundary at Action Time [audit: PARTIAL → lost element restored]

A PR's stated gate (for example "Human Director merge gate") is a claim about governance, not governance: narrative decays, ratified law governs. At action time: (1) isolate the gate claim from the authority — the claim is evidence of past governance, not current governance; (2) re-derive the authority classification from the ratified sources (authority-model change, authority-envelope change, or implementation inside an already-authorized contract); (3) check the changed-path set against protected surfaces at the exact head — protected-path touch is what routes a change to a human gate, not the PR's prose; (4) if the narrative is stale, name it stale explicitly in the record and proceed under the ratified law — do not ask for a permission the law does not require.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn560-stale-narrative-loses-to-ratified-law`
- `IB-SMART-NOTE-20260930-sn0175-endorsement-on-live-venue-reread`
- `IB-SMART-NOTE-20260930-sn0624-quarantine-snapshot-stale-reconstruct-live-bytes`
- `IB-SMART-NOTE-20260930-sn0185-pr-body-drift-rebind-to-head`
- `IB-SMART-NOTE-20260930-sn041-stale-caveat-decay`
- `IB-SMART-NOTE-20260930-sn0451-audit-the-authority-text-itself`
- `IB-SMART-NOTE-20260930-sn0426-relay-receipt-corroborate-live-bytes-not-prose`
- `IB-SMART-NOTE-20260930-sn0587-production-is-truth-ledger-is-claim`
- `IB-SMART-NOTE-20261005-sn0398-stale-state-claims-die-on-live-bytes`
- `IB-SMART-NOTE-20261005-sn0354-check-contradicts-evidence`
- `IB-SMART-NOTE-20261005-sn0356-check-was-right-csv-truncated`
- `IB-SMART-NOTE-20261007-sn0554-stale-base-red-vs-current-main-red`
- `IB-SMART-NOTE-20261007-sn0536-ledger-applied-is-a-claim-not-a-proof`
- `IB-SMART-NOTE-20261006-sn0520-ghost-table-phantom-schema-reference`
- `IB-SMART-NOTE-20261006-sn0492-one-sign-out-per-tick-live-bytes-break-ties`
- `IB-SMART-NOTE-20261005-sn0371-verify-gates-teeth-before-designing-around`
