#!/usr/bin/python

import os
from ctypes import *
class Hunspell(Object):
    def __init__(self):
        libtest = cdll.LoadLibrary('/usr/lib/libhunspell.so')
