#!/usr/bin/env python
import sys,os,time
import numpy as np
import time

JOBID = os.environ['PBS_JOBID'].split('.')[0]
my_dir=os.path.abspath(os.path.dirname(__file__))
howmany=1
t_data = np.array([])

def run_amb(i):
    st = time.time()
    os.system('mpirun -np 4 \
              -machinefile $PBS_NODEFILE ${AMBERHOME}/bin/sander -O \
              -i mdyn.in \
              -o mdout.out \
              -c ../min/da_e.rst \
              -ref ../../03.exp/da_e.inpcrd \
              -p ../../03.exp/da_e.prmtop \
              -r da_eq.rst \
              -x da_eq.mdcrd')
    tt = time.time()-st
    return tt

for i in range(1,howmany+1):
    t1 = run_amb(i)
    t_data = np.append(t_data,t1)
    if i%howmany==0:
        np.savetxt('time.dat',t_data,fmt='%.4f')
