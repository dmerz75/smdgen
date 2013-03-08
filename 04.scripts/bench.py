#!/usr/bin/env python
import os, sys
import numpy as np
import math
import pylab as p
import pickle

my_dir = os.path.abspath(os.path.dirname(__file__))
if len(sys.argv) >= 2:                               # load pickle if available
    confd=pickle.load(open(sys.argv[1],'rb'))
elif len(sys.argv) <2:
    confd=pickle.load(open('time345.pkl','rb'))
listl=['vac03','imp03','exp03','vac04','imp04','exp04','vac05','imp05','exp05']
bars=np.arange(3,6,1)
widthb=0.06
ticks=np.arange(3,6,1)
ticky=np.arange(0,7,1)
xmin=ticks[0]-0.19
xmax=ticks[2]+0.19
ymin=ticky[0]
ymax=ticky[-1]

config={0:{'tk':0,'cr':'red','dot':'ro','xd':-0.06,'xb':-0.09},
        1:{'tk':0,'cr':'green','dot':'go','xd':0,'xb':-0.03},
        2:{'tk':0,'cr':'blue','dot':'bo','xd':0.06,'xb':0.03},
        3:{'tk':1,'cr':'red','dot':'ro','xd':-0.06,'xb':-0.09},
        4:{'tk':1,'cr':'green','dot':'go','xd':0,'xb':-0.03},
        5:{'tk':1,'cr':'blue','dot':'bo','xd':0.06,'xb':0.03},
        6:{'tk':2,'cr':'red','dot':'ro','xd':-0.06,'xb':-0.09},
        7:{'tk':2,'cr':'green','dot':'go','xd':0,'xb':-0.03},
        8:{'tk':2,'cr':'blue','dot':'bo','xd':0.06,'xb':0.03}}

def lg_func(l):
    ls=listl[l]
    print ls
    y=[math.log10(float(u)) for u in confd[ls]]
    d=config[l]['tk']+3
    x=np.linspace(d-.03,d+.03,len(y))
    return x,y

fig=p.figure()
p.subplot(1,1,1)

for l in range(0,9):
    ls=listl[l]
    x,y=lg_func(l)
    ym=np.mean(y)
    p.plot(x+config[l]['xd'],y,config[l]['dot'])
    #p.plot(x+config[l]['xd'],y,config[l]['dot'], label='%s=%d' %(ls,ym))
    p.bar(bars[config[l]['tk']]+config[l]['xb'],ym,widthb,color=config[l]['cr'])

p.xlim(xmin,xmax)
p.ylim(ymin,ymax)
p.xticks(ticks)
p.yticks(ticky)
p.xlabel('Velocities')
p.ylabel('Log(Time)')
p.title('Benchmark')

#p.legend()

p.draw()
#p.show()
fig.savefig('bench.png')
fig.savefig('bench.eps')
