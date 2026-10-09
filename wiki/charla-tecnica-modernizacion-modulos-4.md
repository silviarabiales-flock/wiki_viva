---
type: Fuente de video
title: Charla Técnica Modernización de módulos 4
description: Sesión práctica sobre la migración de la tabla ?XT_ORIGEN_RECAUDO desde Forms al sistema parametrizable, con permisos, Red Code/Ref Code, formatos (Case Restriction), type y paquete, relaciones, campo query, paso 4 de parametrización, vistas, listas de valores y pase de desa a test y a prod.
resource: "Transcripciones/Charla tecnica modernizacion 04.docx"
duracion: "1:54:00"
participantes: []
dominio: ambos
tags: [modernizacion-de-modulos, oracle-forms, migracion, permisos, red-code, ref-code, record-group, lov, case-restriction, type, paquete, campo-query, parametrizacion, vistas, grupo-de-negocio, operatoria-auxiliar, pase-a-produccion]
estado: borrador
calidad_transcripcion: baja
---

# Charla Técnica Modernización de módulos 4

## Resumen
- Se continúa la migración de la tabla `?XT_ORIGEN_RECAUDO` [?] (clave de definición "PXOR2" [?]) siguiendo los pasos del proceso genérico: definición de campos, type (paso 2), paquete con plantilla de query (paso 3), parametrización para consulta/grilla/insert (paso 4) y, cuando corresponda, operatoria auxiliar (paso 5).
- Regla de permisos: hay que dar permisos tanto a la tabla que se migra como a todas las tablas con las que se relaciona (por ejemplo, la de monedas o la tabla de Ref Codes), porque el script de relación los necesita.
- Se explica por qué un descriptivo ("esquema") no traía datos: en Forms la LOV mapea código y descripción mediante Column Mapping y el Record Group, pero el descriptivo nunca se llenaba en el post-query.
- Restricción del generador: una tabla solo puede relacionarse una vez. Si varios campos usan la Red Code, se elige uno solo para la relación automática y los demás descriptivos se cargan después en el paquete.
- Case Restriction pasa a usarse también como formato: MONTO para números con decimales o separador de miles, NUMBER para enteros, UPPER para varchar que deben ir en mayúsculas (claves) y MIXED por defecto.
- "Grupo de negocio": configuración para que un campo sea un link (en azul) a otra pantalla (consulta de póliza, siniestro, productor) usando una clave del tipo ramo/póliza/certificado.
- El indicador "campo query" marca los campos que están en el select del query. Permite que el front ordene y filtre en la base, que es más performante; conviene llevar al query todo lo posible.
- Las listas de valores se arman en el paquete (procedimiento a partir de la plantilla "LOV ejemplo"). Después hay que engancharlas en "lista genérica" e indicar en la definición del campo que tiene lista (A = ayuda, S = solo valores de la lista).
- Pase entre ambientes: se carga en desa, se pasa a test (donde el usuario puede ajustar la parametrización) y de test se genera con `pases_gen` [?] el script de inserts de las tablas de parametrización, que se manda junto con el paquete y el type a prod.

## Temas
| # | Tema | Desde | Hasta | Dominio |
|---|---|---|---|---|
| 1 | Arranque y permisos sobre la tabla migrada y sus relacionadas | 0:02 | 1:50 | tecnico |
| 2 | Descriptivo "esquema" sin datos: LOV, Column Mapping, Record Group y post-query | 1:50 | 8:50 | tecnico |
| 3 | Red Code: nombre, una sola relación por tabla y campos a agregar | 8:50 | 11:02 | tecnico |
| 4 | Alta de campos en la definición: orden, tabla, título, Red Code y sinónimos | 11:02 | 16:39 | tecnico |
| 5 | Grupo de negocio: links a otras pantallas | 16:39 | 19:50 | ambos |
| 6 | Reordenamiento de campos y Case Restriction como formato (MONTO, NUMBER, UPPER) | 19:50 | 25:53 | tecnico |
| 7 | Agregado de los descriptivos faltantes | 25:53 | 29:33 | tecnico |
| 8 | Títulos por defecto y diseño: Forms frente a grilla y vistas | 29:33 | 38:46 | ambos |
| 9 | Alcance: tablas satélite de configuración y pantalla ABM | 38:46 | 41:37 | ambos |
| 10 | Estado de la carga, number/monto y lo que falta (type, paquete, paso 4) | 41:37 | 49:10 | tecnico |
| 11 | Generación del type y del paquete (pasos 2 y 3) | 49:10 | 52:51 | tecnico |
| 12 | Armado de relaciones (join) en el paquete: dominio y low value | 52:51 | 57:41 | tecnico |
| 13 | Completar descriptivos en el paquete copiando el código del Forms | 57:41 | 1:07:16 | tecnico |
| 14 | Prueba del paquete: list type y asignación al type | 1:07:16 | 1:16:09 | tecnico |
| 15 | Campo query y performance de orden y filtro | 1:16:09 | 1:20:55 | tecnico |
| 16 | Paso 4: parametrización de consulta, grilla e insert; operatoria, vistas y permisos | 1:20:55 | 1:28:00 | ambos |
| 17 | Listas de valores en el paquete: plantilla, lista genérica y definición | 1:28:00 | 1:44:36 | tecnico |
| 18 | Edición, pre-update, borrado y tarea para la próxima | 1:44:36 | 1:47:23 | ambos |
| 19 | Paso 5: operatoria auxiliar (tablas padre/hija) | 1:47:23 | 1:49:10 | tecnico |
| 20 | Pase de desa a test y a prod: script de migración de la parametrización | 1:49:10 | 1:53:51 | tecnico |

## Transcripción limpia por tema

### 1. Arranque y permisos sobre la tabla migrada y sus relacionadas (0:02 – 1:50)
[0:02] Se discute si acomodar lo que ya estaba hecho (habría que eliminar los type) o arrancar de cero. Se decide arrancar de cero directamente para no perder tiempo y eliminar lo otro después. [0:30] Este sería el primer paso; si después quieren, lo borran o lo cambian.

[0:30] Pregunta importante: ¿le pusieron permisos a la tabla que están haciendo? [0:58] La tabla a migrar en este caso es `?XT_ORIGEN_RECAUDO` [?] ("Pex t origen recaudos"). Además hay que dar permisos a todas las tablas con las que se vaya a relacionar. Por ejemplo, si la tabla tiene monedas y hay que relacionarla con la tabla de monedas ("contra carta de moneda" [?]), también hay que dar permisos a ese conjunto de tablas relacionadas.

> **Regla:** [1:21] Se debe dar permiso tanto a la tabla que se va a migrar como a las tablas relacionadas con ella. Si no, va a haber problemas en la generación: el script necesita esos permisos.

[1:21] Por ejemplo, con moneda se arma un script con la relación a la tabla de monedas ("cartel de moneda" [?]) y una condición del tipo "código de moneda igual a…", que ellos tienen que completar. [1:50] Hay que verificar todo ese proceso. Los permisos hacen falta para que se pueda armar bien el script de relación.

### 2. Descriptivo "esquema" sin datos: LOV, Column Mapping, Record Group y post-query (1:50 – 8:50)
[1:50] Ya generaron ese dato. Ahora tienen que agregar los campos mirando el Forms y la definición que tienen a partir de… [inaudible].

[2:19] Lo que hicieron el día anterior: sabían que había que agregar campos que vienen de la Red Code, pero con el campo "esquema" veían que no funcionaba. [2:47] En el Forms se ve que el campo de descripción de esquema no tiene ninguna relación: buscaron de dónde viene y no sale de ningún lado, y tampoco tiene LOV. [3:14] Se aclara que en un ítem descriptivo la LOV no está en el propio ítem: se carga en el campo anterior (el código). En este caso el ítem de código tiene la LOV "LOV_ESQUEMA" [?] ("Love esquema"), y a su derecha está el descriptivo de esquema.

