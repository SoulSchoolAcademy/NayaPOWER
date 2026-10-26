Intelligent Block: SN-2015
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
RLS enabled is not private. On 2026-10-26, independent verification found anonymous SELECT, INSERT, UPDATE, and DELETE allowed on both project-intelligence tables, with open policy conditions — even though row-level security was enabled on them. A feed may therefore be called private only after two things are attached to the claim: the actual policy expressions for every table behind the feed, and witnessed negative tests in which an outsider's anonymous attempts fail. Until then, "RLS on" proves nothing about privacy, and any permission change itself stays behind Shawn's explicit authority — this note changes no permission, it states the verification rule.

## 🩷 HUMAN NOTE
A locked door with the key taped to it is not a locked door. That is what happened here: the database had its security switch turned on, but the rules underneath it said "any anonymous visitor may read, write, change, and delete." Anyone checking only the switch would have called the data private while it was open. The rule from now on: before you call any feed private, read the actual rules underneath, and then prove an outsider gets refused — in person, on the record. A claim without that proof is not a claim, it is a guess.

## 🟣 CHILD NOTE
Imagine a clubhouse with a big sign that says "Members Only" — but the door is wide open and anyone can walk in, take toys, or move them around. The sign does not keep anyone out; only a door that actually stays shut does. So before you say "this clubhouse is private," you have to try the door as a stranger and show that it really stays shut.

## 🔵 GRANDMA NOTE
Dear, it is like a medicine cabinet with a lock on the front but the back panel missing — anyone who walks around the side can reach straight in. The lock being there is not the same as the cabinet being safe. You have to check the whole box, and then have someone who is not family try to open it and fail, before you tell anyone the medicine is put away safe. Same here, with the computer's private rooms.

## 🟠 NAYA NOTE
Cold successor, this is a posture-measurement rule, not a one-day finding. Security posture is a dated measurement, never a permanent property: a 2026-10-15 audit found authenticated-only policies and zero anonymous policies, and by 2026-10-26 the same surface carried open anonymous policies on both PI tables. Do not inherit a privacy claim from an old audit, a schema flag, or a table label. The only privacy evidence that counts is current: the policy expressions as they read today, plus negative tests witnessed in the outsider role for every command the claim covers. And hold the boundary: this note authorizes no permission change — production permission changes stay behind Shawn's explicit authority. The note tells you how to verify; it never tells you to re-lock anything yourself.

## 🟢 MACHINE NOTE
{
  "applies_when": ["privacy", "supabase", "rls", "feed", "privacy-gate"],
  "enforcement": "Privacy-gate check: before any feed is declared private or member-only, the declaring seat must attach (1) the policy-expression read for every table behind the feed and (2) witnessed anonymous negative tests in the outsider role covering SELECT, INSERT, UPDATE, and DELETE; a declaration without both is void and must be retracted in the same slot, as the 2026-10-26 privacy gate required. Production permission changes themselves stay behind Shawn's explicit authority and are never made by the verifying seat.",
  "evidence": "Live board #3066 comment 6428206476 (2026-10-26T21:52:14Z, Tree/Power+Security): non-owner-scoped anonymous SELECT access condition across project/work and private-note tables; RLS enabled alone does not prove data private. Comment 6428397499 (2026-10-26T22:03:03Z, Naya Nitro Narzan, independent verification): anon SELECT/INSERT/UPDATE/DELETE on BOTH PI tables (work_items, project_intel_items), qual=true/with_check=true — anyone with the public anon key can read AND write AND delete every PI row. Comment 6429388876 (2026-10-26T23:03:13Z, Nitro): privacy gate unchanged; anon policies on both tables allow all four commands with open conditions; production permission changes stay behind Shawn explicit authority.",
  "decision_change": "Whether to declare a Personal, Business, Space, or member-only feed private: declare it only when current policy expressions plus witnessed outsider negative tests support it; never from RLS-enabled status, a table label, or a prior audit alone.",
  "falsifiability": "This rule would be wrong if, on a current policy-expression read, the anonymous policies were shown to be owner-scoped or absent, and witnessed outsider attempts for all four commands were refused — then the tables would be private despite RLS being merely 'enabled', and the failure would be in the 2026-10-26 measurement, not the rule. The 2026-10-26 measurements pass the opposite way on both tables.",
  "mechanism": "Row-level security enforces policy predicates per command, not the enabled flag: an anonymous policy with an open condition (qual=true, with_check=true) authorizes that command for any anonymous caller, so the enabled flag and the effective access are independent facts. A label like 'private' describes intent; only predicates plus negative tests describe access.",
  "cousins": "SN-2011 (a present artifact is not proof — applied to receipts; this is the same shape applied to a security flag). Contrast case: the 2026-10-15 RLS audit posture (authenticated-only policies, zero anon policies) — posture is a dated measurement, and it changed."
}
