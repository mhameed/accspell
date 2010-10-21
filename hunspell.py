#!/usr/bin/python

import os
from ctypes import *
hunspell = cdll['libhunspell.so']

hunspell.Hunspell_create.restype = POINTER(c_int)
hunspell.Hunspell_create.argtypes = (c_char_p, c_char_p)

hunspell.Hunspell_destroy.argtype = POINTER(c_int)

hunspell.Hunspell_spell.argtypes = (POINTER(c_int), c_char_p)

hunspell.Hunspell_suggest.argtypes = (POINTER(c_int), POINTER(POINTER(c_char_p)), c_char_p)
hunspell.Hunspell_free_list.argtypes = (POINTER(c_int), POINTER(POINTER(c_char_p)), c_int)


class Hunspell(object):

    def __init__(self):
         afpath = '/usr/share/hunspell/en_GB.aff'
         dpath = '/usr/share/hunspell/en_GB.dic'
         self.hunhandle = hunspell.Hunspell_create(afpath, dpath)
         a = c_char_p()
         p = pointer(a)
         self.pp = pointer(p)
         self.retval = 0
         self.suggestions = []

    def checkWord(self, word):
         return hunspell.Hunspell_spell(self.hunhandle, word)

    def suggest(self,word):
        self.retval = hunspell.Hunspell_suggest(self.hunhandle, self.pp, word)
        p = self.pp.contents
        self.suggestions = []
        for i in range(0, self.retval):
             self.suggestions.append( c_char_p(p[i]).value )
        self.freeSuggestions()
        return self.retval

    def freeSuggestions(self):
         hunspell.Hunspell_free_list(self.hunhandle, self.pp, self.retval)

    def __del__(self):
         #hunspell.Hunspell_destroy(self.hunhandle)
         pass

    def check(self, word):
         if self.checkWord(word) == 1: return []
         self.suggest(word)
         return self.suggestions

