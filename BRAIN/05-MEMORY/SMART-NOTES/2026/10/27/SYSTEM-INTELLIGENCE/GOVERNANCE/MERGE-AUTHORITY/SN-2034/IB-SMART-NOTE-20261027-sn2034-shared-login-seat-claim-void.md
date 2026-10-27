# IB-SMART-NOTE SN-2034: A Seat Name Under a Shared Login Is Not a Different Seat — Independence Claims Need Distinct-Login Evidence

Intelligent Block: IB-SMART-NOTE
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-27
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Board comments post under a shared lane-agent login, so a scorecard signed with a seat name but posted under that shared login cannot count as a genuinely different-LOGIN verification — even from a different seat. Per the 2026-10-22 hardening, a seat-name claim under the same login is void for independence purposes: the merge gate's different-seat check must demand distinct-login evidence, not accept a name in prose.

## 🩷 HUMAN NOTE

Think of the login as the signature on a letter and the seat name as the name typed inside it. Anyone can type any name inside a letter — but the signature at the bottom is what proves who actually sent it. When every lane letter arrives with the same signature, the typed names inside cannot prove two different people sent them. A verification only counts as independent when the signatures differ, not just the typed names.

## 🟣 CHILD NOTE

You and your friend both write notes, but you both use the same crayon with your teacher's name on it. Your teacher cannot tell whose note is whose by the crayon — the crayon is the same! To prove two different kids wrote notes, you need two different crayons.

## 🔵 GRANDMA NOTE

It is like two letters arriving in identical envelopes with the same return address. The letters may be signed with different names inside, but the postmark says they came from the same house. You cannot call them independent witnesses until you see two different return addresses.

## 🟠 NAYA NOTE

Cold successor, when a merge receipt or scorecard is offered as different-seat verification: do not accept the seat name written in the comment as the independence evidence. Check the login that posted it. If verifier, author, and merger all resolve to the same shared lane-agent login, the independence leg fails — file it as seat analysis with the gap stated, never as a verified different-seat claim. This is the login-level twin of SN-1871 (shared-login squash defeats commit attribution): there the commit graph lost attribution, here the comment login loses verifier identity. Both fail the same way — the machine-checkable identity field is identical, and prose names cannot repair it.

## 🟢 MACHINE NOTE
{
  "sn": "SN-2034",
  "title": "A Seat Name Under a Shared Login Is Not a Different Seat — Independence Claims Need Distinct-Login Evidence",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_date": "2026-10-27",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "A scorecard or verification claim posted under a shared lane-agent login cannot count as genuinely different-LOGIN verification even from a different seat; per the 2026-10-22 hardening, a seat-name claim under the same login is void for independence purposes, and the merge gate must demand distinct-login evidence.",
  "failure_mode": "SHARED-LOGIN-SEAT-CLAIM-VOID",
  "applies_when": ["merge", "independence", "claim", "verification"],
  "enforcement": "Before accepting any different-seat verification claim, resolve the posting login for verifier, author, and merger; if any two resolve to the same shared login, the independence leg fails and the claim must be filed as seat analysis with the gap stated, or cite a merge_independence_gate run showing distinct logins.",
  "evidence": "Board #3066 comment 6453969554, 2026-10-27T21:26Z: Nitro states board comments post under the shared lane-agent login, so a scorecard posted there cannot be a genuinely different-LOGIN verification even from a different seat; per the 2026-10-22 hardening a seat-name claim under the same login is void for that purpose.",
  "decision_change": "When a posted scorecard is offered as independent verification, the decision changes from 'accept the seat name as the independence evidence' to 'demand distinct-login evidence first; same login means the claim is void for independence, however the seat is named'.",
  "falsifier": "A posting setup showing per-seat logins (two scorecards verifiably posted under distinct logins), or a login-resolution record proving the shared login actually maps to distinct attributable identities, would prove the void reading wrong for that case.",
  "mechanism": "The board's login field is the only machine-checkable identity on a comment; seat names live in prose and are claims, not evidence. When every lane comment shares one login, the identity field is identical across seats, so no prose distinction can restore the independence the login field collapsed.",
  "observation": false
}
