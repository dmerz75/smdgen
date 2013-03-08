#!/bin/bash
#PBS -N xxjobnamexx
#PBS -j oe
#PBS -l xxwalltimexx
#PBS -l pmem=220mb
#PBS -l xxnodesxx
#PBS -V

# job properties
GRO_DIR=/share/apps/gromacs-4.5.5/
export PATH=${GRO_DIR}:${PATH}
export LD_LIBRARY_PATH=${GRO_DIR}:${LD_LIBRARY_PATH}

cd $PBS_O_WORKDIR

# run job
./go.py
