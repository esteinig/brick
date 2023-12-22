import dataclasses

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

LAPUTA_MEDIUM = [
    '#14191F',
    '#1D2645',
    '#403369',
    '#5C5992',
    '#AE93BE',
    '#B4DAE5',
    '#F0D77B',
]

YESTERDAY_MEDIUM = [
    '#061A21',
    '#132E41',
    '#26432F',
    '#4D6D93',
    '#6FB382',
    '#DCCA2C',
    '#92BBD9',
]

DALI = [
    "#b4b87f", 
    "#9c913f", 
    "#585b33", 
    "#6ea8ab", 
    "#397893", 
    "#31333f",
    "#8f5715", 
    "#ba9a44", 
    "#cfbb83"
]

PANTON = [
    "#e84a00",
    "#bb1d2c",
    "#9b0c43",
    "#661f66",
    "#2c1f62",
    "#006289",
    "#004759"
]

RATTNER = [
    "#de8e69", 
    "#f1be99", 
    "#c1bd38", 
    "#7a9132",  
    "#4c849a", 
    "#184363", 
    "#5d5686",
    "#a39fc9"
]

LAPUTA_MEDIUM.reverse()
YESTERDAY_MEDIUM.reverse()

def slice_fasta_sequences(fasta_file, slice_size=10000):
    """
    Takes a FASTA file and returns slices of each sequence with slice coordinates in the header.
    
    :param fasta_file: Path to the FASTA file
    :param slice_size: Size of each slice (default is 10,000 bases)
    :return: A dictionary with sequence IDs as keys and a list of SeqRecords as values
    """
    sliced_sequences = {}

    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        slices = []
        for i in range(0, len(seq_record), slice_size):
            slice_seq = seq_record.seq[i:i+slice_size]
            slice_id = f"{seq_record.id}_{i}:{i+slice_size}"
            slice_description = f"Slice {i}-{i+slice_size} of {seq_record.id}"
            slices.append(SeqRecord(Seq(slice_seq), id=slice_id, description=slice_description))

        sliced_sequences[seq_record.id] = slices

    return sliced_sequences

