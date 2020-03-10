# tidyfasta

 A python program to tidy and sanitise FASTA sequence files

## Problems and fixes

| Problem                     | Fix                                     |
|-----------------------------|-----------------------------------------|
| Sequence without ID         | ID name added                           |
| ID without sequence         | Exception raised                        |
| Multiline sequence          | One line per sequence                   |
| Non canonical AA            | Exception raise                         |
| Dangerous characters in ID  | Exception raise                         |
| Lowercase AA                | Converts to uppercase AA                |
| Excessive Whitespace        | Removes excessive whitespace            | 

## Usage

    tidyfasta.py --input file.FASTA
    tidyfasta.py --input file.FASTA --single
    tidyfasta.py --input file.FASTA --single --strict

## Output

1. Tidied version of original file
