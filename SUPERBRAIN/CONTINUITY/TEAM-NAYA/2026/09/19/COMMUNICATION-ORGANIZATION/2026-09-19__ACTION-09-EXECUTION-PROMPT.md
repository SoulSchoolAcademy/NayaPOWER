# ACTION 09 — CLOUDFLARE SOURCE / BUILD / RUNTIME PARITY

## MISSION

Prove that the canonical Hub source containing the new Communication + Organization runtime is the artifact actually served by the canonical Cloudflare runtime.

## EXACT EXECUTION

1. Identify the canonical Cloudflare release workflow.
2. Confirm its trigger includes `assistant-runtime.js`.
3. Confirm its source is `main`.
4. Confirm its build copies the exact Hub and runtime files.
5. Confirm deployed worker/route identity.
6. Confirm live HTML hash equals source HTML hash.
7. Confirm live `assistant-runtime.js` hash equals source runtime hash.
8. Confirm deployed runtime contains the new adapters:
   - `nayanet_join_space`
   - `nayanet_save_connection`
   - `nayanet_create_smart_list`
   - `nayanet-smart-mail`
9. Confirm the old Connections→Spaces bridge is replaced by Connections→Your Connections.
10. Confirm no cache/stale marker is serving the prior runtime.
11. Record exact workflow run, job, artifact, route and parity evidence.
12. Update Team Naya and the master directive.
13. Then immediately return to Action 08 browser proof.

## HARD RULES

No Cloudflare parity claim from GitHub commit alone. No cached HTML assumption. No browser success claim without actual runtime observation.

## REQUIRED REPORT

DONE / PROOF / NOT PROVEN / DECISION / BLOCKERS / NEXT.

NEXT must be a complete cold-start successor directive.
