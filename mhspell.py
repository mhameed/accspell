#!/usr/bin/python

import os
import readline
import string
import sys

from hunspell import *

linesList = []

def readFile(fname):
    global linesList 
    fh = open(fname, "r")
    linesList = fh.readlines()
    fh.close()

    # separate out words:
    for i in range(0, len(linesList)):
        linesList[i] = linesList[i].rstrip('\n')
        linesList[i] = linesList[i].split(' ')


def writeFile(fname):
    fh = open(fname, 'w')
    for line in linesList:
        fh.write(" ".join(line) + "\n")
    fh.close()

def context(lineno):
    print " ".join(linesList[lineno])

def getInput(word, suggList, lineno):
    while True:
        val = raw_input("%s, corrections: [%s]: (q,0, ..)? " % (word, ", ".join(suggList) ) )
        if val == 'c':
            context(lineno)
            continue
        elif val == 'q':
            return -1
        if not val.isdigit():
            val = -1
        else:
            val = int(val)

        if val == 0:
            return 0
        elif 0 < val and val <= len(suggList):
            return val 
        else:
            print "got something strange, please try again."



def spellcheck(a):
   mh = Hunspell()
   if not isinstance(a, list):
        print "hey!, i wanted a list, i got something else, cant continue."
        return
   for line in range(0,len(a)):
        if a[line] == []: continue
        for i in range(0,len(a[line])):
            origword = a[line][i]
            word = origword.rstrip(string.punctuation) \
              .lstrip(string.punctuation)
            if word == '': continue
            res = mh.check(word)
            if res == []: continue
            val = getInput(word, res, line)
            if val == -1: writeFile('out.txt')
            elif val == 0: continue
            # we had a valid number, so do the swap.
            a[line][i] = origword.replace(word, res[val-1])

readFile('wrong.txt')
spellcheck(linesList)
writeFile('out.txt')
