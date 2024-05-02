# Inference

Running a simulation with LC using the SiMLInt framework requires SmartSim, BOUT++ (with modified [hw.cxx](https://github.com/EPCCed/SiMLInt/tree/main/files/HW-error-correction/hw.cxx)) and TensorFlow. To install these, follow the [example installation](example-installation.md). The modifications made to `hw.cxx` differ from those made for ground-truth data generation. Now the SmartRedis Client is included to send/receive data from the SmartRedis database, request ML model runs and add the inferred error correction to BOUT++ internal variables for vorticity and density.

- Run a simulation via `sbatch submit-hw.sh`.

The output should differ slightly from a "pure" BOUT++ Hasegawa-Wakatani in that information about the SmartRedis database is given, and extra lines are produced during simulation to give timing information on communication with the database.

To visualise the result of this, or any other BOUT++ simulations, see the Jupyter Notebook, [Visualise.ipynb](https://github.com/EPCCed/SiMLInt/tree/main/files/7-visualisation/Visualise.ipynb).

[< Back](./)