import unittest

from tidyfasta.common.process import *
from tidyfasta.tests.integration_tests import get_test_dir

class UnitTests(unittest.TestCase):

    def test_func_read_fasta(self):

        test_array = read_fasta(get_test_dir()+"/inputs/test_gold_short.txt")
        ref_array = ["> alirocumab","MVKVYAPASSANMSVGFDVL","GAAVTPVDG"]

        self.assertEqual(ref_array, test_array)

    def test_func_read_fasta_empty(self):

        with self.assertRaises(Exception) : read_fasta(get_test_dir()+"/inputs/test_empty.txt")

    def test_func_read_fasta_not_str(self):

        with self.assertRaises(Exception) : read_fasta(0)

    def test_func_read_fasta_path_not_exists(self):

        with self.assertRaises(Exception) : read_fasta("I_DONT_EXIST.txt")

    def test_func_read_fasta_excess_whitespace_multi(self):

        input_array = read_fasta(get_test_dir()+"/inputs/test_excess_whitespace_multi.txt")
        test_array = remove_excess_whitespace(input_array)

        ref_array = ["> alirocumab1", "MVKVYAPASSANMSVGFDVLGAA",
                    "> alirocumab2", "MVKVYAPASSANMSVGFDVLGAA",
                    "> alirocumab3", "MVKVYAPASSANMSVGFDVLGAA"]

        self.assertEqual(ref_array, test_array)

    def test_func_remove_excess_whitespace(self):

        input_array = ["> alirocumab1", " ", "MVKVYAPASSANMSVGFDVLGAA",
                     "   > alirocumab2", "   MVKVYAPASSANMSVGFDVLGAA",
                     "> alirocumab3   ", "MVKVYAPASSANMSVGFDVLGAA", "", " ", " "]

        test_array = remove_excess_whitespace(input_array)

        ref_array = ["> alirocumab1", "MVKVYAPASSANMSVGFDVLGAA",
                     "> alirocumab2", "MVKVYAPASSANMSVGFDVLGAA",
                     "> alirocumab3", "MVKVYAPASSANMSVGFDVLGAA"]

        self.assertEqual(ref_array, test_array)

    def test_func_remove_excess_whitespace_empty_input(self):

        with self.assertRaises(Exception) : remove_excess_whitespace([])

    def test_func_combine_split_sequences(self):

        input_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVL", "GAAVTPVDG", " ", ">SEQ 2", "ATYYTYTY"]
        test_array = combine_split_sequences(input_array)
        ref_array = ["> alirocumab", "MVKVYAPASSANMSVGFDVLGAAVTPVDG", " ", ">SEQ 2", "ATYYTYTY"]

        self.assertEqual(ref_array, test_array)

    def test_func_combine_split_sequences_empty(self):

        with self.assertRaises(Exception) : combine_split_sequences([])

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

    def test_func_convert_to_obj_not_list(self):

        with self.assertRaises(Exception) : convert_to_obj_array("DOG")

    def test_func_convert_to_obj_empty(self):

        with self.assertRaises(Exception) : convert_to_obj_array([])

    def test_func_convert_to_obj_unpaired(self):

        with self.assertRaises(Exception) : convert_to_obj_array([">DOG", "AAAAAA", ">CAT"])

    def test_func_validate_input(self):

        with self.assertRaises(Exception) : test_ID_sequence([])

    def test_func_validate_id_sequence_upper(self):

        test_array = convert_to_obj_array(["> alirocumab", "aaaaaaaaaaaaaaaaaaa"])
        valid_array = test_ID_sequence(False, False, test_array)

        self.assertEqual("> alirocumab", valid_array[0].ID)
        self.assertEqual("AAAAAAAAAAAAAAAAAAA", valid_array[0].sequence)

    def test_func_validate_id_sequence_bad_AA(self):

        test_array = convert_to_obj_array(["> alirocumab", "AAAAAAXXXKKKKKK"])

        with self.assertRaises(Exception) : test_ID_sequence(test_array)

    def test_func_validate_id_sequence_bad_AA_numbers(self):

        test_array = convert_to_obj_array(["> alirocumab", "aaaaaa1KKKKK"])

        with self.assertRaises(Exception) : test_ID_sequence(False, True, test_array)

    def test_func_validate_id_sequence_bad_AA_space(self):

        test_array = convert_to_obj_array(["> alirocumab", "AAAAA KKKKK"])

        with self.assertRaises(Exception) : test_ID_sequence(False, True, test_array)

    def test_func_validate_id_sequence_bad_AA_numbers_nonstrict(self):

        test_array = convert_to_obj_array(["> alirocumab", "AAAAAAK1KKKK",
                                           "> secondone", "TTTTTTTT"])

        valid_array = test_ID_sequence(False, False, test_array)

        self.assertEqual(len(valid_array), 1)

    def test_func_test_single(self):

        test_array = convert_to_obj_array(["> alirocumab", "AAAAAAKKKKK",
                                           "> secondone", "TTTTTTTT"])

        with self.assertRaises(Exception) : test_ID_sequence(True, True, test_array)

    def test_func_write_FASTA(self):

        test_array = convert_to_obj_array(["> alirocumab", "AAAAAAKKKKK",
                                           "> secondone", "TTTTTTTT"])
        write_FASTA(get_test_dir() + "/outputs/test-write.txt", test_array)

        output_file = get_test_dir() + "/outputs/tidied-test-write.txt"

        assert(os.path.exists(output_file))

        os.remove(output_file)

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

        with self.assertRaises(Exception) : ProcessFasta(get_test_dir() + "/inputs/test_ID_only_single.txt",
                                                         False, False)

if __name__ == '__main__':
    unittest.main()