[3:42] La LOV de esquema tiene un mapping código–descripción. ¿Por qué entonces no trae datos cuando se consulta? Va a ser algo que les pase bastante.

[4:11] Mientras se comparte pantalla, se menciona una de las restricciones que van a encontrar:

> **Regla:** [4:11] El proceso no puede hacer relaciones sobre la misma tabla varias veces. [4:41] Si se relaciona el campo moneda con la tabla de monedas para obtener la descripción y hay otro campo "moneda dos" que también se relaciona con la misma tabla, eso no se puede hacer desde el script. Después se ajusta a mano. De movida solo puede haber una relación por tabla con el campo que se solicita.

> **Regla:** [4:41] Si hay más de un campo con Red Code, hay que seleccionar uno solo para hacer la relación con la Red Code.

[5:07] Los otros datos se llenan después, como un post-query: un ítem se puede llenar en cualquier momento con el dato que se quiera. Ya se vio y se va a volver a hacer.

[5:32] Normalmente la lista de valores tiene la relación de a dónde va cada campo. Si el ítem tiene lista de valores (acá se llama "LOV esquemas"), hay que mirarla muy bien; es lo que se vio la clase pasada (cómo asignar la lista de valores a los ítems). [6:02] En la LOV de esquema hay una propiedad Column Mapping ("Column Mapy") donde se mapea qué valor va con qué campo. También está el Record Group, que es el select que tienen que copiarse para llevarlo al query: el RG "RG_ESQUEMA" [?].

[6:29] Lo que pasó: se armó la lista de valores con una descripción, pero cuando buscaron no la encontraron porque no se llena en el post-query. Normalmente, cuando se hace una LOV con descripción, después en el post-query hay que ir a buscar el dato y llenarlo, y seguramente acá no se hizo. Por eso nunca pueden llegar a ver de dónde viene. [6:53] En otros campos que tenían Red Code sí lo llenaban en el post-query, y por eso encontraron la relación de todos menos la de descripción de esquema. Pueden hacer la relación para traer el dato con un descriptivo, pero igual después tienen que hacer la lista de valores.

[7:23] Cuando se hizo el Record Group se armó un select con un código y una descripción. El Column Mapping dice que el código va al campo de esquema del bloque origen ingreso y que el descriptivo va a "origen ingreso de SP esquema" (probablemente el ítem `DESP_ESQUEMA` del bloque ORIGEN_INGRESO [?]). [7:52] No lo encontraron porque quien dio de alta el campo se olvidó de la segunda parte, cargarlo en el post-query. Al consultar desde Forms se llenan todos los campos y este queda vacío porque nunca se llena.

[7:52] Qué hay que hacer: buscar la LOV, ver cuál es su Record Group y entrar ahí. Los Record Groups son distintos queries. [8:22] En este caso es "RG_ESQUEMA" [?], y ahí está el query que deberían copiarse tal cual. Las columnas se llaman código y descripción, que son los alias que se les puso (como lo que hacían cuando entraban a la Red Code y ponían código y descripción), junto con origen ingreso.

### 3. Red Code: nombre, una sola relación por tabla y campos a agregar (8:50 – 11:02)
[8:50] Las Red Codes normalmente tienen que llevar el nombre de la tabla. A veces no lo tienen, pero además deberían llevar el nombre del campo al que hacen referencia. Ahí aparecen, por ejemplo, las que van a cajero o a productor.

[8:50] Como la Red Code puede ir una sola vez en la definición, [9:19] y todos estos campos (incluido el de lavado) salen de la Red Code, eligen uno solo cuando tengan que poner la tabla en el campo. En ese campo ponen la tabla Red Code; en el resto, null, igual que en otros descriptivos. [9:45] Después se les explica cómo llenarlos. Cuando el proceso detecta que ya se hizo una relación con esa tabla, no arma otra.

[9:45] Se repasan los campos con Red Code: lista pro, descripción lista caja ("lista caja TSP" [?]), descripción lista pro, etc. [10:14] Esto pasa mucho porque, como se dijo:

> **Regla:** [10:14] Si un campo tiene distintos valores fijos, siempre va a la Red Code para no generar una tabla con esos valores.

[10:14] Se vuelve a revisar los campos de la definición "PXOR2" [?] ("pexo r dos"). [10:43] Hay 6 campos a agregar; los 6 salen de la Red Code y solo a uno se le pone la tabla. El primero a agregar es "desc lista pro" (descripción de lista pro), que va al lado de lista pro.

### 4. Alta de campos en la definición: orden, tabla, título, Red Code y sinónimos (11:02 – 16:39)
[11:02] Se ofrece borrar las partes y que ellos llenen los alias, pero igual falta agregar el paquete, que todavía no se ejecutó: todavía no está el paso cuatro. Por eso se trabaja ahora sobre la definición "PXOR2" [?]. El nuevo campo va en la posición 7: [11:31] a los campos con orden mayor a 7 se les suma uno con un update sobre la definición ("cejo_" [?]). Hubo un error de tipeo con el guion bajo y se corrige. [12:04] Una vez corridos los mayores a 7, el nuevo queda en 7 y el que antes era 7 pasa a 8. A ese le ponen la Red Code.

[12:33] Columnas que se completan al insertar el campo: nombre de tabla (la tabla de origen, `?XT_ORIGEN_RECAUDO` [?], con todo lo que corresponde), después el nombre y después el título. [13:02] El título se puede cargar ahora porque se está insertando uno nuevo; en el resto, por ahora, null, y después se cargan todos juntos. Siguen el tipo, el orden y la longitud. [13:31] En la última columna va el nombre de la Red Code: "CG Red Code", que es el nombre de la tabla (`CG_REF_CODES` [?]). Se recomienda copiarlo de otro registro que se sepa que funciona.

[14:02] Hay que tener permisos sobre `CG_REF_CODES` [?] ("CG rescover"). Los tienen porque se los puso el instructor, pero siempre tienen que verificarlo porque se está haciendo una relación. El valor va entre comillas simples y en mayúsculas. Se pregunta si se antepone el esquema ("conevalse" [?]).

[14:25] No hace falta: van a encontrarse con tablas que están en otros esquemas y para eso se usa el sinónimo. Todas las tablas del esquema "valsec" [?] tienen sinónimo para que se puedan referenciar desde cualquier lado, independientemente de dónde estén. Un sinónimo es un nombre "de fantasía", normalmente igual al de la tabla, que se usa desde esquemas distintos de "valsec" [?]. [14:54] Por ejemplo, si desde el esquema del sistema se quiere ir a `?XT_ORIGEN_RECAUDO` [?], primero se busca si existe una tabla con ese nombre en ese esquema. Si no, se busca un sinónimo que la referencie. Si no hay permiso, no deja.

> **Regla:** [14:54] Un sinónimo no da acceso, solo referencia: igual hacen falta los permisos.

[15:27] Se verifica la carga: tabla y nombre del campo (la PK no). Si están cargando la Red Code, el nombre del campo hay que cargarlo y hay que sacarlo de la Red Code: ir al query de la Red Code y ver de dónde obtiene el dato. [15:52] Se copian ese dato y se traen el query tal cual está. [16:10] El campo es `RV_MEANING` [?] ("RB maining"): es el campo de la tabla que se llena con la Red Code.

> **Caso especial:** [16:10] El campo de la Red Code es casi siempre el mismo (`RV_MEANING` [?]). Hay casos muy especiales en que puede ser otro, pero el 99% es ese. Igual hay que verificarlo.

[16:39] Se carga entonces el campo de la Red Code. El campo origen no; va el de consulta. Después viene un null para grupo de negocio.

### 5. Grupo de negocio: links a otras pantallas (16:39 – 19:50)
[17:08] El grupo de negocio todavía no se había explicado. Se usa cuando se crea un campo que va a ser un link para ir a otra pantalla. Por ejemplo, ya existe el grupo de negocio "póliza"; el instructor lo probó y funciona.

