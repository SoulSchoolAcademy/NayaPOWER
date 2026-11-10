# Deploy the retrieval engine — one-tap prep (NOT deployed)
Filed 2026-11-10, Supabase master first pass. Status: PREPARED. Nothing
below has been run. Shawn's tap fires it; no seat deploys it.

## Title: The Retrieval Engine, Ready to Fire
## Subtitle: The code is complete and tested — three prerequisites stand between it and live
## Nutshell: Ask Naya and smart search have nothing to query today because
the retrieval engine was never deployed. This file is the one tap: the exact
commands, the exact checks, and the exact proof it worked — plus the three
things that must be true first.

## What it is, in plain words
`nayanet-intelligence-retrieve` is the search engine of NayaNET: a caller
sends a free-text question, it returns ranked Intelligent Blocks (keyword
match + applicability + truth-state weighting + recency). Without it, Ask
Naya, smart search, and every intelligence query path have nothing to call.
The code is complete in the repo (`supabase/functions/nayanet-intelligence-retrieve/`,
`index.ts` + `retrieve.ts` + `retrieve_applicability.ts`, last touched
2026-10-20) with tests (`retrieve_applicability.test.ts`). A live call to
its endpoint today returns `NOT_FOUND` — it does not exist yet.

## The three prerequisites (all must be true before the tap)
1. **Secret: `SUPABASE_SERVICE_ROLE_KEY` must be set on the project.**
   The function's code reads it at start (`adminClient()` throws
   `SERVER_AUTH_CONFIG_MISSING` without it). Only Shawn holds the service
   key. Set it in the Supabase dashboard (Edge Functions → Secrets) or:
   `supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<service key> --project-ref dahisasgpfvziswqvmvm`
   Never paste the key into chat, a file, or a log.
2. **Config entry: the function is not in `supabase/config.toml`.**
   The 13 functions with the platform auth check off are all listed there
   with `verify_jwt = false`. Retrieval checks identity inside its own
   code (GitHub OIDC, same pattern as the governed runtimes), so it needs
   the same entry. Add to `supabase/config.toml` and file to main:
   ```toml
   [functions.nayanet-intelligence-retrieve]
   verify_jwt = false
   ```
3. **widget-39a1bf91 is still pending.** The brief names it as pending;
   no record in the repo or memory found in this pass says what it is or
   whether it blocks the deploy. It is named here so it is not lost: ask
   before firing if it is meant to gate this deploy.

## The one tap (his hand)
```bash
supabase functions deploy nayanet-intelligence-retrieve --project-ref dahisasgpfvziswqvmvm
```
Notes: the governed deploy workflow (`governed-supabase-production-deploy.yml`)
deploys a FIXED list of runtimes and does NOT include retrieval, so the
workflow path cannot fire this — the CLI command above is the tap. The
deploy needs a Supabase login with deploy rights on project
`dahisasgpfvziswqvmvm` (supabase-red-cable, production).

## Proof it worked (run right after, before reporting done)
1. List functions: the Management API list must now show
   `nayanet-intelligence-retrieve` as ACTIVE (22 functions, was 21).
2. Probe the endpoint WITHOUT credentials:
   `curl https://dahisasgpfvziswqvmvm.supabase.co/functions/v1/nayanet-intelligence-retrieve`
   must NO LONGER return `NOT_FOUND`. It must return an auth error
   (`RUNTIME_IDENTITY_REQUIRED` — the function demands a GitHub OIDC
   bearer token). An auth error IS the proof: the function exists and
   guards its own door. A 200 without credentials would be a defect.
3. Run the cold-successor proof workflow (`live-supabase-runtime-proof.yml`)
   — it is one of the four workflows the function trusts — and confirm a
   real query returns ranked blocks.

## What it unblocks
Ask Naya, smart search, and every intelligence query path. It closes the
audit's −1 (the retrieval gap) and moves the score from 6 toward 10.
