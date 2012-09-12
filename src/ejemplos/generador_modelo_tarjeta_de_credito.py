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

import datetime
import logging
import multiprocessing
import os
import sys

# Para facilitar ejecucion, intentamos importar, y si falla, seteamos sys.path
try:
    from utenabi.api import MultiGenerador as _ignore_this_import #@UnusedImport
except ImportError:
    sys.path.append(os.path.split(os.path.dirname(__file__))[0])

from utenabi.api import MultiGenerador
from utenabi.generadores_de_archivos import ArchivoCSV, AdaptadorMultiproceso
from utenabi.generadores_de_datos import GeneradorDeItemDesdeCsv,\
    GeneradorDeOpcionPreestablecida, \
    GeneradorDePalabrasEspaniol, GeneradorDeBarrioCiudadProvincia,\
    GeneradorDeEntero, GeneradorDeRazonSocial,\
    GeneradorDeFloat, GeneradorDeFechaSecuencial, GeneradorDeEnteroSecuencial

logger = logging.getLogger(__name__)

RUBROS = [
    'Supermercados',
    'Electrónica',
    'Automotores',
    'Servicios',
]


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Genera datos, emulando los datos que se tomarian de un sistema transaccional
# de una empresa financiera generica que posee tarjetas de credito.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def generar_todos(filename_prefix, cant_tarjetas, cant_comercios, cant_cupones):

    filename_tarjetas_personas = '/tmp/' + filename_prefix + '_tarjeta_con_persona.csv'
    filename_comercios = '/tmp/' + filename_prefix + '_comercios.csv'
    filename_fechas = '/tmp/' + filename_prefix + '_fechas.csv'
    filename_cupones = '/tmp/' + filename_prefix + '_cupones.csv'
    filename_sql = '/tmp/' + filename_prefix + '.sql'

    #===========================================================================
    # Generamos comercios
    #===========================================================================

    #
    # Un comercio tiene varios datos:
    # -id
    # - codigo de comercio
    # - razon social
    # - rubro
    #
    # Usamos un `Generador` para generar cada uno de estos datos: Ej:
    # - GeneradorDeEnteroSecuencial: numero secuencial (para PRIMARY KEY)
    # - GeneradorDeEntero: generara un entero aleatorio UNICO
    # - GeneradorDeRazonSocial: generara 2 palabras aleatorios, y le agregara "S.A.", "S.R.L.", etc
    # - GeneradorDeOpcionPreestablecida: devolvera aleatoriamente alguna de las opciones
    #    pasadas por parametros (en este caso, devolvera aleatoriamente alguno de los rubros preestablecidos)
    #
    multigenerador = MultiGenerador((
        GeneradorDeEnteroSecuencial(seed=1),
        GeneradorDeEntero(10000000, 99999999, unique=True),
        GeneradorDeRazonSocial(), # razon social
        GeneradorDeOpcionPreestablecida(opciones=RUBROS),
    ))

    # El archivo CSV debe tener un encabezado...
    headers_csv = (
        "id",
        "numero_de_comercio",
        "razon_social",
        "rubro",
    )

    # Creamos instancia de `ArchivoCSV`, para luego generar los datos aleatorios
    archivo_csv = ArchivoCSV(multigenerador, headers_csv)

    # La cantidad de filas a generar depende de `cant_comercios`
    logger.info("Iniciando generacion de comercios...")
    archivo_csv.generar_csv(filename_comercios, cant_comercios)

    # Liberamos recursos...
    archivo_csv.close()

    del multigenerador, headers_csv, archivo_csv

    #===========================================================================
    # Generamos fechas
    #===========================================================================
    logger.info("Iniciando generacion de fechas...")

    fecha_desde = datetime.date(year=2001, month=1, day=1)
    fecha_hasta = datetime.date(year=2011, month=12, day=31)

    # Creamos 'generador' de fechas antes que nada, porque mas adelante
    # necesitaremos tener una referencia a este objeto...
    generador_fechas = GeneradorDeFechaSecuencial(fecha_desde, fecha_hasta)

    # Los elementos del encabezado serán:
    headers_csv = (
        "id",
        "fecha", # <PK>
        "anio",
        "mes",
        "dia",
    )

    # Cada fila del CSV de fecha debe tener MULTIPLES columnas, por eso usamos `MultiGenerador`
    # Un `MultiGenerador` es un contenedor de `Generadores`
    # 1er columna. ID -> lo generamos con `GeneradorDeEnteroSecuencial()`
    # 2da, 3ra, 4ta, 5ta columna -> fecha, año, mes y dia: lo genera `GeneradorDeFechaSecuencial()`
    multigenerador = MultiGenerador(
        (
            GeneradorDeEnteroSecuencial(seed=1),
            generador_fechas,
        )
    )

    # Creamos instancia de `ArchivoCSV`, para luego generar los datos aleatorios
    archivo_csv = ArchivoCSV(multigenerador, headers_csv)

    # En este caso, no sabemos la cantidad de registros a crear,
    # sino que quremos crear desde la fecha `fecha_desde` hasta la fecha `fecha_hasta`...
    # El calculo de cuantas fechas hay en ese rango, usamos `generador_fechas.calcular_count()`
    archivo_csv.generar_csv(filename_fechas, generador_fechas.calcular_count())

    # Liberamos recursos...
    archivo_csv.close()

    del multigenerador, headers_csv, archivo_csv, generador_fechas, fecha_desde, fecha_hasta

    #===========================================================================
    # Generamos tarjeta + personas
    #===========================================================================

    logger.info("Iniciando generacion de tarjetas (con infor de personas)...")

    multigenerador = MultiGenerador((
            GeneradorDeEntero(100000000000, 999999999999, unique=True), # numero_de_tarjeta
            GeneradorDeEntero(1000000, 9999999, unique=True), # numero_de_cuenta
            GeneradorDePalabrasEspaniol(seed=0, cant_palabras_default=2), # nombre, apellido
            GeneradorDePalabrasEspaniol(seed=0, cant_palabras_default=1), # barrio
            GeneradorDeBarrioCiudadProvincia(), # ciudad, provincia
    ))
    headers_csv = (
            # "id", -> es generado al crear el archivo: parametro `generar_id` de `generar_csv()`
            "numero_de_tarjeta", # <PK>
            "numero_de_cuenta",
            "nombre",
            "apellido",
            "barrio",
            "ciudad",
            "provincia",
    )
    archivo_csv = ArchivoCSV(multigenerador, headers_csv)

    # En este caso, queremos aprovechar los multiples procesadores que posee el hardware,
    # por lo tanto creamos una instancia de `AdaptadorMultiproceso`, para que los datos
    # del archivo CSV sean generados en paralelo
    adaptador_multiproceso = AdaptadorMultiproceso(archivo_csv, multiprocessing.cpu_count())

    # Como queremos que exista un identificador secuencial, usamos `generar_id`. Esto
    # hace que se cree una columa `id`, numercia, incremental, que comienza en `1`.
    adaptador_multiproceso.generar_csv(filename_tarjetas_personas, cant_tarjetas, generar_id=True)
    adaptador_multiproceso.close()

    del adaptador_multiproceso, multigenerador, headers_csv, archivo_csv

    #===========================================================================
    # Dict con tarjetas generadas
    #===========================================================================
    def callback_fecha(obj):
        return obj[0]
    dict_fechas = GeneradorDeItemDesdeCsv(filename_fechas, callback_fecha)

    #===========================================================================
    # Dict con tarjetas generadas
    #===========================================================================
    def callback_tarjeta(obj):
        return obj[0]
    dict_tarjetas = GeneradorDeItemDesdeCsv(filename_tarjetas_personas, callback_tarjeta)

    #===========================================================================
    # Dict con comercios generados
    #===========================================================================
    def callback_comercio(obj):
        return obj[0]
    dict_comercios = GeneradorDeItemDesdeCsv(filename_comercios, callback_comercio)

    #===========================================================================
    # Generamos cupones
    #===========================================================================
    logger.info("Iniciando generacion de cupones...")

    generadores = (
        dict_fechas,
        dict_tarjetas,
        dict_comercios,
        # dict_plan,
        GeneradorDeFloat(20, 2000, seed=0).set_formateador_2_decimales(),
        GeneradorDeEntero(0, 9999999), # cupon
    )
    headers_csv = (
            "id_fecha", # <FK>
            "id_tarjeta", # <FK>
            "id_comercio", # <FK>
            "monto", # HECHO
            "numero_cupon",
    )
    multigenerador = MultiGenerador(generadores)
    archivo_csv = ArchivoCSV(multigenerador, headers_csv)
    generador_cupones = AdaptadorMultiproceso(
        archivo_csv,
        multiprocessing.cpu_count(),
    )
    generated_filenames_list = []
    generador_cupones.generar_multiples_csv_concurrentes(filename_cupones, generated_filenames_list,
        cant_cupones)
    generador_cupones.close()
    del generador_cupones

    #===========================================================================
    # Generamos archivo SQL
    #===========================================================================

    #
    # Para facilitar la carga de estos datos, aqui mismo generamos un archivo SQL
    # que incluya la estructura de la BD y haga la carga de los datos teniendo
    # en cuenta los nombres de los archivos generados.
    #

    sql = """

    -- #
    -- # Cambios en configuracion por default:
    -- #
    -- # + PERFORMANCE: http://www.postgresql.org/docs/current/static/populate.html
    -- # + NON-DURABILITY: http://www.postgresql.org/docs/current/static/non-durability.html
    -- #
    -- # fsync = off
    -- # full_page_writes = off
    -- # checkpoint_segments = 30
    -- # autovacuum = off
    -- #

    -- # http://www.postgresql.org/docs/current/static/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM
    set maintenance_work_mem = '512MB';

    DROP TABLE IF EXISTS th_cupones;
    DROP TABLE IF EXISTS d_tarjeta;
    DROP TABLE IF EXISTS d_fecha;
    DROP TABLE IF EXISTS d_comercio;
    
    --
    -- FECHA
    --

    CREATE TABLE d_fecha (
        id integer PRIMARY KEY,
        fecha char(10) not null,
        anio integer not null,
        mes integer not null,
        dia integer not null
    );

    select now();

    COPY d_fecha from '%(archivo_csv_d_fecha)s' CSV HEADER;

    select now();

    CREATE INDEX ON d_fecha (anio);

    select now();

    CREATE INDEX ON d_fecha (mes);

    select now();

    CREATE INDEX ON d_fecha (dia);

    select now();

    --
    -- TARJETAS
    --

    CREATE TABLE d_tarjeta (
        id integer PRIMARY KEY,
        numero_de_tarjeta bigint not null,
        numero_de_cuenta integer not null,
        nombre char(40) not null,
        apellido char(40) not null,
        barrio char(40) not null,
        ciudad char(40) not null,
        provincia char(40) not null
    );

    select now();

    COPY d_tarjeta from '%(archivo_csv_d_tarjeta)s' CSV HEADER;

    select now();

    CREATE INDEX ON d_tarjeta (barrio);

    select now();

    CREATE INDEX ON d_tarjeta (ciudad);

    select now();

    CREATE INDEX ON d_tarjeta (provincia);

    select now();

    --
    -- COMERCIOS
    --

    CREATE TABLE d_comercio (
        id integer PRIMARY KEY,
        numero_de_comercio integer not null,
        razon_social char(60) not null,
        rubro char(40) not null
    );

    select now();

    COPY d_comercio from '%(archivo_csv_d_comercio)s' CSV HEADER;

    select now();

    CREATE INDEX ON d_comercio (rubro);

    select now();

    --
    -- CUPONES
    --

    CREATE TABLE th_cupones (
        id_fecha integer not null,
        id_tarjeta integer not null,
        id_comercio integer not null,
        monto float not null,
        numero_cupon integer not null
    );

    select now();

    """ % {
        'archivo_csv_d_fecha': filename_fechas,
        'archivo_csv_d_tarjeta': filename_tarjetas_personas,
        'archivo_csv_d_comercio': filename_comercios,
    }

    for a_filename in generated_filenames_list:
        sql += """

        COPY th_cupones from '{0}' CSV HEADER;

        select now();

        """.format(a_filename)

    sql += """

    CREATE INDEX ON th_cupones (id_fecha);

    select now();

    CREATE INDEX ON th_cupones (id_tarjeta);

    select now();

    CREATE INDEX ON th_cupones (id_comercio);

    select now();

    ALTER TABLE th_cupones
        ADD CONSTRAINT cupones_fecha_fk
            FOREIGN KEY (id_fecha)
                REFERENCES d_fecha(id);

    select now();

    ALTER TABLE th_cupones
        ADD CONSTRAINT cupones_tarjeta_fk
            FOREIGN KEY (id_tarjeta)
                REFERENCES d_tarjeta(id);

    select now();

    ALTER TABLE th_cupones
        ADD CONSTRAINT cupones_comercio_fk
            FOREIGN KEY (id_comercio)
                REFERENCES d_comercio(id);

    select now();

    """

    logger.info("Guardando SQL en {0}...".format(filename_sql))
    with open(filename_sql, 'w') as sql_f:
        sql_f.write(sql)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        filename_prefix = sys.argv[1]
        cant_tarjetas = int(sys.argv[2])
        cant_comercios = int(sys.argv[3])
        cant_cupones = int(sys.argv[4])
    except:
        raise(Exception("Argumentos: <prefijo_nombre_de_archivo> <cant_tarjetas> <cant_comercios> <cant_cupones>"))
    generar_todos(filename_prefix, cant_tarjetas, cant_comercios, cant_cupones)