[17:28] Ejemplo: en una tabla está la póliza y se quiere que al hacer clic vaya a la consulta de póliza, que está en otro lado y tiene una URL determinada. Eso se va a poder implementar desde acá con un grupo de negocio, que se va a llamar "grupo negocio póliza" y va a tener su propio comportamiento. Va a haber un grupo siniestro que lleve a siniestro, [17:55] un grupo productor que lleve a la consulta de productor, etc. Se van a armar distintas configuraciones para ir a las distintas pantallas.

[17:55] En pantalla el campo aparece en azul y su contenido lo llena el programa. [18:24] Se ve la clave con la que va a buscar. Por ejemplo, para grupo póliza se ve algo como "4/número/0", que es ramo/póliza/certificado. Para siniestro la clave tiene otros valores (serie, ramo, siniestro). Cada grupo tiene su propia configuración de clave, y se muestra en azul.

[18:54] Cuando el usuario hace clic, se llama a un servicio propio que le dice a dónde tiene que ir y lo lleva solo. Con eso se va a poder ir integrando el sistema con otros. [19:20] Ya está hecho en "Orion" [?]: cuando se busca una póliza se puede ir a la consulta.

[19:20] (Pausa breve; charla sobre el mouse y la pantalla.)

### 6. Reordenamiento de campos y Case Restriction como formato (MONTO, NUMBER, UPPER) (19:50 – 25:53)
[19:50] Siguen con la lista de caja, que ya estaba hecha. Su descripción entra en la posición 9, así que hay que correr todo de la 10 en adelante para cambiar el número de orden. [20:22] Se insertan los otros campos. El 10 ya tiene la tabla, así que a ese no hay que ponérsela. [20:49] Otro campo (ubicación [?]): varchar 100, null.

[20:49] Se va a agregar también un formato para los numéricos. Si el campo es varchar, pueden poner MIXED ("Apple mix"). [21:17] Si es numérico y es un monto (un número con decimales, o se quiere separar los miles), lo indican en el formato. El campo se llama Case Restriction (el que en Forms muestra "mix"), y ahí ponen MONTO. [21:43] En numéricos va MONTO o NUMBER [?] ("van Amber"). Se puede poner cualquier valor, pero en mayúsculas. Se cree que después hay una lista de valores asociada, buscada en la Red Code. [22:04] Hay que actualizar los numéricos. Esto apareció hace 2 días, cuando se empezó a dar formato a los montos; por eso no lo sabían.

> **Regla:** [22:29] A grandes rasgos, los números sin decimales (enteros) llevan NUMBER y los que tienen decimales (dos, cuatro…) llevan MONTO. El front interpreta MONTO como "esto es un monto" y le pone separación de miles y decimales. NUMBER es un entero sin separadores.

[22:29] El motivo: había un problema con números que no son montos, porque les aparecían las comas. [22:59] Por ejemplo, el número de asiento (algo como 101020230102) se necesita tal cual; si aparece una coma cada 3 dígitos, se pierden. Por eso se empezó a dar formato. También apareció la necesidad de que algunos campos aparezcan sí o sí en mayúsculas, que es el caso de las claves.

> **Regla:** [22:59] Un varchar que es parte de la clave primaria lleva UPPER ("Apple"/"APP") en Case Restriction, para que quede en mayúsculas.

[23:27] Por defecto el valor se carga igual para todos, y ellos van a tener que definirlo. En este caso la PK es number, así que lleva NUMBER, no MONTO. [23:57] Number sin decimales → NUMBER; con decimales → MONTO. Nivel de permiso y grupo recaudador también son NUMBER. En esta tabla todos son NUMBER; no hay ningún monto.

> **Caso especial:** [24:22] "Ingresos mensuales" es un número entero, así que por ahora va NUMBER. Si después el usuario quiere que un entero muestre separador de miles (por ejemplo, porque es una cantidad muy grande), se le pone MONTO y se separa con comas.

[24:50] El instructor quiere que entiendan la lógica: por qué apareció, para qué es y cómo se ve en el front. [25:30] Todos van en mayúscula (MONTO, NUMBER). Lo demás se representó igual que en Forms para que, si ven algo en Forms, lo pasen acá sin ninguna conversión. [25:53] En Forms la propiedad Case Restriction aparece como MIXED.

### 7. Agregado de los descriptivos faltantes (25:53 – 29:33)
[25:53] Faltaba agregar el campo 10, que era una descripción; lo demás ya estaba en null. [26:24] ¿Hay que sacarle la Red Code? No: la Red Code solo se le puso al número 8, no al 10. Se sigue con el campo de lavado; el código está en la posición 21. [26:52] Hay que actualizar todos los mayores a 21. Queda el número 12, que había quedado mal.

[27:20] Se agrega al final un campo que no tenía ningún lado. Era el vacío que no habían encontrado (se cree que en la 29): grupo recaudador. [27:48] Se lo agrega como 29.

[27:48] Observación sobre el Forms: no entró todo en la pantalla, así que algunos campos se pusieron arriba y se van mirando al pararse en el registro, porque no se puede correr a la derecha. Cuando terminen, una cosa que se puede hacer es mostrarle esto al usuario y ofrecerle alguna vista resumida para ciertos casos.

[28:17] Siguen: el 12 es "ind gen cobranza" [?] ("12 eje en cobranza") y se le agrega "desc cobranza". [28:47] El campo 27 es "esquema de trabajo" y se le agrega "desc esquema". Se actualiza y se agrega. [29:15] Se guarda.

### 8. Títulos por defecto y diseño: Forms frente a grilla y vistas (29:33 – 38:46)
[29:33] Ya están todos los campos. A diferencia de la primera vez, ahora tienen la tabla y el nombre del campo. Falta poner los títulos por defecto. [30:01] Se pregunta si no es más fácil hacerlo desde la pantalla de parametrización ("rector" [?]). No, porque todavía no se creó; una vez creada sí se puede, pero hay que hacerlo para el insert, para el update y para lo demás. Es más sencillo cargarlo en la definición, así ya se crea bien. La clave de la definición es "PXOR2" [?] ("P X O R P X_ dos").

[30:31] Van a la pantalla de parametrización (un Forms). El instructor tiene que arreglar ahí el Case Restriction, porque antes tenía lista de valores y tiene que agregar los valores nuevos. Todavía no hay nada cargado para esa definición, pero sí los campos. La pantalla es "FDQM70000" [?] ("QM 70000", "FDQMEP"). [31:01] Se consulta con Enter Query / Execute Query por "PXOR2" [?].

[31:26] En la parte de abajo están los campos, y ahí es más fácil cargar los títulos. Por ejemplo, origen: pueden ponerle solo "Código". Mirando la pantalla vieja tiene que reflejar más o menos lo mismo, porque el título va a decir "origen" en inglés [?]. [31:52] Ponen código, descripción, origen, etc. [32:23] "Descrip corta": en el Forms está en dos renglones y acá no hay dos renglones. [32:52] Comisión cobranza: en Forms dice "IN COM Cobras" [?]. [33:18] Hay una sigla y otra "sigla navegación" [?]. [33:56] Como no aparece en la pantalla, le ponen "sigla nav" [?] solo para saber qué es. Después, en la vista, figura lista pro.

[33:56] Duda planteada a Martín: en la pantalla vieja hay un cuadro con varios campos arriba y una grilla abajo; ¿cómo se ubica eso acá? [34:24] ¿Se puede representar lo más parecido posible, por ejemplo campos a la izquierda y grilla a la derecha? [34:54] Respuesta: va a ser una vista con todo uno al lado del otro. Recuerdan una prueba anterior del dinámico, donde aparecían todos los campos a la izquierda y la grilla a la derecha.

[35:21] En Forms se pusieron campos arriba porque Forms no puede seguir corriendo la grilla a la derecha y al usuario no le gusta tenerla toda a la derecha. Es una manera de resumir. A los usuarios tampoco les gusta así; preferirían columnas, como está abajo. A veces se ponen solo los descriptivos y no los códigos. No se va a representar igual que el Forms.

