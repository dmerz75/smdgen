#!/usr/bin/env python
import sys,os,re,pickle,datetime,time,fnmatch,itertools
import os.path
from glob import glob
import numpy as np
from random import *
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import LSQUnivariateSpline

my_dir = os.path.abspath(os.path.dirname(__file__))

class mdict(dict):
    def __setitem__(self,key,value):
        self.setdefault(key,[]).append(value)
def print_dict(dct):
    for key,val in dct.items():
        print key,val
        print ''
    return key

config = pickle.load(open('config.pkl','rb'))
key = print_dict(config)

vel  = key
dist = config[vel][0][0]
ts   = config[vel][0][1]
path_seg   = config[vel][0][2]
path_svel  = config[vel][0][3]
path_vel   = config[vel][0][4]
path_steps = config[vel][0][5]
dct        = config[vel][0][6]       # 'freq'  50*ts/1000
dt         = dct['freq']*ts/1000
path_v_aps = path_vel/ts*1000
domain     = np.cumsum(((path_steps*ts)/1000)*path_v_aps)

spos=xxsposxx
num =str(len(path_steps)).zfill(2)

def pack(stage):
    def plot_ihb(data):
        phase = int(stage)-1
        if stage=='01':
            d = np.linspace(spos,spos+domain[phase],len(data.mean(axis=1)[0]))
            plt.plot(d,data.mean(axis=1)[0],'r-',label="i->i+3",linewidth=1.5)
            d = np.linspace(spos,spos+domain[phase],len(data.mean(axis=1)[1]))
            plt.plot(d,data.mean(axis=1)[1],'k-',label="i->i+4",linewidth=1.5)
            d = np.linspace(spos,spos+domain[phase],len(data.mean(axis=1)[2]))
            plt.plot(d,data.mean(axis=1)[2],'g-',label="i->i+5",linewidth=1.5)
        if stage!='01':
            d = np.linspace(spos+domain[phase-1],spos+domain[phase], \
                                             len(data.mean(axis=1)[0]))
            plt.plot(d,data.mean(axis=1)[0],'r-',linewidth=1.5)
            d = np.linspace(spos+domain[phase-1],spos+domain[phase], \
                                             len(data.mean(axis=1)[1]))
            plt.plot(d,data.mean(axis=1)[1],'k-',linewidth=1.5)
            d = np.linspace(spos+domain[phase-1],spos+domain[phase], \
                                             len(data.mean(axis=1)[2]))
            plt.plot(d,data.mean(axis=1)[2],'g-',linewidth=1.5)
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

# main call
dirs = []
for i in range(1,int(num)+1):
    dirs.append(str(i).zfill(2))
[pack(st) for st in sorted(dirs)]

# matplotlib
plt.xlabel('end-to-end distance (A)')
plt.ylabel('average H-bond count')
plt.title('xxmoleculexx | xxngnxx | ASMD | Charmm22 \n \
          All Hydrogen Bonds, intra-protein, xxenvironxx')
plt.legend()
plt.gca().set_ylim(ymin=-0.2)
plt.draw()

texdir = os.path.join(('/'.join(my_dir.split('/')[0:-2])), \
                       'tex_%s/fig_bond' % my_dir.split('/')[-3])
if not os.path.exists(texdir): os.makedirs(texdir)
plotname = 'xxplotnamexx_ihbond'
plt.savefig('%s/%s.png' % (texdir,plotname))
plt.savefig('%s/%s.eps' % (texdir,plotname))
