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

import os
import unittest
import random
import time

from utenabi.api import MultiGenerador
from utenabi.dicts import UsCitiesDict, DictFromCsv
from utenabi.generators import \
    GeneradorDeBarrioCiudadProvincia, \
    GeneradorDeEntero, GeneradorDeFecha,\
    GeneradorDeFloat, GeneradorDeOpcionPreestablecida, GeneradorDeBooleano,\
    MultiGeneradorConcatenador, GeneradorDeNroDocumento,\
    GeneradorDePalabrasEspaniol, GeneradorDeEnteroGauss


class DictTest(unittest.TestCase):

    def test_spanish(self):
        self.assertTrue(GeneradorDePalabrasEspaniol())

    def test_generar(self):
        wdict = GeneradorDePalabrasEspaniol()
        self.assertNotEqual(wdict.generar(), wdict.generar())

    def test_generar_oracion(self):
        wdict = GeneradorDePalabrasEspaniol()
        sentence = wdict.generar_oracion(5)
        self.assertEqual(len(sentence.split()), 5)

    def test_dictfromcsv(self):
        def getfirst(obj):
            return obj[0]
        filename = os.path.join(os.path.join(os.path.dirname(__file__), 'dicts'), 'cities_us.csv')
        dfc = DictFromCsv(filename, getfirst, seed=0)
        self.assertNotEqual(dfc.generar(), dfc.generar())
        self.assertTrue(len(dfc.generar()) > 0)


class RandomTest(unittest.TestCase):

    def test_gauss(self):
        """Simple test to check out how `gauss()` works"""
        rnd = random.Random(0)
        numbers = {}
        mu = 20
        sigma = int(mu / 5)
        for _ in range(0, 10000):
            n = int(rnd.gauss(mu, sigma))
            try:
                numbers[n] = numbers[n] + 1
            except KeyError:
                numbers[n] = 1

        for x in range(0, mu * 2):
            try:
                val = numbers[x]
            except KeyError:
                val = 0
            print x, ":", val


class GeneradorDeNumDocumentoTest(unittest.TestCase):

    def test_doc(self):
        generator = GeneradorDeNroDocumento()
        self.assertNotEqual(generator.generar(), generator.generar())


class GeneradorDeEnteroTest(unittest.TestCase):

    def test(self):
        generator = GeneradorDeEntero(0, 1)
        gen_list = set([generator.generar() for _ in range(0, 20)])
        self.assertTrue(0 in gen_list)
        self.assertTrue(1 in gen_list)
        self.assertEqual(len(gen_list), 2)


class GeneradorDeBooleanoTest(unittest.TestCase):

    def test(self):
        generator = GeneradorDeBooleano()
        gen_list = set([generator.generar() for _ in range(0, 20)])
        self.assertTrue(True in gen_list)
        self.assertTrue(False in gen_list)
        self.assertEqual(len(gen_list), 2)


class GeneradorDeFloatTest(unittest.TestCase):

    def test(self):
        generator = GeneradorDeFloat(100, 500)
        for num in [generator.generar() for _ in range(0, 20)]:
            self.assertTrue(num >= 100.0)
            self.assertTrue(num <= 500.0)


class GeneradorDeFechaTest(unittest.TestCase):

    def test(self):
        anio_actual = time.gmtime().tm_year
        generador = GeneradorDeFecha()
        fechas = [generador.generar() for _ in range(0, 50)]
        print fechas[0]
        for fecha in fechas:
            self.assertEqual(len(fecha), 8)
            y, m, d = int(fecha[0:4]), int(fecha[4:6]), int(fecha[6:8])
            self.assertTrue(y >= 1969 and y <= anio_actual)
            self.assertTrue(m >= 1 and m <= 12)
            self.assertTrue(d >= 1 and d <= 31)


class UsCitiesDictTest(unittest.TestCase):

    def test_dict(self):
        cities_dict = UsCitiesDict()
        print UsCitiesDict.US_CITIES_DICT[0]
        print UsCitiesDict.US_CITIES_DICT[-1]
        print UsCitiesDict.US_CITIES_DICT[0:10]

        self.assertNotEqual(cities_dict.generar(), cities_dict.generar())


class GeneradorDeBarrioCiudadProvinciaTest(unittest.TestCase):

    def test_generator(self):
        generator = GeneradorDeBarrioCiudadProvincia()
        print generator.generar()
        self.assertNotEqual(generator.generar(), generator.generar())


class GeneradorDeOpcionPreestablecidaTest(unittest.TestCase):

    def test(self):
        generador = GeneradorDeOpcionPreestablecida(['A', 'B', 'C'])
        opciones = set([generador.generar() for _ in range(0, 30)])
        self.assertTrue('A' in opciones)
        self.assertTrue('B' in opciones)
        self.assertTrue('C' in opciones)


class ReseedTest(unittest.TestCase):

    def test(self):
        generadores = (
            GeneradorDePalabrasEspaniol(seed=0),
            GeneradorDeEntero(0, 999999, seed=0),
            GeneradorDeEnteroGauss(100, 5, seed=0),
            GeneradorDeBooleano(seed=0),
            GeneradorDeFloat(0, 999999, seed=0),
            GeneradorDeFecha(seed=0),
            GeneradorDeBarrioCiudadProvincia(seed=0),
            GeneradorDeNroDocumento(unique=False, seed=0),
        )
        for gen in generadores:
            print gen
            gen1 = gen
            gen2 = gen1.reseed(0)
            gen3 = gen1.reseed(1)

            val1 = gen1.generar()
            val2 = gen2.generar()
            val3 = gen3.generar()
            self.assertEqual(val1, val2)
            self.assertNotEqual(val1, val3)


class MultiGeneradorTest(unittest.TestCase):

    def test(self):
        metagen = MultiGenerador()
        metagen.agregar_generador(GeneradorDeNroDocumento())
        metagen.agregar_generador(GeneradorDeBarrioCiudadProvincia())
        metagen.agregar_generador(GeneradorDeNroDocumento())

        undato = metagen.generar()
        print undato
        self.assertEqual(len(undato), 5)
        int(undato[0]) # dni deberia ser convertible a `int`
        int(undato[4]) # dni deberia ser convertible a `int`

    def test_reseed(self):
        metagen = MultiGenerador()
        metagen.agregar_generador(GeneradorDeNroDocumento(seed=0, unique=False))
        metagen.agregar_generador(GeneradorDeBarrioCiudadProvincia(seed=0))
        metagen.agregar_generador(GeneradorDeNroDocumento(seed=0, unique=False))
        val1 = metagen.generar()
        val2 = metagen.generar()
        self.assertNotEqual(val1, val2)

        reseeded = metagen.reseed(0)
        val3 = reseeded.generar()
        val4 = reseeded.generar()
        self.assertEqual(val1, val3)
        self.assertEqual(val2, val4)


class MultiGeneradorConcatenadorTest(unittest.TestCase):

    def test(self):
        concatenador = MultiGeneradorConcatenador()
        concatenador.agregar_generador(GeneradorDeEntero(0, 9))
        concatenador.agregar_generador(GeneradorDeEntero(0, 9))
        concatenador.agregar_generador(GeneradorDeEntero(0, 9))
        numeros = [int(num) for num in concatenador.generar().split()]
        self.assertEqual(len(numeros), 3)
        self.assertTrue(sum(numeros) >= 0)
        self.assertTrue(sum(numeros) <= 3 * 9)


if __name__ == '__main__':
    unittest.main()