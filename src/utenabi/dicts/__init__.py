# -*- coding: utf-8 -*-

##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    utenabi - Herramientas para tutoria de materia BI en UTN FRC
##    Copyright (C) 2012 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of utenabi.
##
##    utenabi is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    utenabi is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with utenabi; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import copy
import logging
import os
import random
import sys


class DictFromCsv(object):
    
    def __init__(self, csv_filename, callback, seed=0):
        with open(csv_filename, 'r') as thefile:
            thefile.readline() # 1st line
            self.items = [
                callback(entry.split(','))
                    for entry in thefile.readlines()
            ]
        logging.info("Se cargaron %s entradas desde %s", len(self.items), csv_filename)

    def get_items(self):
        return self.items


class UsCitiesDict(object):
    US_CITIES_DICT = None
    
    def __init__(self, seed=0):
        if UsCitiesDict.US_CITIES_DICT is None:
            filename = os.path.join(os.path.dirname(__file__), 'cities_us.csv')
            with open(filename, 'r') as thefile:
                thefile.readline() # 1st line
                UsCitiesDict.US_CITIES_DICT = [entry.split(',')[0:2] for entry in thefile.readlines()]


class WordDict(object):
    ENTRIES = {}
    
    def __init__(self, archivo):
        self.archivo = archivo
        if self.archivo not in WordDict.ENTRIES:
            with open(archivo, 'r') as thefile:
                WordDict.ENTRIES[self.archivo] = [entry.strip().capitalize()
                    for entry in thefile.readlines()]

    def get_entries(self):
        return WordDict.ENTRIES[self.archivo]


#===============================================================================
# Main
#===============================================================================

def main():
    print "Entradas:", len(WordDict(sys.argv[1]).ENTRIES)


if __name__ == '__main__':
    main()
