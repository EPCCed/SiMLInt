This page shows 
1. how to [install BOUT++](./example-installation.md#1-bout) on Cirrus, and
2. how to [install and set-up SmartSim](./example-installation.md#2-smartsim-with-bout) so that it can communicate with BOUT++.

[< Back](./)

# 1. BOUT++

Go to the `/work` filesystem:
```
export WORK=/work${HOME#/home}
cd $WORK
```

Download BOUT++ source code:
```
git clone https://github.com/boutproject/BOUT-dev.git
```

> We are using v5.0.0; you can download this specific version like this:
> 
> ```wget https://github.com/boutproject/BOUT-dev/archive/refs/tags/v5.0.0.tar.gz```

Load required modules:
```
module load intel-20.4/mpi
module load intel-20.4/compilers
module load fftw/3.3.10-intel20.4-impi20.4
module load netcdf-parallel/4.9.2-intel20-impi20
module load cmake
```

Create a Python virtual environment - we have found the easiest way to do this is with `miniconda`, although care should be taken to use `pip` to install some features rather than `conda` as the later creates libraries that supercede those loaded by `module load`, and which are incompatible with some components of the workflow.
```
export HOME=$WORK # optional, see the note below
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
~/miniconda3/bin/conda init bash

#re-login may be required here
conda create -y --name boutsmartsim python=3.10
conda activate boutsmartsim
python -m pip install cython numpy zoidberg
```

Following the first run of the above, simply `conda activate boutsmartsim` is enough.

Build:
```
cd $WORK/BOUT-dev

MPICXX_CXX=icpc MPICXX=mpiicpc cmake . -B build -DBOUT_DOWNLOAD_NETCDF_CXX4=ON -DBOUT_USE_LAPACK=off -DCMAKE_CXX_FLAGS=-std=c++17 -DCMAKE_BUILD_TYPE=Release

export PYTHONPATH=$WORK/BOUT-dev/build/tools/pylib:$WORK/BOUT-dev/tools/pylib:$PYTHONPATH
# This may not be not required

cmake --build build -j 6
```

## BOUT++ Hasegawa-Wakatani example
This will build a *pure* BOUT++ version of the Hasegawa-Wakatani example. A build with SmartSim connection capability is described on the [workflow page](./workflow.md#compile-hasegawa-wakatani-with-smartredis).

Still in `$WORK/BOUT-dev`:
```
# For full compatibility with the test simulations run during the SiMLInt project, the diffusive function is modified.
# Comment out the two lines below if the HW example is to be left as it is in BOUT-dev
sed -i 's/-Dn \* Delp4(n);/+Dn \* Delp2(n);/g' examples/hasegawa-wakatani/hw.cxx
sed -i 's/-Dvort \* Delp4(vort);/+Dvort \* Delp2(vort);/g' examples/hasegawa-wakatani/hw.cxx

MPICXX_CXX=icpc MPICXX=mpiicpc cmake . -B build -DBOUT_BUILD_EXAMPLES=on
cmake --build build --target hasegawa-wakatani
```

[< Back](./)


# 2. SmartSim with BOUT++

## Python/conda environment

Add the following packages to install SmartSim ML wrapper:
```
conda activate boutsmartsim
conda install git-lfs
git lfs install
conda install cmake
python -m pip install smartsim[ml]
```

Build:
```

module load intel-20.4/mpi
module load intel-20.4/compilers
module load fftw/3.3.10-intel20.4-impi20.4
module load netcdf-parallel/4.9.2-intel20-impi20

export CC=icc
export CXX=icpc

smart build --device cpu --no_pt
```
We will only use Tensorflow so we are not building Pytorch support. Check out available options with `smart build --help`.

## Build SmartRedis libraries

Clone the git repo and the required version and build:
```
git clone https://github.com/CrayLabs/SmartRedis.git --branch v0.5.2 smartredis
cd smartredis
make lib CC=icc CXX=icpc
```

The install path is then available in `smartredis/install`. Modify the `CMakeLists.txt` file to point to this path on your system in place of `/work/x01/x01/auser/smartsim/smartredis/install/include` on line 12.


[< Back](./)
