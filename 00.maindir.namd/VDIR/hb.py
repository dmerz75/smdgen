#!/usr/bin/env python
import MDAnalysis
import MDAnalysis.analysis.hbonds
import MDAnalysis.analysis.distances
from sys import argv
import numpy as np
import pickle
import os,sys

#______________universe________________________________________________________
u = MDAnalysis.Universe('../../xxenvironxx/00.psf','da_smd.dcd', \
                        permissive=True)

def analyze_bond(univ,seg1,seg2):
    try:
        name1=seg1.replace(' ','')
        name2=seg2.replace(' ','')
        h = MDAnalysis.analysis.hbonds.HydrogenBondAnalysis(univ,seg1,seg2, \
                                                 distance=4.0, angle=140.0)
        results = h.run()
        pickle.dump(h.timeseries,open('%s-hb_%s_%s.pkl.%s' % (sys.argv[1], \
                                              name1,name2,sys.argv[2]),'w'))
    except:
        pass

#__analyze__bonds______________________________________________________________
analyze_bond(u,'protein','protein')
analyze_bond(u,'protein','segid WT1')

'''
f = open('%s-hlist.dat.%s' % (stri,jbid),'w')
f = open('%s-hlist.dat.%s' % (sys.argv[1],sys.argv[2],'w')

for n in range(0,len(h.timeseries)):
    for bond in h.timeseries[n]:
        for val in bond:
            try:
                f.write(val+'   \t')
            except:
                f.write(str(val)+'   \t')
        f.write('\n')
    f.write('# '+str(n)+' ')
    f.write(str(len(h.timeseries[n])))
    f.write('\n')
    f.write('\n')
f.close()
#______________rgyr__________________________________________________________
acc=[]
listl=[]
rg=[]

def cyc(ca1,ca2):
    for ts in u.trajectory:
        r1 = ca2.coordinates() - ca1.coordinates()
        d1 = np.linalg.norm(r1)
        acc.append(d1)

def calcd(i,ca):
    ca1 = u.selectAtoms("resid %d and name CA" % i)
    ca2 = u.selectAtoms("resid %d and name CA" % ca)
    cyc(ca1,ca2)

for i in range(1,5):
    ca = 11-i
    calcd(i,ca)
    listl.append(acc)
    acc=[]

def rgyr(bb):
    for ts in u.trajectory:
        rgyr = bb.radiusOfGyration()
        rg.append(rgyr)

bb = u.selectAtoms('protein and backbone')   # a selection (a AtomGroup)
rgyr(bb)
listl.append(rg)

dd = np.array(listl)
dd = np.transpose(dd)
np.savetxt('%s-rgyr.dat.%s' % (stri,jbid),dd,fmt='%.14f')
np.save('%s-rgyr.%s' % (stri,jbid),dd)
'''
