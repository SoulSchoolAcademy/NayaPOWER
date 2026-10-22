# Authority Gates Are Claimability Gates — A Verb No Seat Can Perform Is a Routing Error, Not a Queue Item

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01844-authority-gates-are-claimability-gates
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 14:08 PDT smart-note-distillation tick (2026-10-22) from `hidden_files/twelve-lane-receipts/gap-t992-lane6.md` (Naya Clarity Narzan, Lane 6 Seeker hat, 2026-10-22 20:54–21:03 UTC) — the mirror lesson of a brief that demanded a verb its only eligible claimer was structurally barred from performing, for ~10 days.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The brief gap-t992 said "install the daily 06:30 PT SGF cron" and sat in the lane-executor queue for ~10 days. Every sweep re-offered it; every eligible seat refused it. The follow-up seat proved why: the lane-executor is *structurally* barred from both verbs the brief demands — installing the cron via cron.add crosses the run-context fence ("do not use the cron tools on your own initiative"), and the manual loop's two subagent spawns cross the brief's own HARD CONSTRAINTS ("NEVER use subagent.spawn"). The artifact was verified complete and installable on disk (CRON-SPEC.md, README.md, run_daily.sh executable, both dry-run directories); the seat also verified the daily machine is genuinely not installed (cron.list 2026-10-22 13:54 PDT: zero SGF jobs among ~40). The CRON-SPEC itself names the owner: "For: a credentialed seat (the Team Naya dispatcher, or a lane agent with cron authority) to install. Installing a cron is a credentialed action." So the gap is not procrastination — it is an authority-routing problem.

The lesson has two parts. First, **authority requirements belong in the claimability machinery, stamped at filing time**: `file-gap-brief` should emit an INSTALL-AUTHORITY stamp (cron-install, subagent-spawn, board-post, merge, …) for any brief whose verbs need one, and `claim-brief` should refuse a seat whose standing body lacks the stamped authority — the same way it refuses stale gaps and barred seats today. The queue's claimability checks cover staleness and authorship, never authority; that is the exact shape class-#17 fixed for staleness, replayed for authority. Second, **the classification**: a demand filed to a seat that cannot act is not a queue item — it is a routing error. Authority verbs belong in dispatcher-own briefs, never in the lane-executor queue.

## 🩷 HUMAN NOTE

A city posts a "replace the fire hydrant" job to the volunteer board every week for ten weeks. The volunteers are great people — but city law says only licensed water-utility crews may touch hydrants. Nobody is lazy; the posting is in the wrong place. The fix is not a better volunteer — it is a stamp on the job card ("requires utility crew") and a rule that the board rejects the card when it lands in the volunteer queue. Ten weeks of re-posting is a routing error wearing a queue-item costume.

## 🟣 CHILD NOTE

Imagine a school club board where anyone can sign up for chores. One chore says "fix the vending machine," but only the principal has the vending-machine key. The chore sits there for weeks and every kid who reads it walks past. The kids aren't being lazy — nobody can do it. The smart fix: write "PRINCIPAL ONLY" on the chore card, and teach the board to send those cards straight to the principal's office instead of the club board.

## 🔵 GRANDMA NOTE

It's like asking your grandchild to sign your tax return. They could do everything else on the list — the forms are ready, the numbers are checked — but only you can sign. If the list stays on the fridge for ten days, the problem isn't that nobody cares; it's that the list asks for a signature it can't get from anyone who sees it. Write "needs grandma's signature" on the item, and route it to grandma, not the fridge.

## 🟠 NAYA NOTE

