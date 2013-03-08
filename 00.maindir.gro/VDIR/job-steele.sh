#!/bin/bash
#PBS -q xxqueuexx
#PBS -N xxjobnamexx
#PBS -l pmem=220mb
#PBS -l xxwalltimexx
#PBS -l xxnodesxx
#PBS -j oe
#PBS -V

# job_________________________
module load gromacs/4.5.5_openmpi-1.6  #(default)
module load python/2.7.2

cd $PBS_O_WORKDIR

# run job
./go.py
