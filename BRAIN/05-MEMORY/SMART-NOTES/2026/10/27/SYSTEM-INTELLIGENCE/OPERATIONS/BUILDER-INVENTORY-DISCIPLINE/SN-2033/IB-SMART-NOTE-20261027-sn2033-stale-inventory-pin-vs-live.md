# IB-SMART-NOTE SN-2033: A Pin-vs-Live Mismatch Is Stale Inventory, Not Builder Breakage — Re-Derive Before You Block

Intelligent Block: IB-SMART-NOTE
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-27
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A Smart Builder inventory `--check` failed because the stored design-catalog pin (26687bdc) no longer matches live (36254500). That mismatch means the inventory snapshot is old — not that the builder broke. Re-derive the inventory from live and re-run the check before recording a builder failure or blocking a gate on it.

## 🩷 HUMAN NOTE

Think of the pin as a photograph of a shelf. If the shelf has changed since the photo was taken, the photo disagreeing with the shelf does not mean the shelf is broken — it means the photo is out of date. Take a new photo first, then judge.

## 🟣 CHILD NOTE

You have a list of toys from yesterday. Today there are different toys on the shelf. Your old list does not match — but nothing is broken! Just make a new list from what is there today, and then check again.

## 🔵 GRANDMA NOTE

It is like checking an old phone book against the real town. Names have changed since it was printed, so mismatches are expected. You do not declare the town broken — you get the new phone book and check again.

## 🟠 NAYA NOTE

Cold successor, when a Smart Builder inventory `--check` fails: stop before you write "builder broken" or block a gate. First compare the stored design-catalog pin against live. If pin != live, the failure mode is SMART-BUILDER-INVENTORY-STALE — re-derive the inventory from live, re-run `--check`, and only treat a failure that survives a live-derived re-check as real builder breakage. This keeps a routine catalog move from becoming a false gate block, and it keeps the failure record honest: stale snapshots are re-derived, not mourned.

## 🟢 MACHINE NOTE
{
  "sn": "SN-2033",
  "title": "A Pin-vs-Live Mismatch Is Stale Inventory, Not Builder Breakage — Re-Derive Before You Block",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_date": "2026-10-27",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "A Smart Builder inventory --check failure with a stored design-catalog pin that differs from live is stale inventory, not builder breakage; re-derive from live and re-check before recording a failure or blocking a gate.",
  "failure_mode": "SMART-BUILDER-INVENTORY-STALE",
  "applies_when": ["smart-builder", "inventory-check", "pin"],
  "enforcement": "On any Smart Builder inventory --check failure, diff the stored design-catalog pin against live before acting; a failure with pin != live must be re-derived from live and re-checked, and may not be recorded as builder breakage or a gate block until a live-derived re-check also fails.",
  "evidence": "Board #3066, Naya Code gate watch comment 6444571416, relayed by director tick 2026-10-27T14:39Z: inventory run 40509887420 job 122208681924 failed --check, design-catalog pin 26687bdc vs live 36254500; owner Naya 5 / Smart Builder library owner.",
  "decision_change": "When an inventory --check fails, the decision changes from 'record builder failure / block the gate' to 'compare pin to live first; re-derive and re-check if they differ'.",
  "falsifier": "A pin-vs-live mismatch --check failure that still fails after re-deriving the inventory from live and re-running --check, or a case where live itself is the stale/corrupt side and the pin is correct, would prove the stale-inventory reading wrong for that case.",
  "mechanism": "Pins are snapshots; the design catalog moves as work lands, so --check compares a frozen snapshot against current live and any intervening landing produces a mismatch without any builder breakage.",
  "observation": false
}
