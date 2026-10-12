"""Read-only Marty Leeds mirrored Septenary cipher explorer.

Mathematical encoding, not a decision engine, truth oracle, learning promotion,
proof of semantic equivalence, or authorization source.

Primary published derivation: Marty Leeds, "Decoding The Gematria Of The
English Alphabet" (2014), https://grahamhancock.com/leedsm1/
User reference calculator: https://septenarygematria.com/

Mapping for A..M: 1,2,3,4,5,6,7,6,5,4,3,2,1; N..Z repeats.
We reproduce the arithmetic, not the original website's proprietary code/UI.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass

CIPHER_ID = "marty-leeds-mirrored-septenary-v1"
SOURCE_URL = "https://grahamhancock.com/leedsm1/"
REFERENCE_CALCULATOR_URL = "https://septenarygematria.com/"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
HALF = (1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1)
WEIGHTS = dict(zip(ALPHABET, HALF + HALF))


@dataclass(frozen=True)
class CipherResult:
    cipher_id: str
    source_url: str
    input_text: str
    letters: tuple[str, ...]
    values: tuple[int, ...]
    total: int
    digit_sum_once: int
    digital_root: int
    ignored_nonletters: int

    def as_dict(self) -> dict:
        return {
            "cipher_id": self.cipher_id,
            "source_url": self.source_url,
            "text": self.input_text,
            "breakdown": [{"letter": c, "value": v} for c, v in zip(self.letters, self.values)],
            "total": self.total,
            "digit_sum_once": self.digit_sum_once,
            "digital_root": self.digital_root,
            "ignored_nonletters": self.ignored_nonletters,
            "claim_scope": "symbolic_arithmetic_only",
            "epistemic_state": "COMPUTED; no semantic, causal, spiritual, or predictive conclusion",
        }


def digit_sum_once(n: int) -> int:
    """Add decimal digits once: 59 -> 14; not full digital-root reduction."""
    if type(n) is not int or n < 0:
        raise ValueError("digit_sum_once expects a nonnegative integer")
    return sum(int(d) for d in str(n))


def digital_root(n: int) -> int:
    """Repeated decimal digit reduction: 59 -> 14 -> 5 (separate operation)."""
    if type(n) is not int or n < 0:
        raise ValueError("digital_root expects a nonnegative integer")
    while n >= 10:
        n = digit_sum_once(n)
    return n


def calculate(text: str) -> CipherResult:
    """Compute the mirrored 1..7..1 cipher for the English A-Z alphabet.

    Whitespace, punctuation and digits are ignored; non-ASCII *letters* are
    rejected rather than silently transliterated. The casefold is ASCII-only.
    No network calls, storage, private data forwarding, or authority effects.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    chars: list[str] = []
    ignored = 0
    for char in text:
        c = char.upper()
        if len(c) == 1 and c in WEIGHTS and char.isascii():
            chars.append(c)
        elif char.isalpha():
            raise ValueError("Only English A-Z letters are supported; no implicit transliteration")
        else:
            ignored += 1
    vals = tuple(WEIGHTS[char] for char in chars)
    total = sum(vals)
    return CipherResult(
        cipher_id=CIPHER_ID, source_url=SOURCE_URL, input_text=text,
        letters=tuple(chars), values=vals, total=total,
        digit_sum_once=digit_sum_once(total), digital_root=digital_root(total),
        ignored_nonletters=ignored,
    )


def compare(left: str, right: str) -> dict:
    """Compare numeric totals only. Equal totals imply no semantic relation."""
    a, b = calculate(left), calculate(right)
    return {
        "left": a.as_dict(), "right": b.as_dict(),
        "same_numeric_total": a.total == b.total,
        "interpretation_status": "HYPOTHESIS_ONLY; independent evidence required",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Mirrored Septenary pattern explorer (read-only)")
    parser.add_argument("text", help="English word or phrase")
    parser.add_argument("--compare", metavar="TEXT", help="Second phrase for numeric comparison")
    args = parser.parse_args()
    result = compare(args.text, args.compare) if args.compare is not None else calculate(args.text).as_dict()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
