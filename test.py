import unittest
import filecmp

import os
import sys

from run_tidy import run_tidy

def get_dir_name():
    return os.path.dirname(os.path.realpath(__file__))+"/tests"

def set_up_files(testfile_name):
    original_name = get_dir_name()+"/inputs/" + testfile_name + ".txt"
    intermediate_name = get_dir_name()+"/inputs/" + testfile_name + ".txt-old"
    reference_name = get_dir_name()+"/outputs/" + testfile_name + ".txt"
        
    return original_name, intermediate_name, reference_name

def tidy_up_files(original_name,intermediate_name):
        os.remove(original_name)
        os.rename(intermediate_name,original_name)

def assert_test_match(self,testfile_name,single):
    original_name, intermediate_name, reference_name = set_up_files(testfile_name)

    run_tidy(original_name,single)

    try:
        self.assertTrue(filecmp.cmp(original_name, reference_name, shallow=False))
    finally:
        tidy_up_files(original_name,intermediate_name)


class TestSum(unittest.TestCase):

    def test_gold_standard(self):

        assert_test_match(self,"test_gold_standard",False)

    def test_gold_standard_multiple(self):

        assert_test_match(self,"test_gold_standard_multiple",False)

    def test_missing_name(self):

        assert_test_match(self,"test_missing_name",False)

    def test_multiple_sequences_nonames(self):

        assert_test_match(self,"test_multiple_sequences_nonames",False)

    def test_broken_lines(self):

        assert_test_match(self,"test_broken_lines",False)

    def test_broken_lines_multiple(self):

        assert_test_match(self,"test_broken_lines_multiple",False)

    def test_lowercase(self):

        assert_test_match(self,"test_lowercase",False)

    def test_excess_whitespace_end(self):

        assert_test_match(self,"test_excess_whitespace_end",False)

    def test_excess_whitespace_mid(self):

        assert_test_match(self,"test_excess_whitespace_mid",False)

    def test_weird_id_name(self):

        assert_test_match(self,"test_excess_whitespace_mid",False)

    def test_bad_chars_sequence(self):
        original_name     = get_dir_name()+"/inputs/test_bad_chars_sequence.txt"

        with self.assertRaises(ValueError):
            run_tidy(original_name,False)

    def test_bad_no_sequence(self):
        original_name     = get_dir_name()+"/inputs/test_no_sequence.txt"

        with self.assertRaises(ValueError):
            run_tidy(original_name,False)

    def test_bad_no_sequence_multiple(self):
        original_name     = get_dir_name()+"/inputs/test_no_sequence_multiple.txt"

        with self.assertRaises(ValueError):
            run_tidy(original_name,False)

    def test_single_check(self):
        original_name     = get_dir_name()+"/inputs/test_gold_standard_multiple.txt"

        with self.assertRaises(ValueError):
            run_tidy(original_name,True)

if __name__ == '__main__':
    unittest.main()
