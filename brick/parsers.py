from pathlib import Path
from typing import List

def parse_blastn_output(file_path: Path) -> List[BlastnEntry]:
    """
    Parses a BLASTn output file with `-outfmt 6` format.
    
    Args:
    file_path (FilePath): The path to the BLASTn output file.

    Returns:
    List[BlastnEntry]: A list of BlastnEntry models representing each line in the BLASTn output.
    """
    result = []

    with file_path.open('r') as file:
        for line in file:
            fields = line.strip().split('\t')
            entry = BlastnEntry(
                query_id=fields[0],
                subject_id=fields[1],
                perc_identity=float(fields[2]),
                alignment_length=int(fields[3]),
                mismatches=int(fields[4]),
                gap_opens=int(fields[5]),
                query_start=int(fields[6]),
                query_end=int(fields[7]),
                subject_start=int(fields[8]),
                subject_end=int(fields[9]),
                e_value=float(fields[10]),
                bit_score=float(fields[11])
            )
            result.append(entry)

    return result

