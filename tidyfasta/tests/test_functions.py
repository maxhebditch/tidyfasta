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

    def test_func_read_fasta_empty(self):

        with self.assertRaises(Exception) : read_fasta(get_test_dir_name()+"/inputs/test_empty.txt")

    def test_func_read_fasta_not_str(self):

        with self.assertRaises(Exception) : read_fasta(0)

    def test_func_read_fasta_path_not_exists(self):

        with self.assertRaises(Exception) : read_fasta("I_DONT_EXIST.txt")

    def test_func_read_fasta_excess_whitespace_multi(self):

        input_array = read_fasta(get_test_dir_name()+"/inputs/test_excess_whitespace_multi.txt")
        test_array = remove_excess_whitespace(input_array)

        ref_array = ["> alirocumab1", "MVKVYAPASSANMSVGFDVLGAA",
                    "> alirocumab2", "MVKVYAPASSANMSVGFDVLGAA",
                    "> alirocumab3", "MVKVYAPASSANMSVGFDVLGAA"]

        self.assertEqual(ref_array, test_array)

    def test_func_combine_split_sequences(self):

        input_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVL", "GAAVTPVDG", " ", ">SEQ 2", "ATYYTYTY"]
        test_array = combine_split_sequences(input_array)
        ref_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVLGAAVTPVDG", " ", ">SEQ 2", "ATYYTYTY"]

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

    def test_add_missing_names_uneven(self):

        input_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVL",
                       " ", "ATYYTYTY",
                       "ATYYTYTY"]

        test_array = add_missing_names(input_array)
        ref_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVL",
                     "> sequence0", "ATYYTYTY",
                     "> sequence1", "ATYYTYTY"]

        self.assertEqual(ref_array, test_array)


    def test_convert_to_object_array(self):

        input_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVL",
                     "> sequence1", "GGGGGGGG"]

        test_array = convert_to_obj_array(input_array)

        obj0 = fasta_sequence("> alirocumab", "MVKVYAPASSANMSVGFDVL")
        obj1 = fasta_sequence("> sequence1", "GGGGGGGG")

        self.assertEqual(test_array[0].ID, obj0.ID)
        self.assertEqual(test_array[1].ID, obj1.ID)
        self.assertEqual(test_array[0].sequence, obj0.sequence)
        self.assertEqual(test_array[1].sequence, obj1.sequence)

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


if __name__ == '__main__':
    unittest.main()
