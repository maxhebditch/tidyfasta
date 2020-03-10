# tidyfasta

 A python program to tidy and sanitise FASTA sequence files.
 
 It can be imported as a package or used directly from the command line.

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

#### Command line interface

    $ tidyfasta --input file.txt
    
    $ tidyfasta --input file.txt --strict --single

#### Script

    from tidyfasta.common.process import ProcessFasta
    
    input_file = "sample.txt"
    
    np = ProcessFasta(input_file, strict=True, single=False)
    
    fasta_array = np.get_fasta()
    print(fasta_array)
    
    for i in np.validated_array:
        print(i.id+"\n")
        print(i.sequence+"\n")
    
    np.write_fasta()
