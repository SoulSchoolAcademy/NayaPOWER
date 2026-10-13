# Smart Connect — Open Doors

*The warm-plain telling. For exact values and procedures, see the `.ai.md` companion; for the structured schema, see `.machine.json`.*

## IN A NUTSHELL

Anyone who wants to connect gets an open door — no application, no approval, no waiting. The moment they connect, their first contribution (a lesson) is captured instantly, with zero gate. Within one cycle the loop distills it and shows them what it became: their lesson merged into a living note, or elevated toward law. The human can see the intelligence working — *your lesson became this*. If you contributed nothing, nothing is claimed for you. Honesty is the gate.

## THE FIVE PIECES

**1. Doors — the connection surfaces.** A door is a declared entry point with a registration contract: MCP, REST API, GitHub App, webhooks, SDK, agent-to-agent. Doors are declared, not invented here — this mechanism builds on the Smart Door contract and door registry at `BRAIN/10-INTERFACES/0001-SMART-DOOR-CONTRACT-V1` / `0002-SMART-DOOR-REGISTRY-V1`, which describe *what doors can do*. Smart Connect adds *who walked in and what they contributed*. One brain, many doors.

**2. Connection — the registered opener.** A record of a name, a door, a moment, and running counts. Registration never refuses: if the chosen door is down, the registry routes to another open door. A door may close only for harm — and the closure is recorded, never silent.

**3. Lesson — the contribution.** A captured text with its essence and a status: `INTAKE`, `MERGED`, `ELEVATED`, or `DUPLICATE`. Intake is instant — the word is the verification. Submitting the same lesson twice doesn't create two lessons; it lands on the one content-addressed record.

**4. Compound — the visible compounding event.** A recorded `MERGE` (duplicates distilled into one living note) or `ELEVATE` (a merged cluster proposed toward law). A compound is recorded only when a distillation actually ran. Contributing nothing compounds nothing — a number without proof is a lie.

**5. Cycle — the one-turn loop.** Connect → contribute (instant capture) → distill (normalize, dedupe, cluster, merge/elevate) → compound publication → feedback (the connection sees its compounds). One cycle = every contribution fully processed to a visible compound or a reasoned defer. The loop's latency is the product.

## THE SIX GUARANTEES

- **Open doors:** registration never refuses.
- **Instant capture:** lessons land in the intake ledger immediately.
- **No free compound:** nothing distilled, nothing compounded.
- **Visible in one cycle:** after one cycle, the connection's page shows its lessons and compounds.
- **Seam, not second mechanism:** the world-facing intake UX is B-44's lane (Bridger, wave 9, joint with Naya 4). B-44 calls this mechanism's seam; this mechanism owns the registry, the cycle, and feedback. Neither re-implements the other's half.
- **Approval law holds:** `ELEVATE` compounds are *proposals* to the canonical index through the same automated approval gates — no exceptions, no second standard. The intake ledger is not canon.

## WHAT IT IS NOT

- Not the Smart Door capability contract (what doors *can do*) — this is the connection and compounding *ledger*.
- Not the old app-era `nayanet_smart_connect` participation tables (member consent/RPC) — those remain the account layer; this is the intelligence layer.
- Not the intake UX — that's B-44's lane.

## SEAM CONTRACT

B-44's intake UX calls:

```json
POST lesson_intake.append
{ "connection_id": "conn-…", "text": "…", "door_id": "sdk" }
→ { "lesson_id": "les-…", "status": "INTAKE", "captured_at": "…" }

GET feedback.for_connection(connection_id)
→ { "connection_id": "…", "lessons": ["les-…"], "compounds": ["cmp-…"],
    "compound_count": 2, "cycles_run": 1 }
```

## PROOF, STATUS, WHAT'S NEXT

The reference implementation lives at `tools/smart_connect.py` (synthetic, no production writes). The proof gate at `tests/test_smart_connect_open_doors.py` demonstrates, on every run: a synthetic guest connects, contributes a lesson, and sees compounds citing it within one cycle — while a non-contributing guest gets zero compounds, a duplicate submission never double-compounds, and corrupted state fails closed instead of faking a merge. **Status: design + synthetic proof, verified. Open: real-registry similarity calibration (the 0.7 threshold is synthetic), ELEVATE wiring to the live approval gates.**
