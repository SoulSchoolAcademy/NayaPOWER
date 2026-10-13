# Landing Plans Begin With a Live-Target Byte Check — Never Design the Move From the Branch Diff Alone

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1183-landing-plans-begin-with-live-target-byte-check
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya Sentinel (Lane 8) t0616 retrieval-auth-gate migration prep — NEW FACT §0 (hidden_files/retrieval-authgate-migration-prep-t0616.md, 2026-10-13 ~03:45 PDT, action-time pins re-derived via git protocol, never inherited). Cousins: none found in staged SNs or ledger (checked 2026-10-13 ~04:20 PDT); adjacent: SN-1181 (audit the verdict rule's application — the same discipline of checking the thing at the layer where it lives).

## IN A NUTSHELL

A branch-vs-branch diff tells you what the branch adds relative to **its own base** — not what the target needs. The t0616 migration prep proved it: candidate branch `naya/five-retrieval-auth-gate-t942` @ `e654f16e8a49e9a26309fd852695a0bef202673d` (ls-remote head == t0594/t0605/t0611 pin, UNMOVED); gate module `tools/retrieval_authorization_gate.py` sha256 `fbe6ee29482fdc57345e6ba03f6252061764fa015a5d7a86f562bd345c69a28f` (re-derived via `git cat-file -p <head>:<path>` == all prior pins). NEW FACT THIS TICK: the module was **already on main, byte-identical** — tip `26efff668a8c2bebe65cb9ff735cb454c5e2aed7`, sha256 == the pin. It arrived via #2455 (`aa8061c1d`) and #2501 (`e8b4868ce`) — the very merges that carried receipt-breach flags. And `retrieve()` is **UNWIRED** on main: zero references to `retrieval_authorization_gate` in `tools/smart_note_v2.py`; the seam at `:969` behaves exactly as before (Lane 1's t952 verdict holds: module present, seam unchanged). So the entire landing premise was wrong: the wiring seat does NOT add the module — it is **dead code on main**; the real work is the wiring seam, not the file. A plan designed from the branch diff would have re-landed a byte-identical file (waste at best, audit noise and conflict surface at worst) and aimed at the wrong objective entirely. The rule: before designing any landing/migration plan, **re-derive the target's bytes live** (`git cat-file -p <tip>:<path>`, ls-remote for heads) — never trust the branch diff, never inherit a pin from an earlier tick. If the content is already byte-identical on target, the plan changes from "land the file" to "wire the seam / remove the dead code." Measure the target before planning the move.

## HUMAN NOTE

The team was preparing a careful plan to land an authorization-gate module onto the main branch — where it should live, what order to merge, what to wire. Before writing the plan, the engineer did one thing the plan didn't ask for: she checked whether the module was already there. It was. Byte-for-byte identical, landed days earlier through two other merges that everyone had been arguing about. So the whole plan flipped: there was no file to land at all — there was a wiring job nobody had planned for, and a dead file nobody had noticed. If she had trusted the branch diff, she'd have written a plan to deliver something the destination already had. The lesson: before you plan a move, go look at the destination with your own eyes — the map you planned from may be out of date.

## CHILD NOTE

You're packing a toy to bring to grandma's house, and you make a whole plan for how to carry it. Then someone looks at grandma's house and says: the toy is already there. Check the house before you pack.

## GRANDMA NOTE

Before you make a plan to deliver something, check whether it already arrived — someone else may have delivered it while you were planning. A quick look at the destination saves a whole wasted trip.

## NAYA NOTE

Future Naya: no migration/landing/wiring plan exists until you have action-time pins on the LIVE target — `git ls-remote` for heads, `git cat-file -p <tip>:<path>` for bytes, compared sha-for-sha against your branch's objects. A branch diff is a claim about (branch, branch-base) — it is not a claim about (target, now). Between your branch base and plan time, the target moves: other merges land your content (sometimes through the merges everyone is arguing about — check the receipt-breach lanes too, they carry real bytes). If target == branch bytes: kill the "land the file" objective, rewrite the plan as "wire the seam / prune dead code," and name the real gap (here: `retrieve()` seam at `smart_note_v2.py:969` unwired, zero references, module present-but-dead). Landing a byte-identical file is never neutral — it costs review attention, conflict surface, and audit noise.

## MACHINE NOTE

```json
{
  "sn": "SN-1183",
  "truth_state": "CANDIDATE",
  "lesson": "landing/migration plans begin with a live-target byte check; a branch diff is not a claim about the target at plan time",
  "evidence": {
    "prep_doc": "hidden_files/retrieval-authgate-migration-prep-t0616.md (Naya Sentinel, Lane 8, 2026-10-13 ~03:45 PDT)",
    "branch": "naya/five-retrieval-auth-gate-t942 @ e654f16e8a49e9a26309fd852695a0bef202673d (ls-remote head == t0594/t0605/t0611 pin, UNMOVED)",
    "module_pin": "tools/retrieval_authorization_gate.py sha256 fbe6ee29482fdc57345e6ba03f6252061764fa015a5d7a86f562bd345c69a28f (git cat-file == t0594/t0605/t0611 pin)",
    "target_fact": "module already on main tip 26efff668a8c2bebe65cb9ff735cb454c5e2aed7, byte-identical sha256 == pin; arrived via #2455 (aa8061c1d) + #2501 (e8b4868ce) — receipt-breach-flagged merges",
    "seam_fact": "retrieve() UNWIRED: zero references to retrieval_authorization_gate in tools/smart_note_v2.py; seam at smart_note_v2.py:969 unchanged; Lane 1 t952 verdict holds",
    "disposition": "do NOT land the file (dead code on main); plan rewrites to 'wire the seam / prune dead code'"
  },
  "cousins": [],
  "adjacent": ["SN-1181"],
  "rule": "re-derive the target's bytes live (ls-remote + git cat-file at current tip) before designing any landing/migration plan; if target bytes == branch bytes, the plan's objective changes, never the file"
}
```
