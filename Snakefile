import configparser
import yaml

from scripts import util_functions

PROJECT_DIR = config["all"]["project_dir"]
INTER_DIR = PROJECT_DIR + "/intermediates"
MUX_DIR = config["all"]["mux_dir"] if config["all"]["mux_dir"] else PROJECT_DIR + "/multiplexed_fastq"
DEMUX_DIR = config["all"]["demux_dir"] if config["all"]["demux_dir"] else INTER_DIR + "/demultiplexed_fastq"
PRIMER_TRIM_FP = INTER_DIR + "/primer_trim"
READ_DIR = PROJECT_DIR + "/reads"
READ_INTER_DIR = READ_DIR + "/intermediates"
OTU_DIR = PROJECT_DIR + "/otu"
FASTA_DIR = INTER_DIR + "/fq2fa"
BL_BR_DIR = PROJECT_DIR + "/BLAST_BROCC_output"
MAPPING_FP = PROJECT_DIR + "/" + config["all"]["mapping_file"]
SAMPLE_IDS = util_functions.get_sample(MAPPING_FP)

include: "rules/targets.rules"
include: "rules/blast_n_brocc.rules"
include: "rules/otu.rules"
include: "rules/demux.rules"
include: "rules/trim.rules"
include: "rules/trim_len.rules"

workdir: PROJECT_DIR

rule all:
  input: TARGET_ALL
