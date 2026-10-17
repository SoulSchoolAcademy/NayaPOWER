#!/usr/bin/env python3
"""Show-your-work gate: no receipt = no merge.

Shawn's law (2026-10-11): every merge must carry a receipt proving three
honest scoring passes happened. This gate reads the PR body and validates
the `## Show-Your-Work Receipt` section.

A valid receipt must contain:
  1. The branch name and the exact 40-char head SHA being certified.
  2. Three passes, EACH labeled as self-validation (never as independent
     verification — three self-passes must not be mislabeled).
  3. Each pass has a score in X/10 format.
  4. Pass 1 and Pass 2 list the holes found and the repairs made.
     (If a pass scored 10/10 with no holes, it must say so explicitly —
     silence is not evidence.)
  5. Pass 3 states the final result and re-confirms the exact head SHA.
  6. The head SHA in the receipt matches the actual PR head SHA
     (passed via HEAD_SHA env var).

Exit 0 = receipt valid. Exit 1 = fail with a plain-words reason.
Stdlib only. No network.
"""
import os
import re
import sys


def fail(msg):
    print(f"SHOW-YOUR-WORK GATE FAILED: {msg}")
    print()
    print("Fix: add a `## Show-Your-Work Receipt` section to the PR body with:")
    print("  - Branch name and exact 40-char head SHA")
    print("  - Pass 1: score (X/10), holes found, repairs made")
    print("  - Pass 2: score (X/10), remaining holes, repairs made")
    print("  - Pass 3: score (X/10), final result, exact head SHA re-confirmed")
    print("  - All three passes labeled as self-validation")
    print()
    print("Template:")
    print("  ## Show-Your-Work Receipt")
    print("  **Branch:** `my-branch`")
    print("  **Head SHA:** `<40-char-sha>`")
    print("  ### Pass 1 (self-validation) — Score: 7/10")
    print("  **Holes found:** ...")
    print("  **Repairs made:** ...")
    print("  ### Pass 2 (self-validation) — Score: 9/10")
    print("  **Remaining holes:** ...")
    print("  **Repairs made:** ...")
    print("  ### Pass 3 (self-validation) — Score: 10/10")
    print("  **Result:** ...")
    print("  **Exact head certified:** `<40-char-sha>`")
    sys.exit(1)


def extract_section(body, heading_pattern):
    """Extract the text of a markdown section by heading pattern."""
    m = re.search(heading_pattern, body, re.IGNORECASE | re.MULTILINE)
    if not m:
        return None
    section = body[m.end():]
    nxt = re.search(r"^##\s+", section, re.MULTILINE)
    if nxt:
        section = section[:nxt.start()]
    return section


def find_score(text):
    """Find X/10 score in text. Returns int or None."""
    m = re.search(r"[Ss]core\s*:\s*(\d+)\s*/\s*10", text)
    if m:
        return int(m.group(1))
    return None


def has_holes_and_repairs(text):
    """Check that holes and repairs are documented (not just empty)."""
    holes_m = re.search(r"\*\*Holes found:\*\*\s*(.+)", text, re.DOTALL)
    repairs_m = re.search(r"\*\*Repairs made:\*\*\s*(.+)", text, re.DOTALL)
    if not holes_m or not repairs_m:
        # Also accept "Remaining holes" for pass 2
        holes_m = holes_m or re.search(r"\*\*Remaining holes:\*\*\s*(.+)", text, re.DOTALL)
        if not holes_m or not repairs_m:
            return False
    holes_text = holes_m.group(1).strip()
    repairs_text = repairs_m.group(1).strip()
    # Must have actual content, not just whitespace or "TBD"
    for t in (holes_text, repairs_text):
        first_line = t.split("\n")[0].strip().lower()
        if not first_line or first_line in ("tbd", "todo", "n/a", "none yet"):
            return False
    return True


