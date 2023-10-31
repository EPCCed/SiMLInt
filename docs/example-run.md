### Run using the scheduler

The slurm job file starts the SmartSim orchestrator (in Python) with a Redis database and RedisAI communication layer.
The environment variable SSDB points to the database entrypoint to which the simulation connects.
In this example, the Redis DB runs on the same node since the simulation only runs in one process.

*link the file*
