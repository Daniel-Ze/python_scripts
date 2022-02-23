# sw_readcount.py
A script that uses a sliding window to count mapped reads in sorted bam files.
Useful for visualizing read mappings with e.g. gggenomes (https://github.com/thackl/gggenomes).

<img src="example.jpg" alt="drawing" width="1200"/>

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

