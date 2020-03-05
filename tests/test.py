import importlib.util

import unittest
import filecmp

import os

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

tidy_fasta = module_from_file("tidy_fasta", "../tidy_fasta/tidy_fasta.py")

class TestSum(unittest.TestCase):

    def test_missing_name(self):
        original_name     = "./inputs/test_missing_name.txt"
        intermediate_name = "./inputs/test_missing_name.txt-old"
        output_name       = "./inputs/test_missing_name.txt_output"
        reference_name    = "./outputs/test_missing_name.txt"

        tidy_fasta.tidy_fasta(original_name,False)

        self.assertTrue(filecmp.cmp(original_name, reference_name, shallow=False),"test for missing name failed")

        os.remove(original_name)
        os.rename(intermediate_name,original_name)

if __name__ == '__main__':
    unittest.main()
