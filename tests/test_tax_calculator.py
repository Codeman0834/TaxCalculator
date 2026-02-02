import unittest

from tax_calculator import Bracket, calculate_tax


class TaxCalculatorTests(unittest.TestCase):
    def test_zero_income(self):
        brackets = [Bracket(0, 0.1)]
        self.assertEqual(calculate_tax(0, brackets), 0.0)

    def test_single_bracket(self):
        brackets = [Bracket(0, 0.1)]
        self.assertAlmostEqual(calculate_tax(1000, brackets), 100.0)

    def test_multiple_brackets(self):
        brackets = [Bracket(0, 0.1), Bracket(1000, 0.2), Bracket(2000, 0.3)]
        self.assertAlmostEqual(calculate_tax(2500, brackets), 100 + 200 + 150)


if __name__ == "__main__":
    unittest.main()
