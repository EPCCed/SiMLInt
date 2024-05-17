#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
# #SBATCH --exclusive
#SBATCH --time=01:00:00
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --array=1-10

export WORK=${HOME/home/work}
SIMLINT_HOME=${WORK}/SiMLInt

eval "$(${WORK}/miniconda3/bin/conda shell.bash hook)"
conda activate boutsmartsim

TRAJ_INDEX=$SLURM_ARRAY_TASK_ID
BASE_PATH=${WORK}/data/extracted/${TRAJ_INDEX}
TRAINING_PATH=${WORK}/data/training

python ${SIMLINT_HOME}/files/4-training-data/gen_training_nc.py $TRAJ_INDEX $BASE_PATH $TRAINING_PATH
