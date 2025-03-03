#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=62GB
#SBATCH --time=4:00:00
#SBATCH --job-name=process_lanzarini
#SBATCH --output=process_lanzarini_%A_%a.out

export HF_HOME="/vast/eo41/huggingface"
export HF_DATASETS_CACHE="/vast/eo41/huggingface"

python -u process_lanzarini.py --data_dir /scratch/eo41/neural-data/data/lanzarini/data

echo "Done"