import re

class fasta_sequence:
    def __init__(self, sequence, ID):
        self.ID = ID
        self.sequence = sequence


def read_fasta(inputfile) -> object:
    read_file_array = []

    with open(inputfile, "r") as fasta:
        for line in fasta:
            read_file_array.append(line.replace("\n", ""))

    return read_file_array


def combine_split_sequences(fasta_array):

    def find_end_of_sequence(array_test):
        for item in array_test:
            if item.startswith(">"):
                return True
            elif re.match(r'^\s*$', item):
                return True
            else:
                return False

    combined_array = []

    for index in range(0,len(fasta_array)):

        current_item = fasta_array[index]

        if current_item.startswith(">"):
            combined_array.append(current_item)
        else:
            while find_end_of_sequence(fasta_array[index:]):
                combined_array.append(fasta_array[index])
                index += 1

    return combined_array











class ProcessFasta():

    def __init__(self, inputfile, single):
        self.inputfile = inputfile
        self.single = single

        self.fasta_array = self.get_fasta()

    def get_fasta(self):
        fasta_array = read_fasta(self.inputfile)
        return combine_split_sequences(fasta_array)
