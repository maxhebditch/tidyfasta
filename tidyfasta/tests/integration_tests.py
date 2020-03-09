import unittest
import filecmp

from tidyfasta.common.process import *

def get_test_dir():
    return os.path.dirname(os.path.realpath(__file__))

class IntegrationTests(unittest.TestCase):

    def test_class_method_ProcessFASTA_get_fasta_gold_standard(self):

        input_file = get_test_dir() + "/inputs/test_gold_standard.txt"
        output_file = get_outputfile(input_file)

        new = ProcessFasta(input_file, False, False)
        new.write_FASTA()

        try:
            renamed_file = get_test_dir() + "/outputs/test_gold_standard.txt"
            os.rename(output_file, renamed_file)

            standard_file = get_test_dir() + "/standards/test_gold_standard.txt"

            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)

    def test_class_method_ProcessFASTA_get_fasta_gold_standard(self):

        input_file = get_test_dir() + "/inputs/test_gold_standard_multiple.txt"
        output_file = get_outputfile(input_file)

        new = ProcessFasta(input_file, False, False)
        new.write_FASTA()

        try:
            renamed_file = get_test_dir() + "/outputs/test_gold_standard_multiple.txt"
            os.rename(output_file, renamed_file)

            standard_file = get_test_dir() + "/standards/test_gold_standard_multiple.txt"

            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)



    def test_class_method_ProcessFASTA_get_fasta_ID_only(self):

        with self.assertRaises(Exception) : ProcessFasta(get_test_dir() + "/inputs/test_ID_only.txt", False, False)

    def test_class_method_ProcessFASTA_get_fasta_ID_only_single(self):

        with self.assertRaises(Exception) : ProcessFasta(get_test_dir() + "/inputs/test_ID_only_single.txt",
                                                         False, False)

if __name__ == '__main__':
    unittest.main()
