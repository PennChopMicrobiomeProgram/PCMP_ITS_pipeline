#!/usr/bin/env bash

#SBATCH --no-requeue
#SBATCH -n 1
#SBATCH --export=ALL
#SBATCH --mem=2G
#SBATCH --output=slurm_%x_%j.out
#SBATCH -t 5-0

#Uncomment the next two lines if you want to 'qsub' this script
source ~/.bashrc.conda #needed to make "conda" command to work
conda activate PCMP_ITS_pipeline

set -xeuo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: bash $0 PATH_TO_CONFIG"
    exit 1
fi

CONFIG_FP=$1

snakemake \
    --jobs 100 \
    --configfile ${CONFIG_FP} \
    --cluster-config cluster.json \
    --keep-going \
    --latency-wait 90 \
    --notemp \
    --printshellcmds \
    --cluster \
    "sbatch --no-requeue --export=ALL --mem={cluster.memcpu} -n {threads} -t 2-0 -J {cluster.name} --output=slurm_%x_%j.out"
