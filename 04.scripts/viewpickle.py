#!/usr/bin/env python
import sys,os,pickle

my_dir = os.path.abspath(os.path.dirname(__file__))

class mdict(dict):
    def __setitem__(self,key,value):
        self.setdefault(key,[]).append(value)

def print_dict(dct):
    for key,val in dct.items():
        print key,val
        print ''

config = pickle.load(open('config.pkl','rb'))

print_dict(config)
