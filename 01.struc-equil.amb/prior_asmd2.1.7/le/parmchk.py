#!/usr/bin/env python
import sys, os

# JOBID = os.environ['PBS_JOBID']
# JOBID1 = JOBID.split('.')[0]

os.system('${AMBERHOME}/bin/parmchk -i ll.mol2 -f mol2 -o le.frcmod')