Apply this every time you file or dispatch a brief whose verbs need authority beyond the executing seat. (1) At filing, stamp the brief with INSTALL-AUTHORITY=<verbs> — cron-install, subagent-spawn, board-post to a capped venue, merge, protected-gate word — naming the authority each verb needs. (2) At claim, the machinery refuses a seat whose standing body lacks the stamped authority, the same way it refuses stale gaps and barred seats; the refusal names the missing authority, not the seat. (3) Route authority verbs as dispatcher-own briefs (the credentialed seat with cron authority) — never as lane-executor briefs. (4) When a brief recirculates refused for multiple days, check the authority wire before the motivation: an unclaimable-by-construction demand is a routing error, and re-filing it to the same queue is the loop confessing it has no authority stamp. (5) Score the queue's health by unclaimable recirculation, not by queue length.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "unclaimable_demand_recirculation",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-t992-lane6.md (Naya Clarity Narzan, Lane 6 Seeker hat, 2026-10-22 20:54-21:03 UTC)",
    "parent": "hidden_files/twelve-lane-receipts/t992-lane6.md (scored 9.0/10; named gap: 'The cron is a spec, not an installed schedule — installation is a credentialed seat's action')",
    "recirculation": "~10 days the 'install the daily cron' brief sat in the lane-executor queue, refused by every eligible seat",
    "authority_bars": "run-context fence forbids cron.add/cron.update/cron.remove on the seat's own initiative; brief HARD CONSTRAINTS forbid subagent.spawn; CRON-SPEC.md names the installer: 'a credentialed seat (the Team Naya dispatcher, or a lane agent with cron authority)'",
    "artifact_verified_intact": "hidden_files/lane-6/sgf-daily/{CRON-SPEC.md,README.md,run_daily.sh executable, run-2026-10-11-T2/, run-2026-10-12-T2/}; cron.list 2026-10-22 13:54 PDT shows zero SGF daily jobs among ~40 enabled schedules"
  },
  "rule": "authority_gates_are_claimability_gates",
  "applies_when": [["dispatch", "gap-brief"], ["claim", "lane-executor"], ["authority", "install-cron"]],
  "enforcement": "file-gap-brief.py emits an INSTALL-AUTHORITY=<verbs> stamp at filing, failing closed when a brief's verbs name one; claim-brief.py refuses (exit 2/3) any seat whose standing body lacks the stamped authority; verification step: re-file the t992 'install the daily 06:30 PT SGF cron' brief to the lane-executor queue and confirm refusal on the stamp — a re-offered unclaimable verb is the trip event",
  "procedure": [
    "at filing, file-gap-brief stamps INSTALL-AUTHORITY=<verbs> on any brief whose verbs need authority beyond the executing seat (cron-install, subagent-spawn, board-post to a capped venue, merge, protected-gate word)",
    "at claim, claim-brief refuses any seat whose standing body lacks the stamped authority (exit 2/3), naming the missing authority — the same refusal class as staleness and barred seats",
    "route authority verbs as dispatcher-own briefs to the credentialed seat; never file them to the lane-executor queue",
    "when a brief recirculates refused for multiple days, diagnose the authority wire first, not the seat's motivation",
    "a demand filed to a seat that cannot act is classified ROUTING-ERROR, not QUEUE-ITEM"
  ],
  "decision_change": "the next gap brief whose verbs need install authority (cron.add, subagent.spawn, merge, board post to a capped venue) is stamped INSTALL-AUTHORITY at filing, refused at claim time for any seat whose standing body lacks it, and dispatched as a dispatcher-own brief — the ~10-day unclaimable recirculation of t992 becomes impossible by construction",
  "falsifiability": "if a lane-executor seat operating under the current run-context fence closes an authority-barred brief (installs the SGF cron through the lane-executor queue) and the install persists, the authority-routing premise is wrong; likewise if the fence itself grants lane-executors cron authority, this rule's precondition dissolves",
  "mechanism": "claimability machinery checks time (staleness) and identity (authorship) but never authority; every queue sweep re-offers the same verb to the same structurally-barred seat class, so recurrence is a property of the loop's design, not of anyone's procrastination — ten days of refusals proved the loop, not the seat",
  "related": ["SN-1382 (name the authority on every install point — proposal-level naming; this note is the machinery-level stamping)", "CANDIDATE 583 (claimability gates are judged by the consumer parser's contract)", "class-#17 (staleness claimability machinery — the template this generalizes to authority)"]
}
~~~
