# PCMP_ITS_pipeline
This is a Snakemake pipeline for analyzing unpaired fungal internal transcribed spacer (ITS) sequences

## Installation
To install, we assume you already have installed `Miniconda3` (https://docs.conda.io/en/latest/miniconda.html)
- Clone the repository:
```bash
git clone https://github.com/PennChopMicrobiomeProgram/PCMP_ITS_pipeline.git
```
- Create a conda environment and install the required packages:
```bash
cd PCMP_ITS_pipeline
conda create -n PCMP_ITS_pipeline --channel bioconda --channel conda-forge --channel defaults python=3.10
conda install --name PCMP_ITS_pipeline --file requirements.txt
```

- The following software also need to be installed into the new environment:
  - `dnabc` (https://github.com/PennChopMicrobiomeProgram/dnabc)
  - `primertrim` (https://github.com/PennChopMicrobiomeProgram/primertrim)
  - `brocc` (https://github.com/kylebittinger/brocc)
  - `heyfastq` (https://github.com/kylebittinger/heyfastq)
  - To install (dnabc as example):
  ```bash
  git clone https://github.com/PennChopMicrobiomeProgram/dnabc
  cd dnabc
  conda activate PCMP_ITS_pipeline
  pip install -e ./
  ```

## Required input files for the pipeline
To run the pipeline, we need
- De/Multiplexed Illumina reads

## How to run
- Create a project directory, e.g. `/scr1/users/tuv/ITS_Run1`
- Copy the files from this repository into that directory
- Edit `project_config.yml` so that it suits your project. In particular,
  - **all: project_dir**: Path to the project directory, e.g. `"/scr1/users/tuv/ITS_Run1"`
  - **all: mux_dir**: Directory containing multiplexed Illumina sequencing reads, which does not have to be in the project directory, e.g. `"/path/to/mux_files"`; if samples are already demultiplexed, just fill in demux_dir
  - **all: demux_dir**: Leave blank if want to demultiplex using this pipeline; otherwise, the directory containing demultiplexed R1/R2 read pairs, which does not have to be in the project directory
  - **all: mapping_file**: Mapping file of samples with barcode information for demultiplexing
  - **all: forward_direction**: TRUE/FALSE for using forward/reverse read for this pipeline
  - **demux: mismatch**: Number of allowable basepair mismatches on barcode sequence for demultiplexing
  - **demux: revcomp**: If `TRUE`, reverse complement barcode sequence before demultiplexing
  - **trim: f_primer**: Sequence of forward primer used for ITS PCR
  - **trim: r_primer**: Sequence of reverse primer used for ITS PCR
  - **trim: mismatch**: Number of allowable basepair mismatches on ITS PCR primers for trimming
  - **trim: min_length**: Minimum length of match during the partial matching stage
  - **trim: align_id**: Minimum percent identity to consider a primer match in vsearch alignment
  - **otu: expected_error**: Threshold for truncating reads 
  - **otu: otu_id**: Percent sequence identity for clustering reads into OTUs
  - **otu: threads**: Number of threads to use
  - **otu: chimera_db**: Path to UCHIME reference dataset for chimera detection (see https://unite.ut.ee/repository.php); leave blank if using mock DNA amplified with chimera primers
  - **blastn: ncbi_db**: Path to a local ncbi nt database
  - **brocc: taxonomy_db**: Path to brocc nt database created with brocc's `create_local_taxonomy_db.py`
- Edit congfig.yml:
  - **cluster:** and **default-resources:** to match your slurm cluster setup
  - **configfile:** Absolute path to the `project_config.yml` above
- To run the pipeline, simply `bash run_snakemake.bash`
- You can use the files in the `Rmd` folder to create a basic bioinformatic report from the results (assuming some skill with Rstudio / R)
  
## Notes on BROCC
`create_local_taxonomy_db.py` may be used to install a local taxonomy db for faster processing

## Rules
### Demultiplexing
Input: Multiplexed Illumina sequencing files  
Output: manifest.csv, total_read_counts.tsv, demultiplexed fastq files
### Fastqc
Input: demultiplexed fastq files OR output reads from Primer trimming
Output: fastqc reports, concatenated fastqc_quality.tsv with all quality scores
*Note* Fastqc is done at beginning and end of quality control to show differences
### Primer trimming
Removes ITS forward and reverse primer sequences from reads  
Output: reads/(reads.log, top_{rf}_seqs_trimmed.txt, {rf}_trimmed_removed_counts.txt, {rf}_trimmed.fastq)
### OTU clustering
Create OTUs from amplicons using vsearch. Singletons are discarded for creating the OTUs, but used for the counts.  
Rules are based on this wiki: (https://github.com/torognes/vsearch/wiki/Alternative-VSEARCH-pipeline)  
Output: otu/otu_sorted.tsv
### BROCC
Determine the taxonomic assignments of the OTUs through a consensus based BLAST result (https://github.com/kylebittinger/brocc)  
Output: BLAST_BROCC_output/out_brocc/brocc.log

## Optional but sometimes necessary
`run_fastqc_report.py` is included to manually run the concatenation step for all the individual fastqc reports. This is because snakemake errors out when, for example, one of the samples has an empty report.
