import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claim_check_addon as cc

def t(name, cond, detail=""):
    # Fail-fast: under pytest a failure raises at collection (honest red);
    # under direct execution the traceback names the failed case.
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail else ""))
    assert cond, f"FAIL {name} — {detail}"

# --- claim-check ---
ok, d = cc.check_claim("verdict: nothing quantitative here\nnext: sleep | owner: Naya Zeta")
t("no-claim-vacuous-pass", ok, d)

ok, d = cc.check_claim("verdict: CI is green, all 12/12 checks passed\nnext: merge | owner: Naya Zeta")
t("green-claim-no-receipt-flags", not ok, d)

ok, d = cc.check_claim("verdict: CI is green, all 12/12 checks passed @ ba6263870425 check-run 115421538481 observed this mission\nnext: merge | owner: Naya Zeta")
t("green-claim-with-receipt-passes", ok, d)

ok, d = cc.check_claim("verdict: no failures on the gate, zero errors\nnext: ship | owner: Naya Zeta")
t("zero-failure-claim-no-receipt-flags", not ok, d)

ok, d = cc.check_claim("verdict: no failures, head sha ba6263870425\nnext: ship | owner: Naya Zeta")
t("zero-failure-with-sha-passes", ok, d)

# quoted/fenced claims must NOT bind (author's words only)
ok, d = cc.check_claim('> CI is green, all 12/12 checks passed\nverdict: reviewing a claim\nnext: n/a | owner: Naya Zeta')
t("quoted-green-claim-does-not-bind", ok, d)

ok, d = cc.check_claim('```\nCI is green, all 12/12 passed\n```\nverdict: pasted log\nnext: n/a | owner: Naya Zeta')
t("fenced-green-claim-does-not-bind", ok, d)

# scores belong to check_score, not claim-check
ok, d = cc.check_claim("score: 9.5/10 — verified\nverdict: done\nnext: n/a | owner: Naya Zeta")
t("score-not-a-claim-check-target", ok, d)

# --- dedup ---
recent = ["[PULSE] Naya Zeta | lane 3 | IB-w195: harden post_checker emission gates\nstate: doing\nverdict: signed in and working the gates\nnext: build | owner: Naya Zeta"]
dup = "[PULSE] Naya Zeta | lane 3 | IB-w195: harden post_checker emission gates\nstate: doing\nverdict: signed in and working the gates\nnext: build | owner: Naya Zeta"
ok, d = cc.check_dedup(dup, recent)
t("exact-duplicate-flags", not ok, d)

fresh = "[PULSE] Naya Zeta | lane 3 | IB-w195: P-035 routed\nstate: doing\nverdict: fixture hash verified, invitation posted to Epsilon\nnext: claim-check build | owner: Naya Zeta"
ok, d = cc.check_dedup(fresh, recent)
t("distinct-post-passes", ok, d)

ok, d = cc.check_dedup(fresh, [])
t("empty-recent-passes", ok, d)

# --- vocabulary alignment: Gamma's claim_reconcile fixtures (w201) ---
# The addon requires receipt PRESENCE; truth/freshness is claim_reconcile's job.
# Repo-relative: fixtures ship in-PR under tools/claim_reconcile_fixtures
# (w206 fix-pass — the absolute gamma-w186 worktree path died with the worktree)
FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claim_reconcile_fixtures")
A40 = "a" * 40
def fx(name):
    return open(f"{FX}/{name}").read()

ok, d = cc.check_claim(fx("claim-clean.txt"))
t("gamma-claim-clean-binds", ok, d)                       # "CI is green at <sha>"

ok, d = cc.check_claim(fx("claim-stale.txt"))
t("gamma-claim-stale-binds", ok, d)                       # receipt present; STALE is the CI gate's verdict

ok, d = cc.check_claim(fx("claim-cherrypick.txt"))
t("gamma-claim-cherrypick-binds", ok, d)                  # ordering is the CI gate's verdict

ok, d = cc.check_claim(fx("claim-named-exact.txt"))
t("gamma-claim-named-exact-binds", ok, d)                 # "Team gate green at <sha>"

ok, d = cc.check_claim(fx("claim-named-homograph.txt"))
t("gamma-claim-named-homograph-binds", ok, d)             # homograph binds at CI gate; presence here

ok, d = cc.check_claim(fx("claim-ambiguous.txt"))
t("gamma-claim-ambiguous-binds", ok, d)                   # ambiguous fails closed at CI gate; presence here

ok, d = cc.check_claim(fx("claim-conflict.txt"))
t("gamma-claim-conflict-binds", ok, d)                    # bare #NNNN binds (BARE_ISSUE_BINDS=True; item 9 owns the verdict)

ok, d = cc.check_claim(fx("claim-vacuous.txt"))
t("gamma-claim-vacuous-pass", ok, d)                      # no adjudicable claim

# regression: canonical "green at <sha>" must NEVER flag for missing receipt
ok, d = cc.check_claim(f"verdict: CI is green at {A40} observed this mission\nnext: n/a | owner: Naya Zeta")
t("bare-sha-is-a-receipt", ok, d)

# named-green without any receipt still flags
ok, d = cc.check_claim("verdict: Team gate green\nnext: merge | owner: Naya Zeta")
t("named-green-no-receipt-flags", not ok, d)

# bare #NNNN binding is the item-9 verdict boundary, isolated on one flag
t("bare-issue-bind-flag-exists", isinstance(cc.BARE_ISSUE_BINDS, bool),
  f"BARE_ISSUE_BINDS={cc.BARE_ISSUE_BINDS}")

# date shapes are not count claims (Kappa w219 IV on #2625 — the false positive)
ok, d = cc.check_claim("verdict: deploy scheduled 2026/11/15\nnext: wait | owner: Naya Zeta")
t("slash-date-not-a-count-claim", ok, d)

ok, d = cc.check_claim("verdict: retro on 2026/10/15 went well\nnext: n/a | owner: Naya Zeta")
t("october-slash-date-not-a-count-claim", ok, d)

# a real N/N count next to a date must STILL bind (the fix must not over-strip)
ok, d = cc.check_claim("verdict: 2026/11/15 deploy, all 12/12 checks green\nnext: merge | owner: Naya Zeta")
t("date-plus-real-count-still-flags", not ok, d)

ok, d = cc.check_claim("verdict: 2026/11/15 deploy, all 12/12 checks green @ ba6263870425\nnext: merge | owner: Naya Zeta")
t("date-plus-bound-count-passes", ok, d)

if __name__ == "__main__":
    # Reaching here means every t() above passed.
    print("\nALL GREEN")
