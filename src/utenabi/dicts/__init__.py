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

from utenabi.api import Generador, RandomGeneratorMixin


class DictFromCsv(RandomGeneratorMixin, Generador):
    
    def __init__(self, csv_filename, callback, seed=0):
        self.rnd = random.Random(seed)
        with open(csv_filename, 'r') as thefile:
            thefile.readline() # 1st line
            self.items = [
                callback(entry.split(','))
                    for entry in thefile.readlines()
            ]
        logging.info("Se cargaron %s entradas desde %s", len(self.items), csv_filename)

    def generar(self):
        """API"""
        return self.rnd.choice(self.items)

    def close(self):
        """API"""
        self.rnd = None


class UsCitiesDict(RandomGeneratorMixin, Generador):
    US_CITIES_DICT = None
    
    def __init__(self, seed=0):
        self.rnd = random.Random(seed)
        if UsCitiesDict.US_CITIES_DICT is None:
            filename = os.path.join(os.path.dirname(__file__), 'cities_us.csv')
            with open(filename, 'r') as thefile:
                thefile.readline() # 1st line
                UsCitiesDict.US_CITIES_DICT = [entry.split(',')[0:2] for entry in thefile.readlines()]

    def generar(self):
        """API"""
        return self.rnd.choice(UsCitiesDict.US_CITIES_DICT)

    def close(self):
        """API"""
        self.rnd = None


class WordDict(RandomGeneratorMixin, Generador):
    ENTRIES = {}
    
    def __init__(self, archivo, seed=0, cant_palabras_default=1):
        self.rnd = random.Random(seed)
        self.archivo = archivo
        self.cant_palabras_default = cant_palabras_default
        if self.archivo not in WordDict.ENTRIES:
            with open(archivo, 'r') as thefile:
                WordDict.ENTRIES[self.archivo] = [entry.strip().capitalize()
                    for entry in thefile.readlines()]

    def _get_entrie(self):
        return self.rnd.choice(WordDict.ENTRIES[self.archivo])

    def generar(self):
        """API"""
        if self.cant_palabras_default == 1:
            return self._get_entrie()
        else:
            return self.generar_oracion(self.cant_palabras_default)

    def generar_oracion(self, word_num):
        assert word_num >= 1
        return " ".join([self._get_entrie() for _ in range(0, word_num)])

    def close(self):
        """API"""
        self.rnd = None

    def reseed(self, generador_de_seeds):
        """API"""
        new_copy = copy.copy(self)
        new_copy.rnd = random.Random(generador_de_seeds.generar())
        return new_copy


#===============================================================================
# Main
#===============================================================================

def main():
    print "Entradas:", len(WordDict(sys.argv[1]).ENTRIES)


if __name__ == '__main__':
    main()
