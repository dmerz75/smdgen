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
quota=xxhowmanyxx*xxquotaxx

# matplotlib begin
fig=plt.figure()
plt.clf()

def calc_work(data,st,w_c):
    phase = int(st)-1
    data[::,3] = np.cumsum(data[::,3]*path_v_aps[phase]*dt)
    data[::,3] = data[::,3] + w_c[phase]
    wf = data[::,3][-1]
    if phase == 0:
        d = np.linspace(spos,spos+domain[phase],data.shape[0])
    else:
        d = np.linspace(spos+domain[phase-1],spos+domain[phase],data.shape[0])
    plt.plot(d,data[::,3],'#000000',linewidth=0.3)
    return data,wf
def calc_pmf(data,st,w_c):
    phase = int(st)-1
    data[::,::,3] = np.cumsum(data[::,::,3]*path_v_aps[phase]*dt,axis=1)
    data[::,::,3] = data[::,::,3] + w_c[phase]
    deltaf = np.log(np.exp(data[::,::,3]*beta).mean(axis=0))*(1/beta)
    if phase == 0:
        d = np.linspace(spos,spos+domain[phase],deltaf.shape[0])
    else:
        d = np.linspace(spos+domain[phase-1],spos+domain[phase],deltaf.shape[0])
    lb = st+' '+str(int(path_steps[phase]))+' '+str(quota)
    plt.plot(d,deltaf,'r-',linewidth=4.0,label=lb)
    plt.plot(d,deltaf,'k--',linewidth=1.4)
    JA = deltaf[-1]
    return JA

class asmd_calcs:
    def __init__(self,wrk_pkl,w_c,d_cp):
        self.wrk = wrk_pkl
        self.w_c = w_c
        self.d_cp = d_cp
    def create_pkl(self,st):
        acc = []
        self.wrk[st]={}
        self.d_cp[st]={}
        stdir = os.path.join(my_dir,st)
        folds=[f for f in os.listdir(stdir) if os.path.isdir(os.path.join( \
                                                        stdir,f))]
        foldp=[os.path.join(stdir,f) for f in folds]
        seeds=[(p.split('/')[-2],p.split('/')[-1].split('.')[2]) for f in foldp \
               for p in glob(os.path.join(f,'*tef.dat*'))]
        seeds=[p.split('/')[-1].split('.')[2] for f in foldp \
                 for p in glob(os.path.join(f,'*tef.dat*'))]
        for path in glob(os.path.join(my_dir,'%s/*/*tef.dat*' % st)):
            folder = path.split('/')[-2]
            seed = path.split('/')[-1].split('.')[2]
            self.wrk[st][seed]={}
        for path in glob(os.path.join(my_dir,'%s/*/*tef.dat*' % st)):
            folder = path.split('/')[-2]
            seed = path.split('/')[-1].split('.')[2]
            sample_i = np.loadtxt(path)
            acc.append(sample_i)
            data_1= np.array(sample_i)
            tew,wf = calc_work(data_1,st,self.w_c)    # converted sample_i/data => tew
            self.wrk[st][seed]=folder,tew,wf
        data= np.array(acc)
        JA = calc_pmf(data,st,self.w_c)               # get JA
        wf_sd=dict([(self.wrk[st][s][2],s) for s in seeds])
        sel_seed=wf_sd.get(JA, wf_sd[min(wf_sd.keys(), key=lambda k: abs(k-JA))])
        work_ss=self.wrk[st][sel_seed][2]
        self.d_cp[st][sel_seed]=self.wrk[st][sel_seed][0]
        print wf_sd
        print 'JA:',JA
        print 'selected seed',sel_seed
        print 'work for selected seed:',work_ss
        self.w_c[int(st)]=work_ss
        return seeds

def cp_file(f_dir,f,d_dir,d):
    shutil.copy(os.path.join(f_dir,f),os.path.join(d_dir,d))

w_c={}
w_c[0]=0
d_cp={}

def main_call(st,w_c,d_cp):
    wrk_pkl={}
    c1 = asmd_calcs(wrk_pkl,w_c,d_cp)
    seed_l = c1.create_pkl(st)
    print w_c
    nextnum=str(int(st)+1).zfill(2)
    seed_folder = d_cp[st]
    '''
    if st == num:
        for s,f in seed_folder.items():
            if not os.path.exists(os.path.join(my_dir,nextnum)):
                os.makedirs(os.path.join(my_dir,nextnum))
            cp_file(os.path.join(my_dir,st,f),'daOut.coor.%s' % s, \
                    os.path.join(my_dir,nextnum),'00.coor')
            cp_file(os.path.join(my_dir,st,f),'daOut.vel.%s' % s, \
                    os.path.join(my_dir,nextnum),'00.vel')
    '''

# main call
dirs = []
for i in range(1,int(num)+1):
    dirs.append(str(i).zfill(2))
[main_call(st,w_c,d_cp) for st in sorted(dirs)]

# matplotlib end
plt.legend(title='Stage | Steps | Traj\'s',loc='upper left', \
       shadow=True, fancybox=True) #,bbox_to_anchor=(1.4,1))
plt.xlabel('Extension (A)')
plt.ylabel('Work (kcal/mol)')
plt.title('xxmoleculexx - xxngnxx - ASMD \n xxenvironxx xxvelxx A/ns')
plt.xlim([spos,spos+dist])
#plt.setp(plt.gca(),'yticklabels',[])
#plt.setp(plt.gca(),'xticklabels',[])
# LEGEND - details
leg = plt.gca().get_legend()
ltext = leg.get_texts()
llines= leg.get_lines()
frame = leg.get_frame()
frame.set_facecolor('0.90')
plt.setp(ltext, fontsize='small')
plt.setp(llines, linewidth=1)
plt.draw()

def tex_pic(n):
    texdir = os.path.join(('/'.join(my_dir.split('/')[0:-2])), \
                       'tex_%s/fig_pmf' % my_dir.split('/')[-3])
    if not os.path.exists(texdir): os.makedirs(texdir)
    plt.savefig('%s/xxplotnamexx2s%s.png' % (texdir,n))
    plt.savefig('%s/xxplotnamexx2s%s.eps' % (texdir,n))
def continue_pic(n):
    plotname = '%s-eval' % num
    plt.savefig('%s.png' % plotname)
    plt.savefig('%s.eps' % plotname)

tex_pic(num)
#continue_pic(num)
