import argparse
import sys

from .common.process import ProcessFasta

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input file name")
    parser.add_argument("--single", action="store_true", help="Ensure only single sequence")
    parser.add_argument("--strict", action="store_true", help="Quit if any issue found")
    args = parser.parse_args()

    inputfile = args.input
    single = args.single
    strict = args.strict

    if inputfile:
        np = ProcessFasta(inputfile, single, strict)
        np.write_fasta()
    else:
        print("No input file specified")
        parser.print_help(sys.stderr)
        sys.exit(0)
    
if __name__ == "__main__":
    main()
