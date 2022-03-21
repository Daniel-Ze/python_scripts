#!/usr/bin/env python

import getopt
import sys
import os


def usage():
    print("sw_genecount.py -i genome.index -g gene.gff3")
    print("\t-i Path to genome index file (mandatory)")
    print("\t-g Path to gene.gff3 file (mandatory)")
    print("\t-w Sliding window size (default 200000)")
    print("\nCount genes in non overlapping sliding")
    print("windows. Default window size is 200000. Make sure")
    print("to have to have only one feature like gene in your")
    print("supplied gff3 file.")
    exit()


def input_data():
	if len(sys.argv) == 1:
		usage()
	
	index_file = ""
	gff_file = ""
	window = 200000
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "i:w:g:", ["input=", "window=", "gff="])
	except getopt.GetoptError as err:
		print(err)
		usage()
	
	for o, a in opts:
		if o in ("-i", "--input"):
			index_file = a
		if o in ("-w", "--window"):
			window = int(a)
		if o in ("-g", "--gff"):
			gff_file = a
	
	if index_file == "":
		print("[error]\tNo path to index file.\n")
		usage()
	if gff_file == "":
		print("[error]\tNo path to gff file.\n")
		usage()
	
	file_path = os.path.dirname(gff_file)
	if file_path == "":
		file_path = "."
	file_name = os.path.basename(gff_file).split(".")[0]
	out_file = str(file_path)+"/"+file_name+".sw_genecount.bed"

	return index_file, gff_file, out_file, window


def main():
	with open(str(input_data()[0]), 'r') as file:
		index_file = file.readlines()
	with open(str(input_data()[1]), 'r') as file:
		gff_file = file.readlines()
	
	out_file = input_data()[2]
	
	sw = int(input_data()[3])
	output = open(out_file, 'w')

	for i in range(len(index_file)):
		chr_name = str(index_file[i].split("\t")[0])
		chr_len = int(index_file[i].split("\t")[1])
		current_chr_gff = []

		for j in range(len(gff_file)):
			if gff_file[j].split("\t")[0] == chr_name:
				current_chr_gff.append(gff_file[j].rstrip().split("\t"))
		
		for h in range(1, chr_len, sw):
			stop = h+sw-1 if h+sw-1 < chr_len else chr_len
			window_count = 0
			if len(current_chr_gff) > 0:
				for f in range(len(current_chr_gff)):
					if int(current_chr_gff[f][3]) >= h and int(current_chr_gff[f][3]) <=stop:
						window_count = window_count + 1
				
				output.write("{}\t{}\t{}\t{}\t{}\n".format(chr_name, h, stop, "window_size_"+str(sw), window_count))


if __name__ == '__main__':
    main()