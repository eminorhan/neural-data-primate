#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=240GB
#SBATCH --time=1:00:00
#SBATCH --job-name=read_rajalingham
#SBATCH --output=read_rajalingham_%A_%a.out

export HF_HOME="/vast/eo41/huggingface"
export HF_DATASETS_CACHE="/vast/eo41/huggingface"

python -u read_rajalingham.py

echo "Done"