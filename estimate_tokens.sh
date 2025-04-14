#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=240GB
#SBATCH --time=2:00:00
#SBATCH --job-name=estimate_tokens
#SBATCH --output=estimate_tokens_%A_%a.out

export HF_HOME="/vast/eo41/huggingface"
export HF_DATASETS_CACHE="/vast/eo41/huggingface"

python -u estimate_tokens.py

echo "Done"