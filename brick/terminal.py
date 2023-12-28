
import typer

from pathlib import Path
from typing import List

from .brick import *
from .utils import *

app = typer.Typer(add_completion=False)


@app.command()
def brig_viz(
    reference: Path = typer.Option(
        ..., help="Reference genome against which the rings of other genomes are BLASTED (.fasta)"
    ),
    genomes: str = typer.Option(
        ..., help="Other genomes to include as BLAST identity rings for BRIG-like visualisation (comma-separated string)"
    ),
    output: Path = typer.Option(
        "brick.html", help="Output HTML file path"
    ),
    colors: str = typer.Option(
        ",".join(LAPUTA_MEDIUM), help="Colors for BLAST rings"
    ),
    labels: str = typer.Option(
        None, help="Labels for BLAST rings"
    ),
    radius: int = typer.Option(
        200, help="Total radius of the ring visualization (px)"
    ),
    svg_width: int = typer.Option(
        1600, help="Total radius of the ring visualization (px)"
    ),
    svg_height: int = typer.Option(
        1200, help="Total radius of the ring visualization (px)"
    ),
    title: str = typer.Option(
        "BRICK", help="Title inside ring visualiztion"
    ),
    title_size: str = typer.Option(
        "100%", help="Title size (font-size style)"
    ),
    min_identity: int = typer.Option(
        70, help="Other genomes for BLAST rings"
    ),
    min_length: int = typer.Option(
        100, help="Other genomes for BLAST rings"
    ),
    json: Path = typer.Option(
        None, help="Ring data JSON output file"
    ),
    threads: int = typer.Option(
        None, help="Threads for BLAST"
    ),
    tmpdir: Path = typer.Option(
        Path("/tmp"), help="Temporary working directory for intermediary outputs from tools run as part of BRICK"
    ),
    annotation_ring_gbk: str = typer.Option(
        None, help="Genbank (.gbk) annotation file(s) e.g. output from Prokka or Bacta genome annotation pipelines"
    ),
    annotation_ring_colors: str = typer.Option(
        ",".join(YESTERDAY_MEDIUM), help="Annotation ring colors"
    ),
    annotation_ring_names: str = typer.Option(
        "Annotation", help="Annotation ring name"
    ),
    annotation_ring_height: str = typer.Option(
        20, help="Ring data JSON output file"
    ),
    annotation_ring_feature: str = typer.Option(
        "Annotation", help="Annotation ring feature to "
    ),
    annotation_ring_qualifiers: str = typer.Option(
        None, help="Annotation ring feature qualifiers and their title in the viz tooltip in format e.g. note:Note"
    ),
    cds_ring_gbk: Path = typer.Option(
        None, help="Add a ring internal to the annotation rings showing CDS feature annotations for each GBK file"
    ),
    cds_ring_color: str = typer.Option(
        "#b4b87f", help="CDS ring color"
    ),
    cds_ring_name: str = typer.Option(
        "ORFs", help="CDS ring name"
    ),
    cds_ring_height: str = typer.Option(
        20, help="CDS ring color"
    )
):  
    
    
    genomes = [Path(s.strip()) for s in genomes.split(",")]
    colors = [s.strip() for s in colors.split(",")]
    labels = [s.strip() for s in labels.split(",")] if labels else []

    if cds_ring_gbk:
        ring_gen = AnnotationRing()
        ring_gen.set_options(
            color=cds_ring_color,
            name=cds_ring_name,
            height=cds_ring_height, 
            feature='CDS', 
            qualifiers={
                'gene': 'Gene: ', 
                'product': 'Product: '
            }
        )
        ring_gen.read_genbank(file=cds_ring_gbk)
        ring_gen = [ring_gen]
    else:
        ring_gen = []

    annotation_rings = []
    if annotation_ring_gbk:
        annotation_ring_gbk = [Path(s.strip()) for s in annotation_ring_gbk.split(",")]
        annotation_ring_colors = [s.strip() for s in annotation_ring_colors.split(",")]
        annotation_ring_names = [s.strip() for s in annotation_ring_names.split(",")]
        
        for i, gbk_file in enumerate(annotation_ring_gbk):

            ring_misc = AnnotationRing()
            
            ring_misc.set_options(
                color=annotation_ring_colors[i], 
                name=annotation_ring_names[i], 
                height=annotation_ring_height,
                feature=annotation_ring_feature,
                qualifiers={q: v for q, v in [q.split(":") for  q  in annotation_ring_qualifiers]}
            )

            ring_misc.read_genbank(file=gbk_file)

            annotation_rings.append(ring_misc)
            
    blaster = Blaster(reference=reference, genomes=genomes) ; blaster.run_blast(threads=threads)

    blast_rings = []
    for i in range(blaster.num_results):
        ring_blast = BlastRing()

        ring_blast.set_options(
            color=colors[i], 
            name=labels[i]
        )
        ring_blast.set_filter(
            min_identity=min_identity, 
            min_length=min_length
        )
        ring_blast.read_comparison(
            file=blaster.results[i]
        )
        
        blast_rings.append(ring_blast)

    # Combine rings in preferred order
    rings = ring_gen + blast_rings + annotation_rings

    # Initialize ring generator and set options, write as JSON and HTML
    generator = RingGenerator(rings)
    generator.set_options(
        circle=generator.get_genome_size(file=reference), 
        project='brick', 
        title=title, 
        title_size=title_size, 
        radius=radius,
        width=svg_width, 
        height=svg_height
    )
    generator.brick(
        html_output=output, 
        json_output=json
    )

@app.command()
def concat(
    fasta: Path = typer.Argument(
        ..., help="Fasta contigs input"
    ),
    output: Path = typer.Argument(
        ..., help="Fasta contigs concat output"
    ),
    header: str = typer.Option(
        None, help="Custom header as {id} {descr}"
    ),
    join_chars: str = typer.Option(
        "", help="Join contigs with chcaracter string e.g. NNNNNN"
    ),
):
    
    seq = f"{join_chars}".join(
        [str(rec.seq) for rec in SeqIO.parse(fasta, "fasta")]
    )

    with output.open("w") as out:
        out.write(
            f">{header if header else fasta.stem}\n{seq}"
        )

@app.command()
def slice(
    fasta: Path = typer.Argument(
        ..., help="Fasta contigs input"
    ),
    output: Path = typer.Option(
        "slices.fasta", help="Fasta file output",
    ),
    outdir: Path = typer.Option(
        None, help="Fasta slice per file output directory"
    ),
    size: int =  typer.Option(
        10000, help="Size of non overlapping slices of concatenated output"
    )
):  
    

    if outdir is not None and not outdir.exists():
        outdir.mkdir(parents=True)

    seq_slices = slice_fasta_sequences(fasta_file=fasta, slice_size=size)

    

    if outdir:
        for rec_id, slices in seq_slices.items():
            for record in slices:
                with (outdir / f"{record.id}.fasta").open("w") as out:
                    out.write(
                        f">{record.id} {record.description}\n{record.seq}\n"
                    )
    else:
        with output.open("w") as out:
            for rec_id, slices in seq_slices.items():
                for record in slices:
                    out.write(
                        f">{record.id} {record.description}\n{record.seq}\n"
                    )
