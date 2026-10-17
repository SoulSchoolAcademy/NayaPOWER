# 37 — GITHUB ACCESS: the two identities

## ESSENCE
Two identities, right tool each time. Keys live on machines — never in chat, never in history. Tokens are minted short-lived, piped into the work, and never printed, logged, or stored.

## WHAT IT IS
The team's GitHub access system for worker machines. A GitHub App ("NayaPOWER Lane Agent") mints 1-hour installation tokens from a machine-local private key; a stored PAT covers everything else. Three scripts in `~/workspace/custom-connectors/custom.legacy-github/bin/`:

- `gh-app-token` — mints the installation token (cached `~/.cache/nayapower/gh-app-token.json`, chmod 600; auto-refreshed when <120s of life remains). Pipe it — never print, log, or store it.
- `gh-app-api` — REST client on the App identity. Lane-attributed writes, `.github/workflows/**` commits (Contents-write 403s there on other credentials), read-only Actions access.
- `gh-api` — REST client on the stored PAT (`custom.github` credential). Everything else.

## WHAT IT DOES
Gives a fresh machine the team's write path without a human in the loop per action: app-minted tokens for governed writes, PAT for the rest. Reads never needed approval; this system is about writes done right.

## WHY IT MATTERS
This manual exists because a fresh box had nothing: no scripts, no key, no PAT — and the setup knowledge was nowhere in the repo (four searches, zero hits). A Naya who cannot reach GitHub cannot receipt, cannot merge, cannot prove. Tribal setup knowledge is a single point of failure with a human face. This page removes it.

## THE RIGHT WAY
1. **Get the three scripts** — `gh-app-token`, `gh-app-api`, `gh-api` — into `~/workspace/custom-connectors/custom.legacy-github/bin/`, `chmod +x`. **Read them before trusting them:** no embedded keys, tokens, or secrets; every network call pinned to `api.github.com`. Clean scripts are checkable scripts.
2. **Get the private key — NEVER via chat.** A `.pem` in a message lives in history forever. Recommended: generate a **second** private key in the GitHub App settings for the new box — Apps support multiple keys, each machine independently revocable; if the box is ever compromised, revoke its key without touching the team's. Alternative: move the existing key via a channel you control, outside chat.
3. **Place it once.** `mkdir -p ~/.config/nayapower`, then **move** (not copy) the `.pem` to `~/.config/nayapower/github-app.pem`. `chmod 600`. `ls -la` must show `-rw-------` and nothing else. After this, exactly one copy exists: that path, 600, nowhere else.
4. **Verify the mint.** Run `bin/gh-app-token`. It must print a token starting with `ghs_`. Capture it into a variable, check the prefix programmatically, `unset` it — the value never touches a log. If it says "app PEM not found," the path is wrong: stop, fix the path, do not proceed.
5. **Verify the full flow.** `bin/gh-app-api GET /repos/{OWNER}/{REPO}` must return the repo's JSON. That proves the whole chain: key → JWT → installation token → authenticated API, end to end.
6. **Wire the PAT identity.** `gh-api` needs `export PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin` (that's where `dynamic_credentials` lives) and the `custom.github` credential in the secure vault — a fresh box re-runs the GitHub connect flow once. Large bodies: write JSON to a file, pass `@file` (ARG_MAX kills inline bodies).
7. **Push with the token — URL form ONLY.** The Bearer-header form fails here:
   `TOK=$(bin/gh-app-token); git push "https://x-access-token:${TOK}@github.com/{OWNER}/{REPO}.git" <branch>; unset TOK`
   Mint fresh per push; unset right after.
8. **Budget.** 10 API calls per worker per mission. Local first, cheap check first. A 401/403 is a question about the REQUEST before the key — verify the credential was attached before asking for a reconnect.

## THE WRONG WAY
- Pasting a `.pem` or token into chat, a doc, or a log — history is forever, revocation is paperwork.
- Printing a minted token to "check it" — check the `ghs_` prefix programmatically; eyes never needed.
- Copying the key instead of moving it — stray copies are future breaches. Move. Verify. Sweep.
- Using the Bearer-header form for push — it fails here; URL form only.
- Inlining a large JSON body on the command line — ARG_MAX will kill it; `@file` always.
- Reading a 401/403 as "the key is bad" — first verify the credential was actually attached to the request.

## VERIFY
Three yes/no checks, in order. All three must be yes:
1. Token mints (`ghs_` prefix confirmed, value never printed)?
2. `gh-app-api GET /repos/{OWNER}/{REPO}` returns the repo JSON?
3. Exactly one key copy exists at `~/.config/nayapower/github-app.pem`, `-rw-------`?

Report back those three. Anything else is commentary.
