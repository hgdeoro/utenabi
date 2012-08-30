# -*- coding: utf-8 -*-

import logging
import os
import sys

from utenabi.api import MultiGenerador, GeneradorCSVMultiprocess, GeneradorCSV
from utenabi.generators import GeneradorDeOpcionPreestablecida,\
    GeneradorDeNroDocumento, GeneradorDePalabrasEspaniol,\
    GeneradorDeBarrioCiudadProvincia, GeneradorDeCP, GeneradorDeFecha,\
    GeneradorDeEntero


def main():
    assert len(sys.argv) == 3, "Debe especificar: process_count, obj_count"
    process_count = int(sys.argv[1])
    obj_count = int(sys.argv[2])

    assert process_count <= 32, "Ha especificado demasiados proceos (>32)"

    multigenerador = MultiGenerador((
            GeneradorDeOpcionPreestablecida(opciones=('dni', 'le', 'lc'), seed=0),
            GeneradorDeNroDocumento(seed=0),
            GeneradorDePalabrasEspaniol(seed=0, cant_palabras_default=2),
            GeneradorDePalabrasEspaniol(seed=0, cant_palabras_default=1),
            GeneradorDeBarrioCiudadProvincia(),
            GeneradorDeCP(),
            GeneradorDeFecha(seed=0),
            GeneradorDeEntero(0, 9),
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
            "cod_no_deseable",
    )
    generador_csv = GeneradorCSV(multigenerador, headers_csv)
    if process_count > 1:
        logging.info("Iniciando GeneradorCSVMultiprocess")
        generador_multiprocess = GeneradorCSVMultiprocess(
            generador_csv,
            range(0, process_count)
        )
        generador_multiprocess.generar_csv('/tmp/multigenerador.csv', obj_count)
        generador_multiprocess.close()
    else:
        logging.info("Iniciando GeneradorCSV")
        generador_csv.generar_csv('/tmp/uniprocesador.csv', obj_count)
        generador_csv.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if 'DOPROFILE' in os.environ:
        import cProfile
        import pstats
        cProfile.run('main()', 'profile_result')
        p = pstats.Stats('profile_result')
        p.sort_stats('cumulative').print_stats(10)
    else:
        main()
