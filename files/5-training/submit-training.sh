#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --time=48:00:00

CUDA_VERSION=11.6
CUDNN_VERSION=8.6.0-cuda-${CUDA_VERSION}
TENSORRT_VERSION=8.4.3.1-u2

export WORK=${HOME/home/work}
SIMLINT_HOME=${WORK}/SiMLInt

eval "$(${WORK}/miniconda3/bin/conda shell.bash hook)"
conda activate boutsmartsim

module load intel-20.4/compilers
module load nvidia/cudnn/${CUDNN_VERSION}
module load nvidia/tensorrt/${TENSORRT_VERSION}
module load nvidia/nvhpc

cd ${WORK}/data/training

# choose appropriate parameters here
# create a model each for vorticity and density error correction

# model the vorticity error
python ${SIMLINT_HOME}/files/5-training/training.py --epochs 100 --batch-size 32 --learning-rate 0.0001 \
    --trajectories 10 --data-directory ${WORK}/data/training/ --variables vort --task-id vort

# model the density error
python ${SIMLINT_HOME}/files/5-training/training.py --epochs 100 --batch-size 32 --learning-rate 0.0001 \
    --trajectories 10 --data-directory ${WORK}/data/training/ --variables n --task-id dens

# model the electrostatic potential error
python ${SIMLINT_HOME}/files/5-training/training.py --epochs 100 --batch-size 32 --learning-rate 0.0001 \
    --trajectories 10 --data-directory ${WORK}/data/training/ --variables phi --task-id phi
