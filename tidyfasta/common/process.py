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


class ProcessFasta():

    def __init__(self, inputfile, single):
        self.inputfile = inputfile
        self.single = single

        fasta_array = read_fasta(inputfile)
