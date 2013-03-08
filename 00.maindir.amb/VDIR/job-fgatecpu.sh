#!/bin/bash
#PBS -N xxjobnamexx
#PBS -j oe
#PBS -l pmem=220mb
#PBS -l xxwalltimexx
#PBS -l xxnodesxx
#PBS -V

# run job ________________________
export AMBERHOME=/share/apps/amber11
source /opt/intel/Compiler/11.1/075/bin/iccvars.sh intel64

cd $PBS_O_WORKDIR

# run job
./go.py
