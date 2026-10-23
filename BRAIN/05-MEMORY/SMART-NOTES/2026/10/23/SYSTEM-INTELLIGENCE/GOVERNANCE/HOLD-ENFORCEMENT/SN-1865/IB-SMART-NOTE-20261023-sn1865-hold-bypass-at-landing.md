Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

#2990 merged at 04:33Z over an open independent HOLD (6356956833) on its exact head. The mechanism: **the merge path reads PR state, never the board's open-hold list — a STOP-class hold is invisible to the merge button.** VERIFY's post-merge card (STAND 8.0, card 6357842162) names the unreconciled premise: the landed test pins the publisher #2968 documents as the stale Hub overwriter, and the premise was never reconciled before landing. The durable rule: a HOLD is a STOP-class, and STOP-class means the landing machinery re-reads open holds at merge time and reconciles before the button counts. A hold that no gate reads is a comment with ambitions.

## 🩷 HUMAN NOTE

Shawn — a hold was placed on #2990's exact head and it merged anyway, because the merge button never looks at the hold list. Holds live on the board; the button reads the PR. So a STOP can be open and the landing still goes through — nobody's fault at the button, the wiring just never connected the two. The fix: at landing time, the machinery reads open holds and reconciles them before the merge counts. A hold must be something the machine checks, not just something a human reads.

## 🟣 CHILD NOTE

Imagine a red "STOP — do not cross" sign on a hallway, but the door at the end opens with a keypad that doesn't know the sign exists. You can walk right past the sign, type the code, and the door opens. The sign was right and the door was right — they just never talked. The fix: wire the keypad to the sign, so when the sign is up, the code doesn't work.

## 🔵 GRANDMA NOTE

It's like putting a "do not disturb" sign on the hotel door while housekeeping's key card opens it anyway — the sign is on one system and the key is on another, and they were never introduced. A sign that the key doesn't read is decoration. To make it real, the lock has to know about the sign.

## 🟠 NAYA NOTE

Holds are our strongest STOP-class signal — an independent seat saying "do not land this." But the signal travels on the board while the landing decision travels on the PR, and the two channels never meet at merge time. The lesson is architectural: every STOP-class signal must be readable by the machinery at the moment of action, or it is theater. Until the w704 pre-merge hold-check hook is ratified, VERIFY's post-merge card carries the load: it must name the hold's reconciliation state explicitly, and any landing over an open hold gets flagged HOLD-BYPASS-AT-LANDING into the named-failure-mode list so the pattern stays counted, not just noted.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1865-hold-bypass-at-landing",
  "lesson": "A HOLD is a STOP-class, but the merge path reads PR state, never the board's open-hold list — so #2990 landed over an open independent HOLD (6356956833) on its exact head with the hold invisible to the merge button. Any STOP-class signal must be readable by the machinery at the moment of action; until the w704 pre-merge hold-check hook is ratified, the post-merge card must name the hold's reconciliation state and every landing over an open hold is flagged HOLD-BYPASS-AT-LANDING.",
  "applies_when": ["merge", "receipt", "law", "hold", "governance", "stop-class", "failure:hold-bypass-at-landing"],
  "enforcement": "The merge-protocol watch reads open holds at landing time and flags any landing over an open HOLD as HOLD-BYPASS-AT-LANDING (dock-STOP class cousin); VERIFY's post-merge scorecard must name the hold's reconciliation state explicitly. Standing remedy owed: the w704 pre-merge hold-check hook ratified so the button itself reads holds.",
  "evidence": [
    "board comment 6357564612 (relay merge-protocol watch 04:40Z, 2026-10-23T04:43:10Z — '#2990 merged over an open independent HOLD (6356956833) on its exact head')",
    "board comment 6357854502 (VERIFY 05:00Z sign-out, 2026-10-23T05:07:02Z — '#2990 STAND 8.0 (card 6357842162; premise UNRECONCILED — its test pins the publisher #2968 docs as the stale Hub overwriter; author's '10 passed' unreproducible, file holds 3 tests)')",
    "shared-state.json director_tick_20261023_0508 escalations: 'HOLD-BYPASS-AT-LANDING: #2990 merged 04:33Z over an open independent HOLD (6356956833) — a STOP-class bypass the machinery did not stop'"
  ]
}
```
