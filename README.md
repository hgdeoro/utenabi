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

	$ head -n 5 /tmp/personas.csv
	tipo_doc,nro_doc,nombre,apellido,barrio,ciudad,provincia,cp,fecha_nacimiento
	dni,25637979,Encorsetar Cidrera,Asaetinado,Laconismo,Norton,Kansas,7331,19851130
	le,46522288,Raza Silvicultura,Tejano,Pultáceo,Robert Lee,Texas,4417,19840528
	dni,57659895,Cordero Deshilada,Trompillar,Sojuzgador,Belleville,Michigan,2225,19850719
	dni,43222787,Moderna Otilar,Unalbo,Tasar,Mesick,Michigan,1300,19820823
	
	$ tail -n 5 /tmp/personas.csv
	lc,41628571,Atrófico Amelía,Sepia,Duranza,Clifton Park,New York,6445,20010613
	dni,39781852,Desencogimiento Omitir,Chalón,Alabancera,Tucker,Georgia,7085,19830801
	dni,28492040,Horrífico Mimbrear,Escuálido,Denticulado,Blue Ball,Pennsylvania,8688,19891016
	lc,25073845,Entalegada Ceremoniáticamente,Aventador,Chavola,Lake Charles,Louisiana,1212,19781105
	le,40506531,Ababillarse Desacostumbrar,Ambiciar,Autocrítica,New River,Virginia,1198,19940814
	
	$ wc -l /tmp/personas.csv 
	100001 /tmp/personas.csv