> **Regla:** [35:21] Para el sistema nuevo todo es una grilla: cada uno de esos campos es una columna más de la grilla. Después las vistas definen cuántos campos se ven en una u otra. [35:50] A nivel de edición se pueden armar grupos; el usuario va a estar parado en un solo registro y va a ver y editar lo que corresponda, pero no se replica el layout del Forms.

[36:11] Ese layout fue una consecuencia de que el usuario no quería moverse con tantas columnas a la derecha y quería ver de un vistazo todos los datos al pararse en un registro. [36:40] Siguen con los títulos: lista pro, "desc productor" para que no se choque, lista caja, "desc caja". [37:08] Tipo de cierre ("TP cierre"): quinta columna de la grilla. Ingen cobranza [?] ("5 Granza").

[37:46] Comentario: ahora parece tedioso cargar todos estos campos, pero hacerlo a mano implicaría el front campo por campo, el backend y la base de datos. Acá ya están, indirectamente, preparando el frontend (qué se va a ver a grandes rasgos) y armando las distintas capas. [38:15] Mostrar, mostrar… (se menciona "self regco" [?], ininteligible).

### 9. Alcance: tablas satélite de configuración y pantalla ABM (38:46 – 41:37)
[38:46] Pregunta a Martín: ¿con qué área o pantallas se va a arrancar? No se sabe todavía; se supone que con administración, que lo tiene más claro. Hay muchas de "ART" [?].

[39:14] El objetivo inicial es hacer todas las tablas satélite de configuración: tablas simples que se van mejorando y a las que se agregan cosas. Lo primero sería relevar las tablas de configuración como esta, que alimentan a otras: origen ingreso, moneda, tasa de cambio, tipo de movimiento, todo lo que sea mantenimiento de datos. [39:48] Hay unas cuantas.

[39:48] Ironía: aprenden Forms aunque ya no se use. La pantalla ABM que están usando para la definición también se va a migrar en algún momento: es la "FDQM70000" [?]. [40:12] Tarde o temprano se va a migrar para dar toda la configuración desde el sistema nuevo. Esa pantalla es compleja: hay que separar si es usuario común (podrá modificar algunas cosas) o programador (por permiso podrá modificar más). [40:38] Ahora está muy rústica porque necesitaba salir y que ellos puedan ver todo. Si se elige una operatoria arriba, se pueden cambiar algunos campos, no todos. Habría que acomodarla; es una migración directa.

[41:06] Hasta que no esté todo (por ejemplo, recién se agregaron los montos y después se agregan campos nuevos e indicadores) no tiene sentido ponerse a migrar esa pantalla. Primero hay que acostumbrarse a esto.

### 10. Estado de la carga, number/monto y lo que falta (type, paquete, paso 4) (41:37 – 49:10)
[41:37] (Se recorren "lista hoy" [?] y "lista compañía".) [42:20] Otra tabla, más larga, con muchos campos: donde dice "tabla de origen" está vacío. Ahí correspondería la Red Code, pero no debería aparecer ahí. [42:45] Fragmento poco claro sobre que solo puede consumirse una vez y sobre las dos maneras de completar las restantes [inaudible].

[43:34] Se graba y, si se consulta la tabla, tendrían que estar los registros. [44:03] ¿Eso ya se debería ver en el front? No, todavía no. Falta correr los type, que son la comunicación con el backend web. Faltan los paquetes, donde están las validaciones. Una vez creado el paquete hay que armar el query (ya viene armado, pero ellos tienen más relaciones). [44:29] Después viene el paso cuatro, que inserta todos los valores en tabla. Recién ahí el backend web puede ver algo. Hasta entonces no aparece nada en el front.

[44:57] Con todos los campos cargados hay que actualizar lo que es NUMBER y MONTO. En esta tabla todo es entero: código de origen, nivel de permiso, ingreso mensual, día de ingreso diario, recaudador. Por eso se puso NUMBER a todo. También se puede hacer desde la pantalla de parametrización.

[45:28] La lista de valores del Case Restriction todavía no tiene MONTO para seleccionarlo, pero ya lo pueden agregar en la Red Code (ya saben cuál es).

[45:57] Siguen con los type. [46:19] Mientras se corre el type (unos 2 minutos): después hay que crear el paquete y meterse en el query del paquete para acomodarlo.

[46:49] (Charla personal sobre vacaciones y licencias por nacimiento; se omite.)

### 11. Generación del type y del paquete (pasos 2 y 3) (49:10 – 52:51)
[49:10] Corrió el TYPE: ya está creado. [49:38] Se entra al type, que es el de lista: está la especificación y el body. Ahí están todas las asignaciones del dato de un lado a otro.

> **Regla:** [50:09] Es importantísimo no saltearse campos. Aunque algo no se vea en el Forms, por lo menos hay que generar el campo. Ejemplo: cantidad de actualizaciones y cantidad de digitalización. Se verificó que se crean por defecto y están como NUMBER.

[50:37] El paso dos ya se corrió y se generó todo. Sigue el paso 3: el paquete con plantilla de query, que se genera con los campos y los nombres que se pusieron. [51:01] Se ingresa la clave "CJ…" [?]. Corre bien. Después de correr el proceso, se busca el script generado y se ejecuta. [51:46] Faltaba una comilla.

[52:13] Apareció un problema en desa ("Endesa") que todavía no está en test: lo nuevo de los montos dejó de andar en test y hubo que hacer un ajuste. Se corre y ya está el paquete de "PX 2" [?].

### 12. Armado de relaciones (join) en el paquete: dominio y low value (52:51 – 57:41)
[52:51] Se refresca y se busca el select del paquete. Pregunta: ¿en este select hay que poner la Red Code para todos los demás campos?

[53:20] Hay dos maneras:
- Ponerlo en el FROM, lo que implica cambiarlo y es bastante complejo.
- Como se dijo en la clase anterior, copiar los códigos de las Ref Codes y ponerlos abajo.

Primero se arma la relación que hicieron, que fue solamente con la Ref Code, no con ninguna otra tabla. En la parte del FROM, ¿qué dominio es? [53:50] El dominio lo tienen escrito en el query (de dónde sale). Cuidado: tiene doble comilla. [54:19] Después hay que poner el valor: el campo del código que se busca. En el query aparece con dos puntos.

[54:49] Ahí están armando la relación, no el dato (el dato ya lo pusieron). Hay que ver cuál es el dominio y cuál es el low value ("low valver"; `RV_LOW_VALUE` [?]). Se pone el nombre del campo sin los dos puntos. [55:14] Siempre ponen un numeral para indicar qué hay que llenar. Va siempre el nombre de la tabla (alias). [55:32] Lo que arman es la relación: el WHERE que tienen en el Forms es el WHERE que hay que hacer acá. Una condición es el dominio y la otra es el código, que indica contra qué dato de la tabla se hace la relación.

[55:57] Si quisieran armar otra relación a la misma tabla, tendrían que copiar todo el bloque de arriba (donde dice `CG_REF_CODES` [?]), ponerle "CG_REF_CODES 2" [?] y agregarlo en el FROM. No se justifica; se hace algo más fácil. Eso se haría para cada descripción que se necesite, no por cada tabla.

[56:22] En este caso es una misma tabla, así que eligen solo una relación y las otras se cargan a mano. Si en la definición hay otra tabla, aparece otro join en el FROM con el nombre de la otra tabla (se vio con el ejemplo de monedas).

> **Regla:** [56:48] Al generar un campo descriptivo siempre se indica la tabla a la que pertenece el campo. Ejemplo: para la descripción de la moneda se agrega un campo nuevo, se pone el nombre de la tabla de monedas y el nombre del campo de descripción. [57:12] Así el join se arma solo y después hay que completarlo.

[57:12] Bajando en el paquete aparecen todos los campos que se inicializan.

