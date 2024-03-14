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

Create a Python `venv` extending the central `python/3.9.13` module, since the BOUT++ build requires Python with additional packages (Cython, zoidberg, boututils and others) which are not provided by `python/3.9.13`:
```
export HOME=$WORK # optional, see the note below 
module load python/3.9.13
python -m venv --system-site-packages bout
extend-venv-activate bout
source bout/bin/activate
python -m pip install cython
module unload -f openmpi
```

Following the first run of the above, simply `source bout/bin/activate` is enough.

> **Note:** The Python `venv` module expects the venv parent directory to be `$HOME`, i.e. venv folders are in `$HOME/<venv name>`.
> If `export HOME=$WORK` is not used, full paths must be given to `venv`, for example, `python -m venv --system-site-packages $WORK/bout`.
> This isn't a big deal at this stage, but is more important when running SiMLInt Jupyter Notebooks.

> **Note:** `module unload -f openmpi` removes the openmpi compilers from `$PATH`, which breaks `mpi4py`, but allows `BOUT++` to be compiled.
> In our case we will not be using `mpi4py`.

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
MPICXX_CXX=icpc MPICXX=mpiicpc cmake . -B build -DBOUT_BUILD_EXAMPLES=on
cmake --build build --target hasegawa-wakatani
```

[< Back](./)


# 2. SmartSim with BOUT++

## Python/conda environment
Follow [Cirrus docs](https://docs.cirrus.ac.uk/user-guide/python/#installing-your-own-python-packages-with-conda) to set up a python environment to which further packages can be added. We refer to this environment `myvenv`.

Add the following packages to install SmartSim ML wrapper:
```
conda activate myvenv
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
