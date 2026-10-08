# IB-SMART-NOTE-20261006-sn0496-agent-capture-must-present-a-real-user-jwt-receiver-stays-byte-identical

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20261006-sn0496-agent-capture-must-present-a-real-user-jwt-receiver-stays-byte-identical |
| Smart Note | SN-0496 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-06 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

The CAPTURE lane resolved Blocker B1 (agent runtimes cannot capture through the canonical Receiver) to the gate without weakening auth. The Receiver (`v7-smart-note-canonical`) requires an `Authorization` header plus `supabase.auth.getUser()` — a user JWT no Naya runtime holds. The tempting shortcut — extending the Receiver to accept GitHub-OIDC directly — was verified structurally unsound on live code: `nayanet_record_cognition_event` is `security invoker` and raises `AUTH_REQUIRED` on null `auth.uid()`; `nayanet_cognition_events.user_id` carries an `auth.users` foreign key; RLS is owner-scoped. Any correct path MUST present a real user JWT. So the Receiver stays **byte-identical**; instead a governed workflow (`.github/workflows/nayanet-agent-capture.yml`) signs in as a dedicated `naya-runtime` auth user using credentials held in repo secrets — Naya runtimes never hold the credential — and calls the unchanged Receiver. Branch `naya/capture-agent-invocation-path` (commit `06010d1d`), with spec + workflow + Naya-side helper `scripts/naya-runtime-capture.sh`, all validated. Lane at 4/10, ready-for-proof; behavioral proof waits on Shawn's three steps: create the `naya-runtime` auth user, set 4 repo secrets, merge the PR. A correct integration path hardens the mechanism without touching the canonical surface; a second memory system or a weakened auth check was never on the table.

## HUMAN NOTE

Shawn — the capture seat hit a wall today: our agent runtimes couldn't save Smart Notes into the brain because the doorway requires a real human login token, which no agent holds. The easy fix would've been to widen the doorway — but that would've weakened the lock, so he checked the actual machinery and proved it won't work anyway (the database checks for a real user ID in three different places). The answer: keep the doorway exactly as it is, and have a governed workflow — a trusted process that holds the key, not the agents — sign in as a dedicated "naya-runtime" user to make the capture on the agent's behalf. The key lives in repo secrets, never in any agent's hands. It's a clean design: the brain's front door never changes, agents never touch credentials, and the one human-gated step is exactly named — create the user, set four secrets, merge. No shortcuts, no second memory.

## CHILD NOTE

The treasure room door needs a real key, and you don't have one — so you can't just make the door looser, because then anyone could get in. The smart move: the grown-up who owns the key (a special helper, not you) unlocks the door and puts your drawing in the treasure room for you. The door stays exactly as strong as before, you never hold the key, and the helper only opens it the one proper way.

## GRANDMA NOTE

The bank vault needs the manager's key, and the staff don't carry one — you don't solve that by leaving the vault unlocked. The manager unlocks it himself, deposits the customer's papers, and keeps the key on his own ring. The vault's lock is never changed, nobody else gets a copy, and there's one clear procedure anyone can follow. Security kept, problem solved.

## NAYA NOTE

Note to future me: when an agent runtime needs to act through a user-authenticated path (the Receiver, `security invoker` RPCs, owner-scoped RLS), do NOT weaken the check or bolt on a second auth surface. Verify the constraints on live code first — here, null `auth.uid()` raises, the user_id FK requires a real `auth.users` row, RLS is owner-scoped — then design the governed path: a dedicated identity (here, `naya-runtime` auth user) whose credential lives in repo secrets and is presented by a governed workflow, never by the agent runtime. The canonical surface stays byte-identical. The human gate is explicit: create the identity, set the secrets, merge.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261006-sn0496-agent-capture-must-present-a-real-user-jwt-receiver-stays-byte-identical",
  "smart_note": "SN-0496",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "Agent capture through the canonical Receiver requires a real user JWT; the correct path is a governed workflow presenting a dedicated identity's credential from repo secrets, with the Receiver byte-identical.",
  "evidence": {
    "board": "#1354",
    "comments": ["6026679478"],
    "branch": "naya/capture-agent-invocation-path",
    "commit": "06010d1d",
    "workflow": ".github/workflows/nayanet-agent-capture.yml",
    "helper": "scripts/naya-runtime-capture.sh",
    "lane_score": "4/10 ready-for-proof"
  },
  "verified_constraints": [
    "nayanet_record_cognition_event is security invoker; raises AUTH_REQUIRED on null auth.uid()",
    "nayanet_cognition_events.user_id carries an auth.users FK",
    "RLS is owner-scoped",
    "Extending the Receiver to accept GitHub-OIDC directly is structurally unsound"
  ],
  "design_rules": [
    "The canonical surface stays byte-identical.",
    "A dedicated auth identity (naya-runtime) is presented by a governed workflow, never by an agent runtime.",
    "The credential lives in repo secrets; Naya runtimes never hold it.",
    "No second memory system; no weakened auth."
  ],
  "human_gate": "Create the naya-runtime auth user, set 4 repo secrets, merge the PR — then the behavioral proof runs."
}
```
