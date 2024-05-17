#!/bin/bash
python /start_db.py $1 $2 $3
export SSDB=127.0.0.1:$1
mpirun -np 1 smartsim-hw nout=$4
