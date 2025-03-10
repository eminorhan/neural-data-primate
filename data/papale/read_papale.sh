#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=124GB
#SBATCH --time=1:00:00
#SBATCH --job-name=read_things
#SBATCH --output=read_things_%A_%a.out

export HF_HOME="/vast/eo41/huggingface"
export HF_DATASETS_CACHE="/vast/eo41/huggingface"

python -u read_things.py

echo "Done"