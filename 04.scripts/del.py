#!/usr/bin/env python
import sys, os, glob

low = int(sys.argv[1])
high= int(sys.argv[2])

os.system('qstat -u dmerz3 > tmpjobs.txt')
f = open('tmpjobs.txt','r')
for line in f.readlines()[5:]:
    print line.split('.')[0]
    val=int(line.split('.')[0])
    if (val>=low) and (val<=high):
        print 'match'
        os.system('qdel %d' % val)
f.close()
