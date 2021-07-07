# split_chunk.py
A script to split a multifasta file into **n** chunks. Just give the script the number of chunks to create and the output will be a **tmp/** folder with the chunks.

The script has the following options:

```bash 
(base) 💻 daniel:split_chunk $ python3 split_chunk.py 

Splitting a multifasta file into n equal chunks.

Usage: python split_chunk.py -i fasta.fa -s 500 -p prefix
        -h print this help
        -i / --input=   fasta file
        -s / --seqs=    number of sequence chunks
        -f / --force    Force removal of tmp if it exists
        -p / --prefix=  Naming of sequence chunks
```


