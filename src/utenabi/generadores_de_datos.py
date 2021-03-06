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
import datetime
import logging
import os
import random
import time

from utenabi.dicts import UsCitiesDict, WordDict, DictFromCsv
from utenabi.api import Generador, MultiGeneradorConcatenador, RandomGeneratorMixin,\
    NoSePudoGenerarRandomUnico

logger = logging.getLogger(__name__)


#===============================================================================
# Formateadores
#===============================================================================

def formateador_booleano_01(valor):
    """Genera 0/1 dependiendo de valor booleano de`valor`"""
    if valor:
        return 1
    else:
        return 0


def formateador_2_decimales(valor):
    return "{0:0.2f}".format(valor)


#===============================================================================
# GeneradorDeItemDesdeCsv
#===============================================================================

class GeneradorDeItemDesdeCsv(RandomGeneratorMixin, Generador, DictFromCsv):
    """
    Generador que devuelve un item aleatorio, tomado desde un archivo CSV.
    """

    def __init__(self, csv_filename, callback, seed=0, *args, **kwargs):
        super(GeneradorDeItemDesdeCsv, self).__init__(csv_filename, callback, *args, **kwargs)
        self.rnd = random.Random(seed)

    def generar(self):
        """API"""
        return self.rnd.choice(self.items)

    def close(self):
        """API"""
        self.rnd = None


#===============================================================================
# GeneradorDeCiudadProvincia
#===============================================================================

class GeneradorDeCiudadProvincia(RandomGeneratorMixin, Generador, UsCitiesDict):

    def __init__(self, seed=0, *args, **kwargs):
        super(GeneradorDeCiudadProvincia, self).__init__(*args, **kwargs)
        self.rnd = random.Random(seed)

    def generar(self):
        """API"""
        return self.rnd.choice(UsCitiesDict.US_CITIES_DICT)

    def close(self):
        """API"""
        self.rnd = None


#===============================================================================
# GeneradorDePalabrasEspaniol
#===============================================================================

class GeneradorDePalabrasEspaniol(RandomGeneratorMixin, Generador, WordDict):

    def __init__(self, seed=0, cant_palabras_default=1, *args, **kwargs):
        filename = os.path.join(os.path.dirname(__file__), 'datos', 'spanish')
        super(GeneradorDePalabrasEspaniol, self).__init__(filename, *args, **kwargs)
        self.rnd = random.Random(seed)
        self.cant_palabras_default = cant_palabras_default

    def generar(self):
        """API"""
        if self.cant_palabras_default == 1:
            return self.rnd.choice(self.get_entries())
        else:
            return self.generar_oracion(self.cant_palabras_default)

    def generar_oracion(self, word_num, join_char=" "):
        assert word_num >= 1
        return join_char.join([self.rnd.choice(self.get_entries()) for _ in range(0, word_num)])

    def close(self):
        """API"""
        self.rnd = None

    def reseed(self, generador_de_seeds):
        """API"""
        new_copy = copy.copy(self)
        new_copy.rnd = random.Random(generador_de_seeds.generar())
        return new_copy


#===============================================================================
# GeneradorDeEnteroGauss
#===============================================================================

class GeneradorDeEnteroGauss(RandomGeneratorMixin, Generador):
    """
    Genera numeros aleatorios, usando `random.gauss()`
    """

    def __init__(self, gauss_mu, gauss_sigma, seed=0, unique=False, max_intentos=10):
        self.gauss_mu = gauss_mu
        self.gauss_sigma = gauss_sigma
        self.unique = unique
        self.max_intentos = max_intentos

        self.generados = set()
        self.rnd = random.Random(seed)

    def generar_numero(self):
        assert self.rnd is not None, "Generador esta cerrado"
        if self.unique:
            for _ in xrange(0, self.max_intentos):
                numero_random = int(self.rnd.gauss(self.gauss_mu, self.gauss_sigma))
                if numero_random not in self.generados:
                    self.generados.add(numero_random)
                    return numero_random
            assert False, "No se pudo generar random despues de {0} intentos".format(self.max_intentos)
        else:
            numero_random = int(self.rnd.gauss(self.gauss_mu, self.gauss_sigma))
            return numero_random

    def generar(self):
        """API"""
        return self.generar_numero()

    def close(self):
        """API"""
        self.generados = None
        self.rnd = None

    def es_unique(self, generador_de_seeds):
        """API"""
        return self.unique


