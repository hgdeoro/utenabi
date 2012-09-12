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

import logging
import copy
import random

logger = logging.getLogger(__name__)


class NoSePudoGenerarRandomUnico(Exception):
    """
    Excepcion lanzada cuando luego de muchos intentos, no se pudo
    generar un nro aleatorio unico (diferente a los generados anteriormente).
    """
    pass


#===============================================================================
# Generador generico
#===============================================================================

class Generador(object):
    """
    Un generador de datos. Ej: numero entero, float, nombre, etc.
    """

    def generar(self):
        """API"""
        assert False, "Este metodo deberia estar implemetado"

    def close(self):
        """API"""
        assert False, "Este metodo deberia estar implemetado"

    def reseed(self, generador_de_seeds):
        """API"""
        assert False, "Este metodo deberia estar implemetado"

    def es_unique(self):
        """API"""
        return False


class RandomGeneratorMixin(object):

    def reseed(self, generador_de_seeds):
        """API"""
        new_copy = copy.copy(self)
        new_copy.rnd = random.Random(generador_de_seeds.generar())
        return new_copy


#===============================================================================
# MultiGenerador
#===============================================================================

class MultiGenerador(Generador):
    """
    Contenedor de Generadores.
    Genera un CONJUNTO de elementos
    (un elemento por cada generador agregado)
    """

    def __init__(self, generadores=None, seed=0):
        if generadores is None:
            self.generadores = []
        else:
            assert isinstance(generadores, (list, tuple))
            self.generadores = list(generadores)
        for gen in self.generadores:
            assert isinstance(gen, Generador)

    def agregar_generador(self, generador):
        assert isinstance(generador, Generador)
        self.generadores.append(generador)
        return self

    def generar(self):
        """API"""
        multiple = []
        for generador in self.generadores:
            nuevo_item = generador.generar()
            if isinstance(nuevo_item, list):
                multiple += nuevo_item
            elif isinstance(nuevo_item, tuple):
                multiple += list(nuevo_item)
            else:
                multiple.append(nuevo_item)
        return multiple

    def close(self):
        """API"""
        for generador in self.generadores:
            generador.close()

    def reseed(self, generador_de_seeds):
        """API"""
        new_copy = copy.copy(self)
        new_copy.generadores = tuple([g.reseed(generador_de_seeds)
            for g in self.generadores])
        return new_copy


class MultiGeneradorConcatenador(MultiGenerador):
    """
    Contenedor de Generadores.
    Genera un elemento, resultado de concatenar los elementos
    generados por c/u de los generadores contenidos.
    """

    def generar(self):
        """API"""
        generados = super(MultiGeneradorConcatenador, self).generar()
        if isinstance(generados, (list, tuple,)):
            generados = [str(item) for item in generados]
        else:
            generados = str(generados)

        return " ".join(generados)
