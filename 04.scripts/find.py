#!/usr/bin/env python
import sys, os, glob
import os.path
from glob import glob
import fnmatch
import itertools

my_dir = os.path.abspath(os.path.dirname(__file__))

acc=[]
for root, dirnames, filenames in os.walk(my_dir):
    for filename in fnmatch.filter(filenames, '*tef.dat*'):
        jobs=os.path.join(root,filename)
        dir='/'.join(jobs.split('/')[0:-1])
        a=(jobs.split('/')[-2]).split('.')[0]
        if (a=='04') or (a=='04') or (a=='04'):
            print jobs
            b=(jobs.split('/')[-4]).split('.')[-2]
            b2=(jobs.split('/')[-4]).split('.')[-1]
            b3=b+b2
            c=(jobs.split('/')[-3]).split('.')[1]
            #print c
            d=(jobs.split('/')[-2])
            #print d
            f=b3+c
            print f
            acc.append(f)
            os.chdir(dir)
            #os.system('qsub %s' % jobs)
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
    mydata.append(t)
