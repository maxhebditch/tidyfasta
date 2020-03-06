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

    combined_array = []
    combiner = []

    for item in fasta_array:
        if item.startswith(">"):
            if len(combiner) > 0:
                combined_array.append("".join(combiner))
                combiner.clear()
            combined_array.append(item)
        else:
            combiner.append(item.strip())
    combined_array.append("".join(combiner))

    return combined_array


def add_missing_names(fasta_array):

    named_array = []
    new_name_int = 0

    for index in range(0, fasta_array):
        current_item = fasta_array[index]

        if current_item.startswith(">"):
            named_array.append(current_item)
        else:
            if index % 2 == 0:
                new_name = "> sequence"+new_name_int
                named_array.append(new_name)
                named_array.append(current_item)
                new_name_int += 1
            else:
                named_array.append(current_item)














class ProcessFasta():

    def __init__(self, inputfile, single):
        self.inputfile = inputfile
        self.single = single

        self.fasta_array = self.get_fasta()

    def get_fasta(self):
        fasta_array = read_fasta(self.inputfile)
        fasta_array = combine_split_sequences(fasta_array)
        return fasta_array
