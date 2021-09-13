from __future__ import print_function
import sys, os
import getopt
import math
import shutil


def usage():
    '''
        Print the usage information.
    '''

    print("\nSplitting a multifasta file into n equal chunks.\n")
    print("Usage: python split_chunk.py -i fasta.fa -c 500 -p prefix")
    print("\t-h print this help")
    print("\t-i / --input=\tfasta file")
    print("\t-c / --seqs=\tnumber of sequence chunks")
    print("\t-f / --force\tForce removal of tmp if it exists")
    print("\t-p / --prefix=\tNaming of sequence chunks\n")
    exit()


def parseInput():
    '''
        Parse the commandline input.
    '''

    input_multiFasta = ""
    prefix = ""
    nr_chunks = 0
    seq_name_index = []
    force = False

    if len(sys.argv) == 1:
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:i:p:fh", ["chunks=", "input=", "prefix=","force","help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()

    for o, a in opts:
        if o in ("-c", "--chunks="):
            nr_chunks = int(a)
        elif o in ("-h", "--help"):
            usage()
        elif o in ("-i", "--input="):
            input_multiFasta = a
        elif o in ("-p", "--prefix="):
            prefix = a
        elif o in("-f", "--force"):
            force = True
        else:
            assert False, "unhandled option"
            usage()

    if input_multiFasta == "":
        print("[error]\tNo fasta file.")
        usage()

    with open(input_multiFasta, 'r') as f:
        fasta = f.readlines()

    seq_name_index = getSeqNameIndex(fasta)

    count_seqs = len(seq_name_index)

    cwd = os.path.dirname(input_multiFasta)

    if cwd == "":
        cwd = "."

    if nr_chunks == 0:
        print("[error]\tNo number to split into seq chunks.")
        usage()

    if prefix == "":
        print("[warning]\tNo prefix given. Using split.")
        prefix = "split"

    if count_seqs == 0:
        print("[error]\tNo sequences in multifasta file.")
        usage()

    return cwd, fasta, nr_chunks, prefix, count_seqs, seq_name_index, force


def getSeqNameIndex(x):
    '''
        Get the indexes of all sequence names in supplied multifasta file
        for easy access of sequences in the fasta file.
    '''

    seq_name_lineindex = []
    count = 0
    a = 0
    seq_dict = {}

    print("[info]\tGetting indexes:")
    
    for lines in x:
        if lines != "" and lines[:1] == '>':
            seq_name_lineindex.append(count)
            a = a + 1
            seq_dict[x[count-1].strip()] = count
        count = count + 1

    print("[info]\tIndexes of "+str(a)+" sequences extracted.")

    return seq_name_lineindex


def main():
    '''
        Run the main part of the script.
    '''
    
    # Get the input
    input_data = parseInput()

    # All the different parsed inputs
    cwd = input_data[0]
    fasta = input_data[1]
    nr_chunks = input_data[2]
    prefix = input_data[3]
    count_seqs = input_data[4]
    seq_name_index = input_data[5]
    force = input_data[6]

    # Some variables
    seq_index = 0
    i = 0
    index_range_end = 0
    seq = ""
    missing_1 = 0

    # Calculate the number of sequences in the chunks
    seq_per_chunk = round(int(count_seqs)/int(nr_chunks), 0)
    print("[info]\tCalculated sequences per chunks: " + str(seq_per_chunk))

    # Check if the numbers add up
    if seq_per_chunk == 1:
        seq_per_chunk = 1
        print("[info]\tOne sequence per file.")
    elif (seq_per_chunk%2) == 0 and (count_seqs-(nr_chunks*seq_per_chunk)) > 0:
        missing_1 = count_seqs - (nr_chunks * seq_per_chunk)
        print("[info]\tCalculated missing sequences " + str(missing_1))
        add_chunk = math.ceil(missing_1 / seq_per_chunk)
        nr_chunks = nr_chunks + add_chunk
        print("[info]\tAdjusted the number of chunks to " + str(nr_chunks))

    # Print out all the infos
    print("[info]\tCurrent working dir:      "+cwd)
    print("[info]\tPrefix:                   "+prefix)
    print("[info]\tSequences in file:        "+str(count_seqs))
    print("[info]\tSequences per chunk:      "+str(seq_per_chunk))
    print("[info]\tAdj. nr. chunks:          "+str(nr_chunks))
    print("[info]\tTheo. tot. sequences:     "+str(nr_chunks*seq_per_chunk))
    print("[info]\tFroce:                    "+str(force))

    # Creating tmp/ dir. If you supplied force an old tmp/ folder will be
    # removed before genrating a new tmp/ folder.
    try:
        os.mkdir(cwd+"/tmp")
    except OSError as error:
        print(error)
        if force is True:
            try:
                print("[info]\tForcefully removing tmp! All will be lost!")
                shutil.rmtree(cwd+"/tmp")
                os.mkdir(cwd+"/tmp")
            except OSError as e:
                print(e)
                usage()
        else:
            usage()
    
    # Start the chunking
    while i < int(nr_chunks):
        index_range_end = index_range_end + seq_per_chunk
        out=open(cwd+'/tmp/'+prefix+"_chunk_"+str(i)+".fa", 'a')

        for f in range(int(index_range_end-seq_per_chunk),int(index_range_end)):
            try:
                out.write(fasta[int(seq_name_index[f])])
                seq_index = int(seq_name_index[f]) + 1
                
                while '>' not in fasta[seq_index]:
                    seq = seq + fasta[seq_index].rstrip().upper()
                    try:
                        seq_index = seq_index + 1
                        fasta[seq_index+1]
                    except IndexError:
                        continue

                out.write(seq+"\n")

            except IndexError:
                #l = l + 1
                out.write(seq+"\n")
                break

            seq = ""
        i = i + 1
        out.close()

if __name__ == "__main__":
    main()
