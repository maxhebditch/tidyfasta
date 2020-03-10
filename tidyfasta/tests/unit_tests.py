import unittest
import os

from tidyfasta.common.process import *
from tidyfasta.tests.integration_tests import get_test_dir

class UnitTests(unittest.TestCase):

    def test_func_read_fasta(self):

        test_array = read_fasta(get_test_dir()+"/inputs/test_gold_short.txt")
        ref_array = ["> alirocumab","MVKVYAPASSANMSVGFDVL","GAAVTPVDG"]

        self.assertEqual(ref_array, test_array)

    def test_func_read_fasta_path_not_exists(self):

        with self.assertRaisesRegex(Exception, "doesn't exist") : read_fasta("I_DONT_EXIST.txt")

    def test_func_read_fasta_empty(self):

        with self.assertRaisesRegex(Exception, "No data in file") : read_fasta(get_test_dir()+"/inputs/test_empty.txt")

    def test_func_read_fasta_not_str(self):

        with self.assertRaisesRegex(TypeError, "not int") : read_fasta(0)

    def test_func_read_fasta_excess_whitespace_multi(self):

        input_array = read_fasta(get_test_dir()+"/inputs/test_excess_whitespace_multi.txt")
        test_array = remove_whitespace(input_array)

        ref_array = ["> alirocumab1", "MVKVYAPASSANMSVGFDVLGAA",
                    "> alirocumab2", "MVKVYAPASSANMSVGFDVLGAA",
                    "> alirocumab3", "MVKVYAPASSANMSVGFDVLGAA"]

        self.assertEqual(ref_array, test_array)

    def test_func_remove_excess_whitespace(self):

        input_array = ["> alirocumab1", " ", "MVKVYAPASSANMSVGFDVLGAA",
                     "   > alirocumab2", "   MVKVYAPASSANMSVGFDVLGAA",
                     "> alirocumab3   ", "MVKVYAPASSANMSVGFDVLGAA", "", " ", " "]

        test_array = remove_whitespace(input_array)

        ref_array = ["> alirocumab1", "MVKVYAPASSANMSVGFDVLGAA",
                     "> alirocumab2", "MVKVYAPASSANMSVGFDVLGAA",
                     "> alirocumab3", "MVKVYAPASSANMSVGFDVLGAA"]

        self.assertEqual(ref_array, test_array)

    def test_func_remove_excess_whitespace_empty_input(self):

        with self.assertRaisesRegex(Exception, "Cleaned array not generated") : remove_whitespace([])

    def test_func_combine_split_sequences(self):

        input_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVL", "GAAVTPVDG", " ", ">SEQ 2", "ATYYTYTY"]
        test_array = combine_split_sequences(input_array)
        ref_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVLGAAVTPVDG", " ", ">SEQ 2", "ATYYTYTY"]

        self.assertEqual(ref_array, test_array)

    def test_func_combine_split_sequences_empty(self):

        with self.assertRaisesRegex(Exception, "Combined array not generated") : combine_split_sequences([])

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

        obj0 = FastaSequence("> alirocumab", "MVKVYAPASSANMSVGFDVL")
        obj1 = FastaSequence("> sequence1", "GGGGGGGG")

        self.assertEqual(test_array[0].id, obj0.id)
        self.assertEqual(test_array[1].id, obj1.id)
        self.assertEqual(test_array[0].sequence, obj0.sequence)
        self.assertEqual(test_array[1].sequence, obj1.sequence)

    def test_func_convert_to_obj_unpaired(self):

        with self.assertRaisesRegex(Exception, "Unpaired ID and sequence") \
                : convert_to_obj_array([">DOG", "AAAAAA", ">CAT"])

    def test_func_convert_to_obj_empty(self):

        with self.assertRaisesRegex(Exception, "Object array failed") : convert_to_obj_array([])

    def test_func_validate_input(self):

        with self.assertRaisesRegex(Exception, "No valid AA in input") : test_id_sequence(True, [])

    def test_func_validate_id_sequence_upper(self):

        test_array = convert_to_obj_array(["> alirocumab", "aaaaaaaaaaaaaaaaaaa"])
        valid_array = test_id_sequence(False, test_array)

        self.assertEqual("> alirocumab", valid_array[0].id)
        self.assertEqual("AAAAAAAAAAAAAAAAAAA", valid_array[0].sequence)

    def test_func_validate_id_sequence_bad_ID(self):

        test_array = convert_to_obj_array(["> alir<cumab", "AAAAAAKKKKK"])
        with self.assertRaisesRegex(Exception, "Bad characters in ID") : test_id_sequence(True, test_array)

    def test_func_validate_id_sequence_bad_AA(self):

        test_array = convert_to_obj_array(["> alirocumab", "AAAAAAXXXKKKKKK"])
        with self.assertRaisesRegex(Exception, "Non canonical amino acids") : test_id_sequence(True, test_array)

    def test_func_validate_id_sequence_bad_AA_numbers(self):

        test_array = convert_to_obj_array(["> alirocumab", "aaaaaa1KKKKK"])
        with self.assertRaisesRegex(Exception, "Non canonical amino acids") : test_id_sequence(True, test_array)

    def test_func_validate_id_sequence_bad_AA_space(self):

        test_array = convert_to_obj_array(["> alirocumab", "AAAAA KKKKK"])
        with self.assertRaisesRegex(Exception, "Non canonical amino acids") : test_id_sequence(True, test_array)

    def test_func_validate_id_sequence_bad_AA_numbers_nonstrict(self):

        test_array = convert_to_obj_array(["> alirocumab", "AAAAAAK1KKKK",
                                           "> secondone", "TTTTTTTT"])
        valid_array = test_id_sequence(False, test_array)

        self.assertEqual(len(valid_array), 1)

    def test_func_test_strict_validation_ok(self):

        input_array  = ["> alirocumab", "GGGGGGGGGGG", "> secondone", "DDDDDDDD"]
        test_array = convert_to_obj_array(input_array)
        output_array = test_id_sequence(True, test_array)

        self.assertEqual(test_array, output_array)

    def test_func_test_single(self):

        test_array = convert_to_obj_array(["> alirocumab", "GGGGGGGGGGG",
                                           "> secondone", "DDDDDDDD"])
        test_array = test_id_sequence(False, test_array)

        with self.assertRaisesRegex(Exception, "More than 1 sequence present") : check_single(True, test_array)

    def test_func_write_FASTA(self):

        test_array = convert_to_obj_array(["> alirocumab", "AAAAAAKKKKK",
                                           "> secondone", "TTTTTTTT"])
        write_fasta(get_test_dir() + "/outputs/test-write.txt", test_array)

        output_file = get_test_dir() + "/outputs/tidied-test-write.txt"

        try:
            path_exists = os.path.exists(output_file)
            self.assertEqual(1, path_exists)
        finally:
            os.remove(output_file)

    def test_class_method_ProcessFASTA_get_fasta_gold_standard(self):

        test_processfasta = ProcessFasta(get_test_dir() + "/inputs/test_gold_standard.txt", False, False)

        test_processfasta.get_fasta()
        valid_array = test_processfasta.validate_fasta()

        self.assertEqual("> alirocumab", valid_array[0].id)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAAVTPVDGALLGDVVTVEAAETF", valid_array[0].sequence)

    def test_class_method_ProcessFASTA_get_fasta_excess_whitespace_multi(self):

        test_processfasta = ProcessFasta(get_test_dir() + "/inputs/test_excess_whitespace_multi.txt", False, False)

        test_processfasta.get_fasta()
        valid_array = test_processfasta.validate_fasta()

        self.assertEqual("> alirocumab1", valid_array[0].id)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAA", valid_array[0].sequence)
        self.assertEqual("> alirocumab2", valid_array[1].id)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAA", valid_array[1].sequence)
        self.assertEqual("> alirocumab3", valid_array[2].id)
        self.assertEqual("MVKVYAPASSANMSVGFDVLGAA", valid_array[2].sequence)

    def test_class_method_ProcessFASTA_get_fasta_ID_only(self):

        fasta_array = read_fasta(get_test_dir() + "/inputs/test_ID_only.txt")
        with self.assertRaisesRegex(Exception, "ID without sequence") : convert_to_obj_array(fasta_array)

    def test_class_method_ProcessFASTA_get_fasta_ID_only_single(self):

        fasta_array = read_fasta(get_test_dir() + "/inputs/test_ID_only_single.txt")
        with self.assertRaisesRegex(Exception, "Unpaired ID and sequence") : convert_to_obj_array(fasta_array)


if __name__ == '__main__':
    unittest.main()
