#!/bin/bash
#
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --time=48:00:00
#SBATCH --account=x01

CUDA_VERSION=11.6
CUDNN_VERSION=8.6.0-cuda-${CUDA_VERSION}
TENSORRT_VERSION=8.4.3.1-u2

module load intel-20.4/compilers
module load nvidia/cudnn/${CUDNN_VERSION}
module load nvidia/tensorrt/${TENSORRT_VERSION}
module load nvidia/nvhpc

conda activate boutsmartsim

cd /scratch/space1/x01/data/my-scratch-data/training/training_nc

# choose appropriate parameters here
python training.py --epochs 100 --batch-size 32 --learning-rate 0.0001
