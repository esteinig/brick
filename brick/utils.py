

import requests

from pathlib import Path
from typing import List, Dict

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

def slice_fasta_sequences(fasta_file, slice_size=10000) -> Dict[str, List[SeqRecord]]:
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


def summarize_protein_annotations_gpt35(annotations: List[str], api_key: str) -> str:
    """
    This function takes a list of protein annotations and sends a request to the GPT-3.5 API to generate
    a summary of their likely functions and origins.

    Args:
    - annotations (List[str]): A list of protein annotations to be summarized.
    - api_key (str): The API key for authenticating with the OpenAI API.

    Returns:
    - str: A summary text of the proteins' functions and origins.

    Raises:
    - Exception: If the API request fails or returns an error.

    Note:
    - The function uses the OpenAI GPT-3.5 API endpoint and settings.
    - You should replace 'API_ENDPOINT' with the actual GPT-3.5 API endpoint provided by OpenAI.
    """

    # Define the GPT-3.5 API endpoint
    api_endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"

    # Prepare the payload
    payload = {
        "prompt": f"Summarize the functions and origins of these proteins: {', '.join(annotations)}",
        "max_tokens": 250,
        "temperature": 0.7,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }

    # Set headers including the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Make the request to the API
    response = requests.post(api_endpoint, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the response data
        response_data = response.json()
        # The GPT-3.5 API returns a list of choices with text; get the first one.
        return response_data["choices"][0]["text"].strip()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

