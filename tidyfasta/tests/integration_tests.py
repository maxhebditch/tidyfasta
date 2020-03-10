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

        renamed_file = get_test_dir() + "/outputs/test_broken_lines.txt"
        os.rename(output_file, renamed_file)

        standard_file = get_test_dir() + "/standards/test_broken_lines.txt"

        try:
            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)

    def test_ProcessFASTA_broken_lines_multi(self):

        input_file = get_test_dir() + "/inputs/test_broken_lines_multiple.txt"
        output_file = get_outputfile(input_file)

        new = ProcessFasta(input_file, False, False)
        new.write_FASTA()

        renamed_file = get_test_dir() + "/outputs/test_broken_lines_multiple.txt"
        os.rename(output_file, renamed_file)

        standard_file = get_test_dir() + "/standards/test_broken_lines_multiple.txt"

        try:
            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)

    def test_ProcessFASTA_broken_lines_multi_single(self):

        input_file = get_test_dir() + "/inputs/test_broken_lines_multiple.txt"
        output_file = get_outputfile(input_file)

        new = ProcessFasta(input_file, True, False)
        new.write_FASTA()

        renamed_file = get_test_dir() + "/outputs/test_broken_lines_multiple.txt"
        os.rename(output_file, renamed_file)

        standard_file = get_test_dir() + "/standards/test_broken_lines_multiple.txt"

        try:
            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)

    def test_ProcessFASTA_excess_whitespace(self):

        input_file = get_test_dir() + "/inputs/test_excess_whitespace_end.txt"
        output_file = get_outputfile(input_file)

        new = ProcessFasta(input_file, True, False)
        new.write_FASTA()

        renamed_file = get_test_dir() + "/outputs/test_excess_whitespace_end.txt"
        os.rename(output_file, renamed_file)

        standard_file = get_test_dir() + "/standards/test_excess_whitespace_end.txt"

        try:
            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)

    def test_ProcessFASTA_excess_whitespace_mid(self):

        input_file = get_test_dir() + "/inputs/test_excess_whitespace_mid.txt"
        output_file = get_outputfile(input_file)

        new = ProcessFasta(input_file, False, False)
        new.write_FASTA()

        renamed_file = get_test_dir() + "/outputs/test_excess_whitespace_mid.txt"
        os.rename(output_file, renamed_file)

        standard_file = get_test_dir() + "/standards/test_excess_whitespace_mid.txt"

        try:
            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)

    def test_ProcessFASTA_missing_name(self):

        input_file = get_test_dir() + "/inputs/test_missing_name.txt"
        output_file = get_outputfile(input_file)
        new = ProcessFasta(input_file, False, False)
        new.write_FASTA()

        renamed_file = get_test_dir() + "/outputs/test_missing_name.txt"
        os.rename(output_file, renamed_file)

        standard_file = get_test_dir() + "/standards/test_missing_name.txt"

        try:
            self.assertTrue(filecmp.cmp(renamed_file, standard_file, shallow=False))
        finally:
            os.remove(renamed_file)

if __name__ == '__main__':
    unittest.main()
