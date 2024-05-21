# SiMLInt Docker Containers

## SiMLInt CPU Container
A Docker container, [simlint](https://github.com/EPCCed/SiMLInt/pkgs/container/simlint) (13 GB), which can perform run BOUT Hasegawa-Wakatani simulations, generate ground-truth data, or run SiMLInt simulations with inference, has been made available, with the SiMLInt components installed on an Ubuntu 22.04 image using GCC, OpenMPI and Miniconda3. For Docker container usage instructions, click [here](../../docs/docker-images.md).

## SiMLInt GPU Container
A Docker container, [simlint-gpu]([https://github.com/EPCCed/SiMLInt/pkgs/container/simlint](https://github.com/EPCCed/SiMLInt/pkgs/container/simlint-gpu)) (22 GB), has also been made available. This has been built on an NVIDIA CUDA image, itself built on Ubuntu 22.04. This image can be used on hardware with GPUs and is intended for training of ML models. For Docker container usage instructions, click [here](../../docs/docker-images.md).
