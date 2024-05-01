# Data Generation

Following the structure given in the [general data generation](ML_training.md) case, this page describes our implementation for the Hasegawa-Wakatani example.

1. Fine- and coarse-grained resolutions. We chose:
 - 1024x1024 for fine-grained simulations; and
 - 256x256 for coarse-grained simulations.

    For BOUT++ our implementation, we performed 2-d simulations, with guard cells in the x-dimension (1028 or 260 x values), 1 y value, and a periodic z-dimension (1024 or 256 values). Therefore the shapes of the variables used by BOUT++ are (1028x1x1024) for the fine-grained simulations and (260x1x256) for the coarse-grained simultions.

2. Generate a "fully resolved" simulation.

First, a "burn-in" or "equilibration" run must be conducted at the desired resolution. For an example of this, see [fine_init.sh](files/data-generation/fine_init.sh). Edit `<account>` on line 9 and `x01` in lines containing paths for your projec and submit via `sbatch fine_init.sh`.

Following that, we run a number of sequentially trajectories to generate fine-grained ground-truth data. See [fine_trajectories.sh](files/data-generation/fine_trajectories.sh)

The initial simulation produces "restart files", `/scratch/space1/x01/data/my-scratch-data/initial/data/BOUT.restart.*.nc` from which a simulation can be continued. Those, as well as the input file (`/scratch/space1/x01/data/my-scratch-data/initial/data/BOUT.inp` should be placed in `/scratch/space1/x01/data/my-scratch-data/0`.

Edit line 17 (`for TRAJ_INDEX in {1..10}`) to give the desired number of trajectories. Edit `<account>` on line 9 and `x01` in lines containing paths for your project and submit via `sbatch fine_trajectories.sh`.

3. Coarsen selected simulation snapshots. ## check this

Fine-grained data must be coarsened to match the desired coarse-grained resolution. This can be done via interpolation for a general solution. Files in [files/coarsening](files/coarsening) perform this task.
