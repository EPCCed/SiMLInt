#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
# #SBATCH --exclusive
#SBATCH --time=01:00:00
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --account=<account>

eval "$(/work/x01/x01/$USER/miniconda3/bin/conda shell.bash hook)"
conda activate boutsmartsim

TRAJECTORY=1

python gen_training_nc.py $TRAJECTORY
