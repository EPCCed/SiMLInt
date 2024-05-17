# SiMLInt Docker Image

A containerised version of SiMLInt that performs an example simulation with LC is provided via [SiMLInt Docker image](https://github.com/EPCCed/SiMLInt/pkgs/container/simlint).

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)

## Building the Docker Image

To pull the Docker image:

```shell
docker pull ghcr.io/epcced/simlint:latest
```

Alternatively, to buid the Docker image:

```shell
cd $SIMLINT_HOME
docker build -t simlint -f files/container/Dockerfile .
```

## Running the Docker Image

Before running, the `containerised-runs` folder must be writable by Docker:

```shell
chmod -R 777 $SIMLINT_HOME/files/containerised-runs
```

To run the SiMLInt Docker image follow these steps:

1. "Pure" BOUT++ Simulation: Run the following command:

    ```shell
    cp $SIMLINT_HOME/files/6-simulation/BOUT.inp $SIMLINT_HOME/files/containerised-runs/data; \
    cp $SIMLINT_HOME/files/containerised-runs/BOUT.restart.0.nc $SIMLINT_HOME/files/containerised-runs/data; \
    docker run -v $SIMLINT_HOME/files/containerised-runs:/sim -u $(id -u):$(id -g) ghcr.io/epcced/simlint:latest mpirun -np 1 bout-hw nout=10
    ```

2. Ground-truth simulation:

    ```shell
    cp $SIMLINT_HOME/files/6-simulation/BOUT.inp $SIMLINT_HOME/files/containerised-runs/data; \
    cp $SIMLINT_HOME/files/containerised-runs/BOUT.restart.0.nc $SIMLINT_HOME/files/containerised-runs/data; \
    docker run -v $SIMLINT_HOME/files/containerised-runs:/sim -u $(id -u):$(id -g) ghcr.io/epcced/simlint:latest mpirun -np 1 gt-hw nout=10
    ```

    For these first two commands, the OpenMPI command `mpirun -n 1`, which instructs BOUT++ to use one processor only due to the format of the example input data, can be instructed to use *N* processors `mpirun -n N`, however appropriately decomposed input data must be provided.

3. Inference runs:

    ```shell
    cp $SIMLINT_HOME/files/6-simulation/BOUT.inp $SIMLINT_HOME/files/containerised-runs/data && \
    cp $SIMLINT_HOME/files/containerised-runs/BOUT.restart.0.nc $SIMLINT_HOME/files/containerised-runs/data && \
    docker run -v $SIMLINT_HOME/files/containerised-runs:/sim -v $SIMLINT_HOME/files/models:/models \
    -u $(id -u):$(id -g) ghcr.io/epcced/simlint:latest \
    smartsim-hw.sh 6899 /models/model-hw-20240427-164026-vort.pb /models/model-hw-20240427-210530-dens.pb 10
    ```

That's it! You have successfully built the SiMLInt Docker image and run it with a volume. Feel free to explore and modify the code inside the container as needed.

<!-- 


Running with Singularity is possible, but not optimised for the particular machine. Need to see how to connect it to ghcr.io.


# Using SiMLInt with Singularity
SiMLInt is available as a Docker image, with BOUT++, SmartSim and TensorFlow, and with an example Hasegawa-Wakatani simulation with and without inference available.
Typically, however, Singularity containers are preferred on HPC systems. And while it is recommended to install using the (system-adapted) SiMLInt installation instructions, it is possible to convert the Docker image to a Singularity image. Currently this 

To use this image with Singularity, build `simlint.sif` from the latest image:
```shell
singularity build simlint.sif docker://davedavemckay/simlint:latest
```

Then `exec`:
```shell
singularity exec simlint.sif mpirun -n 1 /BOUT-dev/build/examples/hasegawa-wakatani/hasegawa-wakatani
```

 -  Note: `simlint.sif` will be around 3 GB

 Check the image is as expected with `singularity inspect`, something like:
 ```shell
$ singularity inspect simlint.sif
org.label-schema.build-arch: amd64
org.label-schema.build-date: Monday_1_April_2024_10:36:5_BST
org.label-schema.schema-version: 1.0
org.label-schema.usage.singularity.deffile.bootstrap: docker
org.label-schema.usage.singularity.deffile.from: davedavemckay/simlint:latest
org.label-schema.usage.singularity.version: 3.7.2-1.el8
 ```

Further examples of use of the image are given in the SiMLInt-Docker [`README.md`](../README.md), however it is worth noting differences in syntax in terms of using host volume bindings.

Where the simplest volume binding method with Docker is the `--volume` option to `docker run`, i.e., `docker run --volume /host/path:/image/path`, Singularity uses an environment variable, e.g.,:
```bash
module load singularity
export SINGULARITY_BIND="/scratch/data,/opt,/work/x01/x01/username/sim:/sim"
srun singularity exec simlint.sif mpirun -n $nprocs /BOUT-dev/build/examples/hasegawa-wakatani/hasegawa-wakatani
```
will use the data in `/work/x01/x01/username/sim` to run the simulation.
This is especially useful where modules loaded on the HPC system are to be accessed by a container and the bind list gets quite long.

  - Note: while the above will allow SiMLInt to be run with Singularity, it uses OpenMPI compiled within the image for portability. To achieve performant simulation runs it is recommended that an image is built using recommended libraries on the target HPC system. To do this, the Dockerfile should be adapted to a [Singularity Definition File](https://docs.sylabs.io/guides/3.0/user-guide/definition_files.html).

An [example](run_simlint.sh) SLURM submission script that runs SiMLInt (BOUT only) on Cirrus is provided. Run with: `sbatch run_simlint.sh`. -->
