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

import csv
import logging
import time
import copy
import random
import multiprocessing

from itertools import izip

logger = logging.getLogger(__name__)

LOGUEAR_CADA = 2000

"""
CHILD_CHUNK_SIZE: cuantos elementos enviar al queue por vez.
Los procesos hijos generan elementos aleatorios en un buffer,
y al crear CHILD_CHUNK_SIZE elementos, son enviados juntos.
"""
CHILD_CHUNK_SIZE = 100


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


class GeneradorCSV(object):
    """
    MultiGenerador, que genera items y los guarda en archivo CSV
    """

    def __init__(self, generador, headers_csv):
        super(GeneradorCSV, self).__init__()
        assert isinstance(headers_csv, (list, tuple))
        assert isinstance(generador, MultiGenerador)
        self.headers_csv = list(headers_csv)
        self.generador = generador

    def agregar_generador(self, generador):
        """Agrega nuevo generador a self.generador"""
        self.generador.agregar_generador(generador)
        return self

    def agregar_headers_csv(self, header_csv):
        """Agrega nuevo header para csv"""
        self.headers_csv.append(header_csv)
        return self

    def get_headers_csv(self):
        return self.headers_csv

    def generar_multiples(self, max_count=2):
        for num in xrange(0, max_count):
            yield self.generador.generar()
            if num % LOGUEAR_CADA == 0:
                logger.info("Ya se crearon %s instancias", num)

    def generar_csv(self, filename, max_count=2):
        start = time.time()
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(self.get_headers_csv())
            writer.writerows(self.generar_multiples(max_count))
        end = time.time()
        logger.info("Se generaron {0} objetos en {1:0.2f} seg. - Promedio: {2:0.2f} obj/seg. - {3}".format(
            max_count, end - start, (float(max_count) / (end - start)), filename))
        return self

    def close(self):
        """API"""
        self.generador.close()


def _gen_data(generador, count, queue):
    chunk = []
    for iter_num in xrange(0, count):
        chunk.append(generador.generar())
        if iter_num % CHILD_CHUNK_SIZE == 0 and chunk:
            queue.put(chunk)
            chunk = []
    if chunk:
        queue.put(chunk)
    queue.put(None)


class GeneradorCSVMultiprocess(object):

    def __init__(self, generador_csv_base, cant_procesos, seed_generador_de_seeds=0):
        """Cant. de procesos determinado por items en seeds"""
        self.generador_csv_base = generador_csv_base
        # `generador_de_seeds` -> es usado para generar los nuevos seeds
        from utenabi.generators import GeneradorDeEntero
        self.generador_de_seeds = GeneradorDeEntero(0, 99999999,
            seed=seed_generador_de_seeds, unique=True)
        self.generadores = [generador_csv_base.generador.reseed(self.generador_de_seeds)
            for _ in range(0, cant_procesos)]

    def generar_csv(self, filename, max_count=100, generar_id=False):
        """
        Parametros:
        - generar_id: si `True`, genera una columna "ID", numerica, secuencial, comenzando en 1
        """
        queue = multiprocessing.Queue()
        if generar_id:
            id_generator = xrange(1, max_count + 1)
        else:
            id_generator = None

        start = time.time()
        num = 0
        loguear_cada = LOGUEAR_CADA / 100
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            if id_generator is None:
                writer.writerow(self.generador_csv_base.get_headers_csv())
            else:
                writer.writerow(["id"] + list(self.generador_csv_base.get_headers_csv()))

            # Iniciamos multiprocesamiento
            processes = []
            try:
                unique_gens = []
                unique_gens_index = []
                index = 0
                for gen in self.generadores:
                    target_args = (gen, int(max_count / len(self.generadores)), queue, )
                    proc = multiprocessing.Process(target=_gen_data, args=target_args)
                    proc.start()
                    logger.info("Iniciando proceso %s", proc.pid)
                    processes.append(proc)

                    if gen.es_unique():
                        unique_gens.append(set())
                        unique_gens_index.append(index)
                    else:
                        unique_gens.append(None)
                    index += 1

                iter_num = 0
                none_recibidos = 0
                while none_recibidos < len(processes):
                    data = queue.get(timeout=1)
                    if data is None:
                        none_recibidos += 1 # se finalizo el child
                    else:
                        unique_data = []
                        for row in data:
                            linea_es_unica = True
                            for index in unique_gens_index:
                                if row[index] in unique_gens[index]:
                                    logger.warn("Ignorando item repetido")
                                    linea_es_unica = False
                                else:
                                    unique_gens[index].add(row[index])
                            if linea_es_unica:
                                unique_data.append(row)
                        if id_generator is not None:
                            writer.writerows(izip(id_generator, unique_data))
                        else:
                            writer.writerows(unique_data)
                        num += len(unique_data)
                        iter_num += 1
                        if iter_num % loguear_cada == 0:
                            logger.info("Ya se crearon %s instancias", num)
            except:
                logger.exception("Excepcion detectada... ejecutaremos terminate() sobre procesos hijos")
                try:
                    for p in processes:
                        p.terminate()
                except:
                    pass
            finally:
                try:
                    for p in processes:
                        p.join()
                except:
                    pass

        end = time.time()
        logger.info("Se generaron {0} objetos en {1:0.2f} seg. - Promedio: {2:0.2f} obj/seg. - {3}".format(
            num, end - start, (float(num) / (end - start)), filename))
        return self

    def close(self):
        """API"""
        [gen.close() for gen in self.generadores]
