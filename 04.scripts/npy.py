#!/usr/bin/env python
import os, os.path
from glob import glob
import numpy as np

my_dir=os.path.abspath(os.path.dirname(__file__))
acc=[]

num='02'
opdir='02.100'

def pack(i):
    acc=[]
    for path in glob(os.path.join(my_dir,'%s.100/*-tef.dat.*' % num)):
        if len(acc)==20:
	    break
        print path
        sample_i = np.loadtxt(path)
        os.remove(path)
        acc.append(sample_i)
    data = np.array(acc)
    np.save('%s_%d.npy' % (num,i),data)

os.chdir(os.path.join(my_dir,opdir))
count=((len([name for name in os.listdir('.') if os.path.isfile(name)]))/20)+1

for i in range(1,count):
    pack(i)