### 13. Completar descriptivos en el paquete copiando el código del Forms (57:41 – 1:07:16)
[57:41] Los campos se inicializan con el query. En el select hay algunos que dicen null y el nombre del campo: son los que faltan llenar. Lo que hay que hacer es copiar lo que está en el Forms, hacer el mismo select acá y hacer el INTO al dato que corresponde.

[58:08] Se toma el segundo descriptivo en el Forms y se copia tal cual: todo el BEGIN … EXCEPTION, para que si hay algún error quede nulo. [58:35] Se pega abajo del campo correspondiente (buscar "lista caja"). Falta el código: [59:05] hay que reemplazar los dos puntos (referencias a ítems del Forms) por "LR Move" [?] (la variable del registro en el paquete).

[59:30] La asignación a nulo anterior se puede comentar o dejar, porque después se pisa. Queda como referencia.

[1:00:01] Sobre las excepciones: si no lo encuentra, se asigna nulo; queda a gusto. Falta el TOO_MANY_ROWS ("tu money rock"), que debería estar porque el dominio puede estar mal escrito. [1:00:22] Habría que tener el WHEN NO_DATA_FOUND ("no data Fund") y además un WHEN TOO_MANY_ROWS, porque dominio más código no es clave primaria. Se deja para después.

[1:00:22] Sigue el descriptivo de cobranza: se copia tal cual del Forms. [1:01:34] Indicador de lavado: está en la línea 258 [?] del Forms; se pone abajo. [1:02:42] En la línea 273 [?] estaba el de esquema, que hay que ir a buscar al Record Group.

[1:03:08] En el Forms hay uno más: "desc medio de pagos". Está hecho de otra manera. Comentario de performance: lo óptimo sería hacer el join de todas estas, pero por ahora les conviene hacerlo así porque queda más claro y más representativo de cómo trabaja Forms. [1:03:41] Hubiera sido mejor hacer todo en el query.

[1:03:41] Grupo recaudador no tiene descripción. [1:04:06] Medio de pago estaba al final: se agregó en el último lugar.

> **Regla:** [1:04:30] El orden es tan importante como estar todos los campos. No hay que alterar ningún campo; es donde más atención tienen que prestar.

[1:05:28] Falta el de esquema, que hay que traer del Record Group. Sería una mejora, porque en la pantalla vieja no funcionaba. [1:05:57] Se lo olvidaron de poner en su momento. [1:06:19] Lo que hay que hacer: tomar uno de los bloques ya pegados (para mantener el BEGIN/EXCEPTION, que en el Record Group no está) y cambiarle el query. [1:06:46] Lo que cambia es el dominio: se pone el dominio de esquema, se completa y queda "esquema de trabajo". Se guarda.

### 14. Prueba del paquete: list type y asignación al type (1:07:16 – 1:16:09)
[1:07:16] Cuando lo tengan armado, avisan y el instructor lo revisa. [1:07:43] En el paquete están todos los campos.

> **Regla:** [1:07:43] Si se agrega un campo nuevo a la tabla, también hay que agregarlo a mano en el paquete.

[1:07:43] En el paquete hay "lista movimiento query" y "lista movimiento JSON": la segunda manda directamente el JSON con la lista de movimientos. Los parámetros (nombre, operatoria, texto adicional…) todavía no tienen nada porque solo se acomodó el paquete. [1:08:09] El nombre de la operatoria aparece cuando se agregan las tablas de la vista (OP).

[1:08:09] ¿Se puede ejecutar para probar si funciona o si quedó algo mal? Sí, aunque si trajera 2.000.000 de registros no conviene. [1:08:34] Es una función que devuelve un list type: cuando armaron el type y el tipo lista, el list type "simula una tabla". El front lo recibe como JSON. Para probarlo se hace un `select * from table(` y se llama a la función con los parámetros (la primera, no la de JSON).

[1:09:04] Se ejecuta con todo nulo: trae origen, descripción, sigla, descripción corta, lista pro, "no mostrar"… Así se ve si acertaron. Descripción de ingen cobranza [?] no trae nada, aunque el código tiene dato. [1:09:33] Habría que ver si la descripción está en otro dominio. Descripción de medio de pago tampoco trae nada.

[1:10:02] Hay que mirar qué falta o por qué no traen la descripción, ejecutando la consulta en la Ref Code en desa. A veces en desa no hay datos, o los borran.

[1:11:13] Encuentran el problema: los datos del cursor se cargan en el type campo por campo. [1:11:34] Ellos asignaron el valor a la variable LR, pero nunca lo pasaron al type, así que nunca se ve. Lo que hay que cambiar es asignarlo al campo del type. [1:12:02] Esa es la forma de probar si anduvo: con el select.

[1:12:34] Uno solo comparte y modifica el paquete, para no romperlo entre varios. Se corrige la asignación en "L_TYPE_REG" [?] ("L Type REG").

> **Regla:** [1:13:36] El valor se asigna campo por campo al type, y el type es el que devuelve el dato. No alcanza con cargarlo en una variable.

[1:14:12] Se ejecuta de nuevo. [1:14:45] Da error y se corrige. Aparecen descripción lista pro y descripción lista origen.

[1:15:09] Duda: antes no andaba cobranza, pero sí la descripción de "no mostrar". Era la que se generó sola: la relación directa con la Red Code generada por el proceso anda. [1:15:38] Con 3 o 4 tablas relacionadas hay que revisarlo porque se complica. La primera anduvo porque se hizo con otro método, en el WHERE.

### 15. Campo query y performance de orden y filtro (1:16:09 – 1:20:55)
[1:16:09] Alternativa: armar todo en el FROM del query (origen ingreso más la Red Code varias veces con alias 1, 2, 3), pero se vuelve un lío. [1:16:38] Por eso se simplificó así. Total, el Forms trabaja así y es una tabla chica. Sería más performante en el query, pero así funciona perfecto.

[1:16:38] Lo que cambia es esto: en la definición de tablas hay un campo que indica si el campo está en el query o no. [1:17:07] Desde el front, cuando el usuario quiere ordenar por algún campo desde la pantalla:
- Si el campo está en el query, mandan el texto del query con el ORDER BY y lo resuelve la base, mucho más performante, porque reciben el dato ya ordenado.
- Si no está en el query (se llena aparte en el paquete), tienen que ejecutar todo y recién después ordenar, porque reciben todo.

[1:17:37] Para eso es el campo: mejora la performance. [1:18:00] Si se quiere ordenar por origen, que está en el query, se pone ORDER BY origen; lo mismo para descripción, productor, indicador de cobranza, etc. Todo orden y filtro se puede hacer sobre lo que está en el query. Lo que no está en el query (porque el select tiene null para ese campo y se llena después) no se puede ordenar ni filtrar así.

> **Regla:** [1:18:28] A los campos que están en el select del query (incluidos los que vienen por join) se les marca "campo query". A los descriptivos que se llenan aparte, no. [1:19:26] Siempre hay que tratar de llevar todo lo posible al query; es muy importante para la performance del front.

[1:18:56] Ejemplo: si con moneda se hace el join en el query para traer la descripción, se marca campo query. Si se busca abajo en el paquete, no, y es menos performante. [1:19:26] En esta tabla se marca solo el primer descriptivo (descripción de lista pro), que vino por join. [1:19:56] Al marcarlo, el registro estaba bloqueado por otro usuario; luego se pudo.

[1:20:27] Normalmente, si hay un join y el dato tiene primary key, se puede llevar al query; si es complejo, se saca. [1:20:55] Lo habitual (producto-descripción, banco-descripción, etc.) se puede poner en el query.

### 16. Paso 4: parametrización de consulta, grilla e insert; operatoria, vistas y permisos (1:20:55 – 1:28:00)
[1:20:55] Repaso de lo hecho: se definieron todos los campos, el type, el paquete y los joins y relaciones; ya se traen todos los datos. [1:21:24] Falta el paso cuatro: completar la tabla de parametrización para consulta, grilla e insert.

