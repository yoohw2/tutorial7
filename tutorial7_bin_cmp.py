# -*- coding: utf-8 -*-
"""tutorial7_bin_cmp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-pfLSS3kzPgZco5RU5aIrlkh5J8jZffz

## start of the file
"""

from google.colab import drive
drive.mount('/content/drive')

"""## get flie"""

'/content/drive/MyDrive/playground_test_anything/class_bio_genomics/tutorials/sampled_1percent_RL_S001__insert_270.fq.gz'

from Bio import SeqIO
import gzip

# File path
file_path = '/content/drive/MyDrive/playground_test_anything/class_bio_genomics/tutorials/sampled_1percent_RL_S001__insert_270_trimmed_paired.fq.gz'

# Open the gzipped FASTQ file
with gzip.open(file_path, "rt") as handle:
    # Read the FASTQ file
    records = list(SeqIO.parse(handle, "fastq"))

    # Separate the records into forward and reverse reads
    forward_reads = [record for i, record in enumerate(records) if i % 2 == 0]
    reverse_reads = [record for i, record in enumerate(records) if i % 2 != 0]

# Ensure the separated reads are of equal length
assert len(forward_reads) == len(reverse_reads), "Forward and reverse reads are not equal in number."

# Save the separated reads to new FASTQ files
forward_reads_file = '/content/forward_reads.fq'
reverse_reads_file = '/content/reverse_reads.fq'

with open(forward_reads_file, "w") as output_handle:
    SeqIO.write(forward_reads, output_handle, "fastq")

with open(reverse_reads_file, "w") as output_handle:
    SeqIO.write(reverse_reads, output_handle, "fastq")

forward_reads_file, reverse_reads_file

"""## Compare Contigs"""

!pip install biopython

from Bio import SeqIO

def calculate_assembly_stats(contigs_file):
    contigs_lengths = [len(rec) for rec in SeqIO.parse(contigs_file, "fasta")]
    total_length = sum(contigs_lengths)
    contigs_lengths.sort(reverse=True)

    # N50
    running_total = 0
    for i, length in enumerate(contigs_lengths, 1):
        running_total += length
        if running_total >= total_length / 2:
            N50 = length
            L50 = i
            break

    print(f"Total length: {total_length}")
    print(f"Number of contigs: {len(contigs_lengths)}")
    print(f"N50: {N50}")
    print(f"L50: {L50}")

# Contigs
contigs_file = '/content/drive/MyDrive/path_to_your_contigs_file.fasta'

# call calculation
calculate_assembly_stats(contigs_file)

"""## Bin Contigs: MaxBin2

"""

# Commented out IPython magic to ensure Python compatibility.
# MaxBin2
!wget -O MaxBin-2.2.7.tar.gz https://sourceforge.net/projects/maxbin2/files/MaxBin-2.2.7.tar.gz/download
!tar -zxvf MaxBin-2.2.7.tar.gz
# %cd MaxBin-2.2.7
!./autogen.sh
!./configure
!make

#
import os
os.environ['PATH'] += ":/content/MaxBin-2.2.7/src"

# MaxBin2 실행
!run_MaxBin.pl -contig <path_to_contigs.fasta> -out maxbin2_result

"""## Bin Contigs: MetaBAT2"""

# MetaBAT2 install
!conda install -c bioconda metabat2

# MetaBAT2 execute
!metabat2 -i <path_to_contigs.fasta> -o metabat2_result

"""## Bin Contigs: CONCOCT"""

# CONCOCT install
!conda install -c bioconda concoct

# CONCOCT execute
!concoct --composition_file <path_to_contigs.fasta> --coverage_file <path_to_coverage.tsv> -b concoct_result

"""## Optimize Binned Contigs by Consensus: DasTool

"""

# Miniconda install
!wget -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
!chmod +x Miniconda3-latest-Linux-x86_64.sh
!bash ./Miniconda3-latest-Linux-x86_64.sh -bfp /usr/local

# Conda initiate
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages/')

# DAS Tool install
!conda install -c bioconda -y das_tool

!DAS_Tool -i /content/bin_result -c /content/contigs_file -o /content/out

!DAS_Tool -i maxbin2_result/bins/;metabat2_result/bins/ -c contigs.fasta -o das_output