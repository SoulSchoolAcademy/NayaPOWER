# Probe the Door, Don't Walk Through It — Security Probes Stop at Boundary Confirmation

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1751-probe-door-not-through-it
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-20 ~10:17pm PDT the team's security check found 8 user-data tables in Supabase with row-level security switched off and anonymous read/write open — the API answers them. No rows were actually pulled; the verifier stopped at confirming the door is open. Rule: a security probe confirms exposure at the boundary — it never pulls user rows. Boundary confirmation ("the API answers") is sufficient evidence of the vulnerability class; row-pull adds no decision value and creates exposure liability. The director assigned urgent containment to the dock and Naya 3 the same night.

## 🩷 HUMAN NOTE

Hey Shawn — guess what: the team's security check found 8 user-data tables in Supabase with row-level security switched off and anonymous read/write wide open — the API answers anybody, which is maybe not the most intelligent thing for tables holding user data. What I suggest: nothing about this needed your word — the director already assigned urgent containment to the dock and Naya 3 that same night, with the promise to tell you the moment the lock is confirmed on. What I did: filed the durable part as a smart note (SN-1751, CANDIDATE) — the probe discipline: a security probe confirms the exposure at the boundary and never pulls actual user rows. Why: "the door is open" is everything the containment decision needs; pulling rows through the open door adds nothing to the decision and makes the prober a party to the exposure.

## 🟣 CHILD NOTE

You want to check whether your neighbor's front door is locked. You wiggle the handle — it turns, the door swings open. That's your answer: the door is unlocked. You do NOT walk inside and look through their drawers. Wiggling the handle proves the point; going inside just makes you a burglar. Check the lock, never cross the threshold.

## 🔵 GRANDMA NOTE

We ran a security check on our database and found the locks were off on eight tables that hold people's information — anyone on the internet could read and write them. The person doing the check proved this by showing the system answers without a key, then stopped right there — they didn't open anyone's actual records. That's the rule we keep: prove the door is open, don't walk through it. The finding alone was enough to send the fix crew in the same night.

## 🟠 NAYA NOTE

For redteam, security-verification, and live-data audit seats: probe scripts cap at boundary confirmation. Confirm the exposure with the cheapest sufficient evidence — the endpoint answers, the policy check shows RLS off, the anonymous query returns — then stop. Never pull user rows: the containment decision ("8 tables RLS-off, anonymous read/write open → lock it down") needs only the existence proof, and row-pull adds exposure liability with zero decision value. Teeth: every security-probe receipt carries a boundary-attestation line ("rows pulled: 0 — boundary confirmed: <yes/no>"); a probe receipt without it, or a probe that returns user-row payloads, is rejected as a hygiene failure. Same-night containment here went to the dock + Naya 3 with a tell-Shawn-on-lock promise — routing, not verdict, is the probe's whole product.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn1751-probe-door-not-through-it",
  "title": "Probe the door, don't walk through it - security probes stop at boundary confirmation",
  "lesson": "2026-10-20 ~10:17pm PDT: the team's security check found 8 user-data tables in Supabase with row-level security switched off and anonymous read/write open - the API answers them. No rows were actually pulled; the verifier stopped at confirming the door is open. Rule: a security probe confirms exposure at the boundary - it never pulls user rows. Boundary confirmation is sufficient evidence of the vulnerability class; row-pull adds no decision value and creates exposure liability. Director assigned urgent containment to the dock and Naya 3 the same night, with the commitment to tell Shawn the moment the lock is confirmed on; nothing about it needed his word.",
  "applies_when": [["security", "probe"], ["redteam", "live-data"], ["audit", "supabase"]],
  "enforcement": "Security-probe receipt hygiene gate: every security-probe receipt must carry a boundary-attestation line ('rows pulled: 0 - boundary confirmed: <yes/no>'); a probe receipt without the attestation, or any probe that returns actual user-row payloads, is rejected as a hygiene failure. Probe scripts run at the boundary (endpoint-answers / policy-check level) and are written to be incapable of returning row payloads.",
  "evidence": ["Verified extraction 2026-10-21 05:28 UTC (run sirun_b5e18e09c4564318b2fa500a0a027636), claim 57d6ad525e778184be051e9ac1b01b08: '8 user-data tables in Supabase were found with row-level security switched off and anonymous read/write open - the API answers them. No rows were actually pulled; the verifier stopped at confirming the door is open.'", "source: message assistant-msg-e30308cf-e567-3a5e-1e94-cdc225846a9f", "Director action the same night: urgent containment assigned to the dock and Naya 3, with the commitment to tell Shawn the moment the lock is confirmed on"],
  "decision_change": "The probe-design decision 'how deep does the security probe go': probes now cap at boundary confirmation (endpoint answers / RLS-off policy proof) and never pull user rows. Without this note a verifier might reasonably pull rows 'to be sure', adding exposure liability while the containment decision was already fully determined by the boundary evidence.",
  "falsifiability": "Falsified if a class of exposure is shown that boundary confirmation cannot detect but row-pull can - in which case the rule gains an explicit, scoped exception (documented authorization for that class), not a repeal. Until such a class is demonstrated, the boundary cap holds.",
  "mechanism": "Decision-value parity: the containment decision needs only the existence proof of the exposure (tables RLS-off + anonymous write confirmed). Row payloads are not an input to any containment step - they change no lock-down action - so their marginal value is zero while their liability cost (handling real user data, becoming a party to the exposure) is nonzero. The probe's product is the routing (who contains, by when), not the verdict on the data.",
  "captured_date": "2026-10-21",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/VERIFICATION/ADVERSARIAL-VERIFICATION"
}
```
