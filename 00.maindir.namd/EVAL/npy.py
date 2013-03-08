#!/usr/bin/env python
import os, os.path
from glob import glob
import numpy as np
from random import randint
import datetime

my_dir='/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[0:-1])
now=datetime.datetime.now()
now=now.strftime("%Y%m%dt%H%M")
acc=[]

#os.chdir(os.path.join(my_dir,opdir))
num='xxnumxx'
dnum='xxnumxx.data'
ddir=os.path.join(my_dir,dnum)
if not os.path.exists(ddir): os.makedirs(ddir)

def pack(i):
    acc=[]
    for path in glob(os.path.join(my_dir,'%s.*/*-tef.dat*' % num)):
        if len(acc)==4:
	    break
        print path
        sample_i = np.loadtxt(path)
        os.remove(path)
        acc.append(sample_i)
    os.chdir(ddir)
    data = np.array(acc)
    if not len(data)==0:
        np.save('%s_%d_%s' % (num,i,now),data)
    else:
        print "zero trajectories remain"

count=0
for path in glob(os.path.join(my_dir,'%s.*/*-tef.dat*' % num)):
    count+=1
print count
for i in range(0,(count/4)+1):
    pack(i)
