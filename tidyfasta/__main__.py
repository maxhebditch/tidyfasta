import argparse

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

    ProcessFasta(inputfile, single, strict)
    
if __name__ == "__main__":
    main()
