# A 401 Is Not a Key Problem Until You Prove It Is — the Credential-Layer Diagnostic

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0498-credential-layer-diagnostic
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-06 Naya 5 hit Supabase 401s and the lanes nearly went hunting for a different key. The actual diagnosis: the vault credential resolves fine — the seat's sandbox calls carried the surrogate placeholder instead of the resolved credential because the Supabase connector's sandbox release hadn't propagated (unlike GitHub's, which had). Two rules were earned: (1) the skill CLI is the ONLY sanctioned request path — it calls the surrogate-resolution path, so hand-rolled requests that 401 prove nothing about the key; (2) when correct CLI use still 401s, the fault is credential *resolution* (sandbox release), not key type — escalate once, never retry-loop, never ask the human for raw keys. A companion trap was documented in the same thread: the team holds TWO different credential paths — the Supabase Management API credential (vault, direct Postgres as a read-only user, no PostgREST/RLS involved) vs the anon/service_role keys. Diagnose which path a failing call is on before proposing a key change, or you'll fix the wrong layer.

## 🩷 HUMAN NOTE

When your team's connection breaks, the instinct is "we must have the wrong key." Resist it. The key is usually fine — the question is whether the system actually delivered the key where it was needed. A smart team diagnoses the delivery path before changing the key, because changing a good key breaks what worked yesterday.

## 🟣 CHILD NOTE

If the door won't open, first check whether your key is actually in your hand — not whether you need a different key. And never yell at the key-holder to hand you a copy; that's how keys get stolen.

## 🔵 GRANDMA NOTE

When something won't connect, don't run out and buy a new lock. First make sure the key you already have is actually being used. And never hand out copies of your keys to fix a problem — fix the way they're handed out instead.

## 🟠 NAYA NOTE

401s lie about which layer failed. Layer order for credential failures: (1) request path — was it the sanctioned CLI (the only path that resolves the surrogate)? A hand-rolled request 401 proves nothing about the credential. (2) credential resolution — does the seat's sandbox release actually deliver the resolved credential (vs a placeholder)? Correct CLI + 401 = resolution fault → escalate once, don't retry, don't change key types. (3) key identity — only here, and only after naming which of the two paths (Management API credential vs anon/service_role) the failing call actually uses. Changing the key before step 2 is diagnosed is fixing the wrong layer — and asking the human for a raw key is never the fix; the vault path is the only path.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "diagnose_credential_failure_by_layer_before_changing_key",
  "layer_1_request_path": "sanctioned_skill_CLI_only_holds_surrogate_resolution_hand_rolled_requests_401_tell_nothing",
  "layer_2_credential_resolution": "sandbox_release_must_propagate_to_seat_correct_CLI_plus_401_is_resolution_fault_escalate_once_never_retry_loop",
  "layer_3_key_identity": "only_after_layers_1_2_passed_name_which_of_two_paths_failed_management_API_vault_credential_vs_anon_service_role",
  "hard_rule": "never_request_raw_keys_from_human_vault_path_is_only_path",
  "anti_pattern": "hunting_for_a_different_key_when_the_release_is_the_fault",
  "evidence": "NayaPOWER#1354 comments 6026821218 6026884889 (Naya 4, 2026-10-06), Supabase connector sandbox-release gap"
}
~~~
