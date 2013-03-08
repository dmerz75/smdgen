#!/usr/bin/env python
import sys, os

#JOBID = os.environ['PBS_JOBID']
#JOBID1 = JOBID.split('.')[0]

os.system('${AMBERHOME}/bin/antechamber -i semi.pdb -fi pdb -o ll.mol2 \
          -fo mol2 -c bcc -nc +1 -s 2 -ek scfconv=1.d-8')
