#!/usr/bin/env python
import MDAnalysis
import MDAnalysis.analysis.hbonds
import matplotlib.pyplot as plt
from sys import argv
from glob import glob
import numpy as np
import pickle
import sys,os,re

my_dir = os.path.abspath(os.path.dirname(__file__))
my_dir='/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[0:-1])

acc=[]
for path in glob(os.path.join(my_dir,'xxnumxx.*/*-hb_protein_pr*.pkl.*')):
    print path
    sample_i = pickle.load(open(path,'rb'))
    acc.append(sample_i)
    if len(acc)==250:
        break

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


b_data = np.array([[charac_bond2(traj_i, n) for traj_i in acc]
     for n in [3,4,5]])

trj  = str(len(acc))
trjl = len(acc[0])

frames = np.linspace(xxstartconstraintxx,xxendconstraintxx,len(acc[0]))
# matplotlib
plt.plot(frames,b_data.mean(axis=1)[0],'r-',label="i->i+3",linewidth=1.5)
plt.plot(frames,b_data.mean(axis=1)[1],'k-',label="i->i+4",linewidth=1.5)
plt.plot(frames,b_data.mean(axis=1)[2],'g-',label="i->i+5",linewidth=1.5)
plt.xlabel('end-to-end distance (A)')
plt.ylabel('average H-bond count')
plt.title('xxmoleculexx | NAMD | Charmm22 \n xxenvironxx %strj' % trj)
plt.legend()
plt.gca().set_ylim(ymin=-0.2)
#plt.axis([9.9,35.1,-.1,6.4])

plt.draw()
texdir = os.path.join(('/'.join(my_dir.split('/')[0:-1])), \
                       'tex_%s/fig_bond' % my_dir.split('/')[-2])
if not os.path.exists(texdir): os.makedirs(texdir)

#plt.savefig('xxplotnamexx_ihb.eps')
#plt.savefig('xxplotnamexx_ihb.png')
plt.savefig('%s/xxplotnamexx_ihb.eps' % texdir)
plt.savefig('%s/xxplotnamexx_ihb.png' % texdir)
