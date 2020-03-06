import unittest
import filecmp

import os
import sys

from tidyfasta.common.process import *

def get_test_dir_name():
    return os.path.dirname(os.path.realpath(__file__))

class TestFunctions(unittest.TestCase):

    def test_func_read_fasta(self):

        test_array = read_fasta(get_test_dir_name()+"/inputs/test_gold_short.txt")
        ref_array = ["> alirocumab","MVKVYAPASSANMSVGFDVL","GAAVTPVDG"]

        self.assertEqual(ref_array, test_array)

    def test_func_combine_split_sequences(self):

        input_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVL", "GAAVTPVDG", " ", ">SEQ 2", "ATYYTYTY"]
        test_array = combine_split_sequences(input_array)
        ref_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVLGAAVTPVDG", " ", ">SEQ 2", "ATYYTYTY"]

        self.assertEqual(ref_array, test_array)

    def test_class_method_ProcessFasta_get_fasta(self):

        test_file = get_test_dir_name()+"/inputs/test_gold_short.txt"

        test_ProcessFasta = ProcessFasta(test_file, False)

        test_array = test_ProcessFasta.get_fasta()
        ref_array = ['> alirocumab', 'MVKVYAPASSANMSVGFDVLGAAVTPVDG']

        self.assertEqual(ref_array, test_array)

    def test_class_method_ProcessFasta_get_fasta_missing_id(self):

        test_file = get_test_dir_name()+"/inputs/test_missing_id.txt"

        test_ProcessFasta = ProcessFasta(test_file, False)

        test_array = test_ProcessFasta.get_fasta()
        ref_array = ['> sequence0', 'MVKVYAPASSANMSVGFDVLGAAVTPVDG']

        self.assertEqual(ref_array, test_array)

    def test_class_method_ProcessFasta_get_fasta_missing_id_multi(self):

        test_file = get_test_dir_name()+"/inputs/test_missing_id_multi.txt"

        test_ProcessFasta = ProcessFasta(test_file, False)

        test_array = test_ProcessFasta.get_fasta()
        ref_array = ['> sequence0', 'MVKVYAPASSANMSVGFDVLGAAVTPVDG',
                     '> sequence1', 'MVKVYAPASSANMSVGFDVLGAAVTPVDG',
                     '> sequence2', 'MVKVYAPASSANMSVGFDVLGAAVTPVDG']

        self.assertEqual(ref_array, test_array)

    def test_add_missing_names(self):

        input_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVL",
                       " ", "ATYYTYTY",
                       "> NAMED", "ATYYTYTY",
                       " ", "GGGGGGGG"]

        test_array = add_missing_names(input_array)

        ref_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVL",
                       "> sequence0", "ATYYTYTY",
                       "> NAMED", "ATYYTYTY",
                       "> sequence1", "GGGGGGGG"]

        self.assertEqual(ref_array, test_array)

if __name__ == '__main__':
    unittest.main()
