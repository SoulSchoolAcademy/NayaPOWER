#!/usr/bin/env python3
"""Identity Separation — a review counts only from a different identity.

This check encodes the main seat's 2026-10-20 adjudication of the
merge-protocol breaches (team board #2793, comments 6296868688 /
6296909966): PRs #2796 / #2799 / #2800 / #2801 were merged by the
nayapower-lane-agent[bot] login, with the sole "reviews" also posted
from that same login, claimed in text as a different seat. Ruling:
a same-login review is NOT different-seat validation. Identity is
what counts, never a seat name in text.

That is why this module reads IDENTITIES — GitHub logins — only. It
never reads a seat name, a signature, a title, or any claim inside
review text. Text can claim any seat; a login cannot claim to be a
different login. The reviewing identity must differ from the author
identity and from the merger identity before it counts as independent
verification, because doer, scorer, and verifier are never the same
mind (PROTOCOL.md, Standing Laws) — and "mind", for a machine check,
means identity.

Input record:
    {
      "number": 2799,
      "title": "<PR title>",
      "author_login": "<login that authored the PR>",
      "merger_login": "<login that merged it>",     # may be ""
      "merged": true,
      "claims_validated": false,   # optional, default false: the record
                                   # (or text riding with it) claims this
                                   # work was validated / verified
      "reviews": [
        {"login": "<reviewer login>",
         "state": "APPROVED" | "COMMENTED" | "CHANGES_REQUESTED"
                  | "DISMISSED"},
        ...
      ]
    }

Checks:
  1. Shape, fail closed: author_login is a non-empty string;
     merger_login, when present, is a string ("" allowed — unmerged
     work often has no merger yet); merged and claims_validated, when
     present, are booleans; reviews is a list of objects each carrying
     a non-empty login and a state in the known set. A missing or
     malformed login is not a smaller identity — it is no identity,
     and no identity can never establish separation.
  2. (c) Merged with zero reviews FAILS: MERGED_WITHOUT_ANY_REVIEW.
     A merge nobody reviewed at all has no validation to argue about.
  3. (b) Reviews exist and EVERY review login == author_login:
     if merged or claims_validated, FAILS: SELF_REVIEW_ONLY — a
     same-login review is not verification, whatever seat the text
     claims. If neither merged nor claims_validated, the record passes
     with a warning reason: the self-review exists, but nothing has
     been merged or claimed validated on its strength.
  4. (a) Merged, merger_login == author_login, and no review from any
     login != author_login FAILS:
     SELF_MERGE_WITHOUT_INDEPENDENT_REVIEW. Self-merge is survivable
     only when an independent identity actually reviewed the work.
  5. Merged with reviews, but no reviewer login different from BOTH
     author_login and merger_login FAILS: NO_INDEPENDENT_REVIEW —
     a review from the merger's own login is the merger agreeing with
     herself, not independence.
  6. (d) Merged, and at least one review from a login different from
     BOTH author and merger, PASSES — naming the independent identity.
     (This includes rule (d)'s merger != author shape, and the
     self-merge shape rule (a) excepts: self-merge WITH a genuinely
     independent review on the record.)
  7. (e) Not merged, and an independent review exists, PASSES.
     Not merged with no claims and no independent review also passes:
     nothing has been merged and nothing has been claimed validated,
     so no separation breach has occurred — reviews are noted as
     absent, not treated as a violation. But claims_validated with NO
     independent review (and no self-review — rule 3 already covered
     that shape) FAILS: VALIDATION_CLAIMED_WITHOUT_INDEPENDENT_REVIEW;
     a validation claim needs an independent identity behind it.

details always include author_login, merger_login, and
independent_reviewers: the sorted set of reviewer logins different
from both author_login and merger_login.

Honest bounds: this check reads the record it is given. It cannot
tell whether two different logins are secretly operated by the same
mind, whether a review's CONTENT actually examined the work, or
whether the record itself matches GitHub's real review list — feeding
it a true record is the caller's job, and independent verification of
the underlying PR is a different check's job. What it does settle,
exactly, is the adjudicated question: on THIS record, did a login
other than the author's and merger's review the work — yes or no,
with no seat name in any text able to change the answer.

Usage:
    python3 tools/protocol/checks/identity_separation.py \
        --record '{"number": 2799, ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

REVIEW_STATES = frozenset(
    ["APPROVED", "COMMENTED", "CHANGES_REQUESTED", "DISMISSED"]
)


def _nonempty_str(value) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {
        "law": "IDENTITY-SEPARATION",
        "law_status": (
            "ADJUDICATED 2026-10-20 (board #2793, comments 6296868688 / "
            "6296909966; breaches #2796/#2799/#2800/#2801)"
        ),
    }

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    # Record identity, for receipts — never used as a check input.
    if record.get("number") is not None:
        details["number"] = record.get("number")
    title = _nonempty_str(record.get("title"))
    if title:
        details["title"] = title

    # 1. Shape — fail closed on malformed / missing logins.
    author_login = _nonempty_str(record.get("author_login"))
    if not author_login:
        return fail(
            "author_login missing or empty — identity separation reads "
            "logins only, and a record with no author identity can "
            "establish no separation at all",
            details,
        )
    merger_raw = record.get("merger_login", "")
    if not isinstance(merger_raw, str):
        return fail(
            "merger_login is not a string — a merger identity must be "
            "a login string (or \"\" when there is no merger yet)",
            details,
        )
    merger_login = merger_raw.strip()

    merged = record.get("merged", False)
    if not isinstance(merged, bool):
        return fail(
            "merged is not a boolean — the merge state decides which "
            "separation rules bite, so it must be stated exactly",
            details,
        )
    claims_validated = record.get("claims_validated", False)
    if not isinstance(claims_validated, bool):
        return fail(
            "claims_validated is not a boolean — whether validation was "
            "claimed decides which separation rules bite, so it must "
            "be stated exactly",
            details,
        )

    reviews = record.get("reviews")
    if not isinstance(reviews, list):
        return fail(
            "reviews is not a list — absence of the review record fails "
            "closed; an unlisted review cannot count as independent",
            details,
        )
    reviewer_logins: list[str] = []
    for i, rev in enumerate(reviews):
        if not isinstance(rev, dict):
            return fail(
                f"review #{i} is not an object — every review must "
                "carry its reviewer's login and state",
                details,
            )
        login = _nonempty_str(rev.get("login"))
        if not login:
            return fail(
                f"review #{i} has no login — a review with no identity "
                "is not a review this check can count, in either "
                "direction",
                details,
            )
        state = rev.get("state")
        if state not in REVIEW_STATES:
            return fail(
                f"review #{i} by {login!r} has state {state!r}, not one "
                f"of {', '.join(sorted(REVIEW_STATES))} — an unknown "
                "review state fails closed",
                details,
            )
        reviewer_logins.append(login)

    independent_reviewers = sorted(
        {
            login
            for login in reviewer_logins
            if login != author_login and login != merger_login
        }
    )
    any_review_beyond_author = any(
        login != author_login for login in reviewer_logins
    )
    details["author_login"] = author_login
    details["merger_login"] = merger_login
    details["independent_reviewers"] = independent_reviewers
    details["reviewer_logins"] = sorted(set(reviewer_logins))
    details["merged"] = merged
    details["claims_validated"] = claims_validated

    # 2. (c) Merged with zero reviews at all.
    if merged and not reviews:
        extra = (
            " SELF_MERGE_WITHOUT_INDEPENDENT_REVIEW also applies: "
            "merger_login == author_login."
            if merger_login == author_login
            else ""
        )
        return fail(
            "MERGED_WITHOUT_ANY_REVIEW: PR merged with zero reviews on "
            f"the record (author {author_login!r}, merger "
            f"{merger_login!r}) — a merge nobody reviewed has no "
            "validation at all." + extra,
            details,
        )

    # 3. (b) Every review is from the author's own login.
    if reviews and all(login == author_login for login in reviewer_logins):
        if merged or claims_validated:
            extra = (
                " SELF_MERGE_WITHOUT_INDEPENDENT_REVIEW also applies: "
                "merged by the author login with no review from any "
                "other login."
                if merged and merger_login == author_login
                else ""
            )
            return fail(
                "SELF_REVIEW_ONLY: every review is from the author "
                f"login {author_login!r} itself, yet the record is "
                f"merged={merged} / claims_validated={claims_validated} "
                "— a same-login review is not different-seat "
                "validation; identity is what counts, never a seat name "
                "in text (2026-10-20 adjudication, breaches "
                "#2796/#2799/#2800/#2801)." + extra,
                details,
            )
        return result(
            True,
            [
                "WARNING: SELF_REVIEW_ONLY — every review is from the "
                f"author login {author_login!r} itself. Nothing is "
                "merged and nothing claims validation, so no breach has "
                "occurred yet — but this review can never count as "
                "verification if either changes."
            ],
            details,
        )

    # 4. (a) Self-merge with no review from beyond the author.
    if merged and merger_login == author_login and not any_review_beyond_author:
        return fail(
            "SELF_MERGE_WITHOUT_INDEPENDENT_REVIEW: merger_login == "
            f"author_login ({author_login!r}) and no review came from "
            "any login other than the author's — the author merged her "
            "own work with no independent identity on the record",
            details,
        )

    # Validation claimed, independent review required behind it.
    if claims_validated and not independent_reviewers and not merged:
        return fail(
            "VALIDATION_CLAIMED_WITHOUT_INDEPENDENT_REVIEW: the record "
            "claims validation, but no reviewer login differs from "
            f"both author {author_login!r} and merger "
            f"{merger_login!r} — a validation claim needs an "
            "independent identity behind it",
            details,
        )

    if merged:
        # 5 / 6. Merged: an identity independent of BOTH must have reviewed.
        if not independent_reviewers:
            return fail(
                "NO_INDEPENDENT_REVIEW: PR merged, but no reviewer "
                f"login differs from both author {author_login!r} and "
                f"merger {merger_login!r} (reviewers: "
                f"{', '.join(sorted(set(reviewer_logins))) or 'none'}) "
                "— a review from the merger's own login is the merger "
                "agreeing with herself, not independence",
                details,
            )
        names = ", ".join(independent_reviewers)
        if merger_login == author_login:
            reasons.append(
                "self-merge WITH independent review: merger == author "
                f"({author_login!r}), but independent identity "
                f"{names} reviewed the work — rule (a)'s exception is "
                "met on identities, not on seat names"
            )
        else:
            reasons.append(
                f"independent review by {names} — different from both "
                f"author {author_login!r} and merger {merger_login!r}"
            )
        reasons.append(
            "identity separation holds: author, merger, and at least "
            "one reviewer are not all the same login"
        )
        return result(True, reasons, details)

    # 7. (e) Not merged.
    if independent_reviewers:
        reasons.append(
            "not merged, and independent review exists by "
            f"{', '.join(independent_reviewers)} — different from both "
            f"author {author_login!r} and merger {merger_login!r}"
        )
        return result(True, reasons, details)

    reasons.append(
        "not merged and no validation claimed — no separation breach "
        "has occurred; independent review is absent, and that absence "
        "is noted, not treated as a violation of an unmerged record"
    )
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Identity Separation check")
    parser.add_argument("--record", required=True,
                        help="JSON identity-separation record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}",
                         {"law": "IDENTITY-SEPARATION"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
