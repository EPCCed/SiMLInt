#!/bin/bash

#SBATCH --job-name=resizetraj
#SBATCH --time=0:20:00
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1

#SBATCH --account=x01
#SBATCH --partition=standard
#SBATCH --qos=standard

# activate conda environment for boutdata and xbout packages
conda activate boutsmartsim

cd /scratch/space1/x01/data/my-scratch-data
TRAJECTORY=1
OUTPUT_PATH=${TRAJECTORY}/extracted
python resize_trajectory.py ${TRAJECTORY} ${OUTPUT_PATH}
