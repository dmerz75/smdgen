#!/usr/bin/env python
import sys,os,re
import os.path
from glob import glob
import fnmatch
import itertools
import numpy as np
from random import *
import datetime
import time
import pickle
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import LSQUnivariateSpline

my_dir = os.path.abspath(os.path.dirname(__file__))
now=datetime.datetime.now()
now=now.strftime("%Y%m%dt%H%M")

spos=xxsposxx
v   =xxvelapsxx
dt  =xxdtxx
beta=-0.6

class mdict(dict):
    def __setitem__(self,key,value):
        self.setdefault(key,[]).append(value)
pmf_ideal = mdict()
work_used = mdict()
corr_work = mdict()

def select_traj(dct,wfsd,JA):
    for keys,values in dct.iteritems():
        wf=np.cumsum(values[::,3]*v*dt)[-1]
        wfsd[wf]=keys
    seed=wfsd.get(JA, wfsd[min(wfsd.keys(), key=lambda k: abs(k-JA))])
    return seed

def corrected_work(data,stage,sdwf,work_used):
    if stage=='01':
        cdata = data[::,::,3]
        corr_work[stage]=0
    elif stage!='01':
        uptonowstages=[str(st).zfill(2) for st in range(1,int(stage))]
        print uptonowstages
        awp=[]
        for i in uptonowstages:
            print 'work_used i',work_used[i]
            awp.append(work_used[i])
        print awp
        dawp=np.array(awp)
        print dawp
        wp=np.cumsum(dawp)[-1]
        print wp
        corr_work[stage]=wp
    xmin = int(stage)*2+spos-2
    xmax = int(stage)*2+spos

def write_data(data,info,stage):
    xmin = int(stage)*2+spos-2
    xmax = int(stage)*2+spos
    data[::,::,3] = np.exp(np.cumsum(data[::,::,3]*v*dt,axis=1)*beta)
    deltaf = np.log(data[::,::,3].mean(axis=0))*(1/beta)
    domain=np.linspace(xmin,xmax,len(deltaf))
    dataout=np.column_stack((domain,deltaf))
    JA=deltaf[-1]
    pmf_ideal[stage]=deltaf[-1]
    wfsd={}
    seed=select_traj(info,wfsd,JA)
    sdwf = dict((v,k) for k,v in wfsd.iteritems())
    work_used[stage]=sdwf[seed]
    print 'stage',stage,'JA',JA,'seed',seed,'work',sdwf[seed]
    corrected_work(data,stage,sdwf,work_used)

def pack(stage):
    info={}
    acc=[]
    for path in glob(os.path.join(my_dir,'%s/*/*-tef.dat.*' % stage)):
        #print path
        seed = path.split('/')[-2]
        sample_i = np.loadtxt(path)
        #os.remove(path)
        acc.append(sample_i)
        info[seed]=sample_i
    data = np.array(acc)
    write_data(data,info,stage)

[pack(str(st).zfill(2)) for st in range(1,11)]
print 'ideally, the jarzynski averaging result was'
print pmf_ideal
print 'however, work from coordinates/vels available'
print work_used
print 'corrected work, for prepending...'
print corr_work

def plot_multi_traj(data,domain):
    rnd = np.random.RandomState(0x1913)
    indices = np.arange(data.shape[0])
    rnd.shuffle(indices)
    plot_indices = indices[1:200:1]
    for index in plot_indices:
        w_i = data[index,::,3]
        print w_i
        ax1.plot(domain[::1],w_i[::1],'#660033',linewidth=0.4)

def plot_pmf(deltaf,domain):
    ax1.plot(domain[::1], deltaf[::1],'b-',linewidth=3)
    ax1.plot(domain[::1], deltaf[::1],'k--',linewidth=0.6)

def pack2(stage):
    acd=[]
    for path in glob(os.path.join(my_dir,'%s/*/*-tef.dat.*' % stage)):
        sample_i = np.loadtxt(path)
        acd.append(sample_i)
    data = np.array(acd)
    xmin = int(stage)*2+spos-2
    xmax = int(stage)*2+spos
    data[::,::,3] = np.cumsum(data[::,::,3]*v*dt,axis=1)
    df = np.exp(data[::,::,3]*beta)
    deltaf = np.log(df.mean(axis=0))*(1/beta)+corr_work[stage]
    domain=np.linspace(xmin,xmax,data.shape[1])
    data[::,::,3] = data[::,::,3]+corr_work[stage]
    plot_multi_traj(data,domain)
    plot_pmf(deltaf,domain)

# PLOT - pmf
fig=plt.figure()
plt.clf()
ax1=fig.add_subplot(111)

[pack2(str(st).zfill(2)) for st in range(1,11)]

#ax1.xlabel('Extension (A)')
ax1.set_xlabel('Extension (A)')
ax1.set_ylabel('Work (kcal/mol)')
plt.title('xxmoleculexx - xxngnxx - ASMD \n xxenvironxx xxvelansxx A/ns')
ax1.set_ylim([-2,50.5])
ax1.set_xlim([13,33.0])
texdir = os.path.join(('/'.join(my_dir.split('/')[0:-2])), \
                       'tex_%s/fig_pmf' % my_dir.split('/')[-3])
if not os.path.exists(texdir): os.makedirs(texdir)

spos=13

def pack(stage):
    def plot_ihb(data):
        xmin = int(stage)*2+spos-2
        xmax = int(stage)*2+spos
        if stage=='01':
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[0]))
            ax2.plot(domain,data.mean(axis=1)[0],'r-',label="i->i+3",linewidth=1.5)
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[1]))
            ax2.plot(domain,data.mean(axis=1)[1],'k-',label="i->i+4",linewidth=1.5)
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[2]))
            ax2.plot(domain,data.mean(axis=1)[2],'g-',label="i->i+5",linewidth=1.5)
        if stage!='01':
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[0]))
            ax2.plot(domain,data.mean(axis=1)[0],'r-',linewidth=1.5)
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[1]))
            ax2.plot(domain,data.mean(axis=1)[1],'k-',linewidth=1.5)
            domain = np.linspace(xmin,xmax,len(data.mean(axis=1)[2]))
            ax2.plot(domain,data.mean(axis=1)[2],'g-',linewidth=1.5)
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
#fig=plt.figure()
#plt.clf()
ax2 = ax1.twinx()

[pack(str(st).zfill(2)) for st in range(1,11)]

# matplotlib
ax2.set_ylabel('average H-bond count')
ax2.set_ylim([-0.1,7.2])

def plot_hb(data,stage):
    xmin = int(stage)*2+spos-2
    xmax = int(stage)*2+spos
    domain = np.linspace(xmin,xmax,len(data))
    print domain
    if stage =='01':
        ax2.plot(domain,data,'k-',label="H-bonds",linewidth=1)
    elif stage !='01':
        ax2.plot(domain,data,'k-',linewidth=1)

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
#fig=plt.figure()
#plt.clf()

[pack(str(st).zfill(2)) for st in range(1,11)]

# matplotlib
plt.legend(loc=2)
plt.draw()

#plt.savefig('danamdvacvv100asmd.png')
#plt.savefig('danamdvacvv100asmd.eps')
plt.savefig('%s/xxplotnamexx_enable.png' % texdir)
plt.savefig('%s/xxplotnamexx_enable.eps' % texdir)
