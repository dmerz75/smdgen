#!/usr/bin/env python
import sys, os

os.system('${AMBERHOME}/bin/sander -O -i mdyn.in -o mdout.out -c ../min/da.rst -p ../../da.prmtop -r dadyn.rst -x da.mdcrd') 
