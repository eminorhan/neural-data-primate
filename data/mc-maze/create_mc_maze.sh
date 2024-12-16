#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32GB
#SBATCH --time=00:10:00
#SBATCH --job-name=create_mc_maze
#SBATCH --output=create_mc_maze_%A_%a.out

export HF_HOME="/vast/eo41/huggingface"
export HF_DATASETS_CACHE="/vast/eo41/huggingface"

python -u create_mc_maze.py --data_dir "sub-Jenkins"

echo "Done"