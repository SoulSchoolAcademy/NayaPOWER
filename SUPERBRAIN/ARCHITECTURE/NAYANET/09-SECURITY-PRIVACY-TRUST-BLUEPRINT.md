# 🔱 NAYANET — SECURITY / PRIVACY / TRUST BLUEPRINT

## 1. Core principle

Privacy is an architectural property, not marketing copy.

## 2. Data minimization

Collect only what is necessary for the requested capability.

Initial identity entry should be minimal.

Do not require email merely because it is convenient if the product can safely defer it.

## 3. Authentication

A lightweight initial account experience must not be confused with security authentication.

Before security-sensitive operations, establish a durable authenticated session.

Preferred future integration: Supabase Auth or another explicit identity provider behind the application boundary.

## 4. Authorization

Every privileged operation must evaluate:

- authenticated actor;
- resource ownership;
- requested scope;
- consent;
- current session;
- provider permissions;
- policy.

## 5. GitHub

Use GitHub Apps for production repository integration where possible.

Request minimum permissions and selected repositories.

Never request a user's GitHub password.

Never place GitHub credentials in static client code.

## 6. Superbrain

Default state is private.

No contribution occurs without explicit user authorization.

## 7. Collective

Collective publication requires:

- contribution intent;
- privacy transformation;
- quality validation;
- human review where required;
- publication policy.

## 8. Anonymous communication

An alias may be shown to other participants.

The platform still maintains internal account integrity necessary for safety and governance.

## 9. Threat model

Plan for:

- account takeover;
- session theft;
- malicious prompts;
- prompt injection through connected sources;
- data exfiltration attempts;
- malicious contributions;
- impersonation;
- spam;
- harassment;
- malicious links;
- iframe message spoofing;
- compromised integrations.

## 10. iframe messaging

If `postMessage` is introduced:

- strict target origin;
- strict accepted origin allowlist;
- schema validation;
- versioned messages;
- no sensitive data in uncontrolled messages;
- replay/idempotency strategy for actions.

## 11. Trust UX

Users must understand:

- what Naya knows;
- what Naya can access;
- what is private;
- what is shared;
- what will happen next;
- how to revoke access.

## 12. Security law

> **Never trade user sovereignty for convenience without an explicit, informed choice.**
