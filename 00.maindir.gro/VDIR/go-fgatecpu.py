#!/usr/bin/env python
import sys,os,time
import numpy as np
import datetime

JOBID = os.environ['PBS_JOBID'].split('.')[0]
#now=datetime.datetime.now().strftime("%m%dt%H%M")

howmany= xxhowmanyxx
t_data = np.array([])
num    = 'xxnumxx'

def run_namd(i):
    os.system('grompp -f smd.mdp -c ../../xxstrucequilxx/00.gro \
              -p ../../topol/topol.top
              -n ../../xxstrucequilxx/index.ndx \
              -o md.tpr')
    st = time.time()
    os.system('mpirun -np xxnodecountxx \
              -machinefile $PBS_NODEFILE ${GRO_DIR}/bin/mdrun \
              -s md.tpr \
              -o traj.trr \
              -pf fsmd.xvg \
              -px xsmd.xvg')
    tt = time.time()-st
    os.system('mv fsmd.xvg %d-tef.dat.%s' % (i,JOBID))
    os.system('python ../%s-hb.py %d %s' % (num,i,JOBID))
    return tt

for i in range(1,howmany+1):
    t1 = run_namd(i)
    t_data = np.append(t_data,t1)
    if i==1:
        os.system('mv traj.trr %d-traj.trr.%s' % (i,JOBID))
    if i%8==0 or i%howmany==0:
        #np.save('%d_time' % i,t_data)
        np.savetxt('time.dat',t_data,fmt='%.4f')

#os.system('rm *#*')
#os.system('rm .gro')
#os.system('rm .log')
