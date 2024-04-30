#!/bin/bash

#SBATCH --job-name=boutsmartsim
#SBATCH --time=0:20:00
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1

#SBATCH --account=d175
#SBATCH --partition=standard
#SBATCH --qos=standard

# activate conda environment for boutdata and xbout packages
conda activate boutsmartsim

cd /path/to/SiMLInt/files/coarsening
TRAJECTORY=17
OUTPUT_PATH=/path/to/${TRAJECTORY}
python resize_trajectory.py ${TRAJECTORY} ${OUTPUT_PATH}