#===============================================================================
# GeneradorDeEntero
#===============================================================================

class GeneradorDeEntero(RandomGeneratorMixin, Generador):
    """
    Genera numeros aleatorios, usando `random.randint()`
    """

    def __init__(self, min_num, max_num, seed=0, unique=False, max_intentos=10):
        self.min_num = min_num
        self.max_num = max_num
        self.unique = unique
        self.max_intentos = max_intentos

        self.generados = set()
        self.rnd = random.Random(seed)

    def generar(self):
        """API"""
        assert self.rnd is not None, "Generador esta cerrado"
        if self.unique:
            for _ in xrange(0, self.max_intentos):
                numero_random = self.rnd.randint(self.min_num, self.max_num)
                if numero_random not in self.generados:
                    self.generados.add(numero_random)
                    return numero_random
            raise(NoSePudoGenerarRandomUnico("No se pudo generar random despues de {0} intentos".format(
                self.max_intentos)))
        else:
            numero_random = self.rnd.randint(self.min_num, self.max_num)
            return numero_random

    def close(self):
        """API"""
        self.generados = None
        self.rnd = None

    def es_unique(self, generador_de_seeds):
        """API"""
        return self.unique


#===============================================================================
# GeneradorDeEnteroSecuencial
#===============================================================================

class GeneradorDeEnteroSecuencial(Generador):
    """
    Genera enteros secuencialmente.
    """

    def __init__(self, seed=0):
        """
        Aqui seed juega el papel de 'valor inicial'
        """
        super(GeneradorDeEnteroSecuencial, self).__init__()
        self.seed = seed
        self.entero_a_devolver = self.seed

    def generar(self):
        """API"""
        to_return = self.entero_a_devolver
        self.entero_a_devolver += 1
        return to_return

    def close(self):
        """API"""
        pass

    def reseed(self, generador_de_seeds):
        """API"""
        pass

    def es_unique(self):
        """API"""
        return False


#===============================================================================
# GeneradorDeBooleano
#===============================================================================

class GeneradorDeBooleano(RandomGeneratorMixin, Generador):
    OPCIONES = (True, False,)

    def __init__(self, seed=0, formateador=None):
        self.rnd = random.Random(seed)
        self.formateador = formateador

    def generar(self):
        """API"""
        if self.formateador:
            return self.formateador(self.rnd.choice(GeneradorDeBooleano.OPCIONES))
        else:
            return self.rnd.choice(GeneradorDeBooleano.OPCIONES)

    def set_formateador_01(self):
        self.formateador = formateador_booleano_01
        return self

    def close(self):
        """API"""
        self.rnd = None


#===============================================================================
# GeneradorDeFloat
#===============================================================================

class GeneradorDeFloat(RandomGeneratorMixin, Generador):
    """
    Genera numeros aleatorios de tipo `float`.
    """

    def __init__(self, min_num, max_num, seed=0, formateador=None):
        self.min_num = float(min_num)
        self.max_num = float(max_num)
        self.rnd = random.Random(seed)
        assert min_num < max_num
        self.formateador = formateador

    def generar(self):
        """API"""
        assert self.rnd is not None, "Generador esta cerrado"
        numero_random = (self.rnd.random() * (self.max_num - self.min_num)) + self.min_num
        if self.formateador:
            return self.formateador(numero_random)
        else:
            return numero_random

    def set_formateador_2_decimales(self):
        self.formateador = formateador_2_decimales
        return self

    def close(self):
        """API"""
        pass


#===============================================================================
# GeneradorDeOpcionPreestablecida
#===============================================================================

class GeneradorDeOpcionPreestablecida(RandomGeneratorMixin, Generador):
    """
    Devuelve alguno de los objetos (choices) preestablecidas
    """

    def __init__(self, opciones, seed=0):
        self.opciones = opciones
        self.rnd = random.Random(seed)

    def generar(self):
        """API"""
        assert self.rnd is not None, "Generador esta cerrado"
        return self.rnd.choice(self.opciones)

    def close(self):
        """API"""
        self.rnd = None


#===============================================================================
# GeneradorDeFecha
#===============================================================================

class GeneradorDeFecha(GeneradorDeEntero):
    """
    Genera fecha aleatoria
    """

    def __init__(self, seed=0):
        super(GeneradorDeFecha, self).__init__(0, int(time.time()), seed=seed)

    def generar(self):
        """API"""
        fecha_rnd = time.gmtime(super(GeneradorDeFecha, self).generar())
        return "{0:04}{1:02}{2:02}".format(fecha_rnd.tm_year, fecha_rnd.tm_mon, fecha_rnd.tm_mday)

    def close(self):
        """API"""
        self.rnd = None


