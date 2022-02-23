#!/usr/bin/env python
from oma_go.input_data import input_data
from oma_go.conv_fasta import conv_fasta
from oma_go.oma_request import oma_request
from os import path


def main():
    """
    Put all things together:
      - Get the input with input_dat()
      - Convert the read in protein file to a dictonary
      - Run the oma_request for as long there are sequences
        in the dictonary
    """

    data_input = input_data()
    out_file = str(data_input[2])
    start = int(data_input[3])
    count_p = 0
    out_log = str(path.splitext(out_file)[0])+".log"

    if path.isfile(out_file) and path.isfile(out_log):
        print("[warning]\tOutput and logging file exists already.")
        print("[warning]\tWill append to existing files. Use -s to specify starting point.")
    
    protein_list, protein_dict = conv_fasta(data_input[0])

    print("[info]\tLoaded sequences:\t{}".format(len(protein_dict)))
    print("[info]\tOutput of data to:\t{}".format(out_file))
    print("[info]\tLogging to:\t\t{}".format(out_log))

    if start > 0:
        print("[info]\tResuming script from sequence: {}".format(start))
        count_p = start

    print("[info]\tGetting functional annotation for:")

    while count_p < len(protein_dict):
        if count_p > 0:
            start = count_p
        count_p = oma_request(protein_dict,start,out_file, int(data_input[1]))
        if int(count_p) < int(len(protein_dict)):
            print("\n[info]\tRestarting.")
    
    print("\n[info]\tFinished.")

if __name__ == '__main__':
    main()