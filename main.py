import argparse

from run_tidy import run_tidy

if __name__ == "__main__":

    #Take Input file as a command line arguement
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input file name")
    parser.add_argument("--single", action="store_true", help="Ensure only single sequence")
    args = parser.parse_args()

    inputfile  = args.input
    single     = args.single

    run_tidy(inputfile, single)
