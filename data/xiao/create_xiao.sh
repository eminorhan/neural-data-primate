#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=64GB
#SBATCH --time=03:00:00
#SBATCH --job-name=create_xiao
#SBATCH --output=create_xiao_%A_%a.out

export HF_HOME="/vast/eo41/huggingface"
export HF_DATASETS_CACHE="/vast/eo41/huggingface"

python -u create_xiao.py --data_dir /scratch/eo41/neural-data/data/xiao

echo "Done"