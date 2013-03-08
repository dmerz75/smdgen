#!/bin/bash
# rsync ggate

SOURCEDIR=/home/dale/Documents/valiant/workgen/namdgen/source100.da.c130/

#/home/dale/Documents/valiant/steele/01.da/100ss/100sa.da.c130/01.vac

DESTDIR=/home/dale/Documents/valiant/ggate/01.da/100ggr/100gb.da.c130/

#scp -r $SOURCEDIR $DESTDIR
rsync -avh --include='*/' --include='*-expavg.py' --exclude='*' $SOURCEDIR $DESTDIR
