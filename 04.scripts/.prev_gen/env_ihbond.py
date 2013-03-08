#!/usr/bin/env python
import sys,os,re
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

def pack(stage):
    def plot_ihb(data):
        xmin = int(stage)*2+spos-2
        xmax = int(stage)*2+spos
        if stage=='01':
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[0]))
            plt.plot(domain,data.mean(axis=1)[0],'r-',label="i->i+3",linewidth=1.5)
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[1]))
            plt.plot(domain,data.mean(axis=1)[1],'k-',label="i->i+4",linewidth=1.5)
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[2]))
            plt.plot(domain,data.mean(axis=1)[2],'g-',label="i->i+5",linewidth=1.5)
        if stage!='01':
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[0]))
            plt.plot(domain,data.mean(axis=1)[0],'r-',linewidth=1.5)
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[1]))
            plt.plot(domain,data.mean(axis=1)[1],'k-',linewidth=1.5)
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[2]))
            plt.plot(domain,data.mean(axis=1)[2],'g-',linewidth=1.5)
    def residue_index(label):
        return int(re.sub("[^0-9]","",label))
    def charac_bond2(trajectory, distance_target):
        acc_count_frames = []
        for frame in trajectory:
            acc_count = 0
            for bond in frame:
                distance = residue_index(bond[2]) - residue_index(bond[3])
                if distance == distance_target:
                   acc_count += 1
            acc_count_frames.append(acc_count)
        return acc_count_frames
    def bond_count(trj,ii):
        lens = [(len(acc[trj][n])) for n in range(len(acc[trj]))]
        return lens
    ####
    acc=[]
    for path in glob(os.path.join(my_dir,'%s/*/*-hb_p*.pkl.*' % stage)):
        print path
        sample_i = pickle.load(open(path,'rb'))
        acc.append(sample_i)
    b_data = np.array([[charac_bond2(traj_i, n) for traj_i in acc]
        for n in [3,4,5]])
    trj  = str(len(acc))
    trjl = len(acc[0])
    plot_ihb(b_data)

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
plt.savefig('%s/ihbond.png' % texdir)
plt.savefig('%s/ihbond.eps' % texdir)
