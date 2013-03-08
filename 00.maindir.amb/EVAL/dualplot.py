#!/usr/bin/env python
import os.path
from glob import glob
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import LSQUnivariateSpline
import math

acc    = []
accd   = []
my_dir=os.path.abspath(os.path.dirname(__file__))
my_dir='/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[0:-1])

for path in glob(os.path.join(my_dir,'adaptive*-xxnumxx.out')):
    if len(accd) == 1:
	break
    print path
    sample_i = np.loadtxt(path)
    accd.append(sample_i)
adata = np.array(accd)

for path in glob(os.path.join(my_dir,'xxnumxx.data/*.npy')):
    print path
    sample_i = np.load(path)
    print sample_i.shape
    acc.append(sample_i)
data=np.concatenate(acc,axis=0)

# variables, simulation parameters;  10,000 steps
v        = xxvelapsxx           ;#  20 A in 20 ps, 1.0000 A/ps
dt       = xxdtxx        ;#  2 fs * 50(smd.tcl) / 1000, 0.1 ps
beta     = -0.6     ;#  8.31 J/K*mol, 4.184 J/cal -> .6 kcal/mol
# columns of data 3D array
time     = adata[::,::,0].flatten()
zcoord   = adata[::,::,1].flatten()
endend   = adata[::,::,2].flatten()
netforce = adata[::,::,3].flatten()
dwork    = netforce*v*dt
expavg   = adata[::,::,4].flatten()
seccum   = adata[::,::,5].flatten()
# columns of data 3D array
f        = data[::,::,2]
ext      = data[::,::,1]
fvdt     = f*v*dt
work     = np.cumsum(fvdt,axis=1)
betawork = beta*work
ebw      = np.exp(betawork)
meanebw  = ebw.mean(axis=0)
lnmeanebw= np.log(meanebw)
deltaf   = (1/beta)*lnmeanebw
#plot parameters
adx  = np.linspace(xxstartconstraintxx,xxendconstraintxx,sample_i.shape[1])
xmin = xxstartconstraintxx
xmax = xxendconstraintxx
smx  = np.linspace(xmin,xmax,len(deltaf))

# plot_indices, random number between 1 and number of 'force columns'
rnd = np.random.RandomState(0x2028)
indices = np.arange(data.shape[0])
rnd.shuffle(indices)
plot_indices = indices[1:99:1]

# PLOT - pmf
fig=plt.figure()
plt.clf()

for index in plot_indices:
   e_i = data[index,::,1]
   w_i = work[index,::]
   plt.plot(domain[::xxpfxx],w_i[::xxpfxx],'k-',linewidth=0.4)

plt.plot(smx[::xxpfxx], deltaf[::xxpfxx],'r-',linewidth=4,label='SMD')
plt.plot(smx[::xxpfxx], deltaf[::xxpfxx],'k--',linewidth=0.8)

plt.plot(adx, seccum,'b-',linewidth=4,label='ASMD')
plt.plot(adx, seccum,'k--',linewidth=.8)
'''
# y
miny=min(deltaf)
maxy=deltaf[0.7*len(deltaf)]
# x
minx=domain[np.argmin(deltaf)]
maxx=domain[0.7*len(deltaf)]
plt.annotate('(%3.2f,%3.2f)' % (minx,miny),xy=(minx,miny),\
             xytext=(0,60),textcoords='offset points',ha='center',va='bottom',\
             bbox=dict(boxstyle='round,pad=0.4', fc='cyan',alpha=0.5),\
             arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0'))
plt.annotate('(%3.2f,%3.2f)' % (maxx,maxy),xy=(maxx,maxy),\
             xytext=(0,-60),textcoords='offset points',ha='center',va='bottom',\
             bbox=dict(boxstyle='round,pad=0.4', fc='cyan',alpha=0.5),\
             arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0'))
'''
plt.xlim([xmin-.1,xmax+.1])
plt.legend(loc=2,borderaxespad=2)
plt.xlabel('Extension (A)')
plt.ylabel('Work (kcal/mol)')
plt.title('xxmoleculexx SMD | AMB | Charmm22 \n
          xxenvironxx'+str(data.shape[1])+'trj xxvelansxx A/ns')
plt.draw()
#plt.show()
texdir = os.path.join(('/'.join(my_dir.split('/')[0:-1])), \
                       'tex_%s/fig_pmf' % my_dir.split('/')[-2])
if not os.path.exists(texdir): os.makedirs(texdir)

#plt.savefig('xxplotnamexxd2.png')
#plt.savefig('xxplotnamexxd2.eps')
plt.savefig('%s/xxplotnamexxd2.png' % texdir)
plt.savefig('%s/xxplotnamexxd2.eps' % texdir)
