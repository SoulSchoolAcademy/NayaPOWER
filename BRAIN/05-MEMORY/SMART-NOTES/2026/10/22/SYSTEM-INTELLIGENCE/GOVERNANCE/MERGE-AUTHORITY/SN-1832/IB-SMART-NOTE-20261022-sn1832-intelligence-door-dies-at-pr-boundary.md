Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

PR #2916 merged at 15:04:13Z carrying the SN-1801/SN-1802 intelligence markdown with no scorecard — CodeRabbit/Codex bot reviews only, which do not substitute. The 2026-10-21 intelligence door ruling gives direct writes the no-queue path ("Smart Notes + lessons land by direct write, no merge queue"); a PR is not a direct write. The privilege attaches to the transport (direct write avoids queue cost), not to the content class. Intelligence riding a PR is a PR, and it carries a scorecard like one — the merge-loop receipt check never accepts "intelligence content" as a scorecard waiver. A merged intelligence-carrying PR without a scorecard is filed as the named failure mode RECEIPT-GAP-INTELLIGENCE-DOOR, not absorbed as door traffic.

## 🩷 HUMAN NOTE

Shawn — there's a shortcut for getting Smart Notes into the system: they go in by direct write, no review queue. But that shortcut is about the path, not the content. Tonight a pull request carrying Smart Note files got merged with no scorecard, and bot reviews were offered as the proof. That doesn't count. The moment intelligence rides a pull request, it's a pull request — and pull requests carry scorecards. The shortcut can't hitch a ride inside the thing it was designed to bypass. The gap got named tonight so it can't hide in the "it's just intelligence" excuse again.

## 🟣 CHILD NOTE

Imagine the teacher says, "homework can be turned in at the special box, no line needed." But then a kid walks to the front of the grading line with his homework and says, "no line — this is homework!" The rule was about the special box, not about the homework. If it rides the line, it waits in the line. The paper doesn't carry the shortcut with it.

## 🔵 GRANDMA NOTE

It's like the express lane at the market — ten items or less, no waiting. But the express lane is about where you check out, not what's in your cart. If you take those same ten items to the regular checkout, you wait in line like everyone else. The groceries don't carry the express lane with them; the lane is the lane.

## 🟠 NAYA NOTE

Receipt discipline, Naya to Naya: the intelligence door's no-queue privilege dies at the PR boundary. The 2026-10-21 door ruling is precise — "Smart Notes and learning lessons land on main by direct write — no merge queue, no delay"; the other half of the same ruling is that "code, interfaces, and everything that is not intelligence itself goes through the full scored process." PR #2916 (merged 15:04:13Z, SN-1801/SN-1802 md-only landing) crossed the boundary the wrong way: it rode the PR path with no scorecard and no human seat, only CodeRabbit/Codex bot reviews — which the director's 1508 tick explicitly rules out as substitutes — and was filed as RECEIPT-GAP-INTELLIGENCE-DOOR. The mechanism is transport-bound, not content-bound: the door's no-queue privilege is a cost optimization on the direct-write transport (no queue to drain, no scorecard to reconcile). A PR re-enters the scored merge machinery by construction — queue, scorecard, exact-head pin, dock hand. An exemption attached to the transport cannot travel inside the content; the moment intelligence boards a PR, it has left the door. The check is one receipt-read at merge: every merged PR carries a scorecard at its merged head, and "intelligence content" is not an accepted waiver reason. The failure mode is named so the next lane can't route around the gate with "it's just notes."

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1832-intelligence-door-dies-at-pr-boundary",
  "lesson": "The intelligence door's no-queue privilege attaches to the direct-write transport, not to the content class: intelligence riding a pull request is a pull request and carries a scorecard like one. A merged intelligence-carrying PR without a scorecard is the named failure mode RECEIPT-GAP-INTELLIGENCE-DOOR; bot reviews (CodeRabbit/Codex) do not substitute.",
  "applies_when": ["merge", "receipt"],
  "enforcement": "Merge-loop receipt check: every merged PR carries a scorecard at its merged head; 'intelligence content' is not an accepted waiver reason. A merged PR with intelligence files and no scorecard is filed as RECEIPT-GAP-INTELLIGENCE-DOOR in the tick entry and routed to the pipeline owner. Intelligence that must skip the queue lands by direct write — the door ruling's own delivery path — never by PR.",
  "evidence": [
    "hidden_files/shared-state.json director_tick_20261022_1508 receipt_watch (#2916 = RECEIPT GAP (intelligence-door class: SN-1801/1802 merged via PR 15:04:13Z, no scorecard, CodeRabbit/Codex bot reviews only which do not substitute; surfaced))",
    "Intelligence door ruling 2026-10-21 (MEMORY.md: Smart Notes + lessons land by direct write, no merge queue; code/interfaces go through the full scored process; the door never carries code)"
  ],
  "decision_change": "The next lane that wants intelligence on main without the merge queue uses the door's own path — direct write. The lane tempted to 'just open a PR, it's only notes' now faces the receipt check: a PR without a scorecard is bounced at the gate, whatever the content class.",
  "falsifiability": "Superseded if the intelligence door ruling is ever extended to PRs in Shawn's own bytes — the door's current text is transport-scoped ('direct write'), so a ruling that explicitly waives scorecards for intelligence-carrying PRs would retire this note.",
  "mechanism": "Transport-bound privilege: the door's no-queue privilege is a cost optimization of the direct-write transport — no queue exists on that path, so nothing is skipped. A PR re-enters the scored merge machinery by construction (queue, scorecard, exact-head pin, dock hand); carrying intelligence cannot buy it out because the machinery is defined by the path, not the cargo. Bot reviews are static analysis, not verdicts — they answer 'does it parse' while a scorecard answers 'does it hold at the frozen head.'"
}
```
