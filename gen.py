#!/usr/bin/env python
import sys,os,itertools,shutil,re,pickle,time
from smdwork import *
import numpy as np

jobid='test'

#_____MOLECULE___configurations________________________________________________
ngn    =['namd']                           # 'namd','amb,'gro'
mlist  =['da','rda','ee','le','el','oo']   # da,rda
molec  =[mlist[0]]                         # can use [0],[1] ... [n]
zcrd   = 13                                # z constraint:  13,33,4, start pos.
envdist={'01.vac':zcrd,'02.imp':zcrd,'03.exp':zcrd} # i.e. '01.vac':zc7...
dist   = 20.0                              # declare a float dist: 6.0, 28.0
ts     = 2.0                               # 0.5, 1.0, 2.0
n      =[2.]                               # [1.,2.] | [4.,5.]
xcopy  ={'1':2,'2':2,'3':3,'4':5,'5':5}    # duplication for smd() only
environ=['01.vac','02.imp','03.exp']       # ['01.vac'] | ['01.vac','03.exp']
langevD='5'                                # langevin Damping: 0.2, 1, 5
sf     = 1                     # untrusted # scale factor: -1, 1, or 5 if el
direct = 1                     # untrusted # direction
setup  ={1:{'howmany':100,'freq':50},
         2:{'howmany':32,'freq':50},    # 45*18t = 810, 29*28t = 812,
         3:{'howmany':32,'freq':50},    # 20*40t = 800, 25*32t = 800
         4:{'howmany':2,'freq':50},
         5:{'howmany':1,'freq':50}}
#_____GATE_______configurations________________________________________________
gate ='steele2'     # namd                 # ggategpu,ggatecpu,fgatecpu,steele
                                           # steele2,fgatecpu2,ggatecpu2/gpu2
gate='fgatecpu2'   # amb                  # multisndr,fgatecpu
cn   ='2'                                  # ppn request
ppn_env={'01.vac':'2','02.imp':cn,'03.exp':cn}
comp ='cpu'                                # gpu or cpu !TESLA: always 1
wallt='lwt'                    # smd       # sst=15m,swt=72h,mwt=368h,lwt=720h
                               # asmd      # swt=1.5h,mwt:4h,lwt:72h,dwt:15d
wt_env={'01.vac':wallt,'02.imp':wallt,'03.exp':'dwt'}
queue='workq'                            # tg_'short'72 'workq'720
q_env={'01.vac':'standby','02.imp':queue,'03.exp':queue}
                                           # 'standby-8','standby','debug'
#_____ASMD_____________________________________________________________________
howmany='25'              # total trajectories = howmany*setup[n]['howmany']
path_seg  = np.array([0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])  # <--Sum to 1
path_svel = np.array([1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])# <--STAGES
#_________pickle_______________________________________________________________
def super_pickle(nset):
    config = mdict()
    def construct(n):
        vel = 1/(100*10**n)
        path_vel = (np.linspace(vel,vel,len(path_seg)))*ts*path_svel
        return path_vel
    path_vel  = construct(float(nset))
    path_steps=np.rint(path_seg*dist/path_vel)
    config[float(nset)]=dist,ts,path_seg,path_svel,path_vel, \
            path_steps,setup[nset]
    return config

class mdict(dict):
    def __setitem__(self,key,value):
        self.setdefault(key,[]).append(value)
def  print_dict(dt):
    for key,value in dt.items():
        print key,value
        print ''

#_____CODE_____________________________________________________________________
def smd():
    def call_Smd(ng,mol,env,v,zc,workdir,jobdir):
        print 'SMD is ready with',ng,'for',mol,'in',env,'at velocity',v, \
              'assembled inside',jobdir+'.'
        f = Smd_Method(ng,mol,env,v,ts,zc,langevD,sf,workdir,jobdir, \
          gate,ppn_env[env],comp,wt_env[env],q_env[env],direct)
        f.makeEnvDir()
        subdir = f.makeSubDir()
        f.reg_exp(subdir)
        f.makeSubDirCopies(xcopy[str(int(v))])
        subdir = f.makeEvalDir()
        f.reg_exp(subdir)
    def call_steer_cntrl(ng,mol,env,v,zc,workdir,jobdir):
        f = Smd_Steering(ng,mol,env,v,ts,zc,langevD,sf,workdir,jobdir, \
               gate,ppn_env[env],comp,wt_env[env],q_env[env],direct)
        subdir = f.place_steering_control()
        f.reg_exp(subdir)
    def call_Struc(ng,mol,env,workdir,jobdir):
        s = Struc_Dirs(ng,mol,env,workdir,jobdir)
        s.makeStrucDir()
    def work_dir():
        w = make_JobDirSmd(ngn[0],molec[0],zcrd,workdir,jobdir)
        subdir = w.makeJobDir()
        w.reg_exp(subdir)
    # sub call starts here !!
    workdir=os.path.abspath(os.path.dirname(__file__))
    jobdir =ngn[0]+'_'+molec[0]+'_'+'smd2'+'_'+jobid
    work_dir()
    [call_Struc(ng,mol,env,workdir,jobdir) for ng in ngn for mol in molec \
         for env in environ]
    [call_Smd(ng,mol,env,v,envdist[env],workdir,jobdir) for ng in ngn \
         for mol in molec for env in environ for v in n]
    [call_steer_cntrl(ng,mol,env,v,envdist[env],workdir,jobdir) \
           for ng in ngn for mol in molec for env in environ for v in n]

#___main_calls___
smd()
