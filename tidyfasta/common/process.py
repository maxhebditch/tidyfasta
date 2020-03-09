import pathlib
import re
import os

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
            raise Exception("Issue generating object array")

    if not object_array:
        raise Exception("Object array failed")

    return object_array

def test_ID_sequence(single, strict, fasta_array):

    if not fasta_array:
        raise Exception("Input array empty")

    if single and len(fasta_array) > 1:
        raise Exception("More than 1 sequence present and single mode activated")

    validated_array = []
    non_canonical_AA = re.compile(r"[^ACDEFGHIKLMNPQRSTVWY]")

    for fasta_object in fasta_array:

        fasta_object.sequence = fasta_object.sequence.upper()

        if non_canonical_AA.search(fasta_object.sequence):
            if strict:
                raise Exception("Non canonical amino acids detected and strict mode activated")
        else:
            validated_array.append(fasta_object)

    if len(validated_array) == 0:
        raise Exception("No valid AA in input")

    return validated_array

def write_FASTA(inputfile, validated_array):

    def get_outputfile(inputfile):
        split_path = os.path.split(inputfile)

        if not os.path.exists(split_path[0]):
            raise Exception("Output location: " + split_path[0] + " does not exist")

        candidate_output_file = split_path[0]+"/tidied-"+split_path[1]

        if os.path.exists(candidate_output_file):
            unix_timestamp = datetime.datetime.now()
            os.rename(candidate_output_file, split_path[0]+"/tidied-"+str(unix_timestamp)+"-"+split_path[1])

        return candidate_output_file

    outputfile = get_outputfile(inputfile)


    with open(outputfile, "w") as output:
        for index, object in enumerate(validated_array):
            output.write(object.ID+"\n")
            if index == len(validated_array):
                output.write(object.sequence+"\n")
            else:
                output.write(object.sequence+"\n\n")


class ProcessFasta():

    def __init__(self, inputfile, single, strict):
        self.inputfile = inputfile
        self.single = single
        self.strict = strict

        self.fasta_array = self.get_fasta()
        self.validated_array = self.validate_FASTA()

    def get_fasta(self):
        try:
            fasta_array = read_fasta(self.inputfile)
            fasta_array = combine_split_sequences(fasta_array)
            fasta_array = remove_excess_whitespace(fasta_array)
            fasta_array = add_missing_names(fasta_array)
        except:
            raise(ValueError)
        return fasta_array

    def validate_FASTA(self):
        try:
            object_array = convert_to_obj_array(self.fasta_array)
            validated_array = test_ID_sequence(self.single, self.strict, object_array)
        except:
            raise(ValueError)
        return validated_array

    def write_FASTA(self):
        try:
            write_FASTA(self.inputfile, self.validated_array)
        except:
            raise(ValueError)
