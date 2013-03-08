#!/usr/bin/env python
import sys,os,pickle,fnmatch,itertools
import os.path
from glob import glob
import numpy as np
from random import *
import datetime,time

import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import LSQUnivariateSpline

my_dir = os.path.abspath(os.path.dirname(__file__))
now=datetime.datetime.now()
now=now.strftime("%Y%m%dt%H%M")

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
dct        = config[vel][0][6] # 'freq' 50*ts/1000
dt         = dct['freq']*ts/1000
path_v_aps = path_vel/ts*1000

spos=xxsposxx
beta=-0.6

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
            awp.append(work_used[i])
        dawp=np.array(awp)
        wp=np.cumsum(dawp)[-1]
        corr_work[stage]=wp

def write_data(data,info,stage):
    data[::,::,3] = np.exp(np.cumsum(data[::,::,3]*v*dt,axis=1)*beta)
    deltaf = np.log(data[::,::,3].mean(axis=0))*(1/beta)
    JA=deltaf[-1]
    pmf_ideal[stage]=deltaf[-1]
    wfsd={}
    seed=select_traj(info,wfsd,JA)
    sdwf = dict((v,k) for k,v in wfsd.iteritems())
    work_used[stage]=sdwf[seed]
    print 'Jarzynski\'s average:',JA,'compared to work:',sdwf[seed]
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

# get DIRECTORIES
dirs = []
[dirs.append(d) for d in os.listdir(my_dir) if \
    os.path.isdir(os.path.join(my_dir,d))]
# dirs = ['01','02','03']
[pack(st) for st in sorted(dirs)]

'''
print 'ideally, the jarzynski averaging result was'
print pmf_ideal
print 'however, work from coordinates/vels available'
print work_used
print 'corrected work, for prepending...(4..3..2..)'
print corr_work
time.sleep(4)
'''

def plot_multi_traj(data,domain,stage,phase):
    rnd = np.random.RandomState(0x1913)
    indices = np.arange(data.shape[0])
    rnd.shuffle(indices)
    plot_indices = indices[1:125:1]    # howmany actually appear on plot
    for index in plot_indices:
        w_i = data[index,::,3]
        plt.plot(domain[::1],w_i[::1],'#660033',linewidth=0.4)
    print 'trajectories in domain %d to %d' % (domain[0],domain[-1])

def plot_pmf(deltaf,domain,stage,phase,size):
    lb = stage+' '+str(int(path_steps[0][phase]))+' '+str(size)
    plt.plot(domain[::1], deltaf[::1],'b-',linewidth=3)
    plt.plot(domain[::1], deltaf[::1],'k--',linewidth=0.6,label=lb)

def pack2(stage):
    acd=[]
    for path in glob(os.path.join(my_dir,'%s/*/*-tef.dat.*' % stage)):
        sample_i = np.loadtxt(path)
        acd.append(sample_i)
    data = np.array(acd)
    phase = int(stage)-1
    zdist = (path_vel*path_steps).cumsum()
    if phase==0:
        xmin=spos
        xmax=spos+zdist[phase]
    else:
        xmin=spos+zdist[phase-1]
        xmax=spos+zdist[phase]
    data[::,::,3] = np.cumsum(data[::,::,3]*path_v_aps[phase]*dt,axis=1)
    df = np.exp(data[::,::,3]*beta)
    deltaf = np.log(df.mean(axis=0))*(1/beta)+corr_work[stage]
    domain=np.linspace(xmin,xmax,data.shape[1])
    data[::,::,3] = data[::,::,3]+corr_work[stage]
    plot_multi_traj(data,domain,stage,phase)
    plot_pmf(deltaf,domain,stage,phase,data.shape[0])

# PLOT - pmf
fig=plt.figure()
plt.clf()

[pack2(st) for st in sorted(dirs)]

# PLOT labels
plt.legend(title='Stage | Steps | Traj\'s',loc='upper left', \
       shadow=True, fancybox=True) #,bbox_to_anchor=(1.4,1))
plt.xlabel('Extension (A)')
plt.ylabel('Work (kcal/mol)')
plt.title('da - namd - asmd \n vac 100.0 A/ns')
plt.xlim([spos,spos+dist])
#plt.ylim([ymin,ymax])
#plt.ylim([-6,48])
#plt.setp(plt.gca(),'yticklabels',[])
#plt.setp(plt.gca(),'xticklabels',[])
# LEGEND - details
leg = plt.gca().get_legend()
ltext = leg.get_texts()
llines= leg.get_lines()
frame = leg.get_frame()
frame.set_facecolor('0.80')
plt.setp(ltext, fontsize='small')
plt.setp(llines, linewidth=1)
# end plot modifications
plt.draw()

texdir = os.path.join(('/'.join(my_dir.split('/')[0:-2])), \
                       'tex_%s/fig_pmf' % my_dir.split('/')[-3])
if not os.path.exists(texdir): os.makedirs(texdir)

plt.savefig('%s/xxplotnamexx2.png' % texdir)
plt.savefig('%s/xxplotnamexx2.eps' % texdir)
