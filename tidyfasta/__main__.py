import argparse
import sys
import re
import pathlib

from .common.process import ProcessFasta

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input file name")
    parser.add_argument("--single", action="store_true", help="Ensure only single sequence")
    parser.add_argument("--strict", action="store_true", help="Quit if any issue found")
    parser.add_argument("-v", "--version", action="store_true", help="Show program version")
    args = parser.parse_args()

    inputfile = args.input
    single = args.single
    strict = args.strict
    version = args.version

    if version:
        curdir = pathlib.Path(__file__).parent
        version_buffer = (curdir / "__init__.py").read_text()
        print(re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_buffer).group(1))
        sys.exit()

    if inputfile:
        np = ProcessFasta(inputfile, single, strict)
        np.write_fasta()
    else:
        print("No input file specified")
        parser.print_help(sys.stderr)
        sys.exit(0)
    
if __name__ == "__main__":
    main()
