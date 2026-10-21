# Dock-Claimed Rows Are Hands-Off — Consult the Workdown State Before Dispatching

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1749-dock-claimed-rows-hands-off
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-21 the dock owned ranked workdown row #2804 (rank 20) and ran a cure agent on it — while an area-builder's workdown execution independently started a second cure on the same row. Two cures raced; the second push stomped the first on a stale base. The dock reconciled them (tree comparison + stacking commit → one IV target 184363c0), absorbing a full diagnosis-and-port cycle that an hour of coordination would have prevented. Rule: before any area builder touches a ranked workdown row, the dispatcher must read hidden_files/dock-workdown-1to21.json and treat rows marked in-flight/HELD/routed as hands-off. A wave that double-dispatches a dock-claimed row fails its own fold as a coordination miss.

## 🩷 HUMAN NOTE

Hey Shawn — guess what: two of our own agents rebuilt the same fix on PR #2804 at the same time — the dock's cure agent and an area builder — and the second push stomped the first. The dock had to reconcile both by comparing trees and stacking a commit, which is maybe not the most intelligent thing when a one-line check would have prevented it. What I suggest: the dispatcher reads the dock's workdown state file (dock-workdown-1to21.json) before handing out ranked rows, and any row marked in-flight, HELD, or routed is hands-off for anyone but the owning dock agent. Why: one authoritative list of who's doing what is the cheapest serialization we have — cheaper than reconciling two pushes after the fact. What I did: filed this as a smart note (SN-1749, CANDIDATE) with the enforcement wired in — a wave that double-dispatches a dock-claimed row fails its own fold as a coordination miss.

## 🟣 CHILD NOTE

Two cooks grabbed the same pot and both tried to stir the soup — soup splashed everywhere. The fix isn't better stirring; it's a sign-up sheet on the fridge that says which pot is taken. Before you cook, read the sheet. If the pot is taken, pick another pot.

## 🔵 GRANDMA NOTE

We keep a ranked to-do list for fixing code, and one team (the dock) keeps a little ledger saying which items it's already working on. An area builder picked up an item the dock was already fixing — both wrote fixes, and the second one overwrote the first. The dock had to merge the two by hand. The lesson: before handing out work from the list, look at the dock's ledger first. If an item says someone's on it, hands off — hand out something else.

## 🟠 NAYA NOTE

For the director/dispatcher briefing area builders against ranked workdown rows: consult hidden_files/dock-workdown-1to21.json in the brief generator before every dispatch — read the row's state and print it in the thinking block. Rows marked in-flight, HELD, or routed are hands-off for any seat that is not the owning dock agent; dispatch a different row. Teeth: a wave that double-dispatches a dock-claimed row fails its own fold as a coordination miss (not a dock problem to reconcile). Owner of the mechanism repair: director + dispatcher (dock event 6306874220). Cousins: SN-1708 (stale re-dispatch — verify before rebuilding; this note is the claim-racing leg, SN-1708 is the staleness leg); SN-0479 three-try circuit breaker (the reframe principle: change the mechanism, not the seat — the reframe here is check-before-dispatch).

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn1749-dock-claimed-rows-hands-off",
  "title": "Dock-claimed rows are hands-off: consult the workdown state before dispatching",
  "lesson": "2026-10-21: PR #2804 (rank 20, dock-owned) got parallel cures from the dock's cure agent and an area-builder's workdown execution - the second push stomped the first on a stale base; the dock reconciled by tree comparison + stacking commit into ONE IV target 184363c0 (superseding IV requests 6306795697 + 6306831848), costing a full diagnosis-and-port cycle. Rule: before dispatching any ranked workdown row, the brief generator must read hidden_files/dock-workdown-1to21.json, print the row state in the thinking block, and treat rows marked in-flight/HELD/routed as hands-off for non-owning seats. Cousins: SN-1708 (stale re-dispatch verify-before-rebuild - same dispatch family, different leg: racing claims vs stale premise); SN-0479 (three-try circuit breaker - the reframe principle: change the mechanism, not the seat).",
  "applies_when": [["dispatch", "workdown"], ["coordination", "dock"]],
  "enforcement": "Brief-generator mechanical check: read hidden_files/dock-workdown-1to21.json and print the row state in the thinking block before dispatching any ranked workdown row; rows marked in-flight/HELD/routed are hands-off for any seat that is not the owning dock agent. A wave that double-dispatches a dock-claimed row fails its own fold as a coordination miss. Owning lanes: director + dispatcher (per dock event 6306874220).",
  "evidence": ["#2793 comment 6306874220 (Naya Verity Narzan, dock, 2026-10-21T03:08:00Z): 'BUILDERS RACED THE DOCK on ranked workdown row: #2804 (rank 20, dock-owned) got parallel cures from the dock's cure agent and an area-builder's workdown execution - second push stomped the first on a stale base. Reconciled by dock (tree comparison + stacking commit). next: every area-builder brief must consult hidden_files/dock-workdown-1to21.json before touching a ranked workdown PR - rows marked in-flight/HELD/routed are hands-off.'", "shared-state.json director_tick_20261020_2008 (2026-10-21T03:08:00Z): '#2804 race RECONCILED (tree compare + stacking commit) -> ONE IV target 184363c0; mechanism repair owed (dock-claimed rows hands-off)'", "#2793 comment 6306873909 (dock, reconciled ONE-IV request superseding 6306795697 + 6306831848): the race's cost made visible as two superseded IV requests"],
  "decision_change": "The director/dispatcher decision 'which seat to dispatch to a ranked workdown row': the brief generator now reads hidden_files/dock-workdown-1to21.json first and prints the row state in the thinking block; a row marked in-flight/HELD/routed is hands-off and a different row is dispatched. Without this note the dispatcher dispatches blind and the dock pays the reconciliation cost.",
  "falsifiability": "Falsified if: (1) the brief generator consults the row-state file and a double-dispatch still occurs - then a file read is not a claim lock and the mechanism needs a real atomic claim, not a read; or (2) parallel cures are shown harmless-by-construction (tree-compare reconciliation always converges with zero lost work), which would weaken the hands-off rule to advisory. Until either is shown, the note holds.",
  "mechanism": "Claim serialization through a single authoritative row-state file: consulting dock-workdown-1to21.json before dispatch makes a double-claim visible pre-work (read the sheet, see the pot is taken) instead of post-push (two pushes, one stomps the other). The fold-fail teeth route the cost to the cause - the dispatching wave fails its own fold as a coordination miss - rather than taxing the dock with reconciliation.",
  "captured_date": "2026-10-21",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/OPERATING-MODE/DISPATCH-COORDINATION"
}
```
