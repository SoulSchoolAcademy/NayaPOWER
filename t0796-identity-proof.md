# t0796 identity proof (scratch — safe to delete)

This commit exists only to prove the t0796 (lane 1, Verity) repair:
the push tooling stamps the EXECUTING SEAT's identity on commit
author/committer lines via the shared bin/seat_identity.py mechanism
(fail-closed when NAYA_SEAT_NAME/NAYA_SEAT_EMAIL are unset),
instead of a hardcoded default or the GitHub App identity.
