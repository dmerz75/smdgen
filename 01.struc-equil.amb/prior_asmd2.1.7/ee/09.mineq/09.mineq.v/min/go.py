#!/usr/bin/env python
import sys, os

os.system('${AMBERHOME}/bin/sander -O -i mdin.in -o mdout.out -c ../../da.inpcrd -p ../../da.prmtop -r da.rst') 
