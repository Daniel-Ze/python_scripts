#!/us/bin/env python

from math import factorial
import pysam
import getopt
import sys
import os
import multiprocessing

def usage():
    print("sw_readcount.py -i sorted.bam")
    print("\t-i Path to sorted bam file")
    print("\t-w Sliding window size (default 200)")
    print("\t-c Number of CPUs to use (default 1)")
    print("\nCount mapped reads in non overlapping sliding")
    print("windows. Default window size is 200. Make sure")
    print("to have a index file with the bam file.")
    exit()


def input_data():
    """
    Parse the input:
        -i Path to input file
        -w Sliding window size (default 200)
        -c Number of CPUs (default 1)
    """
    if len(sys.argv) == 1:
        usage()
    
    input_file = ""
    window = 200
    cpu = 1

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:w:c:", ["input=", "window=", "cpu="])
    except getopt.GetoptError as err:
        print(err)
        usage()
    
    for o, a in opts:
        if o in ("-i", "--input"):
            input_file = a
        if o in ("-w", "--window"):
            window = int(a)
        if o in ("-c", "--cpu"):
            cpu = int(a)

    if input_file == "":
        print("[error]\tNo path to input file.\n")
        usage()
    
    if os.path.isfile(input_file+str(".bai")) == False:
        print("[error]\tNo index found.\n")
        usage()

    bam_file = pysam.AlignmentFile(input_file)

    file_path = os.path.dirname(input_file)
    file_name = os.path.basename(input_file).split(".")[0]
    out_file = str(file_path)+"/"+file_name+".sw_readmap.bed"

    return bam_file, out_file, window, cpu

def sliding_window(i):
    bam_file = input_data()[0]
    window = int(input_data()[2])
    output = []

    refname = bam_file.references[i]
    seqlen = bam_file.lengths[i]

    print("[info]\tWorking on:\t{0}".format(refname))
    for j in range(1, seqlen, window):
        stop = j+window-1 if j+window-1 < bam_file.lengths[i] else bam_file.lengths[i]
        region_set = set()
        for read in bam_file.fetch(refname, j, stop):
            region_set.add(read.query_name)
        output.append(str("{0}\t{1}\t{2}\treadmap_w{3}\t{4}\n".format(refname, j, stop, window, len(region_set))))

    return output

def main():
    bam_file = input_data()[0]
    out_file = input_data()[1]
    window = int(input_data()[2])
    cpu = input_data()[3]

    output = open(out_file, 'a')

    print("[info]\tReference seqs:\t{}".format(len(bam_file.references)))
    print("[info]\tSlidinw window:\t{}".format(window))
    print("[info]\tUse CPUs:\t{}".format(cpu))
    print("[info]\tOutput file:\t{}".format(out_file))

    a_pool = multiprocessing.Pool(processes=int(cpu))
    result = a_pool.map(sliding_window, range(len(bam_file.references)))

    for f in range(len(result)):
        for g in range(len(result[f])):
            output.write(result[f][g])
    output.close()


if __name__ == '__main__':
    main()
