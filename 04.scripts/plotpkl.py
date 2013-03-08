#!/usr/bin/env python
import sys,os,pickle,shutil,fnmatch,itertools
import os.path
from glob import glob
from sys import argv
import numpy as np
from random import *
from lockfile import FileLock  # provided in 04.scripts dir ->
import datetime,time                         # export PYTHONPATH

'''
lock = FileLock(__file__)
if lock.is_locked()==True: sys.exit()
lock.acquire()
'''

import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import LSQUnivariateSpline

my_dir = os.path.abspath(os.path.dirname(__file__))
num=sys.argv[1]

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
beta=-0.6
quota=xxquotaxx*xxhowmanyxx

# matplotlib begin
fig=plt.figure()
plt.clf()

def plot_work(data,st):
    rnd = np.random.RandomState(0x2913)
    indices = np.arange(data.shape[0])
    rnd.shuffle(indices)
    plot_indices = indices[1:data.shape[0]:1]   # plot this many
    phase = int(st)-1
    if phase == 0:
        d = np.linspace(spos,spos+domain[phase],data.shape[1])
    else:
        d = np.linspace(spos+domain[phase-1],spos+domain[phase],data.shape[1])
    for index in plot_indices:
        w_i = data[index,::,3]
        plt.plot(d,w_i,'#000000',linewidth=0.3)
def plot_pmf(data,st):
    print data.shape[0]
    phase = int(st)-1
    deltaf= np.log(np.exp(data[::,::,3]*beta).mean(axis=0))*(1/beta)
    if phase == 0:
        d = np.linspace(spos,spos+domain[phase],deltaf.shape[0])
    else:
        d = np.linspace(spos+domain[phase-1],spos+domain[phase],deltaf.shape[0])
    lb = st+' '+str(data.shape[0])
    plt.plot(d,deltaf,'r-',linewidth=4.0,label=lb)
    plt.plot(d,deltaf,'k--',linewidth=1.4)

def main_call(st,w_c,d_cp):
    acc = []
    wrk_pkl={}
    wrk_pkl= pickle.load(open('%s-sfwf.pkl' % st,'rb'))
    print len(wrk_pkl[st])
    seeds = wrk_pkl[st].keys()
    #print seeds[::100]
    for s in seeds:
        sample_i = wrk_pkl[st][s][1]
        acc.append(sample_i)
    data = np.array(acc)
    print data.shape
    plot_work(data,st)
    plot_pmf(data,st)

w_c={}
w_c[0]=0
d_cp={}

# main call
dirs = []
for i in range(1,int(num)+1):
    dirs.append(str(i).zfill(2))
[main_call(st,w_c,d_cp) for st in sorted(dirs)]

# matplotlib end
#plt.legend(title='Stage | Steps | Traj\'s',loc='upper left', \
       #shadow=True, fancybox=True) #,bbox_to_anchor=(1.4,1))
plt.xlabel('Extension (A)')
plt.ylabel('Work (kcal/mol)')
plt.title('xxmoleculexx - xxngnxx - ASMD \n xxenvironxx xxvelxx A/ns')
plt.xlim([spos,spos+dist])
#plt.setp(plt.gca(),'yticklabels',[])
#plt.setp(plt.gca(),'xticklabels',[])
# LEGEND - details
'''
leg = plt.gca().get_legend()
ltext = leg.get_texts()
llines= leg.get_lines()
frame = leg.get_frame()
frame.set_facecolor('0.90')
plt.setp(ltext, fontsize='small')
plt.setp(llines, linewidth=1)
'''
plt.draw()

def tex_pic(n):
    texdir = os.path.join(('/'.join(my_dir.split('/')[0:-2])), \
                       'tex_%s/fig_pmf' % my_dir.split('/')[-3])
    if not os.path.exists(texdir): os.makedirs(texdir)
    plt.savefig('%s/xxplotnamexxpkl%s.png' % (texdir,n))
    plt.savefig('%s/xxplotnamexxpkl%s.eps' % (texdir,n))
def continue_pic(n):
    plotname = '%s-pk' % num
    plt.savefig('%s.png' % plotname)
    plt.savefig('%s.eps' % plotname)

tex_pic(num)
#continue_pic(num)
