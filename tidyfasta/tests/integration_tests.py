import unittest
import filecmp

import os
import sys

from tidyfasta.common.process import *

def get_test_dir():
    return os.path.dirname(os.path.realpath(__file__))

class IntegrationTests(unittest.TestCase):

    def test_class_method_ProcessFASTA_get_fasta_gold_standard(self):

        test_ProcessFasta = ProcessFasta(get_test_dir() + "/inputs/test_gold_standard.txt", False, False)

        valid_array = test_ProcessFasta.get_fasta()
        valid_array = test_ProcessFasta.validate_FASTA()

        self.assertEqual("> alirocumab", valid_array[0].ID)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAAVTPVDGALLGDVVTVEAAETF", valid_array[0].sequence)

    def test_class_method_ProcessFASTA_get_fasta_excess_whitespace_multi(self):

        test_ProcessFasta = ProcessFasta(get_test_dir() + "/inputs/test_excess_whitespace_multi.txt", False, False)

        valid_array = test_ProcessFasta.get_fasta()
        valid_array = test_ProcessFasta.validate_FASTA()

        self.assertEqual("> alirocumab1", valid_array[0].ID)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAA", valid_array[0].sequence)
        self.assertEqual("> alirocumab2", valid_array[1].ID)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAA", valid_array[1].sequence)
        self.assertEqual("> alirocumab3", valid_array[2].ID)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAA", valid_array[2].sequence)

    def test_class_method_ProcessFASTA_get_fasta_ID_only(self):

        with self.assertRaises(Exception) : ProcessFasta(get_test_dir() + "/inputs/test_ID_only.txt", False, False)

    def test_class_method_ProcessFASTA_get_fasta_ID_only_single(self):

        with self.assertRaises(Exception) : ProcessFasta(get_test_dir() + "/inputs/test_ID_only_single.txt", False, False)

if __name__ == '__main__':
    unittest.main()
