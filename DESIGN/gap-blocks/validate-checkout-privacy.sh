#!/usr/bin/env bash
# validate-checkout-privacy.sh — privacy-boundary contract for checkout-blocks.md
#
# The PAY-002 / PAY-005 privacy boundary, as a runnable check:
#   1. No full PAN anywhere in the spec (13-19 digits, with or without separators).
#   2. Card-field identifiers (card_number, card_cvc, card_expiry, cardholder_name,
#      cc-number, cc-exp, cc-csc, cc-name) appear ONLY in input name=/autocomplete=
#      attribute contexts — never in rendered text, error copy, or scripts.
#   3. No card fields are logged: no console.* calls anywhere in the spec.
#   4. Display layer shows at most last-4 + brand: after stripping hex colors,
#      years, decimal amounts, masked last-4s (···· NNNN), and opaque method
#      tokens (pm_<brand>_<last4> — brand + last-4 only, never a PAN; a real
#      build uses the processor's method id), no run of 4+ digits may remain.
#
# Usage: bash validate-checkout-privacy.sh [path/to/checkout-blocks.md]
# Exit 0 = boundary holds. Exit 1 = violation (file:line printed).
set -u

SPEC="${1:-$(dirname "$0")/checkout-blocks.md}"
if [ ! -f "$SPEC" ]; then
  echo "FAIL: spec not found: $SPEC" >&2
  exit 1
fi

fail=0
hit() { printf 'VIOLATION %s\n' "$1"; fail=1; }

# 1. No full PAN: 13-19 digits, allowing single spaces/dashes/dots/underscores
#    between digits (catches "4242 4242 4242 4242" as well as "4242424242424242").
while IFS= read -r line; do
  hit "possible full PAN: $line"
done < <(grep -nE '[0-9]([ ._-]?[0-9]){12,18}' "$SPEC" || true)

# 2. Card identifiers live only in input attributes (name=/autocomplete=).
#    Anything else — rendered text, error messages, prose claims of a number —
#    is a boundary violation.
while IFS= read -r line; do
  body="${line#*:}"
  case "$body" in
    *'name="card'*|*'autocomplete="cc-'*) ;;
    *) hit "card identifier outside an input attribute: $line" ;;
  esac
done < <(grep -nE 'card_number|card_cvc|card_expiry|cardholder_name|cc-number|cc-exp|cc-csc|cc-name' "$SPEC" || true)

# 3. No logging of card fields: the spec contains no console.* calls at all.
while IFS= read -r line; do
  hit "console call in spec (card fields must never be logged): $line"
done < <(grep -nE 'console\.[A-Za-z]+' "$SPEC" || true)

# 4. Display layer: at most last-4 + brand.
#    Strip everything that is legitimately numeric, then flag 4+ digit runs.
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
sed -E \
  -e 's/#[0-9a-fA-F]{3,8}//g' \
  -e 's/····[[:space:]]*[0-9]{4}//g' \
  -e 's/\bpm_[a-z]+_[0-9]{4}\b//g' \
  -e 's/\b(19|20)[0-9]{2}\b//g' \
  -e 's/\$[0-9][0-9.,]*//g' \
  -e 's/\b[0-9]{1,2}:[0-9]{2}\b//g' \
  -e 's/\{[0-9]+(,[0-9]+)?\}//g' \
  "$SPEC" > "$tmp"
while IFS= read -r line; do
  hit "unmasked 4+ digit run in display layer: $line"
done < <(grep -nE '[0-9]{4,}' "$tmp" || true)

if [ "$fail" -eq 0 ]; then
  echo "PASS: privacy boundary holds — no PAN, identifiers attribute-scoped, nothing logged, display shows at most last-4 + brand."
fi
exit "$fail"
