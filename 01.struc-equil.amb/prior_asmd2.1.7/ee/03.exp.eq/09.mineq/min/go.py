#!/usr/bin/env python
import sys, os

os.system('${AMBERHOME}/bin/sander -O -i mdin.in -o mdout.out -c ../../eewb.inpcrd -p ../../eewb.prmtop -r ee.rst') 
