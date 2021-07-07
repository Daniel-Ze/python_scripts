import random
import numpy as np
import os
import sys
import getopt
import matplotlib.pyplot as plt
from multiprocessing import Process
from multiprocessing import Semaphore


def usage():
    """Simple function returning the usage information for the script."""

    print("\n")
    print("Usage: python random_coordinates.py -i fasta.fai -n 100 -s 300 -r 200:20000 -c 10")
    print("\n")
    print("\t-i / --input=\tIndex of fasta file e.g. Seq1\t199192370")
    print("\t-n / --nsample=\tNumber of times to draw random samples (default 100)")
    print("\t-s / --nseqs=\tNumber of random sequences to draw each time")
    print("\t-r / --range=\tSize range of random sampled sequences")
    print("\t-c / --cpus=\t Number CPUs to use")
    print("\n")
    exit()


def random_chose_sequence(sequence_list, seq_prop):
    """Random select a sequence from the fasta index list. Sequences are
    chosen with the calculated probabilities (relative sequence sizes)."""

    q = []
    q = np.random.choice(len(sequence_list), 1, p=seq_prop)
    return q


def sequence_sampling_probability(sequence_list):
    """Calculate genome size and the relative sizes of the the sequences in
    the multi-fasta file. Relative sizes are further used as probabilities
    for random sampling."""

    # Calculate genome size
    genome_size = 0
    for f in sequence_list:
        genome_size = genome_size + int(f[1])

    # Calculate the size percentage of each sequence
    probabilities = []
    for f in sequence_list:
        probabilities.append(int(f[1]) / genome_size)

    return (probabilities, genome_size)


def input_data():
    """Parse the input of the command line and check if everything's alright.
    Mandatory inputs are: Genome index file (-i), number of sequences (-s)."""

    if len(sys.argv) == 1:
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:n:s:r:c:", ["input=","nsample=","nseqs=","range=","cpus="])
    except getopt.GetoptError as err:
        print(err)
        usage()

    samplings = 0
    sequences_to_sample = 0
    sampling_range = ""
    cpus = 1
    # Parse the options
    for o, a in opts:
        if o in ("-i", "--input"):
            input_file = a
        if o in ("-n", "--nsample"):
            samplings = int(a)
        if o in ("-s", "--nseqs"):
            sequences_to_sample = int(a)
        if o in ("-r", "--range"):
            sampling_range = a
        if o in ("-c", "--cpus"):
            cpus = int(a)

    # Fasta index file
    if input_file == "":
        print("No input.")
        usage()

    # Number of sequences to sampling per sampling
    if sequences_to_sample == 0:
        print("No number of sequences to sample.")
        usage()

    # Number of samplings
    if samplings == 0:
        samplings = 100
        print("Defaulting to 100 samplings.")

    # Sequence sice between x and y
    if sampling_range == "":
        sampling_range = "200:20000"
        print("Defaulting to 200:20000 as sampling range.")

    sampling_range_start = int(sampling_range.split(":")[0])
    sampling_range_stop = int(sampling_range.split(":")[1])

    return input_file, sequences_to_sample, samplings, sampling_range_start, sampling_range_stop, cpus


