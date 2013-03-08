#!/usr/bin/env python
import os.path
from glob import glob
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import LSQUnivariateSpline

my_dir=os.path.abspath(os.path.dirname(__file__))
my_dir='/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[0:-1])
acc=[]

for path in glob(os.path.join(my_dir,'xxnumxx.data/*.npy')):
    print path
    sample_i = np.load(path)
    print sample_i.shape
    acc.append(sample_i)
data=np.concatenate(acc,axis=0)

# variables, simulation parameters;  10,000 steps
v    = xxvelapsxx              ;#  20 A in 20 ps, 1.0000 A/ps
dt   = xxdtxx                ;#  2 fs * 50(smd.tcl) / 1000, 0.1 ps
beta = -0.6              ;#  8.31 J/K*mol, 4.184 J/cal -> .6 kcal/mol

# columns of data 3D array
f    = data[::,::,2]
ext  = data[::,::,1]
fvdt = f*v*dt
work = np.cumsum(fvdt,axis=1)
betawork = beta*work
ebw  = np.exp(betawork)
meanebw  = ebw.mean(axis=0)
lnmeanebw= np.log(meanebw)
deltaf= (1/beta)*lnmeanebw

#plot parameters
xmin=xxstartconstraintxx
xmax=xxendconstraintxx
domain=np.linspace(xmin,xmax,len(deltaf))

# plot_indices, random number between 1 and number of 'force columns'
rnd = np.random.RandomState(0x1913)
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
'''
   t = np.linspace(e_i[0],e_i[-1],15)
   t = t[1:-1:]
   spline = LSQUnivariateSpline(e_i,w_i,t)
   t_plot = np.linspace(e_i[0],e_i[-1],100)
   plt.plot(t_plot,spline(t_plot),'k',linewidth=.5)
ec = ext[1,::]
t = np.linspace(ec[0],ec[-1],15)
t = t[1:-1:]
spline = LSQUnivariateSpline(ec,deltaf,t)
t_plot = np.linspace(ec[0],ec[-1],100)
plt.plot(t_plot,spline(t_plot),'r',linewidth=7)
plt.plot(t_plot,spline(t_plot),'k--',linewidth=1.5)
'''
plt.plot(domain[::xxpfxx], deltaf[::xxpfxx],'r-',linewidth=5)
plt.plot(domain[::xxpfxx], deltaf[::xxpfxx],'k--',linewidth=0.6)

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

plt.xlabel('Extension (A)')
plt.ylabel('Work (kcal/mol)')
plt.title('xxmoleculexx | SMD | AMB | FF99SB \n xxenvironxx ' \
          +str(data.shape[0])+'trj xxvelansxx A/ns')

#plt.ylim([ymin,ymax])
plt.xlim([xmin-.1,xmax+.1])

plt.draw()
texdir = os.path.join(('/'.join(my_dir.split('/')[0:-1])), \
                      'tex_%s/fig_pmf' % my_dir.split('/')[-2])
if not os.path.exists(texdir): os.makedirs(texdir)

#plt.savefig('xxplotnamexxea.png')
#plt.savefig('xxplotnamexxea.eps')
plt.savefig('%s/xxplotnamexxea.png' % texdir)
plt.savefig('%s/xxplotnamexxea.eps' % texdir)
