#!/bin/bash
# rsync ggate

SOURCEDIR=/home/dale/Documents/valiant/workgen/namdgen/source100.da.c130/
DESTDIR=/mnt/hgfs/debian2shared/namd/

#scp -r $SOURCEDIR $DESTDIR
rsync -avh --include='*/' --include='*-npy.py' --include='*-expavg.py' --include='*-dualplot.py' --exclude='*' $SOURCEDIR $DESTDIR
