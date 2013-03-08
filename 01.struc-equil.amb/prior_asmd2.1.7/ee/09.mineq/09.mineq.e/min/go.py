#!/usr/bin/env python
import sys, os

os.system('${AMBERHOME}/bin/sander -O -i mdin.in -o mdout.out -c ../../dawb.inpcrd -p ../../dawb.prmtop -r da.rst') 
