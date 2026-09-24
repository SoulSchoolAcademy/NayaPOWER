# GITHUB SENDER CODA 3 — P5 INTEGRATION / RUNTIME PARITY

Date: 2026-09-24
Status: PARTIALLY VERIFIED / BLOCKED_EXTERNAL_CONFIGURATION

## Finding

The integration audit caught a real production defect in the owner resolver: PostgreSQL does not provide min(uuid). The resolver therefore could not reach its intended missing-binding denial path.

## Repair

Production resolver now uses (array_agg(sp.member_id))[1], preserving the existing count-based ambiguity checks and service-role-only boundary.

Production verification:
- Unknown installation/repository => GITHUB_BINDING_NOT_FOUND.
- service_role execute => true.
- authenticated execute => false.
- SECURITY DEFINER/search_path public preserved.

## Runtime parity

- Main HEAD: 79c0eeacaaf023ea2e2fbad1bfa65957b52522c5
- Webhook source SHA: 61a6fcce188cc617d35c6b06bd2444dde4c9b965
- Webhook production version: 4
- Webhook production digest: 36f89f5c9beadcf77298ee0ccf8705a8e836cbdd4813ef1c70282d40bd366072
- Webhook source/runtime exact content match: PASS
- Hub release run: 36065304937 SUCCESS at e4bb2c20aec1e5d2811bf2030da7d4bb85365255
- Hub source unchanged through current HEAD.
- Current live Hub SHA-256: 798b1fb67d5d88815b90be9523b0da778e802ffa86031e8eff2e69a218a46184
- Current main Hub source SHA-256: 798b1fb67d5d88815b90be9523b0da778e802ffa86031e8eff2e69a218a46184
- Hub source/runtime exact bytes: PASS

## Hub receiver contract

The Smart Feed uses NayaAssistantRuntime.smartFeed(), which invokes the production naya-smart-feed function. Personal/activity reads require authenticated identity and are owner-scoped; collective reads require explicit publication consent. The Hub therefore consumes canonical runtime output rather than fabricated static feed data.

## External sender state

Production Smart Connect currently has zero github_app participation rows. Repository inspection found no caller of nayanet_smart_connect_github_bind and no GitHub App installation identity/configuration in source.

The final sender loop therefore remains blocked by two genuine external configuration boundaries:

1. GITHUB_WEBHOOK_SECRET must be configured through the authorized production secret-management boundary.
2. A real GitHub App must be installed and its installation + selected repository bound to the authenticated owner's existing github_app participation.

No secret was requested, exposed, committed, or logged.

## Architecture preserved

GitHub → signed webhook → owner resolver → canonical cognition persistence → Smart Feed runtime → Hub.

No second receiver, intelligence store, connection store, or authority model was added.

## Single next action

Through the authorized external GitHub/Supabase administration boundary, install/configure the real GitHub App and production webhook secret, then create the authenticated owner's existing Smart Connect github_app participation binding for the selected repository. Do not paste or expose any secret in chat.
