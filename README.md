utenabi
=======

Generador de datos aleatorios.

Cada item de cada linea generada puede ser:

- enteros,
- decimales,
- booleanos,
- palabras en español,
- ciudades/provincia de USA
- items de archivos CSV.

En cada ejecucion el sistema genera los mismos valores (si se mantiene la estructura de los datos generados).

Ejemplo
-------

El codigo fuente puede verse [aqui](https://github.com/hgdeoro/utenabi/blob/master/src/ejemplos/generador_modelo_tarjeta_de_credito.py).

Para ejecutarlo:

	$ python src/ejemplos/generador_modelo_tarjeta_de_credito.py datos_aleat 100000 100000 100000 900000

Por pantalla veremos la generación de los comercios:

	INFO:__main__:Iniciando generacion de comercios...
	INFO:utenabi.generadores_de_archivos:Ya se crearon 0 instancias de 100000 (0.00%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 2000 instancias de 100000 (2.00%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 4000 instancias de 100000 (4.00%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 6000 instancias de 100000 (6.00%)
	(...)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 92000 instancias de 100000 (92.00%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 94000 instancias de 100000 (94.00%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 96000 instancias de 100000 (96.00%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 98000 instancias de 100000 (98.00%)
	INFO:utenabi.generadores_de_archivos:Se generaron 100000 objetos en 2.76 seg. - Promedio: 36218.82 obj/seg. - /tmp/datos_aleat_comercios.csv
	(continua...)

Lo anterior indica que se genero un listado de *100.000* comercios, a razon de 36.000 filas por segundo.

Luego veremos que se inicia la generacino del CSV con fechas:

	(continuacion...)
	INFO:__main__:Iniciando generacion de fechas...
	INFO:utenabi.generadores_de_archivos:Ya se crearon 0 instancias de 4017 (0.00%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 2000 instancias de 4017 (49.79%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 4000 instancias de 4017 (99.58%)
	INFO:utenabi.generadores_de_archivos:Se generaron 4017 objetos en 0.05 seg. - Promedio: 77889.54 obj/seg. - /tmp/datos_aleat_fechas.csv
	(continua...)

Y ahora se generan las tarjetas, pero esta vez utilizando multiples procesos con currentes:

	(continuacion...)
	INFO:__main__:Iniciando generacion de tarjetas (con infor de personas)...
	INFO:utenabi.generadores_de_archivos:Iniciando proceso 27271
	INFO:utenabi.generadores_de_archivos:Iniciando proceso 27272
	INFO:utenabi.generadores_de_archivos:Ya se crearon 1802 instancias de 100000 (1.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 3802 instancias de 100000 (3.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 5802 instancias de 100000 (5.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 7802 instancias de 100000 (7.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 9802 instancias de 100000 (9.80%)
	(...)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 91801 instancias de 100000 (91.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 93801 instancias de 100000 (93.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 95801 instancias de 100000 (95.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 97801 instancias de 100000 (97.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 99801 instancias de 100000 (99.80%)
	INFO:utenabi.generadores_de_archivos:Se generaron 100000 objetos en 2.86 seg. - Promedio: 34942.08 obj/seg. - /tmp/datos_aleat_tarjeta_con_persona.csv
	INFO:root:Se cargaron 4017 entradas desde /tmp/datos_aleat_fechas.csv
	(continua...)

Y finalmente se generan los cupones (representando 'gastos' realizados por una tarjeta, en una fecha dada, en un comercio dado):

	INFO:root:Se cargaron 100000 entradas desde /tmp/datos_aleat_tarjeta_con_persona.csv
	INFO:root:Se cargaron 100000 entradas desde /tmp/datos_aleat_comercios.csv
	INFO:__main__:Iniciando generacion de cupones...
	INFO:utenabi.generadores_de_archivos:Iniciando proceso 27277
	INFO:utenabi.generadores_de_archivos:Iniciando proceso 27278
	INFO:utenabi.generadores_de_archivos:Ya se crearon 1802 instancias de 100000 (1.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 3802 instancias de 100000 (3.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 5802 instancias de 100000 (5.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 7802 instancias de 100000 (7.80%)
	(...)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 91802 instancias de 100000 (91.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 93802 instancias de 100000 (93.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 95801 instancias de 100000 (95.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 97801 instancias de 100000 (97.80%)
	INFO:utenabi.generadores_de_archivos:Ya se crearon 99801 instancias de 100000 (99.80%)
	INFO:utenabi.generadores_de_archivos:Se generaron 100000 objetos en 1.19 seg. - Promedio: 83827.50 obj/seg.

En este caso vemos que se generaron *100.000* cupones, a razon de 83.000 cupones por segundo.

He incluido un [diagrama de clases](https://raw.github.com/hgdeoro/utenabi/master/diagramas_de_clases.png).

