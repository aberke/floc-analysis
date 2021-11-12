# test_prefixLSH.py

import unittest

from prefixLSH import get_bit_hash_cohorts_dict


class TestPrefixLSH(unittest.TestCase):

    def test_trivial_cohorts(self):
        self.assertEqual(get_bit_hash_cohorts_dict(["0"], min_k=1), {"0": 1})
        self.assertEqual(get_bit_hash_cohorts_dict(["1"], min_k=1), {"1": 1})
        self.assertEqual(get_bit_hash_cohorts_dict(["01"], min_k=1), {"01": 1})

    def test_cohorts(self):
        self.assertEqual(get_bit_hash_cohorts_dict(["01", "10"], min_k=1), {"01": 1,"10":2})
        self.assertEqual(
            get_bit_hash_cohorts_dict(["00", "01", "10"], min_k=1),
            {"00":1,"01":2,"10":3}
        )
        self.assertEqual(
            get_bit_hash_cohorts_dict(["00", "01", "10", "11"], min_k=1),
            {"00":1,"01":2,"10":3,"11":4}
        )
        self.assertEqual(
            get_bit_hash_cohorts_dict(["000", "010", "100", "110", "111"], min_k=2),
            {"000":1,"010":1,"100":2,"110":2,"111":2}
        )
        self.assertEqual(
            get_bit_hash_cohorts_dict(["000", "010", "100", "100", "110", "111"], min_k=2),
            {"000":1,"010":1,"100":2,"110":3,"111":3}
        )

    def test_duplicate_hashes(self):
        """Duplicate hashes should be in the same cohort."""
        hash_list = ["01"]*100
        expected_cohorts_dict = {"01": 1}
        self.assertEqual(get_bit_hash_cohorts_dict(hash_list, min_k=50), expected_cohorts_dict)
        hash_list = ["010"]*100 + ["110"]*100 + ["111"] # all alone
        expected_cohorts_dict = {"010": 1, "110": 2, "111": 2}
        self.assertEqual(get_bit_hash_cohorts_dict(hash_list, min_k=50), expected_cohorts_dict)


if __name__ == '__main__':
    unittest.main()
