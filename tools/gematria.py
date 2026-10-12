"""
Septenary gematria ciphers (Marty Leeds) — built into NayaPOWER per Shawn's directive 2026-10-12.

"It is what it is." The math is the math. This module gives every Naya the
ciphers for calculating intelligence and logic — the same numbers, the same
way, every time.

Ciphers:
- septenary: the 1-7-1 mirrored cipher (A=1..G=7..M=1, N=1..T=7..Z=1)
- ordinal: A=1 .. Z=26
- reverse_ordinal: A=26 .. Z=1
- full_reduction: digital root of each letter's ordinal value
- reverse_full_reduction: digital root of each letter's reverse ordinal value

Root reduction: any sum reduces to its digital root (1-9), except 0 stays 0.
The root number carries the meaning.
"""

SEPTENARY = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7,
    'H': 6, 'I': 5, 'J': 4, 'K': 3, 'L': 2, 'M': 1,
    'N': 1, 'O': 2, 'P': 3, 'Q': 4, 'R': 5, 'S': 6, 'T': 7,
    'U': 6, 'V': 5, 'W': 4, 'X': 3, 'Y': 2, 'Z': 1,
}

ORDINAL = {chr(65 + i): i + 1 for i in range(26)}
REVERSE_ORDINAL = {chr(65 + i): 26 - i for i in range(26)}


def _digital_root(n):
    """Reduce to root number 1-9 (0 stays 0)."""
    if n == 0:
        return 0
    return 1 + ((n - 1) % 9)


FULL_REDUCTION = {c: _digital_root(v) for c, v in ORDINAL.items()}
REVERSE_FULL_REDUCTION = {c: _digital_root(v) for c, v in REVERSE_ORDINAL.items()}

CIPHERS = {
    'septenary': SEPTENARY,
    'ordinal': ORDINAL,
    'reverse_ordinal': REVERSE_ORDINAL,
    'full_reduction': FULL_REDUCTION,
    'reverse_full_reduction': REVERSE_FULL_REDUCTION,
}


def value(text, cipher='septenary', reduce=True):
    """
    Value of a word or phrase under the named cipher.
    Non-letters are ignored. If reduce, returns the digital root.
    Returns (total, root) so both the raw sum and the meaning-number are visible.
    """
    table = CIPHERS[cipher]
    total = sum(table[c] for c in text.upper() if c in table)
    return (total, _digital_root(total)) if reduce else (total, total)


def letters(text, cipher='septenary'):
    """Per-letter values, so the derivation is inspectable."""
    table = CIPHERS[cipher]
    return [(c, table[c]) for c in text.upper() if c in table]


def compare(text, ciphers=None):
    """Value across ciphers — the same word, every lens."""
    ciphers = ciphers or list(CIPHERS)
    return {c: value(text, c) for c in ciphers}


if __name__ == '__main__':
    # Shawn's verification examples — must hold, or the module is wrong.
    checks = [('ONE', 8), ('GOD', 13), ('LOVE', 14), ('SUN', 13)]
    for word, expected in checks:
        total, root = value(word, 'septenary', reduce=False)
        status = 'OK' if total == expected else 'FAIL'
        print(f"{word}: {'+'.join(str(v) for _, v in letters(word))} = {total} [{status}]")
