#!/bin/bash
# rsync steele

SOURCEDIR=/home/dale/Documents/valiant/xproject/smdgen/namd_da_asmd_zc1_cub/
DESTDIR=dmerz3@tg-steele.purdue.teragrid.org:/scratch/scratch96/d/dmerz3/valiant/steele/01.da/

#rsync -avh $SOURCEDIR $DESTDIR
scp -r $SOURCEDIR $DESTDIR
