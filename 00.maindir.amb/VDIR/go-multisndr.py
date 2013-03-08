#!/usr/bin/env python
import sys,os,time
import numpy as np
import datetime

JOBID = os.environ['PBS_JOBID'].split('.')[0]
#now=datetime.datetime.now().strftime("%m%dt%H%M")

howmany= xxhowmanyxx
t_data = np.array([])
num    = 'xxnumxx'

def run_amb(i):
    st = time.time()
    os.system('mpirun -np xxnodecountxx \
              -machinefile $PBS_NODEFILE ${AMBERHOME}/bin/sander -O \
              -i smd.in \
              -o run.log \
              -c ../../xxstrucequilxx/00.inpcrd \
              -p ../../xxstrucequilxx/00.prmtop \
              -r md_smd.rst \
              -x mdtraj.mdcrd \
              -v mdvel.mdvel')
    tt = time.time()-st
    os.system("mv dist_vs_t %d-tef.dat.%s" % (i,JOBID))
    os.system("python ../%s-hb.py %d %s" % (num,i,JOBID))
    return tt

for i in range(1,howmany+1):
    t1 = run_amb(i)
    t_data = np.append(t_data,t1)
    if i ==1:
        os.system('mv mdtraj.mdcrd %d-mdtraj.mdcrd.%s' % (i,JOBID))
    if i%8==0 or i%howmany==0:
        #np.save('%d_time' % i,t_data)
        np.savetxt('time.dat',t_data,fmt='%.4f')

os.system('rm *.BAK')
os.system('rm *.rst')
os.system('rm mden')
os.system('rm mdinfo')
os.system('rm *.mdcrd')
os.system('rm run.log')
