#!/usr/bin/env bash

#SBATCH --no-requeue
#SBATCH -n 1
#SBATCH --export=ALL
#SBATCH --mem=2G
#SBATCH --output=slurm_%x_%j.out
#SBATCH -t 5-0

#Uncomment the next two lines if you want to 'sbatch' this script
source ~/.bashrc.conda #needed to make "conda" command to work
conda activate PCMP_ITS_pipeline

if [[ ! -f ./config.yaml ]]; then
    echo "Must have a config.yaml to be able to run"
    exit 1
fi

set -xeuo pipefail

snakemake --profile ./
