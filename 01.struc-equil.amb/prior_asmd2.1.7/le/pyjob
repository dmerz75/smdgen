#!/bin/bash
#PBS -N mopac
#PBS -j oe
#PBS -l walltime=05:00:00:00
#PBS -l pmem=920mb
#PBS -l nodes=1:ppn=1
# #PBS -M dmerz3@gatech.edu
#PBS -V

# Job proper starts here

# Additional environment setting, if necessary
# export PATH=/some/dir/:$PATH
# run job ________________________
export AMBERHOME=/share/apps/amber11
source /opt/intel/Compiler/11.1/075/bin/iccvars.sh intel64
cd $PBS_O_WORKDIR 

# run job
./go.py
