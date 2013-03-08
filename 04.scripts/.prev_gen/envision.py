#!/usr/bin/env python
import sys,os
import os.path
from glob import glob
import fnmatch
import itertools
import numpy as np
from random import *
import datetime
import time

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
        plt.plot(domain[::1],w_i[::1],'#660033',linewidth=0.4)

def plot_pmf(deltaf,domain):
    plt.plot(domain[::1], deltaf[::1],'b-',linewidth=3)
    plt.plot(domain[::1], deltaf[::1],'k--',linewidth=0.6)

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

[pack2(str(st).zfill(2)) for st in range(1,11)]

plt.xlabel('Extension (A)')
plt.ylabel('Work (kcal/mol)')
plt.title('xxmoleculexx - xxngnxx - asmd \n xxenvironxx 100.0 A/ns')
#plt.ylim([ymin,ymax])
plt.xlim([xxstartconstraintxx,xxendconstraintxx])
plt.draw()
texdir = os.path.join(('/'.join(my_dir.split('/')[0:-2])), \
                       'tex_%s/fig_pmf' % my_dir.split('/')[-3])
if not os.path.exists(texdir): os.makedirs(texdir)
#plt.savefig('xxplotnamexx.png')
#plt.savefig('xxplotnamexx.eps')
plt.savefig('%s/xxplotnamexx.png' % texdir)
plt.savefig('%s/xxplotnamexx.eps' % texdir)
