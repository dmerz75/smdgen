#!/usr/bin/env python
import sys,os
import os.path
from glob import glob
import fnmatch
import itertools
import numpy as np
from random import *
import pickle
import datetime
import time
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import LSQUnivariateSpline

my_dir = os.path.abspath(os.path.dirname(__file__))
now=datetime.datetime.now()
now=now.strftime("%Y%m%dt%H%M")

spos=xxsposxx

def plot_hb(data,stage):
    xmin = int(stage)*2+spos-2
    xmax = int(stage)*2+spos
    domain = np.linspace(xmin,xmax,len(data))
    print domain
    if stage =='01':
        plt.plot(domain,data,'k-',label="hydrogen bonds",linewidth=1)
    elif stage !='01':
        plt.plot(domain,data,'k-',linewidth=1)

def pack(stage):
    def bond_count(trj,ii):
        lens = [(len(acc[trj][n])) for n in range(len(acc[trj]))]
        return lens
    acc=[]
    for path in glob(os.path.join(my_dir,'%s/*/*-hb_p*.pkl.*' % stage)):
        print path
        sample_i = pickle.load(open(path,'rb'))
        acc.append(sample_i)
    acclens= []
    for c in range(len(acc)):
        lens = bond_count(c,3)
        print lens
        acclens.append(lens)
    idata= np.array(acclens)
    data = idata.mean(axis=0)
    print data
    time.sleep(0.4)
    plot_hb(data,stage)

# PLOT - pmf
fig=plt.figure()
plt.clf()

[pack(str(st).zfill(2)) for st in range(1,11)]

# matplotlib
plt.xlabel('end-to-end distance (A)')
plt.ylabel('average H-bond count')
plt.title('da | NAMD | ASMD | Charmm22 \n \
          All Hydrogen Bonds, intra-protein, vac')
plt.legend()
plt.gca().set_ylim(ymin=-0.2)
#plt.axis([9.9,35.1,-.1,7.4])
plt.draw()

texdir = os.path.join(('/'.join(my_dir.split('/')[0:-2])), \
                       'tex_%s/fig_bond' % my_dir.split('/')[-3])
if not os.path.exists(texdir): os.makedirs(texdir)
#plt.savefig('danamdvacvv100asmd.png')
#plt.savefig('danamdvacvv100asmd.eps')
plt.savefig('%s/hbond.png' % texdir)
plt.savefig('%s/hbond.eps' % texdir)
