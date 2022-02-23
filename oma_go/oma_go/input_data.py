#!/usr/bin/env python
from .usage import usage
import os
import sys
import getopt


def input_data():
    """
    Parse the commandline input

    -i = full path to protein file in fasta format
    -d = request delay in seconds
    -s = restarting the script at a specific sequence in the multi 
         fasta file to find the position:
         
         grep -E '^>' protein.fa | less -SN -p 'SeqID'

    The specified input protein multi fasta file will be read 
    line by line.

    Function returns the parameters as list:
      1. Read in protein file
      2. Delay time
      3. Path to output file
      4. Start index if script is restartet
    """

    sleep_time = 5
    start = 0

    if len(sys.argv) == 1:
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:d:s:", ["input=","delay=","start="])
    except getopt.GetoptError as err:
        print(err)
        usage()

    # Parse the input from the command line
    for o, a in opts:
        if o in ("-i", "--input"):
            input_file = a
        if o in ("-d", "--delay"):
            sleep_time = int(a)
        if o in ("-s", "--start"):
            start = int(a)
    
    if input_file == "":
        print("[error]\tNo input. Nothing to do here.")
        exit()
    
    if sleep_time < 5:
        print("[warning]\tRequest delay time shorter than 5s might result in connection termination by OMA database server.")

    with open(input_file, 'r') as f:
        try:
            protein_file = f.readlines()
        except:
            exit("[Error]\tProblem parsing multi fasta file.")

    # Get the file path for the output
    file_path = os.path.dirname(input_file)
    # Get fasta file name without file ending
    file_name = os.path.basename(input_file).split(".")[0]
    # Create the out file path and name
    out_file = str(file_path)+"/"+file_name+".oma_out.txt"
    
    return protein_file, sleep_time, out_file, start