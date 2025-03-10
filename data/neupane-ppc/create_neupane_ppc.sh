#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=240GB
#SBATCH --time=01:00:00
#SBATCH --job-name=create_neupane_ppc
#SBATCH --output=create_neupane_ppc_%A_%a.out

export HF_HOME="/vast/eo41/huggingface"
export HF_DATASETS_CACHE="/vast/eo41/huggingface"

python -u create_neupane_ppc.py --data_dir /scratch/eo41/neural-data/data/neupane-ppc

echo "Done"