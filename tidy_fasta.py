#!/usr/bin/env python
# coding: utf-8

import re
import argparse
from shutil import copy2

def read_fasta(inputfile):

    read_file_array = []
    badAA = False

    with open (inputfile, "r") as fasta:
        for idx, line in enumerate(fasta):
            if not line.startswith(">") and re.match("^[bjouxBJOUX]+.*", line):
                print(f"Unrecognised amino acids at line {idx}")
                print(re.match("^[bjouxBJOUX]+.*", line)[0])
                badAA = True
            else:
                read_file_array.append(line.replace("\n",""))

    if badAA:
        raise ValueError("Non-standard AA included")

    return read_file_array


def remove_blanks(original_array):

    tidy_array = []

    for idx, line in enumerate(original_array):
        if line == "":
            if original_array[idx-1] != "":
                tidy_array.append(line)
        else:
            tidy_array.append(line)

    return tidy_array

def name_lines(unnamed_array):

    named_array = []
    id_num = 0
    lonely_ID = False

    for idx, line in enumerate(unnamed_array):
        if line.startswith(">"):
            if idx != len(unnamed_array):
                if re.match("^[a-zA-Z]+.*", unnamed_array[idx+1]):
                    named_array.append(line)
                else:
                    lonely_ID = True
                    print(line)
        elif idx == 0:
            if re.match("^[a-zA-Z]+.*", line):
                named_array.append(f">protein-sol-{id_num}")
                id_num += 1
                named_array.append(line)
        else:
            if idx != len(unnamed_array)-1:
                if line == "" and not unnamed_array[idx+1].startswith(">"):
                    named_array.append(f">protein-sol-{id_num}")
                    id_num += 1
                else:
                    named_array.append(line)
            if idx != len(unnamed_array):
                if re.match("^[a-zA-Z]+.*", line):
                    named_array.append(line)

    if lonely_ID:
        raise ValueError("IDs without sequence identified")
                
    return named_array

def combine_lines(uncombined_array):

    def testseq(seq,idx):
    
        strseq = "".join(seq)
        if re.match("^[a-z]+.*", strseq):
            print(f"Lowercase aa code found on line {idx}, converting to uppercase")
            strseq = strseq.upper()

        return strseq

    combined_array = []
    combiner = []

    for idx, line in enumerate(uncombined_array):
        if idx == 0:
            combined_array.append(line)
        else:
            if line.startswith(">"):
                newseq = testseq(combiner,idx)
                combined_array.append(newseq)
                combined_array.append("")
                combined_array.append(line)
                combiner = []
            elif re.match("^[a-zA-Z]+.*", line):
                combiner.append(line)

    newseq = testseq(combiner,idx)
    combined_array.append(newseq)
    return combined_array

def write_fasta(clean_array,outputfile):
    with open(outputfile, "w") as output:
        for line in clean_array:
            output.write(line+"\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input file name")
    args = parser.parse_args()

    inputfile  = args.input
    outputfile = str(inputfile+"-formatted")

    fasta_array = read_fasta(inputfile)
    tidy_array = remove_blanks(fasta_array)
    named_array = name_lines(tidy_array)
    final_array = combine_lines(named_array)
    write_fasta(final_array,outputfile)

    copy2(inputfile,str(inputfile+"-old"))
    copy2(outputfile,inputfile)
