#!/bin/bash
# rsync ggate

SOURCEDIR=/home/dale/Documents/valiant/xproject/smdgen/namd_da_asmd_zc1_zatt1g100/
DESTDIR=dmerz3@ggate.chemistry.gatech.edu:/nethome/dmerz3/Documents/valiant/ggate/01.da/

#rsync -avh $SOURCEDIR $DESTDIR
scp -r $SOURCEDIR $DESTDIR
