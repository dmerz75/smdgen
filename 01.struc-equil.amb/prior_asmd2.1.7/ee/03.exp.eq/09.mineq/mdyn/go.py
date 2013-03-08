#!/usr/bin/env python
import sys, os

os.system('${AMBERHOME}/bin/sander -O -i mdyn.in -o mdout.out -c ../min/ee.rst -p ../../eewb.prmtop -r eedyn.rst -x ee.mdcrd') 
