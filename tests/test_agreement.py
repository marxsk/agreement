#!/usr/bin/python -tt

import unittest
import agreement

ABC_AGREEMENT_FILE = "abc.csv"
STRING_FILE = "string.csv"

class TestCohenClass(unittest.TestCase):
	def test_kappa_int(self):
		k = agreement.cohen_kappa(agreement.load_data(ABC_AGREEMENT_FILE))
		self.assertAlmostEquals(0.46, k, delta=0.01)

	def test_init_string(self):
		self.assertIsNotNone(agreement.cohen_kappa(agreement.load_data(STRING_FILE)))

if __name__ == "__main__":
	unittest.main()