[1:21:24] Pregunta: ¿los permisos se pueden ajustar después? Sí. Por ahora se pone 000 para poder trabajar; después se agregan los que se quieran. [1:21:52] Se corre el paso con la clave "PXOR2" [?] ("P chor dos"). Hace commit.

[1:22:27] En la pantalla ya aparecen la vista, la operatoria y la grilla. A partir de ahí empiezan las configuraciones. [1:22:53] Hay que asignarle una operatoria; si no aparece "general" es porque hay una operatoria general. Más adelante se van a generar operatorias por sector o grupo. Por ahora se pone "general", [1:23:23] aunque en realidad corresponde poner la que se esté usando, cuando el usuario arme sus grupos.

[1:23:23] Se mira la definición de la vista ("el BI" [?]): qué campos se muestran, cuáles son visibles y navegables. Había algunos que no se veían. [1:23:52] La navegación se puede sacar. Está el orden en que se muestran. El instructor haría dos vistas, pero eso lo define el usuario: una más restrictiva, para quien quiere ver algo acotado.

> **Caso especial:** [1:24:22] Conociendo el negocio: hay usuarios que, aunque tengan permiso, solo modifican 4 o 5 datos (los que conocen), y otros que modifican más. Puede convenir una vista restrictiva con solo lo que necesitan, para que editen sin el lío de toda la grilla.

[1:24:50] Se abre la pantalla nueva para ver los datos. [1:25:35] Aparecieron solo 8 registros porque había un valor por defecto de cantidad; se pone 12. Si no está cargado, no anda. Hay que refrescar todo.

[1:26:04] Ya están todos los datos en orden. Se pueden tener dos vistas: quien quiere ver el nivel y el grupo, que están al final, usa otra vista. Pueden ser vistas por nivel (resumida, nivel 1, nivel 2), cada una con su permiso.

[1:26:34] Botones del costado: clonar y editar. No aparece borrar porque en la lista de permisos no se le dio permiso de borrado. En este caso está bien, porque no se debe poder borrar. [1:27:01] Insertar quedó con permiso 0 (no se encontró cuál correspondía); editar (update) tiene permiso 33 [?]. [1:27:29] Al entrar a editar no aparece nada: la definición de edición del paso cuatro está vacía, no hay ningún campo visible para editar. Así como no aparece borrar sin permiso, sin campos visibles no hay nada para editar.

### 17. Listas de valores en el paquete: plantilla, lista genérica y definición (1:28:00 – 1:44:36)
[1:28:00] Lo que les queda es mirar cuáles campos son editables y cuáles no. Como mínimo tienen que hacer las asignaciones de listas de valores: cada lista de valores que tiene el Forms hay que armarla en el paquete, porque se usa en el alta o en la edición. [1:28:26] Cuando el usuario modifica el campo, tiene que aparecerle como en el Forms.

[1:28:26] Con eso ya está toda la configuración y el usuario puede empezar a usar la tabla. Con permisos puede consultarla, pero no editarla hasta que se definan qué campos puede editar; eso lo tiene que dar el usuario.

[1:28:48] Por ejemplo, al editar el productor tiene que aparecer la lista de valores de productor, porque en el Forms está. Por eso hay que tenerla armada. Después hay que recorrer los validadores que tiene cada campo en el Forms. [1:29:13] Hay que mirar el Forms, ver qué se valida en cada campo y saber en qué punto ponerlo. Era lo que se iba a ver hoy, pero queda para después.

[1:29:43] Se arma una lista de valores en el paquete. En la especificación hay un procedimiento "lista genérica". [1:30:14] Recibe el nombre del campo de validación y con eso arma la lista. En el body, un poco más arriba, está "LOV ejemplo plantilla", que es un ejemplo de lista.

[1:30:44] Pasos:
1. Copiar la plantilla completa y pegarla abajo.
2. Cambiar el nombre "LOV ejemplo" por el de la lista que se quiere hacer; se elige la de productor ("des pro"). [1:31:13] El nombre va también abajo.
3. Cambiar el query.

[1:31:40] El query se saca del join que ya se había hecho para la descripción de lista pro. [1:32:06] Se lleva así, en este caso sin excepción. En la plantilla está el formato con un ejemplo de moneda y una asignación al type; [1:32:31] arma lo necesario para el JSON.

[1:32:31] Al select hay que agregarle código y descripción: `RV_MEANING` [?] con alias descripción. Además falta el código: el INTO se va y el low value (`RV_LOW_VALUE` [?]) pasa arriba en el select, como código. [1:33:00] Normalmente va primero el código y después la descripción, pero el orden no importa si se ponen los alias. [1:33:31] La diferencia es que antes ya se tenía el código y había que traer la descripción; ahora hay que mostrar una lista (código 1 con su descripción, código 2 con la suya…) para que el usuario elija. Con el query listo está el 90% hecho.

[1:34:02] Falta asignar a qué campo va el código y a cuál la descripción. Eso también está en el Forms. En el display se indica qué se le muestra al usuario: normalmente código y descripción. [1:34:32] Después se indica en qué campo va el código: no es el alias, es el nombre del campo destino ("LM campo"). [1:35:01] Se busca en la especificación del TYPE: el código que elige el usuario es lista pro. [1:35:21] El usuario se para en lista pro y le aparece la lista. Al seleccionar, el código va al campo lista pro y la descripción al campo de descripción de lista pro.

[1:35:21] Repaso:
1. Conseguir el query con código y descripción.
2. [1:35:51] Definir el display: lo que ve el usuario en el combo (código, un guion y la descripción).
3. Indicar que, al elegir, el código va al campo lista pro y la descripción al campo "DESP lista pro" [?].

[1:36:20] ¿Ya aparece la lista al editar? No, porque en editar no se hizo nada: no se pusieron campos visibles. [1:36:46] Se ponen varios campos visibles, los primeros arriba. Más adelante se explica cómo agrupar con contexto de agrupación. [1:37:17] Se marca editable lista pro. También se puede marcar requerido para que no quede nulo; en este caso puede ir nulo. [1:37:41] La descripción no se edita: se pone el código y la descripción se completa sola.

[1:38:19] No aparece modificar: los campos estaban como no navegables, así que no dejaba modificarlos. [1:38:46] Se corrige; el cambio se toma al salir y volver a entrar. [1:39:15] Ahora aparece lista pro, pero no la flechita de la lista.

> **Regla:** [1:39:15] No alcanza con definir el procedimiento de la lista: hay que engancharlo. [1:39:41] En "lista genérica" hay un IF por nombre del campo ("nombre campo valida"). [1:40:04] Ahí hay que agregar que, si piden el campo tal, se llama al procedimiento de la lista correspondiente.

[1:40:33] Se agrega la condición con el nombre del campo y la llamada al procedimiento (en la línea 842 [?] del paquete). [1:41:03] Se compila. Se comenta que se podría hacer más prolijo (con el nombre del atributo JSON y la flechita), pero no importa. [1:41:28] Al recompilar el paquete, la pantalla da error hasta que se actualiza varias veces. [1:41:55] Sigue el mismo error; se prueba Ctrl+F5 por si quedó en caché. [1:42:25] Se revisa que el nombre del campo sea lista pro y no el descriptivo. [1:42:49] Se revisa la actualización GR [?] (línea 826 [?]) y el parámetro "nombre campo a validar".

> **Regla:** [1:43:17] Además hay que indicar en la definición del campo, en la pantalla de parametrización, que tiene lista. Si no, el front no la pide.

[1:43:46] En el campo de tipo de lista hay dos opciones:
- **A** (ayuda): se puede poner un valor de la lista o cualquier otro.
- **S**: solo se pueden poner valores de la lista.

Se guarda: así el front sabe que hay una lista asociada. [1:44:16] Ahora sí aparece la lista y se puede guardar.

### 18. Edición, pre-update, borrado y tarea para la próxima (1:44:36 – 1:47:23)
[1:44:36] Después hay que ver qué se hace en la edición. Antes del update hay un pre-update donde se pueden verificar cosas, por ejemplo mirar en una tabla para permitir o no la operación, o llenar datos ("si pongo una A acá, pongo una J en otro campo"). Todo eso se maneja desde atrás. Hoy se llegó hasta la edición.

