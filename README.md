# Tidy fasta sequences

Simple code that takes a messy FASTA file and tidies up

## Problems and fixes

| Problem                | Fix                                     |
|------------------------|-----------------------------------------|
| Sequence without ID    | ID name added                           |
| Multiline sequence     | One line per sequence                   |
| Non canonical AA       | Script raises exception and alert user  |
| ID without sequence    | Script raises exception and alerts user |
| Lowercase AA           | Converts to uppercase AA                |
| Whitespace             | Removes excessive whitespace            | 

## Usage

    tidy_fasta.py --input file.FASTA

## Output

1. Original file
2. Formatted file (old file renamed)
