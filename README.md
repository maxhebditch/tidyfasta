# tidyfasta

A python program to tidy and sanitise FASTA sequence files.
 
It can be imported as a package or used directly from the command line.

If run in non-strict mode (default), any sequence that a breaking issue, such as a non-canonical AA, dangerous characters (any non-alphanumeric character with the exception of `_ -`), or is just an ID without a sequence, will be ignored. 
If run in strict mode then an exception is raised.

When run from the command line interface the script will write a file to the same directory as the input file with the prefix `tidied-` followed by the input file name. 
If there is already an output file, then the prefix will be `tidied-UNIXTIME-` where UNIXTIME is the time at which the script was called.

If imported, after calling the class `ProcessFasta`, two member variables are available. 
`ProcessFasta.fasta_array` returns a minimally validated array of strings, where split lines are combined, excess whitespace is removed, and missing names are added.
`ProcessFasta.validated_array` returns a validated_array of objects, where each object has two variables `id` and `sequence`.
The validated array is checked for non-canonical AA in the sequence and banned characters from the ID. 


## Problems and fixes

| Problem                     | Fix (Strict mode)                       |
|-----------------------------|-----------------------------------------|
| Sequence without ID         | ID name added                           |
| Multiline sequence          | One line per sequence                   |
| ID without sequence         | Sequence ignored (Exception raised)     |
| Non canonical AA            | Sequence ignored (Exception raised)     |
| Dangerous characters in ID  | Sequence ignored (Exception raised)     |
| Lowercase AA                | Converts to uppercase AA                |
| Excessive Whitespace        | Removes excessive whitespace            | 

## Install

    pip install tidyfasta

## Usage

#### Command line interface

    $ tidyfasta --input file.txt

    $ tidyfasta --input file.txt --strict --single

    $ tidyfasta --input file.txt --version

    $ tidyfasta --input file.txt --help
    

#### Script

    from tidyfasta.common.process import ProcessFasta
    
    input_file = "sample.txt"
    
    np = ProcessFasta(input_file, strict=True, single=False)
    
    fasta_array = np.fasta_array
    print(fasta_array)
    
    for i in np.validated_array:
        print(i.id+"\n")
        print(i.sequence+"\n")
    
    np.write_fasta()
