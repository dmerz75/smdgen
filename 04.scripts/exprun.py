#!/usr/bin/env python
import sys, os, glob
import os.path
from glob import glob
import fnmatch
import itertools

my_dir = os.path.abspath(os.path.dirname(__file__))
#prj_dir= ('/').join(my_dir.split('/')[:-1])
acc=[]

def run_script(vel,solv,script):
    for root, dirnames, filenames in os.walk(my_dir):
    #for root, dirnames, filenames in os.walk(prj_dir):
        for filename in fnmatch.filter(filenames,'%s-%s' % (vel,script)):
            sol=(root.split('/')[-2]).split('.')[1]
            if sol==solv:
                jobs=os.path.join(root,filename)
                print jobs
                os.chdir(root)
                os.system('python ' + '%s' % jobs)

vels = ['02','03']
solvs= ['vac','imp','exp']
analy_scripts = ['npy.py','allhb.py','allwp.py','ihbond.py','expavg.py']
[run_script(v,s,sc) for v in vels for s in solvs for sc in analy_scripts]
