#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --time=48:00:00

CUDA_VERSION=11.6
CUDNN_VERSION=8.6.0-cuda-${CUDA_VERSION}
TENSORRT_VERSION=8.4.3.1-u2

export WORK=${HOME/home/work}

eval "$(${WORK}/miniconda3/bin/conda shell.bash hook)"
conda activate boutsmartsim

module load intel-20.4/compilers
module load nvidia/cudnn/${CUDNN_VERSION}
module load nvidia/tensorrt/${TENSORRT_VERSION}
module load nvidia/nvhpc

cd ${WORK}/data/training

# choose appropriate parameters here
python ${SIMLINT_HOME}/files/5-training/training.py --epochs 100 --batch-size 32 --learning-rate 0.0001
