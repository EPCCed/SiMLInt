# SiMLInt Data Generation Implementation 

Following the structure given in the [general data generation](ML_training.md) case, this page describes the data generation phase of our implementation for the Hasegawa-Wakatani example.

1. Fine- and coarse-grained resolutions. We chose:
 - 1024x1024 for fine-grained simulations; and
 - 256x256 for coarse-grained simulations.

    For BOUT++ our implementation, we performed 2-d simulations, with guard cells in the x-dimension (1028 or 260 x values), 1 y value, and a periodic z-dimension (1024 or 256 values). Therefore the shapes of the variables used by BOUT++ are (1028x1x1024) for the fine-grained simulations and (260x1x256) for the coarse-grained simultions.

2. Generate a "fully resolved" simulation

    The first step is to create a modified version of the Hasegawa-Wakatani example from BOUT++, which we'll copy to your work directory.

    ```shell
    # For full compatibility with the test simulations run during the SiMLInt project, the diffusive function is modified.
    cp -r $WORK/BOUT-dev/examples/hasegawa-wakatani $WORK/my-hw
    cd $WORK/my-hw
    sed -i 's/-Dn \* Delp4(n);/+Dn \* Delp2(n);/g' hw.cxx
    sed -i 's/-Dvort \* Delp4(vort);/+Dvort \* Delp2(vort);/g' hw.cxx
    ```

    Compile the code.
    ```
    module load intel-20.4/mpi
    module load intel-20.4/compilers
    module load fftw/3.3.10-intel20.4-impi20.4
    module load netcdf-parallel/4.9.2-intel20-impi20
    module load cmake

    cmake . -B build -Dbout++_DIR=$WORK/BOUT-dev/build -DCMAKE_CXX_FLAGS=-std=c++17 -DCMAKE_BUILD_TYPE=Release
    cmake --build build --target hasegawa-wakatani
    ```

    Before simulating the training data, a burn-in run must be conducted at the desired resolution. For an example of this, see [fine_init.sh](https://github.com/EPCCed/SiMLInt/tree/main/files/1-data-generation/fine_init.sh).

    Clone the repository if you haven't already done this:
    ```
    git clone https://github.com/EPCCed/SiMLInt.git
    ```
    
    Submit the burn-in run:
    ```
    $ACCOUNT=x01
    cd files/1-data-generation/
    sbatch fine_init.sh --account $ACCOUNT
    ```

    Following that, we run a number of sequentially trajectories to generate fine-grained ground-truth data. See [fine_trajectories.sh](https://github.com/EPCCed/SiMLInt/tree/main/files/1-data-generation/fine_trajectories.sh)

    The initial simulation produces "restart files" `BOUT.restart.*.nc` from which a simulation can be continued.

    Edit `fine_trajectories.sh`
    ```bash
    for TRAJ_INDEX in {1..10}
    ```
    to give the desired number of trajectories.

3. Coarsen selected simulation snapshots.

    Fine-grained data must be coarsened to match the desired coarse-grained resolution. This can be done via interpolation for a general solution. Files in [files/2-coarsening](https://github.com/EPCCed/SiMLInt/tree/main/files/2-coarsening) perform this task. Submit `submit-resize.sh` via `sbatch submit-resize.sh`.

    Note: this operates on one trajectory at a time and will therefore need to be repeated for each trajectory run in step 2.

4. Single-timestep coarse simulations.

    With the previous step having extracted fine-grained data for each time step (and each trajectory for which it was repeated), we now need to run a single-timestep coarse-grained simulation. To do this, see [files/3-coarse_simulations](../files/3-coarse_simulations/). Submitting [run_coarse_sims.sh](https://github.com/EPCCed/SiMLInt/tree/main/files/3-coarse_simulations/run_coarse_sims.sh) will run a single step simulation for each coarsened timestep created in the previous step.

5. Generating training data.

    We now have all of the data required to train the ML models, but not in the format we require. Files in [files/4-training-data](../files/4-training-data) perform this task. Edit [files/4-training-data/](../files/4-training-data/sub_gen_training_nc.sh) and [files/4-training-data/gen_training_nc.py](../files/4-training-data/gen_training_nc.py) so that the paths work with your setup.
    
    Note: paths are hardcoded in [files/4-training-data/gen_training_nc.py](../files/4-training-data/gen_training_nc.py), not read in from the command line.

Subsequent steps: calculating the error and model training are covered in [ML model training implementation](training_implementation.md).

[< Back](./)