[1:45:04] Tarea: con esta tabla, hacer todas las listas de valores. Una lista puede ser solo para editar y otra distinta para dar de alta un registro; eso se indica en la definición y puede variar según se quiera. [1:45:32] Hay que agregarle a todos los campos sus listas y definir la edición mirando en el Forms qué se puede modificar y qué no.

> **Regla:** [1:45:32] En la edición no se puede editar el código (el primer campo).

[1:45:56] Borrado: en principio no se va a habilitar ahora. Podría habilitarse para algún permiso especial.

> **Caso especial:** [1:45:56] Un origen que ya existe no se puede borrar si ya generó un ingreso con ese origen. Se controla con un trigger de base de datos o con una validación propia: [1:46:24] antes de borrar se verifica si existe en tal tabla, y si existe se informa que no se puede borrar.

[1:46:24] La parte de listas quedó a medias, pero hay una plantilla para generar las distintas listas. Esta tabla tiene 4 o 5 listas de valores; sería bueno que las hagan los 3 juntos [1:46:52] para mecanizarlo. Se carga en 3 lugares: armar el query, asignar lo que ve el usuario y asignar valor→campo (normalmente dos pares; hay casos con más). [1:47:23] Para la próxima, con todo esto armado, se ve el insert (qué se inserta cuando hay algo nuevo).

### 19. Paso 5: operatoria auxiliar (tablas padre/hija) (1:47:23 – 1:49:10)
[1:47:23] Pregunta sobre el paso 5: en este caso no se usaría porque no hay operatoria auxiliar. [1:47:52] El paso 5 sirve si la tabla, además de tener su propio ABM, es hija de otra. Ahí hay que saber quién es el padre y cómo se relaciona con él, y aparece la operatoria auxiliar.

> **Regla:** [1:48:17] Cuando en la parte operatoria aparece una operatoria auxiliar, quiere decir que la tabla se define como hija de otra (la parte de abajo de otra).

[1:48:17] Esta tabla no tiene padre. Más adelante se va a hacer alguna con padre. Ejemplo: tipo de movimiento, con varias hijas debajo (como las monedas por cuenta; eran unas 3 hijas). [1:48:43] Se puede generar el ABM de una tabla y en algún momento definir que es hija de otra: eso es el punto 5 (padre-hijos). Todavía no se va a ver.

### 20. Pase de desa a test y a prod: script de migración de la parametrización (1:49:10 – 1:53:51)
[1:49:10] Pregunta: una vez desarrollado todo, ¿cómo se pasa a otro ambiente? Correr de nuevo el proceso genérico no alcanza: hay que llevar el paquete y todos los datos cargados en las tablas de parametrización. Hay un paquete que se llama "pases_gen" [?] ("actualizaciones gen completar datos"). [1:49:38] Tiene un procedimiento que arma el script con el insert de todos los datos de las tablas, en orden, y lo deja en un archivo TXT del sistema, igual que cuando se genera el paquete. Se le pasa la clave y genera el script que hay que mandar para el pase.

[1:50:05] Ese script tiene el insert de todos los datos de todas las tablas, y hay que mandarlo junto con el paquete. Son muchas tablas. [1:50:34] La función se busca en el paquete `pases_gen` [?] ("general script migración, actualización"), al final de la especificación. [1:51:02] Se ejecuta con la clave. El grupo no va porque se usa uno por defecto; van el ID y la agrupación. Genera un archivo TXT con todos los inserts de las tablas.

> **Regla:** [1:51:02] Flujo de ambientes: se carga en desa y se pasa a test. Cuando está en test, se genera desde test el script por clave.

[1:51:28] Antes el instructor lo hacía a mano. El proceso genérico abarca muchas tablas (el proceso, los campos, los permisos, las operatorias, las validaciones…). En principio no debería haber problemas; si hace falta algún ajuste, se hace.

> **Regla:** [1:51:57] Para el pase se generan 3 cosas: el script de la parametrización (se corre el proceso, se baja el script y se deja en "paquetes a pasar"), el paquete y el type. Sin eso no se puede replicar.

[1:52:28] Motivo de generarlo desde test: en desa se carga todo y se pasa a test. En test el usuario puede modificar cosas de nivel tabla que no afectan la programación (qué ve, qué no, cómo va…) y dar el OK. [1:52:56] Al pasar a prod hay que llevar lo que está en test de las tablas de parametrización: qué se navega, qué se ve, si se generó un grupo nuevo, etc. Ellos van a tener que hacer una tarea para el pase a producción.

> **Regla:** [1:53:24] Hay parametrizaciones que puede hacer el usuario en test sin afectar la programación. Por eso, para pasar a prod hay que regenerar desde test el script de inserts de las tablas de parametrización.

[1:52:56] Próxima clase: con las listas de valores hechas, se profundiza en cómo armar la edición y el insert con grupos (un título con un conjunto de campos, otro título con otro conjunto), algo que también pueden trabajar los usuarios. [1:53:51] Cierre: quedaron muchas cosas más claras.

