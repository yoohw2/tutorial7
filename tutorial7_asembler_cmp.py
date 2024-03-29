# -*- coding: utf-8 -*-
"""tutorial7_asembler_cmp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19h1Yc7o6_NenP4N6XUX5n9yBoUQ_1jmO

## start of the file
"""

from google.colab import drive
drive.mount('/content/drive')

"""## get flie"""

'/content/drive/MyDrive/playground_test_anything/class_bio_genomics/tutorials/sampled_1percent_RL_S001__insert_270.fq.gz'

"""## Assemble: metaSPAdes"""

!wget https://github.com/ablab/spades/releases/download/v3.15.5/SPAdes-3.15.5-Linux.tar.gz
!tar -xzf SPAdes-3.15.5-Linux.tar.gz

!pip install Bio

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

import os
os.environ['PATH'] += ":/content/SPAdes-3.15.5-Linux/bin"

from datetime import datetime

start_time = datetime.now()

!spades.py --meta -s /content/drive/MyDrive/playground_test_anything/class_bio_genomics/tutorials/sampled_1percent_RL_S001__insert_270_trimmed_paired.fq.gz -o /content/

end_time = datetime.now()

end_time = datetime.now()
print(f"time spent for SPAdes {end_time - start_time}")

"""## Assemble: megahit"""

!apt-get update
!apt-get install -y megahit

start_time = datetime.now()



!megahit -1 /content/forward_reads.fq -2 /content/reverse_reads.fq -o /content/new4/

end_time = datetime.now()
print(f"time spent for MEGAHIT {end_time - start_time}")

"""## Assemble: idba_ud"""

# Commented out IPython magic to ensure Python compatibility.
# IDBA-UD install
!wget https://github.com/loneknightpy/idba/archive/1.1.3.tar.gz
!tar -xzf 1.1.3.tar.gz
# %cd idba-1.1.3

# IDBA-UD compile
!./build.sh
# %cd bin



start_time = datetime.now()
!./idba_ud -r /content/drive/MyDrive/playground_test_anything/class_bio_genomics/tutorials/sampled_1percent_RL_S001__insert_270_trimmed_paired.fq.gz -o /content/output

end_time = datetime.now()
print(f"time spent for idba_ud {end_time - start_time}")





