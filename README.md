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
conda create -n PCMP_ITS_pipeline --channel bioconda --channel conda-forge --channel defaults python=3.6
conda install --name PCMP_ITS_pipeline --file requirements.txt
/anaconda/envs/venv_name/bin/pip install brocc #brocc needs to be installed through your environment's pip
```

- The following software also need to be installed:
  - `dnabc` (https://github.com/PennChopMicrobiomeProgram/dnabc)
  - `primertrim` (https://github.com/PennChopMicrobiomeProgram/primertrim)
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
- Edit `config.yml` so that it suits your project. In particular,
  - **all: project_dir**: Path to the project directory, e.g. `"/scr1/users/tuv/ITS_Run1"`
  - **all: mux_dir**: Directory containing multiplexed Illumina sequencing reads, which does not have to be in the project directory, e.g. `"/path/to/mux_files"`; if samples are already demultiplexed, just fill in demux_dir
  - **all: demux_dir**: Leave blank if want to demultiplex using this pipeline; otherwise, the directory containing demultiplexed R1/R2 read pairs, which does not have to be in the project directory
  - **all: threads**: Number of threads to use
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
- To run the pipeline, activate the environment by entering `conda activate PCMP_ITS_pipeline`, `cd` into the project directory and execute:
```bash
snakemake \
    --configfile path/to/config.yml \
    --keep-going \
    --latency-wait 90 \
    --notemp
```
- When submitting jobs using slurm, you may run `sbatch run_snakemake.bash config.yml`
- You can use the [skeleton.Rmd](Rmd/skeleton.Rmd) to create a basic bioinformatic report from the results
  
## Notes on BROCC
`create_local_taxonomy_db.py` may be used to install a local taxonomy db for faster processing

## Rules
### Demultiplexing
Input: Multiplexed Illumina sequencing files  
Output: manifest.csv, total_read_counts.tsv, demultiplexed fastq files
### Primer trimming
Removes ITS forward and reverse primer sequences from reads  
Output: reads/(reads.log, top_{rf}_seqs_trimmed.txt, {rf}_trimmed_removed_counts.txt)
### OTU clustering
Create OTUs from amplicons using vsearch. Singletons are discarded for creating the OTUs, but used for the counts.  
Rules are based on this wiki: (https://github.com/torognes/vsearch/wiki/Alternative-VSEARCH-pipeline)  
Output: otu/otu_sorted.tsv
### BROCC
Determine the taxonomic assignments of the OTUs by through a consensus based BLAST result (https://github.com/kylebittinger/brocc)  
Output: BLAST_BROCC_output/out_brocc/brocc.log
