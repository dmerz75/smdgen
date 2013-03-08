#!/usr/bin/env python
import sys, os

os.system('${AMBERHOME}/bin/sander -O -i mdin.in -o mdout.out -c ../../ee.inpcrd -p ../../ee.prmtop -r ee.rst') 
