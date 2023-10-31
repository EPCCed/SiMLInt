This page shows 1. how to install BOUT++ on Cirrus, and 2. how to install and set-up SmartSim so that in can communicate with BOUT++.

# 1. BOUT++

(copy from gitlab)


# 2. SmartSim with BOUT++

## Python/conda stuff 
Follow [Cirrus docs](https://docs.cirrus.ac.uk/user-guide/python/#installing-your-own-python-packages-with-conda) to set up a python environment to which further packages can be added.



## Add packages

```
conda activate myvenv
conda install git-lfs
git lfs install
conda install cmake
python -m pip install smartsim[ml]
```

Build:

```
module load mpt
module load intel-compilers-19
export CC=mpicc
export CXX=mpicxx

smart build --device cpu  
```

## Build SmartRedis libraries

Clone the git repo and the required version and build:
```
git clone https://github.com/CrayLabs/SmartRedis.git --branch v0.4.1 smartredis
cd smartredis
make lib
```

The install path is then available in `smartredis/install`. Modify the `CMakeLists.txt` file to point to this path on your system in place of `/work/x01/x01/auser/smartsim/smartredis/install/include` on line 12.


[back](./)
