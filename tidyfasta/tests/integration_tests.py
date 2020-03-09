import unittest
import filecmp

import os
import sys

from tidyfasta.common.process import *

def get_test_dir_name():
    return os.path.dirname(os.path.realpath(__file__))

class IntegrationTests(unittest.TestCase):

    def test_class_method_ProcessFASTA_get_fasta_gold_standard(self):

        test_ProcessFasta = ProcessFasta(get_test_dir_name()+"/inputs/test_gold_standard.txt",False)

        test_array = test_ProcessFasta.get_fasta()

        self.assertEqual("> alirocumab", test_array[0].ID)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAAVTPVDGALLGDVVTVEAAETF", test_array[0].sequence)

    def test_class_method_ProcessFASTA_get_fasta_excess_whitespace_multi(self):

        test_ProcessFasta = ProcessFasta(get_test_dir_name()+"/inputs/test_excess_whitespace_multi.txt",False)

        test_array = test_ProcessFasta.get_fasta()

        self.assertEqual("> alirocumab1", test_array[0].ID)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAA", test_array[0].sequence)
        self.assertEqual("> alirocumab2", test_array[1].ID)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAA", test_array[1].sequence)
        self.assertEqual("> alirocumab3", test_array[2].ID)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAA", test_array[2].sequence)

    def test_class_method_ProcessFASTA_get_fasta_ID_only(self):

        with self.assertRaises(Exception) : ProcessFasta(get_test_dir_name()+"/inputs/test_ID_only.txt",False)

    def test_class_method_ProcessFASTA_get_fasta_ID_only_single(self):

        with self.assertRaises(Exception) : ProcessFasta(get_test_dir_name()+"/inputs/test_ID_only_single.txt",False)

if __name__ == '__main__':
    unittest.main()
