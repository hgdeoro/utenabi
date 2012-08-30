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

Para ejecutar un ejemplo:

	$ python src/examples/generador_personas.py 100000 /tmp/personas.csv 
	INFO:root:Lanzando 2 procesos concurrentes
	INFO:root:Iniciando GeneradorCSVMultiprocess
	INFO:utenabi.api:Iniciando proceso 14679
	INFO:utenabi.api:Iniciando proceso 14680
	INFO:utenabi.api:Ya se crearon 1802 instancias
	INFO:utenabi.api:Ya se crearon 3802 instancias
	INFO:utenabi.api:Ya se crearon 97801 instancias
	(...)
	INFO:utenabi.api:Ya se crearon 99801 instancias
	INFO:utenabi.api:Se generaron 100000 objetos en 3.33 seg. - Promedio: 30012.47 obj/seg. - /tmp/personas.csv

En el ejemplo utilizo la version *multiprocesador* (automaticamente detecta 2 procesadores)
y genero 100.000 personas en 3.3 segs.

