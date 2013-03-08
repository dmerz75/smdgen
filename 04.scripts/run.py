#!/usr/bin/env python
import sys, os, glob
import os.path
from glob import glob
import fnmatch
import itertools

my_dir = os.path.abspath(os.path.dirname(__file__))
acc=[]

def qsub_job(vel,solv):
    for root, dirnames, filenames in os.walk(my_dir):
        for filename in fnmatch.filter(filenames,'job.sh'):
            num=(root.split('/')[-1]).split('.')[0]
            sol=(root.split('/')[-2]).split('.')[1]
            if (num==vel) and (sol==solv):
                jobs=os.path.join(root,filename)
                print jobs
                mol=(jobs.split('/')[-4]).split('_')[1]
                jtype=mol+vel+solv
                acc.append(jtype)
                #root='/'+'/'.join(root.split('/')[2:])
                #jobs=os.path.join(root,'job.sh')
                #print root
                #print jobs
                os.chdir(root)
                os.system('qsub %s' % jobs)
                #os.system('./job.sh &')

velocities = ['01','02','03']
solvents   = ['vac','imp','exp']
# MAIN SUBMISSION CALL
# alternatively, qsub_job('01','vac')
[qsub_job(v,s) for v in velocities for s in solvents]

print len(acc)

result={}
def count():
    for cond in acc:
        if cond not in result:
            result[cond]= 0
        result[cond] += 1
count()

os.chdir(my_dir)
for key in result:
    print key + '  ' + str(result[key])
    t = key + '  ' + str(result[key])
