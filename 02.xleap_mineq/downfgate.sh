#!/bin/bash
# rsync steele

S=dmerz3@fgate-fs.chemistry.gatech.edu:/nethome/dmerz3/Documents/valiant/fgate/01.da/amberprep_mar_13_final10
D=/home/dale/Documents/md/analyze

rsync -avh $S $D
#scp -r $SOURCEDIR $DESTDIR
