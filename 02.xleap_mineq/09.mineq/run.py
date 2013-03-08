#!/usr/bin/env python
import sys, os, glob
import os.path
from glob import glob
import fnmatch
import itertools

my_dir = os.path.abspath(os.path.dirname(__file__))
acc=[]

def qsub_job(sjob,sol):
    for root, dirnames, filenames in os.walk(my_dir):
        for filename in fnmatch.filter(filenames,'job.sh'):
            sj=(root.split('/')[-1])
            solv=(root.split('/')[-2]).split('.')[2]
            if (sj==sjob) and (solv==sol):
                jobs=os.path.join(root,filename)
                jtype=sjob+sol
                acc.append(jtype)
                root='/'+'/'.join(root.split('/')[2:])
                jobs=os.path.join(root,'job.sh')
                print jobs
                os.chdir(root)
                os.system('qsub %s' % jobs)

solv = ['v','i','e']
subj = ['min']
#subj = ['mdyn']
#subj = ['equil']
[qsub_job(subj[0],s) for s in solv]

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