def main():
    body = os.environ.get("PR_BODY") or ""
    expected_sha = (os.environ.get("HEAD_SHA") or "").lower().strip()

    section = extract_section(body, r"^##\s+show-your-work receipt\s*$")
    if section is None:
        fail("no `## Show-Your-Work Receipt` section in the PR body.")

    # --- 1. Branch and head SHA ---
    branch_m = re.search(r"\*\*Branch:\*\*\s*`([^`]+)`", section)
    if not branch_m:
        fail("receipt is missing the `**Branch:**` field.")
    branch = branch_m.group(1).strip()

    sha_m = re.search(r"\*\*Head SHA:\*\*\s*`([0-9a-fA-F]{40})`", section)
    if not sha_m:
        fail("receipt is missing a valid 40-char `**Head SHA:**` field.")
    receipt_sha = sha_m.group(1).lower()

    if expected_sha and receipt_sha != expected_sha:
        fail(
            f"receipt certifies head SHA {receipt_sha[:8]}... but the PR's "
            f"actual head is {expected_sha[:8]}... The receipt must pin the "
            f"exact head being merged."
        )

    # --- 2. Three passes, each labeled self-validation ---
    passes = []
    for i in (1, 2, 3):
        # Find "Pass N" heading with self-validation label
        pattern = rf"^###\s+Pass\s+{i}\s*\(self-validation\)"
        m = re.search(pattern, section, re.IGNORECASE | re.MULTILINE)
        if not m:
            # Check if the pass exists but is mislabeled
            mislabeled = re.search(
                rf"^###\s+Pass\s+{i}\s*\(([^)]+)\)", section,
                re.IGNORECASE | re.MULTILINE)
            if mislabeled:
                label = mislabeled.group(1).strip()
                fail(
                    f"Pass {i} is labeled '{label}' but must be labeled "
                    f"'self-validation'. Three self-passes must never be "
                    f"described as independent verification.")
            fail(f"receipt is missing `### Pass {i} (self-validation)`.")

        # Extract this pass's text (until next ### or end)
        pass_text = section[m.end():]
        nxt = re.search(r"^###\s+", pass_text, re.MULTILINE)
        if nxt:
            pass_text = pass_text[:nxt.start()]
        passes.append(pass_text)

    # --- 3. Each pass has a score ---
    for i, pass_text in enumerate(passes, 1):
        score = find_score(pass_text)
        if score is None:
            fail(f"Pass {i} is missing a score in X/10 format (e.g. 'Score: 7/10').")
        if not (0 <= score <= 10):
            fail(f"Pass {i} score {score}/10 is out of range (must be 0-10).")

    # --- 4. Passes 1 and 2 document holes and repairs ---
    for i in (1, 2):
        if not has_holes_and_repairs(passes[i - 1]):
            fail(
                f"Pass {i} must list holes found and repairs made "
                f"(`**Holes found:**` and `**Repairs made:**`). "
                f"If there were truly no holes, say so explicitly.")

    # --- 5. Pass 3 confirms the exact head ---
    pass3 = passes[2]
    cert_m = re.search(r"\*\*Exact head certified:\*\*\s*`([0-9a-fA-F]{40})`", pass3)
    if not cert_m:
        fail("Pass 3 must re-confirm with `**Exact head certified:**` + 40-char SHA.")
    cert_sha = cert_m.group(1).lower()
    if cert_sha != receipt_sha:
        fail(
            f"Pass 3 certifies {cert_sha[:8]}... but the receipt header "
            f"names {receipt_sha[:8]}... They must match.")

    result_m = re.search(r"\*\*Result:\*\*\s*(.+)", pass3)
    if not result_m or not result_m.group(1).strip():
        fail("Pass 3 must state the final `**Result:**`.")

    # --- All checks passed ---
    print(f"SHOW-YOUR-WORK GATE PASSED: receipt valid for branch `{branch}`,")
    print(f"  head {receipt_sha[:12]}..., "
          f"scores {find_score(passes[0])}/10 → "
          f"{find_score(passes[1])}/10 → {find_score(passes[2])}/10.")
    print("  All three passes labeled self-validation. No merge block.")


if __name__ == "__main__":
    main()