## Términos detectados
| Término | Variante en el audio | Qué significa según el video | Timestamp |
|---|---|---|---|
| `?XT_ORIGEN_RECAUDO` [?] | "Pex t origen recaudos", "Pecs t origen recaudo", "BPX origen recaudo" | Tabla que se está migrando en la sesión | 0:58, 12:33, 14:54 |
| PXOR2 [?] | "pexo r dos", "P Xo R dos", "P X O R P X_ dos", "pcor dos", "P chor dos", "PX 2" | Clave de la definición de la tabla en el proceso genérico (probable sigla de PXT_ORIGEN_RECAUDO) | 10:14, 11:02, 30:01, 31:01, 1:21:52 |
| Forms | "Font", "fon", "fonk", "Fom", "from", "Front", "Ford", "phone", "forma" | Pantalla vieja de Oracle Forms | passim |
| LOV (lista de valores) | "Love", "Lob", "logo esquema" | Lista de valores de Forms; en un ítem descriptivo se define en el campo anterior (código) | 2:47, 3:14, 6:02 |
| Column Mapping | "Column Mapy" | Propiedad de la LOV que mapea columna→campo | 6:02 |
| Record Group (RG) | "record Group", "RG", "recor Grupo" | Query de la LOV; se copia tal cual al query o al paquete | 6:02, 7:52, 8:22 |
| RG_ESQUEMA / LOV_ESQUEMA [?] | "RG esquema", "Love esquema(s)" | Record Group y LOV del campo esquema | 3:14, 6:02, 8:22 |
| post-query | "post Quei", "postcuel", "Post Code" | Trigger de Forms donde se llenan los descriptivos | 6:29, 6:53, 7:52 |
| Red Code / Ref Code | "Red Code", "red codec", "refcode", "refcorde", "red Cow", "red CO" | Tabla de códigos/dominios para campos con valores fijos (en esta charla se refiere sobre todo a Ref Codes, no a Record Group) | 4:41, 8:50, 10:14, 13:31 |
| `CG_REF_CODES` [?] | "CG Red Code", "CG rescover", "CG, REF Code", "CG res code dos" | Nombre de la tabla de Ref Codes; requiere permisos | 13:31, 14:02, 55:57 |
| `RV_MEANING` [?] | "RB maining", "RB main" | Campo de la Ref Code con la descripción | 16:10, 1:32:31 |
| `RV_LOW_VALUE` [?] | "Low valver", "low value", "low vale" | Campo de la Ref Code con el código; se usa en el join y en la LOV | 54:49, 1:32:31 |
| Dominio | "dominio", "Domain", "dos main" | Dominio de la Ref Code usado en el WHERE del join | 53:50, 1:06:19 |
| Sinónimo | "sinónimo" | Nombre alternativo que permite referenciar tablas de otros esquemas; no da acceso | 14:25, 14:54 |
| valsec [?] | "valsec", "conevalse" | Esquema cuyas tablas tienen sinónimo | 14:02, 14:25 |
| Grupo de negocio | "grupo negocio", "grupo de negocio" | Configuración de un campo como link (azul) a otra pantalla, con clave (p. ej. ramo/póliza/certificado) | 17:08–18:54 |
| Case Restriction | "case restriction", "Apple mix", "mix", "Apple", "APP" | Propiedad de formato: MIXED/UPPER para varchar; MONTO/NUMBER para numéricos | 20:49–25:53 |
| MONTO / NUMBER | "monto", "numb", "Amber" [?] | MONTO = decimales o separador de miles; NUMBER = entero sin separadores | 21:43, 22:29 |
| FDQM70000 [?] | "QM 70000", "FDQMEP", "FDQQ", "FDQM" | Pantalla ABM (Forms) de parametrización del proceso genérico | 30:31, 31:01, 39:48 |
| desa | "Endesa" | Ambiente de desarrollo (desa → test → prod) | 52:13, 1:10:02, 1:51:02 |
| prod | "pro", "prop", "Prof" | Ambiente de producción | 1:52:28, 1:53:24 |
| TYPE / list type | "type", "tai", "tripe", "taip", "Altai", "list tail", "lista type" | Type del registro y tipo lista que "simula una tabla"; se consulta con `select * from table(...)` | 44:03, 49:10, 1:08:34 |
| Query / select | "cuello", "cueli", "cuelli", "cueri", "Cell" | Query del paquete o del Forms | passim |
| INTO / WHERE | "intu", "Wear" | Cláusulas SQL | 55:32, 57:41 |
| NO_DATA_FOUND / TOO_MANY_ROWS | "no data funk/Fund", "tu money rock", "to man y rojo" | Excepciones PL/SQL en los bloques de descriptivos | 59:30–1:00:22 |
| Campo query | "campo query", "en cueri" | Indicador de que el campo está en el select del query (permite ordenar y filtrar en base) | 1:16:38–1:20:27 |
| Lista genérica | "lista genérica" | Procedimiento del paquete que despacha la LOV según el nombre del campo | 1:29:43, 1:39:41 |
| LOV ejemplo plantilla | "Love ejemplo plantilla" | Plantilla del paquete para crear una LOV | 1:30:14 |
| Tipo de lista A / S | "la A de … ayuda", "con una s" | A = ayuda (permite otros valores); S = solo valores de la lista | 1:43:46 |
| Operatoria / operatoria auxiliar | "operatoria", "operatorio auxiliar" | Agrupador de vista; la auxiliar define una tabla hija de otra (paso 5) | 1:22:53, 1:47:52 |
| pases_gen [?] | "actualizaciones gen", "actualización gen completar datos", "general script migración" | Paquete/procedimiento que genera el script de inserts de la parametrización para el pase | 1:49:10, 1:50:34 |
| lista pro / desc lista pro | "lista pro", "deslista prod", "DESP lista pro", "Expo" | Campo código de productor y su descripción | 10:43, 1:35:21 |

## Reglas y casos especiales detectados
- [1:21] Dar permisos a la tabla que se migra y a todas sus tablas relacionadas; el script de relación los necesita.
- [4:11] El generador no puede relacionar la misma tabla más de una vez; las demás relaciones se ajustan a mano.
- [4:41] Con varios campos de Red Code, se elige uno solo para la relación automática; en el resto la tabla va null.
- [7:52] Un descriptivo con LOV en Forms puede no llenarse si falta el post-query; hay que ir al Record Group.
- [10:14] Un campo con distintos valores fijos va a la Red Code en lugar de crear una tabla.
- [14:02] Siempre verificar permisos sobre `CG_REF_CODES` [?] al relacionar.
- [14:54] Un sinónimo da referencia, no acceso.
- [16:10] El campo de la Red Code es casi siempre `RV_MEANING` [?]; hay casos especiales: verificar.
- [22:29] Enteros → NUMBER; con decimales → MONTO.
- [22:59] Varchar parte de la PK → UPPER.
- [24:22] Un entero que el usuario quiera con separador de miles → MONTO.
- [35:21] En el sistema nuevo todo es grilla; no se replica el layout del Forms. Las vistas definen qué se ve.
- [50:09] No saltearse campos; generar aunque no se vean en Forms.
- [56:48] Al crear un descriptivo, indicar la tabla y el campo de origen para que se arme el join.
- [1:00:22] Los bloques de descriptivos deberían manejar NO_DATA_FOUND y TOO_MANY_ROWS (dominio más código no es PK).
- [1:04:30] Respetar el orden y no alterar campos en el paquete.
- [1:07:43] Un campo nuevo en la tabla se agrega a mano en el paquete.
- [1:13:36] Los valores se asignan al type campo por campo; si solo se cargan en una variable, no se ven.
- [1:18:28] Marcar "campo query" en los campos que están en el select; llevar al query todo lo posible.
- [1:21:24] Los permisos se pueden ajustar después (inicialmente 000).
- [1:24:22] Caso: usuarios que editan solo 4 o 5 datos → vista restrictiva.
- [1:26:34] Sin permiso de borrado no aparece el botón borrar; sin campos visibles en la edición no hay nada para editar.
- [1:39:15] Una LOV hay que engancharla en lista genérica (IF por nombre de campo).
- [1:43:17] Hay que marcar en la definición del campo que tiene lista (A o S); si no, el front no la pide.
- [1:45:32] En la edición no se puede editar el código.
- [1:45:56] Caso: no se puede borrar un origen que ya generó ingresos (trigger o validación).
- [1:48:17] Una operatoria auxiliar indica una tabla hija (paso 5).
- [1:51:02] Ambientes: desa → test → prod; el script de pase a prod se genera desde test.
- [1:51:57] Para el pase se mandan el script de parametrización, el paquete y el type.

## Pendientes / dudas abiertas
- [0:58] Confirmar el prefijo real de la tabla: `?XT_ORIGEN_RECAUDO` ("Pex t", "Pecs t"; la clave "PXOR2" sugiere PXT).
- [3:14] Confirmar los nombres exactos de la LOV y el Record Group de esquema (LOV_ESQUEMA / RG_ESQUEMA) y del ítem descriptivo (DESP_ESQUEMA [?]).
- [13:31] Confirmar el nombre `CG_REF_CODES` y las columnas `RV_MEANING` / `RV_LOW_VALUE` (lectura del ASR).
- [14:25] Confirmar el nombre del esquema "valsec".
- [19:20] "Orion" [?]: sistema donde ya funciona el link a consulta de póliza.
- [21:43] "van Amber" [?]: probablemente NUMBER; confirmar los valores válidos de Case Restriction.
- [28:17] Confirmar el nombre del campo "ind gen cobranza" [?] y "sigla navegación" [?].
- [38:46] "pantallas de ART" [?]: área con la que se arranca; no definida.
- [42:20] Fragmento poco claro sobre otra tabla con "tabla de origen" vacía.
- [59:05] "LR Move" [?]: variable del paquete por la que se reemplazan las referencias `:campo` del Forms.
- [1:00:22] Agregar el manejo de TOO_MANY_ROWS en los bloques de descriptivos (quedó para después).
- [1:09:04] Descripciones de ingen cobranza y medio de pago que no traían datos: revisar el dominio en desa.
- [1:23:23] "el BI" [?]: definición de la vista.
- [1:27:01] Permiso de insert quedó en 0 por no encontrar el correcto; update con 33 [?]. Definir los permisos reales.
- [1:29:13] Validadores de campos del Forms: tema pendiente para otra clase.
- [1:45:04] Tarea: completar todas las LOV de la tabla (4 o 5) y definir campos editables.
- [1:52:56] Próxima clase: edición e insert con grupos de campos; tarea de pase a producción.
- Nombres mencionados en el audio (sin rol confirmado): Martín (parece ser el instructor), Paula, Gus, Tomás, Dieguito, Inés.

