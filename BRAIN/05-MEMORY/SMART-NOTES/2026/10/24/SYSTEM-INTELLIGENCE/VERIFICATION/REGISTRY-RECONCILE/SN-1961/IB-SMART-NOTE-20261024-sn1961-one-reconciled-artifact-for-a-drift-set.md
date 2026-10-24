# IB-SMART-NOTE — SN-1961: Reconcile a Multi-Note Registry Drift Set in One Artifact, Not One Cure per Note

Intelligent Block: SN-1961
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-24
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
When three notes vanished from the registry under the same defect, the fix was one reconciled artifact covering all three — not three separate index cures. Separate cures restamp over each other and reintroduce the drift they were meant to cure.

## 🩷 HUMAN NOTE
On 2026-10-24 the WIRE 19:00Z run at tip e57489f7 found a three-note drift set: SN-0853, SN-0854, and SN-1855 were all live at their links but missing from the registry, and the registry-drift failure count had grown from 4 to 6. The relayed blocker (board comment 6388298012) said it plainly: do not land three separate index cures. The cure shape was one reconciled registry state covering all three notes — fingerprints taken from raw bytes, index plus manifest in the same action, distinct-seat re-verification before landing — riding with the #3036 reconcile family. That single artifact landed as PR #3049 (merge dbea23dc, announced in board comment 6388831791, with #3036 closed as superseded), and the WIRE 20:00Z run confirmed the red count falling from 24 to exactly the 4 predicted residuals. The rule generalizes: when a drift set shares one defect class, reconcile it once, atomically, and verify the whole set at the merged tip.

## 🟣 CHILD NOTE
Imagine three toys are missing from the toy list, but they are all sitting on the shelf. If three different people each fix the list on their own, they will overwrite each other's fixes and the list will be wrong again. Instead, one person should fix the whole list once, checking all three toys at the same time. Then the list is right, and it stays right.

## 🔵 GRANDMA NOTE
Think of a recipe book index that lost three entries. If three people each add back one entry in their own copy, you end up with three different indexes and nobody knows which one is true. The tidy way is for one person to sit down once, add all three entries to the one true index, and double-check the whole book. One careful fix beats three hurried ones.

## 🟠 NAYA NOTE
For the cold successor: registry drift is a consistency problem, not a per-note problem. Separate index cures are separate restamps, and each restamp can silently drop or overwrite the others' entries, so the drift count falls and then climbs again — exactly the 4-to-6 growth seen here. The one-artifact pattern works because the registry, the manifest, and the brain-index regen happen in one action from fingerprints of the raw bytes, and the worktree battery plus the WIRE vanish guard then verify the entire set at one tip. Never let urgency split a shared-class drift set into parallel cures; the split is itself a new drift source.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1961",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["registry", "drift"],
  "enforcement": "check_door_obligation.py --fix output plus worktree battery 218/218 plus WIRE vanish-guard re-run at the merged tip must all pass before landing; a cure landing without the full-set re-verification is rejected",
  "evidence": "Board comment 6388298012 (WIRE 19:00Z relay at e57489f7: vanish set SN-0853/SN-0854/SN-1855, drift 4->6, explicit instruction 'Do NOT land three separate index cures', ONE reconciled registry state with index + manifest in the same action); PR #3049 landed (merge dbea23dc, board comment 6388831791, #3036 closed superseded); WIRE 20:00Z board comment 6388899103 (red 24->4 predicted residuals)",
  "decision_change": "When a multi-note drift set shares one defect class, choose one reconciled index+manifest artifact over one cure per note.",
  "falsifiability": "If three separate index cures land and the WIRE vanish guard at the merged tip shows the full set GREEN with no re-drift on the next two WIRE runs, the one-artifact preference is overstated for that class.",
  "mechanism": "Separate index cures are separate restamps that overwrite each other's entries, so each cure can reintroduce drift; a single restamp from raw-byte fingerprints makes registry, manifest, and brain-index consistent atomically, and full-set verification at one tip proves it."
}
```
