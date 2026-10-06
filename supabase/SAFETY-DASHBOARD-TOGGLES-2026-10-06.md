# Safety Remediation — Dashboard Toggles (Manual Steps for Shawn)

These two fixes cannot be done via SQL migration — they require dashboard config changes.
They are part of the 27-WARN remediation plan (2026-10-06).

## Toggle 1: Enable leaked password protection (fixes 1 WARN)

**Path:** Supabase Dashboard → Authentication → Policies → "Leaked password protection"
**Action:** Enable the toggle.
**Effect:** Supabase will reject passwords that have appeared in data breaches (via HaveIBeenPwned).
**Risk:** None. Only affects new password choices. No existing logins break.
**Reversible:** Yes, toggle off.

## Toggle 2: Disable anonymous sign-ins (fixes 18 WARNs)

**Path:** Supabase Dashboard → Authentication → Providers → "Anonymous sign-ins"
**Action:** Disable the toggle.
**Effect:** All 18 WARNs disappear. The `authenticated` role will only include users with real accounts (email/OAuth), not anonymous click-to-sign-in users.
**Risk:** LOW. 7,460 anonymous accounts exist, 0 active in the last 7 days. If any flow depends on creating anonymous users (testing, demo), it stops working.
**Reversible:** Yes, toggle back on. The 7,460 accounts are not deleted, just unable to sign in while disabled.
**Shawn's call:** Required. This changes who can access the system.

## Verification after toggles

Run a fresh Security Advisor pull. Expected:
- After Toggle 1: 27 → 26 WARNs
- After Toggle 2: 26 → 8 WARNs
- After the SQL migration (PR #XXXX): 8 → 6 WARNs (trigger + evolve fixed)
- Remaining 6: 5 intentional API functions (acknowledge) + 1 intelligence_commit (Shawn's call)

**Target state (all approved):** 27 → 0 WARNs.