#===============================================================================
# GeneradorDeFechaSecuencial
#===============================================================================

class GeneradorDeFechaSecuencial(Generador):
    """
    Genera fechas secuencialmente.
    Genera desde fecha_inicial hasta fecha_final, incluyendo ambas fechas.
    `fecha_final` solo sirve para calcular cuantas filas habria que crear,
    a tavez de `calcular_count()`.
    """

    def __init__(self, fecha_inicial, fecha_final, seed=0):
        super(GeneradorDeFechaSecuencial, self).__init__()
        self.fecha_inicial = fecha_inicial
        self.fecha_final = fecha_final
        self.fecha_a_devolver = self.fecha_inicial
        assert isinstance(self.fecha_inicial, datetime.date)
        assert isinstance(self.fecha_final, datetime.date)
        assert (self.fecha_final - self.fecha_inicial).days >= 0

    def calcular_count(self):
        return (self.fecha_final - self.fecha_inicial).days + 1

    def generar(self):
        """API"""
        ymd = "{0:04}-{1:02}-{2:02}".format(self.fecha_a_devolver.year,
            self.fecha_a_devolver.month, self.fecha_a_devolver.day)
        to_return = (ymd, str(self.fecha_a_devolver.year),
            str(self.fecha_a_devolver.month), str(self.fecha_a_devolver.day))
        self.fecha_a_devolver = self.fecha_a_devolver + datetime.timedelta(days=1)
        return to_return

    def close(self):
        """API"""
        pass

    def reseed(self, generador_de_seeds):
        """API"""
        pass

    def es_unique(self):
        """API"""
        return False


#===============================================================================
# GeneradorDeBarrioCiudadProvincia
#===============================================================================

class GeneradorDeBarrioCiudadProvincia(Generador):
    """Genera Barrio, Ciudad, Estado"""

    def __init__(self, seed=0):
        self.spanish_word_dict = GeneradorDePalabrasEspaniol(seed=seed)
        self.us_cities_dict = GeneradorDeCiudadProvincia(seed=seed)

    def generar(self):
        """API"""
        city = self.us_cities_dict.generar()
        return (self.spanish_word_dict.generar(), city[1], city[0])

    def close(self):
        """API"""
        self.spanish_word_dict.close()
        self.us_cities_dict.close()

    def reseed(self, generador_de_seeds):
        """API"""
        new_copy = copy.copy(self)
        new_copy.spanish_word_dict = self.spanish_word_dict.reseed(generador_de_seeds)
        new_copy.us_cities_dict = self.us_cities_dict.reseed(generador_de_seeds)
        return new_copy


#===============================================================================
# GeneradorDeNroDocumento
#===============================================================================

class GeneradorDeNroDocumento(GeneradorDeEnteroGauss):
    """Genera numeros de documentos UNICOS"""

    def __init__(self, *args, **kwargs):
        super(GeneradorDeNroDocumento, self).__init__(40000000, 10000000,
            unique=kwargs.pop('unique', True), *args, **kwargs)


#===============================================================================
# GeneradorDeCP
#===============================================================================

class GeneradorDeCP(GeneradorDeEntero):
    """Genera CP"""

    def __init__(self, *args, **kwargs):
        super(GeneradorDeCP, self).__init__(1000, 9000, *args, **kwargs)


#===============================================================================
# GeneradorDeRazonSocial
#===============================================================================

class GeneradorDeRazonSocial(MultiGeneradorConcatenador):
    """Genera Razon Social"""

    SUFIJO_RAZON_SOCIAL = (
        'S.A.',
        'S.R.L.',
        'y Cia.',
        'e Hijos',
    )

    def __init__(self, *args, **kwargs):
        if 'seed' in kwargs:
            seed = kwargs['seed']
        else:
            seed = 0
        super(GeneradorDeRazonSocial, self).__init__(
            generadores=(
                GeneradorDePalabrasEspaniol(cant_palabras_default=2,
                    seed=seed),
                GeneradorDeOpcionPreestablecida(opciones=GeneradorDeRazonSocial.SUFIJO_RAZON_SOCIAL,
                    seed=seed),
            ),
            *args,
            **kwargs)
