#!/bin/bash

#SBATCH --job-name=resizetraj
#SBATCH --time=0:20:00
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --array=1-10

export WORK=${HOME/home/work}
SIMLINT_HOME=${WORK}/SiMLInt

# activate conda environment for boutdata and xbout packages
eval "$(${WORK}/miniconda3/bin/conda shell.bash hook)"
conda activate boutsmartsim

cd ${WORK}/data/extracted

TRAJ_INDEX=$SLURM_ARRAY_TASK_ID
OUTPUT_PATH=${TRAJ_INDEX}
python ${SIMLINT_HOME}/files/2-coarsening/resize_trajectory.py ${TRAJ_INDEX} ${OUTPUT_PATH}
