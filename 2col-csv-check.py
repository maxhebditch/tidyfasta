#!/usr/bin/env python

import pandas as pd
import argparse
from shutil import copy2
import sys
import numbers
import re

def errorwrite(msg,ofile):
    print(errmsg)
    with open(ofile,"a") as outputfile:
        for item in msg:
            outputfile.write(item+"\n")
    sys.exit()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input file name")
    args = parser.parse_args()

    csvname  = args.input

    pH_array = []
    with open(csvname, "r") as inputfile:
        for idx, line in enumerate(inputfile):
            if line == "\n":
                errmsg = (f"Blank line found in file at line {idx+1}")
                errorwrite([errmsg],str(csvname+"-ERROR"))
            if re.search("[a-zA-Z]", line):
                errmsg = (f"Alpha characters found at line {idx+1}, please provide a csv with numbers only")
                errorwrite([errmsg],str(csvname+"-ERROR"))
            if re.search("[!@#$%£\[\]~^&*()?\"\':{}|<>]", line):
                errmsg = (f"Symbol characters found at line {idx+1}, please provide a csv with numbers only")
                errorwrite([errmsg],str(csvname+"-ERROR"))
            if re.search("[!@#$%£\[\]~^&*()?\"\':{}|<>]", line):
                errmsg = (f"Symbol characters found at line {idx+1}, please provide a csv with numbers only")
                errorwrite([errmsg],str(csvname+"-ERROR"))
            
            pH = line.split(",")[0]
            
            try:
                [float(i) for i in line.split(",")]
            except:
                errmsg = (f"Suspected non-number found at line {idx+1}, please provide a csv with numbers only")
                errorwrite([errmsg],str(csvname+"-ERROR"))

            if pH in pH_array:
                errmsg = (f"pH{pH} repeated, only one value per pH required")
                errorwrite([errmsg],str(csvname+"-ERROR"))
            else:
                pH_array.append(pH)
            

    try:
        df = pd.read_csv(csvname,header=None)
    except:
        errmsg = ("Cannot load csv, possibly a varying number of columns, please check that the file for inconsistencies")
        errorwrite([errmsg],str(csvname+"-ERROR"))

    if len(df.columns) != 2:
        errmsg = ("More than two columns")
        errorwrite([errmsg],str(csvname+"-ERROR"))

    missing_items = df.isnull().values.any()

    if missing_items:
        errmsg = ("Missing items")
        errorwrite([errmsg],str(csvname+"-ERROR"))

    df.columns =  ["pH","charge"]

    bound_low = 7
    bound_top = 10
    number_phys = 3

    count_phys = [i for i in df["pH"].values if i >= bound_low and i <= bound_top]

    if len(count_phys) < number_phys:
        errmsg = (f"Only {len(count_phys)} values between {bound_low} and {bound_top}, require at least {number_phys}")
        errorwrite([errmsg],str(csvname+"-ERROR"))
