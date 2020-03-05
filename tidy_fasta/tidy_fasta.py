#!/usr/bin/env python
# coding: utf-8

import re
import argparse
from shutil import copy2
import sys
import os

def read_fasta(inputfile):
    read_file_array = []

    with open (inputfile, "r") as fasta:
        for line in fasta:
            read_file_array.append(line.replace("\n",""))

    return read_file_array

def add_missing_names(unnamed_array):

    named_array = []
    id_num = 0
    lonely_ID = False

    lonely_ID_array = []

    for idx, line in enumerate(unnamed_array):
        #if it looks like an ID line
        if line.startswith(">"):
            #check if penultimate item in array
            if idx != len(unnamed_array)-1:
                #If the next item in the array looks like a sequence,
                #add it to the array
                if re.match("^[a-zA-Z]+.*", unnamed_array[idx+1]):
                    named_array.append(line)
                #If not, then it may be an ID without a sequence
                else:
                    lonely_ID = True
                    lonely_ID_array.append(line)
            #If its an ID line, but its the last item in the array
            #then it should/could be an ID without a sequence
            else:
                lonely_ID = True
                lonely_ID_array.append(line)
        #if its the first item in the array and it looks like a sequence
        #then give it a name and add it
        elif idx == 0:
            if re.match("^[a-zA-Z]+.*", line):
                named_array.append(f">protein-sol-{id_num}")
                id_num += 1
                named_array.append(line)
            if re.match("^ +", line):
                named_array.append(f">protein-sol-{id_num}")
                id_num += 1
        #if it isnt the first line and doesnt look like a sequence
        else:
            if re.search("[\\\\<!#\/\"]", line):
                raise ValueError(f"Nonstandard AA detected")
            if not re.search("[\s+]", line):
                #if its not the penultimate item in the array
                if idx != len(unnamed_array)-1:
                    #if its not blank and the next item isnt an ID
                    #then add a generated ID name
                    if line == "" and not unnamed_array[idx+1].startswith(">"):
                        named_array.append(f">protein-sol-{id_num}")
                        id_num += 1
                    if re.match("^ +", line)  and not unnamed_array[idx+1].startswith(">"):
                        named_array.append(f">protein-sol-{id_num}")
                        id_num += 1
                #if not last item in array and looks like a sequence then add
                if idx != len(unnamed_array):
                    if re.match("^[a-zA-Z]+.*", line):
                        named_array.append(line)

    #Raise an exception if any IDs without sequences are found
    if lonely_ID:

        for ID in lonely_ID_array:
            print(f"ID {ID} has no sequence identified")

        raise ValueError("IDs with no sequence identified: stopping")
    else:
        return named_array

def combine_split_lines(uncombined_array):

    #Combine multiline sequences to one line
    #detect non AA characters and correct lowercase

    def testseq(seq,name):
        #Combine gathered array into one string
        strseq = "".join(seq)

        #if lowercase found, announce and correct
        if re.search("[a-z]", strseq):
            print(f"Lowercase AA code found for sequence {name}, converting to uppercase")
            strseq = strseq.upper()

        #if non AA characters found, announce and return bool
        if re.search("[^acdefghiklmnpqrstvwyACDEFGHIKLMNPQRSTVWY]", strseq):
            #check that return is a string not boolean
            print(f"Unrecognised AA code found for sequence {name}")
            return False
        #if only 20 standard aa return string
        else:
            return strseq

    #Array to hold finalised data
    combined_array = []
    #Iterative array to hold combined sequence to be assembled
    combiner       = []
    #Set initial name to None to assign before reference
    name           = None

    #go through array
    for item in uncombined_array:
        #if it looks like an ID
        if item.startswith(">"):
            #run combiner iterative array through test seq
            newseq = testseq(combiner,name)
            #check that return is a string not boolean
            if isinstance(newseq,str):
                #if string (no bad AA) then add this seq
                #to the iterative combiner array
                #add the iterative combiner array to the main
                #array and set the name to match the item
                combined_array.append(newseq)
                combined_array.append(item)
                combiner = []
                name = item
            #if its a bool then raise error
            else:
                raise ValueError("Non-standard AA identified: stopping")
        #Otherwise if it looks like a string rather than a blank add to combiner
        elif re.search("^[a-zA-Z]", item):
            combiner.append(item)

    #check and add last item after going through array
    newseq = testseq(combiner,name)
    if isinstance(newseq,str):
        combined_array.append(newseq)
    else:
        raise ValueError("Non-standard AA identified: stopping")

    return combined_array

def test_single(test_array):

    number_sequences=0

    #go through array
    for item in test_array:
        #if it looks like an ID
        if item.startswith(">"):
            number_sequences+=1

    if number_sequences > 1:
        raise ValueError("More than one sequence present: stopping")

def orphan_check(fasta_array):

    clean_array = []

    for idx, item in enumerate(fasta_array):
        if item.startswith(">"):
            if re.match("[A-Z]",fasta_array[idx+1]):
                clean_array.append(item)
        elif re.match("[A-Z]",item):
            clean_array.append(item)

    return clean_array

#write fasta file
def write_fasta(clean_array,outputfile):

    with open(outputfile, "w") as output:
        for idx,line in enumerate(clean_array):
            if line.startswith(">"):
                output.write(line+"\n")
            else:
                if idx == len(clean_array)-1:
                    output.write(line+"\n")
                else:
                    output.write(line+"\n\n")


def remove_blanks(fasta_array):

    clean_array = []

    for line in fasta_array:
        if not re.match('^\s*$',line):
            clean_array.append(line)

    return clean_array


def tidy_fasta(inputfile,single):
    #temporary outputfile name
    outputfile = str(inputfile+"-formatted")

    try:
        #read file into array
        fasta_array = read_fasta(inputfile)

        fasta_array = add_missing_names(fasta_array)

        fasta_array = remove_blanks(fasta_array)

        fasta_array = combine_split_lines(fasta_array)

        fasta_array = orphan_check(fasta_array)

        if single:
            test_single(fasta_array)

        write_fasta(fasta_array,outputfile)
        
        #copy inputfile to a backup
        copy2(inputfile,str(inputfile+"-old"))
        #rename output file to the inputfile
        copy2(outputfile,inputfile)
        #remove temp file
        os.remove(outputfile)

    except ValueError:
        raise

if __name__ == "__main__":

    #Take Input file as a command line arguement
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input file name")
    parser.add_argument("--single", action="store_true", help="Ensure only single sequence")
    args = parser.parse_args()

    inputfile  = args.input
    single     = args.single

    tidy_fasta(inputfile,single)
