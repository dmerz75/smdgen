#!/usr/bin/env python
import sys,os
import os.path
from glob import glob
import fnmatch
import itertools

my_dir = os.path.abspath(os.path.dirname(__file__))
acc=[]

def qsub_job(s,v,st):
    for root, dirnames, filenames in os.walk(my_dir):
        for filename in fnmatch.filter(filenames,'job.sh'):
            num=(root.split('/')[-3])
            sol=(root.split('/')[-4]).split('.')[1]
            stg=(root.split('/')[-2])
            if (num==v) and (sol==s) and (stg==st):
                jobs=os.path.join(root,filename)
                print jobs
                jtype=v+s+st
                acc.append(jtype)
                #root='/'+'/'.join(root.split('/')[2:])
                #jobs=os.path.join(root,'job.sh')
                #print root
                #print jobs
                os.chdir(root)
                os.system('qsub %s' % jobs)
                #os.system('./job.sh &')

solvents   = ['vac']
#solvents   = ['vac','imp','exp']
velocities = ['02']
stages     = ['01']
# MAIN SUBMISSION CALL
# alternatively, qsub_job('01','vac')
[qsub_job(s,v,st) for s in solvents for v in velocities for st in stages]


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
