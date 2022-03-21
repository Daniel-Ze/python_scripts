# sw_readcount.py
A script that uses a sliding window to count mapped reads in sorted bam files.
Useful for visualizing read mappings with e.g. gggenomes (https://github.com/thackl/gggenomes).

<img src="example.jpg" alt="drawing" width="1000"/>

It requires pysam:

```bash
pip install pysam
```

The script has the following options:

```bash 
(base) 💻 daniel:sw_readcout $ python sw_readmapping.py
sw_read_count.py -i sorted.bam -w 200
	-i Path to sorted bam file
	-w Sliding window size (default 200)
	-c Number of CPUs to use (default 1)

Count mapped reads in non overlapping sliding
windows. Default window size is 200. Make sure
to have a index file with the bam file.
```

The main part of the script was taken from here:
https://bioinformatics.stackexchange.com/questions/5606/how-to-count-the-number-of-mapped-read-in-100-bp-window-from-a-bam-sam-file

# sw_genecount.py
A script that uses a sliding window to count genes in genomic regions. It needs a index file and a gff3 file.

The index file:
```bash
awk '/>/{if (l!="") print l; print; l=0; next} {l+=length($0)} END {print l}' genome.fa | paste - - | cut -d ">" -f2 > genome.index
```

From your genome annotation extract only one feature like 'gene' by using grep -w 'gene' my.gff3:
```
chr12       transdecoder    gene    9328849 9331814 .       +       .       ID=Seq.10877;Name=ORF type:complete len:915 (+)
```

The script has the following options:
```
(base) 💻 daniel:sw_readcount $ python sw_genecount.py 
sw_genecount.py -i genome.index -g gene.gff3
        -i Path to genome index file (mandatory)
        -g Path to gene.gff3 file (mandatory)
        -w Sliding window size (default 200000)

Count genes in non overlapping sliding
windows. Default window size is 200000. Make sure
to have to have only one feature like gene in your
supplied gff3 file.
```
