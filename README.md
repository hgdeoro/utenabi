utenabi - Generador de datos aleatorios
=======================================

El objetivo es facilitar la generacion de datos aleatorios, en formato de archivos CSV (separados por comas).

El sitema permite crear columnas con distintos tipos de datos:

- enteros,
- decimales,
- booleanos,
- palabras en español,
- ciudades/provincia de USA,
- items de archivos CSV (o sea, que en cierta columna se incluya un item leido previamente desde un archivo CSV).

En cada ejecucion el sistema genera los mismos valores (si se mantiene la estructura de los datos generados).

Ejemplo: generador_modelo_tarjeta_de_credito.py
-----------------------------------------------

Suponemos que necesitamos crear datos aleatorios para cargar la BD de un modelo multi-dimensional que permita realizar analisis
de consumo de los clientes de una empresa de tarjeta de creditos.

Por lo tanto debemos crear los datos para cargar las siguentes tablas:

![Modelo](https://raw.github.com/hgdeoro/utenabi/master/src/ejemplos/modelo_tarjeta_de_credito.png).

El codigo fuente del ejemplo puede verse [aqui](https://github.com/hgdeoro/utenabi/blob/master/src/ejemplos/generador_modelo_tarjeta_de_credito.py).
El codigo posee muchos comentarios explicando como funciona.

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

Lo anterior indica que se genero un listado de _100.000_ comercios, a razon de _36.000_ comercios por segundo.

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

En este caso vemos que se generaron _100.000_ cupones, a razon de _83.000_ cupones por segundo. (CPU: AMD Turion(tm) II Dual-Core Mobile M500)

Ejemplo 2
---------

El mismo ejemplo, en PC con 8 nucleosi (CPU: AMD FX(tm)-8120 Eight-Core), generamos:

* 1.000.000 de tarjetas de creditos
* 200.000 comercios
* 50.000.000 de cupones (utilizando los 8 nucleos, acanza a generar 297.000 cupones por segundo)

Para lograrlo, ejecutamos:

	$ python src/ejemplos/generador_modelo_tarjeta_de_credito.py millones 1000000 200000 50000000
	INFO:__main__:Iniciando generacion de comercios...
	(...)
	INFO:utenabi.generadores_de_archivos:Se generaron 200000 objetos en 4.30 seg. - Promedio: 46540.71 obj/seg. - /tmp/millones_comercios.csv
	.
	INFO:__main__:Iniciando generacion de fechas...
	(...)
	INFO:utenabi.generadores_de_archivos:Se generaron 4017 objetos en 0.04 seg. - Promedio: 100523.36 obj/seg. - /tmp/millones_fechas.csv
	.
	INFO:__main__:Iniciando generacion de tarjetas (con infor de personas)...
	(...)
	INFO:utenabi.generadores_de_archivos:Se generaron 1000000 objetos en 12.04 seg. - Promedio: 83030.69 obj/seg. - /tmp/millones_tarjeta_con_persona.csv
	.
	INFO:__main__:Iniciando generacion de cupones...
	(...)
	INFO:utenabi.generadores_de_archivos:Se generaron 50000000 objetos en 168.18 seg. - Promedio: 297306.91 obj/seg.

Datos generados
---------------

Estas son las primeras lineas de los CSV generados:

	$ head -n 5 /tmp/millones_comercios.csv /tmp/millones_fechas.csv /tmp/millones_tarjeta_con_persona.csv /tmp/millones_cupones.csv.1
	==> /tmp/millones_comercios.csv <==
	id,numero_de_comercio,razon_social,rubro
	1,85997966,Reverendo Pezpítalo e Hijos,Servicios
	2,78215896,Enrodelada Cojate e Hijos,Servicios
	3,47851442,Garrapatero Encarnadino S.R.L.,Electrónica
	4,33302507,Prejuicio Cristianísima S.R.L.,Electrónica
	
	==> /tmp/millones_fechas.csv <==
	id,fecha,anio,mes,dia
	1,2001-01-01,2001,1,1
	2,2001-01-02,2001,1,2
	3,2001-01-03,2001,1,3
	4,2001-01-04,2001,1,4
	
	==> /tmp/millones_tarjeta_con_persona.csv <==
	id,numero_de_tarjeta,numero_de_cuenta,nombre,apellido,barrio,ciudad,provincia
	1,380065468772,4889389,Encorsetar Cidrera,Asaetinado,Laconismo,Norton,Kansas
	2,556483920173,7406041,Raza Silvicultura,Tejano,Pultáceo,Robert Lee,Texas
	3,155983437996,1258555,Cordero Deshilada,Trompillar,Sojuzgador,Belleville,Michigan
	4,303944692588,8203332,Moderna Otilar,Unalbo,Tasar,Mesick,Michigan
	
	==> /tmp/millones_cupones.csv.1 <==
	id_fecha,id_tarjeta,id_comercio,monto,numero_cupon
	1251,432155,81725,240.01,6076034
	2038,711783,48909,1840.60,7996683
	250,28729,162750,1913.21,8929958
	911,800371,176886,1927.31,9176544

<!--
Carga de datos en PostgreSql
----------------------------

La forma más rápida de cargar datos con PostgreSql es utilizando el comando COPY.

En este caso, el archivo de cupones contenia _125.000.000_ de cupones, tardo _343_ segundos:

	[2012-09-12 18:25:53.726 ART] [utenabi2b] 17031 LOG:  statement: COPY th_cupones from '/tmp/utenabi2b_cupones.csv.1' CSV HEADER;
	(...)
	[2012-09-12 18:31:37.337 ART] [utenabi2b] 17031 LOG:  duration: 343611.864 ms

lo que nos da un promedio de carga de _364.400_ cupones por segundo.

Este se logró bajo las siguientes condiciones:

* Utilizando el comando COPY de PostgreSql
* Utilizando tablas "planas" (sin indices ni FK... estos son creados despues de la carga de datos)
* Los archivos CSV y la particion de PostgreSql estaban en discos separados
* PostgreSql optimizado para carga de datos
-->

Diagramas UML
-------------

He incluido un [diagrama de clases](https://raw.github.com/hgdeoro/utenabi/master/diagramas_de_clases.png).


Licencia del software desarrollado
----------------------------------

GPLv2


Recursos externos incluidos en el repositorio
---------------------------------------------

* _src/utenabi/dicts/cities\_us.csv_: fue bajado desde [https://developers.google.com/adwords/api/docs/appendix/cities\_us](https://developers.google.com/adwords/api/docs/appendix/cities\_us).
* _src/utenabi/dicts/cities\_world.csv_: fue bajado desde [https://developers.google.com/adwords/api/docs/appendix/cities\_world](https://developers.google.com/adwords/api/docs/appendix/cities\_us).
* _src/utenabi/dicts/spanish_: obtenido del paquete _wspanish_ de Ubuntu 12.04 (Licencia: Dominio Público).

