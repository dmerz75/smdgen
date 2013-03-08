#!/bin/bash
# rsync ggate

SOURCEDIR=/home/dale/Documents/valiant/workgen/namdgen/chi4/
DESTDIR=cukachukwu3@ggate.chemistry.gatech.edu:/nethome/cukachukwu3/

#rsync -avh $SOURCEDIR $DESTDIR
scp -r $SOURCEDIR $DESTDIR
