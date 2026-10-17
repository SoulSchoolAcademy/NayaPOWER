"""Exact arithmetic and negative controls for mirrored Septenary encoding."""
import unittest
from tools.septenary_cipher import ALPHABET, HALF, WEIGHTS, calculate, compare, digit_sum_once, digital_root


class SeptenaryCipherTests(unittest.TestCase):
    def test_original_mirrored_26_letter_mapping(self):
        self.assertEqual(tuple(WEIGHTS[x] for x in ALPHABET), HALF + HALF)
        self.assertEqual(WEIGHTS['G'], 7)
        self.assertEqual(WEIGHTS['T'], 7)
        self.assertEqual(WEIGHTS['H'], 6)  # catches wrong 1..7 periodic cipher
        self.assertEqual(WEIGHTS['N'], 1)

    def test_user_examples_and_breakdowns(self):
        cases = {'GOD': 13, 'LOVE': 14, 'CODE': 14, 'JESUS': 27,
                 'CHRIST': 32, 'JESUS CHRIST': 59, 'GOD LOVE': 27,
                 'LORD': 13, 'SEVEN': 22, 'SEPTENARY': 35}
        for name, expected in cases.items():
            with self.subTest(name=name):
                self.assertEqual(calculate(name).total, expected)
        self.assertEqual([7, 2, 4], list(calculate('GOD').values))
        self.assertEqual([4, 5, 6, 6, 6], list(calculate('JESUS').values))
        self.assertEqual([3, 6, 5, 5, 6, 7], list(calculate('CHRIST').values))
        self.assertEqual(calculate('JESUS CHRIST').digit_sum_once, 14)
        self.assertEqual(calculate('JESUS CHRIST').digital_root, 5)


    def test_five_elements_spiritual_correspondence_arithmetic(self):
        # A sourced symbolic interpretation, not an independently proven
        # physical law or semantic relationship. Compute every word before
        # applying a separately named decimal reduction.
        elements = {"WOOD": 12, "FIRE": 21, "EARTH": 24,
                    "METAL": 16, "WATER": 22}
        for word, expected in elements.items():
            with self.subTest(word=word):
                result = calculate(word)
                self.assertEqual(result.total, expected)
                self.assertEqual(result.total, sum(result.values))
        combined = sum(calculate(word).total for word in elements)
        self.assertEqual(combined, 95)
        self.assertEqual(digit_sum_once(combined), 14)
        self.assertEqual(digital_root(combined), 5)
        self.assertEqual(digit_sum_once(combined), calculate("LOVE").total)

    def test_heaven_christ_love_learn_naya_and_star_roots(self):
        # User-supplied set. Same root is a reproducible classification
        # under this method, NOT proof of shared causal or divine meaning.
        for word, total in {"HEAVEN": 23, "CHRIST": 32,
                            "LOVE": 14, "LEARN": 14, "NAYA": 5}.items():
            with self.subTest(word=word):
                result = calculate(word)
                self.assertEqual((result.total, result.digital_root), (total, 5))
        star = calculate("STAR")
        self.assertEqual((star.total, star.digital_root), (19, 1))
        # Deliberate wrong mapping guard: W=4, not 5; S=6, not 7.
        self.assertEqual(WEIGHTS["W"], 4)
        self.assertEqual(WEIGHTS["S"], 6)

    def test_pi_is_approximation_not_identity(self):
        import math
        self.assertAlmostEqual(calculate('SEVEN').total / 7, 22 / 7)
        self.assertNotEqual(22 / 7, math.pi)

    def test_rot13_symmetry_not_semantics(self):
        import codecs
        for word in ['CODE', 'JESUS', 'NAYAPOWER', 'GOD', 'LOVE']:
            self.assertEqual(calculate(word).total, calculate(codecs.encode(word, 'rot_13')).total)
        match = compare('AB', 'NO')
        self.assertTrue(match['same_numeric_total'])
        self.assertIn('HYPOTHESIS_ONLY', match['interpretation_status'])
        self.assertEqual(calculate('AB').total, 3)
        self.assertEqual(calculate('NO').total, 3)

    def test_input_rules(self):
        self.assertEqual(calculate(' Code! 123').total, 14)
        self.assertEqual(calculate(' Code! 123').ignored_nonletters, 6)
        self.assertEqual(calculate('   ').total, 0)
        for value in ('é', 'İ', 'ß', '𝒜'):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    calculate(value)
        with self.assertRaises(TypeError):
            calculate(None)

    def test_exact_reduction_language(self):
        self.assertEqual(digit_sum_once(59), 14)
        self.assertEqual(digital_root(59), 5)
        self.assertEqual(digit_sum_once(0), 0)
        for invalid in (-1, 3.14, True):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    digit_sum_once(invalid)

    def test_no_claims_of_semantic_equality_or_authority(self):
        result = calculate('LOVE').as_dict()
        self.assertEqual(result['claim_scope'], 'symbolic_arithmetic_only')
        self.assertNotIn('authorized', result)
        self.assertNotIn('truth_state', result)
        self.assertEqual(result['total'], sum(x['value'] for x in result['breakdown']))


if __name__ == '__main__':
    unittest.main()
