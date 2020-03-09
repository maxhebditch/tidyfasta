import unittest
import filecmp

from tidyfasta.common.process import *

def get_test_dir():
    return os.path.dirname(os.path.realpath(__file__))

class IntegrationTests(unittest.TestCase):

    def test_ProcessFASTA_broken_lines(self):

        input_file = get_test_dir() + "/inputs/test_broken_lines.txt"
        output_file = get_outputfile(input_file)

        new = ProcessFasta(input_file, False, False)
        new.write_FASTA()

        try:
            renamed_file = get_test_dir() + "/outputs/test_broken_lines.txt"
            os.rename(output_file, renamed_file)

            standard_file = get_test_dir() + "/standards/test_broken_lines.txt"

            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)

    def test_ProcessFASTA_broken_lines_multi(self):

        input_file = get_test_dir() + "/inputs/test_broken_lines_multiple.txt"
        output_file = get_outputfile(input_file)

        new = ProcessFasta(input_file, False, False)
        new.write_FASTA()

        try:
            renamed_file = get_test_dir() + "/outputs/test_broken_lines_multiple.txt"
            os.rename(output_file, renamed_file)

            standard_file = get_test_dir() + "/standards/test_broken_lines_multiple.txt"

            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)

    def test_ProcessFASTA_broken_lines_multi_single(self):

        input_file = get_test_dir() + "/inputs/test_broken_lines_multiple.txt"
        output_file = get_outputfile(input_file)

        new = ProcessFasta(input_file, True, False)
        new.write_FASTA()

        try:
            renamed_file = get_test_dir() + "/outputs/test_broken_lines_multiple.txt"
            os.rename(output_file, renamed_file)

            standard_file = get_test_dir() + "/standards/test_broken_lines.txt"

            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)





if __name__ == '__main__':
    unittest.main()
