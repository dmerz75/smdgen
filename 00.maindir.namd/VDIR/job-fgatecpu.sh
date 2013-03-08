#!/bin/bash
#PBS -N xxjobnamexx
#PBS -j oe
#PBS -l xxwalltimexx
#PBS -l pmem=220mb
#PBS -l xxnodesxx
#PBS -V

# job properties
NAMD_DIR=/share/apps/NAME_2.9_Linux-x86-64-multicore/
export PATH=${NAMD_DIR}:${PATH}
export LD_LIBRARY_PATH=${NAMD_DIR}:${LD_LIBRARY_PATH}

cd $PBS_O_WORKDIR

# run job
./go.py
