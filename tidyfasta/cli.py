import argparse

from tidyfasta.common.process import process_fasta

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input file name")
    parser.add_argument("--single", action="store_true", help="Ensure only single sequence")
    args = parser.parse_args()

    inputfile = args.input
    single = args.single

    process_fasta(inputfile, single)