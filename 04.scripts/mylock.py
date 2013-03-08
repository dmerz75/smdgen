#!/usr/bin env python
from lockfile import FileLock
import sys

lock = FileLock(__file__)
if lock.is_locked()==True: sys.exit()
lock.acquire()

for i in range(10000):
    print i**2
