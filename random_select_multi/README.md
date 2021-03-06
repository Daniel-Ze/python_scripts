![Header](img/randomsampling_header.png)

# random_select_multi.py
A script to select random coordinates for sequences in genomes. The scripts stores the coordinates in .bed format for further processing.
The script performs **n** random samplings with **x** sequences each. More details can be found here: https://www.biotinkertech.eu/project_RandomSampling.html


Install the requirements with pip:

```bash
(base) 💻 daniel:random_select_multi $ pip install -r random_select_multi_requirementes.txt 
```

You need a index file:
```bash
awk '/>/{if (l!="") print l; print; l=0; next} {l+=length($0)} END {print l}' genome.fa | paste - - | cut -d ">" -f2 > genome.index
```

The script has the following options:

```bash 
(base) 💻 daniel:random_select_multi $ python3 random_select_multi.py 


Usage: python random_select_multi.py -i genome.index -n 100 -s 300 -r 200:20000 -c 1


        -i / --input=   Index of fasta file e.g. Seq1   199192370
        -n / --nsample= Number of times to draw random samples (default 100)
        -s / --nseqs=   Number of random sequences to draw each time
        -r / --range=   Size range of random sampled sequences
        -c / --cpus=    Number CPUs to use
```

The script does the following:

![Flowchart of random_select_multi.py](img/random_select_multi_flowchart1.png)
