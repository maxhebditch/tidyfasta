#!/usr/bin/env python
# coding: utf-8

import re
import argparse
from shutil import copy2
import sys

# def excepthook(type, value, traceback):
#     print(value)

# sys.excepthook =  excepthook

def read_fasta(inputfile):

    read_file_array = []

    with open (inputfile, "r") as fasta:
        for idx, line in enumerate(fasta):
            read_file_array.append(line.replace("\n",""))

    return read_file_array

def remove_blanks(original_array):

    tidy_array = []

    for idx, line in enumerate(original_array):
        if idx == 0:
            if line != "":
                tidy_array.append(line)
        elif line == "":
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
            if idx != len(unnamed_array)-1:
                if re.match("^[a-zA-Z]+.*", unnamed_array[idx+1]):
                    named_array.append(line)
                else:
                    lonely_ID = True
                    print(f"ID {line} has no sequence identified")
            else:
                lonely_ID = True
                print(f"ID {line} has no sequence identified")
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
            if idx != len(unnamed_array):
                if re.match("^[a-zA-Z]+.*", line):
                    named_array.append(line)

    if lonely_ID:
        raise ValueError(f"IDs with no sequence identified: stopping")
                
    return named_array

def combine_lines(uncombined_array):

    def testseq(seq,name):
        global badAA

        strseq = "".join(seq)

        if re.search("[a-z]", strseq):
            print(f"Lowercase AA code found for sequence {name}, converting to uppercase")
            strseq = strseq.upper()

        if re.search("[bjouxBJOUX]", strseq):
            print(f"Unrecognised AA code found for sequence {name}")
            badAA = True

        return strseq

    combined_array = []
    combiner = []
    name = None

    for idx, line in enumerate(uncombined_array):
        if line.startswith(">"):
            newseq = testseq(combiner,name)
            combined_array.append(newseq)
            combined_array.append(line)
            combiner = []
            name = line
        elif re.search("^[a-zA-Z]", line):
            combiner.append(line)

    newseq = testseq(combiner,name)
    combined_array.append(newseq)
    return combined_array

def write_fasta(clean_array,outputfile):
    start = False
    with open(outputfile, "w") as output:
        for idx,line in enumerate(clean_array):
            if line.startswith(">"):
                start = True
            if start:
                output.write(line+"\n")
                if idx % 2 != 1:
                    if idx != len(clean_array)-1:
                        output.write("\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input file name")
    args = parser.parse_args()

    inputfile  = args.input
    outputfile = str(inputfile+"-formatted")

    badAA = False

    fasta_array = read_fasta(inputfile)
    tidy_array = remove_blanks(fasta_array)
    named_array = name_lines(tidy_array)
    final_array = combine_lines(named_array)

    if badAA:
        raise ValueError("Non-standard AA identified: stopping")
    else:
        write_fasta(final_array,outputfile)

        copy2(inputfile,str(inputfile+"-old"))
        copy2(outputfile,inputfile)
