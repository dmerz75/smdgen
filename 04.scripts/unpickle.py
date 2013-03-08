#!/usr/bin/env python
import sys, os, glob
import pickle
my_dir = os.path.abspath(os.path.dirname(__file__))

data = pickle.load(open(sys.argv[1],'rb'))

print data