def random_sampling(a, sema):
    read_input = input_data()
    input_file = read_input[0]
    samplings = int(read_input[2])
    global sequences_to_sample
    sequences_to_sample = int(read_input[1])
    global sampling_range_start
    sampling_range_start = int(read_input[3])
    global sampling_range_stop
    sampling_range_stop = int(read_input[4])

    # Create some variables
    content_adj = []
    global content_adj_adj
    content_adj_adj = []

    # Open and read in the index file
    with open(input_file) as f:
        content = f.readlines()
        # remove any trailing information
        for f in content:
            content_adj.append(f.rstrip())
        # split the lines according to the tab
        for f in content_adj:
            content_adj_adj.append(f.split("\t"))
    
    cwd = os.path.dirname(input_data()[0])
    global path_to
    path_to = os.path.join(cwd, "random_sequence_samples")

    global sequence_probabilities
    sequence_probabilities, genome_size = sequence_sampling_probability(content_adj_adj)
    b = 0
    n = 0
    seqLen = 0
    seqName = ""
    start_coord = 0
    stop_coord = 0

    seq_sample = []
    start_coord_sample = []
    uniform_list = []

    # Open the output file
    d = open(os.path.join(path_to, "random_seq_"+str(a)+".bed"), "a")
    # If a range was given create a unifrom distributed list of different
    # sequence lengths
    if sampling_range_start != sampling_range_stop:
        uniform_arr = np.random.uniform(sampling_range_start, sampling_range_stop, sequences_to_sample)

        uniform_list = uniform_arr.tolist()

        plt.hist(uniform_list, bins=30)
        plt.savefig(path_to+'/random_sequence_length_distribution'+str(a)+'.png', dpi=96)
        plt.close()
    # If no range was given create a list with n entries of the the given
    # size
    else:
        for f in range(sequences_to_sample):
            uniform_list.append(sampling_range_start)
    # Iterate over the generated unifrom_list
    for f in uniform_list:
        # chose a random sequence from the genome
        p = random_chose_sequence(content_adj_adj, sequence_probabilities)
        # get the sequence name and length
        seqLen = int(content_adj_adj[int(p)][1])
        seqName = content_adj_adj[int(p)][0]
        # chose a random start coordinate
        start_coord = np.random.choice(int(content_adj_adj[int(p)][1])+1)
        stop_coord = start_coord + int(f)
        # if stop coordinate outside of random genome sequence length:
        # 1. try three times to just get a new start coordiante in the
        #    random genome sequence
        # 2. check if stop coordinate is still longer than the random genome
        #    sequence
        # 3. repeat the whole sampling: new genome sequence, new start coord
        # Repeat until you have a sequence
        if stop_coord > seqLen:
            while b < 3:
                b = b + 1
                if stop_coord > seqLen:
                    start_coord = np.random.choice(int(content_adj_adj[int(p)][1])+1)

                    stop_coord = start_coord + int(f)
        b = 0
        while stop_coord > seqLen:
            p = random_chose_sequence(content_adj_adj, sequence_probabilities)
            seqLen = int(content_adj_adj[int(p)][1])
            seqName = content_adj_adj[int(p)][0]
            start_coord = np.random.choice(int(content_adj_adj[int(p)][1])+1)
            stop_coord = start_coord + int(f)
            n = n + 1
            if stop_coord > seqLen:
                while b < 3:
                    b = b + 1
                    if stop_coord > seqLen:
                        start_coord = np.random.choice(int(content_adj_adj[int(p)][1])+1)
                        stop_coord = start_coord + int(f)
            b = 0
        # Create some lists for some plots
        seq_sample.append(int(p[0]))
        start_coord_sample.append(start_coord)
        # Randomly chose the strand
        strand = random.choice(["+", "-"])
        # Write the results to file
        d.write(str(seqName) + "\t" + str(start_coord) + "\t" + str(stop_coord) + "\t" + ".\t.\t" + strand + "\n")

    d.close()
    # Plot the sampling of genome sequences
    seq_sample_x_value = []
    for f in range(len(content_adj_adj)):
        seq_sample_x_value.append(seq_sample.count(f))

    plt.bar(list(range(0, len(content_adj_adj))), seq_sample_x_value)
    plt.savefig(path_to+'/random_genome_seq_sample_'+str(a)+'.png', dpi=96, bbox_inches = 'tight', facecolor='white')
    plt.close()

    seq_sample_x_value = []
    seq_sample = []

    # Plot the start coordinate sampling
    plt.hist(start_coord_sample, bins=100)
    plt.savefig(path_to+'/random_start_coord_samples_'+str(a)+'.png', dpi=96, bbox_inches = 'tight', facecolor='white')
    plt.close()

    start_coord_sample = []

    print("Number of times for resampling: " + str(n), flush=True)
    n = 0
    sema.release()


if __name__ == "__main__":
    # Parse the input from input_data()
    read_input = input_data()
    input_file = read_input[0]
    samplings = int(read_input[2])
    global sequences_to_sample
    sequences_to_sample = int(read_input[1])
    global sampling_range_start
    sampling_range_start = int(read_input[3])
    global sampling_range_stop
    sampling_range_stop = int(read_input[4])

    cpus = int(read_input[5])

    # Create some variables
    content_adj = []
    global content_adj_adj
    content_adj_adj = []

    # Open and read in the index file
    with open(input_file) as f:
        content = f.readlines()
        # remove any trailing information
        for f in content:
            content_adj.append(f.rstrip())
        # split the lines according to the tab
        for f in content_adj:
            content_adj_adj.append(f.split("\t"))

    # Extract the directory the genome index file is in and create a directory
    # called random_sequence_samples
    cwd = os.path.dirname(input_file)
    global path_to
    path_to = os.path.join(cwd, "random_sequence_samples")

    try:
        os.mkdir(path_to)
    except:
        print("Folder exists.")

    # Calculate the sampling probabilities to account for sequence length
    global sequence_probabilities
    sequence_probabilities, genome_size = sequence_sampling_probability(content_adj_adj)

    print("Number of sequences in file:\t\t" + str(len(content_adj_adj)))
    print("Number of samplings:\t\t\t" + str(samplings))
    print("Number of sequences per sampling:\t" + str(sequences_to_sample))
    print("Sampling sequences in range of:\t\t" + str(sampling_range_start)+":"+str(sampling_range_stop))
    print("Genome size:\t\t\t\t" + str(genome_size))
    print("Output:\t\t\t\t\t" + str(path_to))

    sema = Semaphore(cpus)
    procs = []

    for a in range(samplings):
        sema.acquire()
        proc = Process(target=random_sampling, args=(a, sema))
        procs.append(proc)
        proc.start()
    
    for proc in procs:
        proc.join()
