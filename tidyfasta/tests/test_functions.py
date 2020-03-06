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

        self.assertTrue(test_array,ref_array)

    def test_func_combine_split_sequences(self):

        input_array = ["> alirocumab","MVKVYAPASSANMSVGFDVL","GAAVTPVDG"," ",">SEQ 2","ATYYTYTY"]
        test_array = combine_split_sequences(input_array)
        ref_array = ["> alirocumab","MVKVYAPASSANMSVGFDVLGAAVTPVDG",">SEQ 2","ATYYTYTY"]

        self.assertTrue(test_array,ref_array)

