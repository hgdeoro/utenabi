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

import multiprocessing
import logging
import os
import sys

try:
    from utenabi.api import MultiGenerador as _ignore_this_import #@UnusedImport
except ImportError:
    sys.path.append(os.path.split(os.path.dirname(__file__))[0])

from utenabi.api import MultiGenerador, GeneradorCSV, GeneradorCSVMultiprocess
from utenabi.generators import GeneradorDeOpcionPreestablecida,\
    GeneradorDeNroDocumento, GeneradorDePalabrasEspaniol,\
    GeneradorDeBarrioCiudadProvincia, GeneradorDeCP, GeneradorDeFecha


def main():
    assert len(sys.argv) == 3, "Debe especificar: la cantidad de personas " \
        "a crear y el nombre de archivo destino"

    obj_count = int(sys.argv[1])
    archivo_destino = sys.argv[2]

    assert not os.path.exists(archivo_destino), \
        "El archivo destino ya existe... por las dudas salimos..."

    logging.basicConfig(level=logging.INFO)

    process_count = multiprocessing.cpu_count()
    logging.info("Lanzando %s procesos concurrentes", process_count)

    multigenerador = MultiGenerador((
        # tipo de doc -> dni, le, lc
        GeneradorDeOpcionPreestablecida(opciones=('dni', 'le', 'lc'), seed=0),
        # numero de documento (UNICO, NO GENERA REPETIDOS)
        GeneradorDeNroDocumento(seed=0),
        # nombre -> 2 palabras españolas aleatorias
        GeneradorDePalabrasEspaniol(seed=0, cant_palabras_default=2),
        # apellido -> 1 palabra español aleatoria
        GeneradorDePalabrasEspaniol(seed=0, cant_palabras_default=1),
        # barrio, ciudad, provincia
        GeneradorDeBarrioCiudadProvincia(),
        # codigo postal
        GeneradorDeCP(),
        # fecha de nacimiento
        GeneradorDeFecha(seed=0),
    ))
    headers_csv = (
            "tipo_doc",
            "nro_doc",
            "nombre",
            "apellido",
            "barrio",
            "ciudad",
            "provincia",
            "cp",
            "fecha_nacimiento",
    )

    generador_csv = GeneradorCSV(multigenerador, headers_csv)
    if process_count > 1:
        logging.info("Iniciando GeneradorCSVMultiprocess")
        generador_multiprocess = GeneradorCSVMultiprocess(
            generador_csv,
            process_count
        )
        generador_multiprocess.generar_csv(archivo_destino, obj_count)
        generador_multiprocess.close()
    else:
        logging.info("Iniciando GeneradorCSV")
        generador_csv.generar_csv(archivo_destino, obj_count)
        generador_csv.close()


if __name__ == '__main__':
    main()
