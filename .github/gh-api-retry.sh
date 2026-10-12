#!/usr/bin/env bash
# .github/gh-api-retry.sh — bounded retry wrapper for `gh api` READ calls.
#
# Why this exists: the Governed Production Promotion workflow died on a single
# transient `HTTP 403: API rate limit exceeded` from one `gh api` call
# (run 38185784665, job 114607678497, 2026-10-11). Under `set -euo pipefail`
# a flaked call kills the whole promotion chain — a false red.
#
# Contract:
#   * Retries ONLY transient signals:
#       - GitHub rate limits: HTTP 403 with "rate limit" wording, HTTP 429
#       - Server errors: HTTP 5xx
#       - Transport failures: dial/connect/TLS/DNS/timeout
#   * Genuine failures (401 bad credentials, 404 not found, 403 permission
#     errors WITHOUT rate-limit wording, 422 validation, anything else) are
#     surfaced IMMEDIATELY with gh's original stderr and exit code — never
#     retried, never masked. Fail-closed behavior is preserved.
#   * Stdout passes through byte-identical (it is never captured/re-printed),
#     so `gh_api_retry ... > file.json` and `x="$(gh_api_retry ...)"` behave
#     exactly like the raw `gh api` call on success.
#
# Bounds: GH_API_RETRY_ATTEMPTS (default 5), GH_API_RETRY_BASE_DELAY
# (default 5s). Backoff is base * 2^(n-1) plus up to 4s jitter; set
# GH_API_RETRY_NO_JITTER=1 for deterministic timing (tests).
# GH_API_RETRY_ATTEMPTS=1 disables retry entirely (escape hatch).
#
# Usage in a workflow step (after actions/checkout):
#   source "${GITHUB_WORKSPACE:-.}/.github/gh-api-retry.sh"
#   blocker_state="$(gh_api_retry "repos/$REPO/issues/978" --jq .state)"

# _gh_api_retry_transient <lowercased-stderr> -> 0 if the failure looks
# transient (safe to retry), 1 otherwise. Matching is deliberately narrow:
# a 403 is transient ONLY when it carries rate-limit wording — a permission
# 403 must fail fast.
_gh_api_retry_transient() {
  case "$1" in
    *rate\ limit* | *http\ 429* | *http\ 5[0-9][0-9]*)
      return 0
      ;;
    *connection\ refused* | *connection\ reset* | *connection\ timed\ out* | \
      *i\/o\ timeout* | *no\ such\ host* | *network\ is\ unreachable* | \
      *tls\ handshake\ timeout* | *dial\ tcp* | *temporary\ failure*)
      return 0
      ;;
  esac
  return 1
}

# gh_api_retry <gh api args...> — run `gh api` with bounded transient retry.
gh_api_retry() {
  local max_attempts="${GH_API_RETRY_ATTEMPTS:-5}"
  local base_delay="${GH_API_RETRY_BASE_DELAY:-5}"
  local attempt=1 err rc body lower delay
  while :; do
    err="$(mktemp)" || return 1
    # Stdout streams straight through (byte-identical to raw `gh api`);
    # only stderr is captured, for the transient check.
    # NOTE: gh's exit code MUST be captured inside the `else` branch. `$?`
    # after the whole `if` is 0 when the condition is false with no `else`
    # taken yet — reading it there silently converts failures into success.
    if gh api "$@" 2>"$err"; then
      rm -f "$err"
      return 0
    else
      rc=$?
    fi
    body="$(cat "$err")"
    rm -f "$err"
    lower="$(printf '%s' "$body" | tr '[:upper:]' '[:lower:]')"
    if [ "$attempt" -lt "$max_attempts" ] && _gh_api_retry_transient "$lower"; then
      delay="$((base_delay * (1 << (attempt - 1))))"
      if [ -z "${GH_API_RETRY_NO_JITTER:-}" ]; then
        delay="$((delay + RANDOM % 5))"
      fi
      printf '::warning title=gh api transient failure (attempt %s/%s)::retrying in %ss: %s\n' \
        "$attempt" "$max_attempts" "$delay" "$(printf '%s' "$body" | head -c 200)" >&2
      sleep "$delay"
      attempt="$((attempt + 1))"
      continue
    fi
    # Genuine failure, or retries exhausted: surface gh's original stderr
    # and exit code. The caller's fail-closed path is preserved.
    printf '%s\n' "$body" >&2
    return "$rc"
  done
}
