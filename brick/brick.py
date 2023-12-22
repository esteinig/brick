"""Example using some ring features from the Tutorial"""

__author__ = 'esteinig'

"""
=====
BRICK
=====

BLAST Ring Image Generator (BRIG) adoption in D3.js + Python API
Alikhan et al. (2011) wrote BRIG: http://sourceforge.net/projects/brig
"""

import json
import os
import csv
import statistics

from typing import List
from pathlib import Path
from subprocess import call

from Bio import SeqIO


### Helper Classes ###

class Tooltip:

    """Tooltip class (under construction), will hold more options to customize Tooltips for D3"""

    def __init__(self):

        self.text_color = 'white'
        self.head_color = '#FBB917'

    def get_popup(self, text):

        """Converts text - tuple of header and text, i.e. ('Genome:', 'DAR4145') - to HTML string for Tooltip."""

        if len(text) > 0:
            popup = ''
            for i in range(len(text)):
                popup += '<strong>' + '<span style="color:' + self.head_color + '">' + text[i][0] +\
                        '</span>' + ':</strong>' + '<span style="color:' + self.text_color + '">' + text[i][1] +\
                        '</span>' + '<br>'
        else:
            popup = '-'

        return popup


### Rings ###

class Ring:

    """

    Super Class Ring:

    A ring object reads and transforms data into the data shape accesses by the RingGenerator and JS. The standard Ring
    has base attributes colour, name, height and the tooltip style that can be set by the user via setOptions. The
    standard Ring reads a comma-delimited file via readRing containig raw data on each segment (no header) in
    the columns:

    Start Position, End Position, Color, Height and HTML string for Tooltip

    It writes data in the same format via writeRing. Ring objects can also be merged via mergeRings, which adds multiple
    rings' data (list of ring objects) to the current ring object. Attributes of the ring object which called the
    method are retained.

    Subclasses of the ring object have additional attributes pertaining to their function, as well as different readers
    for data files.

    Attributes:

    self.name:      str, name to be shown in tooltips
    self.color:     str, color of ring, hex or name
    self.height:    int, height of ring
    self.tooltip:   obj, tooltip object to set header and text colors

    """

    def __init__(self):

        """Initialize ring object."""

        self.color = 'black'
        self.name = 'Genome'
        self.height = 20
        self.tooltip = Tooltip()

        self.feature = "CDS"
        self.extract = ""

        self._positions = []
        self._popups = []
        self._colors = []
        self._heights = []

        self.data: List[dict] = []

    def merge_rings(self, rings: List[any]):

        """Merge the current ring with a list of ring objects. Add data of ring objects to current ring."""

        for ring in rings:
            self.data += ring.data

    def set_options(self, name='Ring', color='black', height=20, feature: str = None, qualifiers: dict = None, tooltip: Tooltip = None):

        """Set basic attributes for ring object"""

        self.name = name
        self.color = color
        self.height = height
        self.feature = feature
        self.extract = qualifiers

        if tooltip is None:
            self.tooltip = Tooltip()
        else:
            self.tooltip = tooltip

    def _get_ring(self):

        """Get ring data in dictionary format for Ring Generator and D3."""

        n = len(self._positions)

        print('Generating Ring:', self.name)

        for i in range(n):
            data_dict = {}
            data_dict['start'] = self._positions[i][0]
            data_dict['end'] = self._positions[i][1]
            data_dict['color'] = self._colors[i]
            data_dict['text'] = self._popups[i]
            data_dict['height'] = self._heights[i]
            self.data.append(data_dict)

        return self.data

    def write_ring(self, file):

        """Write raw ring data to comma-delimited file."""

        with open(file, 'w') as outfile:
            w = csv.writer(outfile, delimiter=',')
            d = [[segment['start'], segment['end'], segment['color'], segment['height'], segment['text']] for segment in self.data]
            w.writerows(d)

    def read_ring(self, file):

        """Read raw ring data from comma-delimited file."""

        self._clear()

        with open(file, 'r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                data = {}

                self._heights.append(row[3])
                self._colors.append(row[2])
                self._positions.append([row[0], row[1]])
                self._popups.append(row[4])

                data['start'] = row[0]
                data['end'] = row[1]
                data['color'] = row[2]
                data['height'] = row[3]
                data['text'] = row[4]
                self.data.append(data)

    def _clear(self):

        """Clear all ring data."""

        self._heights = []
        self._colors = []
        self._positions = []
        self._popups = []
        self.data = []

### Ring Generator ###
        
class RingGenerator:

    """

    Class: Ring Generator

    Initiate with list of rings and set options for visualization. The generator transforms the ring data into
    a list of dictionaries for writing as JSON. Options can be set via setOptions. The main access is the brigD3 method,
    which initiates the helper class Visualization containing the JS D3 script and sets its parameters in the string.
    The method then writes the JSON and HTML files to working directory.

    Attributes:

    self.rings:     list, ring objects
    self.project:   str, name of output files
    self.radius:    int, radius of the ring center
    self.gap:       int, gap between the rings

    self.data:      list, data dicts for each segment

    """

    def __init__(self, rings: List[Ring]):

        """Initialize generator with list of rings."""

        self.rings = rings
        self.project = 'project'
        self.radius = 200
        self.gap = 5

        self.data: List[dict] = []

        self._options = {}

        self.get_data()

    def get_data(self):

        """Transform data from rings to data appropriate for D3"""

        d3 = []
        radius = self.radius
        for ring in self.rings:
            for seg in ring.data:
                height = int(seg.pop('height'))
                radius = int(radius)
                seg['inner'] = float(radius)
                seg['outer'] = float(radius + height)
                d3.append(seg)

            radius = int(radius) + int(ring.height) + int(self.gap)

        self.data = d3

        return self.data

    def set_options(self, circle, radius=300, gap=5, project='data', title='brigD3', title_size='100%', title_font='times', ring_opacity=0.8, width: int = 2400, height: int = 1600):

        """Set options for circle generator and visualization with D3."""

        self.radius = radius ; self.gap = gap ; self.project = project

        self._options = {
            'circle': circle, 
            'main_title': title, 
            'title_size': title_size,
            'title_font': title_font, 
            'ring_opacity': ring_opacity, 
            'chart_width': width,
            'chart_height': height
        }

    def get_genome_size(self, file: Path) -> int:
        """ Get the total length of the input genome (sum of contigs in FASTA) to set as circle size for whole genome visualiztions"""
        
        return sum([len(rec.seq) for rec in SeqIO.parse(file, "fasta")])
    
    def brick(self, html_output: Path = Path.cwd() / "brick.html", json_output: Path = None):

        """Write files for BRICK to working directory."""

        print('\nWriting visualization to working directory ...\n')
        
        viz = Visualization(self._options, self.data)

        viz._set_script()
        viz._write_html(output=html_output)

        if json_output:
            with json_output.open("w") as jo:
                json.dump(self.data, jo, indent=4, sort_keys=True)



class CoverageRing(Ring):

    """Subclass Coverage Ring for depicting coverage matrix across genomes (single or average)"""

    def __init__(self):

        """Initialize super-class ring and attributes for Coverage Ring"""

        Ring.__init__(self)

        self.threshold = 0.96
        self.below = '#E41B17'

    def read_coverage(self, file, sep='\t', mean=True, n=5):

        """Read coverage matrix from file (with header): segment_id, start, end, value_sample_1, value_sample_2, ... value_sample_n"""

        self._clear()

        with open(file, 'r') as infile:
            reader = csv.reader(infile, delimiter=sep)

            header = []
            texts = []
            for row in reader:
                if header:
                    start = int(row[1])
                    end = int(row[2])
                    if mean:
                        value = statistics.mean([float(v) for v in row[3:]])
                        cov = 'Mean Coverage'
                    else:
                        value = float(row[n])
                        cov = 'Coverage'
                    self._positions.append((start, end))
                    color = self.below if value < self.threshold else self.color
                    self._colors.append(color)
                    self._heights.append(value*self.height)
                    texts.append([
                        ('Genome:', self.name), 
                        ('Location:', str(start) + ' - ' + str(end)),
                        (cov, format(value*100, ".2f") + '%')
                    ])
                else:
                    header = row

        self._popups = [self.tooltip.get_popup(text) for text in texts]

        self._get_ring()


class AnnotationRing(Ring):

    """Sub-class Annotation Ring for depicting genome annotations and SNPs"""

    def __init__(self):

        """Initialize super-class ring and attributes for Annotation Ring."""

        Ring.__init__(self)

        self.feature = 'CDS'
        self.extract = {
            'gene': 'Gene: ', 
            'product': 'Product: '
        }

        self.snp_length = 100
        self.intergenic = 'yellow'
        self.synonymous = 'orange'
        self.non_synonymous = 'red'

    def read_snp(self, file, single=False, n=5):

        """Read SNP data from comma_delimited file (without header): SNP ID, Location, Type, Notes"""

        self._clear()

        with open(file, 'r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                if single:
                    # If nucleotide is not equal to reference nucleotide or if it is reference nucleotide

                    # Needs a fix, it's a mess...
                    if row[n] != row[4] or n == 4:
                        self._positions.append([int(row[1])-self.snp_length//2, int(row[1])+self.snp_length//2])
                        if row[2] == 'intergenic':
                            self._colors.append(self.intergenic)
                        elif row[2] == 'synonymous':
                            self._colors.append(self.synonymous)
                        elif row[2] == 'non-synonymous':
                            self._colors.append(self.non_synonymous)
                        else:
                            self._colors.append(self.color)

                        self._heights.append(self.height)
                        self._popups.append(self.tooltip.get_popup([
                            ('Genome:', self.name), 
                            ('SNP:', row[0]),
                            ('Location: ', row[1]), 
                            ('Type:', row[2]),
                            ('Note:', row[3])
                        ]))
                else:
                    # Single ring for SNPs along Reference, general SNPs across all isolates from SPANDx
                    self._positions.append([int(row[1])-self.snp_length//2, int(row[1])+self.snp_length//2])
                    if row[2] == 'intergenic':
                        self._colors.append(self.intergenic)
                    elif row[2] == 'synonymous':
                        self._colors.append(self.synonymous)
                    elif row[2] == 'non-synonymous':
                        self._colors.append(self.non_synonymous)
                    else:
                        self._colors.append(self.color)

                    self._heights.append(self.height)
                    self._popups.append(self.tooltip.get_popup([
                            ('Genome:', self.name), 
                            ('SNP:', row[0]), 
                            ('Location: ', row[1]),
                            ('Type:', row[2]), 
                            ('Note:', row[3])
                        ])
                    )

        self._get_ring()

    def read_genbank(self, file: Path) -> None:

        """Read genbank annotation file and extract relevant features and qualifiers."""

        self._clear()

        genome = SeqIO.read(open(file, "r"), "genbank")

        features = [feature for feature in genome.features if feature.type == self.feature]

        # Only include feature with all qualifiers present
        clean = []
        for feature in features:
            check = True
            for q in self.extract.keys():
                if q not in feature.qualifiers:
                    check = False
            if check:
                clean.append(feature)

        # Get tooltips for each extracted feature.
        for feature in features:

            self._positions.append([int(feature.location.start), int(feature.location.end)])
            self._colors.append(self.color)
            self._heights.append(self.height)

            qualifier_texts = []
            for qualifier in self.extract.keys():
                if qualifier in feature.qualifiers:
                    text_tuple = (self.extract[qualifier], ''.join(feature.qualifiers[qualifier]))
                    qualifier_texts.append(text_tuple)
            qualifier_texts.insert(0, ('Location: ', str(feature.location.start) + '-' + str(feature.location.end)))
            qualifier_texts.insert(0, ('Genome: ', self.name))

            popup = self.tooltip.get_popup(qualifier_texts)

            self._popups.append(popup)

        self._get_ring()

class BlastRing(Ring):

    """Sub-class Blast Ring, for depicting BLAST comparisons against a reference DB"""

    def __init__(self):

        """Initialize super-class ring and attributes for Blast Ring."""

        Ring.__init__(self)

        self.min_identity = 70
        self.min_length = 100
        self.values = []

    def set_filter(self, min_identity=70, min_length=100):

        """ Set the BLAST comparison filter values on identity and minimum query alignment length"""

        self.min_identity = min_identity
        self.min_length = min_length

    def read_comparison(self, file):

        """Reads comparison files from BLAST output (--outfmt 6)"""

        self._clear()

        with open(file, 'r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            for row in reader:
                positions = sorted([int(row[8]), int(row[9])])
                if positions[1] - positions[0] >= self.min_length and float(row[2]) >= self.min_identity:
                    self._positions.append(positions)
                    self.values.append(float(row[2]))

        self._colors = [self.color for v in self.values]
        self._heights = [self.height for v in self.values]
        texts = [[('Genome:', self.name), ('BLAST Identity:', str(v) + '%')] for v in self.values]
        self._popups = [self.tooltip.get_popup(text) for text in texts]

        self._get_ring()

class Blaster:

    """

    Class: Blaster

    Convenience module to run BLAST+ (needs to be in $PATH).

    Initialize with a string for the reference genome file (.fasta) and a list of strings for the sequence files
    to be compared (.fasta). Main access is through runBlast. Results attribute hold the string names of the
    output comparison files that can be iterated over to create Blast Rings.

    Attributes:

    self.name_db:       str, name of database to be created from the reference sequence
    self.type:          str, database type, either 'nucl' or 'prot'
    self.mode:          str, type of comparison, either 'blastn' for nucleotide or 'blastp' for protein

    """

    def __init__(self, reference: Path, genomes: List[Path]):

        """Initialize blast object with refernece and sequence files"""

        self.reference = reference
        self.genomes = genomes
        
        self.name_db = 'ReferenceDB'
        self.type = 'nucl'
        self.mode = 'blastn'

        self.results = []

    def _get_db(self):

        """Run makeblastdb to create reference database"""

        call(['makeblastdb', '-in', os.path.join(os.getcwd(), self.reference), '-dbtype', self.type, '-out', self.name_db])
        print('\n')

    def run_blast(self, threads: int = 4):

        """"Blast sequence files against reference DB."""

        self._get_db()

        refname = self.reference.name

        for genome in self.genomes:
            print(genome)
            genname = genome.name
            print('Blasting', genome, 'against Reference DB ...')
            filename = genname + 'vs' + refname
            call([
                self.mode, '-query', os.path.join(os.getcwd(), genome), '-db', self.name_db, '-outfmt', '6', '-out', os.path.join(os.getcwd(), filename)
            ])
            self.results.append(filename)

        print('\n')

    @property
    def num_results(self) -> int:
        return len(self.results)
    
class Visualization:

    """
    Helper class `Visualization`, contains script for JS D3. Methods to replace options from `RingGenerator` in
    script and write the HTML. Initializes with options dict and data from `RingGenerator`.
    """

    def __init__(self, options: dict, data: List[dict]):

        self.options = options
        self.data = data

        self.head = '''
                    <!DOCTYPE html>
                    <meta charset="utf-8">
                    <style>

                      div.tooltip {
                        position: absolute;
                        text-align: left;
                        max-width: 100%;
                        padding: 0.5%;
                        font: 64pt sans-serif;
                        background: black;
                        border-radius: 0.1%;
                        pointer-events: none;
                      }

                    </style>

                    <body>
                    <script src="https://d3js.org/d3.v3.min.js" charset="utf-8"></script>
                    <script type="application/json" id="data">
                    '''

        self.body = '''
                    </script>
                    <script>

                    function saveSvg(svgEl, name) {
                        
                    }

                    pi = Math.PI;
                    seqLength = circle

                    var degreeScale = d3.scale.linear()
                                          .domain([0, seqLength])
                                          .range([0,360])
                    ;

                    var data = JSON.parse(document.getElementById('data').innerHTML);

                    var arc = d3.svg.arc()
                        .innerRadius(function(d, i){return d.inner;})
                        .outerRadius(function(d, i){return d.outer;})
                        .startAngle(function(d, i){return degreeScale(d.start) * (pi/180);})
                        .endAngle(function(d, i){return degreeScale(d.end) * (pi/180);})
                    ;

                    var width = chart_width
                    var height = chart_height

                    var chart = d3.select("body")
                        .append("svg:svg")
                        .attr("width", width)
                        .attr("height", height)
                        .call(d3.behavior.zoom().on("zoom", function () {
                            chart.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
                        }))
                        .append("svg:g")
                    ;

                    var div = d3.select("body").append("div")
                        .attr("class", "tooltip")
                        .style("opacity", 0)
                    ;

                    var ringShell = chart.append("g")
                                         .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

                    var textShell = chart.append("g")
                                         .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

                    ringShell.selectAll("path")
                        .data(data)
                        .enter().append("svg:path")
                        .style("fill", function(d, i){ return d.color; })
                        .style("opacity", ring_opacity)
                        .attr("d", arc)
                        .attr('pointer-events', 'none')
                        .on('mouseover', function(d) {
                                div.transition()
                                    .duration(200)
                                    .style("opacity", .9);
                                div .html(d.text)
                                    .style("left", (d3.event.pageX + 20) + "px")
                                    .style("top", (d3.event.pageY + 10) + "px");
                                })
                        .on('mouseout', function(d) {
                                div.transition()
                                    .duration(200)
                                    .style("opacity", 0)
                            })
                        .attr('pointer-events', 'visible')
                    ;

                    textShell.append("text")
                      .style("opacity", 0)
                      .style("text-anchor", "middle")
                      .style("font-size", "title_size")
                      .style("font-weight", "bold")
                      .style("font-family", "title_font")
                      .attr("class", "inside")
                      .text(function(d) { return 'main_title'; })
                      .transition().duration(5000).style("opacity", 1)
                    ;

                </script>
                </body>

                '''

    def _set_script(self):

        """Replace placeholder values in script with given options."""

        for placeholder, value in self.options.items():
            self.body = self.body.replace(str(placeholder), str(value))

    def _write_html(self, output: Path = Path.cwd() / "brick.html"):

        """Write script to HTML."""

        with output.open('w') as outfile:
            outfile.write(self.head)

        with output.open('a') as outfile:
            json.dump(self.data, outfile, indent=4, sort_keys=True)
            outfile.write(self.body)
            
