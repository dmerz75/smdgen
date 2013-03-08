#!/bin/bash
#PBS -N eq
#PBS -j oe
#PBS -l pmem=220mb
#PBS -l walltime=24:00:00
#PBS -l nodes=1:ppn=1
#PBS -V

cd ${PBS_O_WORKDIR}
cat ${PBS_NODEFILE}

#ulimit -s
ulimit -s unlimited

# environment for Intel compiler version 11 and openmpi
export PATH=/opt/intel/Compiler/11.1/075/bin/intel64:${PATH}
export LD_LIBRARY_PATH=/opt/intel/Compiler/11.1/075/lib/intel64:/opt/intel/Compiler/11.1/075/mkl/lib/em64t:${LD_LIBRARY_PATH}
export PATH=/share/apps/openmpi-1.4.4/intel-11/bin:${PATH}
export LD_LIBRARY_PATH=/share/apps/openmpi-1.4.4/intel-11/lib:${LD_LIBRARY_PATH}

# set Amber environment
export AMBERHOME=/share/apps/amber11

# display number of processors and hosts file.
NP=`cat ${PBS_NODEFILE} | wc -l`
echo "number of processes = ${NP}"

# run job
./go.py
