# Example Installation

This page shows:

1. how to [install BOUT++](./example-installation.md#1-bout) on Cirrus, and
2. how to [install and set-up SmartSim](./example-installation.md#2-smartsim-with-bout) so that it can communicate with BOUT++.

[< Back](./)

## Prerequisites

The following settings, modules and Python environment are required for all installation steps.

Go to the `/work` filesystem:

```shell
export WORK=${HOME/home/work}
cd $WORK
```

Load required modules:

```shell
module load intel-20.4/mpi
module load intel-20.4/compilers
module load fftw/3.3.10-intel20.4-impi20.4
module load netcdf-parallel/4.9.2-intel20-impi20
module load cmake
```

Create a Python virtual environment - we have found the easiest way to do this is with `miniconda`, although care should be taken to use `pip` to install some features rather than `conda` as the later creates libraries that supercede those loaded by `module load`, and which are incompatible with some components of the workflow.

```shell
export HOME=$WORK
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
eval "$(~/miniconda3/bin/conda shell.bash hook)"

conda create -y --name boutsmartsim python=3.11
conda activate boutsmartsim
```

## 1. BOUT++

Download BOUT++ source code:

```shell
git clone https://github.com/boutproject/BOUT-dev.git
```

Build:

```shell
cd $WORK/BOUT-dev

MPICXX_CXX=icpc MPICXX=mpiicpc cmake . -B build -DBOUT_DOWNLOAD_NETCDF_CXX4=ON -DBOUT_USE_LAPACK=off -DCMAKE_CXX_FLAGS=-std=c++17 -DCMAKE_BUILD_TYPE=Release

cmake --build build -j 6
```

### BOUT++ Hasegawa-Wakatani example

This will build a *pure* BOUT++ version of the Hasegawa-Wakatani example. A build with SmartSim connection capability is described on the [workflow page](./workflow.md#compile-hasegawa-wakatani-with-smartredis).

Still in `$WORK/BOUT-dev`:

```shell
MPICXX_CXX=icpc MPICXX=mpiicpc cmake . -B build -DBOUT_BUILD_EXAMPLES=on
cmake --build build --target hasegawa-wakatani
```

### BOUT++ post-processing libraries

To use Python for training data generation, we need the `boutdata` and `xbout` libraries. Install these into your existing environment:

```shell
pip install boutdata
pip install xbout
```

## 2. SmartSim and SmartRedis

### Python/conda environment

Install SmartSim ML wrapper:

```shell
conda install git-lfs
git lfs install
python -m pip install smartsim[ml]
```

Build:

```shell
export CC=icc
export CXX=icpc

smart build --device cpu --no_pt
```

We will only use Tensorflow so we are not building Pytorch support. Check out available options with `smart build --help`.

### Build SmartRedis libraries

Clone the git repo and the required version and build:

```shell
git clone https://github.com/CrayLabs/SmartRedis.git --branch v0.5.2 smartredis
cd smartredis
make lib CC=icc CXX=icpc
```

The install path is then available in `smartredis/install`. You will need to refer to this path later when you compile your simulation code with SmartSim (or the example).

## 3. SiMLInt code

Clone the SiMLInt repository:

```shell
git clone https://github.com/EPCCed/SiMLInt.git
export SIMLINT_HOME=$(PWD)/SiMLInt
export ACCOUNT=x01
```

Note: SiMLInt scripts rely on the environment variables $SIMLINT_HOME and $ACCOUNT.

[< Back](./)
