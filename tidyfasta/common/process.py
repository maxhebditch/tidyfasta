import pathlib
import re

class fasta_sequence:
    def __init__(self, ID, sequence):
        self.ID = ID
        self.sequence = sequence

def identify_line_type(item):
    item = item.strip()
    if item.startswith(">"):
        return "ID"
    elif re.match(r"^\s*$", item):
        return "WHITESPACE"
    elif re.match(r"[a-zA-Z0-9]", item):
        return "SEQUENCE"

def read_fasta(inputfile) -> object:

    if not pathlib.Path(inputfile).exists():
        raise Exception("Path " + str(inputfile) + " doesn't exist")

    read_file_array = []

    with open(inputfile, "r") as fasta:
        for line in fasta:
            read_file_array.append(line.replace("\n", ""))

    if not read_file_array:
        raise Exception("No data in file")

    return read_file_array


def combine_split_sequences(fasta_array):

    def end_of_sequence(item):
        if identify_line_type(item) == "ID":
            return True
        elif identify_line_type(item) == "SEQUENCE":
            return False
        else:
            return True

    combined_array = []
    combiner = []

    for item in fasta_array:
        if end_of_sequence(item):
            if len(combiner) > 0:
                combined_array.append("".join(combiner))
                combiner.clear()
            combined_array.append(item)
        else:
            combiner.append(item)
    if combiner:
        combined_array.append("".join(combiner))

    if not combined_array:
        raise Exception("Combined array not generated")

    return combined_array

def remove_excess_whitespace(fasta_array):

    def is_sequence_or_id(item):
        if identify_line_type(item) == "ID":
            return True
        elif identify_line_type(item) == "SEQUENCE":
            return True
        else:
            return False

    cleaned_array = []
    index = 0

    while index < len(fasta_array):
        if is_sequence_or_id(fasta_array[index]):
            cleaned_array.append(fasta_array[index].strip())
            index += 1
        else:
            index += 1
            for item in fasta_array[index:]:
                if not is_sequence_or_id(item):
                    index += 1
                else:
                    break

    if not cleaned_array:
        raise Exception("Cleaned array not generated")

    return cleaned_array

def add_missing_names(fasta_array):

    named_array = []
    new_name_int = 0
    unknown_name = True

    for item in fasta_array:

        if item.startswith(">"):
            named_array.append(item)
            unknown_name = False

        elif re.match(r'^\s*$', item):
            new_name = "> sequence"+str(new_name_int)
            new_name_int += 1
            unknown_name = False
            named_array.append(new_name)

        elif re.match('^[a-zA-Z]', item):

            if unknown_name:
                new_name = "> sequence" + str(new_name_int)
                new_name_int += 1
                named_array.append(new_name)

            named_array.append(item)
            unknown_name = True

    if not named_array:
        raise Exception("Named array issue")
    if len(named_array) % 2 == 1:
        raise Exception("Unpaired ID and sequence")

    return named_array

def convert_to_obj_array(fasta_array):

    def test_item_pair(fasta_array, index):

        if not fasta_array[index].startswith(">"):
            return False
        elif not re.match(r"^[a-zA-Z]", fasta_array[index + 1]):
            return False
        else:
            return True

    object_array = []
    index = 0

    if len(fasta_array) % 2 == 1:
        raise Exception("Unpaired ID and sequence")

    while index < len(fasta_array):
        if test_item_pair(fasta_array, index):
            object_array.append(fasta_sequence(fasta_array[index], fasta_array[index + 1]))
            index += 2
        else:
            raise Exception("Unpaired ID and sequence")

    if not object_array:
        raise Exception("Object array failed")

    return object_array

def test_ID_sequence(fasta_array):

    if not fasta_array:
        raise Exception("Input array empty")

    for fasta_object in fasta_array:

        fasta_object.sequence = fasta_object.sequence.upper()

        if re.match(r"XZUOJ", fasta_object.sequence):
            raise Exception("Non canonical amino acids detected")


class ProcessFasta():

    def __init__(self, inputfile, single):
        self.inputfile = inputfile
        self.single = single

        self.fasta_array = self.get_fasta()
        self.validate_FASTA()

    def get_fasta(self):
        try:
            fasta_array = read_fasta(self.inputfile)
            fasta_array = combine_split_sequences(fasta_array)
            fasta_array = remove_excess_whitespace(fasta_array)
            fasta_array = add_missing_names(fasta_array)
            fasta_array = convert_to_obj_array(fasta_array)
        except:
            raise(ValueError)
        return fasta_array

    def validate_FASTA(self):
        try:
            test_ID_sequence(self.fasta_array)
        except:
            raise(ValueError)
