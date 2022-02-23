#!/usr/bin/env python


def conv_fasta(x):
    """
    Parse the input fasta file as list and dictonary.
    Input for this function is a line by line parsed multi
    fasta file:

        with open file as f:
            input_file = f.readlines()
        
        prot_list, prot_dict = conv_fasta(input_file)
    
    Returned output:

    prot_list = [SeqID1, 'Sequence', SeqID2, 'Sequence', ...]

    prot_dict = {SeqID1 : [Sequence length, 'Sequence'],
                 SeqID2 : [Sequence length, 'Sequence']}
    
    """

    new_file = ''
    a = 0
    count_l = len(x)
    count_seq = 0
    seq = ''
    seqs = {}

    for lines in x:
        if lines != "" and lines[:1] == '>':
            count_seq = count_seq + 1
    
    print("[info]\tSequences in file:\t{}".format(count_seq))
    print("[info]\tLoading sequences.\n")

    for lines in x:
        if lines != "" and lines[:1] == '>':
            print("\t",lines.rstrip(), flush=True, end="\r")
            new_file = new_file + lines + "\n"
            a = a + 1

            # As long as no new seqID concatenate the sequnence 
            while a < count_l and '>' not in x[a]:
                seq = seq + x[a].rstrip().upper()
                new_file = new_file + x[a].rstrip().upper()
                a = a + 1
            
            new_file = new_file + "\n"
            seqs[lines.rstrip()]=[len(seq),seq.rstrip("*")]
        seq = ''
    new_file = new_file.split()

    print("\n")
    
    return new_file, seqs