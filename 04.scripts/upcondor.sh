#!/bin/bash
# rsync ggate

SOURCEDIR=/home/dale/Documents/valiant/workgen/namdgen/condor.da.c130/
DESTDIR=dmerz3@tg-condor.purdue.teragrid.org:/scratch/scratch96/d/dmerz3/valiant/condor/01.da/condor.da.c130/

rsync -avh $SOURCEDIR $DESTDIR
#scp -r $SOURCEDIR $DESTDIR
